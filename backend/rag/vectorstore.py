from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = "faiss_index"

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return db
