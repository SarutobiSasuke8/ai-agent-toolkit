"""Example script for running the news-to-thread agent locally.

Run from the project root:
python examples/run_agent.py "AI agents in Web3"
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.news_to_thread_agent import NewsToThreadAgent
from tools.formatter import format_thread_preview


def default_model_for_provider(provider: str) -> str:
    """Return a sensible default model for each provider."""
    defaults = {
        "openai": "gpt-4o",
        "ollama": "llama3.2:1b",
    }
    return defaults[provider]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search recent news and turn it into a punchy X thread."
    )
    parser.add_argument("topic", help='Topic to research, for example "AI agents in Web3"')
    parser.add_argument(
        "--provider",
        default="ollama",
        choices=["openai", "ollama"],
        help="Model backend to use. Defaults to ollama so the project can run without API credits.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model override. Example: gpt-4o or llama3.2:3b",
    )
    args = parser.parse_args()

    topic = args.topic.strip()
    model = args.model or default_model_for_provider(args.provider)

    print(f"Running agent for topic: {topic}")
    print(f"Provider: {args.provider}")
    print(f"Model: {model}")
    print("-" * 60)

    try:
        agent = NewsToThreadAgent(provider=args.provider, model=model)
        result = agent.run(topic=topic)
    except Exception as exc:  # noqa: BLE001 - beginner-friendly CLI output
        print(f"Agent failed: {exc}")
        raise SystemExit(1)

    print("Search results used:")
    for index, item in enumerate(result.search_results, start=1):
        print(f"{index}. {item.title} ({item.source}, {item.published})")

    print("\nGenerated X thread:")
    print(format_thread_preview(result.thread_text))


if __name__ == "__main__":
    main()
