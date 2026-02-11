from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_FOLDER = BASE_DIR / "django" / "syllabus"
VECTOR_DB_PATH = BASE_DIR / "faiss_index"

# ✅ OPTIONAL: Force only one PDF to be indexed (recommended for MVP)
TARGET_PDF_NAME = "GCE_A_Level_Chemistry_Syllabus_Cleaned_Structured.pdf"


def ingest_pdfs():
    if not PDF_FOLDER.exists():
        raise FileNotFoundError(f"PDF folder not found: {PDF_FOLDER}")

    # ✅ ONLY index the chemistry syllabus (prevents candlestick being included)
    pdf_path = PDF_FOLDER / TARGET_PDF_NAME
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Target PDF not found: {pdf_path}\n"
            f"Available PDFs: {[p.name for p in PDF_FOLDER.glob('*.pdf')]}"
        )

    # ✅ Delete old FAISS index to avoid mixing old data
    if VECTOR_DB_PATH.exists():
        print("🧹 Deleting old FAISS index:", VECTOR_DB_PATH)
        shutil.rmtree(VECTOR_DB_PATH)

    print(f"📄 Loading: {pdf_path.name}")
    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    print("📄 Pages loaded:", len(docs))

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # ✅ CLEAN chunks (this fixes your tokenizer error)
    clean_chunks = []
    for c in chunks:
        if c.page_content and isinstance(c.page_content, str):
            text = c.page_content.strip()
            if len(text) > 30:
                c.page_content = text
                clean_chunks.append(c)

    chunks = clean_chunks
    print("🧩 Clean chunks:", len(chunks))

    if len(chunks) == 0:
        raise ValueError("No valid text chunks were produced. PDF might be scanned or empty.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(str(VECTOR_DB_PATH))

    print(f"✅ FAISS index created successfully with {len(chunks)} chunks")
    print(f"📁 Saved at: {VECTOR_DB_PATH}")


if __name__ == "__main__":
    ingest_pdfs()
