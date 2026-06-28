import gc
import json
import platform
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from typing import List

from pydantic import BaseModel, Field

from backend.config import get_settings
from backend.exceptions import MemoryLimitExceededError
from backend.logger import logger


class StructuredNote(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence overview of the provided data.")
    action_items: List[str] = Field(description="List of implicit or explicit tasks identified.")
    key_entities: List[str] = Field(description="People, companies, metrics, or major technical terms mentioned.")


class OllamaOrchestrator:
    @staticmethod
    def is_running() -> bool:
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/", method="HEAD")
            urllib.request.urlopen(req, timeout=2)  # nosec
            return True
        except Exception:
            return False

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("ollama") is not None

    @staticmethod
    def install():
        system = platform.system()
        logger.info(f"Ollama not found. Attempting auto-install for {system}...")
        try:
            if system == "Windows":
                subprocess.run(
                    [
                        "winget",
                        "install",
                        "Ollama.Ollama",
                        "--silent",
                        "--accept-source-agreements",
                        "--accept-package-agreements",
                    ],
                    check=True,
                )
            elif system == "Darwin":
                subprocess.run(["brew", "install", "ollama"], check=True)
            else:
                subprocess.run(
                    ["curl -fsSL https://ollama.com/install.sh | sh"],
                    shell=True,
                    check=True,
                )  # nosec
            logger.success("Ollama installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to auto-install Ollama: {e}")
            raise

    @staticmethod
    def ensure_running(model_name: str):
        if OllamaOrchestrator.is_running():
            return

        if not OllamaOrchestrator.is_installed():
            OllamaOrchestrator.install()

        logger.info("Starting Ollama background process...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for it to come online
        for _ in range(15):
            if OllamaOrchestrator.is_running():
                logger.info(f"Ollama is online. Pulling model '{model_name}' if missing (this may take a while)...")
                try:
                    subprocess.run(["ollama", "pull", model_name], check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    logger.warning(f"Failed to pre-pull {model_name}.")
                return
            time.sleep(1)
        raise ConnectionError("Ollama failed to start within 15 seconds.")


class RuleBasedExtractor:
    @staticmethod
    def extract(text: str) -> dict:
        logger.info("Engaging Offline NLP Heuristics Fallback Engine...")

        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        summary = " ".join(sentences[:3]) + "." if sentences else "No readable text found."

        action_items = []
        action_keywords = [
            r"\bmust\b",
            r"\bshould\b",
            r"\bneed\b",
            r"\bto do\b",
            r"\baction\b",
        ]
        for sentence in sentences:
            if any(re.search(kw, sentence.lower()) for kw in action_keywords):
                action_items.append(sentence)
        if not action_items:
            action_items = ["No explicit action items detected by heuristics."]

        words = re.findall(r"\b[A-Z][a-z]+\b", text)
        entities = list(set([w for w in words if len(w) > 2]))[:5]
        if not entities:
            entities = ["No entities detected."]

        return {
            "summary": summary,
            "action_items": action_items[:5],
            "key_entities": entities,
        }


class LLMExtractor:
    def __init__(self):
        self.settings = get_settings()
        self.model = None

    def extract(self, text: str) -> dict:
        try:
            logger.info(f"Connecting to Ollama for {self.settings.ollama_model} extraction...")
            try:
                import ollama
            except ImportError:
                logger.warning("ollama package not installed. Falling back to NLP heuristics.")
                return RuleBasedExtractor.extract(text)

            try:
                OllamaOrchestrator.ensure_running(self.settings.ollama_model)
            except Exception as e:
                logger.warning(f"Ollama Orchestrator failed: {e}. Falling back to NLP heuristics.")
                return RuleBasedExtractor.extract(text)

            system_prompt = "You are an expert archivist. Extract the requested JSON structure exactly."
            user_prompt = f"Extract structured data from the following text:\n\n{text}"

            logger.info("Calling local Ollama API with strict JSON schema...")

            try:
                response = ollama.chat(
                    model=self.settings.ollama_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    format=StructuredNote.model_json_schema(),
                    options={"num_ctx": 2048},
                )
            except Exception as e:
                if "404" in str(e):
                    logger.warning(
                        f"Ollama model '{self.settings.ollama_model}' not found. "
                        f"Please run 'ollama pull {self.settings.ollama_model}' in your terminal."
                    )
                else:
                    logger.warning(f"Ollama server error: {e}.")
                logger.warning("Falling back to Offline NLP Heuristics.")
                return RuleBasedExtractor.extract(text)

            result_text = response["message"]["content"]
            result_text = result_text.strip()

            logger.success("LLM Extraction via Ollama completed successfully.")
            return json.loads(result_text)

        except Exception as e:
            logger.error("Failed during LLM extraction.")
            raise MemoryLimitExceededError("Failed during LLM inference or JSON parsing") from e
        finally:
            gc.collect()
