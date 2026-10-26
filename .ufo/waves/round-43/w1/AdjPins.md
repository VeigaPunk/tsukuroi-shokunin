VERDICT: defect-found (4 sibling pins into boot-chain-audit.sh, all in frozen historical records; 1 moved by +9, 1 unmoved, 1 whose pinned content is the fixed code itself, 1 content line unchanged; zero sibling pins into btrfs-scrub-record-r42.md; both routed round-42 census pins still stale at 717b716a, and the tameshi one is semantically dead, not just +6)

# AdjPins — F-8 moved sibling pins, round 43 wave w1

Seat AdjPins (L2, leaf, read-only). Base `6951ead90566b2d74f7c45b4efca29246badad64` ("B"), implementation `717b716a8943151ace8657e0ca23d7d9b8434f26` ("I"). Lane HEAD at the time of the sweep: `7d0ed1c2` (descendant of I; `git diff --quiet I HEAD` on `tools/boot-chain-audit.sh`, `tools/tsukuroi-census.sh`, `corpus/knowledge/btrfs-scrub-record-r42.md` → no difference, so every coordinate below also holds at HEAD).
Did not run any counter, the census, or the audit; did not touch the lane, any sibling or the host. Scratch `/fast/scratch/hyaku/tsukuroi-r43/AdjPins/` (copies of B/I file bytes via `git show`), removed at the end. Receipts: `.ufo/waves/round-43/w1/AdjPins/` (`sibling-mentions-tracked.txt`, `sibling-mentions-with-untracked.txt`, `hunks-and-identity.txt`).

## 0. Method (all read-only)

```sh
for r in /home/vgpnk/Projects/shokunin/*-shokunin; do [ $(basename $r) = tsukuroi-shokunin ] && continue
  git -C $r grep -n -I -E 'boot-chain-audit|btrfs-scrub-record-r4|boot_inputs_newer|scrub-record'; done   # 21 hits
# same with --untracked: adds no file/line beyond the tracked set (diff of file:line lists empty)
git -C tsukuroi-shokunin show <rev>:tools/boot-chain-audit.sh | sed -n <range>p     # B and I, diffed
git -C tsukuroi-shokunin diff -U0 6951ead9 717b716a -- tools/boot-chain-audit.sh | grep '^@@'
```

The sweep used the broad pattern (any mention of the file name, not only `:<n>`), so pins written as `boot-chain-audit.sh:<n>`, `:<a>-<b>` or `tools/boot-chain-audit.sh:<n>` are all inside the 21 hits. Twelve of the 21 are tabi's own round-34 diff of the r42 entry (headers/prose with no line pin) and kama/kasegi/tameshi mentions without line numbers (listed in section 4).

Hunks B→I of `tools/boot-chain-audit.sh` (`git diff -U0`): `@@ -462,0 +463,14 @@` (helper `inputs_newer_than` 463-475 + blank 476), `@@ -480 +494 @@`, `@@ -482,6 +496 @@` (the `find … | grep -q .` block replaced by a 3-line call), `@@ -1215,0 +1225,14 @@` (three `R43-C1-*` selftest cases + blank, 1225-1238). Net shift by region, each verified byte-identical with `diff <(sed -n a,bp base) <(sed -n c,dp impl)`:

| base range | I range | shift |
|---|---|---|
| 1-462 | 1-462 | 0 |
| 463-479 (`boot_inputs_newer` head, fixture arm, btime) | 477-493 | +14 |
| 480-487 (the `if find … grep -q .; then … fi` block) | 494-496 (call) ; the decision itself now at 463-475 (`hit=$(find …)` at :469) | content replaced (this is the fix) |
| 488 (`}`) | 497 | +9 |
| 489-1215 | 498-1224 | +9 |
| (new) | 1225-1238 | R43-C1 selftest cases |
| 1216-1297 | 1239-1320 | +23 |

`btrfs-scrub-record-r42.md`: one line inserted at :4 (`superseded-in-part:`), every line ≥4 moves +1 (`git diff -U0 B I` → `@@ -3,0 +4 @@`). The r42 counter parses `## SC<n>` sections, not line numbers (`tools/check-scrub-record-r42.py:82-95`), so the +1 is not positional there.

## 1. Sibling pins into `tools/boot-chain-audit.sh`

`boot-chain-audit.sh` last changed before round 43 at `5a133bcf` (round 19), so every sibling pin written in rounds 21-42 was measured against the same bytes as B.

| # | repo | file:line | pinned range | base (B) content at the range | I range holding it |
|---|---|---|---|---|---|
| 1 | chousa | `.ufo/waves/round-36/w1/ConnOverlap.md:37` and `:68` | `boot-chain-audit.sh:1177` | B:1177 = `//safe$(touch canary)` (the conf-text line of the e6 no-canary heredoc, B:1176 `cat >"$e6" <<'EOF'`) | **I:1186** (+9), identical |
| 2 | chousa | `.ufo/waves/round-36/w1/ConnOverlap/scan-log.md:82` | `boot-chain-audit.sh:1174-1191` ("no-canary exec-eval arm") | B:1174-1191 = comment lines 1174-1175, heredoc, `(cd -- "$T" && audit "$e6" >/dev/null)`, `rc=$?`, canary test, `st_check 'e6-no-canary' absent "$got"` (:1191) | **I:1183-1200** (+9), 18 lines byte-identical |
| 3 | kama | `.ufo/waves/round-21/build/out/ConnectorSiblingLinks/sibling-overlap-scan.json:19` | `boot-chain-audit.sh:388` ("inspects new_root symlink target") | B:388 = `        tgt=$(readlink -- "$tree/new_root")`; B:386-392 identical in I | **I:388** (unchanged; first hunk is at 463) |
| 4 | tabi | `.ufo/waves/round-34/w2/ConnSiblingDrift/tsukuroi.diff:59` (inside the diff of the lane's `SKILL.md`, = lane `SKILL.md:3893`) | `tools/boot-chain-audit.sh:480-487` | B:480-487 = `if find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules -newermt "@$btime" -print -quit 2>/dev/null \| grep -q .; then printf '1\n' else printf '0\n' fi` | **no longer exists**: replaced by I:494-496 (`inputs_newer_than "$btime" <same 8 paths>`); decision logic at I:463-475 (`hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)` at :469). The pin is a "Not fixed here (routed)" defect statement, now fixed. |

Notes:
- Pin 1/2 are frozen round-36 wave records and name a pinned arm that moved +9 (insertions at 463 net +14, deletions at 480-487 net −5). The 1174-1191 target and :1177 line are byte-identical at I:1183-1200 / I:1186.
- Pin 3's stated meaning (`readlink … new_root`, B:389-390) is at I:389-390 too. (The pin was already off by 1 at round 21: B:388 itself is the `readlink` line, the `if [ -L … new_root ]` is B:387. Not a round-43 effect.)
- Pin 4 is not drift but fix-consumption: its claim ("reads false under pipefail … BOOTED-OBSERVED can be awarded while an input is newer") is exactly what C1 closes; tabi's frozen diff text keeps the base coordinates, which are correct as *base* coordinates.
- Other sibling mentions with no line number: kama r18 `ConnectTsukuroi.md:50,74` (`boot-chain-audit.sh --live`, a refusal), kama r42 `sibling_tools_sha256_list.txt:384` (path only; a **hash list** of sibling tools — if it records the sha256 of `boot-chain-audit.sh`, that digest is stale as of 717b716a; the file lists paths, I did not open a digest column), tameshi r18 `C04GitEnvPriorArt.md:58` (`git grep -F git HEAD -- tools/boot-chain-audit.sh`, historical result; the I file has no `git` token added: new lines contain none — not re-run).
- Lane-internal self-pins to `:480-487` (not siblings, listed for L1): `SCORECARD.md:2642`, `SKILL.md:3893`, `corpus/lessons/round-42.md:81`, `corpus/lessons/round-42-verifier-spotcheck.md:206` — all state base coordinates and the round-43 declaration says "base :480-487", so they are correct historical statements; they would mislead only if read against I.

No live sibling pin (PROVINCE.md / SKILL.md / corpus/knowledge at a lane root) points into `boot-chain-audit.sh`: the four pins above are all inside `.ufo/waves/*` frozen wave records (chousa r36, kama r21, tabi r34).

## 2. Sibling pins into `corpus/knowledge/btrfs-scrub-record-r42.md`

None with a line number. The only sibling mentions are tabi `.ufo/waves/round-34/w2/ConnSiblingDrift.md:79,109`, `ScoutSiblingDrift.md:33`, `ConnSiblingDrift/tsukuroi.diff:146-154` (diff headers/prose), kasegi `round-39/wave2/SentinelScopeGuard.scope.txt:230` (status listing `M corpus/knowledge/btrfs-scrub-record-r42.md`). The +1 at :4 moves nothing a sibling pins. In-lane: no pin `btrfs-scrub-record-r42.md:<n>` in `tools/` or `corpus/`; r43 entry line 8 and `check-scrub-record-r43.py:5,38,62` cite the file by name/"first 20 lines" only (the `superseded-in-part` line sits at :4, inside the first 20).

Other r43-changed lane files, sibling line pins: `corpus/SOURCES.md` changed at :246 (in place) and +2 inserted after :248; highest sibling SOURCES pin found is :188 (mori r50 `Mo50bConnSiblings.md:40`) — none ≥249, none moved. `SCORECARD.md` +38 appended after :2646; highest sibling pin :2113 (tabi r32) — none moved. Regex sweep for sibling pins ≥ :249 into SOURCES.md or ≥ :2600 into SCORECARD.md: no hits.

## 3. Round-42 routed handoffs, restated and re-checked at I

Round 43 did not touch `tools/tsukuroi-census.sh` (`git diff --quiet 6951ead9 717b716a -- tools/tsukuroi-census.sh` → identical; also identical vs round-42 dispatch tip `78abb8b5`). So the round-42 coordinates are exactly as handed off, and the siblings are unchanged: `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md` and `mori-shokunin/PROVINCE.md` both clean vs their HEAD (`git diff --quiet HEAD -- <file>`), last touched `9f1d3c3` (probation r7) and `af42101d` (round 30).

Source of the arithmetic (`git diff -U0 c8efaa3f 717b716a -- tools/tsukuroi-census.sh`): first hunk `@@ -692 +692,7 @@ probe_packages()` = +6 net before any line ≥ 695. Split by commit: `44766208` (r42 C1) `@@ -692 +692,4 @@` = +3; `78abb8b5` (r42 integration) `@@ -694,2 +694,5 @@` = +3. Every census line > 693 therefore sits +6 below its c8efaa3f position.

**N1 — mori `PROVINCE.md:287`**: pin `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115` (and `PROVINCE.md:30-33`).
- `:1100-1115` content (c8efaa3f:1097-1112, the memory-pressure arm intro "# Round-7 addition, lane S7-2 …") is now at **I:1103-1118** (+6 from base 1097-1112; `diff` of the two 16-line ranges empty). The pinned coordinate names c8efaa3f:1094-1109, i.e. is stale by +3 relative to the content's *pinned* position (the pin was already right at round-24 time; by r42 the content had moved to 1097 via earlier rounds). Observed at I: `sed -n 1103p` = `# Round-7 addition, lane S7-2. Detection-only, read-only, non-root. Vocabulary:`; `sed -n 1100p` = `local k_oom=…`-region text, not the arm.
- `:376` unchanged: line 376 is the btrfs bad-devid comment (`# whose name is not a decimal devid is BLOCKED as <fsid8>:?:bad-devid …`) at c8efaa3f and I; the `/proc/pressure/memory` constant is `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}` at **:455** at both (pre-existing quirk, not a round effect).
- `tsukuroi-shokunin/PROVINCE.md:30-33`: PROVINCE.md not touched by round 43; round 42's insertions landed after :235 (per `w2/AdjMoriPin.md:62-63`).

**N2 — tameshi `corpus/knowledge/service-optin-protocol.md:153`**: pin `tsukuroi-shokunin/tools/tsukuroi-census.sh:915-970` (same doc `:249` also pins `sed -n '915,920p'`).
- Coordinate arithmetic confirmed: c8efaa3f:915-970 → **I:921-976**, byte-identical (`diff` empty). But the content there is the head of `probe_systemd` ("# ---- plane: systemd (user scope)", `probe_systemd() {` …), **not** what the doc means. I:921 is `}`, I:922 blank, I:923 `# ---- plane: systemd (user scope) …`.
- **New finding (correction to the round-42 handoff, which called it "+6 stale, byte-identical under the shift" and thus left the impression that 921-976 is the target):** the doc cites the round-5 selftest block ("9 new cases … 26 → 35", `sed -n '915,920p'` → "the hardening block comment naming tameshi's mutate-and-run.sh, 23 single-edit defects, first pass 13 killed / 10 survived"). That block *was* at 915-970 in `da952909:tools/tsukuroi-census.sh` (1032 lines; `sed -n 915p` = `# ---- round-5 mutation hardening (lane S5-1, 2026-10-14): one case per survivor class`, :970 = `TSUKUROI_CENSUS_SELFTEST: …` precedes). It left those coordinates after round 5 and sits in the census selftest at **I:2425-2480**: a script match of da952909:915-970 (56 lines) against 717b716a's census finds one exact occurrence at 2425-2480. So the pin has been semantically dead since round 6+ (a round-5 historical coordinate), and the round-42 +6 is not the explanation for it.
- Same for `:249`: `sed -n '915,920p'` hardening comment → I:2425-2430.

## 4. Draft handoff lines (report-only; the lane edits no sibling)

Place into the round-43 report/handoff section. Wording uses I and base hashes; replace `<REV>` with the commit L1 closes on.

> **Handoff — chousa-shokunin round-36 records (frozen; report only).** Round 43 (base `6951ead9`, impl `717b716a`) moved `tsukuroi-shokunin/tools/boot-chain-audit.sh` lines ≥463 (+14 helper `inputs_newer_than` at 463-475, −5 at the `boot_inputs_newer` body, +14 selftest cases at 1225-1238). `.ufo/waves/round-36/w1/ConnOverlap.md:37,68` pin `boot-chain-audit.sh:1177` and `ConnOverlap/scan-log.md:82` pins `:1174-1191` (e6 no-canary exec-eval arm): the same bytes now sit at **1186** and **1183-1200** (+9, byte-identical). A frozen record; no action required.

> **Handoff — kama-shokunin round-21 scan (frozen; report only).** `.ufo/waves/round-21/build/out/ConnectorSiblingLinks/sibling-overlap-scan.json:19` pins `boot-chain-audit.sh:388` (new_root symlink target inspection). Unchanged by round 43: line 388 and 386-392 are identical at `717b716a` (the first round-43 hunk is at 463). No action.

> **Handoff — tabi-shokunin round-34 snapshot (frozen; report only).** `.ufo/waves/round-34/w2/ConnSiblingDrift/tsukuroi.diff:59` quotes tsukuroi's round-42 "Not fixed here (routed)" note about `boot-chain-audit.sh:480-487` (`find … -quit | grep -q .` under pipefail). Round 43 fixed it at `717b716a`: the block is replaced by a call at 494-496 and the decision is `hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)` at :469 inside `inputs_newer_than` (463-475). The snapshot's base coordinates remain correct as base coordinates. No action.

> **Handoff — tameshi-shokunin `corpus/knowledge/service-optin-protocol.md:153` (and :249) — live knowledge doc; report only, owner decides.** Round 42 moved `tsukuroi-shokunin/tools/tsukuroi-census.sh` lines after 693 by +6 (`44766208` +3, `78abb8b5` +3); round 43 did not touch the census (still `78abb8b5` bytes at `717b716a`). The coordinates `915-970` now name 921-976 (probe_systemd head), but even before round 42 they did not name the round-5 selftest block the doc means ("9 new cases, 26 → 35"; hardening-comment `sed -n '915,920p'`). That block was at 915-970 only in `da952909` (round 5, census 1032 lines) and now sits, byte-identical (56 lines), at **`tsukuroi-census.sh:2425-2480`** (comment :2425-2430) at `717b716a`. Suggested refresh: cite `tsukuroi-shokunin/tools/tsukuroi-census.sh:2425-2480` at `717b716a`, or the blob pin `da952909`. tsukuroi makes no edit into the sibling.

> **Handoff — mori-shokunin `PROVINCE.md:287` — live adjacency note; report only, owner decides.** The note cites `../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`. The 16-line memory-pressure arm intro ("# Round-7 addition, lane S7-2 … the operator remediates.") sat at 1097-1112 at `c8efaa3f` and sits at **1103-1118** at `717b716a` (+6: `44766208` +3 and `78abb8b5` +3, both in `probe_packages`, hunks `-692 +692,4` and `-694,2 +694,5`; census untouched in round 43). Suggested coordinate: `:1103-1118`. `:376` is a btrfs bad-devid comment at both revisions; the `/proc/pressure/memory` default `PRESSURE_FILE` is at `:455` in both. `tsukuroi-shokunin/PROVINCE.md:30-33` unchanged. The note's meaning ("shared evidence is not shared ownership") is unaffected; this is a bookkeeping side effect of the round-42 C1 fix, not a semantic change.

> **Handoff — btrfs-scrub-record-r42.md (all siblings).** Round 43 inserted one line at `corpus/knowledge/btrfs-scrub-record-r42.md:4` (`superseded-in-part:` pointer to `btrfs-scrub-record-r43.md`); lines ≥4 move +1. No sibling pins a line of this file (checked tracked and untracked files of all 20 sibling repos); nothing to do.

## 5. What I did not do

Did not check sibling pins into lane files other than `boot-chain-audit.sh`, `btrfs-scrub-record-r42.md`, `corpus/SOURCES.md`, `SCORECARD.md` and the census (the r43 changed non-wave set is `SCORECARD.md`, `corpus/SOURCES.md`, the two btrfs entries, `tools/boot-chain-audit.sh`, `check-scrub-record-r43.py`, `score-bootinputs-r43.py`; the last two and `…-r43.md` are new, so cannot be pinned by earlier siblings). Did not open `kama-shokunin/.ufo/waves/round-42/w1/out/R42B16/sibling_tools_sha256_list.txt` for a digest column; did not re-run any `git grep -F git` claim in tameshi r18; did not run any counter, the audit, or the census. No tool installs. Scratch removed on exit.
