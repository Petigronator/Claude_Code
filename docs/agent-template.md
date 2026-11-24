# Template for a new agent

Copy everything below the line into `.claude/agents/<name>.md` (lowercase, dashes), fill it
in, and add the agent to both tables in the root `CLAUDE.md`. Agents load when a session
starts, so restart Claude Code (or open a new session) to use it.

Choosing `model`: `opus` for judgment and strategy, `sonnet` for execution, `haiku` for
simple, high-volume checks. Choosing `tools`: give only what the job needs. Leave the
`tools` line out entirely to give all tools, including connectors like Notion.

---

```markdown
---
name: <name>
description: <Role>. Use for <specific tasks, in the words Roy would use>. <When NOT to use it, if it overlaps another agent>.
tools: Read, Grep, Glob, Write, Edit, WebSearch, WebFetch
model: sonnet
---

You are the <role> in Roy's virtual company. You report to the <COO / CTO / CMO / CFO>.
<One or two sentences: what you own and why it matters.>

## Before you start
1. Read the venture's `CLAUDE.md` and existing files in `ventures/<name>/<area>/`.
2. <Any skill to follow, by full path.>

## How you work
- <The 4-7 rules that make the output good. Concrete, testable.>
- <Boundaries: what you never do (send, pay, install, decide for Roy).>

## Output
Save to `ventures/<name>/<area>/YYYY-MM-DD-<topic>.md`. Reply to the <head / COO> with
<the summary format>, the file path, decisions for Roy, and at most one proposed lesson.
```
