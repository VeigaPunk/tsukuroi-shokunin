# R18 C3 per-surface sweep — corpus/knowledge/boot-plane.md

[obs] Target is byte-identical to baseline 842a5312 (`git diff --quiet` rc=0), 318 lines, no R17/R18 notice heading. The R17 registry (`corpus/knowledge/freshness-recheck-r17.json`) holds 0 records for this path (48 records across six other files); closure defect 5 routes `journal-boot-plane.md`, not this note. Sources: S060 `host-capture-r18.txt`, S051 `boot-chain-capture.txt`.

## Candidates and dispositions

| baseline line | exact quote | ruling |
|---|---|---|
| 6 | ``kernel `7.2.3-arch1-3` `` | Dated by `boot-plane.md:8` (`verified-at: 2026-10-14 13:19–13:31`). R18 `:6` = `7.2.11-arch1-1` is a later environment, not a refutation; R18 `:95` keeps 7.2.3 dkms residue. Not stale [obs]; concurs `FxUnflaggedBoot.md:16`. Divergence: R17 noticed the same-shaped driver-firmware header (`driver-firmware-plane.md:274`). |
| 20-21 | `retention unchanged from round 3: **13 boots**` … `181.3 M` | Dated probe-context (13:19). Captures don't count boots/bytes: `boot-chain-capture.txt:7-10` lists only −2…0; R18 has no `journalctl`. Drift suggested by `corpus/README.md:49` (9 boots, 2026-10-19) but no capture binds it → [unk]. |
| 79 | `Retention wall: nothing older than boot −12` | Capture bound of 2026-10-14; same [unk]. |
| 213 | `operator probe: crypttab/keyfile audit` | Still-live, unresolved action; R18 `:9` confirms `cryptdevice=` but measures no dwell. Not stale. |
| 240 | `Effective journald retention beyond the 13 retained boots.` | Open unknown; the count is dated. |
| 317 | `recheck: 30d; procedure: Appendix command set` | No forbidden binary; due 2026-11-13. |

Method/limitation text (`:225-230`, `:251`) re-checked against both captures: no contradiction [obs].

## Disposition

Bounded no-evidence: no provable stale current-use statement; no append block, no `R18-FRESH-*` record. Do not count this note toward the registry-scoped freshness total; `:20-21` stays a candidate for a capture running `journalctl --list-boots`/`--disk-usage`.

Scope: executed=read-only git/grep/jq/sed/wc over lane corpus and captures; no host probes, no writes outside this report.
