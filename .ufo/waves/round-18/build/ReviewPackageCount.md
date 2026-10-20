# ReviewPackageCount — C1 falsifier: boot-chain-r17:19 count vs boot-chain-capture:59

**Verdict: SURVIVES.** The attack fails to falsify; closure defect3's count premise and the drafted corrections are capture-grounded.

## Attack (quote count 12/13)

- [obs] `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59` — `Running 'pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c sysstat stress-ng btrbk linux-lts linux-lts-headers'`. Independent recount: exactly **12** named targets; line complete (closing quote, no wrap).
- [obs] `corpus/knowledge/boot-chain-r17.md:19` (working tree at 51dd9ee) — "plus 13 named packages (B:59, B:82)" present, unique in file. "13" is unsupported by both cited lines.
- [obs] `boot-chain-capture.txt:82` (sudo journal, same 09:15:30 transaction) names 11 — ends `linux-lts`, omits `linux-lts-headers`.
- [inf] Plausible origin of 13: `boot-chain-r17.md:16` "4 of the 13" counts pacman runs 07:45–09:39, conflated with named targets.

## Correction drafts verified

- [obs] `drafts/NoticeBootCorrections.records.json` R18-CORR-01: `now` says 12 and explicitly scopes the count to B:59; `capture_quote` is an exact substring at committed `boot-chain-capture.txt:59`; `baseline_quote` matches working-tree :19 bytes; scribe reports quote and heading revalidated against baseline 842a5312.
- [obs] CORR-02/03/04 `capture_quote`s byte-exact at B:198, B:199, B:124; B:182–184 and B:251–253 hashes match the corrected citations. 4 records ≥ 3 required by C1.
- [obs] All four notices carry the preserved-historical/supersedes-current-use/read-only scope sentence; cite S051 (`corpus/SOURCES.md:57`), no invented sources; drafts only, production not appended.

## Residual risk / gaps

1. [obs] Updated append draft line 5 and record line 6–7 state that B:59 supplies the 12 count and B:82 names 11, omitting `linux-lts-headers`; no remaining count-scope mismatch.
2. [inf/peer-reported] The notice scribe reports baseline quote and heading revalidated against 842a5312; I did not independently read the baseline blob.
3. Out of scope, not re-derived: the "448 records" clause of :19 (S056:124–125 recount). Its line range 2462–3063 is consistent with B:59–60 (next Running at 3064).

Scope: executed=none
