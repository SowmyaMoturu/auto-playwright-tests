from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def index_repo_code(repo_path):
    from .repo_loader import load_all_files
    documents = load_all_files(repo_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.create_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("vector_repo_index")