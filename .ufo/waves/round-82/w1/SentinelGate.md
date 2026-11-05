# SentinelGate — round 82 w1 (fail-closed, TMPDIR, host safety, over-claim)

Read-only in the lane; wrote only this file. Frozen commit `2786562e49d71e0b3962ad996397c010cf787b16`; the L1
committed the candidates as `f376054a734623c919da3bfc5a6f05b39ff9a9e2` while this seat ran, so every statement
below is re-anchored there. Instruments and recipes still equal the frozen hashes at `f376054a`: `fedd45ce…c3b3`,
`6e6d9715…7c24`, `888a3da9…1e84`, `5e176afc…cb43`.

After-state I measured myself at `f376054a` (matches `.ufo/waves/round-82/after/commands.txt`):
```
C1 -> {"count": 8, "target": 8, "finding": "met"}                                       rc=0
C2 -> {"killed": 22, "total": 26, "genuine_killed": 16, "finding": "unmet",
       "survivors": ["C06-source-id-shape","C07-own-work-rejection",
                     "C16-empty-manifest","M06-mutation-unlink-noop"]}                   rc=1
C3 -> {"count": 0, "examined": 77, "finding": "clean", "findings": []}                  rc=0
```
C1 and C3 met; C2 unmet for a frozen-data reason, not for want of work (R82-V1: 22 and 16 are the maxima).

## 1 — fail-closed (cannot-evaluate for absent/unusable input, never a pass)

**C1 met.** Every unusable input raises `CannotEvaluate` → `main` rc 2: `check-anchor-coordinates.py:120,126,132,
136,139,142,151` (`absent-at-revision`, `snapshot-unnamed`, `entry-absent`, `entry-unreadable`, `snapshot-absent`,
`rows-absent`), `:294,302 return 2`. `met` needs the full target *and* the row count: `:169 finding = "met" if
count == target and len(rows) == target else "unmet"`. Observed on scratch fixtures: absent entry → `rc=2
entry-absent`; truncated entry → `rc=2 entry-unreadable:Unterminated string`; absent snapshot → `rc=2
snapshot-absent:systemd.mount.xml`; snapshot with raw line 3 deleted → `rc=1 count=0 unmet`; ambient `GIT_DIR`
at a foreign repo → `rc=2 absent-at-revision:corpus/knowledge/…json`.

**C2 met.** `recipes-absent` (`:81,83`); red pristine baseline → `CannotEvaluate` (`:107`); a recipe whose old
string no longer occurs is not a kill (`:114` → `recipe-missing`, `killed: false`); `met` needs both legs
(`:134`). Observed: recipes absent → `rc=2 recipes-absent`; one old string removed → `killed 5, genuine 0,
unmet rc 1`, `recipe-missing:old-string-occurs-0x`.

**C3 unmet — one leak (R82-V3).** `no-round-blocks` → `CannotEvaluate` (`:97`); absent fixture → rc 2. But in
`--revision` mode `:204` raises `CannotEvaluate` inside a `try` whose only handler is `except
_revision.RevisionError` (`:207`), so it escapes `main()`. Scratch repo whose tree lacks `SCORECARD.md`:
```
Traceback (most recent call last):
  File ".../check-scorecard-ordinals.py", line 204, in main
    raise CannotEvaluate(f"absent-at-revision:{SCORECARD}")
CannotEvaluate: absent-at-revision:SCORECARD.md
rc=1
```
Never `clean`, so it cannot pass — but cannot-evaluate is reported as exit 1 (= findings per the file's exit
table), with no JSON.

Tampering: single-sided never reaches `met` (C1 fixtures, C2 stale recipe above); two-sided *consistent* tampering
does — R82-V5, outside the frozen predicate but inside "a tampered input cannot produce met".

## 2 — TMPDIR: nothing written outside the scratch root

**met.** `grep -n '/tmp' tools/check-anchor-coordinates.py tools/mutation-kill-r82.py
tools/check-scorecard-ordinals.py` → no matches (rc 1). All three use `tempfile.TemporaryDirectory`
(TMPDIR-aware); C2's child env is an allow-list (`PATH`, `TMPDIR`, `PYTHONDONTWRITEBYTECODE`, `LC_ALL`, `:62-63`)
with `cwd=work`. With a real pre-created TMPDIR per instrument:
```
TMPDIR=$S/tmp/c1 …/check-anchor-coordinates.py   --selftest -> rc=0 total=12 passed=12 failed=0
TMPDIR=$S/tmp/c2 …/mutation-kill-r82.py          --selftest -> rc=0 total=4  passed=4  failed=0
TMPDIR=$S/tmp/c3 …/check-scorecard-ordinals.py   --selftest -> rc=0 total=8  passed=8  failed=0
find $S/tmp/{c1,c2,c3} -mindepth 1 -> (empty, all three)
find <lane> -newer <marker> -type f -not -path './.git/*' -not -path './.ufo/waves/round-82/w1/*' -> (none)
```
`--revision` runs added no bytecode (`ls -la tools/__pycache__` before/after identical: `sys.dont_write_bytecode`
is set before importing `_revision`). `--work DIR` is caller-owned and not removed (`if work is None:
shutil.rmtree`), so my run left 1012K in my scratch only. Caveat: a driver that *imports* a lane instrument
writes `tools/__pycache__/<tool>.cpython-314.pyc` into the lane (R82-V6).

## 3 — host safety

**met.** No pacman, no sudo, no service restart, no unit start; no tool installed or upgraded; writes only to
`/fast/scratch/hyaku/tsukuroi-r82/SentinelGate/` and this report.
```
grep -rInE 'op://|ghp_|sk-|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}' \
  .ufo/waves/round-82/ tools/{check-anchor-coordinates,mutation-kill-r82,check-scorecard-ordinals}.py \
  corpus/knowledge/mount-unit-fstab-plane-r81.{json,md}
```
→ 3 hits, all non-credentials: `w1-dispatch.json:241` and `w1-spec.json:71` are the seat spec's own pattern text;
`corpus/knowledge/mount-unit-fstab-plane-r81.md:73` matched `sk-` inside `dev-disk-by-…device`. No token, cookie,
session id, `op://` reference or private key in any file this round adds.
`grep -rInE '\bpacman\b|\bsudo\b|\bsystemctl\b|\bsystemd-run\b|\breboot\b'` over the same set → prose only
(census URL `man.archlinux.org/man/pacman.8`, dispatch/spec text, `w1/ExecMutCount.md:57` "No pacman, uv, npm or
cargo action"). Children spawned are exactly `git --no-pager -C <root> show <rev>:<path>` and `python3 <tool>
--selftest` (`check-anchor-coordinates.py:114-115`, `mutation-kill-r82.py:51-52,65-66`,
`check-scorecard-ordinals.py:199-200`).

## 4 — over-claim list (new prose landed by the wave)

1. `SCORECARD.md:6982-6983` (frozen declaration): "all eight rows … with the located span **exactly two lines
   later** than the cited one". False for 6 of 8 *cited ranges*: MT1 `[133,137]→[135,138]` +2, MT2
   `[498,503]→[502,503]` +4, MT3 `[481,487]→[486,487]` +5, MT4 `[489,491]→[491,492]` +2, MT5
   `[229,241]→[234,236]` +5, MT6 `[335,347]→[339,341]` +4, MT7 `[194,212]→[198,201]` +4, MT8
   `[254,265]→[259,260]` +5 (`.ufo/waves/round-82/before/controls.txt:22-29`). **Already disclosed**: the wave's
   `corpus/lessons/round-82.md` ("anchor-window-drift") records the same deltas and reframes the claim as
   quote-span-to-quote-span. I verified the reframing: strip span vs per-line-strip span is +2 on both ends for
   all eight (MT1 `(133,136)`→`(135,138)`, MT2 `(500,501)`→`(502,503)`, MT3 `(484,485)`→`(486,487)`, MT4
   `(489,490)`→`(491,492)`, MT5 `(232,234)`→`(234,236)`, MT6 `(337,339)`→`(339,341)`, MT7 `(196,199)`→`(198,201)`,
   MT8 `(257,258)`→`(259,260)`). Residual: the frozen sentence is still false as written; the lesson is the
   correction of record.
2. `corpus/knowledge/mount-unit-fstab-plane-r81.md` ("Coordinate convention"): "so `sed -n '135p;138p'` … shows
   MT1's quote". The quote spans raw 135-138; that command prints only lines 135 and 138 (observed: 2 lines vs 4
   for `sed -n '135,138p'`). `[INFERENCE]` intended `'135,138p'`.
3. `SCORECARD.md:7017` (correction block): "no other round-81 ordinal value is asserted here". True as intent,
   false as machine-read text: the block *quotes* `C1 | depth 8 → 9` and `Axes now: depth9`, and the counter's
   `PAIR`/`AXES_NOW` regexes parse those as assertions — my dump gives `(8,7003), (9,7003), (9,7003), (8,7003)`
   for that block (starts 7003; quoted prose 7009-7010). Only R82-V2's retirement bug keeps the file "clean".
4. `w1/ExecAnchor.md`: "Round-81 numbers were shifted two lines early, as the declaration said" — repeats item 1;
   accurate for quote spans, not for the cited ranges (its own table shows they were containers).
5. `w1/ExecAnchor.md`: "Each new span was checked by eye against the raw file" — process claim I cannot
   reproduce. The rest I did: `--fixture .` gives `count 8 / target 8 / met` rc 0, all eight `cited == located`.
6. `w1/ScribeOrdinal.md`: no over-claim; its "Known limits" correctly says the instrument "does not independently
   re-check that the surviving value is 8", and its 78→77 `examined` explanation matches my dump. Quoted
   authority checks out: `corpus/lessons/round-81-verifier-spotcheck.md:18,88,92,122-124`.
7. `w1/ExecMutMeasure.md`: both round-level claims confirmed by my independent run (R82-V1). No over-claim.
8. `corpus/lessons/round-82.md` (Gate): "the DOCTYPE (raw 2-3) and one `<ulink>` (raw 84-85) each swallow a
   newline, so all eight quote spans sit exactly two lines later … 703 lines against the raw file's 707". 707→703
   and the +2 are both true, but the stated *cause* covers 2 of the 4 swallowed newlines: the whole-file
   `TAG.sub('')` collapses four multiline tags, at raw 2, 84, 560 (`<citerefentry`) and 566 (`<literal`);
   707−4=703. Over-claim: a reader checking 707−2 gets 705.
9. `corpus/lessons/round-82.md`: "fetched live …, HTTP 200, 37 234 bytes, … `cmp` rc 0". Content verified
   (`sha256sum` = `afbf3be6…2394`, `wc -c` = 37234); the HTTP 200 and `cmp` are process claims I cannot
   reproduce.
10. `corpus/lessons/round-82.md` (registry): "S333 … Rows 332 → 333". Verified: `grep -n S333 corpus/SOURCES.md`
    → `:344`; row count 333. No over-claim.

Verified-correct prose (no action): snapshot sha256, 37234 bytes, 707 raw and 707 strip lines, `--fixture` 8/8
`cited == located` at `f376054a`, the eight +2 quote-span deltas, S333 at `corpus/SOURCES.md:344`.

## Routed defects

**L1 ruling (received 2026-11-04): the frozen recipe file is not amended — amending after the freeze would be a
re-scope. C2 stands recorded as `unmet`, `killed 22 / 26` against a ceiling of 22 and `genuine 16 / 17` against a
ceiling of 16, caused by the literal two-char `\n` in the C16 and M06 recipes with C06/C07 declared equivalent.
The double-escaped recipes are routed to round 83 as R82-V1, together with R82-V2…R82-V6 below.**

**R82-V1 (high) — C2's frozen target is unreachable, both legs.** `mutants-r82.json` has exactly four literal
`\\n` (two-char backslash-n) sequences, in `C16-empty-manifest.old/.new` and `M06-mutation-unlink-noop.old/.new`;
their `old` strings occur 0× at the freeze commit *and* at `f376054a`:
```
C16-empty-manifest       count-mount-rows-r81.py occurrences=0 genuine_gap=True
M06-mutation-unlink-noop measure-round81.py      occurrences=0 genuine_gap=False
```
`recipe-missing` is correctly not a kill, so `genuine_killed` maxes at 16/17 (C16 is the stale genuine recipe) and
`killed` at 24−2=22 (< 24), since C06/C07 are declared equivalent and "no test can kill them" (`SCORECARD.md:6973`).
The after-measurement lands on exactly those maxima (`killed 22, genuine 16`, survivors C06/C07/C16/M06), so both
legs are arithmetically out of reach, not merely missed. The freeze control is honest and reproduces exactly
(`rc=1 {"killed": 6, "total": 26, "genuine_killed": 0, "finding": "unmet"}`). Smallest remediation is an L1
decision: amend the frozen recipes (a re-scope, forbidden this wave) or record C2 as a miss and route the
double-escaped recipes to round 83. Independently found by ExecMutMeasure.

**R82-V2 (medium) — C3 retires an axis globally; a supersede line silences every block.**
`check-scorecard-ordinals.py:102  if key[0] == round_no or True:` — the `or True` makes the guard vacuous; the
comment says "retires assertions made *earlier* in the file, never later ones". Any `supersedes-ordinal:` line
drops that (round, axis) from all blocks, including the superseding block's own assertion and every later one.
Fixture (supersede, then a later block re-asserting 9 against the correction's 8): `{"count": 0, "examined": 0,
"finding": "clean"}` rc 0. Live shape: the landed block at 7003 yields 8,9,9,8 and C3 says `count 0, examined 77,
clean`. The suite codifies the same behaviour (`named-correction: clean`), so no test catches it. Fix: delete
`or True`, retire only sites below the superseding block's line.

**R82-V3 (medium) — C3's `--revision` cannot-evaluate leaks as a traceback, rc 1.** Evidence in check 1. Fix: add
`CannotEvaluate` to the `except` at `:207` and emit the JSON/rc 2 shape C1 and C2 use.

**R82-V4 (medium) — C2 counts a hung or unlaunchable selftest as a kill.** `:70-71 except
(subprocess.TimeoutExpired, OSError) … return 124` with `:125 is_killed = rc != 0`. The predicate is "killed when
its own `--selftest` exits non-zero"; 124 is synthesised, not observed. Stubbed child launch, instrument
unmodified: `run_selftest -> 124 "selftest-did-not-finish: … timed out after 300 seconds"`, `is_killed -> True`.
The baseline shares the path, so a global hang is caught as `baseline-red` → cannot-evaluate; a mutant-specific
hang scores as a kill with no observed verdict. Fix: record `rc=None, killed=False,
detail="selftest-did-not-finish"`, or raise `CannotEvaluate`.

**R82-V5 (low) — C1 cannot tell a doctored entry from a repair.** Rewriting the eight `lines` to the spans the
instrument itself locates gives `rc=0 count 8 / target 8 / met`. Outside C1's stated scope, and the commit diff is
the real control, but "a tampered input cannot produce met" does not hold two-sided. Fix: carry
`snapshot_sha256` in the entry and refuse on mismatch.

**R82-V6 (low) — importing a lane instrument writes into the lane.**
`tools/__pycache__/check-anchor-coordinates.cpython-314.pyc` appeared at 21:20 this wave (ExecAnchor.md: "the
counter's own `strip_view` + `locate`"); still present at 21:38. Gitignored, so `git status` stays clean, but it
is a write outside scratch. Fix: copy the instrument to scratch before importing, or `PYTHONDONTWRITEBYTECODE=1`
in the driver.

**Informational.** The blob reads (`check-anchor-coordinates.py:114-115`, `mutation-kill-r82.py:51-52`,
`check-scorecard-ordinals.py:199-200`) use the ambient env while binding uses `_revision.clean_env()`
(`tools/_revision.py:44`). A foreign `GIT_DIR` makes the read fail → rc 2 (fails closed). Hardening only.

## Scratch and tooling

`/fast/scratch/hyaku/tsukuroi-r82/SentinelGate/` (fixtures c1a-c1f, t1-t3, scratch git repo, work-c2/t1/t2,
TMPDIRs) deleted before yield — `ls -d` on it now returns "No such file or directory". No tool installed or
upgraded (python3 3.14.8, git, sha256sum, sed, find, grep only); pacman pause respected, no sudo, no service
restart.
