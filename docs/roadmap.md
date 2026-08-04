# Roadmap

This file tracks where the project is going. It replaces the ad hoc "Next Up"
and "Stronger Future Versions" lists that used to live in
[architecture.md](architecture.md) and
[portfolio-positioning.md](portfolio-positioning.md).

Each item should map to one of the jobs listed in `AGENTS.md`: search quality,
synthesis quality, thread quality, developer clarity, or portfolio credibility.

## Done

- Google News RSS search layer
- OpenAI provider using the Responses API
- Free local provider using Ollama
- Real sample outputs committed to the repo
- Multi-provider support, including Nous Research Hermes models over an
  OpenAI-compatible endpoint

## Next

### 1. Confirm Hermes model IDs against a live account

The provider path is implemented and the base URL is documented, but the exact
model ID strings have not been confirmed against a live Nous Research account.
`Hermes-4-70B` is the current default. Verify with `/v1/models` and correct the
default in `examples/run_agent.py` if it is wrong.

### 2. Use Hermes tool calling instead of one-shot generation

The agent currently does a single prompt-in, text-out call. The search step is
hardcoded to always run. Hermes models are trained for structured function
calling, so the natural next step is to expose `search_news` as a tool and let
the model decide when to call it, how many times, and with which query.

That turns this from a fixed pipeline into an actual agent loop, and it is the
single highest-value change left for portfolio credibility.

### 3. Tests for the parsing layers

`tools/search.py` RSS parsing and `tools/formatter.py` thread splitting are both
pure functions with no network dependency. They should have tests.

### 4. Save runs to timestamped output files

Keep a local record of each run so threads can be compared over time.

### 5. Score candidate threads and generate variants

Generate more than one thread per topic and rank them, rather than trusting the
first output.

## Later

- fetch full article bodies instead of relying on RSS summaries
- a scheduled content pipeline
- a small web app for thread generation

## Explicitly Not Doing

- posting directly to X
- fact-checking claims beyond the returned source snippets
