# Contributing

## AI Usage Tracking

This repository keeps an explicit audit trail of AI-assisted work.

Before or after each meaningful session:

1. Update [AI_AUDIT_LOG.md](AI_AUDIT_LOG.md)
2. State which tool was used:
   - `Codex`
   - `Claude Code`
   - `Human only`
3. List the files changed in that session
4. Summarize the work in plain English

## Suggested Commit Style

Use commit messages that make the tool visible in history.

Examples:

- `codex: build local MVP for news-to-thread agent`
- `claude: refine prompt wording and output style`
- `human: tighten README and fix typos`

This gives you two layers of auditability:

- commit history
- session log in `AI_AUDIT_LOG.md`
