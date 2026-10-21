# FxOut006 — OUT-006 (kumitate) outbound anchor, end-to-end re-verification

Lane: tsukuroi-shokunin, round-19 FALSIFY wave, revision under attack 8e5916360f2dfe7bc4eb4ba144081af555900116. Leaf seat, read-only; the only file written is this report.

## Attack

OUT-006 is the kumitate leg of claim C1 (adjacency, axis 8): tsukuroi PROVINCE.md's pointer to `../kumitate-shokunin/PROVINCE.md:3-6` is republished as a portable anchor with heading + verbatim <=25-word quote + pinned sibling commit + blob sha256. It is falsifiable at every byte level: the heading may not exist, the quote may not be verbatim at `quote_line`, the sha256 may not match the snapshot or the pinned git blob, the pin may be absent or unreachable in the live sibling repo, the original pointer or the appended republication may be missing, and the gate may not actually enforce what the section claims.

## Method

Working-copy blobs first proven identical to the revision's blobs, so working-copy reads are evidence for 8e59163:

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
git show 8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/adjacency-anchors-r19.json | sha256sum   # cd310de18873... == working copy
git show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md | sha256sum                                   # 2114d8cf6f53... == working copy
git show 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md | sha256sum  # fcd69667a102...
```

Per step:
1. Read snapshot `.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md` lines 1-12 (read tool).
2. `python3 -c` read-only compare of registry record OUT-006 (`outbound` array) against snapshot bytes: full-line equality of quote at line 3, substring check (gate semantics), `len(quote.split())`, heading equality. (First attempt errored on wrong top-level key `anchors`; corrected to `outbound`.)
3. `sha256sum` of snapshot (2229 bytes); independent cross-check `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-tree 1770305fae20826b39905a8251ddeca6b4957ac4 -- PROVINCE.md` -> blob `f5cf0fbcd81cfefcbf6d9936c232824acce9830b`, then `git cat-file blob f5cf0fbc... | sha256sum`.
4. `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -e 1770305fae20826b39905a8251ddeca6b4957ac4^{commit}`; `git rev-parse --abbrev-ref HEAD` + `git rev-parse HEAD`; reachability via read-only history walk `git log --format=%H | grep -qx <pin>`.
5. Grep of tsukuroi `PROVINCE.md` for the pointer, the section heading, and any sha256/40-hex commit text; read of PROVINCE.md:104-132; read of gate `tools/check-adjacency-anchors.py` (constants :20-33, `_outbound_publication` :224-227, `_live_object_hash` :241-253, evaluate :261-460); live-sibling hash `sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md`.
6. Gate run as named: `python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116` (cwd = lane; script is read-only on the `--revision` path — only `--selftest` writes, into a `tempfile.TemporaryDirectory`, tools/check-adjacency-anchors.py:742).

No installs were needed; no tool was installed or upgraded (operator directive: nothing to record).

## Verdict

**CONFIRM — C1, anchor OUT-006.** Per-step verdicts:

| Step | Verdict |
|---|---|
| 1 heading | CONFIRM — `# kumitate-shokunin — Province` is snapshot line 1 and equals the record's `heading`; gate heading-section check satisfied (line 1 precedes quote_line 3, no intervening ATX heading). |
| 2 verbatim quote @ line 3, <=25 words | CONFIRM — record quote is byte-identical (full-line `==`, not just gate's substring) to snapshot line 3: `**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`; 12 words <= 25 (gate max 25, ANCHOR-QUOTE-TOO-LONG). |
| 3 blob sha256 | CONFIRM — snapshot file sha256 `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f` == record == `git cat-file blob` of the pin's PROVINCE.md blob `f5cf0fbc...`; independent of the capture. |
| 4 pin existence/reachability | CONFIRM — pin `1770305fae20826b39905a8251ddeca6b4957ac4` exists in the live kumitate repo and is reachable from the current tip: branch label `HEAD` (detached), tip `753446a829edda519c75777ce95888443f51fa94`. **The pin is behind tip** (stated as allowed): the walk found the pin in HEAD's history. |
| 5 pointer + appended section + gate/reader semantics | CONFIRM — original pointer `../kumitate-shokunin/PROVINCE.md:3-6` retained at PROVINCE.md:50 (ADJ-05 row) at the revision; appended section `## Adjacent — portable ownership anchors (round 19)` at PROVINCE.md:108 carries OUT-006 at :126 with heading, verbatim quote, commit `1770305fae20`, proposition. Gate treats the section as operative: republication of id+quote after that exact section heading is a hard PASS/FAIL condition (ANCHOR-UNPUBLISHED). A reader following only the old line range is **not misled today**: live kumitate PROVINCE.md is byte-identical to the pin (same sha256, 2229 bytes), so lines 3-6 read exactly as pinned. |

Gate run (executed, real output): `{"status": "PASS", "revision": "8e59163...", "branch": "master", "branch_tip": "2fd1e6768f187be8c5e837af6286c3736953fcff", "counts": {"outbound_total": 10, "outbound_portable": 10, "inbound_total": 114, "inbound_classified": 114, "inbound_by_class": {"RESOLVES": 97, "DRIFTED": 17}, "inbound_by_scope": {"operative": 25, "historical": 89}, "live_object_checked": 10, "live_object_match": 10}, "findings": []}` — matches C1's declared 10/114/97/17/25/89 exactly, zero findings.

## Evidence

- Record: `corpus/knowledge/adjacency-anchors-r19.json:74-88` (OUT-006: pointer :75, commit `1770305fae20826b39905a8251ddeca6b4957ac4` :78, sha256 `fcd69667...` :79, snapshot path :80, heading :81, quote + `quote_line: 3` :82-83). Working-copy blob == revision blob (`cd310de18873...`).
- Snapshot: `.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md:1` (heading), `:3` (quote line); sha256 `fcd69667...`, 2229 bytes; snapshot blob at revision 8e59163 hashes identically.
- Pinned blob cross-check: `git -C kumitate-shokunin ls-tree 1770305fae... -- PROVINCE.md` -> `100644 blob f5cf0fbcd81cfefcbf6d9936c232824acce9830b`; `cat-file blob f5cf0fbc... | sha256sum` -> `fcd69667a102...`.
- Sibling state: pin exists (`cat-file -e ...^{commit}` -> exists); tip `753446a829edda519c75777ce95888443f51fa94`, detached HEAD; pin found in `git log --format=%H` of tip -> reachable, pin behind tip; live `kumitate-shokunin/PROVINCE.md` sha256 `fcd69667...` == pin (no drift of the cited bytes since the pin).
- PROVINCE.md (revision blob `2114d8cf6f53...` == working copy): pointer at `:50` (ADJ-05 row, inside the unchanged `## Adjacent — finding-to-owner handoffs` table); section heading `:108`; prose "The pinned commit and blob sha256 identify the bytes" `:114`; OUT-006 row `:126` (heading + quote + `@ 1770305fae20` + proposition); Limits paragraph `:129-132` ("pins are stale by design once a sibling commits again ... Recheck: python3 tools/check-adjacency-anchors.py --revision <REV>").
- Gate: `tools/check-adjacency-anchors.py:26` (`PROVINCE_SECTION` constant equals the appended heading), `:224-227` (`_outbound_publication`: a line after the section heading must contain id AND quote), `:241-253` (`_live_object_hash` = `git show <pin>:<path>` in `<siblings_root>/<sibling>-shokunin`), `:392-395` (ANCHOR-SNAPSHOT-TAMPERED on sha mismatch), `:406-410` (ANCHOR-HEADING-MISSING), `:414-419` (quote must be exact substring of snapshot line), `:421-424` (ANCHOR-QUOTE-TOO-LONG, max 25), `:427-437` (pointer must appear in PROVINCE.md at --revision; ANCHOR-UNPUBLISHED if not republished), `:742` (writes confined to selftest temp dir).

## Residual

1. **Placement nuance (not a mismatch):** the appended PROVINCE table row (:126) prints the 12-hex commit `1770305fae20`, not the 40-hex commit, and the blob sha256 hex value appears nowhere in PROVINCE.md — only the prose assertion at :114. The full commit and the sha256 are carried by the registry record (json:78-79) and enforced by the gate (snapshot sha + live-object checks). A reader holding only PROVINCE.md cannot recompute the sha256 without the registry/gate; C1's "+ blob sha256" attribute is satisfied via registry + gate, not by the PROVINCE row itself.
2. The gate's `live_object_match` proves the *pin* resolves in the live sibling repo with the registered bytes (`git show <pin>:<path>`), not that the sibling's *current tip* still carries those bytes. Current-byte non-drift is covered only by my direct `sha256sum` of the live working file (equal today); nothing gate-enforced prevents future sibling edits from silently diverging lines 3-6 — the section's own Limits paragraph (:129-131) states this ("stale by design") and mandates re-reading the live declaration before any handoff.
3. Reachability was proven against kumitate's current HEAD (detached) by full-history walk; no other branch/ref state was enumerated, and `git merge-base` was avoided as it is outside the seat's allowed read-only verb list.
4. Quote fidelity is enforced by the gate as substring-of-line, not full-line equality; I additionally verified full-line equality for OUT-006, so the stronger property holds here even though the gate would accept a longer line.
5. `--selftest` was not run (out of scope for this anchor; the revision-path gate run above is the exercised evidence).

Scope: executed=sha256sum <snapshot> && wc -c <snapshot> ; git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -e 1770305fae20826b39905a8251ddeca6b4957ac4^{commit} ; git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse --abbrev-ref HEAD && git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse HEAD ; git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-tree 1770305fae20826b39905a8251ddeca6b4957ac4 -- PROVINCE.md ; sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md && wc -c /home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md ; git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin log --format=%H | grep -qx 1770305fae20826b39905a8251ddeca6b4957ac4 && echo REACHABLE_FROM_HEAD || echo NOT_REACHABLE_FROM_HEAD ; git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file blob f5cf0fbcd81cfefcbf6d9936c232824acce9830b | sha256sum ; git show 8e5916360f2dfe7bc4eb4ba144081af555900116:{corpus/knowledge/adjacency-anchors-r19.json,PROVINCE.md,.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md} | sha256sum (with working-copy sha256sum of registry and PROVINCE.md) ; python3 -c read-only registry-vs-snapshot field/verbatim/word-count compare (one failed attempt on wrong JSON key, one corrected run) ; wc -l tools/check-adjacency-anchors.py corpus/knowledge/adjacency-anchors-r19.json PROVINCE.md ; cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116
