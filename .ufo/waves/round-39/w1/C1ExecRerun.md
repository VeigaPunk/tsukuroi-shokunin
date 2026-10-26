VERDICT: supports

# C1ExecRerun — item C1-1 (C1 after re-run)

Seat: C1ExecRerun (leaf). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Host: linux 7.2.11-arch1-1, python3 3.14.
Scratch: `/fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun` (created, `TMPDIR` exported there, removed after receipts were copied here).
No tool installs or upgrades were made (none needed).

## 1. Counter identity — three-way equal

| Check | Command | Observed |
|---|---|---|
| declared hash | `sha256sum tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  tools/score-storage-hidden-r39.py` |
| frozen-commit bytes | `git show 6a08925daa30767809eb13bb4b01448ff954d46a:tools/score-storage-hidden-r39.py \| sha256sum` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973  -` |
| same hash at the two run revisions and the current tip | per-revision `git show <rev>:tools/score-storage-hidden-r39.py \| sha256sum` | `75a9e8ab…f973` at 49cc53c, 2e1c2a4, 394e1ba (`host-and-blobs.txt`) |

Both requested equalities hold: the declared digest, the frozen commit's bytes and the worktree bytes are the same file. The author receipt records the same digest (`c1-after-49cc53c.jsonl` head: `"tool_sha256": "75a9e8ab…f973", "tool_revision": "6a08925daa30767809eb13bb4b01448ff954d46a"`), and the declaration row carries it verbatim (`SCORECARD.md:2220`).

Adjacent blob fact (not required, recorded for the L1): the **census** is byte-identical at 49cc53c, 2e1c2a4 and 394e1ba (`e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`), and differs at the counter-freeze commit 6a08925 (`6a675a4e…c33d`). That is the expected shape: the counter is frozen before C1's census edit and reads the census at `--revision` (`tools/score-storage-hidden-r39.py:184-189`).

## 2. Predicate fields — author receipt vs both re-runs

Commands (exact):

```
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun
python3 tools/score-storage-hidden-r39.py --revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 \
    --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun/s
python3 tools/score-storage-hidden-r39.py --revision 2e1c2a40c13dc52e155d89e72f3fdd560db7399a \
    --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecRerun/s2
```

| receipt | revision | hidden_matched | views_matched | fixtures_matched | live_match | six_planes_all | result | exit |
|---|---|---|---|---|---|---|---|---|
| author `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl` | 49cc53c | 2 | 3 | 5 | 1 | 1 | PASS | 0 |
| re-run `…/w1/C1ExecRerun/c1-rerun-49cc53c.jsonl` | 49cc53c | 2 | 3 | 5 | 1 | 1 | PASS | 0 |
| re-run `…/w1/C1ExecRerun/c1-rerun-2e1c2a4.jsonl` | 2e1c2a4 | 2 | 3 | 5 | 1 | 1 | PASS | 0 |

Both re-runs exited 0 with empty stderr (33.93 s and 33.33 s wall). The receipt's `predicate` string is character-identical in all three (`hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1 and six_planes_all == 1`) and equals the declaration sentence and the counter's own verdict expression (`tools/score-storage-hidden-r39.py:265-269`; declaration `SCORECARD.md:2220` column 6).

The base-0eff65b FAIL reading (`hidden 0/2, fixtures 2/5`, `…/before/c1-before.jsonl`) was **not** re-run by this seat (outside C1-1).

## 3. Leg-by-leg comparison with the author receipt

11 legs in every receipt; leg sets are identical.

| leg | author 49cc53c | re-run 49cc53c | re-run 2e1c2a4 | expected+got byte-identical to author |
|---|---|---|---|---|
| H1-hidden-empty | match | match | match | yes |
| H2-hidden-absent | match | match | match | yes |
| V0 zero | match | match | match | no — random tree (see below) |
| V1 nonzero | match | match | match | no — random tree |
| V2 any | match | match | match | no — random tree |
| F1-absent-root-no-btrfs-mounted | match | match | match | yes |
| F2-absent-root-btrfs-mounted | match | match | match | yes |
| F3-absent-root-mounts-unreadable | match | match | match | yes |
| F4-populated-root-no-btrfs-mounted | match | match | match | yes |
| F5-empty-root-btrfs-mounted | match | match | match | yes |
| L live | match | match | match | yes |

8 of 11 legs reproduce the author's `expected` and `got` exactly — including both hidden legs and all five override fixtures, whose expected lines are fixed literals. The three view legs differ only because the view tree is drawn from `os.urandom` (`tools/score-storage-hidden-r39.py:213`) and the seeds differ: author `333cb54a7b9ab13153fbd698084b584e`, re-run@49cc53c `08726c231fa1fa61ca39a514f4ba965d`, re-run@2e1c2a4 `a1326a3d06e04836a3318fb5bdf8b543`.

That difference is by design, not drift: replaying each recorded seed through the counter's own generator and model (`draw_view` :91, `model_from_spec` :110) reproduces each receipt's `expected` tuple exactly in **9/9** view legs, e.g. for the author seed `[('HEALTHY',3,6,0), ('DEGRADED',2,3,6), ('DEGRADED',3,8,17)]` — identical to `c1-after-49cc53c.jsonl`; for `08726c23…` `[('HEALTHY',3,7,0), ('DEGRADED',1,1,4), ('DEGRADED',3,7,16)]`; for `a1326a3d…` `[('HEALTHY',2,4,0), ('DEGRADED',1,3,4), ('DEGRADED',1,2,2)]`, each equal to the corresponding re-run receipt. The expected tuple is therefore computed from the generated tree, not from the census output, and every view leg still matched the census in all three runs.

One non-predicate field differs and is explained: `branch_tip` is `4078eb23…` in the author receipt and `394e1ba4…` in both re-runs (the tip at run time; `tools/score-storage-hidden-r39.py:267`). The census and counter blobs are identical at 49cc53c, 2e1c2a4 and 394e1ba, so the tip field does not enter the score.

## 4. Ancillary evidence that the legs are grounded, not a host read

- Host ground: 4 btrfs mounts (`/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`) and one fsid dir `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e` (`host-and-blobs.txt`). So the hidden legs' `BLOCKED … mounts:btrfs-without-sysfs` is reachable only if the child really lost the root, and the live leg's `HEALTHY filesystems=1 devices=1 nonzero=0` equals the host's one fsid.
- Hidden legs (H1 over `/sys/fs/btrfs`, H2 over `/sys/fs`) reported `BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` while the live leg on the same host reported `HEALTHY 1/1/0` in the same run — direct evidence the tmpfs shadow took effect per child.
- The view data never crosses as a host path: the child is `unshare -rm` and the tree spec is written to the child's stdin (`tools/score-storage-hidden-r39.py:197-198`), with the builder writing only under `/sys/fs/btrfs` (:81). No bind source and no argv carries a view.
- Census implementation matches the claimed ordering: the mount table is consulted only when `fsn == 0` and nothing is blocked (`tools/tsukuroi-census.sh:1903-1914` at 49cc53c); an unreadable table yields `mounts:unreadable` (:1911-1913). A root with fsid entries therefore never reads the table, as claimed.
- Counter write surface is scratch-only: `--scratch` base and `run-*` under it (:180-182), removed at :280-282. This seat's runs created nothing in the lane; its only lane writes are this report and `.ufo/waves/round-39/w1/C1ExecRerun/`.
- `census_exit` is 2 in **every** leg of all three receipts, including the HEALTHY live leg. Cause isolated: under the counter's child env (`PATH=/usr/bin:/bin`, private HOME/TMPDIR) `PLANE systemd: BLOCKED (systemctl --user unusable rc=1 … $DBUS_SESSION_BUS_ADDRESS …)`, and the worst-plane exit map gives 2 (`childenv-census.txt`; exit-map `tools/tsukuroi-census.sh:3094`). The live host census, with a session bus, exits 1 (DEGRADED). So exit 2 is a systemd-plane artefact of the child env, not a STORAGE signal, and it is uniform across author and re-run receipts.
- Census selftest: 4 new round-39 storage cases are present at 49cc53c (`storage-hidden-absent` :2974, `storage-hidden-empty` :2979, `storage-mounts-unreadable` :2984, `storage-mounted-populated` :2989), matching the "4 selftest cases" claim. The 117/117 result is read from `.ufo/waves/round-39/after/selftest-49cc53c.txt`; this seat did not re-run the selftest.

## 5. Finding outside the C1-1 predicate — IN-109 companion cells are stale (defect, documentation)

The C1 claim also asserts "IN-109 anchor repinned". True in the JSON registry, false in the companion Markdown:

- JSON: `corpus/knowledge/adjacency-anchors-r19.json` IN-109 `"found_line": 2447`, and `grep -n "kernel ring class counts" tools/tsukuroi-census.sh` gives `2447:  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \`. Consistent, and the note names the round-39 repin.
- Markdown: `corpus/knowledge/adjacency-anchors-r19.md:204` still has the `… | DRIFTED | 2277 | check 'degraded: …` cell and `:231` still says `| line 2277 |`. The md is unchanged since `3846bd1` (round 33), where 2277 was still correct; the JSON was then repinned at `199beb9` → 2346, `02eeed0` → 2425 and `49cc53c` → 2447, each equal to the live census line at that commit (measured: census line 2277/2346/2425/2447 at those four commits). The published cell is therefore 69 lines behind as of round 35 and 170 lines behind after round 39.
- The gate cannot see it: `tools/check-adjacency-anchors.py:759-761` only asserts `inbound_id in knowledge_text` (presence), not the numeric cell. `python3 tools/check-adjacency-anchors.py --revision 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` returns `"status": "PASS"`, `"findings": []`, exit 0 (`adjacency-gate-49cc53c.json`).
- Precedent that the lane treats the md as live: `corpus/lessons/round-32.md:53` — "`found_line` and the companion Markdown cells were updated in place (`corpus/knowledge/adjacency-anchors-r19.json`, `.md`)".

This does not touch C1's counter predicate or the census behaviour; it is a claim-side record defect the L1 should route. Exact repair text if the L1 wants it: in `corpus/knowledge/adjacency-anchors-r19.md:204` replace the sixth cell `2277` with `2447`, and in `:231` replace `| line 2277 |` with `| line 2447 |` (the JSON note already carries the round-39 sentence).

## 6. What this seat did not do

- Did not run the counter at base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`; the "before" reading is the author's receipt, unverified here.
- Did not re-run `tools/tsukuroi-census.sh --selftest` (117/117 is quoted from the author receipt only).
- Ran exactly one gate, read-only (`check-adjacency-anchors`), because §5 needed its verdict; no other build/lint/test/gate was executed, per the wave rule.
- No lane commit/add/checkout, no host change, no sudo, no pacman, no mount outside the counter's private `unshare -rm` namespaces.
- Observation, not a claim of this seat: `git status --porcelain` currently shows `M PROVINCE.md` and `M SKILL.md` in the working tree; neither was touched by this seat.

## 7. Receipts kept

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/C1ExecRerun/`

| file | what |
|---|---|
| `c1-rerun-49cc53c.jsonl` | full counter JSON at 49cc53c (`sha256 59b4aa887f7dc4eae8e9b95e684b28d8f4c65788ebbde51f68d1bea8cd5dab65`) |
| `c1-rerun-2e1c2a4.jsonl` | full counter JSON at 2e1c2a4 (`sha256 789b0afb9510db5a69de4ae343708f6b17a8ca378bfd5c2828afe8f9a7dccd23`) |
| `SHA256SUMS` | digests of the two receipts |
| `runlog.md` | exact commands, exits, wall times, blob pins |
| `host-and-blobs.txt` | host btrfs mounts/fsids and per-revision counter+census sha256 |
| `childenv-census.txt` | census planes under the counter's child env (systemd BLOCKED → exit 2) |
| `adjacency-gate-49cc53c.json` | gate PASS, `findings: []` at 49cc53c |
