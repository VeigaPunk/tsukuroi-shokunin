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
