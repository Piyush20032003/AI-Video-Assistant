
import yt_dlp
import os
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

FFMPEG_DIR = (
    r"C:\Users\piyus\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.2-full_build\bin"
)

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(
        DOWNLOAD_DIR, "%(title)s.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "ffmpeg_location": FFMPEG_DIR,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = os.path.splitext(
            ydl.prepare_filename(info)
        )[0] + ".wav"

    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"WAV file not found: {filename}"
        )

    return filename

def convert_to_wav(input_path: str) -> str:
    '''Convert any audio/video file to wav format using pydub for whisper AI'''
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16Khz
    audio.export(output_path,format="wav")
    return output_path


def chunk_audio(wav_path : str, chunk_minutes : int = 10) -> list:
    if chunk_minutes <= 0:
        raise ValueError("chunk_minutes must be greater than zero")

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes*60*1000 #multiplying by 60 mins converted in secs and again by 1000 gives us in miliseconds

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start: start+chunk_ms] ##Chunks will be created from 0 to 6000000
        chunk_path = f"{wav_path}_chunk{i}.wav"
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube URL. Downlaoding audio.......")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV.....")
        wav_path = convert_to_wav(source)

    print("chunking audio.....")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunks created.")
    return chunks