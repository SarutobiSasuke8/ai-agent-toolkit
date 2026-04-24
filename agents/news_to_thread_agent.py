"""Main agent entry point for turning news into an X thread."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from openai import OpenAI

from tools.formatter import clean_thread_text
from tools.search import NewsResult, format_results_for_prompt, search_news


ROOT_DIR = Path(__file__).resolve().parents[1]
PROMPTS_FILE = ROOT_DIR / "prompts" / "system_prompts.md"


@dataclass
class AgentRunResult:
    """Structured result returned by the agent."""

    topic: str
    search_results: list[NewsResult]
    thread_text: str


class NewsToThreadAgent:
    """Small AI agent that turns fresh news into an X thread."""

    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. Add it to your environment before running the agent."
            )

        self.client = OpenAI(api_key=api_key)
        self.system_prompt = PROMPTS_FILE.read_text(encoding="utf-8")

    def run(self, topic: str, result_limit: int = 6) -> AgentRunResult:
        """Execute the full workflow for one topic."""
        search_results = search_news(topic=topic, limit=result_limit)
        prompt = self._build_user_prompt(topic=topic, search_results=search_results)
        thread_text = self._generate_thread(prompt)

        return AgentRunResult(
            topic=topic,
            search_results=search_results,
            thread_text=thread_text,
        )

    def _build_user_prompt(self, topic: str, search_results: list[NewsResult]) -> str:
        """Build the user prompt sent to OpenAI."""
        formatted_results = format_results_for_prompt(search_results)
        return f"""
Topic: {topic}

Task:
Use the search results below to write an X thread in the requested style.
Pull out the strongest narrative, not just a boring summary.
Focus on why this matters now for Web3, AI, or crypto people.

Search results:
{formatted_results}

Instructions:
- Write 5 to 7 posts
- Keep each post short and punchy
- Separate each post with a blank line
- Start strong
- End with a hook, opinion, or take
- Do not mention that you are an AI
""".strip()

    def _generate_thread(self, prompt: str) -> str:
        """Call OpenAI and clean the final thread output."""
        response = self.client.responses.create(
            model=self.model,
            instructions=self.system_prompt,
            input=prompt,
        )
        return clean_thread_text(response.output_text)
