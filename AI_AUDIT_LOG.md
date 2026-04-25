# AI Audit Log

This file tracks where AI coding tools were used in the project.

## Why This Exists

This repo is intended as a public portfolio project. The log below creates a
simple audit trail showing:

- which assistant was used
- what work it helped with
- which files were changed
- what decisions were made

## Logging Rules

- Add one entry per meaningful work session
- Be specific about what the AI tool did
- List the files affected
- If a human made final edits after AI help, say so

## Entry Template

```text
Date: YYYY-MM-DD
Tool: Codex | Claude Code | Human only
Task: short summary
Files:
- path/to/file.py
- path/to/file.md
Notes:
- what was implemented
- what was reviewed or changed by hand
```

## Session Log

### Entry 001

Date: 2026-04-24
Tool: Codex
Task: Create the initial local MVP for a news-to-thread AI agent.
Files:
- README.md
- requirements.txt
- agents/news_to_thread_agent.py
- tools/search.py
- tools/formatter.py
- prompts/system_prompts.md
- examples/run_agent.py
- .gitignore
- AI_AUDIT_LOG.md
Notes:
- Created the project scaffold and then built the first working local version.
- Added free Google News RSS search plus OpenAI `gpt-4o` thread generation.
- Installed Python 3.12 locally, created `.venv`, and installed dependencies.
- Verified the CLI usage flow and the missing-API-key error path.

### Entry 002

Date: 2026-04-24
Tool: Codex
Task: Polish the repository using operating-system patterns from the Obsidian vault.
Files:
- README.md
- AGENTS.md
- .env.example
- docs/architecture.md
- docs/portfolio-positioning.md
- AI_AUDIT_LOG.md
Notes:
- Used the vault's emphasis on contracts, conventions, and source-versus-synthesis boundaries.
- Added a repo-level operating contract and stronger architecture and positioning docs.
- Kept the changes portfolio-facing rather than copying private vault content into the repo.

### Entry 003

Date: 2026-04-25
Tool: Codex
Task: Add a free local-model fallback using Ollama.
Files:
- agents/news_to_thread_agent.py
- tools/llm.py
- tools/formatter.py
- examples/run_agent.py
- README.md
- docs/architecture.md
- docs/portfolio-positioning.md
- .env.example
- prompts/system_prompts.md
- AI_AUDIT_LOG.md
Notes:
- Refactored the agent to support both `openai` and `ollama` providers.
- Made `ollama` the default path so the project can run without API credits.
- Added setup and run instructions for local Ollama usage.
- Verified a full local Ollama run using the installed `gemma4:latest` model.

### Entry 004

Date: 2026-04-25
Tool: Codex
Task: Add real sample outputs to improve the portfolio story.
Files:
- examples/run_agent.py
- examples/sample_outputs/ai-agents-in-web3.md
- examples/sample_outputs/crypto-ai-infrastructure.md
- examples/sample_outputs/depin-and-ai.md
- docs/sample-outputs.md
- README.md
- AI_AUDIT_LOG.md
Notes:
- Generated real sample outputs with the free local `ollama` path using `llama3.2:1b`.
- Fixed a Windows console encoding issue in the example runner while producing samples.
- Added a sample-output index page and linked it from the README.
