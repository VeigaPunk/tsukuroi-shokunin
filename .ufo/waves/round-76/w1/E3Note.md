# E3Note — scoped findings

Behavior: completed `corpus/knowledge/journald-retention-plane-r76.md`, exactly eight sourced JD rows plus provenance, mechanism anchors, host derivation and limits.

Gate: final assigned `TMPDIR=/fast/scratch/hyaku/tsukuroi-r76/E3Note python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jd-rows-r76.py` (cwd lane root) returned rc 0:
`JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1`.
Four snapshot SHA-256 checks returned OK. Header checker has no note-path argument; conditional execution not applicable, no pass claimed.

Findings: corrected JD3 from draft “used space plus the smaller of free space and keep_free” to pinned `avail = LESS_BY(vfs_avail, metrics->keep_free);` followed by CLAMP. This conflicts with frozen draft/declaration wording and is preserved for canonical judgment. Corrected JD7 attribution: rate pair assigned in journal_config_set_defaults, sync/max-file defaults supplied in manager_merge_configs. JD4 now states MAX floor precisely; JD2 explicitly covers the smaller allowed constraint. No registry/instrument edits.

Limits: working-tree evidence, not committed-byte or independent semantic approval; host values derived from frozen receipt, not live daemon introspection. No vacuum/rotation/restart/flush or new host probe. No tools installed. Scratch removed successfully.

Artifacts (relative to lane root):
- `.ufo/waves/round-76/w1/E3Note/binding.md`
- `.ufo/waves/round-76/w1/E3Note/counter.txt`
- `.ufo/waves/round-76/w1/E3Note/report.md` — exact commands, outcomes, reviewed ranges, per-row changes, provenance and self-evaluation.
