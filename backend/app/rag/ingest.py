import os

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")


def ingest_documents():
    # Load PDF files
    pdf_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )

    # Load TXT files
    txt_loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = pdf_loader.load() + txt_loader.load()

    print(f"Loaded {len(documents)} documents")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    # Local embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Store embeddings in ChromaDB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )

    print(f"Ingested {len(chunks)} chunks into Chroma at {PERSIST_DIR}")


if __name__ == "__main__":
    ingest_documents()