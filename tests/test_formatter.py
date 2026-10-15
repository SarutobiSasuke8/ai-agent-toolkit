"""Tests for tools/formatter.py."""

from __future__ import annotations

from tools.formatter import clean_thread_text, format_thread_preview, thread_to_posts


def test_clean_thread_text_strips_lines_and_collapses_blank_runs():
    raw = "\n\n   1/ First post   \n\n\n\n2/ Second post\n   \n\n"

    assert clean_thread_text(raw) == "1/ First post\n\n2/ Second post"


def test_clean_thread_text_handles_empty_input():
    assert clean_thread_text("") == ""
    assert clean_thread_text("   \n\n  ") == ""


def test_thread_to_posts_splits_numbered_markers_without_blank_lines():
    thread = "1/ Opening hook\n2/ Middle point\ncontinues here\n3/ Closing take"

    assert thread_to_posts(thread) == [
        "1/ Opening hook",
        "2/ Middle point\ncontinues here",
        "3/ Closing take",
    ]


def test_thread_to_posts_falls_back_to_blank_line_chunks():
    thread = "Opening hook\n\nMiddle point\n\n\n\nClosing take"

    assert thread_to_posts(thread) == ["Opening hook", "Middle point", "Closing take"]


def test_thread_to_posts_returns_empty_list_for_blank_text():
    assert thread_to_posts("") == []


def test_format_thread_preview_numbers_each_post():
    preview = format_thread_preview("1/ Alpha\n\n2/ Beta")

    assert preview == "Post 1\n1/ Alpha\n\nPost 2\n2/ Beta"


def test_format_thread_preview_returns_input_when_no_posts():
    assert format_thread_preview("") == ""
