from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


def process_document(file_path: str,username:str):
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
    elif file_ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
        pages = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Please upload a PDF or TXT file.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    persist_directory = f"./chroma_db/{username}"
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )




