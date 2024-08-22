from langchain_community.vectorstores import FAISS
import faiss

FOLDER_PATH = "faiss_index"


class MyFaissVectorIndex:
    def __init__(self, embedding_model):
        try:
            self._vector_index: FAISS = FAISS.load_local(FOLDER_PATH, embedding_model)
            print("Loaded existing FAISS index")
        except:
            self._vector_index: FAISS = faiss.IndexFlatL2(
                len(embedding_model.embed_query("hello world"))
            )
            print("Created new FAISS index")

    def add_embeddings_and_save(self, embedding_model, documents, pdf_id):
        self._vector_index.add_embeddings(embedding_model, documents, pdf_id)
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
