"""Example script for running the news-to-thread agent locally.

Run from the project root:
python examples/run_agent.py "AI agents in Web3"
"""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.news_to_thread_agent import NewsToThreadAgent
from tools.formatter import format_thread_preview


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python examples/run_agent.py "AI agents in Web3"')
        raise SystemExit(1)

    topic = " ".join(sys.argv[1:]).strip()

    print(f"Running agent for topic: {topic}")
    print("-" * 60)

    try:
        agent = NewsToThreadAgent(model="gpt-4o")
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
