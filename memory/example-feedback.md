---
name: example-feedback
description: SYNTHETIC EXAMPLE — illustrates the memory file format. Not a real memory.
metadata:
  type: feedback
---

When a plan is approved, execute it with a fresh subagent per task rather than batching
everything through the current session.

**Why:** Fresh context per task keeps each step focused and makes the review checkpoint
between tasks meaningful.

**How to apply:** Skip the "inline or subagent?" question and go straight to
subagent-driven execution. Fall back to inline only if the user explicitly asks for it.

Related: [[example-user-profile]].
