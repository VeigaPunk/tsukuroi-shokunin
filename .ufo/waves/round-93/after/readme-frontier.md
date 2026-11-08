## Round 93 — the 12.9.5 tag's own cut, and the installed-version probe

New ground: `knowledge/limine-version-probe-r93.md` (VP1-VP4, S382-S384) — the v12.9.5 tag's own
`common/lib/config.c` carries the cut (byte-identical to v12.9.6 in this clause, sha256 `a940acae…`),
the v12.9.5 ChangeLog dates the parser change to that release, and `limine --version` prints
`Limine <X.Y.Z>` as its first line (`host/limine.c` raw 2029; `--version` dispatch raw 2090). Battery
`tools/limine-pin-battery-r93.py` (96 families) adds four era/refusal families that close three of
round 92's named limits and kill its `N04-accept-any` survivor, plus three probe families for the
gate's V3 `--limine-version auto`. The three new tools/rows are registered in SKILL.md (R93-REG-1).

### Frontier (round-93 addition)

- The r92 launcher residuals (argv via `/proc`, host fingerprint, writable gate-copy parent, `/dev`
  writes; r92 A6) stay open and uncertified; the r93 battery adds a PATH channel for its fake
  `limine` and names it in the docstring, so a later totality claim must close the rest or narrow.
- The probe reads the first `X.Y.Z` of `limine --version`; a pre-release answer (`12.9.6-rc1`) would
  read as `12.9.6` [inference from the regex, not measured on a release binary]. A release-format
  change is a re-pin of S384.
- `--limine-version` still defaults to `12.9.4` (the host package): the probe is opt-in, so a host
  upgraded without `auto` is judged under the old era. Making `auto` the live default is a later
  round's claim (it changes the default's meaning and needs its own freeze).
- `REFUSAL-VERSIONS` certifies ten out-of-range spellings (rc 64, empty stdout); other refusal
  classes (e.g. a non-UTF-8 probe output) are not in its finite set.
- Still open from r89: blanks before CR-LF, ESP containment, empty labels.
