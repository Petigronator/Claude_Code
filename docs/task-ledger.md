# Task ledger: Claude_Code workspace

## Done
| # | Date | What | Why (the request, in Roy's words) | Where |
|---|---|---|---|---|
| 1 | 2026-11-24 | Workspace set up: Git repo, COO role in CLAUDE.md, 11 agents, venture template, knowledge base, ledger and lessons log | "סדר לי את זה כמו בהיררכיה ארגונית" | `CLAUDE.md`, `.claude/agents/`, `ventures/_template/` |
| 2 | 2026-11-24 | Org restructured into departments (tech under CTO, marketing under CMO), adaptive-org rules and agent template added, video-editor agent hired, rough-cut stage (4b) added to video-pipeline skill | "אני רוצה ממש לבנות Adaptive Corporation team" | `CLAUDE.md`, `.claude/agents/video-editor.md`, `docs/agent-template.md`, `~/.claude/skills/video-pipeline/SKILL.md` |

## Pending
| # | Date | What | Owner | Unblocked by |
|---|---|---|---|---|
| 1 | 2026-11-24 | First test run of the agents on a real drawer idea, then fix the agents from what we learn | Roy + COO | Roy raises an idea in chat |
| 2 | 2026-11-24 | Idea bank in Notion (Roy adds ideas from his phone) | COO | After the first test run |
| 3 | 2026-11-24 | Weekly scheduled report from the COO | COO | Check that scheduling is free on Roy's plan |
| 4 | 2026-11-24 | Re-authorise Google Drive in claude.ai connector settings | Roy | - |
| 5 | 2026-11-24 | CTO evaluation: can video-editor generate CapCut 9.7 drafts automatically (draft_content.json is plain JSON), safely and for free? | cto | Roy's go-ahead |
| 6 | 2026-11-24 | First real video through the video-editor pipeline | Roy + video-editor | Roy films raw takes |

## Ruled out
| # | Date | What | Why |
|---|---|---|---|
| 1 | 2026-11-24 | Merging claude-home into this folder | Roy: keep claude-home separate; this folder is for agents and ventures |
| 2 | 2026-11-24 | COO as a subagent | Subagents cannot call other subagents, so the main session plays COO |
