# Round 94 lesson — tsukuroi lane

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by the L1 (URL, access date, located quote; ≤25 words each):

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S386 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, inside `create_menu_tree()`) |
| S387 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | A | "A config whose first line is an entry has had no global options since 12.9.5." (12.9.6 Miscellaneous) |
| S388 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (raw 2035; `--version-only` print raw 2031) |
| S385 (r93 routed 2, rule-1 row now supplied) | https://docs.python.org/3.15/using/cmdline.html#cmdoption-P | A | "1. Command line and environment — Python 3.15.2 documentation" (title, fetched 2026-11-08, sha256 `d3c503060e…`) |

Admitted: all three new rows, `used-by corpus/knowledge/limine-auto-default-r94.md, corpus/lessons/round-94.md`.
Re-opened from the pinned copies: S382 (v12.9.5 `common/lib/config.c`, byte-identical to the v12.9.6
file this round), S383 (v12.9.5 ChangeLog), S384 (v12.9.5 `host/limine.c`, same print bytes). The
v12.9.6 `config.c` and `host/limine.c` are byte-identical to their v12.9.5 counterparts (sha256
`a940acae…` and `4da21c7c…` against the r93 pins); the v12.9.6 ChangeLog's only visibility sentence
is the #700 documentation note, quoted above.

Rejected / refused this round:
- `https://man.archlinux.org/man/limine.8`: the page is not found (HTTP 404, "Page not found — Arch
  manual pages"). Not evidence of anything; the lane does not package a man page for `limine`.
- `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6`: the release JSON
  only points at the ChangeLog ("Changelog can be found here" + tarball-signature text); it states no
  Limine behaviour and is kept as a wave-directory locator, not a SOURCES row.

Anchor changes logged this round: none in place; S386-S388 are new rows (SOURCES 385 → 388).
Status changes this round: none in place; S385's `used-by` gains `corpus/knowledge/limine-auto-default-r94.md`
and this lesson (old → new: `corpus/knowledge/limine-r92-oracle-isolation.md, corpus/lessons/round-92.md,
corpus/lessons/round-93.md` → that plus `corpus/knowledge/limine-auto-default-r94.md,
corpus/lessons/round-94.md`).

Spot-check result: the round-93 spot-check's §6 routed defects 1-6 are dispositioned in this round's
report (routed 1: the report's landed-changes table is built from `git log --format` over the freeze
range; routed 2: the S385 rule-1 row is supplied above; routed 3: this round runs
`python3 tools/limine-pin-battery-r94.py --selftest --reference tools/check-limine-pins.py` before
six bends are scored; routed 4: the ten-digit enumeration and the probe-shape families name the
M13/M12/M03-M05/M11 survivors; routed 5: the not-word-char suffix guard is in the landed gate and
`REFUSAL-VERSIONS-10DIGIT` certifies it; routed 6: the contested kaidoku/revenger RE ownership is
reported, not absorbed). This round's own non-author closure is the hyaku closure.

## Mistakes

- **M1 (`calibration`, self-found) — a bend written from the battery docstring read the wrong clause and
  scored `met`.** Class: `calibration`. N01/N03 were written by editing the gate's `parse_limine_version`
  bound (`len(p) <= 9` → `<= 10` / `<= 11`) as if the published 1-9-digit bound lived in code; the
  battery's *docstring* described the REFUSAL family without the digit-count clause, so the first
  `N01` attempt bent "version must be X.Y.Z" and scored `met`. Captured-by: the make-bends rule itself
  (one clause bent, matched exactly once) — the substitution matched, but the *clause* was wrong.
  Fix: N01/N03 bend the `len(p) <= N` literal in `parse_limine_version`; each reads `unmet` with
  `REFUSAL-VERSIONS-10DIGIT` in `failed_families` (`after/bend-N0{id,…}.json`). Shown able to fail:
  a bend that matched zero times or the wrong clause reads `met` or a usage error in the battery
  receipt (the `make-r94-bends.py` exact-once guard raises, and the receipt records it).

- **M2 (`calibration`, disclosed) — a do-nothing battery carried into the wave was a diagnostic, not a
  receipt.** Class: `calibration`. The L1 ran the r93 battery (frozen at `ddd7e955…`) against the
  candidate gate before the freeze (96/96 `met` on the r93 roster, `after/r93-battery-on-r94-gate.json`,
  one run, 0 error rows), not as a control: the frozen target is `102/102`, which that battery cannot
  reach no matter what. Captured-by: QUALITY 114 (`R82-FROZEN-CONTROLS`) — a run of uncommitted
  counter bytes is development output. Fix: no number in this round's claims is derived from that
  receipt; the do-nothing battery and gate are committed with the freeze
  (`before/controls/do-nothing-battery-r93.py`, `do-nothing-gate-r93.py`), and the target is
  `102/102`, so the pre-change instrument cannot reach it. Shown able to fail: at the freeze commit the
  do-nothing battery reads 0 on the family block and the r93 gate reads `met` below the frozen target
  on the r94 roster only through the do-nothing legs, never through the landed gate's receipts.

- **M3 (`curation`, self-found) — the plan's USER-guide sentence lost a draft word mid-edit.** Class:
  `curation`. The first draft of `.ufo/plans/round-94.md`'s C2 surface paragraph needed a repair whose
  `PUT 81.=85:` replaced a five-line range that included lines never re-read since the previous edit;
  the edit consumed the `shokunin/conf` tail and left a backtick fragment. Captured-by: none for this
  shape — the edit's `N.=M:` contract forbids starting or ending mid-expression, and the L1 read only
  the partial range. Fix: the paragraph was re-read (`read :79-85`) and restored to three lines, then
  verified by a full-file `grep -n` of the C2 clause words. Shown able to fail: the restored text
  names the exact flag default line and the `pacman -Si limine` probe, and the frozen plan's sha256
  (`freeze-manifest.sha256`) binds it.
