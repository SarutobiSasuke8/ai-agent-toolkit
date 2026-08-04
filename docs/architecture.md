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
Prompt assembly
  ->
Thread generation by the configured provider
  ->
Thread cleanup and preview output
```

## Providers

`tools/llm.py` supports three backends behind one `ThreadWriter` interface:

| Provider | Transport | Notes |
| --- | --- | --- |
| `openai` | OpenAI Responses API | Best quality, needs credits |
| `ollama` | Local HTTP at `127.0.0.1:11434` | Free, default, weakest output |
| `nous` | OpenAI-compatible chat completions | Hermes models, remote |

The `nous` path deliberately uses chat completions rather than the Responses
API, because the Responses API is specific to OpenAI. That means the same code
path works against any other OpenAI-compatible host by overriding the base URL
with `--base-url` or `NOUS_BASE_URL`.

## Design Choices

### Free search over paid APIs

The project uses Google News RSS because it is free, simple, and good enough
for a first portfolio-grade MVP.

### Clear separation of concerns

- `tools/search.py` handles source retrieval
- `prompts/system_prompts.md` defines writing behaviour
- `agents/news_to_thread_agent.py` orchestrates the workflow
- `tools/llm.py` switches between model providers
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
- Local Ollama quality will usually be weaker than `gpt-4o`
- The agent always searches before generating, rather than deciding to search

## Next Up

Planned work now lives in [roadmap.md](roadmap.md).
