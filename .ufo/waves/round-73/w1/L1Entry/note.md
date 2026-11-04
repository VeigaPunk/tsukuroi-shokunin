# The systemd unit-load merge plane (round 73, C1)

**What this plane is.** How systemd decides which bytes are a unit: the compiled load path and its
override rule, the drop-in directories merged on top of a unit file, the two forms of masking, the
condition under which the running manager's copy is stale, and the moment an `[Install] Alias=` becomes a
symlink. It is the plane a repair reads before it edits anything: "my drop-in is ignored", "the unit is
masked", "it says changed on disk" and "the instance has no file" are all decided here, by rules rather
than by a service's own state.

**Pins.** Upstream systemd **v262** (`man/systemd.unit.xml`, `src/core/unit.c`,
`src/shared/install.c`), committed byte-exact under `.ufo/waves/round-73/before/src/` with `SHA256SUMS`
and `SOURCES.json`; the host runs **262.1-1-arch** (`systemctl --version`). Every upstream line anchor
below is a line in the pinned tag, **not** a verified line in the host's Arch build, which may carry
patches (QUALITY 103).

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| UL1 | Unit files are loaded from a compiled load path, so a unit found in a directory listed earlier overrides the same name lower in the list, and the SYSTEMD_UNIT_PATH variable replaces the whole path | source=S304 | snapshot=systemd.unit.xml | digest=eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | quote="Unit files found in directories listed earlier override files with the same name in directories lower in the list" |
| UL2 | Multiple drop-in files with different names are applied in lexicographic order regardless of the directory they reside in, drop-in files in etc take precedence over run and usr/lib, and drop-ins beat unit files wherever located | source=S304 | snapshot=systemd.unit.xml | digest=eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | quote="Multiple drop-in files with different names are applied in lexicographic order, regardless of which of the directories they reside in" |
| UL3 | A loaded unit needs a daemon reload when its drop-in path list differs from the list read at load time or a drop-in file is newer than the last reload, and masked drop-ins are omitted from that list | source=S305 | snapshot=unit.c | digest=47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 | quote="any drop-ins that are masked are simply omitted from the list" |
| UL4 | A masked unit stays masked while its fragment path is null or empty, so a zero-size file and a dev/null symlink both keep the masked state until the path changes | source=S305 | snapshot=unit.c | digest=47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 | quote="For masked files check if they are still so" |
| UL5 | The mask operation writes a dev/null symlink at the unit name, the install mode distinguishes masked from masked-runtime, and a mask created by a generator cannot be unmasked | source=S306 | snapshot=install.c | digest=c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d | quote="Unit %s is masked, ignoring." |
| UL6 | An Install alias is parsed when the unit is enabled, and an alias that points at a unit which does not exist is unresolvable and is ignored rather than created | source=S306 | snapshot=install.c | digest=c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d | quote="Unit %s is an alias to a non-existent unit, ignoring." |

## Host readings

| # | reading | command | observed |
|---|---|---|---|
| H1 | the load path the host actually uses | `systemd-analyze unit-paths` | 12 directories, `/etc/systemd/system` before `/run/systemd/system` before `/usr/local/lib/systemd/system` before `/usr/lib/systemd/system` (`.ufo/waves/round-73/before/host.txt`) |
| H2 | masked units and their target | `systemctl list-unit-files --state=masked --no-legend` | `passim.service`, `systemd-networkd-wait-online.service`; both are `/dev/null` symlinks in `/etc/systemd/system` (`readlink -f`) |
| H3 | a masked unit's load state | `systemctl show -p LoadState -p FragmentPath -p UnitFileState passim.service` | `LoadState=masked`, `FragmentPath=/etc/systemd/system/passim.service`, `UnitFileState=masked`; `systemd-networkd-wait-online.service` reads `UnitFileState=enabled` beside the mask |
| H4 | instance and template drop-ins together | `systemctl show -p DropInPaths -p FragmentPath user@1000.service` | `/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf /etc/systemd/system/user@.service.d/faster-shutdown.conf` under `FragmentPath=/usr/lib/systemd/system/user@.service` |
| H5 | template fallback | `systemctl show -p FragmentPath getty@tty1.service` | `LoadState=loaded`, `FragmentPath=/usr/lib/systemd/system/getty@.service` |
| H6 | drop-in directory counts | `find <dir> -maxdepth 1 -type d -name '*.d' \| wc -l` | `/etc/systemd/system` 3, `/usr/lib/systemd/system` 12, `/run/systemd/system` 0 |

## Limits

- **Documented order, not a resolved value.** The rows state systemd's documented merge and precedence;
  the effective merged configuration of any one unit on this host is not read here, and no row claims a
  winning line for a specific file. `systemctl show` output is the manager's *parsed* unit, which is what
  H3-H5 quote — not a fragment-by-fragment resolution.
- **No instance-only drop-in on this host.** H4 shows a template drop-in and a prefix-truncated
  (`user@.service.d/`) drop-in; no `user@1000.service.d/` directory exists, so the instance-specific leg is
  documented, not measured.
- **`SYSTEMD_UNIT_PATH`** is unset on this host, so UL1's override leg is documented only.
- **Alias leg.** No `[Install] Alias=` symlink was read this round; UL6 is a code-level statement
  (`INSTALL_CHANGE_IS_DANGLING`), with no host observation attached.
- **Masking completeness.** A mask can be placed in any higher-priority directory; this round measured the
  `/etc/systemd/system` form only. The still-masked test in UL4 is `null_or_empty`, which is why the
  zero-size form and the `/dev/null` form behave alike.
- **No action is authorized by this entry.** Mask, unmask, enable, disable, edit, `daemon-reload`, unit
  start/stop and any write under a unit directory remain operator-owned; the lane reads and reports.
