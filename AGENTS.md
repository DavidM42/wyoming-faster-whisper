# Wyoming Faster Whisper – Agent Context

This repo is a **Wyoming protocol server** for speech-to-text. It receives audio over the Wyoming protocol and returns transcripts (locally via faster-whisper or optional other backends).

## Overview

| Area | Description |
|------|-------------|
| **Purpose** | STT server for Home Assistant / Rhasspy / other Wyoming clients |
| **Language** | Python 3.8+ |
| **Entry point** | `wyoming-faster-whisper` (CLI) → `wyoming_faster_whisper.__main__:run` |
| **Setup** | `script/setup` (venv + pip install -e), optional `--dev`, `--transformers`, `--sherpa` |

## Key Files

- `wyoming_faster_whisper/__main__.py` – CLI, server startup, ModelLoader, Zeroconf
- `wyoming_faster_whisper/dispatch_handler.py` – Event handler: Audio → WAV → Transcriber
- `wyoming_faster_whisper/models.py` – ModelLoader, selection and loading of transcribers
- `wyoming_faster_whisper/const.py` – SttLibrary, Transcriber ABC, constants
- `wyoming_faster_whisper/faster_whisper_handler.py` – faster-whisper implementation
- Optional handlers: `sherpa_handler.py`, `onnx_asr_handler.py`, `transformers_whisper.py`

## Extending

- **New CLI options**: define in `__main__.py` and pass through to `ModelLoader` or the relevant handler.
- **New transcriber**: implement the `Transcriber` interface from `const.py`; register in `ModelLoader` and extend `SttLibrary` if needed.
- Wyoming events: see the `wyoming` package (Describe, Info, AudioChunk, AudioStop, Transcribe, Transcript).

## Tests & Quality

- Tests in `tests/` (pytest, asyncio).
- `script/lint`, `script/format` for linting and formatting.
- mypy, black, isort, pylint, flake8 (see pyproject.toml and setup.cfg).
