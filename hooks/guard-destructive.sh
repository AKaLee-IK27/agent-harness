#!/usr/bin/env bash
# guard-destructive.sh — thin wrapper so settings.json can call bash.
# Real logic is in guard-destructive.py; stdin (PreToolUse JSON) passes straight through.
exec python3 "$(dirname "$0")/guard-destructive.py"
