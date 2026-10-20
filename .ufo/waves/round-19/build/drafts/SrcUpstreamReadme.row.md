# Candidate SOURCES row — limine-snapper-sync README at tag 1.32.1

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | limine-snapper-sync README at tag 1.32.1 — https://gitlab.com/Zesko/limine-snapper-sync/-/raw/1.32.1/README.md | docs | A | Upstream 1.32.1 README's documented Snapper plugin event triggers for sync; not host configuration or cleanup-unit wiring | § Features > Core sync system, line 826 "Snapper plugin integration for snapshot create, modify, delete, and rollback events"; tag 1.32.1 commit b4c0da2d4532a993809219f9e5d51a1fa85fcb93 dated 2026-10-03; opened 2026-10-20 | The 1.32.1 README states its Snapper plugin integration handles snapshot create, modify, delete and rollback events; it does not name snapper-cleanup.service or ExecStopPost | queued | 2026-10-20 | on-release | — |

## Gate evidence for the round-19 lesson `## Gate`

- URL opened: https://gitlab.com/Zesko/limine-snapper-sync/-/raw/1.32.1/README.md (access date 2026-10-20; full README served, not a Cloudflare challenge)
- Revision/tag: tag `1.32.1` = commit `b4c0da2d4532a993809219f9e5d51a1fa85fcb93`, dated 2026-10-03 (https://gitlab.com/Zesko/limine-snapper-sync/-/tags/1.32.1; API https://gitlab.com/api/v4/projects/Zesko%2Flimine-snapper-sync/repository/tags/1.32.1)
- Section heading: `### Core sync system` (tag README line 824, under `## Features` line 822)
- Exact quote (line 826, 11 words): "Snapper plugin integration for snapshot create, modify, delete, and rollback events"
- Pinned reproduction: https://gitlab.com/api/v4/projects/Zesko%2Flimine-snapper-sync/repository/files/README.md/raw?ref=b4c0da2d4532a993809219f9e5d51a1fa85fcb93 lines 824-826 carry the same heading and quote.

## Notes

- Candidate id S066 per round-19 frontier; kept as `S0NN` for L1 numbering.
- The master-branch URL registered as S019 was not reused.
- Related but not selected: line 865 "Two ways to monitor snapshot changes: `limine-snapper-watcher` or Snapper plugin integration"; line 929 "Snapper CLI-free: triggered by Snapper events and reads snapshot metadata directly without interfering with Snapper services" (under Planned features).
- The README does not name `snapper-cleanup.service` or `ExecStopPost`; cleanup-time attribution rests on the host capture `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:256-260`.
