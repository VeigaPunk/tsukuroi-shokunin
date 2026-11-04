## Round 72 — modprobe configuration plane (C1), the gate's own cases (C2), routed repairs (C3)

Append-only; the round-71 section above stays as written. Map rows appended round 72 (C1) — the kmod
configuration surface the lane never held: the held-ground sweep at the declaration base `a7015d27` read
**0** file hits for `softdep`, `MODPROBE_OPTIONS`, `showconfig`, `APPLY_BLACKLIST`,
`conf_files_insert_sorted` and `lexicographic` across `corpus/knowledge`, and no note named the surface.
The C2 and C3 moves are registry/tool work, not coverage rows: `tools/check-selftest-tally.py` gains its
own `--selftest` mode (its registry row is drafted separately for `SKILL.md`), and the round-71 routed
defects close in committed bytes.

### Coverage rows — round 72

| Note | Holds | Sources |
|---|---|---|
| `knowledge/modprobe-config-plane-r72.md` | The kmod configuration surface at v34, six rule rows MD1-MD6: the SYNOPSIS directory order, with the first file of a given name suppressing the same name in later directories (MD1); one lexicographic pass across all directories, with complete replacement by a higher-priority same-name file and partial replacement by a later-ordered file (MD2); libkmod's single sorted filename list, which rejects a second file of the same name at insertion (MD3); `/proc/cmdline` parsed into the same configuration object after the files (MD4); `-n/--dry-run` executing nothing (MD5); `blacklist` as alias-only unless `--use-blacklist` adds the unconditional flag (MD6). Host shape: `/etc/modprobe.d` 3 names, `/usr/lib/modprobe.d` 5 names (`README` plus four `.conf`), `/run/modprobe.d` and `/usr/local/lib/modprobe.d` absent, `/lib` resolving to `/usr/lib` so two SYNOPSIS entries are one directory | S301 `man/modprobe.d.5.scd`, S302 `libkmod/libkmod-config.c`, S303 `tools/modprobe.c` (kmod v34; host kmod 34.2) |
| `../tools/count-md-rows-r72.py` | The frozen row counter (sha256 `d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6`): per row a unique contiguous id, a statement of at least 12 words, at least 6 distinct non-stopword tokens (length at least 4) shared with the row's own snapshot text and a shared/total ratio of at least 0.5, a `source=` id present in the registry at the same revision whose `source` cell carries the map URL and whose `anchor` cell carries the snapshot basename, a snapshot sha256 equal to both the `digest=` cell and the `SOURCES.json` map digest, and a quote of at most 25 words without a pipe located verbatim (whitespace-normalized) in those bytes; no snapshot cited more than twice, and an `MD`-shaped line that does not parse is a malformed-row finding. Target `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1` | `../SOURCES.md` S301-S303; snapshots `.ufo/waves/round-72/before/src/` with `SHA256SUMS` and `SOURCES.json` |

**Frontier:** the effective configuration of a named module remains unread — fragment contents are out of
bounds for this lane, so the precedence and merge are stated as kmod's documented order (MD1-MD4) and not
as a resolution of this host's fragments; `install`/`softdep`/`weakdep` command semantics,
`MODPROBE_OPTIONS` alteration of the directory list, and any blacklist refusal are documented shapes, not
host observations. The modprobe side of the r71 parameter routes (MP6) is named there as a documented
alternative; this entry does not measure it line by line either.
