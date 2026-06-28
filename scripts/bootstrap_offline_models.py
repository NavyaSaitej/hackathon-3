import os
import urllib.request
from pathlib import Path

# Paths
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# 1. Phi-3-mini GGUF for llama.cpp (Quantized Q4_K_M for 6GB memory ceiling)
PHI3_URL = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
PHI3_PATH = MODELS_DIR / "Phi-3-mini-4k-instruct-q4.gguf"

# 2. Whisper Model (Base)
# faster-whisper will download this automatically when initialized the first time, 
# but we can explicitly trigger it here so the cache is primed before air-gap.

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
        # Download 'base' model to local cache
        model = WhisperModel("base", device="cpu", compute_type="int8")
        print("✅ faster-whisper cache primed successfully.")
    except ImportError:
        print("⚠️ faster-whisper not installed yet. Run 'pip install -r requirements.txt' first.")

if __name__ == "__main__":
    print("🚀 Bootstrapping Local AI Offline Models...")
    download_file(PHI3_URL, PHI3_PATH)
    prime_whisper_cache()
    print("\n🎉 All models downloaded! You are now ready to disable Wi-Fi and develop 100% offline.")
