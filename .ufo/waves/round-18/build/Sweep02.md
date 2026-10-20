# R18 C3 per-surface sweep — corpus/knowledge/systemd-user-plane.md

[obs] Target is byte-identical to baseline 842a5312 and lane 51dd9ee (`git diff --quiet` rc=0), 270 lines, sha256 `85ada775c1dbccd775f9a0710c7cb5274915541aae2521d3e74dd32d4435465e`, no R17/R18 notice heading. The R17 freshness registry holds 0 records for this path (six other files); closure defect 5 does not route it. Sources: S060 `host-capture-r18.txt`, S051 `boot-chain-capture.txt`, S052 `fresh-capture.txt`.

## Candidates and dispositions

| baseline line | exact quote | ruling |
|---|---|---|
| 3 | ``systemd 261 (261.2-1-arch)`` | Dated (`probe 2026-10-14`; `:269` `verified-at: 2026-10-14`). Host now has `systemd-262-1` (upgrade `[ALPM] upgraded systemd (261.2-1 -> 262-1)` at `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:44`; `/var/lib/pacman/local/systemd-262-1` at `fresh-capture.txt:23`), boot 0 at 09:57:09 (`boot-chain-capture.txt:10`). [inf] the user manager runs 262-1. The pin is true at its date; `:169` `on this systemd 261` is version-scoped, not live advice. Not stale under the dated-snapshot rule; revisit at the 30-day recheck. Divergence: R17-FRESH-PARTIAL-01 noticed the same upgrade because that row was current-use, not probe-dated. |
| 17, 52, 82, 88 | ``1 timers listed.`` / `disabled` | Dated 2026-10-14 run-state. No capture measures `systemctl --user`: S060 is host-level only; R17 `fresh-capture.txt:47-54` reads system units only. Unconfirmed [unk]. |
| 76, 78 | `109 unit files` / `17 roots` | 261.2-1 package-shipped values; the package changed, neither capture recounts them. Unverified, not provably stale. |
| 7, 167-170, 249-261 | practical rule / method lessons / recheck pointer | Still-live advice; no capture contradicts it. Recheck due 2026-11-13. |

## Disposition

Bounded no-evidence: no provable stale current-use statement; no append block, no `R18-FRESH-*` record. Do not count this note toward the registry-scoped freshness total. Candidate for a future capture running `systemctl --user --version`, `list-timers --all`, `list-unit-files`, and `is-enabled` for the named units.

Scope: executed=read-only git diff/log, ls, grep, sed, sha256sum, python3 JSON read; no host probes, no writes outside this report.
