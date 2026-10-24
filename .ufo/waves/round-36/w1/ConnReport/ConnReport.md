# ConnReport

Heading time: 02:50:13Z (`date -u +%H:%M:%SZ` immediately before this write).
Seat: `tsukuroi-r36.ConnReport`. Checks file: `connector-checks.md` in this directory.
No tools installed. Pacman not run. Nothing deleted. No production edit. ConnSiblings artifact absent (dependency below).

## Axes

Round-36 declaration axes touched by the move: connector judgment over C1 (operability, fixed-dict child env / `leaking_pairs`) and C2 (depth, journalctl v262 field-filter rejection). Seat axes named for this assignment: scope, connector, misroot.

Not moved: operability and depth ordinals. This seat does not edit the five tools, the probe, or the note.

## Evidence

Full command output is in `connector-checks.md`. Short form:

1. Own `git log --oneline -3` on kumitate, mado, kama. ConnSiblings table missing at 02:47:29Z, 02:48:51Z, and 02:49:32Z (`w1/ConnSiblings/` and `w1/ConnSiblings.md`, both ENOENT). No comparison was possible.
2. `git -C /home/vgpnk/Projects/shokunin status --porcelain`: 32 paths. Substring `round-36` / `round 36`: zero files. Content `tsukuroi`: `.ufo/watchdog.log` (not in the first 512 bytes; includes `launch tsukuroi round=36` at working-tree lines 1086 and 1101) and untracked `.ufo/waves/hyaku/inline-run-20261023.md` line 49 (r35 merit block, not round-36). `.ufo/state/tsukuroi.report-baseline` diff is `22 <empty-sha>` → `36 <empty-sha>`. `printf '' | sha256sum` = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the digest in that file.
3. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/tsukuroi.md` is absent (stat ENOENT). The directory holds other lanes' reports only: `chousa.md`, `kake.md`, `kotodama.md`, `kumitate.md`, `mori.md`.

Sibling window vs labels:

- Kama `f129e27` says "C1/C2 at tip". `git diff HEAD~3 HEAD` has 0 hits for `journalctl`, `leaking_pairs`, `probe-child-env`, `check-revision-binding`, and `GIT_CONFIG_NOSYSTEM`.
- Mado `4f61006` says "six-leg C1 counter + nine-defect C2 counter". Same diff has 0 hits for those C1/C2 surface tokens, and 3 hits for `GIT_CONFIG_NOSYSTEM`. The only non-prompt hit is new `quality/q36-successor-run.sh`: `export HOME="$WORK/home" GIT_CONFIG_NOSYSTEM=1 GIT_OPTIONAL_LOCKS=0` plus an `unset` of `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` / `GIT_COMMON_DIR` / `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_COUNT` / `GIT_CONFIG_PARAMETERS`.
- Mado HEAD has 17 `journalctl` lines (`--user`, hypridle, `mado-tripwire.py` denylist). The v262 rejection sentence count is 0. None of the 17 are in `HEAD~3..HEAD`.
- Kumitate last three commits are round-51 dispatch and attest receipts only. Surface-token diff count 0.

Contradiction, not a score: `git log -3 -S GIT_CONFIG_NOSYSTEM` on kumitate returned round-48/47 commits (`4e4f471`, `ce9aee5`, `8de35e7`), which are not the tip three (`3304a56`, `51f2ecf`, `7d88faa`). Pickaxe `-3` means three matching commits anywhere, not the spot window.

Second contradiction: watchdog content does name `tsukuroi` and `round=36`, and the baseline filename is `tsukuroi.report-baseline`, while no porcelain file contains `round-36` and `tsukuroi.md` is absent. Driver state and a missing report are both true. Collapsing them to "misroot clean" or "misroot dirty" drops one of the two.

## Proposed move

Score sibling overlap and misroot on exact surface tokens inside `git diff HEAD~3 HEAD` (or an equivalent path-limited diff of those three commits). Do not use `git log -3 -S`.

Overlap tokens, any one is a hit: the five basenames `check-revision-binding.py`, `check-report-receipts.py`, `score-census-handoff-r32.py`, `mutants-btrfs-space-r30.py`, `run-receipt.py`; `leaking_pairs`; `probe-child-env-allowlist`; the rejection sentence `cannot be combined with options that limit the journal`.

Non-hits under that rule, kept as separate rows:

- Sibling subjects that merely say C1 or C2 (kama round-31, mado round-28).
- Bare `journalctl` on mado HEAD.
- Mado `quality/q36-successor-run.sh` `GIT_CONFIG_NOSYSTEM=1` line: adjacency (a scrubbed git env already exists next door), not evidence that tsukuroi's five tools already stopped copying the ambient environment, and not a claim to absorb.
- Fleet `.ufo/watchdog.log` `launch tsukuroi round=36` and `.ufo/state/tsukuroi.report-baseline` value `36` plus the empty digest: driver bookkeeping. A misroot hit requires `round-36` in file content, or content that is the probe, one of the five tools, or the C2 note. None of the 32 porcelain paths meet that.

When ConnSiblings' table appears, compare it to the table in `connector-checks.md` under this rule. This seat did not wait for it.

## Risks

- A later ConnSiblings scan with a wider rev range can still find kumitate/kama `GIT_CONFIG_NOSYSTEM` history. That would be a different window, not a contradiction of `HEAD~3`.
- Calling the mado q36 line "not overlap" can hide prior art. It stays in the adjacency row so a C1 design seat can read the `unset` list without treating mado as a shared claim.
- The watchdog added-line sample in this seat was truncated at 40 filter matches (`+492/-0` overall). The two `launch tsukuroi round=36` lines are from the working-tree file, not from a full dump of the diff. Re-grep the diff before calling the log a seat paste.
- The five tool basenames were counted after the first write, at 02:50:57Z: `check-revision-binding.py`, `check-report-receipts.py`, `score-census-handoff-r32.py`, `mutants-btrfs-space-r30.py`, `run-receipt.py`. HEAD `git grep -I -F` excluding `.ufo`, and `git diff --unified=0 HEAD~3 HEAD`, are 0 for every name on kumitate, mado, and kama. `run-receipt.py` did not false-hit.

## Verification

Already run, this seat, read-only:

- `git -C <sibling> log -3 --format='%h %ci %s'` and `--name-only` for the three repos.
- `git grep -I -F -e <token> HEAD` counts in the table above.
- `git diff --unified=0 HEAD~3 HEAD` piped to counts; mado `GIT_CONFIG_NOSYSTEM` hunks inspected.
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` plus per-path first-512 and whole-file substring checks.
- `git diff` of `SCORECARD.md`, `tsukuroi.report-baseline`, and the other `*.report-baseline` files.
- `stat` / `ls` of `.../.ufo/reports/round-36/tsukuroi.md` (ENOENT) and of the ConnSiblings paths (ENOENT).
- `printf '' | sha256sum`.

Not run: no probe, no child-env before/after, no journalctl live matrix, no build. An unrun check has not passed.

L1 can replay the same read-only commands. Do not delete the fleet porcelain paths.
