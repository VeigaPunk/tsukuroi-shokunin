# Receipt index — R49CritAdjA (C2-B6)

All commands were run with absolute paths from
`/fast/scratch/hyaku/tsukuroi-r49/R49CritAdjA`; fixtures were `git clone --shared` of the lane at
`d7cfc27308e8af51b76b5cfe0c656acc1788cefb` with one commit each. Nothing under the lane was written.

## Revisions
- freeze (bytes under test): `55c07cd3f8bff2e12117c34d57b4c618de74d85c`
- lane tip / fixture base: `d7cfc27308e8af51b76b5cfe0c656acc1788cefb`
- round-start base: `6256760d1382ce4ce20fcba830d4b2912cfbf12b`

## Fixtures (repo shas recorded in `fixtures*.txt`)
| id | commit | receipt prefix |
|---|---|---|
| A (whole-section stub) | `5d73aee3ba6c0cb9e32fa65b86895008f21bf715` | `res.A.*`, `chk.A.json` |
| A2 (table-only stub) | `b02f5eb98c3e51585311f02e94c4757d63ca991c` | `res2.A2.*`, `chk2.A2.json` |
| A3 (stub + UNRESOLVABLE bookkeeping) | `8612944ad112ed5169dab05089dd7c0adfcf63e9` | `res3.A3.json`, `chk3.A3.json`, `a3-registry.diff` |
| B (quotes -> x) | `d761e36929948a2804062751555bde1ab2d6a5c9` | `res.B.*`, `chk.B.json` |
| B2 (duplicate fake rows) | `2de1cada1307654965558347db8cfd3af6cbd46f` | `res2.B2.*`, `chk2.B2.json` |
| B2neg (negative control) | `47fc00ca726634c64abe4233f145afbb855c255f` | `res3.B2neg.json` |
| C (wrong sibling cells) | `12505888c91ef29adb37170d932bdb3cba1580c8` | `res.C.*`, `chk.C.json` |
| C2 (wrong sibling+heading) | `cf89b966439eb7fb690d2bf4c888e1e757bc8340` | `res2.C2.*`, `chk2.C2.json` |
| D (recipient mismatch) | `613bee63f99c29a00674411f1adacd66d2d3294f` | `res2.D.*` |
| E (bare range in non-final cell) | `d79248a74cf58350faa3ab8d1c8f14eafcb391bb` | `res3.E.json` |

## Key observations
- `base.json` — counter at the freeze revision: `anchors_checker_rc=1`, verdict FAIL, rc=1.
- `chk.json` / `chk-<rev>.json` — the anchors checker alone at `6256760` (PASS), `55c07cd` (FAIL,
  `INBOUND-CLASSIFICATION-WRONG inbound[108]`), `d7cfc27` (PASS).
- `ovr.B.json`, `ovr.C.json` — `--province-file` at lane `d7cfc27`: PASS rc=0 while the overridden
  province is cheated (checker leg read the lane's clean `PROVINCE.md`).
- `PROVINCE.*.md` — the exact variant documents committed into each fixture.
- `registry.real.json` (freeze), `registry.tip.json` (d7cfc; IN-109 `found_line` 2660).
- `freeze-to-tip-registry.diff` — the post-freeze repair: `found_line 2642 → 2660` (+ note).
- `a3-registry.diff` — the A3 fixture's registry rewrite (17 records → `UNRESOLVABLE`).
- `sha256-frozen-tools.txt` — digests of the frozen counter and checker as extracted by `git show`.
