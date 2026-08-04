"""LLM provider helpers.

This module keeps model-provider details out of the main agent so the workflow
stays easy to read.

Three providers are supported:

- `openai`: the hosted OpenAI API, using the Responses API
- `ollama`: a local model served by Ollama, free to run
- `nous`: Nous Research models such as Hermes, over their OpenAI-compatible API

The `nous` path is a plain OpenAI-compatible chat-completions call, so the same
code also works for any other OpenAI-compatible host by overriding the base URL.
"""

from __future__ import annotations

from dataclasses import dataclass
import os

from openai import APIStatusError, OpenAI
import requests


OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
NOUS_BASE_URL = "https://inference-api.nousresearch.com/v1"

SUPPORTED_PROVIDERS = ("openai", "ollama", "nous")


@dataclass
class LLMConfig:
    """Configuration for a model provider."""

    provider: str
    model: str
    base_url: str | None = None


class ThreadWriter:
    """Small wrapper around one text-generation provider."""

    def __init__(self, config: LLMConfig, system_prompt: str) -> None:
        self.config = config
        self.system_prompt = system_prompt

        if self.config.provider == "openai":
            self.client = OpenAI(api_key=self._require_key("OPENAI_API_KEY"))
        elif self.config.provider == "nous":
            self.client = OpenAI(
                api_key=self._require_key("NOUS_API_KEY"),
                base_url=self._resolve_base_url(),
            )
        elif self.config.provider == "ollama":
            self.client = None
        else:
            raise ValueError(
                f"Unsupported provider '{self.config.provider}'. "
                f"Use one of: {', '.join(SUPPORTED_PROVIDERS)}."
            )

    def generate(self, prompt: str) -> str:
        """Generate thread text using the configured provider."""
        if self.config.provider == "openai":
            return self._generate_with_openai(prompt)
        if self.config.provider == "nous":
            return self._generate_with_openai_compatible(prompt)
        return self._generate_with_ollama(prompt)

    def _require_key(self, env_var: str) -> str:
        """Read a required API key from the environment."""
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError(
                f"{env_var} is not set. Add it to your environment before "
                f"running the agent in {self.config.provider} mode."
            )
        return api_key

    def _resolve_base_url(self) -> str:
        """Pick the base URL for the OpenAI-compatible provider.

        Order of preference: explicit config, then environment, then the
        documented Nous Research endpoint.
        """
        return self.config.base_url or os.getenv("NOUS_BASE_URL") or NOUS_BASE_URL

    def _generate_with_openai(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.config.model,
            instructions=self.system_prompt,
            input=prompt,
        )
        return response.output_text

    def _generate_with_openai_compatible(self, prompt: str) -> str:
        """Call an OpenAI-compatible chat-completions endpoint.

        The Responses API is specific to OpenAI, so third-party compatible
        hosts such as Nous Research need the older chat-completions shape.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
        except APIStatusError as exc:
            raise ValueError(self._describe_api_error(exc)) from exc

        return response.choices[0].message.content or ""

    def _describe_api_error(self, exc: APIStatusError) -> str:
        """Turn a provider HTTP error into a message a beginner can act on."""
        base_url = self._resolve_base_url()

        if exc.status_code == 401:
            return (
                f"{base_url} rejected the API key. Check that NOUS_API_KEY is "
                "correct and still active."
            )
        if exc.status_code == 404:
            return (
                f"Model '{self.config.model}' was not found at {base_url}. "
                f"List the available model IDs with: "
                f"curl -H \"Authorization: Bearer $NOUS_API_KEY\" {base_url}/models"
            )
        return f"Request to {base_url} failed with status {exc.status_code}: {exc}"

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
