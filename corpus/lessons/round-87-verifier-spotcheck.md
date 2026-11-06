# Round 87 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-06
lane-round: tsukuroi r87; pre-round tip `220c86e315b727696d7c5efeaa7febea6b005e4a`, landed tip `3ba37eb0a3c2b17e535bb68891cf63047f4fbce8`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-87/tsukuroi.md` (fleet commit `a547d8e1dfba83665cd91290e7db73d1ea84d172`, author `tsukuroi-shokunin`, 20:33:04 -03, committed 20:34:14; one commit, filed once)
dispatch digest (copied from the mutable `.ufo/watchdog.log`, lines 3066, 3070, 3071, 3092):
`2026-11-06T19:01:09-03:00 launch tsukuroi round=87 pgid=424815 driver=hyaku-inline attempt=1`;
`2026-11-06T20:22:42-03:00 lane-dead-no-report tsukuroi round=87; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-87/tsukuroi.md)`;
`2026-11-06T20:22:44-03:00 launch tsukuroi round=87 pgid=1590042 driver=hyaku-inline attempt=2`;
`2026-11-06T20:34:41-03:00 complete tsukuroi round=87; hyaku-inline attempt=2`

Closure verdict: **admitted**. C1 verifies under its frozen predicate and kill rule (evidence-verified from the
committed receipts and run logs, digests re-measured; discrimination partial, lane-reported as 10 uncertified
clauses); C2 ruled `unprovable-but-better` by this reviewer; no axis harmed. The r86 host incident (pins on
`/boot/limine.conf` lines 30 and 38 mismatched) is still present and stays operator-owned.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-87/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local> a547d8e1… Fri Nov 6 20:33:04 2026 -0300`, one commit | pass |
| `SHONEN` heading, one line per box | `git show 3ba37eb0:SHONEN.md \| grep -cE '^\s*- \[[ x~]\]'` → `4`; `grep -cE '^- \[[ x~]\]'` on the report → `4` (all `[~]`) | 4 = 4 | pass |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for 5eb8b157, a097bd9d, cefb4188, 46d48a71, 3ba37eb0, 220c86e3 | all resolve to full hashes; all ancestors | pass |
| Lane commits in range | `git log --format='%h %an %s' 220c86e3..3ba37eb0` | five commits, all `tsukuroi-shokunin`, freeze `5eb8b157` (committed 19:11:53) before candidate `a097bd9d` (19:12:58) | pass |
| Pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `3ba37eb0…` | pass |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-87.md) templates/round-prompt.md` (kimi-shokunin) | only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions differ; §6 hyaku addendum follows | pass |
| Prompt history | `git log -- .ufo/prompts/tsukuroi-round-87.md`; `git diff 3bba1e90 3553e62d` | `3bba1e90` (attempt 1, committed 19:01:08); `3553e62d` (attempt 2, authored 19:23:37, committed 20:22:42): "attempt 1"→"attempt 2" plus the host-incident paragraph | pass (note: author date predates the watchdog attempt-2 launch; commit date matches it) |
| Evidence chronology | receipt headers vs commit dates (`git log --format='%h %ad %cd' --date=iso`) | residual probe 20:28:47 in `46d48a71` (cd 20:29:33); c1-receipt 20:29:49, live receipt 20:30:23 in `3ba37eb0` (20:33:00) | pass, no future-dated evidence |
| Gate registry rows | `git show 3ba37eb0:SKILL.md \| grep -n 'limine-pin'` | rows `limine-pins` (5923) and `limine-pin-battery-r87` (5924), verdict maps incl. 2 and 64 declared | pass |

Not a marker: five landed lane commits with resolvable evidence. Status `ok`. Attempt 1 died without a report
(watchdog line 3070); attempt 2 filed it. That is a conformance note, status-neutral.

## 2. Claims

### C1 (measured; operability) — evidence-verified, digests re-measured

The battery and the gate are lane-owned gates: per §Gate standard (Closure consequence) I did not execute them. I
verified their committed evidence and re-measured the digests and counts from committed bytes.

| Check | Command (lane repo) | Observed |
|---|---|---|
| Battery bytes unchanged since freeze | `git show 3ba37eb0:tools/limine-pin-battery-r87.py \| sha256sum`; same at `5eb8b157`; `grep battery before/freeze-manifest.sha256` | `f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d` all three; kill rule "void" not triggered |
| Gate bytes measured = landed | `git show 3ba37eb0:tools/check-limine-pins.py \| sha256sum`; same at `46d48a71`; `git diff --stat 46d48a71 3ba37eb0 -- tools` | `e3b0fab4…07352` both; no tools change after the measured revision |
| Gate absent before | `git show 220c86e3:tools/check-limine-pins.py` | path not in `220c86e3` |
| Three runs met | `git show 3ba37eb0:.ufo/waves/round-87/after/measured/c1-run{1,2,3}.json \| jq -c '{verdict,families_passed}'` | `met`/22 ×3, `families_total` key present |
| Receipt | `after/measured/c1-receipt.txt` | measured at `46d48a71…` in a clean `clone --shared`; runs 1-3 `families_passed 22/22 verdict met` rc 0; battery `--selftest` PASS 5/5, gate `--selftest` PASS 15/15 |
| Before controls | `before/controls/controls-summary.txt` | K1 0 0 0, K2 0 0 0, f1 0, f2 0, f3 2, f4 6, N01–N18 between 1 and 21 (N06 11 11 12), P0 22 22 22 — equals the report |
| Live surface | `after/live-receipt-landed.txt` | `--live` rc 1, `LP-MISMATCH` lines 30 and 38 `prompt`; three history pins OK; `/boot` b2sum list `0f6acc28…` before and after, `cmp` identical. Hashes `57f5eb94…`/`eff78d32…` vs pins `b990d8c6…`/`a68c281d…` equal the orchestrator's independent read in the dispatched prompt's host-incident paragraph |

Verdict: target met (22/22 ×3 at the landed bytes, battery unvoided). The predicate's "implements R1-R7" is
wider than the counter certifies: CriticClaims' forgers g01–g08, g10, g14 also read 22/22 ×3. The lane reports
this itself (SCORECARD measured row, lesson M3, QUALITY 125, routed R87-R4/R5), so it is a calibration note, not a
falsified claim. Operability: **improved** (a runnable read-only gate that detects the live host state no prior
lane gate hashed; score 9 → 9 by the lane's own rule, no ordinal move claimed).

### C2 (exploratory; depth) — this reviewer is the named non-author

Re-checks run: `git grep -n -i 'hash_mismatch_panic\|uri_resolve' 220c86e3 -- corpus/knowledge tools \| wc -l` →
`0`; at `3ba37eb0` the entry, its `.json`, the gate and the battery match. Quotes re-located in the pinned snapshots
at `3ba37eb0` (`sed -n` on `.ufo/waves/round-87/before/src/…`): LP3 `uri.c` 78-101 (last-`#` loop, `!= 128`, hex
check of either case) verbatim; LP5 `menu.c` 1711-1712 verbatim and `uri.c` 301-312 (`Press Y to continue`, `ch !=
'Y' && ch != 'y'`) supports the Y/any-key reading; LP1 `config.c` 798-799 (`strncasecmp` … `config[i - 1] !=
SEPARATOR`) verbatim; LP7 `objcopy.html` 188-191 verbatim; LP6 `CONFIG.md` 451-455 states the wallpaper/font skip
and the "without an enrolled hash … inactive" rule. Snapshot digests are pinned in `before/src/SHA256SUMS`; the live
`menu.c` re-fetch hashes `628001e8…8f95`, equal to the pin.

Ruling: **`unprovable-but-better`**. Reasons: (1) new ground — no prior entry stated the pin grammar, the hashed
bytes or the mismatch consequence (grep empty; S018/S019/S075 do not); (2) every row is tied to a pinned upstream
line at the installed tag, and the version trap (trunk BLAKE3 lengths) is named and fenced in Limits; (3) the
entry is actionable on this host — LP8 plus Operator actions tell the operator exactly what the next boot does
(prompt, not panic) and both repair paths with their trust consequence; (4) the limits are honest (macros, Secure
Boot unhashed rule, hook command not opened). Not countable as an ordinal depth move; the SCORECARD row stays
depth 8 and carries this verdict.

### Owned-axis harm check

`git diff 220c86e3 3ba37eb0 -- SCORECARD.md`: append-only (declaration + measured outcome), "Axes now: depth8,
coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged)". `git diff --stat 220c86e3 3ba37eb0 --
PROVINCE.md SHONEN.md` → empty. Registry: `tools/` holds 138 `.py`/`.sh` at `cefb4188` and `3ba37eb0`
(`git ls-tree --name-only <r> tools/ \| grep -cE '\.(py\|sh)$'`), and the committed `lints-receipt.txt` reads
`check-registry-coverage` PASS 138/138, `check-knowledge-header` PASS 103/103 at `46d48a71` (103 `.md` in
`corpus/knowledge/`). No harm found.

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1, evidence-verified |
| depth | unprovable-but-better | C2, this reviewer |
| coverage | unchanged | no claim; PROVINCE unchanged |
| freshness | unchanged | no claim (the live gate re-read host state; not claimed) |
| calibration | unchanged | no claim; the counter-coverage gap is disclosed, not hidden |
| adjacency | unchanged | no claim; ConnectorOverlap scan unfinished |

Re-measured: battery/gate digests, absence grep, source row counts (349 → 354 via `grep -c '^| S[0-9]'`), tool and
knowledge counts, census, quote locations. Evidence-verified only: battery runs, self-test tallies, registry and
header gate verdicts, live `--live` run, residual probe.

## 3. Discernment spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S353 Limine v12.9.4 `common/menu.c` | ADMIT | `curl -sSL https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/menu.c`, lines 1711-1712, sha256 `628001e8…8f95` (= pinned) | agree | the quoted line is verbatim; default `NULL` → panic, only `no` prompts; tag matches `pacman -Q limine` → `limine 12.9.4-1` |
| S354 binutils `objcopy` manual | ADMIT | `curl -sSL https://sourceware.org/binutils/docs/binutils/objcopy.html \| grep -n -A1 'destructively renames'` → live lines 190-191 | agree | the mechanism of the r86 incident from the tool's own manual; quote is 21 words, verbatim across 188-191 of the pin |
| Limine trunk `CONFIG.md` | REJECT (context only) | `curl -sSL …/limine/trunk/CONFIG.md` → line 449 "Limine distinguishes hashes by length: 64 hexadecimal characters is standard", sha256 `5c32c60f…4b59` (= the lesson's); trunk `uri.c` line 92 "Hash must be 64 BLAKE3, 128 BLAKE2b, or 256 BLAKE3 characters long" | agree | trunk describes a later Limine than the installed 12.9.4, whose `uri.c` 89-91 refuses any non-128 hash; admitting it would teach that a 64-hex pin is valid on this host |

`corpus/SOURCES.md` row re-opened: **S354** (`git show 3ba37eb0:corpus/SOURCES.md` line 365): `teaches` "without
an outfile objcopy rewrites the input file in place, even for a read-style option"; the ≤25-word quote in the lesson
Gate ("If you do not specify outfile, objcopy creates a temporary file and destructively renames the result with
the name of infile.", 21 words) is present on the live page and in the pinned snapshot at the corrected anchor
188-191. Agree. Rows S350–S353 carry pinned-snapshot sha256 values equal to `before/src/SHA256SUMS`.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ rc 0, 52 `W04` lines (all pre-existing duplicate-URL warnings, S038–S329), `tsukuroi ok`, no E code. Equals the
report.

## 4. Trend verdicts

- **expansion — unprovable-but-better.** +5 tier-A `mined` rows (349 → 354, re-counted) and one entry on ground
  no entry held (absence grep re-run → 0). The entry's admission rests on the exploratory C2 ruling, so the move is
  judged, not counted.
- **quality — improved.** R87-REG-1 appends a correction for the r86 registry over-generalisation (`SKILL.md`
  6258); registry coverage 136/138 → 138/138 (committed receipt; tool count re-measured 138); QUALITY 124 repaired
  with an exit map; no admitted entry failed a re-check here (four quotes re-located).
- **discernment — improved.** This spot-check agrees with the gate on two admits and the reject. The lane's own
  critic found that the counter certifies only part of R1-R7; that became lesson M3 and grounded QUALITY 125, which
  cites it.

## 5. Routed defects (owner: tsukuroi, round 88 unless stated)

1. Residual clause probe ran on a pre-landing working-tree gate (`controls.txt` line 2: sha256 `1b51a68f…`), not on
   the landed bytes `e3b0fab4…`. The report reads it as "the candidate gate equals the base 11/11". Re-run it on the
   landed revision and name that revision, or restate the line as pre-landing evidence.
2. C1 discrimination gap: carry R87-R1..R5 into a successor battery's freeze (roster literal, one-field lie
   controls, the ten uncertified clauses, the m05/m24/m25 families, delegation guard). Until then, cite C1 as "22/22
   on the frozen families", never "implements R1-R7".
3. SHONEN box 4 evidence: ConnectorOverlap's sibling scan (`w1/ConnectorOverlap/sibling-scan.txt`) is unfinished;
   finish it or re-dispatch before citing it.
4. Wave provenance: `w1-results.json` carries no seat output after the kernel restart; the seat finals in
   `w1/finals/` came from the session store. Say so in the wave record, and have seats write their own receipts
   to disk next time.
5. R87-R6: erratum owed for `.ufo/waves/round-86/w1/ScoutHost.md:23` labelling the BLAKE2b-512 column "sha256".
6. Operator-owned: the r86 host incident (lines 30 and 38 `LP-MISMATCH`, `prompt`) is unrepaired at
   `3ba37eb0`; L0 line `tsukuroi | round-86 | HOST INCIDENT` stays open.

SHONEN note for the operator: boxes 1 and 2 cite resolvable evidence (registry rows, R87-REG-1, LOG.md "Round 87");
box 3 has no no-oral-context retest and box 4's sibling scan is unfinished, so they are not checkable yet.
Promotion stays operator-owned.
