VERDICT: defect-found

# ScoutR42Defects-2 — Item F-9: state of the five round-42 routed defects at 717b716a8943151ace8657e0ca23d7d9b8434f26

Read-only. Bytes read with `git show 717b716a…:<path>` (lane HEAD at run time was 7d0ed1c2, a descendant). No counter, selftest or
host command was run. Receipts: `ScoutR42Defects-2/commands.txt`. Source list: `corpus/lessons/round-42-verifier-spotcheck.md:189-210` (§6).
`R` below = 717b716a. The round-43 declaration (`SCORECARD.md:2648-2684` at R) claims C1 = AMEND item 5 only, C2 = REGROUND + VERDICT-FORM;
defects 2 and 3 and AMEND items 1-4, 6 are not claimed in it.

## Summary table

| # | Defect | State at R | Basis |
|---|---|---|---|
| 1 | R42-C2-REGROUND | **partly done**: header pointer done; SC1/SC3 rows re-grounded as SR1/SR3 (draft, uncounted); SC4 fold narrowings and SC5 not re-grounded; **three live cites of SC1-SC5 carry no "withdrawn/not verified" marker** | below §1 |
| 2 | R42-CAP-HEADER-DUP | **open** (nothing to fix until round 43 writes its own table; append-only) | §2 |
| 3 | R42-ADJ-TAMESHI-UNREPORTED | **open**; both sibling pins still stale at R; nothing in the round-43 declaration carries the handoff | §3 |
| 4 | R42-C1-COUNTER-AMEND | **2 of 6 done** (fail-open fixed with 3 red-before cases + the new counter built with setpriv/`--scratch`/signal handling for that surface); 3 open; 1 not applicable to the r42 counter | §4 |
| 5 | R42-VERDICT-FORM | **spec'd in the frozen r43 counter, not yet exercised**; one residual deviation from "one form" | §5 |

## 1. R42-C2-REGROUND

Header pointer (asked): **yes, done.** `corpus/knowledge/btrfs-scrub-record-r42.md:4` at R:
`superseded-in-part: round 43 — SC1 and SC3 below stand withdrawn (see "Corrections — round-42 wave 2") and are not a verified outcome; their write-discipline, resume and failure-report points are re-grounded as rows SR1 and SR3, and SC4's running-state note as SR6, in corpus/knowledge/btrfs-scrub-record-r43.md`.
The only change to that file in `6951ead9..R` is +1 line (git diff --stat). A K24-style sweep (regex `\bsuperseded\b`, first 20 lines, `tools/check-self-assessment.py:364,423`)
reproduced in Python on the R blob hits line 4. The frozen r43 counter's `pointer_ok` tests only that the first 20 lines contain `btrfs-scrub-record-r43.md`
(`tools/check-scrub-record-r43.py:321`), a weaker test than the K24 marker, but the marker is also there.

Still cited as verified (asked): command `git grep -n 'btrfs-scrub-record-r42' R -- . ':!.ufo'`; none of these files changed in `6951ead9..R`
(`git diff --name-only` lists only SCORECARD.md, SOURCES.md, both scrub entries, boot-chain-audit.sh, two counters):
- `PROVINCE.md:239-245` "Round-42 note — scrub record read from source": cites `btrfs-scrub-record-r42.md SC1-SC5` flat ("its `_tmp`-then-rename write under `flock`, … that only the userspace start process writes it and when recording is switched off"). No withdrawal marker, no r43 pointer. **Stale.** The cited SC1/SC3 text is the withdrawn text.
- `corpus/README.md:410` entry row lists SC1-SC5 including "SC3 the start process writes it, recording disabled on mkdir or first-write failure" with no marker; `git grep 'scrub-record-r43' R -- PROVINCE.md SKILL.md corpus/README.md` is empty, so neither index lists the r43 entry. **Stale.**
- `SKILL.md:3898-3912` "Scrub status record — round 42" table uses SC1/SC3/SC4 as sources, e.g. row `scrub.status.<fsid>_tmp` "not a second record and not damage" and "(SC1, SC3)". It is **mitigated, not fixed**: `SKILL.md:3945-3956` ("Round-42 notes — C2 outcome") says the entry's C2 did not verify and to read the `_tmp` and SC3/SC4 rows through the corrections (a left-over `_tmp` can corrupt a later record). The table row itself still says the opposite of the correction. It does not mention the r43 entry.
- Neutral/historical: `corpus/SOURCES.md:246-248` used-by columns (correct, S237 row also names r43); `SCORECARD.md:2574, 2644` (declaration/planned lines); lessons files.
So "do not cite as verified C2 outcome" is respected only by SKILL.md:3947; PROVINCE.md:240 and README.md:410 still cite it unqualified.

Not re-grounded by r43 (rows are SR1, SR3, SR6 only; `SCORECARD.md:2648+` declaration): SC4's other narrowings (the fold walks the current device list; progress socket is read before the record; entry lines ~176-194 of r42) and SC5's narrowing (status prints a limit only for a device with a record line and only when >1; `start` reports `--limit`, not a preset). SC5 was narrowed in the corrections without a counted verdict (lesson §6.1). Proposed owner action (not done by anyone in the lane yet): add the r43 pointer and a withdrawn marker to PROVINCE.md:240 and README.md:410 and an r43 pointer to the SKILL.md table, or add rows SR4/SR5 for the SC4/SC5 narrowings next wave.
Check commands for the L1: `git grep -n 'btrfs-scrub-record-r4[23]' <rev> -- PROVINCE.md SKILL.md corpus/README.md`.

## 2. R42-CAP-HEADER-DUP

`git show R:SCORECARD.md | grep -n '^| Capability |'` → 159, 850, 1314, 1582, 1993, 2017, 2028, 2036, 2086, 2196, 2277, 2438, 2527, 2630, **2632**.
2630 and 2632 are two header rows of one table, under `## Capabilities — current full evidence set (round 42)` (:2628); an awk scan for a header directly after a header+separator finds exactly one case (2632). `git diff 6951ead9 R -- SCORECARD.md | grep -c '^[-+].*Capability |'` = 0: round 43 neither fixed nor repeated it, and has appended no capabilities table yet (the section after :2648 is the declaration only). Per the defect: fix in round 43's own appended capabilities table (one header, one separator). Status: **open**; the next check is `grep -c '^| Capability |' ` on the round-43 table block = 1 (it is append-only, so the r42 pair stays).

## 3. R42-ADJ-TAMESHI-UNREPORTED

- No r43 report exists yet. `git grep -in tameshi R -- SCORECARD.md PROVINCE.md SKILL.md` shows only old rows (SCORECARD.md:31, 203; PROVINCE.md ADJ-07/OUT-010; SKILL.md round-5 rows); the round-43 declaration (`SCORECARD.md:2648-2684`) has no handoff and says adjacency "stays unclaimed". Status: **open** — the handoff must go into the round-43 report.
- Pin still stale, measured: `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` still reads `tsukuroi-shokunin/tools/tsukuroi-census.sh:915-970` (file last committed 2026-10-14, 9f1d3c33). Census at c8efaa3f: :915 `}`, :970 `t_fail=$((t_fail + 1))`. Census at R (unchanged since the r42 tip 12421a73, `git diff --quiet` holds): :921 `}`, :976 `t_fail=$((t_fail + 1))`. Block is at **921-976 (+6)** — consistent with w2/AdjMoriPin.md §3.
- mori pin: `mori-shokunin/PROVINCE.md:287` still names `tsukuroi-census.sh:376,1100-1115` (last touched af42101d, 2026-10-22). Census at R: :1103 is `# Round-7 addition, lane S7-2` (base c8efaa3f: :1097), :1100 is `}`. The memory-pressure arm intro moved 1097 → 1103 (**+6**, matching N2); the +6 is the arithmetic the handoff must state once. (My own measure at R confirms line 1103 only; I did not re-count the pinned 16-line end.)
- Proposed text for the r43 report (report-only; no sibling edit):
  > Handoff (round 42 → 43, unchanged at 717b716a): `tsukuroi-census.sh` content pinned by sibling notes moved by +6 lines from base c8efaa3f. (a) `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153` pin `915-970` → now `921-976`; (b) `mori-shokunin/PROVINCE.md:287` pin `1100-1115` names the memory-pressure arm intro, which sits at `1103-1118` (base `1097-1112`, +6); line 376 unchanged. Round 43 does not touch `tools/tsukuroi-census.sh` (`git diff 12421a73 717b716a`), so these coordinates hold until the next census edit.

## 4. R42-C1-COUNTER-AMEND (six bullets, §6.4 of the lesson; the lane's "planned item (1)")

Note: the bullets are written against the round-42 counter `tools/score-size-invariance-r42.py` (frozen; unchanged in `12421a73..R`) and the census. Round 43's new counter `tools/score-bootinputs-r43.py` carries several of them for a different surface.

| bullet | at R | evidence |
|---|---|---|
| (a) production-identity legs, uid 1000 via `setpriv`, per-run fixture names | **r42 counter: not done** (no `setpriv`/uid token in `score-size-invariance-r42.py`; it runs `unshare -rm`, line ~283). **r43 counter: done for its surface** (setpriv at caller uid/gid, `--clear-groups`, env minus TSUKUROI_/BOOTCHAIN_/UFO_; values drawn per run; start-point names are production's own by necessity; `score-bootinputs-r43.py:16,84`) | grep of both blobs |
| (b) frozen controls for gated / data-gated / padding-filter arms | **r42 counter: not done.** r43: battery K0-K10 for the r43 counter (uid-gated K3, env-gated K4, name-gated K5, mount-gated K7 recorded as open channel, pre-filter K10), `SCORECARD.md:2670-2680`. "padding-filter arm" is specific to the r42 counter and has no r43 analogue | declaration text |
| (c) `--scratch` required + SIGINT leak | **r42 counter: not done** (`--scratch` optional, falls back to `$TMPDIR` (:296,300); a SIGINT/SIGTERM handler `_sig` does exist (:73,298) but I did not test for a leak). **r43 counter: `--scratch` required (:240) and cleanup in `finally` + signal handler (:247-255); not run by me** | argparse lines |
| (d) selftest case for the `:743` lookup | **not done.** `:743` is now a full-read awk (`$1 == n && !f`, r42 fix) but census `check` cases with "large" are only 2360, 2577, 2584 (-Qkk/-Qu/-Sup); none feeds a >64 KiB `TSUKUROI_FOREIGN_BASELINE`; baseline fixtures at 2153, 2296, 2320, 2616 are small. A revert to `exit` would survive the selftest | `grep -nE "check .*(large|outgrew|pipe buffer|oversize|big)"` |
| (e) `boot-chain-audit.sh` `find -quit \| grep -q` fail-open, red-before case | **done** at R: `inputs_newer_than` decides on find's output (`hit=$(find …)`, non-empty → 1); `boot_inputs_newer` calls it with the same 8 paths; 3 `R43-C1-*` selftest cases; red-before at base: `before/c1-before.jsonl` per the declaration (I did not read or rerun it). Diff `git diff 6951ead9 R -- tools/boot-chain-audit.sh` is limited to that function pair + selftest | diff |
| (f) single-line probe readers | **not done.** Census at R still has `state=$(printf '%s\n' "$CAP_OUT" \| head -n1 \| tr …)` at :934, :972, :1054, :1429, :1504 (the sites w1/C1SweepSites.md rated "unreachable at current sizes, not neutralised"); selftest asserts `printf "$out" \| grep -q` at :2181-2187, :2198, :2229 are also unchanged. Census unchanged `12421a73..R` | grep |

Kill-rule cross-check: the declared C1 kill rule ("a function body other than inputs_newer_than, boot_inputs_newer, run_selftest changes") is consistent with the boot-chain diff (3 hunks, those 3 functions).

## 5. R42-VERDICT-FORM

State at R: specified in the frozen counter docstring and code, not yet exercised (no `w2-dispatch.json` exists in `.ufo/waves/round-43/` — listing shows only `w1-dispatch.json`).
`check-scrub-record-r43.py:20-27,160-195`: a seat counts only if named in `w2-dispatch.json`, exactly one entry in `w2-results.json`, the declared line must `re.fullmatch` `ROW SR<n> VERDICT: (holds|partly|fails)` for its own row, and the committed `w2/<name>.md` must have the identical first non-empty line; mentions elsewhere count for nothing (this closes R42-VERDICT-MENTION). Residuals:
1. `declared_line()` (:160-170) takes the JSON field `verdict_line` when the output parses as a JSON object and the first line otherwise — two accepted forms, whereas the defect asks for "one asserted verdict form". A JSON-wrapped output is accepted only through the key `verdict_line`; N3's `"verdict": "holds"` form is rejected (not bound), which is the safe direction. The w2 seat prompt (not yet written) must name which form it wants.
2. The seat-prompt part ("specify one asserted verdict form in the seat prompt") cannot be checked until w2-dispatch.json exists.
3. Control C2-K13 (report first line differs) and K6 (mention-not-assertion) are in the pre-data battery (`SCORECARD.md:2678-2680`); I did not read them.

## 6. Operator lessons `corpus/lessons/operator-*.md`

**None exist.** `ls corpus/lessons/operator-*.md` fails; the lessons dir holds only `round-*.md` and `round-*-verifier-spotcheck.md`; `find` for `operator-*` (depth 5 across the fleet) finds only unrelated files (tameshi `operator-runbook.md`, kasegi `operator-queue.md`, game-dev-3d reports, tabi handoff, scope `operator-demand.md`, souji census) and no file under any `*lessons*` path; `git log --all --diff-filter=A` in the lane lists no `lessons/operator*` file. So there is nothing unreflected in QUALITY.md/SKILL.md. Operator rulings that do appear as text (QUALITY.md:10 pacman advice, SKILL.md:1853 "all pacman transactions remain paused under the current operator ruling", round-18/19 closure "operator note" on `limine-snapper-sync`) are inside existing entries. If the task path was meant differently (e.g. a fleet-level `LEARNING.md` / `.ufo/l0-questions.md`), I did not audit those; say so if so.

## Not done

No counter, selftest, jj/git mutation or host command ran. The r42 counter's SIGINT behavior was not tested. Receipts in `ScoutR42Defects-2/commands.txt` are my command log (read-only), not tool output dumps.
