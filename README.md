<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:4E9F3D,100:2C5F2D&height=160&section=header&text=agent-harness&fontColor=ffffff&fontSize=46&fontAlignY=36&desc=one%20source%20of%20truth%20for%20a%20fleet%20of%20AI%20coding%20agents&descAlignY=58&descSize=16" alt="agent-harness" />
  <br/>
  <img width="120" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/722.gif" alt="Rowlet" />
  <p>
    <img src="https://img.shields.io/badge/license-MIT-2C5F2D" alt="MIT" />
    <img src="https://img.shields.io/badge/agents-Claude%20Code%20%C2%B7%20Pi-4E9F3D" alt="agents" />
    <img src="https://img.shields.io/badge/built%20with-bash%20%C2%B7%20python-2C5F2D" alt="bash + python" />
  </p>
  <p><b>How I run more than one AI coding agent without letting them drift apart.</b></p>
</div>

---

I don't just *use* AI coding agents — I keep a couple of them (Claude Code and Pi) on the
same page. They share **one source of behavioral rules**, the same **safety rail** in
front of irreversible commands, and the same **typed long-term memory**. Edit a rule once
and every agent picks it up; nothing is configured twice and left to rot.

This repo is the sanitized, documented version of that setup. Private contents — secrets,
real memory, work context — stay on my machine; what's here is how it's wired together and
the pieces that are mine to share.

```
      rules/anti-patterns.md   rules/coaching.md
                  \               /
              scripts/sync-agent-rules.sh
                        │
                        ▼
              AGENTS.shared.md  (generated — never hand-edited)
                  ┌─────┴──────┐
                  ▼            ▼
             Claude Code       Pi
             (@import)   (--append-system-prompt)
                  │
                  ▼
          guard-destructive.py   ← PreToolUse: holds push / publish / reset
                  │
                  ▼
          shared memory  ← MEMORY.md index + typed memory files
```

> A rendered diagram and the full walkthrough live in
> [`docs/architecture.md`](./docs/architecture.md).

## The idea

Run two agents long enough and they drift: you tell one a rule, forget to tell the other,
and a month later they behave differently on the same repo. So the rules live in exactly
**one place** — [`rules/`](./rules/) — and a small script fans them out to each agent
through whatever mechanism it natively supports.

| Layer | What it does | Where |
|-------|--------------|-------|
| **Rules** | 36 cross-agent behavioral guardrails ([adapted from Waza](https://github.com/tw93/Waza)) + an optional coaching rule | [`rules/`](./rules/) |
| **Sync** | Concatenates the rule sources into one generated `AGENTS.shared.md` | [`scripts/sync-agent-rules.sh`](./scripts/sync-agent-rules.sh) |
| **Safety** | A `PreToolUse` hook that holds destructive commands for confirmation | [`hooks/`](./hooks/) |
| **Memory** | Typed, one-fact-per-file long-term memory with a loaded index | [`memory/`](./memory/) |
| **Example** | How Claude imports the rule sources via `CLAUDE.md` | [`examples/`](./examples/) |

Each agent consumes the same source its own way:

| Agent | Mechanism |
|-------|-----------|
| Claude Code | `CLAUDE.md` imports the sources with `@rules/anti-patterns.md` |
| Pi | a shell `pi` wrapper passes the generated file to `--append-system-prompt` |

## The safety rail

A fast auto-approve mode is great — until an agent runs `git push` or `npm publish`
because it read approval of a *draft* as approval of an *action*.
[`hooks/guard-destructive.py`](./hooks/guard-destructive.py) is a `PreToolUse` hook that
inspects every shell command and forces an explicit confirmation for the irreversible,
outward-facing ones — `git push`, `git reset --hard`, `git clean -f`, tag/branch
deletion, package publish, release create, PR merge — while everything else stays fast. It
matches the whole command, so it still catches the dangerous verb buried in a `&&` chain.

That turns rule #19 ("never let draft approval leak into a destructive action") from a
line of prompt text into something the harness enforces and the agent can't argue its way
past.

## Memory

For long-term context I lean on **Claude Code's native file-based memory** — one fact per
file, sorted into four types (`user` / `feedback` / `project` / `reference`), with a single
index loaded each session. What I add is the discipline: keeping it bounded, deduped, and
pruned so it stays useful instead of becoming a dumping ground. The format and a synthetic
example are in [`memory/README.md`](./memory/README.md).

## Built with this setup

A few of my projects shipped while running this harness:

- **[second-brain](https://github.com/AKaLee-IK27/second-brain)** — a React dashboard that
  turns local AI coding-session logs into a navigable knowledge graph: sessions, agents,
  skills, full-text search, backlinks. A UI for making sense of how the agents work.
- **[owlet](https://github.com/AKaLee-IK27/owlet)** — friendly local-LLM tools for macOS;
  a Grammarly-style rewriter popup running entirely on a local Ollama model.
- **[Mogu](https://github.com/AKaLee-IK27/Mogu)** — a minimal SwiftUI front-end for the
  Mole system cleaner, built on editorial design principles.

## Credits

This setup *composes* excellent tools rather than reinventing them. My original work is
the cross-agent rule-sync and the destructive-op guard — **the rule content, the memory
system, and the agents themselves are other people's work**, credited below:

- [Claude Code](https://claude.com/claude-code) — Anthropic's CLI coding agent, and its native file-based memory
- [Pi](https://github.com/earendil-works/pi) — an extensible terminal coding agent by Mario Zechner (part of the earendil-works toolkit)
- [herdr](https://github.com/ogulcancelik/herdr) — terminal-native multi-agent multiplexer (how I run the agents side by side)
- [Waza](https://github.com/tw93/Waza) by [@tw93](https://github.com/tw93) — the engineering-habit skill set that [`rules/anti-patterns.md`](./rules/anti-patterns.md) is adapted from
- [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) — behavioral guidelines for LLM coding

<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:2C5F2D,100:4E9F3D&height=100&section=footer" alt="" />
</div>
