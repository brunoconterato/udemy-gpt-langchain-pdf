import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

from app.chat.embeddings.openai import embedding_model
from app.chat.vector_stores.pinecone import vectorstore

# Explicitly specify the path to the .env file if it's not in the same directory
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
)
print("dotenv_path: ", dotenv_path)
# Load the .env file
if load_dotenv(dotenv_path):
    print("Environment variables loaded successfully.")
else:
    print("Failed to load .env file.")


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    """
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf')
    """
    print("PDF ID: ", pdf_id)
    # 1. Extract text from the specified PDF.
    loader = PyPDFLoader(pdf_path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100, length_function=len
    )

    # 2. Divide the extracted text into manageable chunks.
    documents = loader.load_and_split(splitter)
    for doc in documents:
        doc.metadata = {
            "page": doc.metadata["page"],
            "text": doc.page_content,
            "pdf_id": pdf_id,
        }

    # 3. Generate an embedding for each chunk.
    # 4. Persist the generated embeddings.
    vectorstore.add_documents(
        documents=documents,
        pdf_id=[f"{pdf_id}_{i}" for i in range(len(documents))],
    )
