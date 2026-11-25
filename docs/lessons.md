# Lessons learned

Every approved lesson, and where the fix now lives. The COO adds a row only after Roy
approves. Reviewed weekly: merge duplicates, delete what no longer applies.

| # | Date | What went wrong or was learned | Fix | Where the fix lives |
|---|---|---|---|---|
| 1 | 2026-11-24 | An ASCII org chart in a Hebrew reply was misread (developer and QA looked like they were not under the CTO) | Show structures as tables in Hebrew replies | `~/.claude/CLAUDE.md` > How to answer |
| 2 | 2026-11-24 | CTO found CapCut draft files carry hashed machine IDs | Never commit, upload or quote draft files; strip ID fields from test copies | `.claude/agents/video-editor.md` > Working with CapCut |
| 3 | 2026-11-24 | legal-regulatory returned its report in chat and did not save the file, saying its instructions forbid report files | Every agent's Output section says saving the deliverable is part of the task | `.claude/agents/*.md` > Output |
| 4 | 2026-11-25 | CTO stalled for 10 minutes on pricing pages that would not load | Every research brief sets a web-call budget (~15 total, 2 per source) and skips dead pages | `CLAUDE.md` > Your role (point 5) |
