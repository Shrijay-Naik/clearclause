import os
import uuid

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from ai_service import analyze_document, chat_with_document
from auth import create_token, get_current_user, hash_password, verify_password
from database import Base, engine, get_db
from domains import DOMAINS, find_glossary
from pdf_utils import extract_text

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ClearClause API")

# Which websites may call this API. In production we set ALLOWED_ORIGINS on Render.
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_SIZE_MB = 10
MAX_TEXT_CHARS = 200_000  # the most text we accept from a scan read in the browser
MAX_CHAT_MESSAGES = 200  # saved messages per document (questions + answers)


# ---------- Helpers ----------

def doc_payload(doc: models.Document) -> dict:
    """The shape of a document as sent to the browser, including the category check."""
    domain = DOMAINS[doc.domain]

    detected = str(doc.analysis.get("detected_domain") or "").strip().lower()
    check = {"matches": True, "detected": None, "detected_name": None}
    if detected in DOMAINS and detected != doc.domain:
        check = {
            "matches": False,
            "detected": detected,
            "detected_name": DOMAINS[detected]["name"],
        }
    elif detected == "other":
        check["matches"] = False

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "pages": doc.pages,
        "domain": doc.domain,
        "analysis": doc.analysis,
        "glossary": find_glossary(doc.text, domain),
        "domain_check": check,
        "messages": [{"role": m.role, "content": m.content} for m in doc.messages],
    }


def get_own_document(db: Session, document_id: str, user: models.User) -> models.Document:
    """Finds a document, but only if it belongs to this user."""
    doc = db.get(models.Document, document_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc


def ai_unavailable() -> HTTPException:
    return HTTPException(
        status_code=502,
        detail="The AI service is busy or unavailable. Please try again in a moment.",
    )


def analyse_and_save(
    db: Session,
    user: models.User,
    text: str,
    pages: int,
    filename: str,
    domain: str,
    ocr: bool = False,
) -> dict:
    """Runs the AI analysis, saves the document, and returns it for the browser."""
    try:
        analysis = analyze_document(text, DOMAINS[domain], DOMAINS, ocr=ocr)
    except Exception as e:
        print("AI error:", e)  # visible in the server logs only
        raise ai_unavailable()

    if ocr:
        analysis["ocr"] = True  # lets the interface warn that the text came from a scan

    doc = models.Document(
        id=uuid.uuid4().hex,
        user_id=user.id,
        filename=filename,
        domain=domain,
        pages=pages,
        text=text,
        analysis=analysis,
    )
    db.add(doc)
    db.commit()
    return doc_payload(doc)


# ---------- Public endpoints ----------

@app.get("/")
def home():
    return {"message": "ClearClause backend is running"}


@app.get("/api/domains")
def list_domains():
    return {
        "domains": [
            {
                "id": d["id"],
                "name": d["name"],
                "description": d["description"],
                "accepts": d["accepts"],
                "disclaimer": d["disclaimer"],
                "upload_warning": d["upload_warning"],
                "features": d["features"],
                "sections": d["sections"],
                "chat_suggestions": d.get("chat_suggestions", []),
            }
            for d in DOMAINS.values()
        ]
    }


# ---------- Accounts ----------

class SignupRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=72)


@app.post("/api/auth/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    email = req.email.strip().lower()

    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Please enter a valid email address.")
    if len(req.password.encode()) > 72:
        raise HTTPException(status_code=422, detail="Password is too long (max 72 characters).")
    if db.scalar(select(models.User).where(models.User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user = models.User(email=email, password_hash=hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_token(user.id),
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email},
    }


@app.post("/api/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # The form field is called "username" by convention, but we put the email in it
    email = form.username.strip().lower()
    user = db.scalar(select(models.User).where(models.User.email == email))

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    return {
        "access_token": create_token(user.id),
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email},
    }


@app.get("/api/me")
def me(user: models.User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}


# ---------- Protected endpoints (login required) ----------

@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    domain: str = Form("finance"),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if domain not in DOMAINS:
        raise HTTPException(status_code=400, detail=f"Unknown domain: {domain}")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    data = await file.read()
    if len(data) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File is larger than {MAX_SIZE_MB} MB.")

    try:
        result = extract_text(data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=422, detail="Could not read this PDF.")

    if not result["text"]:
        # The website sees the word "scan" in this message and offers to read it with OCR
        raise HTTPException(
            status_code=422,
            detail="No selectable text found. This PDF looks like a scan.",
        )

    return analyse_and_save(
        db, user, result["text"], result["pages"], file.filename, domain
    )


class TextAnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT_CHARS)
    filename: str = Field(min_length=1, max_length=255)
    pages: int = Field(ge=1, le=100)
    domain: str = "finance"


@app.post("/api/analyze-text")
def analyze_text(
    req: TextAnalyzeRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyses text that the browser read from a scan or a photo (OCR)."""
    if req.domain not in DOMAINS:
        raise HTTPException(status_code=400, detail=f"Unknown domain: {req.domain}")

    text = req.text.strip()
    if len(text) < 40:
        raise HTTPException(
            status_code=422,
            detail="Could not read enough text from the scan. Try a clearer scan or photo.",
        )

    return analyse_and_save(
        db, user, text, req.pages, req.filename.strip(), req.domain, ocr=True
    )


@app.get("/api/documents")
def list_documents(
    user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    rows = db.scalars(
        select(models.Document)
        .where(models.Document.user_id == user.id)
        .order_by(models.Document.created_at.desc())
    ).all()
    return {
        "documents": [
            {
                "document_id": d.id,
                "filename": d.filename,
                "domain": d.domain,
                "pages": d.pages,
                "document_type": d.analysis.get("document_type"),
                "created_at": d.created_at.isoformat(),
            }
            for d in rows
        ]
    }


@app.get("/api/documents/{document_id}")
def get_document(
    document_id: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return doc_payload(get_own_document(db, document_id, user))


@app.delete("/api/documents/{document_id}")
def delete_document(
    document_id: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_own_document(db, document_id, user)
    db.delete(doc)
    db.commit()
    return {"deleted": True}


class ReanalyzeRequest(BaseModel):
    domain: str


@app.post("/api/documents/{document_id}/reanalyze")
def reanalyze(
    document_id: str,
    req: ReanalyzeRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Re-runs the analysis on the saved text under a different domain."""
    doc = get_own_document(db, document_id, user)

    if req.domain not in DOMAINS:
        raise HTTPException(status_code=400, detail=f"Unknown domain: {req.domain}")

    was_ocr = bool(doc.analysis.get("ocr"))
    try:
        analysis = analyze_document(doc.text, DOMAINS[req.domain], DOMAINS, ocr=was_ocr)
    except Exception as e:
        print("AI error:", e)
        raise ai_unavailable()

    # The person chose this domain explicitly, so their choice wins
    analysis["detected_domain"] = req.domain
    if was_ocr:
        analysis["ocr"] = True

    doc.domain = req.domain
    doc.analysis = analysis
    doc.messages.clear()  # a new domain means a new "expert", so start a fresh chat
    db.commit()

    return doc_payload(doc)


class ChatRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1, max_length=2000)


@app.post("/api/chat")
def chat(
    req: ChatRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_own_document(db, req.document_id, user)

    if not DOMAINS[doc.domain]["features"].get("chat", True):
        raise HTTPException(
            status_code=400, detail="Chat is not available for this type of document."
        )

    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Please type a question.")

    if len(doc.messages) >= MAX_CHAT_MESSAGES:
        raise HTTPException(
            status_code=400,
            detail="This conversation is getting long. Please clear the chat to continue.",
        )

    # The server remembers the conversation, so it works across refreshes and devices
    history = [{"role": m.role, "content": m.content} for m in doc.messages[-6:]]

    try:
        answer = chat_with_document(doc.text, DOMAINS[doc.domain], history, question)
    except Exception as e:
        print("AI error:", e)
        raise ai_unavailable()

    # Saved only after a successful answer, so failed attempts leave nothing behind
    doc.messages.append(models.ChatMessage(role="user", content=question))
    doc.messages.append(models.ChatMessage(role="assistant", content=answer))
    db.commit()

    return {"answer": answer}


@app.delete("/api/documents/{document_id}/messages")
def clear_chat(
    document_id: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_own_document(db, document_id, user)
    doc.messages.clear()
    db.commit()
    return {"cleared": True}