"""Search helpers for finding recent Web3, AI, and crypto news.

This module keeps search separate from the LLM logic so the project is easier
to understand, test, and extend later.
"""

from __future__ import annotations

from dataclasses import dataclass
from email.utils import parsedate_to_datetime
import html
import re
from typing import List
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import requests


GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search"


@dataclass
class NewsResult:
    """A single news search result."""

    title: str
    link: str
    source: str
    published: str
    summary: str


def build_google_news_rss_url(topic: str, limit: int = 6) -> str:
    """Build a Google News RSS search URL for a topic."""
    query = quote_plus(topic)
    return (
        f"{GOOGLE_NEWS_RSS_URL}?q={query}&hl=en-IE&gl=IE&ceid=IE:en"
        f"&num={limit}"
    )


def search_news(topic: str, limit: int = 6, timeout: int = 20) -> List[NewsResult]:
    """Search recent news using the free Google News RSS endpoint.

    We only collect lightweight metadata here:
    title, source, date, link, and short summary text from the feed.
    That is enough for a strong MVP without paying for a search API.
    """

    url = build_google_news_rss_url(topic=topic, limit=limit)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall("./channel/item")

    results: List[NewsResult] = []
    for item in items[:limit]:
        title = _safe_text(item.find("title"))
        link = _safe_text(item.find("link"))
        published = _format_pub_date(_safe_text(item.find("pubDate")))
        source = _safe_text(item.find("source")) or "Unknown source"
        summary = _clean_html_summary(_safe_text(item.find("description")))

        results.append(
            NewsResult(
                title=title,
                link=link,
                source=source,
                published=published,
                summary=summary,
            )
        )

    return results


def format_results_for_prompt(results: List[NewsResult]) -> str:
    """Turn search results into compact prompt-ready text."""
    if not results:
        return "No search results found."

    lines = []
    for index, result in enumerate(results, start=1):
        lines.append(
            (
                f"{index}. Title: {result.title}\n"
                f"Source: {result.source}\n"
                f"Published: {result.published}\n"
                f"Summary: {result.summary}\n"
                f"Link: {result.link}"
            )
        )

    return "\n\n".join(lines)


def _safe_text(element: ET.Element | None) -> str:
    """Return stripped text from an XML element."""
    if element is None or element.text is None:
        return ""
    return element.text.strip()


def _clean_html_summary(summary: str) -> str:
    """Convert RSS HTML snippets into plain text."""
    if not summary:
        return ""

    without_tags = re.sub(r"<[^>]+>", "", summary)
    collapsed = re.sub(r"\s+", " ", without_tags).strip()
    return html.unescape(collapsed)


def _format_pub_date(raw_date: str) -> str:
    """Convert RSS pubDate into a cleaner ISO-like timestamp when possible."""
    if not raw_date:
        return "Unknown date"

    try:
        return parsedate_to_datetime(raw_date).strftime("%Y-%m-%d %H:%M %Z")
    except (TypeError, ValueError, OverflowError):
        return raw_date
