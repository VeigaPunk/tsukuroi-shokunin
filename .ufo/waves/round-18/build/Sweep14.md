# C3 recon — corpus/knowledge/degraded-triage-r4.md

[obs] Baseline-identical (842a5312), no R17/R18 notice. Dated narratives stay history. [inf] 1–4 are live operator guidance; 5 is live host context.

1. 'sudo snapper -c root create-config /' (:86); '`snapper list-configs` header-only, rc=0;' (:317); '`/etc/snapper/configs/` empty' (:318); 'Any wave on this host is snapshot-less.' (:339). Now configs `home`,`root` exist; `SNAPPER_CONFIGS="root home"`; `SNAPPER_CONFIG_NAME="root"` set. S060 :76-80; S052 :74.
2. '`paccache`/`checkupdates` absent' (:183); '`pacman-contrib` not installed' (:184); 'Action: optional prune/`pacman-contrib`' (:186); 'cache grows only via `-Sc` (no paccache/checkupdates)' (:65). Now `pacman-contrib-1.13.1-1`; `/usr/bin/paccache`. S060 :36,:83.
3. '`sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`' (:102,:235). Row gone; stale row 'nvidia/615.78.08, 7.2.3-arch1-3' with '(Built modules are missing in the kernel modules folder)'. S060 :95.
4. 'bsdtar -tf /var/lib/pacman/sync/offline.db …' (:597). Five DBs listed; `offline.db` absent, recheck fails. S060 :48-54.
5. [inf] '`zswap.enabled=0` on the cmdline' (:217). Now `zswap.enabled=1 zswap.max_pool_percent=25`, runtime `Y`/`25`/`zstd`. S060 :9,:12-14.

## Proposed notice block
```markdown
## R18-FRESHNESS — degraded-triage-r4 current-use supersessions (S060)
Historical snapshots above are preserved. This notice supersedes current-use only; read-only scope, no package or reboot clearance.
- Snapper: root/home configs exist (`SNAPPER_CONFIGS="root home"`; `SNAPPER_CONFIG_NAME="root"`); `list-configs` is not header-only and `/etc/snapper/configs/` is not empty (S060 :76-80; S052 :74). Do not re-run `create-config`; snapshot capture unmeasured.
- P5: `pacman-contrib-1.13.1-1` and `/usr/bin/paccache` exist; "not installed / only `-Sc`" and the install action are superseded (S060 :36,:83).
- D2: 610.57.04 / 7.1.4 is gone; remaining stale row is `nvidia/615.78.08, 7.2.3-arch1-3` with missing built modules (S060 :95).
- Appendix A: `offline.db` is absent, so its `bsdtar` recheck cannot run (S060 :48-54).
- D1(b): zswap is `enabled=1`, `max_pool_percent=25`, `zstd` (S060 :9,:12-14).
```
No fresh evidence for mirror, sr0, J2, U8; unassessed. U6 still holds (R17 supplement :144), not stale.

Scope: executed=none
