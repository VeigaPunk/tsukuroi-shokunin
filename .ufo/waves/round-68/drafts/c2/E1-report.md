2026-11-03T22:36:10Z

# E1Probe — C2 gate build and red-before proof (round 68, wave w1)

Seat: E1Probe (L2, tsukuroi lane, hyaku run 15). Lane base: 42400ec6. All paths absolute.

## 1. Draft tool

```
$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/drafts/c2/check-knowledge-refs-r68.py
d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5  .../drafts/c2/check-knowledge-refs-r68.py
rc=0
```

Size 23984 bytes. Written to the draft path only; the lane's `tools/` is untouched
(the integration copy is the L1's move).

Implementation, per the frozen rules and `drafts/c2/S2Scout-gate-rules.md`
(read; its revision binding / fence / column-zero / exit-code / JSON-shape rules
match this build with no conflict):

- `_revision` bootstrap copied from `tools/check-knowledge-header.py`:
  `sys.dont_write_bytecode = True`, `_lane_flag`/`_default_lane`/`_unresolved`,
  `sys.path.insert(0, str(LANE / "tools"))`, `import _revision`, `git()` with
  `_revision.clean_env()`, `read_blob()` via `cat-file -t` + `show`, `notes_at()`
  via `ls-tree -r --name-only <sha> corpus/knowledge`.
- Scope: every `corpus/knowledge/*.md` at the bound revision.
- Operative line: the LAST column-0 `source:` line outside a fenced block; the
  fence state machine is byte-for-byte the header gate's (`FENCE`, opening run,
  closing run needs same char, `len(run) >= len(fence)`, no info string).
- Ids: `\bS\d{3,}\b` on that one line only (`ID`).
- Registry: `corpus/SOURCES.md` at the same revision; id set from rows matching
  `^\|\s*(S\d{3,})\s*\|` (the id cell is exactly `S` plus digits; `| S138 extra |`
  registers nothing). A registry with no id row is CANNOT_EVALUATE (E-PATH-MISSING).
- Finding: `KNOWLEDGE-REF-DANGLING`, one per (note, id); the payload finding also
  carries the dangling id under `ref`.
- CLI: mutually exclusive required `--revision` / `--selftest`, `--lane`
  (default nearest ancestor with `tools/_revision.py`), `--branch` (default
  master). Exit 0 PASS / 1 finding / 2 CANNOT_EVALUATE; JSON on stdout.

## 2. Selftest

```
$ S=/fast/scratch/hyaku/tsukuroi-r68/E1Probe
$ TMPDIR="$S" python3 .../drafts/c2/check-knowledge-refs-r68.py --selftest
2026-11-03T22:34:39Z
{"selftest": {"cases": 19, "failures": [], "passed": 19, "status": "PASS"}}
rc=0
```

Receipt: `.ufo/waves/round-68/probes/c2-selftest.txt`.

Cases a-h of the item, all present and passing, plus 11 more:

| case | exit | asserts |
|---|---|---|
| all-ids-registered (a) | 0 | 4 registry ids, 2 refs, 0 findings |
| unregistered-id (b) | 1 | `ref=S999`, 1 finding |
| second-dangling-id (c) | 1 | `refs={S997,S998}`, 2 findings |
| fenced-id-is-example (d) | 0 | `source: S999` only inside ``` fence |
| mid-line-id-is-prose (e) | 0 | body `S999` not on a `source:` line |
| no-source-line-no-finding (f) | 0 | `sourced_count=0`, no finding |
| four-digit-id-counts (g) | 1 | `ref=S0001` (distinct from a registered S001) |
| spaced-registry-cell (h) | 0 | `\|   S185   \|` registers S185 |
| last-source-line-operative (i) | 0 | later `source: S138` supersedes `S999` |
| registry-cell-must-be-exact (j) | 1 | `\| S138 extra \|` registers nothing |
| registry-absent (k) | 2 | E-PATH-MISSING |
| revision-symbolic-rejected | 2 | E-REVISION-INVALID (`HEAD`) |
| revision-unlanded | 2 | E-REVISION-NOT-LANDED |
| branch-missing | 2 | E-BRANCH-MISSING |
| branch-invalid | 2 | E-BRANCH-INVALID (`HEAD`) |
| cli-no-mode / cli-both-modes / cli-bogus-flag / cli-branch-without-value | 2 | E-CLI |

The fixture repo is `tempfile.mkdtemp(prefix="knowledge-refs-gate-")` (under
`TMPDIR=$S`), `git init -b master`, per-case `reset --hard` + `clean -qfd` to a
fixed base commit so every case is isolated; removed in `finally`.

## 3. Live base (sandbox clone @42400ec6)

```
$ git clone --shared -q /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/lane
$ git -C $S/lane checkout -q 42400ec6
clone_rc=0 ; HEAD=42400ec65c45709ade07a92ed72d1277e3478bbb
$ python3 $S/lane/tools/check-knowledge-refs-r68.py --revision 42400ec6 --lane $S/lane
{"status": "PASS", "revision": "42400ec65c45709ade07a92ed72d1277e3478bbb",
 "branch_tip": "3f6edcc9792d892890d7e25b8bf4327bc7d5e6b0",
 "origin_tip": "3f6edcc9792d892890d7e25b8bf4327bc7d5e6b0",
 "note_count": 85, "sourced_count": 85, "ref_count": 247, "dangling_count": 0,
 "registry_id_count": 285, "finding_count": 0, "findings": []}
rc=0
```

Receipt: `.ufo/waves/round-68/probes/c2-live-base.json` (full single-line JSON;
the excerpt above is abridged, the receipt is not).

The sandbox copy is byte-identical to the draft:
```
$ sha256sum <draft> $S/lane/tools/check-knowledge-refs-r68.py
d4390b7a...7858d5  <draft>
d4390b7a...7858d5  $S/lane/tools/check-knowledge-refs-r68.py
```

## 4. Red-before (the round-66 gap)

Sandbox identity guard printed `git -C $S/lane rev-parse --show-toplevel` =
`/fast/scratch/hyaku/tsukuroi-r68/E1Probe/lane` (`guard=ok`) before any mutation.
Throwaway branch `r68-red-before` at 42400ec6; master left at
3f6edcc9792d892890d7e25b8bf4327bc7d5e6b0. One note added:
`corpus/knowledge/s999-fixture-r68.md` with the three header keys and
`source: S999 — fixture (never a registry row)` (line 3). Commit made with
`GIT_AUTHOR_NAME/EMAIL` + `GIT_COMMITTER_NAME/EMAIL` inline
(`r68-sandbox <sandbox@invalid>`); `fixture_sha=a0ba15cce8075ff8600201dca79451733bcf3c22`.

(i) header gate at the fixture revision:
```
$ python3 tools/check-knowledge-header.py --revision a0ba15cce807 --branch r68-red-before --lane $S/lane
{"branch": "r68-red-before", "branch_tip": "a0ba15cce807...", "clean_count": 86,
 "complete_count": 86, "finding_count": 0, "findings": [], "note_count": 86, ...}
rc=0
```

(ii) new reference gate at the same revision:
```
$ python3 $S/lane/tools/check-knowledge-refs-r68.py --revision a0ba15cce807 --branch r68-red-before --lane $S/lane
{"branch": "r68-red-before", "dangling_count": 1, "finding_count": 1,
 "findings": [{"detail": "source: line 3 cites S999, absent from corpus/SOURCES.md at the revision",
               "id": "KNOWLEDGE-REF-DANGLING", "ref": "S999",
               "site": "corpus/knowledge/s999-fixture-r68.md"}],
 "note_count": 86, "sourced_count": 86, ...}
rc=1
```

Control (isolation): the same fixture revision against the default branch is
refused as unlanded — `E-REVISION-NOT-LANDED`, `rc=2` — so the fixture commit
never entered master inside the sandbox either.

Receipt: `.ufo/waves/round-68/probes/c2-red-before.txt`.

The round-66 gap is reproduced and closed: header gate green (rc 0) on the same
bytes where the reference gate is red (rc 1) on `S999`.

## 5. Deviations from the item's step-3 rules, with reasons

1. **Red-before binding uses `--branch r68-red-before`.** `_revision.bind`
   requires the revision to be an ancestor of the named branch; the fixture
   commit deliberately sits on a throwaway branch and is *not* merged into
   master (the item says throwaway branch). Defaulting to master would refuse
   it (rc 2, shown as the control). No rule about the gate's behaviour changes.
2. **Receipts start with a UTC timestamp.** The selftest command was run as
   `{ date -u; python3 ... --selftest; echo rc=$?; } > c2-selftest.txt` with
   `TMPDIR=$S`, per the evidence-discipline rule and step 3's "use the scratch
   dir passed as TMPDIR". The tool's own output is unmodified.
3. **Payload carries ref-specific counters** (`sourced_count`, `ref_count`,
   `dangling_count`, `registry_id_count`) instead of the header gate's
   `complete_count`/`clean_count`, and each DANGLING finding also carries
   `ref`. The header-specific counters have no meaning for a reference gate;
   status/revision/branch/`branch_tip`/`origin_tip`/`note_count`/`finding_count`/
   `scope`/`findings` keep the header gate's shape.
4. **Empty registry is CANNOT_EVALUATE, not a pass.** The frozen rules define
   the id set but not this corner; a registry with zero `| S<digits> |` rows is
   unreadable input, so the gate fails closed (E-PATH-MISSING) rather than
   flagging every id.
5. **`S2Scout-gate-rules.md` was absent at the first check (19:31) and present
   at 19:34.** It was read before the selftest run and reconciled; it agrees
   with the rules coded, including that the fence and column-zero logic must be
   inherited from the header gate rather than re-derived.

No tool was installed or upgraded (no channel used); no pacman transaction, no
sudo, no service action. Scratch `/fast/scratch/hyaku/tsukuroi-r68/E1Probe` is
removed after the receipts above were written into the wave directory.
