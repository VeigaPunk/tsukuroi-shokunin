# Sweep07 — update-safety-v3.md C3 recon

Read-only. Baseline `842a5312`; file `corpus/knowledge/update-safety-v3.md` sha256 `50e387e3…` = tree. R18 = `.ufo/waves/round-18/l1-capture/host-capture-r18.txt`, committed `51dd9ee` (S060); its times are 2026-10-20 16:06:17 -03. 2026-10-14 bytes stay true at their date. R17's `FxFreshUpdaSafeV3` died; one R17 notice exists.

| # | md:line | stale quote | now / capture |
|---|---|---|---|
| 1 | 235 | "`checkupdates`/`pacman-contrib` absent (installing is out of province, SKILL.md:415)." | pacman-contrib 1.13.1-1 installed; paccache present; checkupdates binary unprobed. R18:36 `pacman-contrib-1.13.1-1`; S051 B:55 |
| 2 | 220 | "the preservation set is `offline.db` (md5 `c4b27c38…`, 304 318 B)" | offline.db absent from sync listing (core/extra/multilib/omarchy/openai-chatgpt); elsewhere [unk]; :344 md5sum unrunnable. R18:48 `$ ls -1 /var/lib/pacman/sync/` |
| 3 | 242/218 | "0 `.db.sig`; `SigLevel = PackageRequired" | one signature: openai-chatgpt.db.sig; omarchy.db unsigned. R18:54 `openai-chatgpt.db.sig` |
| 4 | 239 | "beside the current `7.2.3-arch1-3`" | 7.2.11 and 6.18.57-2 installed; 7.2.3 has modules missing = stale. R18:95 `7.2.3-arch1-3, x86_64: installed (Original modules exist)`; :6 `7.2.11-arch1-1` |
| 5 | 112 | "\| 4 \| `elephant-bluetooth` 2.21.0-1 \|" | 09:31:03 -U names all 13 at 2.22.1-1; core in DB; rows 4-15 still 2.21.0-1; per-plugin [inf]. R18:72 `elephant-bluetooth-2.22.1-1-x86_64.pkg.tar.zst`; :30 `elephant-2.22.1-1`; S051 B:64 |

Heading: `## R18-FRESHNESS — update-safety v3 stale current-use statements (2026-10-20)`. Append-only; historical bytes preserved; supersedes current use only; read-only scope, no package/reboot clearance. Sources S060/S051/S052. Each row = one bullet with exact now/capture_ref; capture_quote = backticked text.

No evidence (no notice): row 3 "26 installed"/shadow; row 5 cache/clone counts; row 6 repo set (sync-dir ≠ configured repo, R15 `.ufo/waves/round-15/build/DecisionForeignPackage.md:26`); foreign=16; U6 `/boot`; U7; U5; U1 summary (R17 already notices subclaims); §4/§7 dated ".db.sig 0"/"dkms two rows"; §8 pins.

Scope: executed=none (read-only git show/rev-parse/status/log; read/grep; no host probes).
