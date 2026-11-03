# E1LineEnd — C1-BUILD (round 64 / hyaku run 15 / w1)

Seat: E1LineEnd, executor, claim C1 (operability). Host: Arch, kernel 7.2.11 (canonical
Linux/omp host). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, base rev
`2f3061ef` (declaration commit). No commit, no push, no other tracked file touched.

## What I changed

| Path | Change | Shape |
|---|---|---|
| `corpus/SOURCES.md` | 381 CR bytes stripped | 381 del / 381 ins, no content change |
| `SKILL.md` | 5452 CR bytes stripped | 5452 del / 5452 ins, no content change |
| `SCORECARD.md` | 4723 CR bytes stripped | 4723 del / 4723 ins, no content change |
| `tools/check-line-endings-r64.py` | **new** guard tool (350 lines, stdlib only) | sha256 `15f0e65c889acc3b591ca44c7e52fe16fa14d79c367e743ebcc905b17d50c030` |

Command used for the repair, per file: `sed -i 's/\r$//' F` (removes exactly a CR that
immediately precedes a newline).

### Byte-precise justification of "exactly trailing CRs"

Measured on the pre-normalization worktree, before the sed pass:

```
corpus/SOURCES.md total_CR=381  CR-at-line-end=381  lines=381  last_byte=0a
SKILL.md          total_CR=5452 CR-at-line-end=5452 lines=5489 last_byte=2e
SCORECARD.md      total_CR=4723 CR-at-line-end=4723 lines=4723 last_byte=0a
```

Every CR in every file sat before a LF (`total_CR == CR-at-line-end` in all three), and
`SKILL.md`'s last byte is `2e` (`.`), so no CR-at-EOF case existed — the sed removed
exactly the CRs and had no other byte to touch.

## Evidence (all under `.ufo/waves/round-64/after/`)

### 1. `c1-census-end.txt` — the claim's own gate now passes

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
rc=0
42	W04
1	ok
```

Start receipt (`before/census-start-receipt.txt`): `rc=1`, `E12-count: 278`. End: `rc=0`,
**0 E-code findings**. Verdict row: `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`.

W04 disclosed: **42**, all class `W04` (`duplicate url ... across scopes`) — a
pre-existing warning class that never affects status. The start receipt recorded
`W04-count: 0` not because warnings were absent but because the run **aborted on E12
before reaching the warning pass**; the number only becomes observable once E12 is fixed.
Full 43-line output is in the receipt.

### 2. `c1-cr-identity.txt` — content bytes unchanged

Three runs, all silent, all rc 0:

```
$ git show 2f3061ef:corpus/SOURCES.md | tr -d '\r' | cmp - <lane>/corpus/SOURCES.md   → output: <empty>  rc=0
$ git show 2f3061ef:SKILL.md          | tr -d '\r' | cmp - <lane>/SKILL.md            → output: <empty>  rc=0
$ git show 2f3061ef:SCORECARD.md      | tr -d '\r' | cmp - <lane>/SCORECARD.md        → output: <empty>  rc=0
```

Three independent cross-checks that the diff is *only* CR removal:

- `git diff --ignore-cr-at-eol --stat` → **empty** (a non-CR byte change would show here).
- `git diff --numstat` → `4723/4723 SCORECARD.md`, `5452/5452 SKILL.md`, `381/381
  corpus/SOURCES.md`: deletions == insertions == that file's measured CR count, i.e. one
  line rewritten per stripped CR.
- Line counts identical to `git show 2f3061ef:F | tr -d '\r' | wc -l`: 381 / 5489 / 4723.

Changed-path set at end of seat: ` M SCORECARD.md`, ` M SKILL.md`, ` M corpus/SOURCES.md`,
`?? tools/check-line-endings-r64.py`. Nothing else.

### 3. `c1-guard-selftest.txt` — PASS line, verbatim

```
$ python3 tools/check-line-endings-r64.py --selftest --work /fast/scratch/hyaku/tsukuroi-r64/E1LineEnd
check-line-endings-r64 selftest (fixtures under /fast/scratch/hyaku/tsukuroi-r64/E1LineEnd)
  lf-file-passes                       PASS
  crlf-file-fails-naming-path          PASS
  allowlisted-ufo-path-ignored         PASS
  cr-at-eof-without-newline-flagged    PASS
  cr-midline-flagged                   PASS
CHECK_LINE_ENDINGS_SELFTEST: PASS (5 cases, 5 passed, 0 failed)
rc=0
```

The receipt also records that the fixture base is empty of fixtures after exit (the
`try/finally` cleanup ran) and that `$TMPDIR` — not any hardcoded `/tmp` — supplies the
base when `--work` is absent.

### 4. `c1-guard-check.txt` — repo is clean under the new guard

```
$ python3 tools/check-line-endings-r64.py --check --root /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
CHECK_LINE_ENDINGS: PASS (326 file(s) checked, 0 violation(s))
check-line-endings-r64: 22370 allow-listed .ufo path(s) skipped (upstream captures)
rc=0
```

Guarded-set composition from `git ls-files` (22712 tracked paths → 326 checked):
canonical top level `AGENTS.md LOG.md MINT.md PROVINCE.md SCORECARD.md SHONEN.md
SKILL.md` (7) + `corpus/` 208 + `plans/` 18 + top-level `tools/*.py` 93. Allow-listed
tracked paths (`.ufo/**`, 22370) are never flagged; an explicit `--check .ufo/...`
argument is skipped too (probed live in the receipt). Exit-code contract exercised in the
same receipt: no mode → 2, non-git `--root` → 2 (cannot-evaluate is never "clean"),
missing path → 2, clean tree → 0.

### 5. `c1-mutant-kill.txt` — the guard kills the mutant, and retro-detects the real damage

```
$ python3 tools/check-line-endings-r64.py --check --root <scratch>/mut mutant-cr.md
check-line-endings-r64: 1 violation(s)
  mutant-cr.md:15: CR byte at offset 5000
CHECK_LINE_ENDINGS: FAIL (1 file(s) checked, 1 violation(s))
rc=1
```

Controls in the same receipt: the unmutated copy PASSes (so the FAIL is caused by the CR
alone), and the r59 damage *shape* (one CRLF inserted at offset 200) FAILs.

The decisive case, also in that receipt: run the guard against the **actual** r59 bytes
recovered with `git show 2f3061ef:F` into a scratch root —

```
check-line-endings-r64: 3 violation(s)
  corpus/SOURCES.md:1: CR byte at offset 35
  SKILL.md:1: CR byte at offset 3
  SCORECARD.md:1: CR byte at offset 33
rc=1
```

— it names exactly the three files the C1 claim names and no fourth file. So the guard
both reproduces the historical damage (red-before is now mechanical, not narrative) and
is green on the repaired tree.

## Guard design, in one paragraph

`tools/check-line-endings-r64.py` (Python 3 stdlib: argparse, os, shutil, subprocess,
sys, tempfile) fails any guarded tracked file containing a `0x0D` byte wherever it sits
— before a newline, mid-line, or at EOF without a newline — reporting path, 1-based line
and byte offset. Guarded set comes from `git -C <root> ls-files`, so it tracks the index
rather than a hand-maintained list. Top-level `.ufo/**` is allow-listed because those are
verbatim upstream captures (HTTP headers, patches, raw tool output) whose CRLF is the
evidence; the anchor is the leading component only, so a nested `corpus/.ufo/` buys
nothing.
Exit 0/1/2 = clean/violations/cannot-evaluate. `--check [paths...] --root R --work D`,
`--selftest`. Scratch base precedence `--work` → `$HYAKU_SCRATCH` → `$TMPDIR` →
`/fast/scratch/hyaku`; `/tmp` is never hardcoded and never citable. A guarded path that
`git ls-files` names but the worktree no longer has is reported as rc 2 (cannot evaluate)
with the path named — never silently counted as clean bytes it did not read — and the
same rule is probed in a fixture repo inside `c1-guard-check.txt`. Read-only apart from
the self-deleting selftest fixture tree; no `__pycache__` residue (`sys.dont_write_bytecode`
is not needed — the tool is run as a script, and the stray `.pyc` from my import-based
probes was deleted).

## Risks / notes for the L1

- **The 42 W04s are not mine to fix and are not new.** They are upstream-duplicate-URL
  warnings in `corpus/SOURCES.md` rows; they never change status. If the round's claim
  text expects "zero findings" without qualification, it should say "zero E-codes,
  42 pre-existing W04".
- **`git diff` for these three files is huge by line count** (10 556 changed lines) and
  looks like a rewrite at a glance. It is not: `--ignore-cr-at-eol` is empty and
  numstat del==ins==CR-count. Land with that fact available, or a later reviewer will
  read it as content churn.
- **The guard is not wired into anything.** Nothing invokes it yet — no census hook, no
  pre-commit, no round runner. That wiring was not in this seat's item, and touching the
  fleet-root `scripts/` is out of my write surface. As landed, the guard is a manual
  gate; the class can recur silently until the L1 (or a later round) calls it from the
  census or a round runner. This is the one open operability gap I can name.
- **Guarded-set scope is deliberate and narrow**: top-level canonical docs, `corpus/`,
  `plans/`, top-level `tools/*.py`. Nested tool subtrees are not guarded — a deliberate
  limit (nothing there is canonical source yet), but it means a future `tools/lib/*.py`
  escapes the guard by construction.
- Scratch `/fast/scratch/hyaku/tsukuroi-r64/E1LineEnd` removed at the end of the seat;
  all receipts copied into `.ufo/waves/round-64/after/` first.
- **This path keeps getting regressed by other seats — three separate occurrences.** The
  authoritative sequence for `corpus/SOURCES.md` this wave:
  `18:37` repaired → `18:43:21` guard catches 381 CRs → `18:43:5x` restored to `e1558e4b` →
  `18:44:30` rewrite, same LF digest → `18:47:32` **full regression**: mtime moved,
  size `279287`, sha `2349bfda141ab055…` = the committed `2f3061ef` blob byte-for-byte
  (caught by seat CN1Siblings, reproduced by me at `18:55:56Z`) → `18:56` repaired again.
  Every CRLF state was caught by the guard; the repaired digest is reproducibly
  `e1558e4b3eeef885…` each time (CR strip is idempotent).
- **Mechanism (measured by CN1Siblings, consistent with my numbers).** (i) The E12 flood is
  heading-anchored: one CR inside the `## Registry` heading makes the census read all 278
  rows as outside-Registry — which is exactly why 278 E12 and not 381 or something else.
  (ii) Any `git checkout-index -f` / `git restore` / `git checkout --` on this detached
  HEAD re-materialises the CRLF HEAD blob at that path. Avoid those three commands on this
  file. **Attribution to R1C1Rev was withdrawn** (it proved `git -C <absolute-clone>` put
  its `checkout-index` in its own clone, and its 18:40:53Z lane measurement showed mtime
  `15:37:05`, CR=0); the seat that ran the 18:47:32Z restore is unidentified.
- **The L1 must re-run `--check` and the census after integration**, and should land the
  fix with a `git add` of the normalized blobs rather than any form of worktree restore.
  The guard is what makes the regression visible in one command; that is its main value
  in this wave.
- **Review findings F1/F2 were valid and are now fixed in the tool.** F1: the docstring
  said the allowlist was a *leading* `.ufo` component while the code accepted any component,
  so `corpus/.ufo/x.md` silently escaped. `is_allowlisted` is now anchored to
  `parts[0] == ".ufo"`, and `c1-guard-check.txt` shows the nested case now FAILs (rc 1) while
  a top-level `.ufo` path is still skipped. F2: default mode always printed "0 allow-listed"
  because the set was pre-filtered; it now prints
  `check-line-endings-r64: 22370 allow-listed .ufo path(s) skipped (upstream captures)` as a
  separate disclosure line.
- **Review finding F4 was an unintended live test of my repair, and it passed.** The
  reviewer's `git checkout-index -f` rewrote `corpus/SOURCES.md` from the index (the CRLF
  blob) and the guard flagged `corpus/SOURCES.md:1: CR byte at offset 35` — the guard
  catches the real pre-fix committed state, not just fixtures.
- **Bounded binary caveat (review §5c, accepted):** the guard is a byte scanner with no
  text/binary sniffing, so a guarded *binary* containing a CR would fail as a false
  positive. Today's guarded set is 100 % text (mime sweep in the review: 197 text/plain,
  24 application/json, 1 text/html, 1 text/javascript, 3 text/x-script.python, 0 binary).
  Not a defect now; a future guarded binary would need an extension filter, not a
  line-ending rewrite.

## Retained evidence index

- `.ufo/waves/round-64/after/c1-census-end.txt` — rc 0, 0 E-codes, 42 W04, full output
- `.ufo/waves/round-64/after/c1-cr-identity.txt` — 3× stripped-base `cmp` rc 0 + 3 cross-checks
- `.ufo/waves/round-64/after/c1-guard-selftest.txt` — `CHECK_LINE_ENDINGS_SELFTEST: PASS (5 cases, 5 passed, 0 failed)`
- `.ufo/waves/round-64/after/c1-guard-check.txt` — `PASS (326 file(s) checked, 0 violation(s))`, allowlist anchoring, symlink case, exit-code contract
- `.ufo/waves/round-64/after/c1-mutant-kill.txt` — mutant rc 1 naming the path + real-damage retro-detection

## Tooling

No installs, no upgrades. System Python 3.14.8. `sed`, `cmp`, `tr`, `git` (plumbing reads
only) — all pre-existing.
