# ExecAnchorRed — red-before proof for the digest gate (round 83, wave w1)

Scope: EXECUTOR, depth claim C1 (`tools/check-anchor-coordinates-r83.py`, digest bind R82-V5).
Freeze: d78b3b3982b5df62286dd65b0a42ae8a91847608. Frozen lane not mutated. Full receipts: `.ufo/waves/round-83/w1/ExecAnchorRed/receipts.txt`.

## Verdict

- **Pristine** counter matches the declared expectations: selftest rc0 16/16; doctored fixture rc2 cannot-evaluate; digest-fixed fixture rc0 8/8; real revision rc0 8/8. Battery C1 3/3 (rc0).
- **M-NODIGEST** (both `bind_digest` call sites removed): **RED CONTROL, killed.** Battery leg C1.a misses (rc0, 8/8 met on the doctored snapshot; expected rc2). C1 = 2/3, battery rc1. Mutant's own selftest 13/16 (3 digest cases fail).
- **M-UNDECLARED** (undeclared/malformed digest returns instead of raising): **NOT killed by the frozen battery.** C1.a/C1.b/C1.c all pass; C1 = 3/3, battery rc0. Only the mutant's own selftest catches it (14/16; digest-undeclared-refuses and digest-malformed-refuses fail). The frozen C1 kill rule names exactly this failure ("unmet if the digest gate accepts an undeclared or malformed digest"), but no leg exercises it.

## Finding (defect in the frozen battery; L1 decides)

`tools/round83-battery.py` `c1_legs()` has no leg for an undeclared or malformed `snapshot_sha256`. The frozen C1 predicate is therefore only partly enforced by the battery; the counter's own selftest covers it, but the battery number does not.

Proposed patch (scratch only, not landed): `$S/proposed-battery-C1d.patch` where `$S=/fast/scratch/hyaku/tsukuroi-r83/ExecAnchorRed`.
- Adds leg C1.d: copy `anchor-fixture-digestfixed` to a temp dir, pop `snapshot_sha256` from the entry, run `--fixture`, expect rc2 + `cannot-evaluate`.
- Changes C1 target 3/3 → 4/4 (`"target": "4/4"`, `c1_pass == 4` in `main()`).
- Verified in scratch clone `$S/lane-patch`: pristine battery rc0 C1 4/4; M-UNDECLARED battery rc1 C1 3/4 (C1.d miss); M-NODIGEST battery rc1 C1 2/4.
- Caveat: this changes the frozen "3 of 3 legs" wording. Per the declaration's no-re-scope rule, adopting it is an L1 decision and must be recorded as such; I have not applied it to the frozen lane.

## Minor defect (label only)

`tools/check-anchor-coordinates-r83.py:51` `CLAIM = "C2"`: the depth-C1 counter prints `"claim": "C2"` on every JSON line (lines 321, 328, 333). No verdict is affected. Proposed fix (`CLAIM = "C1"`) is not in the frozen lane; not applied.

## Why the doctored snapshot distinguishes the mutants

The doctored fixture changes only the XML prolog (`version="1.0"` → `"1.1"`). No quoted row text changes, so with the digest gate removed all 8 rows still locate at their declared spans. The digest is the sole mechanism that refuses the doctored snapshot, which is why M-NODIGEST passes the counter's doctored leg while still passing rows 8/8.

## Hashes

| variant | sha256 |
|---|---|
| pristine | b1e208af85965957f46301d307bc52689e3b2f9bcc9a050be6565faac5343e21 |
| M-NODIGEST | b3e983e68dc92194b5f76f723d933382f840a9e40063ad8a7badd2855960a2a1 |
| M-UNDECLARED | cd2407436c387b56f7e5088a3dcf23e2db630ba84f1d7076888d2b4b57917b00 |

## Tooling

No tools installed, upgraded or removed. No pacman, no `~/.local/bin` writes, no fleet-root writes. Scratch retained at `$S` (not deleted) because the proposed patch lives there.

## Checks the main agent should re-run

- `python3 tools/round83-battery.py --instrument r83 --revision d78b3b3982b5df62286dd65b0a42ae8a91847608` (pristine, expect rc0, C1 3/3, C2 4/4) — the same numbers as the declaration.
- If the L1 adopts C1.d: apply `proposed-battery-C1d.patch` and re-run the battery (expect C1 4/4, rc0) plus the M-UNDECLARED variant (expect rc1, C1.d miss).
