VERDICT: supports

Item F-10 — routed defects state at 7e081698d4fc3c4ea944884fd093058de9909de1.

## 1. R43-SR1-LIMITS-CONTRADICTION — repaired

- `corpus/knowledge/btrfs-scrub-record-r43.md` carries the correction: `git show 7e081698:corpus/knowledge/btrfs-scrub-record-r43.md | grep -n "Corrections — round 44"` → `157:## Corrections — round 44`; line 159 (full text read) names the routed defect, the contradiction, and the corrected reading: "SR1's trailing-bytes consequence is inferred from the open flags and reproduced in a harness compiled from the pinned write path; it is not observed on this host". The stale bullet ("…was not reproduced") stays at :153, explicitly "as filed" inside the correction — append-only, not silently rewritten.
- SKILL.md sweep: the "Scrub record re-grounded — round 43" section (`SKILL.md:4002`) already carries the consistent wording — SR1 row action at `SKILL.md:4016` ends "[inference, reproduced in a harness] (SR1)". `grep -n "trailing"` over SKILL.md finds no "not reproduced" wording (only the r43.md original :153 and the correction :159, plus the spot-check lesson). No sweep edit was needed.
- PROVINCE.md sweep: `grep -nE "trailing|not reproduced|reproduc" PROVINCE.md` → no trailing-bytes/reproduction claim; the round-43 note ("**Round-43 note — scrub record re-grounded…**") states only the no-record host reading and the EPERM gate — no contradiction. No edit needed.
- Supporting consistency: `corpus/README.md:420` (r43 entry) describes the consequence as "marked [inference]"; `CORufo/waves/round-43/w1/C2ExecTailRepro.md:136` records the harness byte-check (`$ tail -c 195 final.bin | cmp - <(tail -c 195 longA.bin) -> identical`), matching the correction's claim.
- (Line-number note: the spot-check lesson cites the bullet at `:152`; at 7e081698 it sits at :153 — one line of header drift, content-identical.)

## 2. Item 2 — C2 binding gaps and C1 open channels

### C2 binding (tools/check-scrub-record-r44.py, sha256 c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059 == frozen)
The two named r43 binding gaps are closed in the r44 counter:
- padded verdict line (r43 defect H) → REFUSED. `declared_line` returns the raw first line untouched (`:203-205`), `VERDICT_RE.fullmatch` (`:197`) rejects `"  ROW SR1 VERDICT: holds  "`. Verified: probing the frozen module, `bound(...)` with padded output → `(None, None)` (unbound). Receipt `ScoutR43Defects/binding-probe.out`.
- blank-prefixed report (r43 defect I) → REFUSED. `first_line` (`:222`) no longer skips leading blank lines; a report opening with two blank lines → `(None, None)`.
- contradictory JSON `verdict` beside `verdict_line` (r43 blind spot A) → REFUSED. `declared_line` (`:194-201`) returns None when `verdict` is present and != the line's verdict word. Verified: `{"verdict_line":..., "verdict":"fails"}` → None.
- retraction on a later line (blind spot C) stays unclosed by design: the anchor is the first line; a trailing `fails` line is the mention that "counts for nothing" — unchanged.
Still open at 7e081698 (not in the named two):
- duplicate `verdict_line` keys: `json.loads` last-wins (`:193`) — `{"verdict_line":"…fails…","verdict_line":"…holds…"}` binds `holds` (verified). A contradictory earlier `fails` is silently overwritten.
- malformed orchestrator record shapes crash instead of FAIL: `load_json` (`:143-146`) returns any non-dict truthy JSON; `bound` then hits `AttributeError: 'list' object has no attribute 'get'`/`'int'...` (verified for top-level `w2-results.json` list, `w2-dispatch.json` list, `tasks:[1]`). Exit 1 with no JSON verdict line — indistinguishable from FAIL by exit code, breaks the declared output contract.
- Supporting consistency: `corpus/README.md:420` (r43 entry) describes the consequence as "marked [inference]"; `.ufo/waves/round-43/w1/C2ExecTailRepro.md:136` records the harness byte-check (`$ tail -c 195 final.bin | cmp - <(tail -c 195 longA.bin) -> identical`), matching the correction's claim.
- residual escape hatch (`C2ResSR<n>`) is forgeable exactly like the main path — same binding, declared limit.
The r44 counter's own header claims only the two r43 gaps (`:24-30`), which matches the observed state.

### C1 open channels
The r43 boot-chain counter's channels are no longer the scored surface (round-44 C1 is the scrub-record arm). The new scored counter `tools/score-scrub-arm-r44.py` (sha256 1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388 == frozen) declares its channels at `:48-50`: closed = override env, process identity, drawn fixture values; open, reported = namespace traces (`/proc/self/mountinfo` tmpfs on /sys/fs/btrfs, /var/lib, /etc/systemd/system; `/proc/self/uid_map`; census sourced from /mnt; cwd /mnt/home at `:143`). The control battery has exactly one gated control for the mount-table channel (`C1-K7 mount-table-gated`, `.ufo/waves/round-44/controls/run_controls_c1.py:21-22`); uid_map/script-path/cwd remain open with no dedicated K control — reported, not closed. The empty-btime branch concern is N/A to the new arm (no btime/`/proc/stat` read in score-scrub-arm-r44.py; grep shows no btime); it persists only for the frozen boot-chain counter, which is not part of the round-44 surface.

## 3. Item 3 — census :743/:746 lookup case and five single-line readers — still open
- Foreign-baseline lookup at 7e081698: `tools/tsukuroi-census.sh:779` — `bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }')` (full read, no `exit`; inline comment: "full read (round 42: an awk `exit` under pipefail killed the census on a large baseline)"). The kill-fix is in place; the selftest case is not: all foreign-baseline cases use 16-row fixtures (`healthy-foreign-baseline` `:2402` etc.), none feeds a >64 KB baseline, so reverting :779 to the `exit` form would still pass 141/141 (the round-42 w2 finding stands; nothing was added since).
- Five single-line probe readers by content (`printf '%s\n' "$CAP_OUT" | head -n1`), current lines at 7e081698: `:967` (systemd user `is-system-running` state, probe_systemd), `:1005` (timer `Result` word, probe_systemd), `:1087` (nvidia-smi driver field, probe_drivers), `:1462` (boot target `is-active` word, probe_journal), `:1537` (timer `ActiveState` word, probe_journal). Coordinate drift: r42 pins 931/969/1051/1426/1501 (44766208) → r43 934/972/1054/1429/1504 (6951ead9) → today 967/1005/1087/1462/1537; measured +33 then +33 lines, matching file growth (3220 → 3396 lines). Same five readers, unchanged shape.
- Both stay routed by the round-44 declaration: `SCORECARD.md:2750` keeps planned item (3) ("the census `:746` lookup selftest case past the pipe buffer, the five single-line probe readers") routed — a third census claim would share C1's surface.

## 4. operator-*.md lessons not reflected in QUALITY.md/SKILL.md
- `corpus/lessons/` at 7e081698 contains no `operator-*.md` (`ls corpus/lessons/ | grep -E "^operator-"` → empty; find under the lane root → none). There is nothing to reflect.
- `QUALITY.md` does not exist in the lane (the lane root has LOG.md, MINT.md, PROVINCE.md, SCORECARD.md, SHONEN.md, SKILL.md; QUALITY content lives in `corpus/QUALITY.md`). Grep of `corpus/QUALITY.md` and SKILL.md for `operator-demand|operator-package|operator-queue` → no references.
- Operator-related cross-lane files exist outside the lane: `kasegi-shokunin/corpus/knowledge/operator-queue.md`, `game-dev-3d-shokunin/reports/round-105/…/round-106/operator-*.md`, `.ufo/scopes/*/operator-demand.md` — none are lane lessons and none are referenced by the lane's docs. The only lane record of the absence is `corpus/lessons/round-43.md:129` ("No `corpus/lessons/operator-*.md` exists (`w1/ScoutR42Defects-2.md` §6)"). Status: no gap in QUALITY/SKILL because no operator-authored lessons exist in this lane; the missing-record point from round 42 remains as stated.

## Verification notes
- The C2 binding probes were run against the frozen module read-only (import via importlib from the lane file; no mutation) in scratch `/fast/scratch/hyaku/tsukuroi-r44/ScoutR43Defects/`; receipt `ScoutR43Defects/binding-probe.py` + `binding-probe.out`.
- All git reads are `git show <rev>:<path>`; no lane file was modified; no counter was executed (no heavy run); scratch removed after copying receipts.
- Receipts: `.ufo/waves/round-44/w1/ScoutR43Defects/binding-probe.py`, `binding-probe.out`.
