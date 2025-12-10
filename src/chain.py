import streamlit as st
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.prompt import prompt
from src.memory import get_session_history
from src.reranker import get_rerank_retriever


@st.cache_resource
def load_rag_chain(_chat_model): 
    qa_chain = create_stuff_documents_chain(
        llm=_chat_model,
        prompt=prompt
    )

    retriever = get_rerank_retriever()

    rag_chain = create_retrieval_chain(
        retriever,
        qa_chain
    )

    rag_with_memory = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    return rag_with_memory
