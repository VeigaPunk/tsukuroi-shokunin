# SrcUpstreamReadme — limine-snapper-sync README at tag 1.32.1

- [obs] Opened https://gitlab.com/Zesko/limine-snapper-sync/-/raw/1.32.1/README.md on 2026-10-20; it returned the full README, not a Cloudflare challenge. https://gitlab.com/Zesko/limine-snapper-sync/-/tags/1.32.1 shows tag 1.32.1 → commit b4c0da2d4532a993809219f9e5d51a1fa85fcb93, dated 2026-10-03; the tags API agrees.
- [obs] Installed package is limine-snapper-sync 1.32.1-2: `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:11` (package directory) and `:135` (%VERSION%).
- [obs] Section `### Core sync system` (tag README line 824); exact quote at line 826: "Snapper plugin integration for snapshot create, modify, delete, and rollback events" (11 words). The commit-pinned API raw (`.../files/README.md/raw?ref=b4c0da2d...`) serves the same heading and quote.
- [obs] Rejected alternatives: line 865 ("Two ways to monitor snapshot changes...") does not cover delete events; line 929 ("Snapper CLI-free: triggered by Snapper events...") sits under Planned features, not current behavior. The master-branch URL registered as S019 was not reused.
- [inf] C2 use: the README documents snapshot deletion as a plugin-triggered sync input, but it never names `snapper-cleanup.service` or `ExecStopPost`; cleanup-time attribution stays grounded in the host drop-in capture (`.ufo/waves/round-19/l1-capture/host-capture-r19.txt:256-260`), not this README.
- [unk] Whether the host's `/usr/share/doc/limine-snapper-sync/README.md` matches tag bytes was not checked (host read outside item scope).
- Draft row: `.ufo/waves/round-19/build/drafts/SrcUpstreamReadme.row.md` (id S0NN; candidate S066). Model: harness reports `commandcode/deepseek/deepseek-v4.1-flash`.

Scope: executed=none
