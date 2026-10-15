"""Tests for agents/news_to_thread_agent.py and the provider guard in tools/llm.py.

Search and the model call are both replaced with stubs, so no network or paid
API is touched.
"""

from __future__ import annotations

import pytest

from agents import news_to_thread_agent as agent_module
from agents.news_to_thread_agent import AgentRunResult, NewsToThreadAgent
from tools.llm import LLMConfig, ThreadWriter
from tools.search import NewsResult


FAKE_RESULTS = [
    NewsResult("Agents raise", "https://a", "Wire", "2025-10-14 09:30 UTC", "Funding news"),
]


def test_build_user_prompt_includes_topic_results_and_rules():
    agent = NewsToThreadAgent(provider="ollama", model="llama3.2:1b")

    prompt = agent._build_user_prompt(topic="DePIN and AI", search_results=FAKE_RESULTS)

    assert prompt.startswith("Topic: DePIN and AI")
    assert "1. Title: Agents raise" in prompt
    assert "Write 5 to 7 posts" in prompt
    assert prompt == prompt.strip()


def test_run_wires_search_and_writer_with_stubs(monkeypatch: pytest.MonkeyPatch):
    search_calls = []
    prompts = []

    def fake_search_news(topic, limit):
        search_calls.append((topic, limit))
        return FAKE_RESULTS

    monkeypatch.setattr(agent_module, "search_news", fake_search_news)

    agent = NewsToThreadAgent(provider="ollama", model="llama3.2:1b")

    def fake_generate(prompt):
        prompts.append(prompt)
        return "  1/ Hook  \n\n\n\n2/ Take  \n"

    monkeypatch.setattr(agent.writer, "generate", fake_generate)

    result = agent.run(topic="AI agents in Web3", result_limit=3)

    assert search_calls == [("AI agents in Web3", 3)]
    assert len(prompts) == 1 and "Topic: AI agents in Web3" in prompts[0]
    assert isinstance(result, AgentRunResult)
    assert result.search_results == FAKE_RESULTS
    assert result.thread_text == "1/ Hook\n\n2/ Take"


def test_agent_loads_system_prompt_from_repo():
    agent = NewsToThreadAgent(provider="ollama", model="llama3.2:1b")

    assert agent.system_prompt.strip()
    assert agent.writer.system_prompt == agent.system_prompt


def test_openai_provider_without_key_raises_clear_error():
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        ThreadWriter(LLMConfig(provider="openai", model="gpt-4o"), system_prompt="x")


def test_unsupported_provider_is_rejected():
    with pytest.raises(ValueError, match="Unsupported provider 'claude'"):
        ThreadWriter(LLMConfig(provider="claude", model="any"), system_prompt="x")
