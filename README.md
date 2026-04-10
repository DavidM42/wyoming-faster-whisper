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

For Intel Arc A-series GPUs use the **transformers** backend with `--device xpu` (or `--device auto` to auto-detect). The `intel_xpu` pip extra is only available on **Linux** (no Windows wheels on PyPI). On Linux, install and run:

```sh
pip install -e ".[transformers,intel_xpu]"
script/run --stt-library transformers --device xpu --model openai/whisper-base --language en --uri 'tcp://0.0.0.0:10300' --data-dir /data --download-dir /data
```

The default faster-whisper backend uses CTranslate2, which does not support Intel GPUs; with `--device xpu` it falls back to CPU and logs a warning.

**Windows with Intel Arc (transformers + XPU):** PyPI has no Windows wheels for `intel-extension-for-pytorch`. Intel provides prebuilt Windows binaries (beta/prototype) on their own index. You must use **torch 2.8.x from Intel’s index** (Intel Extension requires it). Use the version constraint so pip does not install torch 2.10 from PyPI. If you already have torch from PyPI, uninstall it first:

```powershell
# Use a Python version Intel supports (e.g. 3.10, 3.11, 3.12 – not 3.14).
python -m venv .venv
.venv\Scripts\activate
pip uninstall torch intel-extension-for-pytorch -y
pip install "torch>=2.8,<2.9" intel-extension-for-pytorch --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/ --extra-index-url https://pypi.org/simple/
pip install -e ".[transformers]"
# If torch was upgraded to 2.10, run the previous pip install line again.
script/run --stt-library transformers --device xpu --model openai/whisper-base --language en --uri tcp://0.0.0.0:10300 --data-dir . --download-dir .
```

If the Intel index does not have a wheel for your Python version (e.g. 3.14), use one of the alternatives below or WSL2. **Python 3.14:** the transformers extra requires `transformers>=4.54.0` so that the installed `torch` (2.9+ on 3.14) is accepted; `intel-extension-for-pytorch` has no Windows wheel for 3.14 on Intel’s index, so XPU on Windows with 3.14 is not supported.

#### Alternatives on Windows (Intel Arc)

| Option | Idea | Effort |
|--------|------|--------|
| **WSL2** | Run the server inside Ubuntu (or another distro) in WSL2. There you can use `pip install -e ".[transformers,intel_xpu]"` and the Linux wheels. Intel Arc GPU support in WSL2 is still evolving; check [Intel docs](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-arc-gpu-wsl2.html) for driver support. | Use existing stack in WSL2 |
| **DirectML (ONNX)** | Use ONNX Runtime with the [DirectML](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html) execution provider so inference runs on the Intel (or AMD/NVIDIA) GPU on Windows. Would require an ONNX Whisper pipeline and wiring it into this server. | New backend or extend onnx-asr |
| **Vulkan** | Vulkan would give one API for GPU acceleration on both Windows and Linux (Intel Arc, AMD, NVIDIA). ONNX Runtime does **not** ship an official Vulkan EP. Options: use a stack that runs Whisper via Vulkan (e.g. [IREE](https://iree.dev/), or AMD’s [SHARK](https://github.com/nod-ai/SHARK) which can use Vulkan); or a custom ONNX Runtime build with a community Vulkan EP if one exists. | Research / new backend |
| **OpenVINO** | Intel’s OpenVINO supports Intel Arc on Windows. Would mean a new backend that loads a Whisper-style model via OpenVINO and uses the GPU. | New backend, more work |
| **CPU / NVIDIA** | On Windows, use `--device cpu` or `--device cuda` if you have an NVIDIA GPU. No code changes. | None |

## Docker Image

``` sh
docker run -it -p 10300:10300 -v /path/to/local/data:/data rhasspy/wyoming-whisper \
    --model tiny-int8 --language en
```

**NOTE**: Models are downloaded to `/data`, so make sure this points to a Docker volume.

[Source](https://github.com/rhasspy/wyoming-addons/tree/master/whisper)
