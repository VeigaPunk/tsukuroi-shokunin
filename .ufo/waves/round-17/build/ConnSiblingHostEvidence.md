# ConnSiblingHostEvidence (R17)

[obs] `/var/log/pacman.log`: `:2416/2419` man-pages 6.19-1 (01:07:12); `:2429/2432` libinput 1.31.3→1.32.0 (04:25:16); `:2462-2464` `-Syu` (09:15:30).

`M`=.ufo/reports/round-17/mado.md; `S`=.ufo/reports/round-16/souji.md; `C`=l1-capture/boot-chain-capture.txt; `J`=mado-shokunin/.ufo/waves/round-17/evidence/tripwire-pacmanlog-join.txt.

| contested (path:line) | finding |
|---|---|
| `M:159` "13 runs … no recorded actor" | holds only "in the log" (`J:17-18`); `C:76-96` shows account vgpnk for 13, PWD four `/home/vgpnk/tmp` (`C:76-79`), rest `nvhelpme`/`/home/vgpnk` (`C:82-96`). Account [obs]; operator [inf]. |
| `M:159` "pacman -Syu, mkinitcpio 41.1→42.2" | omits `limine-update` 09:26:11 second build (`C:86`; `boot-chain-r17.md:28-29,138-139`): upgrade≠booted image. |
| `S:74` "pacman paused host-wide"; kaidoku r16:95/r17:117; kama r16:171 | 13 vgpnk runs postdate r15's 04:44 snapshot; only lane-scope holds [inf]. |
| `L0:54` libinput recovery | verdict: tsukuroi `host-health-report-r3.md:591-594`; call record: `J:8` (`call_38165`). Split unstated. |
| `M:138` mori man-pages | install (`pacman.log:2416-2419`; mori `LOG.md:756`) invalidates current use of tsukuroi r12 `.ufo/waves/round-12/resumed/AclSemanticsR.md:137` "man-pages uninstalled" (a `man`-rc inference); no R17 notice. |

Move (C2→C1; C3 untouched): append one pointer-only `## Cross-lane provenance` block to `boot-chain-r17.md` — `M:159` log-only, `J:8` libinput call, man-pages install vs `AclSemanticsR:137`, account+PWD not "operator", `M:159` not independent. C2 recheck cites the block; no sibling edit.

Risk: sibling receipts are author-asserted; log bytes evidence, sibling lines claims. Verify by re-reading cited log lines, `C:76-96`, `J:8,17-18`.

Deviation: two pre-rule read-only repo listings (`ls`, `head`); no host probe.

Scope: executed=ls,head
