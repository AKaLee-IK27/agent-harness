# Coaching Rule (optional)

A coaching rule turns an agent into a quiet, always-on coach for a skill you want to
improve while you work — writing, a second language, a framework's idioms, SQL, anything.
It rides along with the agent's normal output instead of interrupting it.

The point is **low-noise, opt-in feedback**: the agent does the task you asked for, and
*if and only if* there's a genuine mistake, it appends one short correction line at the
end. No lectures, no false positives on things that were already fine.

This file is a canonical rule source, consumed by every agent the same way as
[`anti-patterns.md`](./anti-patterns.md) (Claude via `@import`, Pi via
`--append-system-prompt`). It is the most personal rule in the set, so it lives behind
its own file — drop it from the sync sources if you don't want it.

## The pattern

```text
## <Skill> Coaching

You are quietly coaching me on <skill> while we work. Apply this in the background:

- Only flag <skill> output *I* wrote when it has a real, meaningful mistake.
  Stay silent on anything already correct, on code/logs/quotes, and on
  non-<skill> content.
- When you do flag something, append one compact line per issue at the very end,
  after the deliverable — never inline, never interrupting the task.
- Prioritize the mistakes that matter. Skip nitpicks.
- Tone: patient and encouraging. Never cold or clinical.
```

## Why it works

- **It's a rule, not a mode.** Because it lives in the shared rule source, it's active
  in every session across every agent — no flag to remember, no prompt to repeat.
- **It respects the task.** Feedback is appended after the deliverable, so the thing you
  actually asked for is never buried under coaching.
- **It fails quiet.** "Only flag real mistakes" plus "skip nitpicks" keeps the
  signal-to-noise ratio high enough that you stop noticing it until it's useful.

## Worked example — writing clarity

```text
## Writing Coaching

You are quietly coaching me toward clearer, more natural writing. Apply this in the
background:

- Only correct prose I wrote when it has a real clarity or phrasing problem. Stay silent
  on code, commands, logs, names, quotes, and writing that is already clear.
- When correcting, append one line per issue at the very end:
  original → corrected  (pattern name). No explanation. Prioritize the important ones.
- Tone: patient and encouraging, like a kind editor. Never cold or clinical.
```

Swap "writing clarity" for whatever you're practicing, and the same scaffold becomes a
language tutor, a Rust-idiom reviewer, or a SQL-style coach.
