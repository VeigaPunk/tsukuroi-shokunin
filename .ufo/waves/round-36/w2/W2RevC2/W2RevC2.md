# W2RevC2 — seat report (round 36, wave 2, falsify)

Scope: adversarial review of the landed C2 note
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journalctl-v262-field-filter-r36.md`
at `c052bb7d41ced49aa888817069afd804eccfecf1` (blob sha256
`0077b6cf7e81ef243997fe5bd8559f5e21569290f271b2f60cb0cd1b57a8a8bf`), against the wave-1 blocking
findings and the round's receipt rule. Evidence captured up to 04:41:08Z (pasted from
`date -u +%H:%M:%SZ`).

## Result

**Verdict: blocking** — 5 blocking, 8 minor. Full findings with line-level evidence and fixes:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w2/W2RevC2/review.md`;
machine output: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w2/W2RevC2/findings.json`.

Blocking, one line each:

- **B1** — wave-1 B1 unclosed: no third "allowed, output silently altered" state. `ext_lines1_F`
  (`-n 1 -F PRIORITY`) is exit 0 with **2 stdout bytes / one value** vs `core_plain` 12 bytes / six values;
  `ext_lines1_N` 2882 == `ext_plain_N`. Mechanism is truncation, not action replacement: `-F` keeps
  `ACTION_LIST_FIELDS` (`journalctl.c:806`) and `-n` sets `arg_lines` (`:221`). `corpus/README.md:269`
  already advertises the missing state.
- **B2** — `--file` (valid path) missing from the table (`:43`) and from both matrices (`grep --file` = 0
  in `matrix-mini.json` and `ExecC2Live/matrix.json`); wave-1 B2 required it. `-D/--root/--system/--user`
  are covered and verified.
- **B3** — §Safe substitution `:58` "Verified live here" has no receipt (no `jq`/`sort -u` cell in either
  matrix); violates QUALITY 2 and the wave receipt rule.
- **B4** — `cap()` hazard `:84` "Measured here … Replicated" has no receipt (`No entries`/`CAP_OUT`
  absent; `ext_grep_F` exists but is unnamed; the no-match comparison run is unrecorded).
- **B5** — prior-state `:88` "no lane entry documented this rejection" is contradicted by
  `corpus/lessons/round-1.md:111` (NEWS rejection quote; pin historical per `:127-129`); the exact-string
  sweep is sound (verified exactly `SCORECARD.md:1632` at the base) but does not support the sentence.
  Also "re-run in the working tree" cannot reproduce at `c052bb7` (the grep now returns the note itself).

Minor: predicate is 15 terms not 16 (note `:126`, `README.md:264,269`); consumer count "43/4" needs
`--exclude-dir=__pycache__` and "every occurrence" should be "every invocation site"; fixture-default
claim only holds for flag-only invocations; `--machine/--image` unmarked; QUALITY 26 gloss false
(`pacman -Q` in the header, redundant vs `journalctl --version`); positional `FIELD=VALUE` claim
unreceipted/wrong guard line; falsifier 4's `-b 0 -n 1 -F` unrun; **M8** action precedence
(last-action-wins, `journalctl.c:802/806/813/825/856/877-878`) is undocumented, so `live_list_boots`,
`ext_diskusage_N`, `ext_header_F` and `ext_sync_F` never execute the named non-field action — `--sync`
in particular is a write request the tested ordering bypasses, so the row must not generalize read-only
safety.

Provenance: B2's `--file` exit-0 receipt is `ReviewC2Draft.md:61`'s live table (that seat's `matrix.out`
records only `--file /nonexistent` rc 1, so a real-path cell is still needed), not mine — I measured the
missing cell/occurrence; the wave-1 checklist is evidence, not a canonical acceptance list, and the
blocking rank rests on this seat's brief naming `--file` plus the row's incompleteness.

## Verified clean (supporting the parts that hold)

Rejection line 83+LF=84 bytes, exit 1, guard `journalctl.c:958-960`; 15/15 predicate terms have a
rejecting cell; 40 distinct table pointers resolve; 54/54 cells carry argv/exit/stderr/stdout/sha;
10/10 peer runs map to a note cell and agree; header gate `PASS` at `c052bb7` (56/56 notes, findings
`[]`) with S198/S199 tier A, 2026-10-23, on-release; rejection string absent from the Arch man render,
v262 xml and full NEWS (0/0/0); no lane tool invokes journalctl with `-F`/`-N` (grep empty); every cited
consumer line number verifies (census `:971`…`:1412`, `cap()` `:541-546`, `case` `:1247-1251`, fixture
`:1883-1900`; score `:150-165`, `:708-731`; boot-chain `:870`; scope `:174`).

## Residual risk / gaps

Matrix not re-executed (review rests on the recorded cells plus read-only source/git/gate checks);
`--machine/--image` remain `[unk]`. Cross-axis observation for the sentinel/critic seats, not judged
here: the "pre-freeze corrections" block is present only at `c052bb7` (pure append, 0 deletions), not at
the base or freeze commits; freeze commit `1e92680` is an ancestor, commit times freeze `01:28:11 -0300`
vs change `01:28:31 -0300`, block text `04:22Z`.

## Tooling and scope compliance

No installs, no package-manager run (pacman never invoked), no VCS mutation, no delegation, no writes
outside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w2/W2RevC2/`. Commands used:
read-only `git show/cat-file/diff/grep`, `grep`/`wc`, `python3` JSON/regex analysis, and
`python3 tools/check-knowledge-header.py --revision c052bb7…` (the lane's read-only header gate).
