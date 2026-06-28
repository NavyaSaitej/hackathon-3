import gc
import json
from pydantic import BaseModel, Field
from typing import List
from src.config import get_settings
from src.logger import logger
from src.exceptions import MemoryLimitExceededError

class StructuredNote(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence overview of the provided data.")
    action_items: List[str] = Field(description="List of implicit or explicit tasks identified.")
    key_entities: List[str] = Field(description="People, companies, metrics, or major technical terms mentioned.")

class LLMExtractor:
    def __init__(self):
        self.settings = get_settings()
        self.model = None

    def extract(self, text: str) -> dict:
        try:
            logger.info("Initializing llama-cpp-python for Phi-3 SLM Extraction...")
            try:
                from llama_cpp import Llama
            except ImportError:
                logger.error("llama-cpp-python not installed.")
                raise MemoryLimitExceededError("Missing LLM dependency")

            logger.debug(f"Loading GGUF from {self.settings.gguf_model_path}")
            
            # Using very conservative memory settings for CPU Hackathon limits
            self.model = Llama(
                model_path=self.settings.gguf_model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            
            system_prompt = "You are an expert archivist. Extract the requested JSON structure exactly."
            user_prompt = f"Extract structured data from the following text:\n\n{text}"
            
            logger.info("Running CPU inference with strict JSON schema...")
            
            response = self.model.create_chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_object",
                    "schema": StructuredNote.model_json_schema()
                },
                max_tokens=512
            )
            
            result_text = response["choices"][0]["message"]["content"]
            logger.success("LLM Extraction completed successfully.")
            return json.loads(result_text)
            
        except Exception as e:
            logger.exception("Failed during LLM extraction.")
            raise
        finally:
            logger.warning("Enforcing strict Garbage Collection. Purging LLM from memory...")
            if self.model is not None:
                del self.model
                self.model = None
            gc.collect()
