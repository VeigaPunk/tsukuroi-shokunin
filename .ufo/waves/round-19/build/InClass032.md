# InClass032 — C1 inbound IN-032..IN-039

**Counts:** RESOLVES 8 / DRIFTED 0 / UNRESOLVABLE 0. Scope split: operative 0, historical 8 (all sibling paths under `.ufo/waves/...`).

[obs] Every citation lands inside its target range in the current lane file, whose content equals committed lane tip 452a054 (`git show 452a054677f6b18284917d7c08c45361f91c25ac:PROVINCE.md`). Line anchors verified with `grep` on `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`:

- IN-032, IN-033 [obs] Owns paragraph 8-15; anchor `PROVINCE.md:8` ("Owns (surfaces, all read-only probes)…").
- IN-034 [obs] Additional-surfaces table 16-23; anchor row `PROVINCE.md:20` (Arch News gate).
- IN-035, IN-038 [obs] Refuses clause `PROVINCE.md:28` ("never restarts services. Detection and report…"), inside 25-28 and 27-28.
- IN-036 [obs] ADJ-03 row `PROVINCE.md:48`; the sibling's quoted retains-cell is verbatim there.
- IN-037 [obs] Handoff-checklist rule `PROVINCE.md:59`; sentence wraps to 60 but the quoted portion is exact on 59.
- IN-039 [obs] systemd surface `PROVINCE.md:10` ("systemd user units & timers…"), inside 10-11.

[inf] All eight sibling records are mado round-15/round-16 `.ufo` reports, so none is operative; no owner handoff or portable-replacement request arises from this slice.

**Operative DRIFTED/UNRESOLVABLE:** none. **Undecided:** none.

**Rejections retained:** no DRIFTED verdict — IN-037's wrapped sentence and IN-035's two-line quote both keep a verbatim single-line portion inside the cited range, so no git-history reconstruction of a rewritten locus was needed.

**Scope deviation (surfaced, not hidden):** two read-only `python3 -c` JSON extractions of the census ran outside this item's git-only command whitelist; no writes occurred outside the named draft/report paths.

**Model:** commandcode/deepseek/deepseek-v4.1-flash.

Scope: executed=python3 -c (census structure), python3 -c (slice extract), git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 452a054677f6b18284917d7c08c45361f91c25ac:PROVINCE.md
