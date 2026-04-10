"""Device detection and selection (CPU, CUDA, Intel XPU)."""

import logging
from importlib.util import find_spec
from typing import Any

_LOGGER = logging.getLogger(__name__)


def _load_intel_extension() -> bool:
    """Load intel_extension_for_pytorch if available. Return True if loaded."""
    if find_spec("intel_extension_for_pytorch") is None:
        return False
    try:
        import intel_extension_for_pytorch  # noqa: F401
        return True
    except (ImportError, OSError) as e:
        _LOGGER.warning(
            "Intel Extension for PyTorch could not be loaded (%s). XPU unavailable.",
            e,
        )
        return False


def get_best_device() -> str:
    """Return best available device: cuda > xpu (Intel Arc) > cpu."""
    try:
        import torch

        if _load_intel_extension():
            pass  # torch.xpu now available if load succeeded

        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch, "xpu", None) is not None and torch.xpu.is_available():
            return "xpu"
    except ImportError:
        pass
    return "cpu"


def get_torch_device(device: str) -> Any:
    """Resolve device string to torch.device (for PyTorch-based backends)."""
    import torch

    if device == "xpu":
        if _load_intel_extension() and getattr(torch, "xpu", None) is not None and torch.xpu.is_available():
            return torch.device("xpu")
        return torch.device("cpu")
    if device == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
