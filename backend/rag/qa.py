# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import ChatOpenAI
# from rag.prompts import SYSTEM_PROMPT



# BASE_DIR = Path(__file__).resolve().parent.parent
# VECTOR_DB_PATH = BASE_DIR / "faiss_index"


# def load_db():
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     db = FAISS.load_local(
#         str(VECTOR_DB_PATH),
#         embeddings=embeddings,
#         allow_dangerous_deserialization=True
#     )
#     return db


# def retrieve_context(db, question: str, k: int = 4):
#     docs = db.similarity_search(question, k=k)
#     context = "\n\n---\n\n".join([d.page_content for d in docs])
#     return context, docs


# def answer_question(question: str, k: int = 4, temperature: float = 0.2):
#     db = load_db()
#     context, docs = retrieve_context(db, question, k=k)

#     llm = ChatOpenAI(temperature=temperature)

#     prompt = f"""
# {SYSTEM_PROMPT}

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """

#     response = llm.invoke(prompt)

#     return response.content, docs


from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_PATH = BASE_DIR / "faiss_index"


def load_db():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    return db


def retrieve_context(db, question: str, k: int = 4):
    docs = db.similarity_search(question, k=k)
    return docs


def answer_question(question: str, k: int = 4):
    db = load_db()
    docs = retrieve_context(db, question, k=k)

    if not docs:
        return "❌ No relevant content found in the syllabus.", []

    # MVP Answer: just return the top retrieved chunk
    top_doc = docs[0]
    answer = top_doc.page_content.strip()

    return answer, docs
