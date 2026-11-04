source: S309, S310 and S311 in `corpus/SOURCES.md` (systemd v262 `src/shared/unit-file.c`, `src/core/load-fragment.c`, `src/shared/unit-file.h`; snapshots under `.ufo/waves/round-74/before/src/` with digests in `before/src/SOURCES.json`), plus read-only host receipts `before/host.txt`, `w1/S1Scout/receipts/host_recapture.txt` and `w1/E3HostProbe/receipt-a-live.txt` under `.ufo/waves/round-74/` (2026-11-04; systemd 262.1-1-arch)
verified-at: 2026-11-04 (snapshot sha256 compared with `before/src/SOURCES.json` and `before/src/SHA256SUMS`; host readings re-measured read-only the same day and agreeing with the capture)
recheck: `python3 tools/count-uf-rows-r74.py --revision <REV>` for the six row predicates; re-run `systemd-analyze unit-paths`, `systemctl list-unit-files --state=masked`, and `systemctl list-units --type=service` readings read-only; re-open the three files at the next systemd tag; cadence on-release

The unit-fragment resolution plane is the set of rules, data structures, and priority algorithms systemd uses to locate, validate, and load unit definitions from disk fragments or built-in fallbacks into the manager's runtime state. This covers the multi-directory lookup search path processed in strict priority order where earlier directories override later ones with first-seen name registration; validation and filtering of alias symlinks rejecting self-aliases and incompatible unit types; restriction of symlink aliasing via `unit_type_may_alias` to services, sockets, targets, devices, timers, and paths; the `UnitFileState` enumeration distinguishing persistent enablement/mask states from runtime counterparts; the `null_or_empty` fragment check marking loaded units as `UNIT_MASKED` while perpetual units remain immune; and the fallback mechanism for missing system-scope units to embedded `builtin_unit_lookup` copies while on-disk files and masks unconditionally override built-ins. Repair operations depend on this plane because unit activation, masking, and alias resolution depend strictly on which fragment wins the resolution hierarchy. Upstream line anchors are pinned to tag v262 snapshots and may differ from the host's installed `262.1-1-arch` package line numbers (QUALITY 103).

# systemd unit-fragment resolution plane: search path, alias validation, UnitFileState, mask check and built-in fallback (round 74)

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| UF1 | Unit search paths are walked in priority order and a name already registered is skipped, so the first-seen copy wins | source=S309 | snapshot=unit-file.c | digest=141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | quote="Search paths are ordered by priority (highest first), and we need to maintain this order." |
| UF2 | unit_validate_alias_symlink_or_warn returns ELOOP for a unit self-alias and EXDEV when the symlink target name type does not match source | source=S309 | snapshot=unit-file.c | digest=141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd | quote="-EXDEV if the target filename is not a valid unit name or doesn't match the source," |
| UF3 | unit_type_may_alias admits only UNIT_SERVICE UNIT_SOCKET UNIT_TARGET UNIT_DEVICE UNIT_TIMER UNIT_PATH so volume units can never carry aliases | source=S311 | snapshot=unit-file.h | digest=e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | quote="static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);" |
| UF4 | UnitFileState separates UNIT_FILE_ENABLED from UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED from UNIT_FILE_LINKED_RUNTIME, and UNIT_FILE_MASKED from UNIT_FILE_MASKED_RUNTIME | source=S311 | snapshot=unit-file.h | digest=e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f | quote="UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME," |
| UF5 | a null_or_empty fragment sets load_state to UNIT_MASKED and zero fragment_mtime except that perpetual units load as UNIT_LOADED instead | source=S310 | snapshot=load-fragment.c | digest=a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | quote="u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;" |
| UF6 | missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins | source=S310 | snapshot=load-fragment.c | digest=a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5 | quote="const char *data = builtin_unit_lookup(u->id);" |

## Reading the rows

UF1 and UF2 capture the unit-file search path and alias resolution algorithm (S309, `unit-file.c`):
`unit_file_build_name_map` at `unit-file.c:364-568` walks search paths in priority order (highest first),
populates `expanded_search_path` chasing directory symlinks (lines 407-443), and iterates through directory
entries, checking at line 536 `hashmap_contains(ids, de->d_name)` so that any unit name already seen is
ignored and the highest-priority file or symlink wins the name mapping. At lines 59-141,
`unit_validate_alias_symlink_or_warn` validates alias symlinks: checking that the source unit type permits
aliasing via `unit_type_may_alias`, rejecting self-aliases at lines 108-111 with `-ELOOP`, and verifying
that the target unit name type and instance match the source, returning `-EXDEV` on type or instance mismatch.

UF3 and UF4 capture unit-file type restrictions and state representations (S311, `unit-file.h`):
`unit_type_may_alias` at `unit-file.h:25-33` defines an inline predicate checking with `IN_SET` that only
services, sockets, targets, devices, timers, and paths may be referenced by alias symlinks, preventing
unsupported unit types from establishing alias names (and confirming volume units can never carry aliases).
At lines 7-23, `typedef enum UnitFileState` enumerates all possible unit file installation states,
explicitly distinguishing persistent states (`UNIT_FILE_ENABLED`, `UNIT_FILE_LINKED`, `UNIT_FILE_MASKED`)
from their volatile counterparts (`UNIT_FILE_ENABLED_RUNTIME`, `UNIT_FILE_LINKED_RUNTIME`,
`UNIT_FILE_MASKED_RUNTIME`), allowing tooling to differentiate permanent configuration in `/etc` from
volatile overrides in `/run`.

UF5 and UF6 capture fragment loading, mask evaluation, and fallback mechanisms (S310, `load-fragment.c`):
`unit_load_fragment` at `load-fragment.c:6228-6315` inspects the located fragment file. At line 6247, if
`null_or_empty(&st)` holds (an empty file or `/dev/null` symlink), line 6250 sets `u->load_state` to
`UNIT_MASKED` and zeroes `fragment_mtime`, unless `u->perpetual` is true: perpetual units (`-.slice`,
`system.slice`, special root targets) are immune from masking and remain `UNIT_LOADED`. If no fragment is
found on disk and the manager runs in `RUNTIME_SCOPE_SYSTEM`, lines 6285-6315 invoke `builtin_unit_lookup`
for embedded unit definitions (e.g., emergency.service, rescue.service), while on-disk unit files and masks
unconditionally override built-ins because built-in lookup is reached only when lookup paths yield no fragment.

## Host readings

All commands below are read-only. The observations were re-measured by the round's seats on
2026-11-04; no exact timestamp is inferred from the undated before/host.txt body.

| reading | command | observed |
|---|---|---|
| build under test | `/usr/lib/systemd/systemd --version` | `systemd 262 (262.1-1-arch)`; `uname -r` reports `7.2.11-arch1-1` |
| system unit search path | `systemd-analyze unit-paths` | 12 lines, first `/etc/systemd/system.control`, then `/run/systemd/system.control`, `/run/systemd/transient`, `/run/systemd/generator.early`, `/etc/systemd/system`, `/etc/systemd/system.attached`, `/run/systemd/system`, `/run/systemd/system.attached`, `/run/systemd/generator`, `/usr/local/lib/systemd/system`, `/usr/lib/systemd/system`, last `/run/systemd/generator.late` |
| user unit search path | `systemd-analyze --user unit-paths` | 18 lines from `/home/vgpnk/.config/systemd/user.control` down to `/run/user/1000/systemd/generator.late` |
| masked set | `systemctl list-unit-files --state=masked --no-legend` | 2 rows: `passim.service masked disabled` and `systemd-networkd-wait-online.service masked enabled`; `--state=masked-runtime` returns 0 rows |
| mask targets | `ls -l /etc/systemd/system/passim.service /etc/systemd/system/systemd-networkd-wait-online.service` | both are symlinks to `/dev/null` (`lrwxrwxrwx ... -> /dev/null`) |
| active alias symlink | `systemctl show -p Id -p Names -p FragmentPath systemd-sysupdate.timer` | `Id=systemd-sysupdate-update.timer`, `Names=systemd-sysupdate-update.timer systemd-sysupdate.timer`, `FragmentPath=/usr/lib/systemd/system/systemd-sysupdate-update.timer` |
| alias symlink on disk | `ls -l /usr/lib/systemd/system/systemd-sysupdate.timer` | `lrwxrwxrwx 1 root root 30 Oct 17 05:46 /usr/lib/systemd/system/systemd-sysupdate.timer -> systemd-sysupdate-update.timer` |
| active instance units | `systemctl list-units --type=service --no-legend \| grep '@'` | 4 rows: `dirmngr@etc-pacman.d-gnupg.service`, `systemd-fsck@dev-disk-by\x2duuid-86D8\x2dC3F6.service`, `user-runtime-dir@1000.service`, `user@1000.service` |

These host readings expose search-path order, two masks, and a valid timer alias. They do not deliberately exercise duplicate-name precedence, self-alias rejection, or builtin fallback. The latter remain code contracts, not live mutation tests. The alias observation supersedes the round-73 no-alias-read limit only for this timer.

## Limits

- No alias symlink error rejection (such as self-alias ELOOP or mismatched unit type EXDEV) was observed on the live host because the host configuration contains only valid alias symlinks; self-alias and type validation are code-level contracts from `unit_validate_alias_symlink_or_warn` in `unit-file.c`.
- Perpetual unit immunity (`u->perpetual ? UNIT_LOADED : UNIT_MASKED`) was not observed under an intentional mask file; testing perpetual mask immunity would require attempting to mask `-.slice` or `init.scope`, which is prohibited on a read-only host.
- Built-in fragment fallback (`builtin_unit_lookup`) was not directly triggered because core system units on Arch Linux have on-disk fragments installed under `/usr/lib/systemd/system/`.
- Upstream line anchors are from the v262 snapshots; host package `262.1-1-arch` may contain minor packaging adjustments and line number offsets (QUALITY 103).
