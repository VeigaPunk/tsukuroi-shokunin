## Attack

C1 adjacency gate fail-capability at `8e5916360f2dfe7bc4eb4ba144081af555900116`: challenge the same bounded detector with four independent, single-site corruptions of committed adjacency data. Axes: (1) outbound verbatim/publication integrity, (2) inbound census completeness, (3) inbound classification correctness, and (4) isolation plus exact restoration. This is a mutation probe, not an admission judgment.

Mutants: (a) remove the published OUT-001 quote row; (b) change one OUT-001 registry quote word, `independently` → `jointly`; (c) remove inbound record IN-001; (d) change IN-001 classification `DRIFTED` → `RESOLVES`. Each should make a pristine-green gate return FAIL/1 with a behavior-specific finding.

## Method

Isolated clone: `/tmp/tsukuroi-r19-FxMutAdj-20261021-8`. Clone source: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Setup ran in `/tmp`; gate and sha256sum commands ran with cwd equal to the clone. Every gate invocation used `python3 tools/check-adjacency-anchors.py --revision <exact commit>` with a 120-second subprocess deadline. No `--registry` or `--registry-from` override was used: the committed-mutant route worked, binding both revision and registry to the clone master; origin was removed before the pristine probe.

Edits were made with the surgical edit tool, not a shell rewriting script. Each case started from TIP, changed only the named site, committed with the fixture identity, and rebound clone master to that mutant. A Python subprocess wrapper recorded actual exit/stdout/stderr, and its finally block reset the clone to TIP, rebound master to TIP, rehashed the files, and ran the identical gate again before proceeding.

| Case | Exact edit against TIP | Expected finding id(s) |
|---|---|---|
| a | Delete `PROVINCE.md:121` in full: the published OUT-001 table row | `ANCHOR-UNPUBLISHED` |
| b | `corpus/knowledge/adjacency-anchors-r19.json:17`: replace only `independently` with `jointly` | `ANCHOR-QUOTE-MISSING`, `ANCHOR-UNPUBLISHED` |
| c | Delete `corpus/knowledge/adjacency-anchors-r19.json:140-159` in full: the IN-001 record and its trailing comma | `CENSUS-INCOMPLETE` |
| d | `corpus/knowledge/adjacency-anchors-r19.json:154`: replace only `DRIFTED` with `RESOLVES` | `INBOUND-CLASSIFICATION-WRONG` |

Exact external-command execution sequence (repetitions retained):

```text
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-FxMutAdj-20261021-8
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 remote remove origin
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD refs/heads/master
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 status --short
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master ef3a37aab20eeac24450de9396767dcac984b20c
python3 tools/check-adjacency-anchors.py --revision ef3a37aab20eeac24450de9396767dcac984b20c
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0
python3 tools/check-adjacency-anchors.py --revision abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e
python3 tools/check-adjacency-anchors.py --revision 8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 9df60fd03b41a8ede2373d8cf09be8a0511eaa9e
python3 tools/check-adjacency-anchors.py --revision 9df60fd03b41a8ede2373d8cf09be8a0511eaa9e
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116
git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116
sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
```

## Verdict

**CONFIRM — C1 fail-capability for these four assigned corruptions.** Pristine: PASS, exit 0, no findings. Mutants: **4 killed / 0 survived / 0 inconclusive**, each FAIL, exit 1, with the expected finding ids. Restored state: PASS, exit 0, no findings after each of the four cases, with every touched file restored to its exact pre-mutation SHA-256. No C2/C3 or overall C1 admission verdict is made.

| Case | Mutant commit | Actual exit/status | Actual finding ids | Restored exit/status |
|---|---|---|---|---|
| a | `ef3a37aab20eeac24450de9396767dcac984b20c` | 1 / FAIL | `ANCHOR-UNPUBLISHED` | 0 / PASS |
| b | `abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0` | 1 / FAIL | `ANCHOR-QUOTE-MISSING`, `ANCHOR-UNPUBLISHED` | 0 / PASS |
| c | `8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e` | 1 / FAIL | `CENSUS-INCOMPLETE` | 0 / PASS |
| d | `9df60fd03b41a8ede2373d8cf09be8a0511eaa9e` | 1 / FAIL | `INBOUND-CLASSIFICATION-WRONG` | 0 / PASS |

## Evidence

Source pointers at the attacked commit:

- `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:108-121` — portable ownership section and OUT-001 publication row.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json:8-20` — OUT-001 quote, pin and snapshot.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json:140-159` — IN-001, cited target line 42, found line 51, DRIFTED classification.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:412-438` — exact quote and publication findings.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:456-467` — inbound census completeness finding.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:521-541` — expected classification from found_line and captured target_ranges.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:618-637` — committed revision/registry loading.

Pristine gate command (exit 0) and stdout; each of the four post-reset executions returned this same stdout with exit 0:

```text
python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
{"branch": "master", "branch_tip": "8e5916360f2dfe7bc4eb4ba144081af555900116", "counts": {"inbound_by_class": {"DRIFTED": 17, "RESOLVES": 97, "UNRESOLVABLE": 0}, "inbound_by_scope": {"historical": 89, "operative": 25}, "inbound_classified": 114, "inbound_total": 114, "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 10, "outbound_total": 10}, "findings": [], "revision": "8e5916360f2dfe7bc4eb4ba144081af555900116", "status": "PASS"}
```

Actual mutant gate outputs (stderr empty for all four):

Case a, killed; exit 1:

```text
python3 tools/check-adjacency-anchors.py --revision ef3a37aab20eeac24450de9396767dcac984b20c
{"branch": "master", "branch_tip": "ef3a37aab20eeac24450de9396767dcac984b20c", "counts": {"inbound_by_class": {"DRIFTED": 17, "RESOLVES": 97, "UNRESOLVABLE": 0}, "inbound_by_scope": {"historical": 89, "operative": 25}, "inbound_classified": 114, "inbound_total": 114, "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 9, "outbound_total": 10}, "findings": [{"detail": "no line after the portable-anchor section heading contains both id and quote", "id": "ANCHOR-UNPUBLISHED", "site": "corpus/knowledge/adjacency-anchors-r19.json:outbound[0]"}], "revision": "ef3a37aab20eeac24450de9396767dcac984b20c", "status": "FAIL"}
```

Case b, killed; exit 1:

```text
python3 tools/check-adjacency-anchors.py --revision abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0
{"branch": "master", "branch_tip": "abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0", "counts": {"inbound_by_class": {"DRIFTED": 17, "RESOLVES": 97, "UNRESOLVABLE": 0}, "inbound_by_scope": {"historical": 89, "operative": 25}, "inbound_classified": 114, "inbound_total": 114, "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 9, "outbound_total": 10}, "findings": [{"detail": "quote is not an exact substring of the cited snapshot line", "id": "ANCHOR-QUOTE-MISSING", "site": "corpus/knowledge/adjacency-anchors-r19.json:outbound[0]"}, {"detail": "no line after the portable-anchor section heading contains both id and quote", "id": "ANCHOR-UNPUBLISHED", "site": "corpus/knowledge/adjacency-anchors-r19.json:outbound[0]"}], "revision": "abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0", "status": "FAIL"}
```

Case c, killed; exit 1:

```text
python3 tools/check-adjacency-anchors.py --revision 8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e
{"branch": "master", "branch_tip": "8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e", "counts": {"inbound_by_class": {"DRIFTED": 16, "RESOLVES": 97, "UNRESOLVABLE": 0}, "inbound_by_scope": {"historical": 88, "operative": 25}, "inbound_classified": 113, "inbound_total": 114, "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 10, "outbound_total": 10}, "findings": [{"detail": "no inbound classification for census id IN-001", "id": "CENSUS-INCOMPLETE", "site": ".ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json"}], "revision": "8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e", "status": "FAIL"}
```

Case d, killed; exit 1:

```text
python3 tools/check-adjacency-anchors.py --revision 9df60fd03b41a8ede2373d8cf09be8a0511eaa9e
{"branch": "master", "branch_tip": "9df60fd03b41a8ede2373d8cf09be8a0511eaa9e", "counts": {"inbound_by_class": {"DRIFTED": 16, "RESOLVES": 97, "UNRESOLVABLE": 0}, "inbound_by_scope": {"historical": 88, "operative": 25}, "inbound_classified": 113, "inbound_total": 114, "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 10, "outbound_total": 10}, "findings": [{"detail": "classification RESOLVES is inconsistent: expected DRIFTED", "id": "INBOUND-CLASSIFICATION-WRONG", "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[0]"}], "revision": "9df60fd03b41a8ede2373d8cf09be8a0511eaa9e", "status": "FAIL"}
```

Before each mutation and after each restoration, `sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py` returned the following pristine hashes (exit 0):

```text
2114d8cf6f53ab26c96183ddac401f2914900f500a59a277661f99da866120ff  PROVINCE.md
cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689  corpus/knowledge/adjacency-anchors-r19.json
c84101e9a99f0551c829035e9ffec83830cbc71e13df0bde74a7c58de52ea307  tools/check-adjacency-anchors.py
```

| Case | Changed file | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|---|
| a | `PROVINCE.md` | `2114d8cf6f53ab26c96183ddac401f2914900f500a59a277661f99da866120ff` | `6e0743274c43f88f6cc313d04e9e1637435140778c49fcb50309eacf5e555812` | `2114d8cf6f53ab26c96183ddac401f2914900f500a59a277661f99da866120ff` |
| b | `corpus/knowledge/adjacency-anchors-r19.json` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` | `bbf8f9e7383e1aa7b59a5ce7d74f0bf1e34ccb3a2b5daa8b29100cecbb834053` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` |
| c | `corpus/knowledge/adjacency-anchors-r19.json` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` | `37da4fd8736759ceea717cdeeb8299da7a591dfe75afe0640d349c29606c379c` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` |
| d | `corpus/knowledge/adjacency-anchors-r19.json` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` | `740a71c08a4f254c75cc889d44759de906b3a23a5e912243a06cee13788b509e` | `cd310de18873c34f93cd6408116c0626613aa9285ba8ee0c5cdff9e8b1139689` |

The gate file hash stayed `c84101e9a99f0551c829035e9ffec83830cbc71e13df0bde74a7c58de52ea307` in every pristine, mutated, and restored hash output. Each fixture commit reported exactly one changed file (a: one deletion; b: one insertion/one deletion; c: twenty deletions; d: one insertion/one deletion). Each restoration command returned exit 0 and `HEAD is now at 8e59163 checkpoint(r19): retain developed verification evidence for resume; admission pending`; each subsequent master update returned exit 0. The initial `git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD refs/heads/master` returned TIP on both lines; initial `status --short` was empty. Final restored gate stdout binds both revision and branch_tip to TIP.

## Residual

This probe covers only the four requested local corruptions, not every quote, inbound record, source attribution or coordinated alteration of registry/census/snapshots. The external-registry alternative and `--selftest` were not exercised. Gate stdout reported 10 live sibling objects checked and 10 matches; those were the gate's read-only pinned-object reads, not additional host probes. No host/service/package/boot operation, sibling edit, production mutation, or fleet-state write was performed. The only lane write is this report; all fixture edits and Git mutations were confined to the named /tmp clone, whose touched bytes were restored. No tools were installed or updated.

Scope: executed=git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-FxMutAdj-20261021-8; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 remote remove origin; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD refs/heads/master; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 status --short; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master ef3a37aab20eeac24450de9396767dcac984b20c; python3 tools/check-adjacency-anchors.py --revision ef3a37aab20eeac24450de9396767dcac984b20c; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0; python3 tools/check-adjacency-anchors.py --revision abe9f6f43559165f6b0a293a7b8b192f8f9b9ae0; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e; python3 tools/check-adjacency-anchors.py --revision 8dcc6fb7596a6b65d50a24a735809f6ed0dcc89e; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 -c user.name=fixture -c user.email=fixture@local commit -am mutant; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 rev-parse HEAD; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 9df60fd03b41a8ede2373d8cf09be8a0511eaa9e; python3 tools/check-adjacency-anchors.py --revision 9df60fd03b41a8ede2373d8cf09be8a0511eaa9e; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 reset --hard 8e5916360f2dfe7bc4eb4ba144081af555900116; git -C /tmp/tsukuroi-r19-FxMutAdj-20261021-8 update-ref refs/heads/master 8e5916360f2dfe7bc4eb4ba144081af555900116; sha256sum PROVINCE.md corpus/knowledge/adjacency-anchors-r19.json tools/check-adjacency-anchors.py; python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
