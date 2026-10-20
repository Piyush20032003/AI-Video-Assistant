
import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """Download YouTube audio and convert it to WAV."""

    output_path = os.path.join(
        DOWNLOAD_DIR, "%(title)s.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,

        # JavaScript runtime and challenge-solving scripts
        "js_runtimes": {"node": {}},
        "remote_components": {"ejs:github"},

        # Convert downloaded audio to WAV using FFmpeg
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        filename = (
            os.path.splitext(ydl.prepare_filename(info))[0]
            + ".wav"
        )

    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"WAV file not found: {filename}"
        )

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert an audio/video file to mono 16 kHz WAV."""

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    output_path = (
        os.path.splitext(input_path)[0] + "_converted.wav"
    )

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

    return output_path


def chunk_audio(
    wav_path: str,
    chunk_minutes: int = 10
) -> list[str]:
    """Split a WAV file into chunks of the specified duration."""

    if chunk_minutes <= 0:
        raise ValueError("chunk_minutes must be greater than zero")

    if not os.path.isfile(wav_path):
        raise FileNotFoundError(
            f"WAV file not found: {wav_path}"
        )

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{wav_path}_chunk{i}.wav"

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list[str]:
    """Process a YouTube URL or local audio/video file."""

    if not source or not source.strip():
        raise ValueError(
            "Please provide a YouTube URL or file path."
        )

    if source.startswith(("http://", "https://")):
        print("Detected YouTube URL. Downloading audio...")

        wav_path = download_youtube_audio(source)

        # Normalize downloaded audio for Whisper
        normalized_path = (
            os.path.splitext(wav_path)[0] + "_converted.wav"
        )

        audio = AudioSegment.from_file(wav_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(normalized_path, format="wav")

        wav_path = normalized_path

    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")

    chunks = chunk_audio(wav_path, chunk_minutes=10)

    print(f"Audio ready - {len(chunks)} chunk(s) created.")

    return chunks
