from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

characters = {
    "walter-white": "static/characters/walter_white.txt",
    "dexter": "static/characters/dexter.txt",
    "thomas-shelby": "static/characters/thomas_shelby.txt",
    "jesse-pinkman": "static/characters/jesse.txt",
    "harvey-specter": "static/characters/harvey.txt",
    "mike-ross": "static/characters/mike_ross.txt",
    "louis-litt": "static/characters/louis_litt.txt",
}

for name, path in characters.items():
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(folder_path="static/faiss_indexes", index_name=name)





