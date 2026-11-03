# GATES-RECON — standing-gate pre/post baseline (round 64 / hyaku 15 / w1)

Seat: SC2Census (scout, read-only, one output file). Host: Arch, kernel 7.2.11-arch1-1
(canonical Linux/omp host). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Measurement window **2026-11-03T18:40:27Z → 18:53:30Z**. No tracked file written by this
seat; no git/jj mutation anywhere (one throwaway clone under
`/fast/scratch/hyaku/tsukuroi-r64/SC2Census/fx`, deleted at yield).

Toolchain observed (no install needed, none performed):
`python3 3.14.8` · `gawk 5.4.1` · `bash 5.3.20(1)` · `git 2.56.0` · `uname -r 7.2.11-arch1-1`.

Lane revision under test: `2f3061ef725abebd8cd157b778203f1cf5c0cb0c` (the round-64
declaration commit, 2026-11-03 15:05:33 -0300). Note: the worktree is on a **detached HEAD**
at that commit (`git status --porcelain --branch` → `## HEAD (no branch)`); `master` and
`refs/remotes/origin/master` both also resolve to `2f3061ef`.

---

## Pre-work baseline

| # | Gate | Value at 2f3061ef | rc |
|---|---|---|---|
| 1 | `check-knowledge-header.py --revision 2f3061ef` | notes=79 complete=79 clean=79 findings=0 | 0 |
| 2 | `check-registry-coverage.py --revision 2f3061ef` | tools=99 rows=99 registered=99 findings=0 PASS | 0 |
| 3 | `check-cited-receipts-r62.py --revision 2f3061ef --round 63` | finding_count=**1** (the named r63 limit), verdict FAIL | 1 |
| 3b | `check-cited-receipts-r62.py --revision 2f3061ef --round 64` | cited_paths=0 finding_count=0 PASS | 0 |
| 4 | `check-scorecard-unique-sections.py` | all duplicate level-2 pairs marked; ok | 0 |
| 5a | frozen row counter on `corpus/SOURCES.md` AS-IS | **278** | 0 |
| 5b | frozen malformed counter on `corpus/SOURCES.md` AS-IS | **0** | 0 |
| 5c | NF distribution over the 278 S-rows (CRLF file) | **278 × NF=13** (CRLF does *not* change NF) | 0 |
| 6 | `bash tools/tsukuroi-census.sh --selftest` | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` | 0 |
| — | canonical `sources-census.sh validate --root … tsukuroi` | E12=**278**, no other E-code, rc=1 | 1 |

Selftests run for completeness (all green, no action implied):

| Gate selftest | Result |
|---|---|
| `check-knowledge-header.py --selftest` | 25 cases, 25 passed |
| `check-registry-coverage.py --selftest` | 23 cases, 23 passed |
| `check-cited-receipts-r62.py --selftest` | PASS, 4 cases (base-pass, head-finds-ghost, landing-clears, bad-rev-cannot) |
| `check-scorecard-unique-sections.py --selftest` | 5 cases, 5 passed |
| `check-line-endings-r64.py --selftest` (new guard, worktree only) | 5 cases, 5 passed |
| `tsukuroi-census.sh --selftest` | 168 cases, 168 passed |

---

## 1. knowledge-header — rc 0, 79/79/0

```
$ python3 tools/check-knowledge-header.py --revision 2f3061ef
rc=0
note_count=79 complete_count=79 clean_count=79 finding_count=0
```

Reproduced 3×; identical each run. Revision binding is live: `--revision HEAD` is refused
(`E-REVISION-INVALID`, "7-64 hex commit required", rc 2), a 7-hex prefix `2f3061e` is accepted
(rc 0). Scope `corpus/knowledge/` has no worktree diff vs `2f3061ef`
(`git status --porcelain --untracked-files=no -- corpus/knowledge` → empty), so the
revision-bound value equals the worktree value for this gate.

## 2. registry-coverage — rc 0, 99/99/0 (PRE value)

```
$ python3 tools/check-registry-coverage.py --revision 2f3061ef
rc=0
{"branch":"master","branch_tip":"2f3061ef…","counts":{"findings":0,"missing":0,
 "registered":99,"rows_total":99,"tools_total":99},"status":"PASS"}
```

`tools_total` is derived from the committed tree's `tools/` blobs
(`GitReader.tool_files()` over `ls-tree`), *not* the worktree: `git ls-tree -r --name-only
2f3061ef tools/` = 99 files. So the PRE value is 99, and it rises to **100 only after
`tools/check-line-endings-r64.py` is committed and given a SKILL.md registry row** (see §7).

## 3. cited-receipts — round 63 FAIL 1 (the disclosed limit), round 64 PASS 0

```
$ python3 tools/check-cited-receipts-r62.py --revision 2f3061ef --round 63
rc=1
round=63 files_scanned=29 cited_paths=19 finding_count=1 verdict=FAIL
 FINDING CITED-RECEIPT-MISSING \
   .ufo/waves/round-63/before/spawn-crash-repro-receipt-expected-absent.txt
   cited-in: .ufo/waves/round-63/after/cited-receipts-r63-*.json (2),
             .ufo/waves/round-63/before/spawn-crash-repro.txt,
             corpus/lessons/round-63.md
```

This is exactly the ONE named permanent finding the round carried in: the path is cited by
proof-of-absence (the committed receipt's own `ls` error line), and a path-existence gate
cannot express cited-as-proven-absent. It is **not** a round-64 regression. Same command,
round 64: `rc=0`, `files_scanned=6 cited_paths=0 finding_count=0 verdict=PASS`.

## 4. scorecard-unique-sections — rc 0

```
$ python3 tools/check-scorecard-unique-sections.py
check-scorecard-unique-sections: every duplicate level-2 heading pair carries a
supersession marker; ok
rc=0
```

Same verdict on the committed `2f3061ef` blob via `--file` (rc 0). The three duplicate
pairs are the declared LEGACY ones and each declares supersession:
`## Axes — current self-assessment (round 26)` ×2 (lines 939, 971),
`## Axes — current self-assessment (round 37)` ×2 (1962, 1986),
`## Capabilities — current (round 37)` ×2 (1975, 1999).

The round-64 declaration section is present exactly once and is **not** a duplicate:
`4704:## Round 64 — declaration (2026-11-03, base 44fc183b, written before any
after-measurement)`. `grep -c '^## Round 64' SCORECARD.md` = 1. **No duplicate-heading
finding at the declaration commit.**

## 5. Manual census counters, `corpus/SOURCES.md` AS-IS (CRLF at this point)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
278                                rc=0

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0                                  rc=0

$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/{print NF}' corpus/SOURCES.md | sort | uniq -c
    278 13
```

**CRLF does not change NF.** `awk -F'|'` splits on `|` only; the `\r` stays *inside* the
last field, so `$13` is `"\r"` and NF is 13 for all 278 rows (verified byte-wise:
`grep -m1 '^| S001 ' … | awk -F'|' '{printf "[%s]", $13}' | cat -A` → `[^M]` on the CRLF
blob vs `[]` on the LF control; `tail -c 40 corpus/SOURCES.md | od -c` → `... . \r \n`).
The frozen malformed counter is therefore **blind to this defect class**: a CR-only
regression keeps rows=278 and malformed=0 while the canonical census goes red. Identical
counters on the `2f3061ef` blob and on its `tr -d '\r'` control (278 / 278, malformed 0 / 0).

## 6. `tsukuroi-census.sh --selftest` — PASS 168

```
$ bash tools/tsukuroi-census.sh --selftest
rc=0   (171 output lines: 168 PASS, 0 FAIL)
TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)
Wall time: 31.13 seconds
```

The r38-era figure of 148 cases has since grown to **168** (R44–R50 cases included). The
`--help` line the item expected ("PASS line + case count") is this final summary line.

---

## 7. Findings for the integrator (delta-attribution material) — F1–F3 here, F4–F8 in §7b/§7c

### F1 — BLOCKER, **DISCHARGED** 18:56:00Z: the lane worktree was reverted to CRLF on `corpus/SOURCES.md`

At recon start the tree was E1's repaired state; from **15:47:32 -0300 (18:47:32Z)** onward
`corpus/SOURCES.md` carries **381 CR bytes** and is **byte-identical to the committed CRLF
blob**, while the other two files stay repaired:

```
$ for f in corpus/SOURCES.md SKILL.md SCORECARD.md; do printf '%s crs=%s sha=%s\n' \
    "$f" "$(tr -cd '\r' < "$f" | wc -c)" "$(sha256sum "$f" | cut -c1-16)"; done
corpus/SOURCES.md  crs=381   sha=2349bfda141ab055   mtime=2026-11-03 15:47:32.602919502 -0300
SKILL.md           crs=0     sha=bda5249b161e7442   mtime=2026-11-03 15:37:05.917665736 -0300
SCORECARD.md       crs=0     sha=1304750516c86ab1   mtime=2026-11-03 15:37:05.920036022 -0300

$ git show 2f3061ef:corpus/SOURCES.md | sha256sum     → 2349bfda141ab0556c2918a08246184f31f70dbbca0bfcd2d6726e3b72d2d800
$ sha256sum corpus/SOURCES.md                          → 2349bfda141ab0556c2918a08246184f31f70dbbca0bfcd2d6726e3b72d2d800
$ git status --porcelain --untracked-files=no
 M SCORECARD.md
 M SKILL.md                     # corpus/SOURCES.md is NOT modified → back to HEAD bytes
```

Stable, not transient: 10 samples at 6-s intervals 18:48:58→18:49:52Z plus samples at
18:51:04/09/14Z and 18:53:24/27/30Z all read `crs=381 sha=2349bfda mtime=15:47:32`.

Consequences measured at that state:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
rc=1   E12=278   (278 output lines, all E12, no other E-code)

$ python3 tools/check-line-endings-r64.py --check
check-line-endings-r64: 1 violation(s)
  corpus/SOURCES.md:1: CR byte at offset 35
CHECK_LINE_ENDINGS: FAIL (326 file(s) checked, 1 violation(s))
rc=1
```

E1's own receipt (`.ufo/waves/round-64/after/c1-guard-check.txt`, `w1/E1LineEnd.md` §
concurrency) records an earlier 18:43:21Z transient that self-restored to sha `e1558e4b…`.
The present state is **not** that transient: it is `2349bfda…` (= committed blob) and it
persists. The author is unknown to this seat; no lane process was running that matched
(`ps` for `check-line-endings|sources-census|sed -i` → empty).

**Repair for the L1** (strip, stage, then prove identity — order matters, see F4):

```
$ sed -i 's/\r$//' corpus/SOURCES.md
$ git add corpus/SOURCES.md SKILL.md SCORECARD.md                  # stage BEFORE any checkout-class cmd
$ git ls-files --eol -- corpus/SOURCES.md SKILL.md SCORECARD.md    # must read i/lf w/lf on all three
$ git show 2f3061ef:corpus/SOURCES.md | tr -d '\r' | cmp - corpus/SOURCES.md   # must be empty
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin tsukuroi                          # expect rc 0, W04 only
```

Expected post-repair numbers, measured on an LF control of the same bytes laid over a
pruned copy of the lane tree: `rc=0`, `ok 1`, **W04=42**, E12=0.

**Anti-clobber warning for the integrator:** three separate writers can silently undo this
repair — `git checkout-index -f`, `git restore`, `git checkout --` on a detached HEAD all
re-materialise the CRLF HEAD blob. The scratch clone reproduced it exactly (guard red at
`2f3061ef` with 3 violations: SCORECARD/SKILL/SOURCES). **The mechanism is the index, not a
process: until the LF content is staged, those commands read the still-CRLF index blob** —
hence the `git add` above, which is what converts them from destructive to safe (F4).

### F2 — the E12 storm is heading-anchored: ONE CR byte in `## Registry` causes all 278

Mechanism (read at `scripts/sources-census.sh:609-623` + proven by 3 single-CR fixtures):

* the row parser computes `in_registry=(trim(substr(line,3))=="Registry")`, and `trim()`
  strips only `[ \t]` — never `\r`;
* so `## Registry\r` yields `"Registry\r" != "Registry"` → `in_registry=0` → the section
  condition is false → every following `| S### |` row is reported `E12 row outside
  Registry section`.

```
# fixture A: every line CRLF            → mx  E12  S001 row outside Registry section   rc=1
# fixture B: ONLY the "## Registry" line has CR → mx  E12  S001 …                      rc=1
# fixture C: ONLY the S001 data row has CR     → mx  ok   …/corpus/SOURCES.md          rc=0
# probe:    grep -m1 '^## Registry' <CRLF blob> | gawk '{trim…}'
            trimmed=<Registry^M> eq=0
```

So the blast radius (278) is the row count, but the *cause* is a single byte on line 3 —
matching E1's guard reporting `corpus/SOURCES.md:1: CR byte at offset 35` for a whole-file
verdict. Reproduced end-to-end on a pristine `2f3061ef` extraction
(`git archive 2f3061ef | tar -x -C <scratch>/base`, symlinked as a lane under a scratch
root): `E12=278 rc=1`; same tree with `tr -d '\r'`: `E12=0 rc=0`.

Side note for readers of earlier rounds' counts: `E11` is **not** part of this story. The
canonical lane run emits E12 only. E11 counts of 27/435 seen in this seat's probes are
artifacts of running the file against scratch roots whose `used-by` paths do not resolve —
`SOURCES.md` used-by paths are lane-relative, so any `--file`/`--root` probe outside a
faithful copy of the lane inflates E11. Do not cite those as lane findings.

### F3 — the new guard tool is unregistered: landing it as-is turns registry-coverage red

`tools/check-line-endings-r64.py` exists in the worktree (sha256
`15f0e65c889acc3b591ca44c7e52fe16fa14d79c367e743ebcc905b17d50c030`, 12858 bytes) and
`git cat-file -e 2f3061ef:tools/check-line-endings-r64.py` → **rc 128, absent at HEAD**;
`grep -c 'check-line-endings' SKILL.md` → **0**. `tool_files()` enumerates every committed
`tools/` blob, so committing it without a row is a guaranteed FAIL. Proven in a shared clone
(`/fast/scratch/.../fx`, `git rev-parse --show-toplevel` asserted = clone, fixture commits
only inside it):

```
# guard committed, no SKILL row:
counts: {findings:1, missing:1, registered:99, rows_total:99, tools_total:100}
finding: REGISTRY-ROW-MISSING  site tools/check-line-endings-r64.py      rc=1

# same + row inserted with 6 columns:
finding: E-REGISTRY-TABLE "malformed registry row at line 5485"          rc=2

# same + row rewritten with all 8 HEADER columns (Name|Kind|Entry command|Verdict map|
#            Self-test|Pinned values|Write scope|Owner):
counts: {findings:0, missing:0, registered:100, rows_total:100, tools_total:100} PASS   rc=0
```

So the post-work expectation for gate 2 is **100/100/0**, and the row must be eight columns.

---

## Post-work rerun protocol for the L1

Run after integration (nothing in this file is a substitute):

```
sed -i 's/\r$//' corpus/SOURCES.md                                   # F1 (if still 381 CR)
git add corpus/SOURCES.md SKILL.md SCORECARD.md                      # MANDATORY BEFORE any checkout-class cmd (F4)
git ls-files --eol -- corpus/SOURCES.md SKILL.md SCORECARD.md        # expect i/lf w/lf on all three
git show 2f3061ef:corpus/SOURCES.md | tr -d '\r' | cmp - corpus/SOURCES.md   # empty, rc 0
python3 tools/check-line-endings-r64.py --check                      # expect rc 0, 326 files, 0 violations
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tsukuroi                    # expect rc 0, E12=0, W04=42
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md # expect 278
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' \
    corpus/SOURCES.md                                                # expect 0 (blind to CR: see §5)
python3 tools/check-knowledge-header.py --revision <final>           # expect 79/79/0
python3 tools/check-registry-coverage.py --revision <final>          # expect 100/100/0 (F3)
python3 tools/check-cited-receipts-r62.py --revision <final> --round 64  # expect PASS 0
python3 tools/check-scorecard-unique-sections.py                     # expect rc 0
```

**Ordering is not cosmetic (F4).** The `git add` must precede every checkout-class command,
including any `git checkout --`/`restore`/`checkout-index` used by a helper or a jj export.
`jj describe` alone does **not** stage — in this jj-managed lane use `jj new` / a jj commit,
or a plain `git add`. The `cmp` line certifies bytes only; the line that certifies the
*durability* is `git ls-files --eol` reading `i/lf w/lf`.

**Predicate for the C1-after run — two corrections, both from seats that measured them:**

* **W04 is 44, not 42, once C3's S279–S281 rows land** (S1Scribe, scratch rig reported to this
  seat). S280 re-pins the limine master hook URL already carried by S021/S098 and S281 re-pins
  the plymouth main-branch hook URL already carried by S022/S111, both in a **new scope** — the
  register's established superseding-row convention, so each adds a W04 warning rather than an
  E04 error. Predicate: `rc=0, E-codes 0, W04=42` **before** the C3 rows, `W04=44` **after**.
  The baseline in §5 is the 42; a 44 on the final run is expected, not a regression.
* **Rows are 281, not 278, on the final run**, and the E11 count is 0 only if
  `corpus/knowledge/mkinitcpio42-onrelease-r64.md` exists on disk at that moment (the S-rows
  cite it as `used-by`; until E3Mk42/L1 lands the note the census reports E11 per row). Take
  the **census END receipt after the note lands**, or the receipt will carry E11s that are
  landing-order artifacts, not findings.

Any *other* deviation from those numbers is attributable to round-64 work, because every one
of them is pinned to a measured PRE state above.

## POST-REPAIR CONFIRMATION — F1 resolved by the L1 (2026-11-03T18:56:00Z)

The L1 landed the CR strip while this seat was still on station; the pre-work baseline above
stands as the PRE state, and this block is the AFTER state for the same gates, measured
unprompted (not a rerun of my own claim):

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
  git rev-parse --show-toplevel  → /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
  git rev-parse HEAD             → 2f3061ef725abebd8cd157b778203f1cf5c0cb0c
  git status --porcelain --branch → ## HEAD (no branch)
  tr -cd '\r' < corpus/SOURCES.md | wc -c → 0
  sha256sum corpus/SOURCES.md    → e1558e4b3eeef8857e27a64299e08c50e52c3b9f5f2160a09cd6647e90c3df77
  size 278906, mtime 2026-11-03 15:56:00.454749634 -0300

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
rc=0      W04=42   ok=1        (E12 gone; 43 output lines)

$ python3 tools/check-line-endings-r64.py --check
CHECK_LINE_ENDINGS: PASS (326 file(s) checked, 0 violation(s))     rc=0

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        → 278
$ awk -F'|' '/… S[0-9][0-9][0-9]+ …/ && NF!=13 {n++} END{print n+0}' …        → 0
```

Every C1 predicate that could be checked at this point matched the value predicted in
"Post-work rerun protocol" **exactly**: `rc 0`, `E12=0`, `W04=42`, guard green at 326 files,
rows 278, malformed 0. The W04=44 and rows=281 figures apply only once C3's S279–S281 land
(see the predicate note). F1 is therefore **discharged**, and the delta against this
baseline is now cleanly attributable to round-64 work.

Two gates remain for the L1 at the final revision and this seat could not measure them
(uncommitted worktree): gate 2 must read **100/100/0** after the guard tool plus its
8-column SKILL.md row are committed (F3), and the census END receipt must be taken after
`corpus/knowledge/mkinitcpio42-onrelease-r64.md` exists (E11 otherwise).

## 7b. F4 — the repair is worktree-only until committed: the index still holds the CRLF blobs

Measured after the L1's strip (this is the *durability* gap, not a regression):

```
$ git ls-files --eol -- corpus/SOURCES.md SKILL.md SCORECARD.md
i/crlf  w/lf    attr/                 	SCORECARD.md
i/mixed w/lf    attr/                 	SKILL.md
i/crlf  w/lf    attr/                 	corpus/SOURCES.md

$ git status --porcelain --untracked-files=no
 M SCORECARD.md
 M SKILL.md
 M corpus/SOURCES.md

$ git hash-object corpus/SOURCES.md      → f693b5d10eb381aca0866e4a3841a0e4f00c771f   (LF)
$ git rev-parse HEAD:corpus/SOURCES.md   → 298592bbc2c4facb369bc7d893f97589cf1bcafb     (CRLF)
$ ls .gitattributes                      → No such file or directory
```

`i/crlf` / `i/mixed` is the whole mechanism of the 18:47 recurrence: the *worktree* is LF,
the *index and HEAD* are still CRLF, so any `git checkout-index -f` / `git restore` /
`git checkout --` / `git stash` on those paths re-materialises CRLF by definition. A
worktree-only sed cannot prevent the next one — only a commit makes the blobs LF. The lane
has **no `.gitattributes`**, so git stores bytes as-is and a plain `git add` of the three
paths is sufficient; `git add --renormalize .` must **not** be used (measured in a sibling
lane: it rewrites unrelated CRLF evidence artifacts).

### The trigger is the INDEX blob, and the staging order therefore matters

Independently measured on the kagi lane by SentHygiene (`.ufo/waves/round-30/build/SentHygiene.md`,
cross-lane, reported to this seat): in exactly this pre-commit state the three checkout-class
commands restore the CRLF blob (`git checkout --`, `git restore`, `git checkout-index -f` →
193 CR bytes on the kagi files) — not because any process "re-materialised" anything, but
because the commands read the still-CRLF index. Once the LF content is staged the index flips
to `i/lf` and **all three become safe**. What updates the index:

| Action | index | checkout-class commands afterwards |
|---|---|---|
| `git add <path>` | `i/lf` | safe (0 CR) |
| `jj new` / a jj commit (snapshots) | `i/lf` | safe (0 CR) |
| `jj describe` **alone** | stays `i/crlf` | **still unsafe** |

S52connector01 proved both arms in a throwaway `jj git init --colocate` fixture plus a plain
git repo (CRLF blob committed, LF worktree): **arm 1** (index CR≠0, worktree CR=0) →
`git checkout-index -f` restores the worktree to CRLF, repair destroyed; **arm 2** (same
state but `git add` first → index CR=0) → `git checkout-index -f` leaves the worktree LF,
repair survives. They also confirmed in a fresh colocated repo that `jj describe -m` alone
leaves the git index unsynced while `jj new` syncs it — so "staging" here is specifically
`git add` / `jj new` / `jj commit`, and `jj describe` does not qualify.

**The trigger is armed in this lane right now, not historically.** The index still holds the
CRLF blobs while the worktree is LF:

```
corpus/SOURCES.md  index CR=381    worktree CR=0
SKILL.md           index CR=5452   worktree CR=0
SCORECARD.md       index CR=4723   worktree CR=0
```

with no `.gitattributes` at HEAD (`git ls-tree HEAD -- .gitattributes` → empty) and
`core.autocrlf` / `core.eol` / `core.safecrlf` unset at every origin, so no normalisation
layer catches this.

That table is live here, not hypothetical: **this lane is jj-managed** — `.jj/` exists and
`git reflog` reads `2f3061ef HEAD@{0}: export from jj`, `44fc183b HEAD@{1}: export from jj`.
So the ordering rule for the repair is: **`sed` → stage (or jj new/commit) → only then any
checkout-class command**; and `jj describe` on its own is not a stage. (The jj-export path is
also a plausible *mechanism* for CRLF reappearing in the index — but it is a candidate, not an
attribution: the 18:47:32Z writer stays unidentified, since the index is not reflogged.)

**My own identity check is necessary but not sufficient, and that is worth stating plainly:**
`git show 2f3061ef:corpus/SOURCES.md | tr -d '\r' | cmp - corpus/SOURCES.md` returns **rc 0
right now**, while the index is still `i/crlf` / `i/mixed` (measured 18:58Z). It compares the
LF form of the committed blob against the worktree, so it certifies the *bytes* and says
nothing about the index. The index-side proof must be `git ls-files --eol` → `i/lf w/lf`.

**The guard does not close this hole, by design**: `check-line-endings-r64.py` builds its set
from `git ls-files` (line 126) but reads the **worktree** bytes (`open(path, "rb")`, line 148).
It therefore reports PASS on a tree whose index is entirely CRLF — as it does right now. It
stops worktree recurrence, not commit recurrence. If it is meant to be the durable gate it
must assert the **index**, not the worktree, and the same bug recurs in the obvious fix: a
pre-commit hook that re-reads worktree bytes has the identical blind spot (a path staged and
then modified again commits bytes the worktree no longer shows). Assert `git ls-files --eol`
(`i/*`) or resolve staged blobs directly (`git diff --cached --name-only -z` then
`git cat-file --batch-check` over `:path`).

Post-commit invariant that catches the real thing:

```
git ls-files --eol -- corpus/SOURCES.md SKILL.md SCORECARD.md
# must read  i/lf w/lf  on all three (worktree-only repair leaves i/crlf / i/mixed)
git cat-file blob $(git rev-parse HEAD:corpus/SOURCES.md) | tr -dc '\r' | wc -c   # belt-and-braces: 0
```

With no `.gitattributes` in the tree, `i/lf` is derived from the raw blob bytes, so `i/lf`
*means* the committed blob is LF — the extra `cat-file` line is redundant but cheap enough to
keep in the receipt as an independent check.

The 18:56 post-repair census/perimeter numbers (rc 0, E12=0, W04=42, guard PASS 326) are
measured on the **worktree** and are therefore true *and* insufficient on their own: they do
not certify the commit.

## 7c. F6 — the declaration's CR-origin claim is wrong for SCORECARD.md (and the r64 declaration itself re-CRLF'd it)

The round-64 declaration (`2f3061ef`) states: *"Windows-era tooling landed CRLF line endings
in corpus/SOURCES.md, SKILL.md, SCORECARD.md (origin: round-59 work commit 2913b75d; parent
c5a33d08 is 100% LF)"*. Measured per file, that holds for two of the three and fails for the
third:

| file | 81776bef (c5a33d08^) | c5a33d08 (r59 **declaration**) | 2913b75d (r59 **work**) | 44fc183b (r63 tip) | 2f3061ef (r64 decl.) |
|---|---|---|---|---|---|
| `corpus/SOURCES.md` | — | 0 | **377** | 381 | 381 |
| `SKILL.md` | — | 0 | **4990** | 5452 | 5452 |
| `SCORECARD.md` | **0** | **4178 / 4178 lines = 100% CRLF** | 4178 | 4654 | **4723 / 4723 = 100% CRLF** |

Three corrections:

1. **"parent c5a33d08 is 100% LF" is true only for `corpus/SOURCES.md` and `SKILL.md`.** At
   `c5a33d08`, `SCORECARD.md` is 4178 CR bytes over 4178 lines — fully CRLF. The declaration's
   blanket statement is false for one of the three files it names.
2. **`SCORECARD.md`'s CRLF origin is `c5a33d08` (the r59 *declaration*), not `2913b75d` (the r59
   *work* commit).** First-parent scan of all 179 commits touching the file: `c5a33d08^`
   (`81776bef`) has CR=0, `c5a33d08` has CR=4178; the content delta is +51/−0 under
   `--ignore-cr-at-eol`, i.e. the commit added 51 lines and CR-terminated the whole file.
   `2913b75d` then carried `corpus/SOURCES.md` (377) and `SKILL.md` (4990) across.
3. **The r64 declaration commit `2f3061ef` itself converted the last 47 LF-only SCORECARD lines
   to CRLF**: `44fc183b` has 47 LF-only lines (4180–4225, 4539), `2f3061ef` has 0, with a
   +22/−0 content delta. So the r64 declaration writer re-CRLF'd SCORECARD on this host —
   SCORECARD's CR is not purely r59 archaeology.

**Why it matters and why it does not block C1:** the repair is content-neutral (`git show
2f3061ef:F | tr -d '\r'` is byte-identical to the repaired file for all three — verified), so
the CR-strip fix is unaffected. What is affected is *provenance*: any round-64 write-up that
repeats "parent c5a33d08 is 100% LF" or "SCORECARD CRLF originated at 2913b75d" is repeating
a claim the committed bytes contradict, and the LOG/lesson would be wrong on a point the
round explicitly spent archaeology effort on. Record the per-file table above instead.

**The over-broad claim is committed upstream, not newly introduced here.** The phrase is in
the subject line of the declaration commit itself:

```
$ git log -1 --format=%B 2f3061ef | grep -o 'CRLF origin[^;)]*'
CRLF origin r59 2913b75d archaeology
```

It names `2913b75d` only — true for `corpus/SOURCES.md` and `SKILL.md`, false for
`SCORECARD.md`. Any future reader citing the declaration commit as the provenance source
inherits the error; the table above is the corrective, and the lesson should record that the
declaration's message is where the claim entered rather than implying the correction is a new
disagreement.

Accurate one-sentence form: **`c5a33d08` made `SCORECARD.md` 100% CRLF (parent `81776bef`
CR=0, +51/−0 ignoring CR); `2f3061ef` took it from 47 LF-only lines to 0 while appending 22
lines — i.e. the declaration left it fully CRLF, it did not introduce CRLF to it.**

Independently corroborated on point 3 by RV1Origin (read-only, committed bytes); the
`corpus/SOURCES.md` / `SKILL.md` origin at `2913b75d` is corroborated by S52connector01.

## Honest limits of this recon

* Gate 1 (knowledge-header) is revision-bound to `2f3061ef`; `corpus/knowledge/` had no
  worktree diff at recon time, so revision == worktree there. It does **not** cover
  `SKILL.md`/`SCORECARD.md` content.
* Gate 2 reads **committed** bytes only. It cannot see the worktree's unregistered guard
  tool (that is why F3 needed a fixture).
* The two gates that read committed blobs (2, 3) were unaffected by the CRLF state; gate 1
  and 4 were measured against matching bytes. Only the bash census (5) and the new guard
  observe the line endings.
* The frozen malformed counter's regex was pinned rather than assumed: `[0-9][0-9][0-9]+`
  is **3-or-more digits** (two fixed positions plus one-or-more), not a 4-digit minimum.
  1-row fixtures agree across three engines — `S99` → 0 matches, `S999` → 1, `S9999` → 1
  (PI grep / `/usr/bin/grep` / gawk identical), so no row class is invisible to it. It
  covers all 278 rows; its only blind spot is the one named in §5 (a CR keeps NF=13).
* The pre-work CR state of `corpus/SOURCES.md` was **E1-repaired** at 18:40–18:43Z and
  **reverted to CRLF** from 18:47:32Z. Both states are recorded above so the delta cannot be
  misattributed to round-64 work in either direction.
