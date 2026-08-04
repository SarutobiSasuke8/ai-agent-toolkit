"""Main agent entry point for turning news into an X thread."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.formatter import clean_thread_text
from tools.llm import LLMConfig, ThreadWriter
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

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o",
        base_url: str | None = None,
    ) -> None:
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self.system_prompt = PROMPTS_FILE.read_text(encoding="utf-8")
        self.writer = ThreadWriter(
            config=LLMConfig(
                provider=self.provider,
                model=self.model,
                base_url=self.base_url,
            ),
            system_prompt=self.system_prompt,
        )

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
- Label each post as 1/, 2/, 3/ and so on
- Separate each post with a blank line
- Start strong
- End with a hook, opinion, or take
- Do not mention that you are an AI
""".strip()

    def _generate_thread(self, prompt: str) -> str:
        """Call the configured provider and clean the final thread output."""
        return clean_thread_text(self.writer.generate(prompt))
