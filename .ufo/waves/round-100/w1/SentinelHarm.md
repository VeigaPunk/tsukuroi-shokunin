# SentinelHarm — round 100 (w1) harm and scope guard — scoped findings

Seat `SentinelHarm`. Lane `tsukuroi` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`).
Base `ce73ccaf` → freeze `743ce449` → dispatch `60b5636f` → land `c450cd68` → land-fix `69474c55`.
Branch tip = `origin/master` = `69474c55eb38632f3e740923b58029dc43e01300`.
Full report + receipts: `.ufo/waves/round-100/w1/SentinelHarm/report.md` and
`.ufo/waves/round-100/w1/SentinelHarm/receipts/01..13`.

**Verdict: findings.** The round harms no axis at the tip, but the land commit `c450cd68` published
a transient broken state (7-of-8 registry row) in which three previously-certified gates read
`CANNOT_EVALUATE`, and the repair commit `69474c55` is disclosed in no record file.

## 1. Byte identity — PASS

`sha256sum -c .ufo/waves/round-100/before/instruments.sha256` (16 lines) → **16/16 `OK`**, no FAILED
line, at the tip worktree *and* at the freeze tip (`git archive 743ce449` extraction). Receipts 01,
02. The manifest pins the 16 instruments but **not** `before/census-before-after.txt` nor the
`before/dev/c1-*.json` / `c2-fixtures.txt` readings (grep count 0 for each) — see F3.

## 2. Freeze diff scope — PASS

`git diff ce73ccaf 743ce449 --stat` → `22 files +106656 -0`; all 22 paths are `A` (additions) and
all are `tools/check-registry-content-r100.py`, `tools/make-r100-bends.py`, `.ufo/plans/round-100.md`
or `.ufo/waves/round-100/**`. No record file, no corpus file, no other instrument. Receipt 03.
`git diff --name-only 743ce449 69474c55 -- tools/` → empty (tools byte-identical freeze→tip).

## 3. Control integrity — PASS

`git show ce73ccaf:<p> | sha256sum` vs the worktree file, four controls, all **IDENTICAL**:

| control | sha256 |
|---|---|
| `tools/check-limine-pins.py` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` |
| `tools/limine-pin-battery-r99.py` | `c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99` |
| `tools/limine-pin-battery-r98.py` | `8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87` |
| `tools/check-registry-content-r99.py` | `b489f5b86fa2fa706698ee32ce05cdefa514e9e7a17d4c0af537535bc597d20d` |

The `before/controls/` copies are byte-equal to the same four (manifest lines 9–12 `OK`). Each bend
changes exactly the one `limine_version` line against the frozen gate (2 changed lines = 1 removed +
1 added each). Receipt 04.

## 4. Scope sweep — PASS (no misroot)

**Fleet repo** `/home/vgpnk/Projects/shokunin` — 10 porcelain paths, per-path verdicts in the report:
`.scratch/closure-tabi-r83-entry.json`, `.scratch/goal-20261103-hyaku-run15.md`,
`.scratch/run15-state.json`, `.scratch/run15-wrapup/misroot-cff0b4cb/{versions.html,w4lines.txt}`
(pre-existing, mtime 2026-11-06, 0 `tsukuroi`/`round-` references), `.ufo/l0-questions.md` (its
round-100 addition is the `tsukuroi | round-92` credential-incident pair — round 92),
`.scratch/closure-kama-r96-entry.json`, `.scratch/closure-tabi-r87-entry.json`,
`.ufo/reports/round-68/kagi.md`, `.ufo/reports/round-90/souji.md`. **No round-100 wave evidence of
this lane exists outside the lane repo.** The fleet's own tracked `.ufo/prompts/tsukuroi-round-100.md`
is tracked and unmodified. Wave receipts name exactly **2** out-of-lane absolute paths, both
read-only references to fleet scripts (`scripts/hyaku/disk-guard.sh`, `scripts/sources-census.sh`).

**Lane repo** — `?? .ufo/waves/round-100/after/`, `?? .ufo/waves/round-100/w1.ready.dispatched`,
`?? .ufo/waves/round-100/w1/`; `git ls-files` under `w1/` and `after/` is **empty** (nothing under
the wave dir is committed). Each seat dir holds only its own files; the only file at `w1/` root is
`swarm-registry.json` (the fleet's). `.ufo/state/` does not exist and was not created. `master` ==
`origin/master` (no ahead/behind). At the **final** sweep the same command also shows
` M corpus/QUALITY.md` (+3 lines: a new criterion 142) and ` M corpus/lessons/round-100.md`
(+1 line: the `R100-CLONE-PATH-PREFIX` mistake) — the wave's own scribe seat's uncommitted working
-tree edits inside the lane's corpus, outside this seat's write scope; this seat did not touch
them, and the L1's settle step owns them. Receipts 05, 06.

## 5. Axis guard — PASS

`git diff ce73ccaf 743ce449 -- SCORECARD.md PROVINCE.md SHONEN.md corpus/` → **empty** (0 bytes,
no path). `corpus/SOURCES.md` byte-unchanged at the freeze. Base→tip removed-line counts:
`SCORECARD.md` 0, `LOG.md` 0, `corpus/SOURCES.md` 0 — all append-only. `PROVINCE.md` and
`SHONEN.md`: untouched. Pair-wise sweep (R26): `ce73ccaf→743ce449` 0, `743ce449→60b5636f` 0,
`60b5636f→c450cd68` 0, **`c450cd68→69474c55` 1** (the SKILL.md row — F2), `ce73ccaf→69474c55` 0.
Receipt 07.

## 6. Harm falsifier — no regression at the tip; one regression window (F1)

No-regression at tip `69474c55`: r99 checker `PASS bindings 7/7 findings 0` (rows 165) —
identical to the baseline `ce73ccaf` reading (rows 163); r100 checker `PASS 7/7`;
`check-registry-coverage.py --revision 69474c55` → `PASS findings 0 missing 0 registered 165
rows_total 165 tools_total 165`; r99 battery `--runs 3` → `families_passed 105/105 verdict met`
×3, `failed_families []`, `cases 420`, **error_rows 0**, with `count-runs.py` naming
`REFUSAL-VERSIONS-9DIGIT [4,0]`, `REFUSAL-VERSIONS-9DIGIT-Y [4,0]`, `EXPLICIT-VERSION-ECHO [4,0]`;
r98 control battery `--runs 3` → `105/105 met` ×3 (still blind on Y at the un-bent gate);
selftests r99 `17/17`, r100 `26/26`, r99 battery `5/5`. Receipts 08, 13.

## 7. Findings

### F1 — published transient `CANNOT_EVALUATE` at the land commit `c450cd68` (severity: medium; repaired at the tip)

The land commit writes the `check-registry-content-r100` SKILL.md registry row with **7 of 8 cells**
(the write-scope cell is absent). Measured with the instrument's own `split_row` on the committed
bytes: line 5951 → `ncells 7` at `c450cd68`, `ncells 8` at `69474c55` (rows 5949/5950 are 8/8 in
both). At `c450cd68` all three previously-certified gates read `CANNOT_EVALUATE`, exit 2:

```
r99  checker : {"findings":[{"detail":"malformed registry row at line 5951","id":"E-TABLE","site":"SKILL.md"}],"status":"CANNOT_EVALUATE"}
r100 checker : same (E-TABLE)
coverage gate: {"counts":{"findings":1,"missing":0,"registered":0,"rows_total":0,"tools_total":0},"findings":[{"id":"E-REGISTRY-TABLE",…}],"status":"CANNOT_EVALUATE"}
```

The same three gates at the baseline `ce73ccaf` read `PASS` (`PASS bindings 7/7 findings 0`;
coverage `PASS findings 0 registered 163 tools_total 163`). So the round *did* reduce a previously
certified surface — at that revision only. Both `c450cd68` and the repair `69474c55` are ancestors
of `origin/master` (published). Note the coverage gate degrades *silently* there: it reports
`tools_total 0` (no tools at all) rather than a table error.

Byte anchors (QUALITY 141, byte level): `grep -abo '| check-registry-content-r100 | gate |' SKILL.md`
→ **1625568**; the added write-scope cell text at **1626567** (two earlier hits 1588165 / 1588946
belong to other rows); row line number at the tip **5951**. Receipts 11, 12.

**L1 decision needed (one question) — RESOLVED.** The frozen C2 target says *"Live table at the
freeze tip and at the landing tip: status PASS, findings [], bindings 7/7 on r100; r99 reads
PASS 7/7 on the same table."* If "the landing tip" is `c450cd68` (the commit titled
`round-100: land`), that sentence is **false at that revision** (CANNOT_EVALUATE, exit 2). If it is
the last lane commit `69474c55`, it is **true** (PASS 7/7, 165/165 coverage).

**L1 ruling (`agent://TsukuroiR100`):** *"the landing tip" is the final round-100 lane tip at which
the round's landing is complete (`69474c55` and any later round-100 commit) — not an intermediate
commit superseded inside the round. C2's two named surfaces are the freeze tip (`743ce449`, table
163 rows) and the final landing tip, both PASS; the intermediate `c450cd68` malformed-row state is
a disclosed defect, not a scoring surface, and it is recorded as mistake
`R100-REGISTRY-ROW-CELL-COUNT` plus an amendment-slot clarification (A1). No widening or narrowing
of the enforced property.*

**Effect.** F1 is **closed on the scoring question** by that ruling: the surface C2 names is the
freeze tip and the final landing tip, and this seat measured both — `743ce449`: r99 `PASS bindings
7/7 findings 0` (rows 163), r100 `PASS 7/7`; `69474c55`: r99 `PASS bindings 7/7 findings 0`
(rows 165), r100 `PASS 7/7`, coverage `PASS findings 0 registered 165 tools_total 165`. The
`c450cd68` reading stands as a **disclosed defect** (the L1's `R100-REGISTRY-ROW-CELL-COUNT` +
amendment A1), not a scoring failure; the published-history exposure I flagged is unchanged by the
ruling. (The wave's `ExecRegistry` seat reported the same 7-of-8 defect independently —
`w1/ExecRegistry/report.md:280-294` — and asked the same question.)

**Smallest remediation:** no code change (the tip is green). Two records: (1) the round report
names which revision "the landing tip" denotes and records that `c450cd68` reads
`CANNOT_EVALUATE`; (2) the lesson/LOG discloses the repair (F2). Optional future hardening: run
`check-registry-coverage.py --revision <land>` *before* pushing the land commit — it would have
caught the 7-of-8 row before publication.

### F2 — the repair commit `69474c55` is disclosed in no record file (severity: medium; a QUALITY 60 / R26 disclosure defect)

QUALITY 60 (R26-UNDISCLOSED-INPLACE, with the round-26 clarification that the sweep covers every
record file **including `SKILL.md`** and must run over **each consecutive pair** of the round's
commits as well as base→head) requires the round lesson to list every removed or changed line of
the record files and to name the sweep whose output equals that list. The lesson says:

```
### In-place registry changes (old → new)

None — the round adds rows; no existing row's `status`, `recheck` or `used-by` changes.
```

but the pair sweep prints exactly one removed line:

```
$ git diff -U0 c450cd68 69474c55 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'
-| check-registry-content-r100 | gate | `python3 tools/check-registry-content-r100.py --revision <REV> …
removed_line_count=1
```

and `grep -rn "69474c55" SCORECARD.md LOG.md corpus/ .ufo/plans/` → **0 hits**: the repair commit
appears in no record file anywhere in the lane. `git diff --stat c450cd68 69474c55 -- SKILL.md` →
`1 file changed, 1 insertion(+), 1 deletion(-)`.

**Impact:** a reader of the lane's records sees "no in-place changes" for round 100 while the round
made one, and sees no mention of the commit that repaired the land. No axis score moves; the harm is
to the round's own disclosure obligation (and to the calibration of "the round changed nothing in
place").

**Smallest remediation:** append-only — the lesson gains a short correction to its
`### In-place registry changes` section naming the one removed line, the sweep command
(`git diff -U0 <base> <REV> -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ |
grep -E '^-[^-]'`) run over each consecutive pair, and the commit `69474c55`. No existing line is
rewritten. **Not done by me** — `corpus/` is outside this seat's write scope.

**L1 response:** *"I am appending the lesson correction now (pair sweep `c450cd68→69474c55`, the
one removed SKILL.md row line, and the commit). No further action needed from you; file your report
as-is with this ruling named."* At this seat's last check the lesson still read
`None — the round adds rows` and `grep -n 'R100-REGISTRY-ROW-CELL-COUNT'` over
`corpus/lessons/round-100.md` found no entry — the correction is **in flight**, owned by the L1
(the L1's `corpus/` edits are outside this seat's write scope, so this seat did not and cannot make
it). F2 is **not yet discharged**; it is discharged when that append lands.

### F3 — observation (not a fault): `before/census-before-after.txt` extended after the freeze (severity: low)

The freeze commit wrote `.ufo/waves/round-100/before/census-before-after.txt` with the *before*
block only (578 bytes); the land commit appended the *after* census block (file 578 → 1030 bytes,
**frozen 578-byte prefix byte-identical**: `b[:len(a)]==a` → True, 452 bytes appended). The edit is
append-only and the lesson declares the mechanism ("the after block is appended the same way"), but
the file lives in the round's *frozen* `before/` directory, and round-99's precedent froze that file
with both blocks already present. The pin manifest does not cover it (§1), so `sha256sum -c` cannot
flag it. No frozen byte was destroyed. The L1 may prefer the next round's shape to freeze the
complete receipt rather than extend a `before/` file after the freeze.

## 8. Credential / host guard — PASS

**Secrets** (families: `ghp_` / `gho_` / `github_pat_` / `glpat-` / `AKIA` / `AIza` / `sk-` / `xox` /
PEM private-key header / JWT `eyJ…`): wave dir **401 files scanned, 0 files with hits, 0 hits**;
`after/` 28 files → 0; the two new record files → 0. Counts only; no value printed. Receipt 09.

**Host mutations** (`\bsudo\b|sysctl|swapon|systemctl|mkinitcpio|insmod|modprobe|setcap`): raw hit
lines over the wave dir = **23**, all text — 4 in each frozen bend file (the gate's own docstring /
usage text, byte-identical to `tools/check-limine-pins.py` lines 59, 60, 525), the rest in
`make-spec.py` / `w1-dispatch.json` / `w1-spec.json` (the seat prompt quoting the operator's rule).
**Executed** privileged commands in receipts: **0**; sysctl/`/etc/sysctl`/boot writes in receipts:
**0**. No receipt shows a privileged invocation, service restart, module load or `/boot` write. This
seat ran no `sudo`, no pacman transaction, and touched no PATH directory. Receipt 10.

## 9. Tooling

No tool was installed or upgraded — nothing in this assignment required one. No pacman / `uv tool` /
`npx` / `~/.local/bin` transaction was performed, so there is nothing to record on that line.

## 10. No cleanup performed

Nothing outside this seat's own directory and scratch was deleted or edited by this seat. The two
findings are reported, not repaired: F2's fix belongs to `corpus/` (outside this seat's scope) and
F1's adjudication belongs to the L1.

{"seat":"SentinelHarm","verdict":"findings","notes":"Round 100 harms no axis at the tip 69474c55: manifest 16/16 OK at worktree and at the freeze 743ce449; freeze diff names only the freeze paths (22 files, all A); gate/r99 battery/r98 battery/r99 checker byte-identical to ce73ccaf; axis files untouched at the freeze and append-only base->tip (0 removed lines each); PROVINCE.md and SHONEN.md untouched; fleet and lane status sweeps show no round-100 misroot outside the lane repo; no-regression runs all green (r99 checker PASS 7/7 rows 165, r100 PASS 7/7, coverage PASS 165/165 findings 0, r99 battery met 105/105 x3 error_rows 0 with count-runs naming the three echo families 4/4, r98 control met 105/105 x3, selftests 17/17, 26/26, 5/5); credential scan 0 hits over 401 files, host-mutation scan 23 text hits all inherited docstring/prompt text with 0 executed privileged commands; no tool installed. TWO FINDINGS: F1 the land commit c450cd68 (published, on origin/master) writes the check-registry-content-r100 SKILL.md registry row with 7 of 8 cells (split_row: line 5951 ncells 7), so r99 checker, r100 checker and check-registry-coverage all read CANNOT_EVALUATE exit 2 at that revision while all three read PASS at ce73ccaf and at the tip 69474c55 - the C2 frozen target 'live table at the landing tip: status PASS' is false if 'landing tip' denotes c450cd68 and true if it denotes 69474c55, so the L1 must adjudicate which revision the frozen sentence names (byte anchors: row 1625568, write-scope cell 1626567, line 5951). F2 the repair commit 69474c55 is disclosed in no record file (grep over SCORECARD.md/LOG.md/corpus/.ufo/plans = 0 hits) and the lesson's 'In-place registry changes: None' contradicts the R26 pair sweep git diff -U0 c450cd68 69474c55 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]' which prints exactly 1 removed line, so QUALITY 60 wants an append-only lesson correction naming that line, the sweep and the commit. F3 observation: before/census-before-after.txt was appended after the freeze (578 -> 1030 bytes, frozen prefix byte-identical) and is not pinned by the manifest so sha256sum -c cannot flag it. No host mutation, no credential, no misroot, nothing cleaned by this seat."}
