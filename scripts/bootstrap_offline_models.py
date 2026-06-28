import os
import urllib.request
from pathlib import Path

# Paths
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# 1. Phi-3-mini GGUF for llama.cpp
PHI3_URL = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
PHI3_PATH = MODELS_DIR / "Phi-3-mini-4k-instruct-q4.gguf"

def download_file(url: str, dest: Path):
    if dest.exists():
        print(f"✅ {dest.name} already exists. Skipping.")
        return
    print(f"⬇️ Downloading {dest.name} (~2.4 GB)... This may take a while.")
    urllib.request.urlretrieve(url, dest)
    print(f"✅ Successfully downloaded {dest.name}")

def prime_whisper_cache():
    print("⬇️ Priming faster-whisper local cache...")
    try:
        from faster_whisper import WhisperModel
        WhisperModel("base", device="cpu", compute_type="int8")
        print("✅ faster-whisper cache primed.")
    except ImportError:
        print("⚠️ faster-whisper not installed.")

def prime_ocr_cache():
    print("⬇️ Priming RapidOCR ONNX local cache...")
    try:
        from rapidocr_onnxruntime import RapidOCR
        RapidOCR()
        print("✅ RapidOCR cache primed.")
    except ImportError:
        print("⚠️ rapidocr-onnxruntime not installed.")

if __name__ == "__main__":
    print("🚀 Bootstrapping Chronicle.cpp Offline Models...")
    download_file(PHI3_URL, PHI3_PATH)
    prime_whisper_cache()
    prime_ocr_cache()
    print("\n🎉 All models downloaded! You are now ready to disable Wi-Fi and develop 100% offline.")
