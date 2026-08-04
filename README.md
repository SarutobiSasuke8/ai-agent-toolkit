# ai-agent-toolkit

A beginner-friendly Python project that searches recent Web3 and AI news,
summarizes the signal with either OpenAI or Ollama, and turns it into a punchy
X thread.

This repo is intentionally small, inspectable, and portfolio-friendly.
The goal is to show a real agent workflow, not hide everything inside one prompt.

## Why This Project Exists

Most people stop at "prompt in, output out."

This project goes one step further:

- gather source material with a tool
- route that source material into a model
- shape the output with a defined voice
- keep the workflow readable in code

## What This Does

1. You give the agent a topic such as `AI agents in Web3`
2. It searches recent news using a free Google News RSS search
3. It sends those results to either OpenAI or a local Ollama model
4. It returns a short thread in a Web3 and AI native tone

## Project Structure

```text
ai-agent-toolkit/
├── AGENTS.md
├── AI_AUDIT_LOG.md
├── README.md
├── docs/
│   ├── architecture.md
│   ├── portfolio-positioning.md
│   ├── roadmap.md
│   └── sample-outputs.md
├── agents/
│   └── news_to_thread_agent.py
├── tools/
│   ├── search.py
│   ├── llm.py
│   └── formatter.py
├── prompts/
│   └── system_prompts.md
├── examples/
│   └── run_agent.py
├── .env.example
└── requirements.txt
```

## Architecture

The high-level flow is:

1. accept a topic
2. search recent news with Google News RSS
3. package the results into a prompt
4. ask the configured model to write the thread
5. clean and preview the final output

More detail lives in [docs/architecture.md](docs/architecture.md).
Real example runs live in [docs/sample-outputs.md](docs/sample-outputs.md).

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

### 3. Choose a model backend

You now have two paths:

#### Option A: Free local mode with Ollama

If Ollama is installed, start it and pull a small model:

```powershell
ollama serve
```

In a second PowerShell window:

```powershell
ollama pull llama3.2:1b
```

Then run the agent:

```powershell
python examples/run_agent.py "AI agents in Web3"
```

`ollama` is the default provider now, so you do not need an API key for this mode.

#### Option B: OpenAI mode with `gpt-4o`

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

After running `setx`, open a new PowerShell window before testing the app.

#### Option C: Hermes mode with Nous Research

Nous Research serves their Hermes models over an OpenAI-compatible API, so this
uses the same client with a different base URL.

```powershell
setx NOUS_API_KEY "your_nous_api_key_here"
```

Then run:

```powershell
python examples/run_agent.py "AI agents in Web3" --provider nous --model Hermes-4-70B
```

The base URL defaults to `https://inference-api.nousresearch.com/v1`. Because
this path is plain OpenAI-compatible chat completions, `--base-url` points the
same code at any other compatible host.

Note on model IDs: `Hermes-4-70B` is the default here, but the exact ID strings
were not confirmed against a live Nous account when this was written. Check what
your key can actually reach before assuming the default is right:

```powershell
curl -H "Authorization: Bearer $NOUS_API_KEY" https://inference-api.nousresearch.com/v1/models
```

You can also copy [.env.example](.env.example) as a local reference, but do not
commit secrets.

### 4. Run the agent

```powershell
python examples/run_agent.py "AI agents in Web3"
```

For OpenAI mode:

```powershell
python examples/run_agent.py "AI agents in Web3" --provider openai --model gpt-4o
```

For a specific Ollama model:

```powershell
python examples/run_agent.py "AI agents in Web3" --provider ollama --model llama3.2:1b
```

For Hermes via Nous Research:

```powershell
python examples/run_agent.py "AI agents in Web3" --provider nous --model Hermes-4-70B
```

Hermes weights are also open, so a local Hermes build works through the `ollama`
provider with no extra code:

```powershell
python examples/run_agent.py "AI agents in Web3" --provider ollama --model hermes3
```

## Example Topics

- `AI agents in Web3`
- `crypto AI infrastructure`
- `tokenized AI startups`
- `DePIN and AI`

## Notes

- Search is free and uses Google News RSS, not a paid search API
- The project supports `openai`, local `ollama`, and `nous` providers
- `ollama` is the default so you can run the project without API credits
- This is the local MVP for Phase 1
- The repo keeps raw source gathering separate from LLM synthesis

## Sample Outputs

The repo now includes real generated examples:

- [AI Agents in Web3](examples/sample_outputs/ai-agents-in-web3.md)
- [Crypto AI Infrastructure](examples/sample_outputs/crypto-ai-infrastructure.md)
- [DePIN and AI](examples/sample_outputs/depin-and-ai.md)

These were generated with the free local Ollama path, so they show the project
working end to end without API credits.

## Roadmap

The full plan lives in [docs/roadmap.md](docs/roadmap.md). The next major step
is exposing the search tool as a callable function so the model decides when to
search, instead of always being handed results.

## Build Audit

This repository includes an explicit AI usage log in [AI_AUDIT_LOG.md](AI_AUDIT_LOG.md).

The goal is simple:

- make AI-assisted work visible
- distinguish `Codex` sessions from `Claude Code` sessions
- keep the repo honest as a portfolio project

Repo-level operating guidance for assistants lives in [AGENTS.md](AGENTS.md).
