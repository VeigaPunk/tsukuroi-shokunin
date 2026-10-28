VERDICT: defect-found

## Evidence and verdicts

Frozen counter: `8029cdba1049df25632c91a23c8db4eefb54be5f:tools/check-adjacency-table-r50.py`; scratch copy SHA-256 `d571adc9562b2832baf270086181c770b25eea6c5147d49b27a1525564e00a8b`. The pristine counter on the frozen lane returned rc=0, PASS, with `adj_rows=7 linked_rows=7 bare_ranges=0 anchors_ok=7 registry_ok=7 anchors_checker_rc=0 quote_at_pin_ok=9 live_quote_ok=9 stub_fails=1`.

Exact common invocation (each `<counter>` and fixture option below substituted):

```sh
python3 <counter> --revision 8029cdba1049df25632c91a23c8db4eefb54be5f --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin <fixture-options>
```

All five requested mutants PASSed the real province (rc=0). Their isolated fixtures and results:

| Mutant | Mutation | Defect fixture and observed result | Fixture verdict |
|---|---|---|---|
| M1 | Removed pinned-blob digest comparison | `--registry-file fx/registry.f1-digest.json`; pristine FAIL/pin=8, M1 PASS/pin=9, rc=0 | Mutant escapes this fixture; digest leg is load-bearing. |
| M2 | Removed pinned-blob heading test | `--province-file fx/PROVINCE.f2-heading.md`; pristine FAIL/pin=8, M2 PASS/pin=9, rc=0 | Mutant escapes this fixture; heading leg is load-bearing. |
| M3 | Replaced live-tip lookup with `d['live']=True` | `--siblings-root fx/root3` (kagi and tameshi fixture clone tips drifted while their pinned blobs remain intact); pristine FAIL/live=7, M3 PASS/live=9, rc=0 | Mutant escapes this fixture; live-tip leg is load-bearing. |
| M4 | Replaced computed `stub_fails` with literal `1` | Real and defective fixture verdicts/`stub_fails` identical; additionally `--siblings-root fx/root6` includes a committed `stub-shokunin` repo but synthesized stub still has `stub_content_pin=0`, `stub_fails=1` | Equivalent on exercised inputs; survives. Structural reason below. |
| M5 | Relaxed `pin_ok == 9` to `pin_ok >= 1` | `--registry-file fx/registry.f1-digest.json`; pristine FAIL/pin=8, M5 PASS/pin=8, rc=0 | Mutant escapes this fixture; exact-count predicate is load-bearing. |

M3 fixture construction used only scratch clones under `/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterD/fx/root3`; pin blob SHA-256s remained the registry values (`kagi 4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523`, `tameshi 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f`), while both fixture tips lacked the quoted sentence.

### Frozen pre-data control battery

The frozen battery file `.ufo/waves/round-50/controls/battery-summary-r50-c3.jsonl` records four controls and their expected outcomes: K1 stub FAIL (`pin=0 live=0`), K2 wrong-class FAIL (`anchors_ok=6 pin=8 live=8`), K3 mutated digest FAIL (`pin=8 live=9`), K-pass real province PASS (`pin=9 live=9`). I reconstructed these exact cases and ran each mutant against them. M1 and M5 were **killed by the battery**: K3 changed from expected FAIL to mutant PASS. M2, M3, and M4 **survived the battery**: all four expected outcomes remained unchanged. The battery contains no heading-less or drifted-tip control; isolated M2/M3 fixtures above show those counter legs do reject such inputs when present.

### `stub_fails` defect

M4 is equivalent because the synthesized stub rows use sibling `stub`, commit `0000000000000000000000000000000000000000`, and digest `111…111` (counter `stub_province()`); `content_legs()` exits on absent `stub-shokunin` or unresolved all-zero commit before digest/heading/quote/live checks can distinguish a weakened checker. The extra root6 probe supplied a real `stub-shokunin` Git repo, but the hard-coded stub commit still could not resolve: observed `stub_content_pin=0, stub_fails=1`. M7, a scratch-only combined mutant dropping digest, heading, quote, and live-tip checks, **PASSed** the strong-stub fixture (`--province-file fx/PROVINCE.f8-strongstub.md`, rc=0, `pin=9 live=9 stub_fails=1`) while it also reports `stub_fails=1`. Thus the current `stub_fails == 1` predicate does not establish that content checks reject a shape-valid stub; it stays true even when all content checks are bypassed. K1 still fails for the unrelated absent synthetic sibling. This is a coverage finding; no lane bytes were changed.

## Commands and receipts

The full matrix command was `cd /fast/scratch/hyaku/tsukuroi-r50/R50MutCounterD && python3 driver.py` (54 runs, 6 counters × 9 fixtures, 9.055 s); output and exact expanded invocations are recorded in `results.json` and `driver.py` under the seat receipts directory. Strong-stub follow-up: `python3 driver2.py`; M7 follow-up used the same common invocation above with `mut/M7.py` and fixture options as reported. Mutants were scratch copies; no mutation touched frozen lane bytes.

Pristine copy hash before/after: `d571adc9562b2832baf270086181c770b25eea6c5147d49b27a1525564e00a8b` (identical). The frozen source was read-only; no restoration of lane bytes was needed. Scratch tree was removed after copying receipts. No tools installed.
