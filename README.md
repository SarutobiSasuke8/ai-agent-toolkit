# ai-agent-toolkit

A beginner-friendly Python project that searches recent Web3 and AI news,
summarizes the signal with OpenAI, and turns it into a punchy X thread.

## What This Does

1. You give the agent a topic such as `AI agents in Web3`
2. It searches recent news using a free Google News RSS search
3. It sends those results to OpenAI `gpt-4o`
4. It returns a short thread in a Web3 and AI native tone

## Project Structure

```text
ai-agent-toolkit/
├── README.md
├── agents/
│   └── news_to_thread_agent.py
├── tools/
│   ├── search.py
│   └── formatter.py
├── prompts/
│   └── system_prompts.md
├── examples/
│   └── run_agent.py
└── requirements.txt
```

## Local Setup

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

After running `setx`, open a new PowerShell window before testing the app.

### 4. Run the agent

```powershell
python examples/run_agent.py "AI agents in Web3"
```

## Example Topics

- `AI agents in Web3`
- `crypto AI infrastructure`
- `tokenized AI startups`
- `DePIN and AI`

## Notes

- Search is free and uses Google News RSS, not a paid search API
- The OpenAI call uses `gpt-4o`
- This is the local MVP for Phase 1

## Build Audit

This repository includes an explicit AI usage log in [AI_AUDIT_LOG.md](AI_AUDIT_LOG.md).

The goal is simple:

- make AI-assisted work visible
- distinguish `Codex` sessions from `Claude Code` sessions
- keep the repo honest as a portfolio project
