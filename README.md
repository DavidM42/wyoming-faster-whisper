# Wyoming Faster Whisper

[Wyoming protocol](https://github.com/rhasspy/wyoming) server for the [faster-whisper](https://github.com/guillaumekln/faster-whisper/) speech to text system.

## Home Assistant Add-on

[![Show add-on](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=core_whisper)

[Source](https://github.com/home-assistant/addons/tree/master/whisper)

## Local Install

Clone the repository and set up Python virtual environment:

``` sh
git clone https://github.com/rhasspy/wyoming-faster-whisper.git
cd wyoming-faster-whisper
script/setup
```

Run a server anyone can connect to:

```sh
script/run --model tiny-int8 --language en --uri 'tcp://0.0.0.0:10300' --data-dir /data --download-dir /data
```

The `--model` can also be a HuggingFace model like `Systran/faster-distil-whisper-small.en`

**NOTE**: Models are downloaded to the first `--data-dir` directory.

### Intel Arc (and other Intel GPUs)

For Intel Arc A-series GPUs use the **transformers** backend with `--device xpu` (or `--device auto` to auto-detect). Install the optional dependency and run:

```sh
pip install -e ".[transformers,intel_xpu]"
script/run --stt-library transformers --device xpu --model openai/whisper-base --language en --uri 'tcp://0.0.0.0:10300' --data-dir /data --download-dir /data
```

The default faster-whisper backend uses CTranslate2, which does not support Intel GPUs; with `--device xpu` it falls back to CPU and logs a warning.

## Docker Image

``` sh
docker run -it -p 10300:10300 -v /path/to/local/data:/data rhasspy/wyoming-whisper \
    --model tiny-int8 --language en
```

**NOTE**: Models are downloaded to `/data`, so make sure this points to a Docker volume.

[Source](https://github.com/rhasspy/wyoming-addons/tree/master/whisper)
