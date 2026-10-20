# QUALITY 1–24 — corpus/knowledge/boot-chain-r17.md

Not admissible: A=satisfied, P=partial, N=fails.

| # | applies | evidence |
|---|---|---|
|1|A|verdict rules, digests, Falsifier (md:62–126)|
|2|P|no anchor: nvhelpme session (md:16), /var/backups (19), snapshot subvols (64–66); pacman.log-after-09:18 false (capture:87–97)|
|3|A|[obs]/[inf]/[unk] split; copy actor in [obs] (md:30–31)|
|4|N/A|new entry; append-only policy (md:146)|
|5|A|four rejections kept (md:129–139)|
|6|N/A|no pacman action advised (md:9–11)|
|7|A|S051–S054 tier A; item 7 names uncited S014 (md:149)|
|8|P|headers present; named tools/boot-chain-audit.sh absent (md:3)|
|9|P|line 157 placeholder; 158 is rc line|
|10|P|no R17 notice: SKILL.md:1833, corpus/README.md:38, host-health-r3:594, update-safety-v3:410|
|11|N|no LOG.md round-17/boot-chain entry (LOG ends r16)|
|12|P|snapshot-copy mechanism declared unread (md:98)|
|13|N/A|no EACCES triage|
|14|N|lessons/round-17.md Gate absent; 11/12/22 unevaluated; S014 uncited|
|15|N/A|no DAC/namespace claim|
|16|N/A|no metadata health grading|
|17|N/A|no unit-permission explanation|
|18|N/A|no fixtures/bots|
|19|P|v42.1/v42.2 absence has no quote; S021 quote elided|
|20|N/A|no comment attribution|
|21|P|capture:144/148/154 truncated pre-rootflags; md:101 no line; l0 path lane-local (fleet:60)|
|22|P|scope+date (md:50); no quote|
|23|N/A|no citation repair|
|24|A|read-only headers; no seat probe|

[dev] read-only repo/capture reads only.

Scope: executed=ls (tools,LOG.md,SKILL.md,lessons), wc -l LOG.md corpus/README.md, tail -c3000 LOG.md, grep/sed capture
