# Sweep13 — C3 reconnaissance: corpus/knowledge/closeout-r11.md

Baseline 51dd9eea; surface byte-equal (`git diff` on it empty). Compared against S060 R18 `host-capture-r18.txt` and R17 S052 `fresh-capture.txt`, S051 `boot-chain-capture.txt`. Dated captures and pin-bounded receipts stay intact. Two still-live elevation actions are stale.

**1. `:223` row 2.** Quote: `` `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1` ``. [obs] S060 `:95`: `nvidia/615.78.08, 7.2.3-arch1-3, x86_64: installed (Original modules exist) (Built modules are missing in the kernel modules folder)`; running kernel `7.2.11-arch1-1` (`:6`); no 610.57.04/7.1.4 row (`:93-95`). Live target is 615.78.08 / 7.2.3-arch1-3. The 2026-10-14 re-measurement stays historical. Operator-only; not executed.

**2. `:229` row 8.** Quote: ``configure snapper + `SNAPPER_CONFIG_NAME` (or accept snapshot-less); re-audit``. [obs] configured: S060 `:76-77` (`home`, `root`), `:80` `SNAPPER_CONFIGS="root home"`; S052 `fresh-capture.txt:74` `SNAPPER_CONFIG_NAME="root"`; S051 `boot-chain-capture.txt:160-161` snapshots #1/#2 `ro=true`. Do not re-run `create-config`; only re-audit remains.

**Proposed block.** Unique heading `## R18-FRESHNESS — elevation-gated register re-verification (2026-10-20)` (absent baseline). Body states: historical snapshots keep dated meaning; supersedes current-use only; read-only, no package/service/reboot clearance; sources S060, S052, S051; then the two corrections with the capture refs above. Record ids `R18-FRESH-Sweep13-01/02`.

**Bounded no-notice.** `:226` bare `-Sy` already append-superseded (`:405-409`). Rows 1,3,4,6,7,9: no R18/R17 capture marks them stale; bounded no-evidence. `:313-315` md5/80-case expectations are pin-bounded ("at this pin"; mismatch procedure documented); baseline tool is `b7de3bdd…`/97 declared cases — revision drift, not host advice, and no capture line exists. Other §3.2 debts are dated freezes; the SCORECARD paren repair landed (`SCORECARD.md:8`).

**Repo-internal.** `:247-248` says `corpus/README.md` is unchanged since r3 (20 `wc -l`, no `## Frontier`); baseline README is 155 lines, md5 `e1a5559e…`, `## Frontier` at `:28`. Not capture-bindable.

[unk] Whether row 8's finding ("no rollback net") is itself resolved, or only its configure action: policy call above C3 evidence.

Scope: executed=read-only git show/diff/hash and text reads (nl, grep, python); no host probe, pacman, test or gate.
