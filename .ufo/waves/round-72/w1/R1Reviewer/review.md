# R1Reviewer — C1 semantic attack, round 72 w1 (2026-11-04)

Seat: attack the six planned MD rows; re-derive each from the committed v34 snapshot bytes, run the
frozen counter against a fixture mirror, probe counter channels, and judge host applicability from
`before/host.txt`. No SC1Entry draft existed in `.ufo/waves/round-72/w1/` at attack time and the
target note did not exist, so the re-derivation below IS the row draft under test: the frozen planned
propositions from SCORECARD.md at 6b42676 rendered into the frozen grammar, then falsified against
bytes. Fixture mirror: note + registry rows S301–S303 + byte-exact snapshot copies; counter run
`--fixture` (counter verified sha256 d615c653…70a6a6 before use).

## Baseline counter run (frozen counter, fixture mirror of the re-derived rows)

```
MD_ROW ok MD1 source=S301 snapshot=modprobe.d.5.scd
...
MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0
MD_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1   (rc 0)
```

## Row-by-row re-derivation

**MD1 — directory precedence, first-of-name suppression — verdict: holds.**
Cited bytes (man, CONFIGURATION DIRECTORIES AND PRECEDENCE): "Configuration files are read from
directories in listed in SYNOPSIS in that order of precedence. Once a file of a given filename is
loaded, any file of the same name in subsequent directories is ignored." (man typo "in listed in" is
in the snapshot; quotes must keep it if quoted). The statement entails: precedence order = SYNOPSIS
order, and same-name-later = ignored. Implementation side consistent within committed bytes:
libkmod-config.c:942-943 rejects a second insertion of the same name (`-EEXIST`, DBG "Ignoring
duplicate config file"), so first-scanned wins and later same-name files are never parsed — the
mechanism the man sentence names. Host: mechanism live (/etc before /usr/lib; /run and
/usr/local/lib absent so two scan calls no-op), suppression clause unexercised (no basename shared
between /etc's 3 and /usr/lib's 4 .conf names; /lib ≡ /usr/lib puts one directory behind two
SYNOPSIS entries, so precedence between those two entries is unobservable on this host).

**MD2 — one lexicographic order, partial replacement — verdict: holds.**
Cited bytes (man): "All configuration files are sorted in lexicographic order, regardless of the
directory they reside in." plus "Configuration files can either be completely replaced (by having a
new configuration file with the same name in a directory of higher priority) or partially replaced
(by having a configuration file that is ordered later)." No tension with MD1: complete replacement
is the same-name/first-wins mechanism seen from the survivor's side (code: EEXIST leaves only the
first copy parsed); partial replacement is different-name files overriding per-command later in the
one sorted order. Host: active with an observable consequence — the parsed set is 7 .conf files
(README is filtered by the `.conf` suffix check, libkmod-config.c:889-890) and they interleave:
parse order starts /usr/lib's bluetooth-usb.conf before any /etc file, and nvidia-utils.conf sorts
before nvidia.conf ('-' 0x2D < '.' 0x2E). Ordering, not precedence, decides which file is parsed
first on this host.

**MD3 — one sorted list, duplicate rejected — verdict: holds.**
Cited bytes (libkmod-config.c:920-946): `conf_files_insert_sorted` walks the list with strcmp,
`if (cmp == 0) { DBG(ctx, "Ignoring duplicate config file: %s/%s\n", path, name); return -EEXIST; }`.
Host: the most consequential row here — /lib/modprobe.d and /usr/lib/modprobe.d are one directory
(host.txt readlink both → /usr/lib), so kmod_config_new's per-path loop (line 1020-1041) offers
every one of its 4 .conf names twice; the EEXIST branch is what collapses the aliased directory to a
single parse. Without MD3 exactly this host would double-parse its /usr/lib modprobe config.

**MD4 — kernel command line into the same config object, after the files — verdict: holds.**
Cited bytes (libkmod-config.c:1044-1084): the parse loop walks the sorted `list` file by file
(`kmod_config_parse(config, fd, fn)`), then `kmod_config_parse_kcmdline(config);` is the last
statement of `kmod_config_new` before return — same `config` object, strictly after the files.
Host: **active, and the declaration's host-fact sentence is wrong about it** — see F1.

**MD5 — dry-run prints, executes nothing — verdict: holds.**
Cited bytes (modprobe.c): help lines 128-129 ("Do not execute operations, just print out" /
"--show Same as --dry-run"); command path `SHOW("%s %s\n", type, cmd); if (dry_run) goto end;`
before `system(cmd)` (lines 297-300); rmmod `SHOW("rmmod %s\n", modname); if (dry_run) return 0;`
(line 322-323); insert path adds `KMOD_PROBE_DRY_RUN` (line 624). Every execution branch visible in
the snapshot is gated. Host: live capability on kmod 34.2.

**MD6 — alias-only by default, unconditional only with --use-blacklist — verdict: holds.**
Cited bytes (modprobe.c:624-629): `flags |= KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY;` is
unconditional; `if (use_blacklist) flags |= KMOD_PROBE_APPLY_BLACKLIST;` is the only widening, set
by `-b/--use-blacklist` (line 62, 808). The man page snapshot alone does NOT state the
alias-only-by-default half — the row must stay anchored on S303 (tools/modprobe.c), which the
planned registry mapping does. See F2 for the quote-cell pipe hazard on this row.

## Host applicability table (from before/host.txt; config contents never read, per boundary)

| row | on this host |
|---|---|
| MD1 | mechanism live; suppression clause inert (no cross-directory name collision; /lib≡/usr/lib makes its own precedence pair unobservable) |
| MD2 | active: 7 .conf files interleave across /etc and /usr/lib; first parsed file is /usr/lib's bluetooth-usb.conf |
| MD3 | active and load-bearing: collapses the /lib≡/usr/lib aliased directory to one parse per name |
| MD4 | active: 4 cmdline tokens are parsed into the config object every run (F1); declaration sentence says otherwise |
| MD5 | live capability (kmod 34.2) |
| MD6 | mechanism live for alias probes; host consequence untestable under paths/modes-only boundary; no `modprobe.blacklist=` token on cmdline |

## Findings

- **F1 (MD4 host applicability, medium).** The frozen declaration asserts "/proc/cmdline carries no
  module.parameter token". Its own captured cmdline contradicts this: `zswap.enabled=1`,
  `zswap.max_pool_percent=25`, `vt.global_cursor_default=0`, `systemd.show_status=false` all match
  modname.param=value and are accepted by the state machine (single '.' in STATE_MODNAME splits
  modname/param, libkmod-config.c:717-725; `underscores(modname)` validity passes; result added via
  `kmod_config_add_options`, lines 610-634). Dropped tokens for contrast: rd.udev.log_level=0
  (second dot → STATE_IGNORE), resume=/dev/mapper/root, loglevel=0, rootfstype=btrfs ('=' in
  STATE_MODNAME → STATE_IGNORE). Correction: restate the host fact as "no `modprobe.blacklist=`
  token; four modname.param tokens present (zswap x2, vt, systemd) and parsed into the config
  object". MD4 is not inert on this host.
- **F2 (MD6 drafting hazard, low).** The natural code quote `flags |= KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY;`
  contains `|=` — an 8th pipe, which trips the counter's `line.count("|") == 7` gate → malformed-row.
  MD6 must quote the help text ("Apply blacklist to resolved alias.") or a pipe-free code span.
- **F3 (counter channel, medium).** Negation-keeping-vocabulary passes the frozen counter (met=1,
  rc 0) — lexical grounding has no entailment channel. The declaration's planned-next-round note
  already names this; fixture confirms it empirically at the frozen counter digest.
- **F4 (counter channel, medium).** `kind=community` at tier A passes: `community` is in the
  counter's KINDS set and the tier cell (registry cell 4) is never read. A community-sourced rule
  row bound to the map URL verifies met=1. Correction for next round's counter: treat community
  like own-work for rule rows, or read the tier cell.
- **F5 (structural channels hold, proof).** An MD9 hidden inside a fenced code block is NOT
  invisible: CAND_RE ignores fences, the row is counted (rows=7, ids-not-contiguous,
  snapshot-reuse modprobe.d.5.scd=3) → met=0, rc 1. A quote taken from a different snapshot than
  the cited one is caught (quote-absent → met=0). Drafting cannot hide behind fences or
  cross-snapshot quotes.
- **F6 (verification gap, low).** That the implementation scans directories in SYNOPSIS order is
  not provable from the three committed snapshots: `config_paths` is built in libkmod.c, which is
  not snapshotted. MD1/MD2 cite the man page (S301) and stand on its bytes; any note sentence
  asserting the implementation's directory ORDER would exceed committed bytes.

## Verification status

Counter digest verified before use (d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6);
snapshot digests re-hashed and match SHA256SUMS/SOURCES.json; all six quotes verified verbatim by the
counter itself (baseline run shows no quote-absent); grounding shares computed empirically by the
frozen counter, not estimated. Scratch tree deleted before yield.
