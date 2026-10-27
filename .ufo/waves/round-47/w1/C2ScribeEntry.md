VERDICT: draft

Seat `C2ScribeEntry`, item **C2-D1** (round 47, w1): draft the lesson knowledge note for the TMPDIR-space
contract and the before->after measurement line. Draft only — no lane file was created, edited or deleted, no
counter or selftest was run, no tool was installed. The two exact-prose blocks the item asks for are under
"Proposed text 1" and "Proposed text 2"; everything else is the evidence those blocks rest on and the
discrepancies the L1 should decide on before pasting.

## What I read (all read-only, in place)

| Path | What it gives |
|---|---|
| `tools/tsukuroi-census.sh:850-866` | `root_locator_class`: `unsafe` arm at `:859` (`*[!A-Za-z0-9._/+-]*)`), `absolute` at `:860`; rationale comment `:851-854` |
| `tools/tsukuroi-census.sh:2050-2059` | the `(R47-C2)` guard comment, `local st_base=${TMPDIR:-/tmp}` (`:2055`), charset reset to `/tmp` (`:2057`), `work=$(mktemp -d "$st_base/…")` (`:2059`) |
| `tools/tsukuroi-census.sh:3473-3482` | the two `(R47-C2)` pinning cases (`ok`/`bad` labels at `:3477`, `:3481`) |
| `tools/tsukuroi-census.sh:3484-3486` | summary `printf` and `[ "$FAIL" -eq 0 ]` (the exit 1 on any failure) |
| base `9160190 tools/tsukuroi-census.sh:2048`, `:857` | no fallback (`work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`); same `unsafe` arm |
| `git diff 9160190 HEAD -- tools/tsukuroi-census.sh` | 4 hunks (`@@ -408,7 +408,8 @@`, `@@ -598,7 +599,8 @@`, `@@ -2045,7 +2047,16 @@`, `@@ -3459,6 +3470,17 @@`), 25 insertions / 3 deletions; every hunk is a comment, the usage text, `run_selftest`, or the new cases — no probe, verdict arm or exit-map line is touched |
| `.ufo/waves/round-47/frozen/src/mktemp.html:94-99`, `SHA256SUMS`, `FETCH.txt` | S252 snapshot; `sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`, FETCH line 1 `2026-10-27 fetch (L1, round 47 start)` |
| `corpus/SOURCES.md:261` | S252 row, registered quote: `-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set` |
| `.ufo/waves/round-47/controls/battery.py:212-250` | C2-K0 clone at `BASE`, C2-K2 guard-strip, C2-K-pass at `IMPL`; each sets `TMPDIR=<clone>/t 2` with only `PATH`/`LC_ALL`/`TMPDIR` in `env` |
| `.ufo/waves/round-47/controls/battery-summary-r47.jsonl:10,11,12` | the three observed C2 control lines quoted below |
| `.ufo/waves/round-47/w1/C2ExecTmpdir/{baseline-space,tab,newline,trailing-space}.log:1-5` | four live runs of the lane script at HEAD, `rc: 0`, `PASS (164 cases, 164 passed, 0 failed)` |
| `/fast/scratch/hyaku/tsukuroi-r47/l1-before/selftest-space-before.log:1-5,165` | the L1's own before run under a space `TMPDIR`: first FAIL line shows `exit 2 wanted 0` with `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED …)`; final line `TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)` |
| `corpus/lessons/round-47.md:1-20` | where the note goes (C2 bullet at `:18-20`) |
| `corpus/lessons/round-46.md:14,23` | the carried finding (`Found, not claimed: the census selftest fails 149/160 when TMPDIR contains a space`) and the round-46 counter's own `selftest_r46 8` |

Version anchor: census `sha256 adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41` at `HEAD f6bc6d05`
equals its worktree bytes and equals the bytes at the freeze `77e9e2b2`; introduced in `3629c46a`
(`git merge-base --is-ancestor 3629c46a 77e9e2b2` prints "3629c46a is ancestor of 77e9e2b2").

## Proposed text 1 — lesson knowledge note (exact prose)

Placement: `corpus/lessons/round-47.md`, expanding the C2 bullet of `## Outcome` (`:18-20`) into the subsection
below, placed before `## Gate`.

> ## The selftest TMPDIR-space contract (R47-C2)
>
> `run_selftest` hands its fixture roots to the census as caller root overrides, and `root_locator_class`
> (`tools/tsukuroi-census.sh:850`) refuses by design any non-absolute path and any path holding a character
> outside `[A-Za-z0-9._/+-]`: a space, a tab or an `=` classifies `unsafe` (`:859`) and the raw path is never
> echoed or stat'd, so `/x root_mode=0755` can neither forge a token nor reach `stat`. `mktemp` does not cover
> for that: it substitutes `$TMPDIR` only for its own default template and under `-p`/`-t` ("interpret TEMPLATE
> as a single file name component, relative to a directory: $TMPDIR, if set", S252; the `-p` wording at
> `.ufo/waves/round-47/frozen/src/mktemp.html:94-96`), while an explicit TEMPLATE is used verbatim — so
> whichever caller interpolates `TMPDIR` inherits its characters. The guard therefore lives in the harness:
> `st_base=${TMPDIR:-/tmp}`, reset to `/tmp` when `TMPDIR` holds a character outside that set, then
> `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` (`:2055-2059`). At base `9160190` the reset was
> absent (`:2048`), and a space in `TMPDIR` turned 149 of 162 cases red as `BLOCKED`/exit 2 — a caller's naming
> choice reading back as a host fault. Two `(R47-C2)` cases now pin the contract (`:3473-3482`): the work dir
> classifies `absolute` however dirty `TMPDIR` is, and `$work/fx/sp dir/root` classifies `unsafe` by design.
> Remove the reset and keep the cases and only the first pin goes red (control K2: `FAIL (164 cases, 14
> passed, 150 failed)`); the refusal pin stays green because it tests the locator, not the harness.

Every assertion in that paragraph maps to an anchor above; the one non-obvious step is "an explicit TEMPLATE is
used verbatim", which is the absence of any `$TMPDIR` rule for a plain `mktemp -d TEMPLATE` call in
`mktemp.html:72-99` (`$TMPDIR` appears only in the default-template sentence `:77-78` and under `-p` `:94-96` /
`-t` `:101-102`), and which the four live runs confirm behaviourally (`tab`, `newline`, `trailing-space` all fall
back and pass, so nothing in `mktemp` is rewriting the caller's `TMPDIR`).

## Proposed text 2 — before->after measurement line (exact prose)

Compact form for the report/lesson table:

> `FAIL (162 cases, 13 passed, 149 failed)` at base `9160190` → `PASS (164 cases, 164 passed, 0 failed)` at census
> `sha256 adb1b4ce…` (`3629c46a`; unchanged at the freeze `77e9e2b2`), rc 0, under the frozen counting command.

Sentence form, if the report wants one line of prose:

> Under the frozen counting command (`S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C
> TMPDIR="$S/t 2" bash tools/tsukuroi-census.sh --selftest`) the selftest reads `FAIL (162 cases, 13 passed, 149
> failed)`, rc 1, at base `9160190` — the fixture root overrides under a space `TMPDIR` class `unsafe`, so the
> probes reading them return `BLOCKED`/exit 2 — and `PASS (164 cases, 164 passed, 0 failed)`, rc 0, at the
> candidate census.

Provenance of each number (observed, not transcribed):

- before, tracking clone: `battery-summary-r47.jsonl:10` — `"control": "C2-K0 do-nothing (base census, space
  TMPDIR)", "detail": "TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)", "observed": "FAIL"`;
  the clone is `fixture('c2-k0', rev=BASE)` (`battery.py:212`) with `TMPDIR=<clone>/t 2` (`:214-215`).
- before, lane's own run: `/fast/scratch/hyaku/tsukuroi-r47/l1-before/selftest-space-before.log:165`
  (same final line; mechanism at `:1-5`).
- before rc 1: `SCORECARD.md` C2 row ("FAILs 13/162 (149 failed, rc 1)") and `tools/tsukuroi-census.sh:3486`
  (`[ "$FAIL" -eq 0 ]` is the function's last command).
- after, tracking clone: `battery-summary-r47.jsonl:12` — `"control": "C2-K-pass candidate", "detail":
  "TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)", "observed": "PASS"` (clone at `IMPL`
  77e9e2b2, `battery.py:243-249`).
- after, live lane script: `w1/C2ExecTmpdir/baseline-space.log:1-5` (`# rc: 0`, `# final-line:
  TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`), plus `tab.log`, `newline.log`,
  `trailing-space.log` with the same `rc: 0` / `164 passed` line; `grep -c '^FAIL' baseline-space.log` → `0`.

## Findings

**F1 (supports the claim).** The base failure is a classification false-red, not a host fault: base
`9160190:2048` built the tree under `${TMPDIR:-/tmp}` unconditionally, so with a space in `TMPDIR` every fixture
root override classed `unsafe` and the probes reading them returned `TSUKUROI_CENSUS: BLOCKED
(packages=BLOCKED …)` with `exit 2 wanted 0`
(`l1-before/selftest-space-before.log:1-5`). The 13 base passes are exactly the cases that do not read a
fixture root override.

**F2 (note for the L1 — the frozen command exercises the /tmp fallback).** The declared counting command sets
`TMPDIR="$S/t 2"`, which contains a space, which the new reset at `tools/tsukuroi-census.sh:2057` turns into
`st_base=/tmp`; the fixture tree of every run of the frozen command therefore lands under `/tmp`, not under the
seat's scratch. That is the fix working as designed, and the executor's receipts show it
(`C2ExecTmpdir/*.log:1-5`). It does mean the seat rule "never build under /tmp" cannot be honoured by a seat
that runs the frozen counting command verbatim; no seat should be faulted for it, and no `/tmp` path from these
runs should be cited as evidence (the receipts are the lane-side logs, which is what I cite).

**F3 (citation nit in the declaration).** The C2 row's "Before at base" cell points at
`.ufo/waves/round-47/before/`, but that directory holds only `sources-census-start.txt` (tracked, added in
3629c46a) and `c1-before-base.jsonl` (untracked C1 evidence). The C2 before bytes exist only in
`controls/battery-summary-r47.jsonl:10` and the L1's `/fast/scratch/…/l1-before/selftest-space-before.log:165`.
The report/lesson should cite those two, not `before/`, or the before leg reads as unreceipted.

**F4 (able-to-fail asymmetry — worth one clause, already in the draft).** Control K2 (guard removed, cases kept)
is `FAIL (164 cases, 14 passed, 150 failed)` (`battery-summary-r47.jsonl:11`): 14 = 13 + 1, i.e. exactly the new
fixture-base pin flips red while the whitespace-refusal pin stays green by construction. The note says so; a
reader should not read "two pinning cases" as two independent failure detectors.

**F5 (count discrepancy in the C2 kill rule).** The declaration's C2 kill rule says "all six (R46-C1) cases still
pass". The script carries **eight** labelled `(R46-C1)` cases — six `identity:` + two `cli:` (`tools/tsukuroi-census.sh:3429-3470`) —
and the live run prints eight `PASS … (R46-C1)` lines (`C2ExecTmpdir/baseline-space.log`, `grep -o
'^PASS .*(R46-C1)' | sort -u | wc -l` → 8). "Six" matches the round-46 *first landing* figure
(`corpus/lessons/round-46.md:14`: "… selftest_r46 8; also PASS at the first landing `a4477049` (…,
selftest_r46 6)"). The 164 = 162 + 2 arithmetic is unaffected. Suggest "all eight (R46-C1) cases" or "the six
`identity:` (R46-C1) cases".

**F6 (carried-count drift, minor).** The round-46 lesson's carried finding reads "fails 149/160"
(`corpus/lessons/round-46.md:23`) while the round-47 base reads 149/**162** — the base grew by an earlier
round-46 landing. Any note that quotes the carried number should quote it as historical, as the draft does not.

**F7 (source-grounding nuance the draft keeps honest).** The registered S252 quote is the `-t` form, and the
census selftest does not use `-t` (it passes an absolute TEMPLATE). The note therefore does not claim "mktemp
uses TMPDIR" for this call; it claims mktemp's TMPDIR rule exists for the default template and `-p`/`-t`, and that
an explicit template is used verbatim. If the L1 prefers the stricter registration, the `-p` sentence
(`mktemp.html:94-96`) is ≤25 words and can replace the `-t` quote in the S252 row; that is a `corpus/SOURCES.md`
edit, outside this draft seat.

## Gates and limits

- No selftest, no counter, no fixture, no scratch: the item is report text, and the frozen counting command
  routes the fixture tree to `/tmp` (F2), which the host guard forbids me to build under. Every number above is
  read from an existing receipt, and each is named with `path:line`.
- Not evaluated by me (other seats own them): the live census output digits-stripped base-vs-final comparison,
  `--identity` line shape, and the exit map. I note only that the base->HEAD census diff is 4 hunks confined to
  comments, usage text, `run_selftest` and the two new cases, and that `C2ExecTmpdir` logs show
  `grep -c '^FAIL' … → 0` and `rc: 0`.
- Touched surfaces: this report only. Nothing under `corpus/`, `tools/`, `SCORECARD.md`, `LOG.md` or any seat
  sibling was written; no git/jj mutation; no agent dispatched (leaf).
- Out of scope for C2-D1: editing `corpus/lessons/round-47.md`, `corpus/SOURCES.md` and the declaration kill-rule
  wording (F3-F5) — all L1 integration decisions.

## Artifacts

- Report: `.ufo/waves/round-47/w1/C2ScribeEntry.md` (this file).
- Receipts: none copied — every piece of evidence is an existing lane file read in place; no scratch dir was
  created under `/fast/scratch/hyaku/tsukuroi-r47/C2ScribeEntry`.
