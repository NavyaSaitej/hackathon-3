import os
import urllib.request
from pathlib import Path

# Paths
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

def pull_ollama_model():
    print("⬇️ Pulling phi3 model via Ollama (~2.4 GB)... This may take a while.")
    import subprocess
    import shutil
    if shutil.which("ollama"):
        subprocess.run(["ollama", "pull", "phi3"])
        print("✅ Successfully pulled phi3")
    else:
        print("⚠️ Ollama is not installed. Run 'winget install Ollama.Ollama' first.")

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
    pull_ollama_model()
    prime_whisper_cache()
    prime_ocr_cache()
    print("\n🎉 All models downloaded! You are now ready to disable Wi-Fi and develop 100% offline.")
