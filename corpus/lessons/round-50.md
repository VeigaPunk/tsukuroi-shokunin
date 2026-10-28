# Round 50 — tsukuroi lane lesson (hyaku run 11, attempt 1)

Base `b866a1d3d26616119a089f1a69b080136becc17b`; freeze `43bcce06e28fe53b6f2e358a1225bb2b1b536b22`;
freeze amendment 1 (pre-data) `8029cdba1049df25632c91a23c8db4eefb54be5f`, which is the bytes the wave
reads. Claims and predicates: `.ufo/waves/round-50/frozen/FROZEN.md`.

## Gate — sources

| id | status change | access | located quote (<=25 words) | note |
|---|---|---|---|---|
| S256 (new) | absent -> `mined` | 2026-10-28, `https://man7.org/linux/man-pages/man1/grep.1.html`, sha256 `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`, raw HTML lines 201-205 | "Exit immediately with zero status if any match is found, even if an error was detected" | tier A docs; source directly states immediate exit, while pipeline SIGPIPE/pipefail behavior is a shell consequence. Claim C2 rests on it. |
| S240 (re-opened) | `mined` -> `mined`; `used-by` old three rows -> old three plus `corpus/knowledge/btrfs-scrub-grounding-r45.md` | 2026-10-28, `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`, sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` (byte-identical to the pin) | "ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end," (line 3093) | the row the GR2 correction now names; its registered ranges do not list :3093, :3109, :3115 or :3190 — declared in the entry's Limits. |

Refused this round: the staged `merge/tsukuroi` package (`/home/vgpnk/Projects/shokuknow`) is not adopted —
57 of its ids collide with the lane registry (`.ufo/waves/round-50/assimilation/collisions`, 256 lane ids vs
147 staged), and the round's claims needed no new entry. Flip: renumber the package in scratch and adopt one
theme in a later round. `Assimilation: none` in the report.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Instrument blind to the defect it claims to close: a `printf ... | grep -qE` site on `$pkgline` survived the first fix; the amendment K-pass control caught it | `.ufo/waves/round-50/frozen/FROZEN.md` "Freeze amendment 1" item 1; `tools/tsukuroi-census.sh:2398` at `43bcce06` | C2 K-pass control | converted to full-read `buf_has`; K-pass now checks zero executable idiom sites |
| Text counter counted a comment that quotes the banned idiom — false positive on the first repaired census | `tools/check-selftest-matcher-r50.py` at `43bcce06` (`idiom_sites 2`) vs amendment `8029cdba` (`0`); `.ufo/waves/round-50/controls/battery-summary-r50-c2.jsonl` | C2 K-pass control | `idiom_sites` scans executable lines only; base still scores 7 |
| Incomplete source-range declaration left out-of-range citations undisclosed; exact quote dropped a comment leader | `.ufo/waves/round-50/w1/R50RevGR1b.md`, `R50CritGR2a.md`, `R50CritGR2b.md`, `R50RevGR2c.md`, `R50RevGR3a.md`; `.ufo/waves/round-50/after/c1-final.json` (`verdicts_ok 0`) | Captured by the round-50 counted cohort; no earlier QUALITY criterion required enumerating all citations against every registered range | QUALITY 94 now requires complete range-gap disclosure and full-line quote fidelity; next counter must include one omitted range and one stripped comment-prefix control. It has not yet been mechanically shown to fail under that criterion. |
| Repin drift left for a later commit (round-49 V3 repeated): the census edit moved IN-109's case line 2671 -> 2683 and `check-adjacency-anchors.py` failed at the first freeze | `.ufo/waves/round-50/frozen/FROZEN.md` "Freeze amendment 1" item 3; `tools/check-adjacency-anchors.py --revision 43bcce06` -> FAIL | C3 K-pass control, which runs the existing anchors checker | repinned in the pre-data amendment `8029cdba` in the same commit as the census edit |
| Two new counters were initially absent from the gate registry; the no-harm seat found three new `REGISTRY-ROW-MISSING` paths | `.ufo/waves/round-50/w1/R50RevNoHarm.md` F3; `tools/check-registry-coverage.py` at base 6 missing / 80 tools and freeze 9 missing / 83 tools | The no-harm reviewer `R50RevNoHarm` | all three round-50 counters are now listed in the SKILL registry; re-run the gate before landing to confirm the new misses return to the base set |

## Admitted / refused this round

Filled at integration: claim verdicts, the GR1-GR3 admission decision, and the trend verdicts live in
`SCORECARD.md` "Round 50 — measured outcome" and the round report.
