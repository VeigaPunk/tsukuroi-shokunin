# SC3Index — index/doc deltas C1 owes (round 73, w1)

Grounding: every claim in these drafts cites UL1-UL6 of `corpus/knowledge/systemd-unit-load-plane-r73.md`
or a committed host reading in `.ufo/waves/round-73/before/host.txt`. Two host values were re-measured
read-only for this seat and are marked as such. No new plane fact is introduced.

Placement and selector rules:

- **All four drafts are append-only.** Append A and B (in that order) at the end of `SKILL.md`, C at the
  end of `PROVINCE.md`, D at the end of `corpus/README.md`.
- **Do not create a `## Gate and probe registry — round73 superseding current rows` heading.** By the
  operative-selector paragraph (SKILL.md:1999; carried into the r71 preamble) the unique highest-numbered
  heading of that exact form becomes the operative table, so a fresh one holding only two rows would
  silently drop every carried row. Round 72 set the precedent: a `## Round 72 — … registry row
  continuation (append-only)` section with its own single-header table. Draft B follows it.
- **Both instruments moved under wave 1.** `tools/check-r72-routed-r73.py`: `93f034e3…` (202 lines,
  declaration, `--selftest` five cases) → `316dd51a…` (267 lines) → `328a6bf6…` (279 lines, eleven cases).
  `tools/count-ul-rows-r73.py`: `542f9c…` (409 lines, declaration, eleven cases) → `84501ab8…` (423 lines,
  twelve cases, the new `EMPTYQUOTE` case). Both carry ` M` in the working tree. Draft B therefore pins each
  construction and requires the digest to be re-read from the committed blob at the measured revision, with
  the round's erratum rule applied; see §F1.
- Each table below has **one header row** and no second header inserted mid-table (QUALITY 92). Rows are
  separated by a blank line before the header only.
- The decision table authorizes no unit action. It names what a repair reader may conclude and what to
  check; every mutating verb in it is the operator's.

## A. `SKILL.md` — append (decision table)

```SKILL.md
## Round 73 — the systemd unit-load merge plane (decision table)

Read-only decision table for an observed unit-load shape. Every row rests on a rule row of
`corpus/knowledge/systemd-unit-load-plane-r73.md` (UL1-UL6; sources S304-S306, systemd **v262**) or on a
committed host reading (`.ufo/waves/round-73/before/host.txt`). **No row authorizes a unit action:** mask,
unmask, enable, disable, edit, `daemon-reload`, start and stop are the operator's, and the lane never runs
them. The table states documented merge and precedence rules; it never states the resolved value of a
specific unit's merged configuration.

| # | Symptom (reported) | Mechanism | Row | Check (read-only) |
|---|---|---|---|---|
| T1 | my drop-in is ignored | The drop-in directory is keyed by the unit name and only `.conf` files enter it. A drop-in of the **same** basename is read from the highest-precedence directory (`/etc` over `/run` over `/usr/lib`), while **different** names from all three merge in one lexicographic pass parsed after the unit file; drop-ins outrank the unit file wherever it lives. If the file is already in the manager's set, the cause is T3 (no reload), not precedence. | UL2 (UL1 for the unit file under the set) | `systemctl show -p DropInPaths -p FragmentPath <unit>`; `systemctl cat <unit>`; `systemd-analyze unit-paths` (12 directories on this host) |
| T2 | my override vanishes after a package update | A drop-in outranks the **whole unit file**, including an `/etc/systemd/system/<unit>.service` copy: replacing the unit file in `/etc` does not displace a vendor drop-in under `/usr/lib/systemd/system/<unit>.d/`. Directory precedence (`/etc` over `/run` over `/usr/lib`) ranks **drop-ins of the same name**, so the copy that outlives an update is a same-named `/etc` drop-in, not a copied unit file. | UL2 | `systemctl cat <unit>` (prints the fragment, then the drop-ins the manager holds in its set — a same-named duplicate that lost precedence is not in that set); `systemctl show -p FragmentPath -p DropInPaths <unit>` |
| T3 | the unit says "changed on disk" or needs a reload | The manager compares the drop-in path list it read at load time with the list computed now, and the drop-in mtimes with the last reload; a new, removed or newer drop-in sets the flag, and masked drop-ins are omitted from the compared list, so masking a drop-in also changes it. | UL3 | `systemctl show -p NeedDaemonReload -p DropInPaths <unit>` (the manager's own flag; observed `NeedDaemonReload=no` re-measured on `user@1000.service`) |
| T4 | the unit is masked | A mask is a fragment that is empty or a symlink to `/dev/null` at the unit name in a directory outranking the real file. While the fragment path is null or empty the unit stays masked and `LoadState` reads `masked`, even though `FragmentPath` still names the mask path. | UL4, UL5 | `systemctl show -p LoadState -p FragmentPath <unit>`; `readlink -f <FragmentPath>`; `stat -c %s <FragmentPath>` (host: `passim.service` reads `LoadState=masked`, `FragmentPath=/etc/systemd/system/passim.service` → `/dev/null`) |
| T5 | the unit is masked but still enabled | Masking is a load-plane state and it is reported first: `systemctl is-enabled` prints `masked` with exit 1, and both `UnitFileState` and `LoadState` read `masked`. The `enabled` word in `systemctl list-unit-files --state=masked` is the **PRESET** column — the header is `UNIT FILE  STATE  PRESET` — so the row `masked enabled` means "state masked, preset enabled", not an enablement that survived the mask. | UL4, UL5 (masked versus masked-runtime; the install mode) | `systemctl list-unit-files --state=masked` (read the header); `systemctl is-enabled <unit>`; `systemctl show -p LoadState -p UnitFileState <unit>` (host: `systemd-networkd-wait-online.service` row `masked enabled`; re-measured `LoadState=masked UnitFileState=masked`, `is-enabled` prints `masked` rc 1) |
| T6 | the instance has no file | There is no file named after an instance: the name resolves to its template unit file, and the drop-in set is looked up for the instance directory first and then for the template directory. On this host `getty@tty1.service` resolves to `/usr/lib/systemd/system/getty@.service` with `DropInPaths=` empty, and `user@1000.service` reads exactly two template-directory drop-ins while no `user@1000.service.d` exists in `/etc` or `/usr/lib`. | host readings H4, H5; the instance-then-template drop-in lookup is documented in the S304 paragraph the UL2 quote comes from, but no UL row states it (the entry's Limit 2 records the instance-only directory as documented-not-measured); UL2 orders the files inside each set | `systemctl show -p FragmentPath -p DropInPaths <unit>`; `systemctl cat <instance>`; `ls -d /etc/systemd/system/<instance>.d /usr/lib/systemd/system/<instance>.d` |

Named limits, not table rows: `systemctl show` and `systemctl cat` report the manager's **parsed** copy at
its last reload, so they answer "what the manager read", not "what the files say now" — a discrepancy is
T3, not a merge rule. The package side of `/usr` is the package plane's and is not claimed here. Whether
`.wants` symlinks survive behind a mask is enablement state, not this plane, and is not read. The instance
directory leg is documented and absent on this host. No row states which line of a fragment wins.
```

## B. `SKILL.md` — append (registry continuation rows)

```SKILL.md
## Round 73 — `count-ul-rows-r73` and `check-r72-routed-r73` registry row continuation (append-only)

Append-only continuation rows for the `## Gate and probe registry — round71 superseding current rows`
table; the r71 table and the round-72 continuation stay as written, and **no round-73 superseding table is
created** (a fresh highest-numbered `## Gate and probe registry — round<N> superseding current rows`
heading would become the operative table and drop every carried row). Each row below sits in its own
single-header table.

### count-ul-rows-r73 (this round's frozen C1 counter)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| count-ul-rows-r73 | gate | `python3 tools/count-ul-rows-r73.py --revision <REV>` (or `--fixture <DIR>`) | 0 target met (`UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`); 1 target missed, including `UL_MAP malformed`; 2 could-not-evaluate under `--selftest` only (`$TMPDIR` names no directory, or resolves to `/tmp`); 3 self-test failed (the declaration writes this code as `-3`; the process exit value is `3`); 128 `UL_NOTE` / `UL_REGISTRY` / `UL_MAP` absent | `python3 tools/count-ul-rows-r73.py --selftest` — hermetic, **twelve** cases over fixtures it copies into one `$TMPDIR` root, one `PASS (SELFTEST-<ID>)` / `FAIL (SELFTEST-<ID>)` line each and a closing `SELFTEST: PASS (12 cases, 12 passed, 0 failed)`: CONTROL (`UL_TARGET`, rc 0); SHORT (`statement-words`); UNREGISTERED (`source-unregistered`); QUOTE (`quote-absent`); FIVE (`UL_ROWS=5`); DUPID (`duplicate-id`); REUSE (`snapshot-reuse`); UNGROUNDED (`statement-grounding`); MALFORMED (`malformed-row`); DIGEST (`digest-mismatch`); OWNWORK (`source-kind`); EMPTYQUOTE (`quote-words`, an empty quote is not admitted) — each case asserting its named finding token | tool sha256 **re-read from the committed blob at the measured revision** — the declaration instrument `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` (409 lines, eleven cases) moved to `84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` (423 lines, twelve cases) inside wave 1, so the erratum rule applies to this instrument too; note `corpus/knowledge/systemd-unit-load-plane-r73.md`; registry `corpus/SOURCES.md`; snapshots `.ufo/waves/round-73/before/src/{systemd.unit.xml,unit.c,install.c}` plus `SOURCES.json`, tag v262, base URL `https://raw.githubusercontent.com/systemd/systemd/v262/`; per row: unique contiguous id, statement of at least 12 words, at least 6 distinct non-stopword tokens of length at least 4 shared with the row's own snapshot and shared/total at least 0.5, `source=S###` row present at the same revision whose source cell carries the map URL and whose anchor cell carries the snapshot basename, kind in the nine source kinds and not `own-work`, snapshot sha256 equal to both the `digest=` cell and the map sha256, quote of at most 25 words without a pipe located verbatim whitespace-normalized; any snapshot cited at most twice; any `UL`-shaped line that does not parse is a `malformed-row` finding; the row-shape rule is seven pipes on the row line | committed reads (Git objects at `--revision`) or a read-only `--fixture` mirror; `--selftest` writes one private `$TMPDIR` root and nothing else, refusing a `$TMPDIR` that resolves to `/tmp` | tsukuroi |

### check-r72-routed-r73 (this round's frozen C2 checker)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| check-r72-routed-r73 | gate | `python3 tools/check-r72-routed-r73.py --revision <REV>` (or `--root <DIR>`) | 0 all three routed items satisfied (`ROUTED_STALE=0 ROUTED_OK=3/3`); 1 one or more stale — findings `LESSON-STALE`, `DIGEST-STALE`, `CAPABILITY-STALE`, each printing `reason=` one of `no-block`, `block-tokens`, `block-need-any`, `block-no-supersede-verb`, `block-digest-direction`, `block-incomplete`, `receipt-absent`, `receipt-count`, and an unreadable required file printing `<FINDING> absent path=<path>`; 2 only under `--selftest` when `$TMPDIR` names no directory; 3 self-test failed. `evaluate` returns only 0 or 1, so the module docstring's "2 cannot evaluate (a required file is absent)" is unreachable in `--revision` mode | `python3 tools/check-r72-routed-r73.py --selftest` — hermetic, **eleven** cases under one `$TMPDIR` root, `PASS (SELFTEST-<ID>)` each and `SELFTEST: PASS (11 cases, 11 passed, 0 failed)`: CONTROL (`ROUTED_STALE=0`, rc 0); LESSON; DIGEST; CAPABILITY; UNANCHORED (every token in prose that is not a line-start `## ` block); RECEIPT-SUPERSTRING (`<receipt>.bak` must not satisfy the receipt token); RECEIPT-MISSING (`receipt-absent`); RECEIPT-NINE (`receipt-count`, nine cases is below ten); SUBSTRING-TEN (`often` must not satisfy `ten`); DIGEST-REVERSED (new digest written before the old); VACUOUS (tokens only, no supersession verb) | tool sha256 **re-read from the committed blob at the measured revision** — observed moving inside wave 1: `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e` (202 lines, the declaration instrument, five cases) -> `316dd51aacc29e1590fbea27657e81956a30198f377d14c52d41ae2369419441` (267 lines) -> `328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` (279 lines, eleven cases), and the round's instrument-change rule requires an appended erratum naming old->new digests with a same-instrument before-control re-run; files `corpus/lessons/round-72.md` and `SCORECARD.md`; instrument digests `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` -> `2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc`; receipt `.ufo/waves/round-72/after/selftest-selftest-after.txt`, which must exist at the same revision and report at least ten cases (`SELFTEST: PASS (N cases, N passed, N failed)`); a token counts only as a whole token inside a line-start `## ` block whose heading matches that item (correction or erratum for LESSON and DIGEST, capability or refresh for CAPABILITY), LESSON and DIGEST also need a supersession verb, DIGEST a digest direction, and LESSON and CAPABILITY a committed receipt | committed reads (Git objects at `--revision`) or a `--root` mirror; `--selftest` writes one private `$TMPDIR` root and nothing else | tsukuroi |
```

## C. `PROVINCE.md` — append (Frontier → Core)

```PROVINCE.md
## Round-73 entry — R73-UNIT-LOAD-VIEW: the systemd unit-load merge plane enters Core

Append-only; the round-70, round-71 and round-72 sections above stay as written. This is a **new area**:
the held-ground sweep at the declaration base `eb105757` read **0** lines for `unit_load_dropin`,
`dropin_paths`, `unit_need_daemon_reload`, `null_or_empty`, `unit_file_mask` and `config_parse_alias`
across `corpus/ SKILL.md PROVINCE.md`; `unit load path`, `unit search path`, `FragmentPath` and
`DropInPaths` read **0** files; and every `corpus/knowledge/` `drop-in` hit is a host observation of a
named drop-in file or an mkinitcpio hook context, none of them a merge rule. The entry is
`corpus/knowledge/systemd-unit-load-plane-r73.md`, rows UL1-UL6, sourced S304-S306 (`man/systemd.unit.xml`,
`src/core/unit.c`, `src/shared/install.c` at systemd **v262**, the tag matching the installed
262.1-1-arch; snapshots committed byte-exact under `.ufo/waves/round-73/before/src/`).

**Core now — the reading:** the six rules a repair reads before touching a unit. Unit files load from a
compiled load path in which a directory listed earlier overrides a same-named file lower down, and
`SYSTEMD_UNIT_PATH` replaces that whole path (UL1). Drop-in `.conf` files merge in one lexicographic pass
parsed after the unit file, `/etc` outranks `/run` which outranks `/usr/lib` for a same-named file, and a
drop-in outranks the unit file wherever that file lives (UL2). A loaded unit needs a daemon reload when the
drop-in path list differs from the list read at load time or a drop-in is newer than the last reload, and
masked drop-ins are omitted from that list (UL3). A masked unit stays masked while its fragment path is
null or empty, so a zero-size file and a `/dev/null` symlink behave alike (UL4). The mask writes a
`/dev/null` symlink, the install mode distinguishes `masked` from `masked-runtime`, and a generator's mask
cannot be unmasked (UL5). `[Install] Alias=` is parsed at enable time, and an alias to a unit that does not
exist is unresolvable and ignored rather than created (UL6). The host shape the reading is grounded on is
committed in `.ufo/waves/round-73/before/host.txt`: 12 search-path directories in their order, two units
masked to `/dev/null` (`passim.service`, `systemd-networkd-wait-online.service`), `user@1000.service`
reading both a template-directory and an `/etc` drop-in, `getty@tty1.service` resolving to
`getty@.service`, and the drop-in directory counts (3 in `/etc`, 12 in `/usr/lib`, 0 in `/run`).

**Core now — the repair table:** `SKILL.md` "Round 73 — the systemd unit-load merge plane (decision
table)" maps six reported symptoms to the mechanism and the rule row behind it, each with the read-only
command that confirms it, and states no resolved value for any unit.

**Still Frontier:** the **effective merged configuration of a specific unit on this host** — no row states
a winning line for any fragment, and `systemctl show`/`systemctl cat` quote the manager's parsed copy at
its last reload, not a fragment-by-fragment resolution, so the surface answers "what the manager read".
**Host-build line numbers** are not claimed: every anchor is a line in the v262 tag, and the Arch build may
carry patches (QUALITY 103). The instance-only drop-in directory leg is documented and absent here (no
`user@1000.service.d` exists), so it is not measured. `SYSTEMD_UNIT_PATH` is unset, so UL1's replacement
leg is documented only. Masking was measured in the `/etc/systemd/system` form only. No `[Install] Alias=`
symlink was read, so UL6 is a code-level statement with no host observation. Whether `.wants` enablement
symlinks survive behind a mask is enablement state, not this plane, and is not read.

**Operator-owned:** mask and unmask (including `--runtime`), enable and disable, edit, `daemon-reload`,
unit start/stop, and any write under a unit directory. The lane reads and reports; no row of this section
authorizes any of those, and a repair never runs them.

**Mori's, unchanged:** nothing about capacity or fleet runway is stated here.

Counted by `python3 tools/count-ul-rows-r73.py --revision <REV>` (frozen; sha256
`542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6`; target `UL_ROWS=6 UL_VERIFIED=6
UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0` and `met=1`) at the round-73 measured revision named in
`SCORECARD.md` "Round 73 — measured outcome".
```

## D. `corpus/README.md` — append (round-73 index)

```corpus/README.md
## Round 73 — systemd unit-load merge plane (C1), the three routed repairs (C2)

Append-only; the round-72 section above stays as written. Map rows appended round 73 (C1) — the systemd
unit-load merge plane the lane never held: the held-ground sweep at the declaration base `eb105757` read
**0** lines for `unit_load_dropin`, `dropin_paths`, `unit_need_daemon_reload`, `null_or_empty`,
`unit_file_mask` and `config_parse_alias` across `corpus/ SKILL.md PROVINCE.md`, `unit load path`,
`unit search path`, `FragmentPath` and `DropInPaths` read **0** files, and every `corpus/knowledge/`
`drop-in` hit is a host observation of a named drop-in file or an mkinitcpio hook context. Notes 90 -> 91,
registry rows 303 -> 306. C2 is registry/tool work, not a coverage row: `check-r72-routed-r73` gains its
row below the registry continuation in `SKILL.md`.

### Coverage rows — round 73

| Note | Holds | Sources |
|---|---|---|
| `knowledge/systemd-unit-load-plane-r73.md` | The systemd unit-load merge plane at v262, six rule rows UL1-UL6: unit files load from a compiled path where an earlier directory's file overrides a same-named file lower in the list, and `SYSTEMD_UNIT_PATH` replaces the whole path (UL1); drop-in `.conf` files merge in one lexicographic pass parsed after the unit file, `/etc` beats `/run` beats `/usr/lib` for a same-named file, and a drop-in beats the unit file wherever located (UL2); a loaded unit needs a daemon reload when its drop-in path list differs from the one read at load time or a drop-in is newer than the last reload, and masked drop-ins are omitted from that list (UL3); a masked unit stays masked while its fragment path is null or empty, so an empty file and a `/dev/null` symlink agree (UL4); the mask writes a `/dev/null` symlink, the install mode distinguishes `masked` from `masked-runtime`, and a generator's mask cannot be unmasked (UL5); `[Install] Alias=` is parsed at enable time and an alias to a missing unit is unresolvable and ignored (UL6). Host shape: 12 search-path directories, `passim.service` and `systemd-networkd-wait-online.service` masked to `/dev/null` with `LoadState=masked`, `user@1000.service` reading a template-directory and an `/etc` drop-in, `getty@tty1.service` resolving to `getty@.service`, and drop-in directory counts 3 in `/etc`, 12 in `/usr/lib`, 0 in `/run` | S304 (man/systemd.unit.xml), S305 (src/core/unit.c), S306 (src/shared/install.c), all systemd v262, committed byte-exact with `SHA256SUMS` and `SOURCES.json` under `.ufo/waves/round-73/before/src/` |
| `SOURCES.md` rows S304-S306 | The three sources, tier A, `mined`; `on-release` recheck; the source cell carries the v262 raw URL and the anchor cell carries the snapshot basename (`systemd.unit.xml`, `unit.c`, `install.c`) plus the snapshot path — the counter's binding condition | raw digests pinned in `.ufo/waves/round-73/before/src/SHA256SUMS` (`eb9479be…`, `47e98d39…`, `c11cd575…`) |
| `../tools/count-ul-rows-r73.py` | The frozen row counter (sha256 `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6`): per row a unique contiguous id, a statement of at least 12 words, at least 6 distinct non-stopword tokens of length at least 4 shared with the row's own snapshot and a shared/total ratio of at least 0.5, a `source=` id present in the registry at the same revision whose source cell carries the map URL and whose anchor cell carries the snapshot basename, a snapshot sha256 equal to both the `digest=` cell and the `SOURCES.json` map digest, and a quote of at most 25 words without a pipe located verbatim (whitespace-normalized) in those bytes; no snapshot cited more than twice, and a `UL`-shaped line that does not parse is a malformed-row finding | `.ufo/waves/round-73/before/src/SOURCES.json`, `SHA256SUMS` |
| `../SKILL.md` | "Round 73 — the systemd unit-load merge plane (decision table)": six symptoms (ignored drop-in, override lost on update, changed-on-disk reload, masked unit, masked-but-enabled display, instance without a file) mapped to mechanism, rule row and read-only check | S304-S306, UL1-UL6, `before/host.txt` |
| `../PROVINCE.md` | "Round-73 entry — R73-UNIT-LOAD-VIEW": the unit-load merge plane moves Frontier -> Core; the effective merged value of a named unit stays Frontier | S304-S306 |

**Frontier:** the effective merged configuration of a specific unit is unread — no row states a winning
line, and the manager's parsed copy at its last reload is not a fragment-by-fragment resolution; anchors
are v262 tag lines and no host-build line number is claimed; the instance-only drop-in directory leg is
documented and absent on this host; `SYSTEMD_UNIT_PATH` is unset, so the replacement leg is documented
only; masking was measured in the `/etc/systemd/system` form only; no `[Install] Alias=` symlink was read;
and whether `.wants` symlinks survive behind a mask is enablement state, not this plane. Mask, unmask,
enable, disable, edit, `daemon-reload` and unit start/stop remain operator-owned.
```

## E. Binding conditions the C1 commit must satisfy (not prose — checklist)

1. `corpus/SOURCES.md` carries **S304, S305, S306** with: source cell containing the exact v262 raw URL
   (`…/v262/man/systemd.unit.xml`, `…/v262/src/core/unit.c`, `…/v262/src/shared/install.c`); anchor cell
   containing the snapshot **basename** (`systemd.unit.xml`, `unit.c`, `install.c`); kind in
   {`spec`,`docs`,`paper`,`code`,`tool`,`dataset`,`talk`,`book`,`community`} and never `own-work`.
   Verified: the counter parses cell 2 as source, cell 3 as kind, cell 6 as anchor of a `| S### |` row.
2. Every UL row line has exactly **seven** pipes (`| ULn | stmt | source=S### | snapshot=… | digest=… |
   quote="…" |`) and the six ids are contiguous 1..6; a seventh `UL`-shaped line is `malformed-row`.
3. Each `digest=` equals the snapshot's sha256 **and** the `SOURCES.json` map sha256; each quote is at
   most 25 words, pipe-free, and present verbatim whitespace-normalized in the snapshot; no snapshot is
   cited more than twice (2+2+2 is the shape the draft uses).
4. Registry row count 303 -> 306 and knowledge-note count 90 -> 91, per the frozen declaration.

**Observed on the wave-1 note draft (fixture, not the lane):** with the three registry rows shaped as in
item 1 and the draft note copied into a private `$TMPDIR` tree,
`TMPDIR=<scratch> python3 tools/count-ul-rows-r73.py --fixture <tree>` printed
`UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `UL_TARGET … met=1`, rc 0. That is a
statement about the counter's mechanics over that tree, not a lane measurement and not the after receipt. After the counter moved, the hardened
`84501ab8…` scored the **lane working tree** the same way (`--fixture <lane root>`): six `UL_ROW ok` lines,
the same five counters, `met=1`, rc 0 — still a working-tree read, not a committed measurement.

## F. Findings from this seat (commands and outputs; nothing here was fixed)

### F1. Both instruments moved inside wave 1; one C2 checker state failed its own control

```
$ sha256sum tools/check-r72-routed-r73.py            # first read, ~23:0x
93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e  tools/check-r72-routed-r73.py   (202 lines)
$ TMPDIR=<scratch> python3 tools/check-r72-routed-r73.py --selftest
... PASS (SELFTEST-{CONTROL,LESSON,DIGEST,CAPABILITY,UNANCHORED}) ...
SELFTEST: PASS (5 cases, 5 passed, 0 failed)          rc=0

$ sha256sum tools/check-r72-routed-r73.py            # 23:11:12
316dd51aacc29e1590fbea27657e81956a30198f377d14c52d41ae2369419441  tools/check-r72-routed-r73.py   (267 lines)
$ TMPDIR=<scratch> python3 tools/check-r72-routed-r73.py --selftest
FAIL (SELFTEST-CONTROL) rc=1 expect=0 token=ROUTED_STALE=0
PASS (SELFTEST-LESSON) ... PASS (SELFTEST-VACUOUS)
SELFTEST: FAIL (11 cases, 10 passed, 1 failed)        rc=3

$ sha256sum tools/check-r72-routed-r73.py            # 23:12:19, current
328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe  tools/check-r72-routed-r73.py   (279 lines)
$ TMPDIR=<scratch> python3 tools/check-r72-routed-r73.py --selftest
... eleven PASS lines ...
SELFTEST: PASS (11 cases, 11 passed, 0 failed)        rc=0
$ git status --porcelain tools/check-r72-routed-r73.py
 M tools/check-r72-routed-r73.py
```

A byte copy of the then-current file, patched only to print the failing case's buffer, passed 11/11, so the
recorded CONTROL failure is a **transient observed output**, not a reproduced suite defect; what is proved
is that the instrument was being rewritten under the wave while seats read it, and that the declaration
digest `93f034e3…` no longer describes the file. Consequence handled in draft B: the row pins the
construction and requires the digest to be re-read from the committed blob at the measured revision, and
the round's frozen instrument-change rule (declaration §(b)) requires the appended erratum with old→new
digests and a same-instrument before-control re-run.

The C1 counter moved as well, later in the same wave: `542f9c29…` (409 lines, eleven cases) ->
`84501ab8d4968293de8b38f68a9f53d658535d90df8191cbd96a20df98e94832` (423 lines, twelve cases, the new
`EMPTYQUOTE` mutant asserting `quote-words`), ` M` uncommitted:

```
$ TMPDIR=<scratch> python3 tools/count-ul-rows-r73.py --selftest
... twelve PASS lines, incl. PASS (SELFTEST-EMPTYQUOTE) rc=1 expect=1 token=quote-words ...
SELFTEST: PASS (12 cases, 12 passed, 0 failed)        rc=0
$ TMPDIR=<scratch> python3 tools/count-ul-rows-r73.py --fixture <lane root>
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
... UL2 ... UL6 ...
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1   rc=0
```

The second run read the **lane working tree** (note + the three landed S304-S306 rows + the snapshots): a
working-tree observation, not the after receipt, and no proof that the same bytes are committed.

### F2. `check-r72-routed-r73`'s documented exit 2 is unreachable outside `--selftest`

The header says "2 cannot evaluate (a required file is absent, or no readable input)"; `evaluate()`
returns `0` or `1` only, and an unreadable input is a finding with rc 1:

```
$ TMPDIR=<scratch> python3 tools/check-r72-routed-r73.py --root <dir with only corpus/lessons/round-72.md>
LESSON-STALE path=corpus/lessons/round-72.md reason=receipt-absent path=.ufo/waves/round-72/after/selftest-selftest-after.txt
ROUTED_ITEM LESSON stale
DIGEST-STALE absent path=SCORECARD.md
ROUTED_ITEM DIGEST stale
CAPABILITY-STALE absent path=SCORECARD.md
ROUTED_ITEM CAPABILITY stale
ROUTED_STALE=3 ROUTED_OK=0/3                          rc=1
```

True for the declaration instrument (202 lines) and for the current one (279 lines). Draft B states the
observed map; the docstring is not edited (frozen).

### F3. The wave-1 note draft's H3 host value is wrong about `UnitFileState`

The draft at `.ufo/waves/round-73/w1/L1Entry/note.md` H3 reads "`systemd-networkd-wait-online.service`
reads `UnitFileState=enabled` beside the mask". Re-measured read-only:

```
$ systemctl show -p UnitFileState -p LoadState -p FragmentPath systemd-networkd-wait-online.service
LoadState=masked
FragmentPath=/etc/systemd/system/systemd-networkd-wait-online.service
UnitFileState=masked
$ systemctl is-enabled systemd-networkd-wait-online.service ; echo rc=$?
masked
rc=1
$ systemctl list-unit-files --state=masked | head -3
UNIT FILE                            STATE  PRESET
passim.service                       masked disabled
systemd-networkd-wait-online.service masked enabled
```

The `enabled` token is the **PRESET** column, not an enablement that survived the mask; `UnitFileState`
and `LoadState` both read `masked`. Draft A's T5 states the corrected mechanism, and the note's H3 must be
corrected before the C1 commit. Committed `before/host.txt` is consistent with this (it records the
`list-unit-files` row verbatim and `LoadState=masked`, `UnitFileState=masked` for `passim.service`).
Held on the same draft: H1's order claim (12 directories, `/etc/systemd/system` before
`/run/systemd/system` before `/usr/local/lib/systemd/system` before `/usr/lib/systemd/system`) reproduces
from `systemd-analyze unit-paths`, and H4/H5 reproduce exactly as quoted (verified this seat).

### F4. `count-ul-rows-r73`'s header omits its 128 code

Its exit map lists 0/1/2/3 but not the `128` it returns for `UL_NOTE`, `UL_REGISTRY` or `UL_MAP` absent —
the code the declaration's do-nothing control relies on (`UL_NOTE absent` rc 128, reproduced this seat).
Documentation gap only; draft B states 128.
