# 🎬 AI Video Assistant

**Turn videos and meeting recordings into searchable, actionable knowledge.**

AI Video Assistant is a Streamlit application that processes YouTube videos or uploaded audio/video files and uses AI to generate a transcript, a concise summary, meeting action items, and a chat interface for asking questions about the content.

🔗 **GitHub Repository:** [Piyush20032003/AI-Video-Assistant](https://github.com/Piyush20032003/AI-Video-Assistant)

---

## ✨ Features

- **Multiple input options** — analyze a YouTube URL or upload an audio/video file.
- **Automatic transcription** — convert spoken content into text.
- **AI-generated title** — generate a title based on the transcript.
- **Smart summarization** — get a concise overview of long videos or meetings.
- **Action-item extraction** — identify key follow-ups and tasks discussed in the content.
- **Chat with your content** — ask questions about the processed transcript using Retrieval-Augmented Generation (RAG).
- **Interactive Streamlit UI** — analyze content through a browser-based interface with processing status updates.
- **Reset and analyze again** — clear the current result and start a new analysis.

## 🖥️ Application Workflow

```text
YouTube URL / Uploaded Audio or Video
                  |
                  v
       Audio Extraction / Processing
                  |
                  v
             Transcription
                  |
                  v
          Transcript Generated
                  |
          +-------+--------+
          |       |        |
          v       v        v
        Title   Summary  Action Items
                  |
                  v
          Build RAG Chat Index
                  |
                  v
       Ask Questions About the Content
```

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| LangChain | LLM and RAG orchestration |
| `yt-dlp` | YouTube media extraction |
| FFmpeg / audio-processing tools | Audio conversion and preparation |
| Embedding model | Semantic representation of transcript chunks |
| Vector store / retriever | Retrieval of relevant transcript context |
| Language model APIs | Title generation, summarization, insight extraction, and answers |
| `python-dotenv` | Load local environment variables |

The exact models, providers, and vector-store implementation are determined by the project's configuration and dependencies.

## 📁 Project Structure

```text
AI-Video-Assistant/
├── app.py                  # Streamlit user interface and main analysis workflow
├── main.py                 # Main/script workflow
├── test.py                 # Testing and experimentation
├── core/
│   ├── extractor.py        # Extract meeting insights and action items
│   ├── rag_engine.py       # Build the RAG chain and answer questions
│   ├── summarize.py        # Generate titles and summaries
│   └── transcriber.py      # Transcribe processed audio
├── utils/
│   └── audio_processor.py  # Prepare audio/video input for processing
├── requirements.txt        # Python dependencies
├── .gitignore              # Files and folders excluded from Git
└── README.md
```

*Note: The structure above highlights the files and modules used by the application. Check the repository for the latest file list.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Piyush20032003/AI-Video-Assistant.git
cd AI-Video-Assistant
```

### 2. Create a virtual environment

**Windows (Command Prompt):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Use a Python version compatible with the packages in `requirements.txt`.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API credentials

The application loads environment variables with `python-dotenv`. Create a `.env` file in the project root and add the API key or keys required by the model providers configured in your code.

Example format:

```env
PROVIDER_API_KEY=your_api_key_here
```

Replace the example variable with the exact variable name expected by your configured provider. Check the relevant modules and dependency configuration to identify which credentials are required.

**Important:** Never commit `.env` files, API keys, tokens, or other secrets to GitHub. For hosted deployments, configure secrets through the hosting provider's secure settings.

### 5. Install system dependencies

If your audio-processing setup uses FFmpeg, install it for your operating system and ensure the `ffmpeg` executable is available on your `PATH`.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

## 🚀 How to Use

1. Start the application.
2. In the sidebar, select **YouTube URL** or **Upload file**.
3. For a YouTube video, paste its URL. For an upload, choose a supported audio/video file.
4. Click **Analyze** and wait for the processing stages to complete.
5. Review the generated title, transcript, summary, and extracted action items.
6. Use the chat feature to ask questions about the processed content.
7. Use **Reset** when you want to analyze another source.

### Supported upload formats

The current interface accepts these file extensions:

`mp3`, `wav`, `m4a`, `mp4`, `mkv`, `mov`, `webm`, `ogg`

Actual processing support can depend on the installed media tools and environment.

## 🧠 How the RAG Chat Works

Retrieval-Augmented Generation (RAG) helps the assistant answer questions using the processed transcript as context.

1. The video or audio is processed and transcribed.
2. The transcript is passed to the RAG workflow.
3. The content is indexed for retrieval using the configured embedding and vector-store components.
4. When a question is submitted, relevant transcript context is retrieved.
5. The configured language model uses that context to generate an answer.

This allows users to explore specific details without manually searching through an entire recording.

## 🛠️ Troubleshooting

### Streamlit command not found

Make sure your virtual environment is activated, then install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Missing API credentials

Check that your `.env` file is in the project root and that its variable names match the names used in the code. Restart the app after changing environment variables.

### YouTube audio extraction fails

- Confirm that the video is publicly accessible to your environment.
- Update `yt-dlp` if appropriate: `python -m pip install --upgrade yt-dlp`
- Check the error output for JavaScript-runtime, access, or format issues.
- Remember that YouTube extraction behavior may differ between a local machine and a cloud host.

### FFmpeg or audio conversion errors

Install FFmpeg and verify it is available from the terminal:

```bash
ffmpeg -version
```

### Python import or package errors

Activate the correct virtual environment and reinstall the project's requirements. If an installation fails, check the Python version supported by the affected package.

## 🔒 Responsible Use and Security

- Only process content you have permission to access and use.
- Follow the applicable platform terms and copyright rules.
- Do not commit API keys, credentials, or private recordings to the repository.
- Be careful when processing confidential meetings or personal information, particularly when sending transcripts to external AI services.

## 🔮 Potential Future Improvements

- Display transcription progress and processing metrics.
- Improve handling of long recordings and failed processing steps.
- Add transcript download and export options.
- Add source references or timestamps to answers.
- Add caching and persistent storage for repeated analyses.
- Add automated tests and deployment monitoring.

## 👨‍💻 Author

**Piyush Rawat**

- GitHub: [@Piyush20032003](https://github.com/Piyush20032003)
- Project: [AI Video Assistant](https://github.com/Piyush20032003/AI-Video-Assistant)

## 📄 License

No license is specified in this README. Add a `LICENSE` file if you want to define how others may use, modify, and distribute the project.
