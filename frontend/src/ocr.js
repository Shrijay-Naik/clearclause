// Reads scanned PDFs and photos of documents, in the user's browser.
// The heavy libraries are loaded only when OCR is actually needed.

const MAX_SIDE = 2000; // longest side, in pixels, of the image given to the OCR engine
export const MAX_OCR_PAGES = 15;

export class OcrCancelled extends Error {
  constructor() {
    super("Cancelled");
    this.name = "OcrCancelled";
  }
}

async function loadTools() {
  const [tess, pdfjs, worker] = await Promise.all([
    import("tesseract.js"),
    import("pdfjs-dist"),
    import("pdfjs-dist/build/pdf.worker.min.mjs?url"),
  ]);
  pdfjs.GlobalWorkerOptions.workerSrc = worker.default;
  const createWorker = tess.createWorker || tess.default?.createWorker;
  return { createWorker, pdfjs };
}

async function recognize(worker, canvas) {
  const { data } = await worker.recognize(canvas);
  return (data.text || "").trim();
}

function newCanvas(width, height) {
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.floor(width));
  canvas.height = Math.max(1, Math.floor(height));
  return canvas;
}

function release(canvas) {
  canvas.width = 0; // frees the memory held by the bitmap
  canvas.height = 0;
}

export async function ocrFile(file, onProgress, isCancelled) {
  const isPdf = file.type === "application/pdf" || /\.pdf$/i.test(file.name);

  onProgress({ stage: "loading" });
  const { createWorker, pdfjs } = await loadTools();

  let current = 1;
  let total = 1;
  const report = (fraction) =>
    onProgress({ stage: "reading", page: current, total, fraction });

  const worker = await createWorker("eng", 1, {
    logger: (m) => {
      if (m.status === "recognizing text") report(m.progress);
    },
  });

  const texts = [];
  try {
    if (isPdf) {
      const data = new Uint8Array(await file.arrayBuffer());
      const pdf = await pdfjs.getDocument({ data }).promise;
      total = pdf.numPages;

      if (total > MAX_OCR_PAGES) {
        throw new Error(
          `This scan has ${total} pages. Reading scans on your device supports up to ${MAX_OCR_PAGES} pages, so please split the file.`
        );
      }

      for (let n = 1; n <= total; n++) {
        if (isCancelled()) throw new OcrCancelled();
        current = n;
        report(0);

        const page = await pdf.getPage(n);
        const base = page.getViewport({ scale: 1 });
        const scale = Math.min(
          3,
          Math.max(1, MAX_SIDE / Math.max(base.width, base.height))
        );
        const viewport = page.getViewport({ scale });

        const canvas = newCanvas(viewport.width, viewport.height);
        await page.render({ canvas, viewport }).promise;
        texts.push(await recognize(worker, canvas));

        release(canvas);
        page.cleanup();
      }
      await pdf.destroy();
    } else {
      report(0);
      const bitmap = await createImageBitmap(file);
      const scale = Math.min(1, MAX_SIDE / Math.max(bitmap.width, bitmap.height));
      const canvas = newCanvas(bitmap.width * scale, bitmap.height * scale);
      canvas.getContext("2d").drawImage(bitmap, 0, 0, canvas.width, canvas.height);
      bitmap.close();

      if (isCancelled()) throw new OcrCancelled();
      texts.push(await recognize(worker, canvas));
      release(canvas);
    }
  } finally {
    await worker.terminate();
  }

  if (isCancelled()) throw new OcrCancelled();

  const text = texts.filter(Boolean).join("\n\n").trim();
  if (text.length < 40) {
    throw new Error(
      "No readable text was found. Try a clearer, well-lit scan with the page filling the frame."
    );
  }
  return { text, pages: total };
}