## Actionable Items, decisions and questions
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

def get_llm():
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.3,num_predict=500
    )
    return llm


def build_chain(system_prompt: str):
    llm = get_llm()
    return (RunnablePassthrough() | RunnableLambda(lambda x : {"text" : x}) |
            ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human","{text}"),
            ]) | llm | StrOutputParser()
            )

def extract_action_items(transcript:str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, extract "
        "each action item's task description and owner (who is responsible). "
        "format as a numbered list. If none found say 'No action items found'"
    )
    return chain.invoke(transcript)

def extract_key_decisions(transcript:str) -> str:
    chain = build_chain(
        "From the meeting transcript, extract all key decisions made. "
        "Format as a numbered list. If none are found, say 'No key decisions found'."
    )
    return chain.invoke(transcript)

def extract_questions(transcript:str) -> str:
    chain = build_chain(
        "From the meeting transcript, extract all unresolved questions or topics "
        "that need follow-up. Format as a numbered list. If none are found, "
        "say 'No follow-up questions found'."
    )
    return chain.invoke(transcript)


def extract_meeting_insights(transcript: str) -> str:
    chain = build_chain(
        "Analyze the meeting transcript and return exactly these sections: "
        "Action Items (include task and owner), Key Decisions, and "
        "Unresolved Questions / Follow-ups. Use numbered lists under each "
        "heading. If a section has no findings, say 'None found'."
    )
    return chain.invoke(transcript)