
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
import os

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")


def get_llm():
    """Initialize the local Ollama language model."""
    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.2,
        num_predict=1500,
    )


def split_transcript(transcript: str) -> list[str]:
    """Split a long transcript into manageable chunks."""
    if not transcript or not transcript.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=200,
    )

    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    """Summarize a meeting transcript using map-reduce."""

    if not transcript or not transcript.strip():
        return "No transcript provided."

    llm = get_llm()
    chunks = split_transcript(transcript)

    if not chunks:
        return "No transcript provided."

    # Step 1: Summarize each chunk.
    map_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            /no_think
            You are an expert meeting summarizer.

            Summarize the transcript accurately and completely.
            Use complete sentences and meaningful bullet points.

            Extract:
            - Main topics and discussion points
            - Important details, names, numbers, and comparisons
            - Decisions and conclusions
            - Action items and deadlines, if mentioned
            - Unresolved questions and next steps

            Do not invent information.
            Do not return headings without explanations.
            Return a useful summary of the actual transcript.
            """
        ),
        ("human", "Meeting transcript:\n{text}"),
    ])

    map_chain = map_prompt | llm | StrOutputParser()

    partial_summaries = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Generating summary for section {index}/{len(chunks)}...")

        try:
            partial = map_chain.invoke({"text": chunk}).strip()

            if partial:
                partial_summaries.append(partial)
        except Exception as e:
            print(f"Warning: Could not summarize section {index}: {e}")

    if not partial_summaries:
        return "Unable to generate a summary. Please check your Ollama model."

    # Step 2: Combine partial summaries.
    combined = "\n\n".join(partial_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            /no_think
            You are a professional meeting summarization assistant.

            Create a complete, detailed, well-organized meeting summary
            from the supplied partial summaries.

            Follow this structure:

            ## Meeting Overview
            Briefly explain the purpose and subject of the meeting.

            ## Key Discussion Points
            Explain every major topic discussed using complete sentences.
            Preserve important product names, specifications, numbers,
            comparisons, budgets, and other relevant details.

            ## Decisions and Conclusions
            List decisions actually made during the meeting.

            ## Action Items
            List tasks explicitly assigned or agreed upon.

            ## Next Steps
            Include follow-up work or unresolved questions when mentioned.

            Rules:
            - Do not invent facts or decisions.
            - Avoid repetition.
            - Do not produce an outline consisting only of headings.
            - Include enough detail to make the summary useful.
            - Omit sections that have no relevant information.
            - Always provide substantive Key Discussion Points.
            - Return the final summary in Markdown.
            """
        ),
        ("human", "Partial summaries:\n{text}"),
    ])

    final_chain = combined_prompt | llm | StrOutputParser()

    try:
        final_summary = final_chain.invoke(
            {"text": combined}
        ).strip()

        if final_summary:
            return final_summary

    except Exception as e:
        print(f"Warning: Final summary generation failed: {e}")

    # Fallback: Return the partial summaries instead of an empty result.
    return "\n\n".join(partial_summaries)


def generate_title(transcript: str) -> str:
    """Generate a short, professional meeting title."""

    if not transcript or not transcript.strip():
        return "Untitled Meeting"

    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            /no_think
            Generate a concise, professional title for this meeting.
            Use no more than 8 words.
            Return only the title, without quotes or explanation.
            """
        ),
        ("human", "Meeting transcript:\n{text}"),
    ])

    title_chain = title_prompt | llm | StrOutputParser()

    try:
        title = title_chain.invoke({
            "text": transcript[:3000]
        }).strip()

        # Remove common formatting and thinking artifacts.
        title = title.replace("<think>", "").replace("</think>", "").strip()
        title = title.strip("\"'").strip()

        if title:
            return title

    except Exception as e:
        print(f"Warning: Title generation failed: {e}")

    return "Untitled Meeting"
