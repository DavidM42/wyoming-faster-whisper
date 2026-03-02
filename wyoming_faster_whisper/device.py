"""Device detection and selection (CPU, CUDA, Intel XPU)."""

from importlib.util import find_spec
from typing import Any


def get_best_device() -> str:
    """Return best available device: cuda > xpu (Intel Arc) > cpu."""
    try:
        import torch

        # Intel XPU: load intel_extension_for_pytorch so torch.xpu is available
        if find_spec("intel_extension_for_pytorch") is not None:
            import intel_extension_for_pytorch  # noqa: F401

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
        if find_spec("intel_extension_for_pytorch") is not None:
            import intel_extension_for_pytorch  # noqa: F401
        if getattr(torch, "xpu", None) is not None and torch.xpu.is_available():
            return torch.device("xpu")
        return torch.device("cpu")
    if device == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
