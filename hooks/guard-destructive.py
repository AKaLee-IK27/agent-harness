#!/usr/bin/env python3
# guard-destructive.py — PreToolUse guard for destructive/outward git & publish ops.
#
# Keeps a fast "auto-approve" permission mode usable for everyday work, but forces
# an explicit confirmation prompt ("ask") for irreversible or outward-facing
# commands — git push, tag, hard reset, branch delete, package publish, releases,
# PR merges. Mirrors the "implicit-authorization escalation" anti-pattern at the
# harness level, so approval can never silently leak into a destructive action.
#
# Reads a PreToolUse JSON event on stdin. Invoked by guard-destructive.sh.
import json, re, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # never block on parse failure

if data.get("tool_name") != "Bash":
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

# Doc/dry-run invocations are never destructive — let them through.
if re.search(r"(?:--help|--dry-run)\b", cmd):
    sys.exit(0)

# (regex, human label) — matched against the whole command (catches && / ; / | chains)
RULES = [
    (r"\bgit\s+push\b",                      "git push (publishes commits / tags / force)"),
    (r"\bgit\s+reset\s+--hard\b",            "git reset --hard (discards working changes)"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f",         "git clean -f (deletes untracked files)"),
    (r"\bgit\s+tag\s+(-d\b|-[asf]|[^-\s])",  "git tag create/delete"),
    (r"\bgit\s+branch\s+-[dD]\b",            "git branch -d/-D (deletes a branch)"),
    (r"\b(npm|pnpm|yarn)\s+publish\b",       "package publish to a registry"),
    (r"\bgh\s+release\s+create\b",           "gh release create (public release)"),
    (r"\bgh\s+pr\s+merge\b",                 "gh pr merge (merges a PR)"),
]

for pat, label in RULES:
    if re.search(pat, cmd):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    f"Destructive/outward op held for confirmation: {label}. "
                    "Approve only if you explicitly intend this now."
                ),
            }
        }))
        sys.exit(0)

sys.exit(0)
