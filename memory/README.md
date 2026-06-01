# Memory: typed, bounded, indexed

This is [Claude Code's native file-based memory](https://code.claude.com/docs/en/memory)
feature — not something I invented. The format, the four types, the `MEMORY.md` index, and
the pruning rules below are all Claude Code's. This folder documents the feature and the
discipline I run it with; the value I add is *using it well*, not designing it.

Each fact is **one file**; one index file (`MEMORY.md`) lists them. This keeps long-term
context small, searchable, and easy to prune — the opposite of an ever-growing scratchpad.

> The files here are **synthetic examples**. Real memory contents (personal, project, and
> work context) stay local and are never published — only the structure and one example
> live in this repo.

## Anatomy of a memory

Each memory file carries frontmatter plus a short body:

```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary — used to decide relevance during recall>
metadata:
  type: user | feedback | project | reference
---

<the fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related memories with [[their-name]].>
```

## The four types

| Type | Holds | Example |
|------|-------|---------|
| `user` | Who the user is — role, expertise, durable preferences | "Prefers fully local LLM tooling; default to a scripted setup." |
| `feedback` | Guidance on *how the agent should work* — corrections and confirmed approaches, with the why | "For plan execution, default to a fresh subagent per task — skip the choice prompt." |
| `project` | Ongoing work, goals, constraints not derivable from the code or git history | "Migration to the new API must ship behind a flag before June." |
| `reference` | Pointers to external resources — URLs, dashboards, tickets | "Design system tokens live at <internal-wiki-link>." |

## The index

`MEMORY.md` is the one file loaded into context every session — one line per memory,
no content, never the fact itself:

```markdown
- [Execution preference](execution-preference.md) — default to subagent-driven execution
- [User profile](user-profile.md) — local-first LLM workflow, scripted setups
```

## Rules that keep it healthy

- **One fact per file.** If a file starts holding two ideas, split it.
- **Dedupe before writing.** Update the existing file rather than adding a near-duplicate;
  delete memories that turn out to be wrong.
- **Don't store what the repo already records.** Code structure, past fixes, and git
  history are not memories. If asked to "remember" one of those, capture what was
  *non-obvious* about it instead.
- **Absolute dates only.** Convert "next week" to a real date at write time, so the fact
  still means the same thing months later.
- **Recall is background context, not instruction.** A recalled memory reflects what was
  true when written — re-verify any file/flag/path it names against current state before
  acting on it.

## Synthetic example

[`example-feedback.md`](./example-feedback.md) shows one complete memory file. It is
fictional — included only to illustrate the format.
