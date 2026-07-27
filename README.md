# JARVIS — Local Voice Assistant

A local, privacy-friendly voice assistant inspired by Iron Man's JARVIS. It listens to your voice, transcribes it, generates a response using a local LLM, and speaks the answer back to you — all through a sci-fi styled desktop interface (PyQt6).

## Features

- 🎙️ **Speech-to-text** via [OpenAI Whisper](https://github.com/openai/whisper) (runs locally)
- 🧠 **LLM reasoning** via [Ollama](https://ollama.com) (runs locally, no cloud API)
- 🔊 **Text-to-speech** via [Piper TTS](https://github.com/rhasspy/piper) (runs locally)
- 🖥️ **Graphical interface** built with PyQt6 — an animated orb, live chat log, and typed input

## Project Structure

```
project/
├── main.py                # Entry point
├── ui/
│   ├── __init__.py
│   └── window.py          # PyQt6 GUI (orb animation, chat panel, input bar)
└── core/
    ├── __init__.py
    ├── audio.py            # Microphone recording + Whisper transcription
    ├── brain.py            # Conversation logic (Ollama LLM)
    └── voice.py            # Text-to-speech (Piper)
```

## Requirements

### Python dependencies

Python 3.10+ is recommended. Install the required packages inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # on Linux/macOS
# .venv\Scripts\activate       # on Windows

pip install PyQt6 openai-whisper sounddevice numpy ollama
```

> **Arch/CachyOS users:** if `pip install` refuses to run outside a venv with an "externally-managed-environment" error, always work inside an activated `.venv` as shown above, and use `python -m pip install ...` if the `pip` command doesn't resolve to your venv.

### External tools

**1. Ollama** — must be installed and running locally, with the LLM model pulled:

```bash
# Install Ollama: https://ollama.com/download
ollama pull qwen2.5:3b
```

**2. Piper TTS** — download the prebuilt binary and a voice model:

```bash
# Binary
mkdir -p ~/piper-tts
cd ~/piper-tts
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xvzf piper_linux_x86_64.tar.gz
# The executable will be at ~/piper-tts/piper/piper

# Voice model (choose any voice from https://huggingface.co/rhasspy/piper-voices)
mkdir -p ~/piper-voices
cd ~/piper-voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

**3. System audio tools** — `aplay` (ALSA) must be available to play back generated speech. It's included by default on most Linux distributions (`alsa-utils` package).

## Running the assistant

Every time you open a new terminal:

```bash
cd /path/to/project
source .venv/bin/activate
python main.py
```

The GUI will launch, greet you, and you can either type a message in the input bar or (if wired to the mic) speak to it.

## Configuration

### Change the AI model (LLM)

Edit `core/brain.py`:

```python
reponse = ollama.chat(
    model="qwen2.5:3b",   # ← change to any model you've pulled with Ollama
    ...
)
```

Make sure the new model is available locally first: `ollama pull <model_name>`.

You can also edit the `system` prompt at the top of `core/brain.py` to change JARVIS's personality, tone, or language.

### Change the voice (TTS)

Edit `core/voice.py`:

```python
MODEL_PATH = "/home/ny_san/piper-voices/en_US-lessac-medium.onnx"  # ← path to the .onnx voice file
PIPER_BIN = "/home/ny_san/piper-tts/piper/piper"                    # ← path to the piper executable
```

Any voice from the [Piper voices library](https://huggingface.co/rhasspy/piper-voices) can be used — just download its `.onnx` and `.onnx.json` files and update `MODEL_PATH` accordingly.

### Change the speech-to-text settings

Edit `core/audio.py`:

```python
model = whisper.load_model("base")   # ← try "tiny", "small", "medium", "large" for accuracy/speed tradeoffs

DUREE = 5           # ← recording duration in seconds
SAMPLE_RATE = 16000  # required by Whisper — don't change unless you know what you're doing

result = model.transcribe(audio, language="en")  # ← change "en" to another language code if needed
```

Larger Whisper models are more accurate but slower and use more RAM/VRAM.

## Troubleshooting

| Problem | Likely cause |
|---|---|
| `ModuleNotFoundError: No module named 'PyQt6...'` | Virtual environment not activated — run `source .venv/bin/activate` first |
| `pip install` fails with "externally-managed-environment" | You're not inside an activated venv, or `pip` resolves to the system one — use `python -m pip install ...` |
| `FileNotFoundError` on Piper | `PIPER_BIN` or `MODEL_PATH` in `core/voice.py` don't point to the actual installed locations |
| Voice never changes / always says the same thing | Make sure `voice.py` doesn't use a fragile `shell=True` pipe — pass text via `stdin` instead (see current implementation) |
| No sound at all | Check `aplay` is installed and your audio output device works (`aplay -l` to list devices) |

## Notes

- Everything runs locally: no data is sent to external APIs (aside from the one-time model downloads).
- Ollama and Piper must both be reachable/installed on the machine running the app; there is currently no remote/server mode.