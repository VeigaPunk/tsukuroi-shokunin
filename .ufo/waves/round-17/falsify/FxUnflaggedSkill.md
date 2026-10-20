# FxUnflaggedSkill — stale current-use, no R17 notice

**Verdict.** C2 as worded ("48 … six knowledge entries") SURVIVES; any reading of 48 as total coverage FAILS. Both assigned files carry zero `R17-FRESHNESS` notices (`grep -c` = 0), and root `SKILL.md` is unreachable by the gate (`tools/check-freshness-r17.py:62` path regex `^corpus/knowledge/…`).

**SKILL.md** — current-use, stale, no R17 notice:
- :118 "both `7.2.3` today" → 7.2.11-arch1-1 [obs] BC:5, FC:41.
- :129-133 "`snapper list-configs` → empty … no snapshot net is configured" → `home`/`root` configs FC:42-46; snapshots #1/#2 `ro=true` BC:160-167.
- :135 "last: 2026-10-13 16:37" → 2026-10-20 09:39:21 BC:67.
- :1833 "Installed `mkinitcpio 41.1-1` with 42.2-1 pending" → 42.2-1 BC:32,45.

**host-health-report-r3.md** — no R17 notice:
- :591-594, inside its own "For current use on 2026-10-20" banner: "413 pending rows … `mkinitcpio 41.1-1` installed with 42.2-1 pending" → upgrade 09:15:31 (FC:8), 448 upgraded (FC:84), 42.2-1 (FC:16).
- :301-306 U1 "Any wave on this host is snapshot-less … before any `-Syu`" → configs exist FC:42-46; snapshot #1 created 09:03:02 BC:80,166.

Wave 1 already marked this unmet: `build/RevQualityChecklist.md:16` "no R17 notice: SKILL.md:1833 … host-health-r3:594".

**Wording.** No full-coverage claim found: SCORECARD.md:505 ("statements carrying a dated R17 notice"), corpus/README.md:152-154 ("Six older entries"), and c2-after.json `scope` all self-scope the count; [unk] round report (unwritten).

BC/FC = `.ufo/waves/round-17/l1-capture/{boot-chain,fresh}-capture.txt`.

Scope: executed=ls, find, wc, grep, sed, awk, cat, python3 -c (registry JSON read)
