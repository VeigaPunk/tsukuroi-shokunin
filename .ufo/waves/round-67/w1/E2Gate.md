# E2Gate — C2 before-measurement + patch draft (round 67, w1)

Status: C2 reproduced on a sandbox mutant; patch drafted and measured. No tracked file touched.

## 1. C2 before measurement (base gate, silent uncount)

Sandbox clone: `/fast/scratch/hyaku/tsukuroi-r67/E2Gate/lane`, `--shared` clone of the lane,
checked out at base `5abc31d995f53d8bd7283fab78fa6d4a51e97ea6`, `rev-parse --show-toplevel`
printed the sandbox path.

Honest baseline (`e2-honest-base.json`, rc=0): `status PASS`, `counts.live_object_checked 10`,
`counts.live_object_match 10`, `findings []`.

Mutant (sandbox commit `2a7a50fb88b3947a6caff274ffd08fc2f64fb66c`, `r67-mutant`):

- `corpus/knowledge/adjacency-anchors-r19.json` `outbound[9]` (OUT-010, tameshi):
  `sibling_commit 01d586ddbc5fcd78659557c4e93a6ee8517b87d1` →
  `aa3dc2b5b3fa5173637b81dea99d76d61b304d5d` (`sha1("r67-fabricated")`).
- `PROVINCE.md` published section: the record's one 40-hex occurrence and its one 12-hex
  abbreviation replaced with the fabricated value; `sibling_blob_sha256` unchanged
  (the snapshot predicate still passes).
- Fabricated commit verified absent in the sibling repo:
  `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e aa3dc2…^{commit}` →
  `fatal: Not a valid object name aa3dc2b5b3fa5173637b81dea99d76d61b304d5d^{commit}`, rc=128.
- `bind` requires the revision to be an ancestor of `refs/remotes/origin/master`, so the
  sandbox-only ref was advanced: `git -C <sandbox> update-ref refs/remotes/origin/master 2a7a50fb`.

Base gate on the mutant (`e2-mutant-base.json`, rc=0): `status PASS`, `findings []`,
`counts.live_object_checked 9`, `counts.live_object_match 9`, `outbound_portable 10`.
This is exactly the declared C2 defect: one fabricated live-object pin is silently uncounted
and the gate still passes.

## 2. Patch draft

- Draft file: `.ufo/waves/round-67/drafts/check-adjacency-anchors.r67.py`
  (sha256 `588cc44fb47a46fadeac87c5f83824111d0acf302b4a0e97141d30b63a60f832`).
- Diff: `.ufo/waves/round-67/drafts/c2-patch.diff` (38 lines; `diff -u` rc=1, files differ;
  headers carry the scratch paths — the draft file is the authoritative artifact).
- Change 1, outbound loop in `evaluate` (after the existing `live_object_hash` block):
  when `live_digest is None` and `Path(siblings_root)/f"{sibling}-shokunin"` is a directory,
  append `_finding("ANCHOR-LIVE-OBJECT-UNRESOLVED", site, "sibling_commit does not resolve in
  the sibling repository")` and set `valid = False`. Absent sibling directory keeps the old
  behaviour (no finding, no count).
- Change 2, one new selftest case `live-object-unresolved` (no existing case altered): a real
  git repo `fixture-shokunin` without the pinned `1*40` commit, run on the clean revision with
  that root as `--siblings-root`; expects `FAIL` with exactly `[ANCHOR-LIVE-OBJECT-UNRESOLVED]`
  and `live_object_checked == 0`.

## 3. Patched measurements

| run | command (patched tool) | rc | status | findings | live_object_checked / match |
|---|---|---|---|---|---|
| mutant revision `2a7a50fb` | `--revision 2a7a50fb --siblings-root /home/vgpnk/Projects/shokunin` | 1 | FAIL | `ANCHOR-LIVE-OBJECT-UNRESOLVED` at `…:outbound[9]` | 9 / 9 |
| honest base `5abc31d9` | same, honest revision | 0 | PASS | `[]` | 10 / 10 |
| absent sibling (kagi) | `--revision 5abc31d9 --siblings-root <scratch>/sibs` | 0 | PASS | `[]` | 9 / 9 |
| selftest | `--selftest` | 0 | PASS (26 cases, 26 passed, 0 failed) | — | — |

Base tool selftest before the patch: `PASS (25 cases, 25 passed, 0 failed)` — the patch adds
exactly one case and breaks none. In the patched mutant run `outbound_portable` drops to 9
because the invalidated record no longer counts as portable; the declaration only fixes
status FAIL + finding id, and that holds.

Absent-sibling fixture: a scratch root symlinking mori, kama, mado, kumitate, kaidoku,
revenger, tameshi but not `kagi-shokunin` (OUT-003); no new finding, status stays PASS.

## 4. Risks / integration notes

- The new finding is keyed on the sibling directory's existence, not on git reachability:
  a present-but-broken sibling clone (unreadable git dir) also yields the finding. That is the
  intended reading of "sibling repo exists but the pin does not resolve"; an absent sibling
  stays silent by design.
- The patch uses `record["sibling"]` directly inside the already field-validated outbound
  loop (records with a wrong key set `continue` earlier), so no new KeyError path.
- The L1 should run the lane gates once after landing; this seat ran none.
- Scratch `/fast/scratch/hyaku/tsukuroi-r67/E2Gate` was deleted after the receipts were copied.

## 5. KEY=VALUE

```
base_mutant_status=PASS
base_mutant_live_checked=9
patched_mutant_status=FAIL
patched_mutant_findings=ANCHOR-LIVE-OBJECT-UNRESOLVED
honest_base_status=PASS
honest_base_live_checked=10
selftest_result=PASS (26 cases, 26 passed, 0 failed)
absent_sibling_findings=none
```
