# RevLeftoverIncident — round-24 inherited-state check

Verdict: the inherited round-24 state is clean — all three flagged files are byte-identical to their master blobs and the tree is git-clean, both untracked probe files are gone from disk, but four round-24 entries carry mtimes 4m23s after the 10:01Z cutoff with master-identical content, which reads as a post-cutoff restore/repair pass, not open-ended seat writing [obs + inf].

Axes (godspeed): correctness of the equality evidence; saturation of the mtime sweep; faithful obs/inf/unk separation.

## Findings

1. The three flagged files equal their blobs at master. `git diff --quiet master -- <path>` returned SAME (exit 0) for all of `.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py`, `.ufo/waves/round-24/w1/RevGateSchema.md` and `.ufo/waves/round-24/w1/ScribeGateEntry/pause-lift-gate-r24.json`, and `git diff --quiet HEAD -- .ufo/waves/round-24/w1` returned SAME for the whole w1 tree. Independent sha256 cross-check matches on all three: worktree `d2dbe8468848b095c3cdca1184e47079070cfa56a6ad1a3d11cbc9ee2329dfa2` == `git cat-file blob master:…check-pause-gate.py`; worktree `30bc8a7970efdc648135623211f85acef704b4bbae49e66d3aa34a0d36453f0c` == master blob of RevGateSchema.md; worktree `ee09f300c5fc84114865dfc9a4ae8399a614049b1a5c984d4df2e9125970896b` == master blob of pause-lift-gate-r24.json. All three are tracked (`git ls-files` lists them). HEAD == master == 6c580b155840c8750a7bb5f14dcb8e48913d0073 ("round-25: declaration, host capture and census before", committed 2026-10-22T07:08:51-03:00), so master equality and HEAD equality coincide here. [obs]

2. The worktree is clean except expected round-25 dispatch files. `git status --porcelain` lists exactly four entries, all untracked and all round-25: `.ufo/waves/round-25/w1-dispatch-result.txt`, `.ufo/waves/round-25/w1-dispatch.json`, `.ufo/waves/round-25/w1-spec.json`, `.ufo/waves/round-25/w1/`. There are no staged or modified entries, so the entire tracked tree matches HEAD and therefore master. No round-24 path appears in status. [obs]

3. The two untracked probe files are gone. Glob over `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/**` and over the whole lane repo (`**`) finds no `p2-measured-probe.txt` and no `zero-probes-measured.txt`. Porcelain shows no `??` entry for either name, and this silence is meaningful rather than ignore-masked: `git check-ignore -v` matches only `__pycache__/` (`.gitignore:2`) and matches neither probe filename, so an existing untracked file with either name would have appeared in status. [obs]

4. Post-cutoff mtimes exist, but only on the repaired set. Host timezone is -03:00; the cutoff 2026-10-22T10:01:00Z is epoch 1792663260 (verified with `date -u -d '2026-10-22 10:01:00' +%s`). Exactly four entries under `.ufo/waves/round-24/` are newer, all at 2026-10-22T10:05:22Z (epoch 1792663522.751–753, i.e. +4m23s after cutoff): `w1/ScribeGateEntry/pause-lift-gate-r24.json`, the `w1/ScribeGateEntry/` directory, `w1/RevGateSchema.md`, and `w1/ExecPauseGateChecker/check-pause-gate.py`. The next-newest entry is `w1/ExecPauseGateChecker/__pycache__/check-pause-gate.cpython-314.pyc` at 09:50:13Z, 10m47s before the cutoff; everything else is older still. The sweep covered all 483 entries of the round-24 tree (sorted by epoch, newest 20 inspected, plus the threshold filter), so coverage is saturated. [obs]

5. The post-cutoff writes look like a restore, not novel seat work. All three rewritten files carry byte-identical content to master (finding 1) and status is clean (finding 2). Timeline: the last commit touching the three files is 44e9542 at 2026-10-22T06:39:03-03:00 ("round-24: retain both target misses, … settle 74 seats"), the rewrite landed at 10:05:22Z between that settlement and the round-25 declaration commit at 10:08:51Z, and the in-place rewrite signature holds — the parent dirs `w1` (09:26:46Z) and `ExecPauseGateChecker` (09:48:44Z) kept pre-cutoff mtimes while `ScribeGateEntry` (10:05:22Z) moved. This is consistent with a single repair pass rewriting exactly those paths to master content before the round-25 declaration. [inf] Who or what performed the 10:05:22Z rewrite, and whether a round-24 seat process was still alive at that moment, is unknowable from mtimes and git metadata alone. [unk]

6. Harmless residue, no action needed. `w1/ExecPauseGateChecker/__pycache__/check-pause-gate.cpython-314.pyc` (09:50:13Z, pre-cutoff) is an untracked but ignored leftover of a checker run; it has no status or content impact. [obs]

## Residual risk and verification gaps

- mtime is metadata: a post-cutoff writer producing master-identical bytes is indistinguishable from a deliberate restore by this survey; content equality makes the distinction immaterial to wave-1 safety, but the writer question stays open. [unk]
- The survey used mtime only per assignment; ctime/atime were not swept, so a rename-into-place after cutoff would only be visible via directory mtimes (checked for the four parents; `round-24` itself is 09:38:56Z, `w1` 09:26:46Z). [obs]
- No sudo was used and none was needed; no config, service, or mount state was touched.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/** (483 entries, mtimes+contents), git metadata of the lane repo (status, diff vs master/HEAD, ls-files, rev-parse, cat-file, log, check-ignore), host clock; wrote=.ufo/waves/round-25/w1/RevLeftoverIncident.md; executed=git status/diff/ls-files/rev-parse/cat-file/log/check-ignore (read-only), stat, find, sha256sum, date, glob (read-only)
Model: zai/glm-5.3-flash
Installs: none
