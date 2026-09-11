import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "rag",
    "chroma_db"
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings,
)


def retrieve_relevant_chunks(query: str, k: int = 4) -> str:
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "কোনো relevant তথ্য পাওয়া যায়নি।"

    return "\n\n".join(
        [doc.page_content for doc in results]
    )