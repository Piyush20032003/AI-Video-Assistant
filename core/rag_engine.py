import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vector_store import build_vector_store, load_vector_store, get_retriver


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

def get_llm():
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.3,num_predict=500
    )
    return llm

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_rag_chain(transcript:str):

    vector_store = build_vector_store(transcript)
    retriever = get_retriver(vector_store, k=4)
    llm = get_llm()

    prompt = ChatPromptTemplate(
        [
            ("system", """You are an exxpert meeting assistant. Answer the user's question based only on the meeting transcript context provided. If answer is not found say 'I am unable to find this information in the given meeting transcript'. Always be concise and precise. Context from meeting transcript:"
            "{context}"""),
            ("human","{question}")
        ]
    ) 

##Full LCEL Rag Pipeline

    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs),"question": RunnablePassthrough()} | prompt| llm | StrOutputParser()
    )
    return rag_chain

def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriver()
    llm = get_llm()
    prompt = ChatPromptTemplate(
            [
                ("system", """You are an exxpert meeting assistant. Answer the user's question based only on the meeting transcript context provided. If answer is not found say 'I am unable to find this information in the given meeting transcript'. Always be concise, precise and try to answer in least possible words. Context from meeting transcript:"
                "{context}"""),
                ("human","{question}")
            ])
     
    rag_chain = (
            {"context": retriever | RunnableLambda(format_docs),"question": RunnablePassthrough()} | prompt| llm | StrOutputParser()
        )
    return rag_chain

def ask_question(rag_chain, question:str) -> str:
    print(f"Question : {question}")
    answer = rag_chain.invoke(question)
    print(f"answer: {answer}")
    return answer