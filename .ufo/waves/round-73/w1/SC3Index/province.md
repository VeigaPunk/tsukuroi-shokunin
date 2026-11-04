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
