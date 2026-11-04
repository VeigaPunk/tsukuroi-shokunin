# R1Reviewer — tsukuroi r73 w1

status: complete
verdict: 2/6 rows hold — UL6 fails, UL1/UL2/UL4 partly hold; instruments form-only (4 attacks survived, 2 held); host delta none

Full findings: `.ufo/waves/round-73/w1/R1Reviewer/report.md`.

Summary:
- Pins verified (SHA256SUMS, SOURCES.json, both instrument digests match the declaration); both
  selftests PASS (11 and 5 cases) under scratch TMPDIR.
- Counter: rc=128 UL_NOTE absent at base/declaration/HEAD (note not yet landed). Checker:
  ROUTED_STALE=3 at base and HEAD. Registry S304-S306 rows absent — must be committed in the
  same revision as the note or the counter reports source-unregistered.
- Row verdicts vs pinned v262 sources: UL3 holds, UL5 holds; UL1 partly (SYSTEMD_UNIT_PATH
  trailing-`:` append exception, xml:374-378); UL2 partly (drop-in precedence scope "under those
  directories", xml:237-238); UL4 partly (predicate is null_or_empty of the file at the fragment
  path; trigger is content/stat change, not path change; null_or_empty defined outside the
  snapshots, stat-util.h:50-52); UL6 fails (enable creates dangling alias symlinks via
  `create_symlink(..., force || broken, ...)`, install.c:2013-2021; INSTALL_CHANGE_IS_DANGLING
  fires on removal paths, install.c:2308-2313, 350-351). ROWS_HOLD=2/6.
- Attack log: A word-salad statement survived, B unrelated-region quote survived, C copied-quote
  writer survived by design, E unanchored registry anchor survived; D pipe-in-quote held;
  hermeticity held. Corrections offered per row in the report.
- Host re-measure: 12 unit-paths, 2 /dev/null masks in /etc/systemd/system, passim masked with
  FragmentPath=/etc/systemd/system/passim.service, user@1000 drop-ins both present in same order,
  getty@tty1 → getty@.service loaded. Delta from before/host.txt: none.
- No tools installed; no lane writes outside my wave dir; no git/jj mutation; scratch deleted.
