"""LLM provider helpers.

This module keeps model-provider details out of the main agent so the workflow
stays easy to read.
"""

from __future__ import annotations

from dataclasses import dataclass
import os

from openai import OpenAI
import requests


OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"


@dataclass
class LLMConfig:
    """Configuration for a model provider."""

    provider: str
    model: str


class ThreadWriter:
    """Small wrapper around one text-generation provider."""

    def __init__(self, config: LLMConfig, system_prompt: str) -> None:
        self.config = config
        self.system_prompt = system_prompt

        if self.config.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY is not set. Add it to your environment before "
                    "running the agent in openai mode."
                )
            self.client = OpenAI(api_key=api_key)
        elif self.config.provider == "ollama":
            self.client = None
        else:
            raise ValueError(
                f"Unsupported provider '{self.config.provider}'. "
                "Use 'openai' or 'ollama'."
            )

    def generate(self, prompt: str) -> str:
        """Generate thread text using the configured provider."""
        if self.config.provider == "openai":
            return self._generate_with_openai(prompt)
        return self._generate_with_ollama(prompt)

    def _generate_with_openai(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.config.model,
            instructions=self.system_prompt,
            input=prompt,
        )
        return response.output_text

    def _generate_with_ollama(self, prompt: str) -> str:
        payload = {
            "model": self.config.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        }

        try:
            response = requests.post(
                OLLAMA_CHAT_URL,
                json=payload,
                timeout=(5, 600),
            )
        except requests.exceptions.ConnectTimeout as exc:
            raise ValueError(
                "Could not reach Ollama at http://127.0.0.1:11434. Start Ollama "
                "first, then try again."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise ValueError(
                "Could not reach Ollama at http://127.0.0.1:11434. Start Ollama "
                "first, then try again."
            ) from exc
        except requests.exceptions.ReadTimeout as exc:
            raise ValueError(
                f"Ollama model '{self.config.model}' took too long to respond. "
                "Try a smaller model such as 'llama3.2:1b' or wait longer."
            ) from exc
        except requests.RequestException as exc:
            raise ValueError(f"Ollama request failed: {exc}") from exc

        if response.status_code == 404:
            raise ValueError(
                f"Ollama model '{self.config.model}' was not found. "
                f"Run: ollama pull {self.config.model}"
            )

        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
