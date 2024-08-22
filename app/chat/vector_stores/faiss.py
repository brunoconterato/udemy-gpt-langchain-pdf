from langchain_community.vectorstores import FAISS

FOLDER_PATH = "faiss_index"

class MyFaissVectorIndex:
    def __init__(self, embedding_model):
        try:
            self._vector_index: FAISS = FAISS.load_local(FOLDER_PATH, embedding_model)
        except:
            self._vector_index: FAISS = None
    def add_embeddings_and_save(self, embedding_model, documents, pdf_id):
        if self._vector_index is None:
            self._vector_index = FAISS.from_documents(documents, embedding_model)
        else:
            self._vector_index.add_embeddings(embedding_model, documents, pdf_id)
        self._save_local(pdf_id)
        
    # @brunoconterato
    # we will not use this method
    # Instead we will use the synchronous version of the method
    # And use celery library to run the task asynchronously
    async def aadd_embeddings_and_save(self, embedding_model, documents, pdf_id):
        if self._vector_index is None:
            self._vector_index = await FAISS.afrom_documents(embedding_model, embedding_model)
        else:
            await self._vector_index.aadd_embeddings(embedding_model, documents, pdf_id)
        self._save_local(pdf_id)

    def _save_local(self, pdf_id):
        self._vector_index.save_local(FOLDER_PATH, pdf_id)