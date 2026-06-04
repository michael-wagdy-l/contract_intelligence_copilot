from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pathlib import Path

load_dotenv()

documents = []
for filepath in Path("legal_kb").rglob("*.txt"):
    text = filepath.read_text(encoding="utf-8")
    documents.append(Document(
        page_content=text,
        metadata={"source": str(filepath)}
    ))

splitter = RecursiveCharacterTextSplitter(
    chunk_size= 500,
    chunk_overlap= 50
)
docs = splitter.split_documents(documents)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vectorDb = Chroma.from_documents(
    documents= docs,
    embedding= embeddings,
    persist_directory= "vector db",
    collection_name="legal_kb"
)


print("legal knowledge base created")