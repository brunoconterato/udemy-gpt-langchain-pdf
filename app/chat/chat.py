from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.retrievers import BaseRetriever
from typing import List
from langchain_community.vectorstores import VectorStore
from langchain_core.prompts import MessagesPlaceholder
from langchain import hub

from app.chat.models import ChatArgs
from app.chat.llm.openai import llm
from app.chat.vector_stores.pinecone import vectorstore
from app.web.api import get_messages_by_conversation_id


# @brunoconterato
# doc BaseRetriever:
# https://api.python.langchain.com/en/latest/retrievers/langchain_core.retrievers.BaseRetriever.html#langchain-core-retrievers-baseretriever
#
class FilteredRetriever:
    def __init__(self, vector_store: VectorStore, pdf_id: str):
        self.vector_store = vector_store
        self.pdf_id = pdf_id

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Return the first k documents from the list of documents"""
        return self.vector_store.similarity_search(
            query, filter={"pdf_id": self.pdf_id}
        )


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    print("build_chat chat_args")
    print("conversation_id: ", chat_args.conversation_id)
    print("pdf_id: ", chat_args.pdf_id)
    print("metadata: ", chat_args.metadata)
    print("streaming: ", chat_args.streaming)

    chat_messages = get_messages_by_conversation_id(chat_args.conversation_id)
    print("build_chat() chat_messages: ", chat_messages)

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # TODO: retriever with history
    # retriever = FilteredRetriever(vector_store=vectorstore, pdf_id=chat_args.pdf_id)
    retriever = vectorstore.as_retriever()
    
    # TODO:filter documents

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # system_prompt = (
    #     "You are an assistant for question-answering tasks. "
    #     "Use the following pieces of retrieved context to answer "
    #     "the question. If you don't know the answer, say that you "
    #     "don't know. Use three sentences maximum and keep the "
    #     "answer concise."
    #     "\n\n"
    #     "{context}"
    # )
    # qa_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", system_prompt),
    #         ("human", "{input}"),
    #     ]
    # )

    # @brunoconterato
    #
    # Conversational RAG: https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/#adding-chat-history
    # The create_stuff_documents_chain explaination: https://python.langchain.com/v0.2/docs/tutorials/rag/#built-in-chains
    #
    # The create_stuff_documents_chain is a method to create a chain from the raw documents content
    # Without any processing on them
    # create_stuff_documents_chain exige message placeholder"context"
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # @brunoconterato
    #
    # Conversational RAG: https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/#adding-chat-history
    # The create_retrieval_chain explaination: https://python.langchain.com/v0.2/docs/tutorials/rag/#built-in-chains
    #
    # The create_retrieval_chain adiciona o retrieval de documentos
    # e propaga os documentos recuperados pelo retrieval para a chain,
    # Para que se possa obter uma resposta
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain
