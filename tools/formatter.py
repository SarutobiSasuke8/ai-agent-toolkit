"""Formatting helpers for thread output."""

from __future__ import annotations

from typing import List


def clean_thread_text(raw_text: str) -> str:
    """Normalize the model output into a clean thread block.

    This keeps the demo output readable in the terminal and easy to copy into X.
    """
    lines = [line.strip() for line in raw_text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines).strip()


def thread_to_posts(thread_text: str) -> List[str]:
    """Split a thread block into individual posts.

    We expect the model to separate posts with blank lines, numbering, or both.
    This parser keeps things simple for the MVP.
    """
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
