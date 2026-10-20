from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import generate_title, summarize
from core.extractor import extract_meeting_insights


def main():
    source = "https://youtu.be/ZJqSym1V99Q"

    chunks = process_input(source)
    transcript = transcribe_all(chunks)

    print("-----------------------------------------------------------------------------------")
    title = generate_title(transcript)
    print(f"Title: {title}")
    print("-----------------------------------------------------------------------------------")
    print(transcript)
    print("-----------------------------------------------------------------------------------")
    print(summarize(transcript))
    print("-----------------------------------------------------------------------------------")
    print(extract_meeting_insights(transcript))


if __name__ == "__main__":
    main()