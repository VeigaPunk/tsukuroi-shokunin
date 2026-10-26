VERDICT: supports

# Seat CritSeparabilityFinal — Item N-15: causal separability of C1 and C2 at the tip

Question: at 8acf0b022586a0f3164c77659fb96ba5f90949b6, can C1 be verified with
C2's changes reverted, and vice versa? Both partial trees were built in scratch
clones and both frozen counters were run on both trees (plus a tip control).

## Trees under test (fixtures, /fast/scratch/hyaku/tsukuroi-r43/CritSeparabilityFinal)

- **C1-only** `1c9e02d5dd8a28477ec52eb2a1f2484e1e027655` = base
  `6951ead90566b2d74f7c45b4efca29246badad64` + `tools/boot-chain-audit.sh` at tip.
  `git diff <base> <C1-only>` shows only `M tools/boot-chain-audit.sh`; blob equals
  tip blob `6a2be016ce6f4b8811eb6150396f7609b48f5371` (C1 surface: `inputs_newer_than`
  at tip line 463, `boot_inputs_newer` rewrite at 477, `R43-C1-*` selftest cases at
  1232–1239).
- **C2-only** `d5a9bb42d77866ccbecd0d6029b50d63ca280dd8` = base + the five C2
  surfaces from tip: `corpus/knowledge/btrfs-scrub-record-r43.md`, `…-r42.md`,
  `corpus/SOURCES.md`, `.ufo/waves/round-43/frozen/src/ioctl.c` (sha256
  7b3488f2…ba01 = S240), `.ufo/waves/round-43/frozen/hostcap/capture.txt` (sha256
  f7ecbe7c…c556 = S241). Diff vs base is exactly those 5 files; all blobs equal tip
  blobs. S237 `scrub.c` is identical at base and tip (sha256 48df2e2f…0801), so the
  base copy is already the frozen S237.
- **Tip control** `8acf0b022586a0f3164c77659fb96ba5f90949b6` (lane HEAD).

Counters were copied to scratch and run as scripts (never imported from the lane):
`score-bootinputs-r43.py --revision <rev> --lane <fixture> --scratch <scratch>`,
`check-scrub-record-r43.py --revision <rev> --lane <fixture>`.

## Run matrix (receipts in w2/CritSeparabilityFinal/)

| Counter | Tree | Verdict | Observed conjuncts |
|---|---|---|---|
| C1 | C1-only | PASS | cases=16, correct=16, identity_ok=1, live_agree=1, selftest_pass=1 (total=49), selftest_r43=4 |
| C1 | C2-only | FAIL | correct=8 (base behavior), selftest total=45, selftest_r43=0; identity_ok=1, live_agree=1, selftest_pass=1 |
| C1 | tip (control) | PASS | identical to C1-only: correct=16, selftest total=49, selftest_r43=4 |
| C2 | C1-only | FAIL | rows=0, quotes_ok=0, props_ok=0, host_ok=0, sources_ok=0, verdicts_ok=0, novelty_base_hits=0, pointer_ok=0, snapshots_ok=false, capture_ok=false |
| C2 | C2-only | FAIL | rows=3, quotes_ok=3, props_ok=3, host_ok=3, sources_ok=1, verdicts_ok=0, novelty_base_hits=0, pointer_ok=1, snapshots_ok=true, capture_ok=true |
| C2 | tip (control) | FAIL | exactly identical to C2-only (all conjuncts hold except verdicts_ok=0) |

## Which conjuncts move

- **C1 counter on C2-only**: the only conjuncts that differ from tip are the ones
  driven by the boot script itself (correct 16→8, selftest_r43 4→0, selftest total
  49→45). C2's surfaces being present changes nothing: identity_ok, live_agree and
  selftest_pass stay 1, and the failure signature (correct=8) is exactly the frozen
  base FAIL. Reverting C2 leaves C1 verification outcome unchanged.
- **C2 counter on C1-only**: six conjuncts move — rows 3→0, quotes_ok 3→0, props_ok
  3→0, host_ok 3→0, sources_ok 1→0, pointer_ok 1→0 (plus the informational
  snapshots_ok/capture_ok false). All of these are caused by the absence of the C2
  surface (entry, SOURCES registry rows S240/S241, frozen S240/S241 files; the r42
  pointer line), i.e. by C2's own changes being reverted, not by which boot script is
  present. verdicts_ok stays 0 and novelty_base_hits stays 0 — unchanged from tip.
  Reverting C1 leaves the C2 verification outcome unchanged (on C1-only it reads
  exactly as the empty-C2 surface would read).
- **verdicts_ok** is 0 on every tree including the tip control, because it counts
  this wave's w2 seats (`C2RevSR<n>`/`C2CritSR<n>`) through `w2-dispatch.json`,
  `w2-results.json` and the seat reports, which do not exist in any tree while the
  wave runs (check-scrub-record-r43.py:178-195, 283-301). It is a wave artifact, not
  a C1/C2 content difference — so it is not a separability signal. This reproduces
  the frozen claim "every conjunct but verdicts_ok holds at tip".

## Static cross-surface reads

- C1 counter reads exactly one lane path: `git show <rev>:tools/boot-chain-audit.sh`
  (score-bootinputs-r43.py:263); everything else is host-derived (oracle, generated
  cases, live probe, selftest). Grep for `corpus|SOURCES|frozen|scrub|btrfs|lessons`
  finds no lane reads.
- C2 counter reads only: SNAP `scrub.c`/`ioctl.c` (check-scrub-record-r43.py:237-238),
  CAPTURE (239-240), ENTRY (244-245), SOURCES.md registry (247-248), OLD (319), and
  the wave dispatch/results/report files (180-195). Grep for `boot-chain|bootinputs|score-boot|tools/`
  finds no reads of the C1 surface (only a usage-docstring mention at line 48).
- Therefore neither counter can observe the other claim's surface — the dynamic
  matrix above confirms this behaviorally (C1 output is identical whether C2 files
  are present or absent; C2 output is identical whether the boot script is base or tip).

## Conclusion

Causal separability holds at the tip: C1 PASSes with C2 reverted and FAILs exactly
like base when only C1 is reverted; C2 reproduces the full claimed state (all
conjuncts but verdicts_ok) with C1 reverted, and fails on the C2 surface only when
C2 itself is reverted. No cross-claim coupling exists in either direction.

## Guard notes

- No tools installed; no lane/fleet/host mutation; only the report and receipts were
  written under `.ufo/waves/round-43/w2/CritSeparabilityFinal/`. Scratch removed
  after copying receipts. No heavy counters ran concurrently (C1 runs serialized).
- Receipts: `c1-on-c1only.json`, `c1-on-c2only.json`, `c1-on-tip.json`,
  `c2-on-c1only.json`, `c2-on-c2only.json`, `c2-on-tip.json`, `build-receipt.txt`.
