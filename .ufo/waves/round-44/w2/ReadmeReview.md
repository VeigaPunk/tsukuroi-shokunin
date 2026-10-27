VERDICT: defect-found

Item R-3 — review of the integrated PROVINCE.md round-44 promotion note ("Round-44 promotion — R44-SCRUB-VIEW") and the corpus/README.md round-44 coverage note + Frontier notice: wording vs the measured sub-surface; counting commands and receipts.

Reviewed state: lane HEAD `3a1c6b5c`; notes committed at `8728e8bc` and untouched since (`git log -- PROVINCE.md corpus/README.md`); `tools/tsukuroi-census.sh` and `corpus/knowledge/btrfs-scrub-record-r44.md` byte-unchanged since measured tip `8eee79db` (`git diff --stat 8eee79db..HEAD -- tools/tsukuroi-census.sh corpus/knowledge/btrfs-scrub-record-r44.md` is empty), so every line number below holds at the measured revision too.

## DEFECT (minor — citation precision)

`corpus/README.md:433` (round-44 coverage table, census row, Sources cell) cites
`contract tools/tsukuroi-census.sh:384-412`.
The "Round-44 addition (C1)" contract paragraph is `tools/tsukuroi-census.sh:384-408`: it starts at :384
(`# Round-44 addition (C1): the scrub-record arm. …`) and ends at :408 (`# text, rollup term or exit code
changes) and live mode creates no files.`). Lines 409–412 are a blank comment line plus the generic
"Read-only guarantee" paragraph (:410–412: "no probe writes; the gate creates no files at all in live mode
… Secrets are never read…"), which speaks of the whole gate, not of the round-44 arm — so the cite
labelled "contract" overshoots the contract by four lines. All other line anchors in both docs are exact
(checked: `corpus/README.md:243` promotion-condition bullet; `corpus/README.md:315` round-39 notice
paragraph carrying `detail=mounts:btrfs-without-sysfs`, cited by PROVINCE for the mount-table guard).

## Verified — wording matches the measured sub-surface

Implementation: `probe_scrub_record` at `tools/tsukuroi-census.sh:1965-2042`; print order in `main()`
(:3418-3421 STORAGE then SCRUB, rollup :3423-3438); contract :384-408.

- Line shape: the format string :2039 is field-for-field the line both docs document (`SCRUB
  btrfs-scrub-record state=… dir=… records= tmp= sockets= unreadable= orphan= limited= timers= [detail=…]`).
- Placement/neutrality: printed after the `STORAGE` line and before the `TSUKUROI_CENSUS` rollup, exactly
  as PROVINCE says; the rollup and the exit code are derived only from the six PLANE verdicts
  (:3423-3438) — "never a rollup term and never an exit-code input" holds by construction, and selftest
  cases confirm BLOCKED scrub lines leave `TSUKUROI_CENSUS: HEALTHY` (e.g. :3260-3262, :3281-3283).
- Name-and-stat-only under `/var/lib/btrfs`: record/tmp regularity tested, readability counted (`-r`),
  content never read; sockets via `-S`; wrong-type names BLOCKED with `record:not-regular`,
  `tmp:not-regular`, `progress:not-socket`; no name echoed. Orphan = a record fsid absent from a listable
  sysfs root; sysfs absent / not-a-directory with records → BLOCKED (`sysfs:absent`, `sysfs:not-directory`)
  — matches both docs' known-limit wording.
- `scrub_speed_max` (SR8): single nonzero decimal → `limited` + `detail=<fsid8>:<devid>:speed_max=<v>`;
  `0` and zero-padded `000` → no limit; empty/malformed/unreadable → BLOCKED (`speed-malformed`,
  `speed-unreadable`) — matches PROVINCE/README and the header contract.
- Timers (SR9): `btrfs-scrub@*.timer` links under `TSUKUROI_TIMER_WANTS` (default
  `/etc/systemd/system/timers.target.wants`); the bare template name is skipped (:2017) and directories
  are not instances (:2019) — "the bare template name is not an instance and is not counted" holds.
- Overrides: `TSUKUROI_SCRUB_DIR`, `TSUKUROI_TIMER_WANTS` as documented; the probe makes no ioctl, calls
  neither `btrfs` nor `systemctl`, needs no privilege and creates no file.
- README table row 1's state rule ("BLOCKED when a reading is unavailable, RECORDED when record/tmp/socket
  names exist") matches :2038 (blocked takes precedence, then rec+tmp+sock > 0, else NONE).
- PROVINCE's namespace-leg sentence (mount-table, `uid_map`, script path; QUALITY 90 "named open";
  control C1-K7) matches the declaration's control record and the receipt's `channels_open`
  (["mount table", "uid_map", "script path /mnt/census-lib.sh"]).

## Verified — counting commands

- PROVINCE: `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` — both flags are
  required by the frozen tool (argparse :513-514); its sha256 is `1409a5fd75adaa4c0a238a7f9ad31621dd34a52
  ad1a40483e4a18d27c9536388` (recomputed this seat), equal to the declared freeze; the quoted predicate
  string is byte-identical to the receipt's `predicate` field.
- README: `../tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` (corpus-relative) and
  `tools/check-scrub-record-r44.py --revision <REV>` — both runnable as written (`--revision` required;
  `--lane`/`--sessions` defaulted per the counter's usage docstring). The frame-less `tools/…` form
  matches the round-43 coverage-table precedent (`counter tools/check-scrub-record-r43.py`,
  corpus/README.md:420), so it is not the defect. The quoted depth predicate (rows/quotes_ok/props_ok/
  host_ok/sources_ok/verdicts_ok/novelty_base_hits/pointer_ok) matches the counter docstring word for
  word; the tool's sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059` (recomputed)
  equals the declaration. Its verdict binding (seats `C2RevSR<n>`/`C2CritSR<n>` via `w2-dispatch.json` +
  `w2-results.json`, report first line identical to the verdict line, `partly` needing a bound residual
  `C2ResSR<n> holds`) matches the README sentence "its three row verdicts binding only from the round-44
  wave-2 reviewer and critic seats"; `w2-dispatch.json` names each of the six seats exactly once.
- Selftest count: PROVINCE's "The census selftest reports 148 cases, sixteen of them labelled `(R44-C1)`"
  re-verified empirically by this seat at HEAD: `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed,
  0 failed)`, exit 0 (receipt `selftest-r44-head3a1c6b5c.log`); 16 `R44-C1` labels in the file — coherent
  with the declaration's nine cases (132 → 141) plus wave-1 hardening's seven (141 → 148).

## Verified — receipts

- `.ufo/waves/round-44/after/c1-after-8eee79db.jsonl`: `revision 8eee79db…` (the measured tip),
  `tool_revision 1d2afff…` (the freeze commit), `verdict PASS`, `exit_code 0`; `live.got == live.want` ==
  the exact host line both docs quote (`SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0
  sockets=0 unreadable=0 orphan=0 limited=0 timers=0`); `selftest_line` "PASS (148 cases, 148 passed,
  0 failed)", `selftest_r44 16`; `cases 16 / correct 16 / identity_ok 1 / wired_ok 1 / live_agree 1`.
- README's "Host at the measured revision … consistent with S245": S245 `capture.txt` (sha256
  `efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900`, equal to the depth counter's pin)
  shows `var_lib_btrfs absent` (:3), `scrub_speed_max … value=0` (:4), `wants_btrfs_scrub_instances 0`
  (:5), the instance `disabled` (:6) — consistent with the measured NONE/absent/all-zero line, and the
  entry's host readings cite existing capture lines.
- Forward reference, not a defect: both docs point to `SCORECARD.md` "Round 44 — measured outcome",
  which does not exist yet at wave 2 (SCORECARD.md:2746 declaration is the only Round 44 section). That
  is the established declare-then-admit convention (round 43's outcome section likewise postdates its
  declaration); the L1 fills it at admission. No repair proposed.

## Proposed text (the one repair)

`corpus/README.md:433`, round-44 coverage table, census row, Sources cell:

    contract `tools/tsukuroi-census.sh:384-412`  →  contract `tools/tsukuroi-census.sh:384-408`

If the intent was to include the generic read-only guarantee, cite it explicitly, e.g.
`contract tools/tsukuroi-census.sh:384-408 (read-only guarantee 410-412)` — but a cite labelled
"contract" should bound the "Round-44 addition (C1)" paragraph, which ends at :408.

Seat receipt: `.ufo/waves/round-44/w2/ReadmeReview/selftest-r44-head3a1c6b5c.log`.
