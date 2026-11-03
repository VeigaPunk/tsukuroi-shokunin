# SC2Census — GATES-RECON (round 64 / hyaku 15 / w1)

Seat: SC2Census, scout, **read-only** (one output file written, plus one throwaway clone under
`/fast/scratch/hyaku/tsukuroi-r64/SC2Census/`, deleted at yield). Host: Arch,
kernel 7.2.11-arch1-1. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, detached HEAD
at `2f3061ef` (= `master` = `origin/master`). Measurement window 18:40:27Z → 18:55:13Z.
No git/jj mutation in the lane or anywhere outside the scratch clone.
Toolchain: python3 3.14.8 · gawk 5.4.1 · bash 5.3.20(1) · git 2.56.0. Nothing installed.

Full evidence (timestamp + `$ command` + rc + decisive output per gate, plus the post-work
rerun protocol) is in **`.ufo/waves/round-64/after/gates-recon.md`**.

## Pre-work baseline

| Gate | Value at 2f3061ef | rc |
|---|---|---|
| `check-knowledge-header.py --revision 2f3061ef` | notes **79** / complete 79 / clean 79 / findings **0** | 0 |
| `check-registry-coverage.py --revision 2f3061ef` | tools **99** / rows 99 / registered 99 / findings **0** PASS | 0 |
| `check-cited-receipts-r62.py --revision 2f3061ef --round 63` | finding_count **1** (the named r63 permanent limit) FAIL | 1 |
| `… --round 64` (bonus, current round) | cited_paths 0 / finding_count 0 PASS | 0 |
| `check-scorecard-unique-sections.py` | all duplicate pairs supersession-marked; ok | 0 |
| frozen rows counter on `corpus/SOURCES.md` as-is | **278** | 0 |
| frozen malformed counter on `corpus/SOURCES.md` as-is | **0** | 0 |
| NF distribution over the 278 S-rows (CRLF file) | **278 × NF=13** — CRLF does not change NF | 0 |
| `bash tools/tsukuroi-census.sh --selftest` | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` | 0 |
| canonical `sources-census.sh validate --root … tsukuroi` | E12 **278**, no other E-code | 1 |

Selftests all green: knowledge-header 25, registry-coverage 23, cited-receipts 4,
scorecard-unique 5, census 168; the new `check-line-endings-r64.py --selftest` 5.

Gate 4 detail: the round-64 declaration section exists **once** (`4704:## Round 64 —
declaration …`) and is not a duplicate — **no duplicate-heading finding at the declaration
commit**. The three duplicate pairs are the declared LEGACY ones (round 26 ×2, round 37
axes ×2, round 37 capabilities ×2), each carrying supersession.

## Three findings handed to the integrator

**F1 — BLOCKER, outside my write surface: `corpus/SOURCES.md` is back to CRLF in the lane
worktree.** 381 CR bytes, sha256 `2349bfda141ab055…` = **byte-identical to the committed
`2f3061ef` blob**, mtime 15:47:32 -0300; SKILL.md/SCORECARD.md stay repaired (crs=0).
Stable across 16 samples from 18:47:32Z to 18:55:13Z — not the 18:43:21Z transient that
self-restored to `e1558e4b…`. Live effect: the canonical census is red again (E12=278, rc 1)
and `check-line-endings-r64.py --check` is red (1 violation, `corpus/SOURCES.md:1` CR at
offset 35). Repair is one command — `sed -i 's/\r$//' corpus/SOURCES.md`, then
`git show 2f3061ef:corpus/SOURCES.md | tr -d '\r' | cmp - corpus/SOURCES.md` must be empty —
and the expected post-repair numbers are rc 0 / **W04=42** / E12=0 (measured on an LF control
over a faithful tree copy). Any `git checkout-index -f` / `git restore` / `git checkout --`
on that path silently re-materialises the CRLF blob; do not use them.

**F2 — the E12 storm is heading-anchored.** `trim()` in `sources-census.sh:609-623` strips
`[ \t]` only, so `## Registry\r` fails the `=="Registry"` test and every following row is
reported "outside Registry section". Three single-CR fixtures prove it: all-CRLF → 1 E12;
**only the `## Registry` line CRLF → 1 E12**; only a data row CRLF → clean rc 0. The 278 is
the row count; the cause is one byte on line 3. Also: `E11` never appears in the canonical
lane run — the 27/435 E11 counts seen in probes are `--file`/`--root` scratch artifacts
(used-by paths are lane-relative) and must not be cited as lane findings.

**F3 — the new guard tool must get an 8-column SKILL.md registry row.** `tools_total` comes
from the committed `tools/` tree, so committing `check-line-endings-r64.py` without a row
yields `tools_total 100 / registered 99 / REGISTRY-ROW-MISSING`, rc 1 (proven in the scratch
clone; an 8-column row gives 100/100/0 PASS, a 6-column row gives `E-REGISTRY-TABLE`). The
correct post-work expectation for gate 2 is **100/100/0**, not 99.

Delta attribution is therefore clean: everything in the baseline table except gate 5 and the
guard is independent of the CRLF state, and both CRLF states (E1-repaired at 18:40–18:43Z,
reverted from 18:47:32Z) are recorded so neither direction can be misread as round-64 work.
