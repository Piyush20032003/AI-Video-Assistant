import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL","tiny")

_model = None

def load_model():
    global _model
    if _model is None:
        print(f"loading model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model is loaded successfully")
    
    return _model

def transcribe_chunk(chunk_path : str, translate : bool = False) -> str:
    model = load_model()
    task = "translate" if translate else "transcribe"
    result = model.transcribe(chunk_path, task = task)
    return result['text']


def transcribe_all(chunks: list, translate:bool = False) -> str:
    transcript_parts = []

    for i, chunk in enumerate(chunks):
        print(f"transcribing chunk {i+1} ")
        text = transcribe_chunk(chunk, translate= translate)

        transcript_parts.append(text)
    print("Transcription Completed")
    return " ".join(transcript_parts)