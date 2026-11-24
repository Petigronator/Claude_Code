# CapCut draft automation: feasibility, tools, risks (CTO evaluation)

- Date checked: 2026-11-24. Re-check after every CapCut update, and anything older than 6 months.
- Scope: can the video-editor agent write CapCut desktop drafts (cuts, Hebrew captions,
  audio) on Roy's PC, safely and for free, instead of Roy importing `roughcut.mp4` + SRT by hand.
- Method: read-only inspection of Roy's local draft "1104" (nothing in CapCut folders was
  changed), plus web sources listed at the end. Third-party reports are marked as such.
- Environment: Windows 11, CapCut desktop international 9.7.0.4153, draft schema
  `version 360000`, `new_version "191.0.0"`, `app_source "cc"`.

## Recommendation: test first (time-boxed), do not adopt yet

Writing a draft is technically feasible on 9.7: the files are plain JSON and the structure
is understandable. But the format is undocumented, changes every few CapCut releases, and
CapCut auto-updates. The gain over today's method is real but modest (editable cut points,
pre-styled captions, no re-encode). So: run one safe, time-boxed spike (about 1.5 days)
on a throwaway project. Adopt only if every success check passes. Keep the current
method as the default fallback either way.

Preferred stack for the spike: a small **Python stdlib-only script** (no install) that uses
**"clone and patch"**. It copies segment and caption objects from a reference draft Roy
makes in CapCut himself, then writes them into an **empty project that CapCut created
itself**. No third-party library is required (reasons in section 2).

---

## 1. Feasibility: what a draft is made of (verified locally, 9.7.0.4153)

### Files in a draft folder (`.../com.lveditor.draft/<draft name>/`)
| File | Role | Must we write it? |
|---|---|---|
| `draft_content.json` (root) | Full timeline: tracks, segments, materials. Times in microseconds. | Yes |
| `Timelines/<main_timeline_id>/draft_content.json` | Per-timeline copy. 9.x uses a multi-timeline layout. On 9.7 it is byte-for-byte the same version header as the root file. | Yes, kept identical to the root file |
| `Timelines/project.json` | Lists timelines and `main_timeline_id` | No (reuse the app-created one) |
| `template-2.tmp` (root and per timeline) | Plain-JSON mirror of the timeline (same header) | Probably yes. Third-party tools found CapCut can prefer it over `draft_content.json` (see section 2) |
| `draft_content.json.bak`, `project.json.bak` | CapCut's own backups, rewritten on save | No |
| `draft_meta_info.json` | Draft id, name, folder path, cover, timestamps, and **`draft_materials`**: the list of imported media | Yes: each media file must be registered here (see below) |
| `draft_virtual_store.json` | Media-bin ordering (child ids of the imported media) | Probably yes, one entry per media file (uncertain) |
| `draft_settings` (INI), `timeline_layout.json`, `attachment_*.json`, `common_attachment/` | Edit time stats, UI layout, feature attachments | No (reuse the app-created ones) |
| `draft_cover.jpg` | Thumbnail | No |

### Links between files that must stay consistent (verified in draft 1104)
- Each video material in `draft_content.json` has `local_material_id`, which equals an
  `id` in `draft_meta_info.json > draft_materials[type 0]` (with `file_Path`, `duration`,
  `width`, `height`, `metetype: "video"`). If this link is missing, newer CapCut shows the
  clip as "file inaccessible" or asks to relink. This was reported for 9.1 by third parties
  (pyCapCut issue #13 and capcut-cli 0.22/0.23) and matches what we see in 9.7.
- Each segment points to a `material_id`, plus `extra_material_refs`: per-segment helper
  objects (speed, canvas, placeholder info, sound-channel mapping, material color, vocal
  separation). Each of these must exist in `materials` with a unique id. That is why
  cloning a CapCut-made segment is safer than writing one from scratch.
- Durations, `source_timerange` and `target_timerange` are in microseconds
  (5,133,333 = 5.133 s at 30 fps).

### Parent folder: `root_meta_info.json`
This is CapCut's index of all drafts (`all_draft_store[]`: path, id, name, cover, json file,
timestamps; plus `draft_ids` count). A brand-new folder would need an entry here, or CapCut
would have to rescan on its own.
- **Uncertain:** whether CapCut 9.7 picks up a new folder by rescanning. The pyCapCut
  README says you may need to enter and leave a draft or restart CapCut for it to appear.
  CapCutAPI forks say copying a folder in is enough. Neither source names 9.7.
- **Our way around it:** never create a folder and never touch `root_meta_info.json`. Roy
  creates an empty project in CapCut, so CapCut registers it itself. With CapCut closed,
  the script fills that project. capcut-cli's docs and a pyCapCut issue comment
  describe the same "app-created shell" approach. Third parties also report that drafts
  built from a stale template are refused as "from an unusual path" on CapCut 8.4 to 9.3.

### What is not yet known for 9.7 (must come from the reference draft)
- **The text and caption schema.** Draft 1104 has no text, so the `texts` material and
  `text`/`subtitle` track fields for 9.7 were not observed. capcut-cli reports that text
  style `range` values count UTF-16 code units, not bytes. Hebrew letters are 1 unit each,
  but emoji take 2.
- **Which mirror CapCut reads on open:** root, `Timelines/<id>/`, or `template-2.tmp`.
  Third-party reports differ: 9.5 Windows reads root-only writes; 9.2.8 macOS reads only
  the nested file; 8.7 Windows sometimes prefers `template-2.tmp`. Safe rule: write all
  mirrors identically.
- Whether CapCut converts or encrypts the draft when it saves a tool-written file. The
  Chinese version (JianYing) does this from 6.0. CapCut international 9.7 still saves plain
  JSON (verified here).

### Answer to Q1
Yes, feasible on 9.7 by writing: root + nested `draft_content.json` (+ `template-2.tmp`
mirrors), registered media in `draft_meta_info.json` (and probably
`draft_virtual_store.json`), with absolute media paths that exist on disk. Writing
`root_meta_info.json` is avoidable and should be avoided. Video audio comes with the video
segment (`has_audio`, volume), so no separate audio track is needed for Roy's own takes.

## 2. Existing free tools (checked 2026-11-24)

| Tool | Language | Licence | Last push / release | CapCut intl. Windows ~9.x | Known breakage | Verdict |
|---|---|---|---|---|---|---|
| [pyCapCut](https://github.com/GuanYixuan/pyCapCut) (GuanYixuan) | Python 3.8+ | **None stated** (GitHub API: `license: null`, no LICENSE file) | push 2026-10-16; PyPI 0.0.4 on 2026-10-16 | Feature tables say "verified" on 8.2.0 and 9.5.0.4050. 9.7 not listed | #13 (open, no maintainer reply): leaves `draft_materials` empty, so media shows "inaccessible" on 9.1. #7: upgrade prompts. 0.1.0 will break the track API. Auto-export only matches the Chinese build (#17). Templates must be plain JSON | Closest fit for Python, but **no licence** means by default we have no right to use it in a brand that earns money. Use only as reading material |
| [pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) | Python | Apache-2.0 | active (5.0k stars) | **No**: targets JianYing (China). Its own README points to pyCapCut for CapCut | JianYing 6.0+ encrypts `draft_content.json`. Template mode needs a fallback loader. #177: JianYing 10.3 macOS reports "content corrupted" (open) | Wrong product |
| [capcut-cli](https://github.com/renezander030/capcut-cli) (Rene Zander) | Node.js 18+, zero runtime deps | MIT | push 2026-11-24, CHANGELOG 0.37.0 on 2026-11-22 | Version matrix: 9.5.0 "supported" (reported round trip), 9.8.0 "untested" (opens, no round trip), **9.7 not listed**. 10.x "reported" to reject tool-written drafts; writes refuse without `--force-write` | Fast-moving, single maintainer. The README also promotes the author's paid services (not needed) | Best safety engineering: `.bak` on every write, `restore`, `--dry-run`, refuses writes while the editor runs, version gate, `register --materials`, timeline-mirror sync. **Needs Node.js installed** (free, but an install needs Roy's OK). Best reference documentation either way |
| [VectCutAPI](https://github.com/sun-guannan/VectCutAPI) (formerly CapCutAPI) | Python 3.10+, HTTP server + MCP | Apache-2.0 | push 2026-11-21 (2.4k stars) | Says "Jianying or CapCut International" with profiles `capcut_legacy`, `jianying_pro_10`. No version numbers | Writes a `dfd_` folder that you copy into CapCut by hand. Cloud render and agent parts are closed or promoted | Overkill: server, AI-generation focus (AI voices are banned for Roy anyway) |
| Own script, "clone and patch" | Python stdlib only | Ours | n/a | Built against Roy's exact 9.7 files | We own the breakage | **Recommended for the spike**: no install, no licence question, Roy can maintain it |

Encryption, as of the check date:
- **JianYing (China)**: encrypted since 6.0 (pyJianYingDraft PyPI page; capcut-cli docs).
- **CapCut international 9.7 on Roy's PC**: plain JSON (verified locally today).
- No source found that says CapCut international encrypts drafts. Treat that as "not yet",
  not "never".

## 3. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Corrupting existing drafts | Low if the rules below are followed | High | Write only into one app-created test project. Never touch `root_meta_info.json` or other drafts. Full backup of the drafts folder first. Hash-check the other drafts before and after |
| CapCut overwrites our write | High if CapCut is open | Medium | CapCut keeps the project in memory and rewrites it on close. The script refuses to run while `CapCut.exe` is running |
| Format change on CapCut update | **High over months**: schema mirrors changed between 8.4, 8.7, 9.2 and 9.5. 10.x is reported to reject tool-written drafts. JianYing went encrypted | Draft won't open, or opens wrong | Version gate: the script refuses unless the installed version matches the tested one (9.7.0.x). Re-run the test after every update before trusting it. The current method stays as the fallback |
| Encryption arrives in CapCut intl. | Unknown | Ends the approach | Nothing to do but fall back. Don't invest beyond the spike until it has survived 1-2 updates |
| CapCut terms of service | Low practical risk, real grey area | Account or support issues | ToS (Bytedance Pte. Ltd., Singapore law, last updated 2026-04-15), section 6, bars users from "copy, decipher, modify, adapt, translate, reverse engineer..." and from "use automated scripts or other technologies to collect information from or otherwise interact with the Services". Writing a local plain-JSON project file does not touch the software or the servers, but "decipher" and "interact" are broad, and CapCut does not sanction it. Not legal advice. Ask legal-regulatory for a first pass if Roy wants one. Keep test drafts local (cloud sync off; it is off on draft 1104) |
| Hebrew RTL in captions | Medium | Visible defects | Copy the exact text object CapCut produced from Roy's own SRT import (including any direction marks). Compute style ranges in UTF-16 units. Check punctuation, numbers and "BMW M3" order in the CapCut preview and on the export. No CapCut-specific Hebrew bug report was found. The general pattern in other editors is punctuation flipping in mixed Hebrew/Latin lines (claim that CapCut's caption editor is LTR-only comes from a vendor page; unverified) |
| Privacy | Certain | Medium | Every `draft_content.json` contains hashed machine identifiers in `platform` / `last_modified_platform` (`device_id`, `hard_disk_id`, `mac_address`). Never commit, upload or share draft files. Strip these fields from any test fixture |
| Library licence / supply chain | n/a for own script | Medium | pyCapCut has no licence. If capcut-cli is chosen: pin the version and read the release before running |

## 4. Alternatives

1. **Current method (keep as default):** `roughcut.mp4` + `captions.he.srt`.
   CapCut desktop officially supports caption import: Captions > Add captions > import a
   UTF-8 .srt file (CapCut help; menu names vary by version). This is robust and documented.
   Costs: cut points are baked into one clip (no trim handles), one extra encode, and
   captions are styled by hand.
2. **Better hand-off without drafts (cheap, no risk):**
   - Render the rough cut at near-lossless quality (high-quality x264 CRF or an intra
     codec) so the extra encode costs nothing visible.
   - Optionally also deliver `edit/segments/01.mp4 ... NN.mp4`, one file per approved cut.
     Roy drops them on the timeline in order and gets editable cut points back.
   - In CapCut, save the caption look once as a text preset or template, then apply it to
     all imported captions. **Uncertain:** the exact preset feature name in 9.7.
3. **XML / EDL route:** not available. CapCut's help (Jan 2026) says it does not support
   importing project files from other editors. Only rendered video works. DaVinci Resolve
   (free) does import EDL/FCPXML, but that means changing editor, and its Hebrew RTL
   support is unverified. Out of scope.

## 5. Test plan (only after Roy's go-ahead)

Goal: prove that one generated draft opens in CapCut 9.7 with correct cuts and correct
Hebrew captions, survives save, close and reopen, and leaves every other draft untouched.

Simplest version that proves it: one 30-60 s test clip of Roy's own footage, 3-5 cuts, 5-10
Hebrew caption lines including one mixed line ("BMW M3") and one with punctuation and a number.

Stack:
- Python 3.13 stdlib only (`json`, `uuid`, `shutil`, `hashlib`, `subprocess` for `tasklist`).
  No venv and no install needed.
- The script lives in `C:/Users/Petigro/OneDrive/Documents/claude-home/VideoStudio/tools/`.
  A single stdlib file is not a "heavy" dependency folder.
- Backups go **outside OneDrive** to `C:/Users/Petigro/CapCutBackups/<date>/`.

Steps, in order:
1. **Roy, in CapCut (about 10 min):**
   - Make project `zz-reference`: import the test clip, split it at 2 points, import a short
     Hebrew SRT via Captions, and style the captions the way he wants.
   - Make project `zz-shell`: empty, 9:16 canvas, or with the clip imported.
   - Note the version in Settings > Version and turn off auto-update if 9.7 offers that
     setting (uncertain).
   - Close CapCut fully.
2. **Backup (agent; copying is not deleting):** confirm `CapCut.exe` is not running. Copy
   the whole `com.lveditor.draft` folder to `C:/Users/Petigro/CapCutBackups/<date>/`.
   Verify the file count and SHA-256 of every file. Record the hashes of all drafts except `zz-shell`.
3. **Read-only analysis:** the script dumps the `zz-reference` structure: text material
   fields, caption track type, style ranges, direction marks, which mirrors exist. This fills
   the unknowns in section 1. No writes.
4. **Dry run:** the script builds the new timeline from `cutlist` + `captions.he.srt` and writes
   it to the scratch folder only. Diff it against `zz-reference`: same keys, unique ids,
   segments end to end, times in microseconds.
5. **Write (only into `zz-shell`):** guarded by checks (CapCut not running, version = 9.7.0.x,
   target folder name = `zz-shell`). Copy `zz-shell` to the backup first. Write root and nested
   `draft_content.json` (and the `template-2.tmp` mirrors) identically. Register the media in
   `draft_meta_info.json` (`local_material_id` link). Never open `root_meta_info.json` for writing.
6. **Roy opens CapCut.** Success means all of these:
   - (a) The draft list is intact and every other draft opens as before.
   - (b) `zz-shell` opens with no "corrupted", "unusual path", relink or upgrade prompt.
   - (c) N video segments whose in and out points match the cut list within 1 frame, with sound.
   - (d) M Hebrew captions within 1 frame of the SRT, rendered right-to-left with punctuation,
     numbers and "BMW M3" correct, editable as one caption group ("apply to all" works).
   - (e) Roy makes a small edit, saves, closes and reopens: the edit persists.
   - (f) After close, the draft files are still plain JSON (not encrypted).
   - (g) Export 1080x1920 and pass the stage-7 checks (fps, duration, loudness, contact sheet).
   - (h) Hashes of the other drafts are unchanged by our write. CapCut may later touch them
     itself, which is fine.
7. **Rollback if anything fails:** close CapCut. Roy deletes `zz-shell` in CapCut, or, with
   Roy's OK, the agent restores `zz-shell` from the backup. Restore the whole folder only if
   other drafts were affected (Roy's OK needed: it overwrites).
8. **Stop rule:** if two attempts, or more than 1.5 days, do not pass every success check,
   drop the approach. Log it as ruled out in the ledger and improve alternative 2 instead.

Effort (rough):
| Part | Who | Time |
|---|---|---|
| Reference + shell projects, look at results | Roy | 30-45 min total |
| Backup + read-only analysis | developer | 1-2 h |
| Clone-and-patch generator with guards, dry run | developer | 5-8 h |
| Verification against the success list | qa + Roy | 2 h |
| **Spike total** | | **about 1.5 days** |
| After each CapCut update: re-run steps 2-6 on a test project | developer + Roy | 1 h if nothing changed; a day or more if the format moved |

If it passes: the video-editor agent gains a stage "4c: generate CapCut draft into an
app-created project", behind the same guards. That needs Roy's approval and a change to
`.claude/agents/video-editor.md` (today it forbids writing into CapCut folders).

## Open uncertainties (honest list)
- Whether CapCut 9.7 rescans for new draft folders (avoided by the app-created shell).
- Which mirror 9.7 reads on open (handled by writing all mirrors; confirmed by test 6b/6e).
- The 9.7 text/caption schema (comes from `zz-reference`).
- Whether 9.7 has an auto-update switch.
- The 10.x rejection claim comes from third parties (capcut-cli version notes; pyJianYingDraft
  #177 is JianYing 10.3 on macOS, possibly a sandbox issue). Not confirmed for CapCut intl. Windows.
- ToS interpretation (not legal advice).

## Sources (all accessed 2026-11-24)
- Local, read-only: `%LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft/1104/*` and `root_meta_info.json`
- pyCapCut repo: https://github.com/GuanYixuan/pyCapCut ; PyPI: https://pypi.org/project/pycapcut/ ; API metadata: https://api.github.com/repos/GuanYixuan/pyCapCut
- pyCapCut issue #13 (draft_materials): https://github.com/GuanYixuan/pyCapCut/issues/13 ; #7: https://github.com/GuanYixuan/pyCapCut/issues/7 ; issue list: https://github.com/GuanYixuan/pyCapCut/issues
- pyJianYingDraft: https://github.com/GuanYixuan/pyJianYingDraft ; PyPI: https://pypi.org/project/pyjianyingdraft/ ; issue #177: https://github.com/GuanYixuan/pyJianYingDraft/issues/177
- capcut-cli: https://github.com/renezander030/capcut-cli ; README: https://cdn.jsdelivr.net/npm/capcut-cli@0.9.0/README.md ; version support: https://raw.githubusercontent.com/renezander030/capcut-cli/master/docs/version-support.md ; changelog: https://raw.githubusercontent.com/renezander030/capcut-cli/master/CHANGELOG.md ; encryption notes: https://raw.githubusercontent.com/renezander030/capcut-cli/master/docs/jianying-encryption.md
- VectCutAPI: https://github.com/sun-guannan/VectCutAPI ; API metadata: https://api.github.com/repos/sun-guannan/VectCutAPI
- CapCut Terms of Service (last updated 2026-04-15): https://www.capcut.com/clause/terms-of-service
- CapCut help, import subtitles: https://www.capcut.com/help/how-to-import-subtitles
- CapCut help, no third-party project import (Premiere): https://www.capcut.com/help/how-to-export-pro-project
- RTL caption issues in other editors (context only): https://community.adobe.com/t5/premiere-pro-discussions/hebrew-mixed-captions-are-not-working-correctly/td-p/12148659 ; https://caption-x.com/capcut-captions/hebrew (vendor claim)
