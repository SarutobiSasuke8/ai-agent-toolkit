"""Tests for tools/search.py.

The RSS endpoint is never called: `requests.get` is replaced with a stub that
returns a canned feed.
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse
import xml.etree.ElementTree as ET

import pytest

from tools import search
from tools.search import (
    NewsResult,
    build_google_news_rss_url,
    format_results_for_prompt,
    search_news,
)


SAMPLE_RSS = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Google News</title>
    <item>
      <title>  Agents raise new round  </title>
      <link>https://example.com/one</link>
      <pubDate>Tue, 14 Oct 2025 09:30:00 GMT</pubDate>
      <source url="https://example.com">Example Wire</source>
      <description>&lt;a href="x"&gt;Agents &amp;amp; wallets&lt;/a&gt;   grow   fast</description>
    </item>
    <item>
      <title>Second story</title>
      <link>https://example.com/two</link>
      <pubDate>not a real date</pubDate>
      <description></description>
    </item>
    <item>
      <title>Third story</title>
      <link>https://example.com/three</link>
    </item>
  </channel>
</rss>
"""


class FakeResponse:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def raise_for_status(self) -> None:
        return None


def test_build_google_news_rss_url_encodes_topic_and_limit():
    url = build_google_news_rss_url("AI agents & Web3", limit=4)
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert url.startswith(search.GOOGLE_NEWS_RSS_URL + "?")
    assert params["q"] == ["AI agents & Web3"]
    assert params["num"] == ["4"]
    assert "q=AI+agents+%26+Web3&" in url


def test_clean_html_summary_removes_tags_and_unescapes():
    raw = '<b>Agents</b> &amp; <i>wallets</i>\n   grow'

    assert search._clean_html_summary(raw) == "Agents & wallets grow"
    assert search._clean_html_summary("") == ""


def test_format_pub_date_parses_rfc822_and_keeps_unparseable_values():
    assert search._format_pub_date("Tue, 14 Oct 2025 09:30:00 GMT") == "2025-10-14 09:30 UTC"
    assert search._format_pub_date("yesterday-ish") == "yesterday-ish"
    assert search._format_pub_date("") == "Unknown date"


def test_safe_text_handles_missing_and_empty_elements():
    assert search._safe_text(None) == ""
    assert search._safe_text(ET.fromstring("<title/>")) == ""
    assert search._safe_text(ET.fromstring("<title>  hi  </title>")) == "hi"


def test_search_news_parses_mocked_feed(monkeypatch: pytest.MonkeyPatch):
    calls = []

    def fake_get(url, timeout):
        calls.append((url, timeout))
        return FakeResponse(SAMPLE_RSS)

    monkeypatch.setattr(search.requests, "get", fake_get)

    results = search_news("AI agents", limit=2, timeout=7)

    assert len(calls) == 1
    assert calls[0][1] == 7
    assert len(results) == 2
    first, second = results
    assert first == NewsResult(
        title="Agents raise new round",
        link="https://example.com/one",
        source="Example Wire",
        published="2025-10-14 09:30 UTC",
        summary="Agents & wallets grow fast",
    )
    assert second.source == "Unknown source"
    assert second.published == "not a real date"
    assert second.summary == ""


def test_format_results_for_prompt_numbers_results():
    results = [
        NewsResult("T1", "https://a", "S1", "2025-10-14", "Sum 1"),
        NewsResult("T2", "https://b", "S2", "2025-10-15", "Sum 2"),
    ]

    text = format_results_for_prompt(results)

    assert text.startswith("1. Title: T1\nSource: S1\nPublished: 2025-10-14")
    assert "\n\n2. Title: T2\n" in text
    assert text.endswith("Link: https://b")


def test_format_results_for_prompt_handles_empty_list():
    assert format_results_for_prompt([]) == "No search results found."
