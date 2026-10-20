
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_meeting_insights
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()


def run_pipeline(source: str) -> dict:
    print("Starting AI Video Assistant...")

    chunks = process_input(source)
    transcript = transcribe_all(chunks=chunks)

    print(f"Raw transcription (first 300 characters): {transcript[:300]}")

    title = generate_title(transcript)
    summary = summarize(transcript)
    action_item = extract_meeting_insights(transcript)
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "rag_chain": rag_chain
    }


if __name__ == "__main__":
    source = input(
        "Enter your YouTube URL or local file path: "
    ).strip()

    result = run_pipeline(source)

    print("=" * 100)
    print(f"Title: {result['title']}")
    print(f"Summary: {result['summary']}")
    print(f"Action Items: {result['action_items']}")

    print("\nChat with your meeting. Type 'exit' to quit.\n")

    rag_chain = result['rag_chain']

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not question:
            continue

        answer = ask_question(rag_chain, question)
        print(f"AI Assistant: {answer}")
