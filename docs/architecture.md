# Architecture

## Purpose

This project turns a topic such as `AI agents in Web3` into a short X thread.

It does that by chaining together three simple layers:

1. search
2. synthesis
3. output formatting

## Flow

```text
User topic
  ->
Google News RSS search
  ->
Structured search results
  ->
OpenAI prompt assembly
  ->
gpt-4o thread generation
  ->
Thread cleanup and preview output
```

## Design Choices

### Free search over paid APIs

The project uses Google News RSS because it is free, simple, and good enough
for a first portfolio-grade MVP.

### Clear separation of concerns

- `tools/search.py` handles source retrieval
- `prompts/system_prompts.md` defines writing behaviour
- `agents/news_to_thread_agent.py` orchestrates the workflow
- `tools/formatter.py` cleans the final output

### Source and synthesis boundary

The search tool gathers raw source context.
The LLM does the synthesis.
The code keeps those responsibilities separate so the workflow stays legible.

## Current Limitations

- Search quality depends on Google News RSS coverage
- The agent does not fetch full article bodies yet
- The tool does not fact-check claims beyond the returned source snippets
- The agent does not post directly to X

## Next Up

- support multiple model providers
- save runs to timestamped output files
- score candidate threads and generate variants
- add tests for search parsing and formatter logic
