import logging
from uuid import uuid4
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
import faiss
import os

FOLDER_PATH = os.path.abspath("faiss_index")
print("FOLDER_PATH:", FOLDER_PATH)


class MyFaissVectorIndex:
    def __init__(self, embedding_model):
        try:
            # Try loading the existing index
            self._vector_index: FAISS = FAISS.load_local(FOLDER_PATH, embedding_model)
            logging.info("Loaded existing FAISS index from", FOLDER_PATH)
        except Exception as e:
            logging.error("Error loading existing FAISS index:", e)
            index = faiss.IndexFlatL2(len(embedding_model.embed_query("hello world")))
            logging.info("Created new FAISS index at", FOLDER_PATH)
            self._vector_index = FAISS(
                embedding_function=embedding_model,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

    def add_embeddings_and_save(self, embedding_model, documents, pdf_id):
        # uuids = [str(uuid4()) for _ in range(len(documents))]
        self._vector_index.add_documents(documents)
        self._save_local(pdf_id)

    # @brunoconterato
    # we will not use this method
    # Instead we will use the synchronous version of the method
    # And use celery library to run the task asynchronously
    async def aadd_embeddings_and_save(self, embedding_model, documents, pdf_id):
        await self._vector_index.aadd_embeddings(embedding_model, documents, pdf_id)
        self._save_local(pdf_id)

    def _save_local(self, pdf_id):
        self._vector_index.save_local(FOLDER_PATH, pdf_id)
