import os
from langchain_pinecone import PineconeVectorStore
from app.chat.embeddings.openai import embedding_model

vectorstore = PineconeVectorStore(
    index_name=os.environ.get("PINECONE_INDEX_NAME"), embedding=embedding_model
)
