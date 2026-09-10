#!/bin/sh
# memory-exit-reminder - the enforcement point for Exit and Checkpoint.
#
# CLAUDE CODE ONLY, AND GIT ONLY. Stop and PreCompact are Claude Code hook events, no other agent
# has them, and this reads `git status`, so outside a work tree it exits 0 and checks nothing. For
# Cursor, Codex or Copilot, and for a memory folder with no version control, the equivalent is the
# instruction in AGENTS.md (or .cursorrules) and nothing enforced - say so plainly rather than
# implying a backstop that is not there.
#
# WHY THIS EXISTS
# AGENTS.md asks the agent to run Exit before saying "done" and to rewrite handoff.md at every
# Checkpoint. Anthropic documents that instruction-file content is "delivered as a user message
# after the system prompt" and that "there's no guarantee of strict compliance", and says that
# anything which must run at a specific point should be a hook, because hooks "apply regardless
# of what Claude decides to do". The prose in AGENTS.md remains the substance: it says what to
# write and where. This script only makes forgetting it visible.
#   Hooks reference: https://code.claude.com/docs/en/hooks
#
# WHAT IT DOES
#   Stop        - if the session changed tracked files outside the memory folder and changed
#                 nothing inside it, exit 2. That blocks the stop and hands the message back to
#                 Claude, which can then write Exit or Checkpoint and stop normally.
#   PreCompact  - if anything is uncommitted, print a reminder that handoff.md is what survives
#                 compaction. Never blocks.
#
# WHAT IT DELIBERATELY DOES NOT DO
#   - It does not write memory. A hook cannot know what was learned; only the agent can.
#   - It does not run on SessionEnd. For that event the output and exit code are ignored, so a
#     SessionEnd hook cannot warn anyone about anything. Registering one would look like a
#     safety net and be nothing.
#   - It does not see work that was already committed. It reads the working tree, so a session
#     that commits code without memory in the same commit passes unnoticed. Catching that needs
#     a SessionStart companion that records HEAD - more moving parts than it is worth here.
#   - It does not block twice: the stop_hook_active guard lets the next stop through, so a
#     disagreement with the agent can never become a loop.
#
# INSTALL
# Copy to .claude/hooks/memory-exit-reminder.sh, chmod +x, and register it in
# .claude/settings.json. Merge these keys into an existing "hooks" block, do not replace it:
#
#   {
#     "hooks": {
#       "Stop": [
#         { "hooks": [ { "type": "command",
#                        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/memory-exit-reminder.sh" } ] }
#       ],
#       "PreCompact": [
#         { "hooks": [ { "type": "command",
#                        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/memory-exit-reminder.sh" } ] }
#       ]
#     }
#   }
#
# Set MEMORY_DIR below to memory if this project keeps its memory there instead of docs.
# POSIX sh and git only. No jq: it is not installed everywhere, and a hook that dies on a missing
# dependency fails silently, which is the one thing an enforcement point must not do.

MEMORY_DIR="docs"

INPUT=$(cat 2>/dev/null)

# Claude Code overrides a Stop hook that blocks repeatedly; it sets stop_hook_active once a hook
# has already continued the conversation. Honour it or risk looping until the cap.
case "$INPUT" in
  *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;;
esac

EVENT=$(printf '%s' "$INPUT" | sed -n 's/.*"hook_event_name"[[:space:]]*:[[:space:]]*"\([A-Za-z]*\)".*/\1/p')

# Outside a work tree there is nothing to compare; stay silent rather than guess.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

CHANGED=$(git status --porcelain --untracked-files=all 2>/dev/null | cut -c4-)
[ -z "$CHANGED" ] && exit 0

IN_MEM=$(printf '%s\n' "$CHANGED" | grep -c "^$MEMORY_DIR/")
OUT_MEM=$(printf '%s\n' "$CHANGED" | grep -vc "^$MEMORY_DIR/")
[ -z "$IN_MEM" ] && IN_MEM=0
[ -z "$OUT_MEM" ] && OUT_MEM=0

if [ "$EVENT" = "PreCompact" ]; then
  echo "Checkpoint: this context is about to be compacted. $MEMORY_DIR/handoff.md is what survives it." >&2
  echo "If a task is in flight, rewrite handoff.md now: task verbatim, done, not done, next single action, numbers with sources." >&2
  exit 0
fi

if [ "$OUT_MEM" -gt 0 ] && [ "$IN_MEM" -eq 0 ]; then
  echo "Exit was not run. This session changed $OUT_MEM tracked file(s) and nothing in $MEMORY_DIR/." >&2
  echo "Before stopping, do one of these:" >&2
  echo "  - task finished  -> run Exit from AGENTS.md: traps.md, tooling.md, decisions.md, tasks.md, then report." >&2
  echo "  - task in flight -> rewrite $MEMORY_DIR/handoff.md (Checkpoint)." >&2
  echo "  - nothing was learned and nothing is left open -> say so in one line and stop; this will not ask again." >&2
  exit 2
fi

exit 0
