import os
import uuid
from typing import Literal

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
from domains import DOMAINS
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


# ---------- Public endpoints ----------

@app.get("/")
def home():
    return {"message": "ClearClause backend is running"}


@app.get("/api/domains")
def list_domains():
    return {"domains": [{"id": d["id"], "name": d["name"]} for d in DOMAINS.values()]}


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
        raise HTTPException(status_code=422, detail="No text found in this PDF.")

    try:
        analysis = analyze_document(result["text"], DOMAINS[domain])
    except Exception as e:
                print("AI error:", e)  # visible in the server logs only
                raise HTTPException(
            status_code=502,
            detail="The AI service is busy or unavailable. Please try again in a moment.",
        )

    doc = models.Document(
        id=uuid.uuid4().hex,
        user_id=user.id,
        filename=file.filename,
        domain=domain,
        pages=result["pages"],
        text=result["text"],
        analysis=analysis,
    )
    db.add(doc)
    db.commit()

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "pages": doc.pages,
        "domain": doc.domain,
        "analysis": doc.analysis,
    }


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


def get_own_document(db: Session, document_id: str, user: models.User) -> models.Document:
    """Finds a document, but only if it belongs to this user."""
    doc = db.get(models.Document, document_id)
    if not doc or doc.user_id != user.id:
        raise HTTPException(status_code=404, detail="Document not found.")
    return doc


@app.get("/api/documents/{document_id}")
def get_document(
    document_id: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_own_document(db, document_id, user)
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "pages": doc.pages,
        "domain": doc.domain,
        "analysis": doc.analysis,
    }


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


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    document_id: str
    question: str
    history: list[Message] = []


@app.post("/api/chat")
def chat(
    req: ChatRequest,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_own_document(db, req.document_id, user)

    try:
        answer = chat_with_document(
            doc.text,
            DOMAINS[doc.domain],
            [m.model_dump() for m in req.history],
            req.question,
        )
    except Exception as e:
                print("AI error:", e)  # visible in the server logs only
                raise HTTPException(
            status_code=502,
            detail="The AI service is busy or unavailable. Please try again in a moment.",
        )

    return {"answer": answer}