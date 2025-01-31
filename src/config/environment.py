import os
import sys
from pathlib import Path
import torch


def check_gpu_availability():
    """Check if GPU is available and properly configured."""
    try:
        if torch.cuda.is_available():
            torch.tensor([1.0], device='cuda')
            return "cuda"
    except Exception as e:
        print(f"GPU detected but CUDA initialization failed: {e}")
        print("Falling back to CPU...")
    return "cpu"


def check_environment():
    """Check and validate environment variables and dependencies."""
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("Error: HF_TOKEN environment variable not set")
        sys.exit(1)

    device = check_gpu_availability()
    compute_type = "float16" if device == "cuda" else "float32"

    config = {
        "hf_token": hf_token,
        "whisper_model": os.getenv("WHISPER_MODEL", "turbo"),
        "device": device,
        "compute_type": compute_type,
        "output_dir": Path(os.getenv("TRANSCRIBER_OUTPUT", "output")),
    }

    config["output_dir"].mkdir(exist_ok=True)
    return config
