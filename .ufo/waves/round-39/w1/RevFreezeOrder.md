VERDICT: supports

Item R-3 — freeze discipline, tsukuroi round 39 (hyaku run 8). Scope: committed history
`0eff65b21bb81195ee06c96a83afbd7a07e52eef..2e1c2a40c13dc52e155d89e72f3fdd560db7399a`
in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Read-only seat: no lane file touched
beyond this report and the receipts dir; no tooling installed or upgraded (git + sha256sum
only); no scratch created (no clones, copies or fixtures — nothing to clean).

## 1. Range and ordering — PASS

`git -C <lane> log --format='%h %cI %s' 0eff65b2..2e1c2a40` → exactly 5 commits (receipt
range-log.txt), oldest→newest:

```
6a08925 2026-10-26T02:47:11-03:00 round-39: freeze C1/C2 counters, libalpm 54d9411 snapshots and pacman.log capture; registry rows
93fddb2 2026-10-26T02:59:31-03:00 round-39: declaration, before receipts and pre-seat controls
49cc53c 2026-10-26T02:59:37-03:00 round-39: C1 storage arm cross-checks the mount table on an absent or empty sysfs root; IN-109 repinned
4078eb2 2026-10-26T02:59:39-03:00 round-39: C2 libalpm transaction order entry; SOURCES S213-S218 (S217 supersedes S210 anchor)
2e1c2a4 2026-10-26T03:00:47-03:00 round-39: author after receipts (C1 PASS at 49cc53c, C2 PASS at 4078eb2; selftest 117/117)
```

Freeze precedes everything else: `git merge-base --is-ancestor 6a08925 <X>` → YES for
93fddb2, 49cc53c, 4078eb2. Dispatch tip is an ancestor of current HEAD
(`394e1ba 2026-10-26T03:01:19-03:00 round-39: w1 spec (70 seats, v2) validated; dispatch
handed to the orchestrator`).

## 2. Freeze adds both counters and frozen inputs, before declaration/receipts/controls/impl — PASS

`git diff-tree -r --name-status 6a08925` (receipt commit-files.txt) adds
`tools/score-storage-hidden-r39.py` (A), `tools/check-transaction-order-r39.py` (A), the
frozen inputs `.ufo/waves/round-39/frozen/src/{SHA256SUMS,FETCH.txt,add.c,hook.c,remove.c,sync.c,trans.c,util.c}`
and `.ufo/waves/round-39/frozen/txcapture/{MANIFEST.sha256,capture-meta.txt,hook-owners.tsv,hook-when.tsv,pacman.log}`
(all A), plus `before/sources-census-start.txt` (A) and SKILL.md (M). The SHA256SUMS is
self-consistent at the freeze: recomputing each of the six source files from
`6a08925:…frozen/src/<f>` reproduces every listed hash (receipt counter-hashes.txt).

`93fddb2` then adds the declaration (`M SCORECARD.md`), both before receipts
(`before/c1-before.jsonl`, `before/c2-before.jsonl`), and the controls
(`controls/controls.jsonl`, `run-controls.sh`, `run.out`, `run.err`, `c1_variant.py`,
`c2-entries/E1…E6`) — after the freeze. Implementation commits touch their claimed
surfaces and no counter: `49cc53c` = M `tools/tsukuroi-census.sh` + M
`corpus/knowledge/adjacency-anchors-r19.json`; `4078eb2` = A
`corpus/knowledge/pacman-transaction-order-r39.md` + M `corpus/SOURCES.md`.

## 3. Counter bytes at tip equal bytes at freeze — PASS

```
6a08925 tools/score-storage-hidden-r39.py  75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973
6a08925 tools/check-transaction-order-r39.py f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e
2e1c2a40 tools/score-storage-hidden-r39.py  75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973
2e1c2a40 tools/check-transaction-order-r39.py f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e
```

Identical, and equal to the declared sha256 prefixes 75a9e8ab… / f1c97836… (blob ids
c502401c… / d46034aa…). The current working tree also matches both hashes.

## 4. Before receipts bind frozen bytes and base revision — PASS

- `.ufo/waves/round-39/before/c1-before.jsonl:1` — `"revision":
  "0eff65b21bb81195ee06c96a83afbd7a07e52eef"`, `"tool_sha256":
  "75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973"` (= frozen bytes),
  `argv … --revision 0eff65b2…`, master at 6a08925 in `lane_branches`; result FAIL with
  hidden_matched 0/2, fixtures_matched 2/5 as declared.
- `.ufo/waves/round-39/before/c2-before.jsonl:1` — `"revision":
  "0eff65b21bb81195ee06c96a83afbd7a07e52eef"`, `"tool_sha256":
  "f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e"` (= frozen bytes),
  `argv … --revision 0eff65b2…`; result FAIL with entry_present false as declared.

## 5. No counter edit after any seat scored — PASS

Path history up to HEAD 394e1ba: `git log -- tools/score-storage-hidden-r39.py` and
`git log -- tools/check-transaction-order-r39.py` each return only 6a08925.
`git log 2e1c2a40..HEAD -- tools/` → empty. Working-tree hashes equal the frozen bytes
(§3). A repo-wide sweep (`git log --all --since='2026-10-26 02:47:11 -0300' -- <both
counters>`) finds only the freeze itself (§6). Controls corroboration: all 12 rows in
`.ufo/waves/round-39/controls/controls.jsonl` carry `counter_sha256` equal to the frozen
bytes (5 C1 rows 75a9e8ab…, 7 C2 rows f1c97836…), K0 rows pinned at revision 6a08925.

## 6. Observation (no defect): three byte-identical anonymous-head staging commits

`--all` surfaces 374003de, 5569c9cc, b5593f8b7: empty subjects, author
2026-10-26T02:34:57-03:00, committed at exactly the freeze second 02:47:11-03:00, each
adding the two counter files (374003d without the frozen src, the other two with the full
freeze set). No branch contains them; none is an ancestor of 6a08925; their counter blobs
are byte-identical to the freeze (c502401c… / d46034aa…). Consistent with jj staging
snapshots taken before the freeze commit; no divergent bytes, and all predate the before
receipts (05:47:20Z+), controls (05:59:31Z) and dispatch (06:01:19Z), so they cannot be
post-scoring edits.

## Residual risk / not done

- I verified freeze discipline from git metadata, receipt headers and frozen checksums; I
  did not rerun either counter or audit its internal logic (other seats' scope).
- "No counter edit after any seat scored" is proven for every ref present in the lane repo
  now and for the working tree; if a scoring seat had exported a mutated counter to a
  location outside this repo and run it, no git history could show that — nothing in the
  lane suggests it, and every in-repo score record binds the frozen sha256.
- The three anonymous heads in §6 are unreferenced and could be garbage-collected; recorded
  here so their existence is not mistaken for a hidden edit.

Receipts: .ufo/waves/round-39/w1/RevFreezeOrder/{range-log.txt,commit-files.txt,counter-hashes.txt,receipt-headers.txt}
