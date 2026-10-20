# FreshPackagePlaneSweep — stale current-use package-state claims (R17, 2026-10-20)

PSP/ARP = `corpus/knowledge/{package-state,aur-risk}-plane.md`; FC/BC = `.ufo/waves/round-17/l1-capture/{fresh,boot-chain}-capture.txt`; PL = `/var/log/pacman.log`.

**Keep (dated 2026-10-14 runs, not current-use):** PSP:3-5, :114-142, :267-270; ARP:30, :205-206, :233. Stale below are present-tense host statements.

| path:line | exact quote | capture now shows |
|---|---|---|
| PSP:42, ARP:40 | "1188 installed, 16 foreign"; "`pacman -Q` = **1188**" | FC:31 → 1394 local dirs [obs] |
| PSP:75 | "All four configured sync dbs" | FC:10-14 → five, incl. `openai-chatgpt.db` [obs] |
| PSP:82,84 | "`offline.db` (304318 B)"; "Dead leftover file" | absent from FC:10-14; ARP:16/:273 probes now rc=1 [obs] |
| PSP:90 | "Last local-db write … 2026-10-13 16:37:59" | PL:3158 transaction 09:39:21 today [obs] |
| PSP:112 | "last data update ≈ Oct 11" | PL:2581 keyring 20260909-1, 09:16:31 [obs] |
| PSP:143 | "`paccache` not installed" | BC:55 `pacman-contrib` installed 07:45 [obs] |
| PSP:277-279 | "`snapper list-configs` → empty table"; "no rollback net is configured" | FC:42-45 root+home; BC:160-167 snapshots 1,2 [obs] |
| PSP:310 | "No stale pin on this note" | BC:5 kernel 7.2.11; PL:2580 pacman …-3 [obs] |
| ARP:47 | "orphans … `electron39`, `mbedtls`, `webp-pixbuf-loader`" | BC:57, PL:3155-3157 all removed [obs] |
| ARP:48 | "None of the 16 has ever been upgraded" | PL:3095-3121 thirteen upgraded → 2.22.1 [obs] |
| ARP:98 | "no `[PACMAN] Running 'pacman -U …'` line anywhere" | PL:3092 is that line [obs] |
| ARP:103 | "**1275** entries including `elephant-2.21.0-1` … exactly the versions installed" | db absent FC:10-14; PL:3095 now 2.22.1 [obs] |
| ARP:109 | "`[options] [core] [extra] [multilib] [omarchy]` (lines 3/19/22/25/28)" | FC:14 sixth repo db [obs] |
| ARP:198 | "fires for **2/16**" | [unk] `%VALIDATION%` after unsigned `-U` |
| ARP:227 | "`active (running) since Wed 2026-10-14 13:11:08`" | BC:9 boot 09:57; PL:3123 restart hook; current state [unk] |

Also stale: ARP:15 "expect 16" (count likely still 16, versions not); ARP:65-79 register rows ("2.21.0-1", `sha256 pgp`, "never"). Unverifiable in captures: PSP:71 `-Qu`=0, PSP:70 yay 13.0.1, PSP:114-142 cache size.

Scope: executed=none
