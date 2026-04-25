# AGENTS.md

This file is the operating contract for AI assistants working in this
repository.

## What This Repository Is

`ai-agent-toolkit` is a public portfolio project. Its job is to demonstrate a
small but real AI workflow:

1. search recent Web3, AI, and crypto news
2. preserve the raw source context
3. synthesise the signal with an LLM
4. produce a punchy X thread in a defined voice

This repository is not a dumping ground for prompts or experiments. Every
change should improve one of these jobs:

- search quality
- synthesis quality
- thread quality
- developer clarity
- portfolio credibility

## Source Discipline

- Search results are the source layer.
- Prompt files and generated thread text are the synthesis layer.
- Do not present invented claims as if they came from the search results.
- If the source quality is weak, say so in code comments or docs rather than
  hiding the weakness.

## Audit Discipline

- AI-assisted work must be visible.
- Update `AI_AUDIT_LOG.md` for every meaningful work session.
- Prefer commit prefixes that expose authorship:
  - `codex:`
  - `claude:`
  - `human:`

## Secrets

- Never commit API keys or tokens.
- Use environment variables only.
- Keep `.env` files local and excluded from Git.

## Documentation Standard

- Keep docs direct and specific.
- Avoid inflated marketing language.
- Write as if a technical reviewer will scan the repo in under five minutes.
