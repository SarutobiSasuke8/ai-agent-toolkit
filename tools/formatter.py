"""Formatting helpers for thread output."""

from __future__ import annotations

import re
from typing import List


def clean_thread_text(raw_text: str) -> str:
    """Normalize the model output into a clean thread block.

    This keeps the demo output readable in the terminal and easy to copy into X.
    """
    cleaned_lines = []
    previous_blank = False

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
            continue

        cleaned_lines.append(line)
        previous_blank = False

    return "\n".join(cleaned_lines).strip()


def thread_to_posts(thread_text: str) -> List[str]:
    """Split a thread block into individual posts.

    We expect the model to separate posts with blank lines, numbering, or both.
    This parser keeps things simple for the MVP.
    """
    numbered_posts = _split_numbered_posts(thread_text)
    if numbered_posts:
        return numbered_posts

    chunks = [chunk.strip() for chunk in thread_text.split("\n\n") if chunk.strip()]
    return chunks


def format_thread_preview(thread_text: str) -> str:
    """Return a numbered preview block for terminal output."""
    posts = thread_to_posts(thread_text)
    if not posts:
        return thread_text

    preview_lines = []
    for index, post in enumerate(posts, start=1):
        preview_lines.append(f"Post {index}\n{post}")

    return "\n\n".join(preview_lines)


def _split_numbered_posts(thread_text: str) -> List[str]:
    """Fallback parser for threads that use `1/`, `2/`, `3/` markers."""
    matches = re.findall(r"(?ms)(?:^|\n)(\d+\/.*?)(?=\n\d+\/|\Z)", thread_text.strip())
    return [match.strip() for match in matches if match.strip()]
