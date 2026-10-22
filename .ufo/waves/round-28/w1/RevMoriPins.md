# RevMoriPins — round 28 wave 1: C1 counter pin verification vs mori sibling

Verdict: holds — all three pins in the round-28 counter match the mori sibling's pinned blob and the committed lane snapshot; the pinned file did change in mori after the pin, but the pin anchors a historical commit so the cross-check stays valid.

## Findings

1. Pin constants at the attack revision [obs]. `git show f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0:tools/check-adjacency-overlap.py` lines 55–57:
   - `PIN_COMMIT = 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'`
   - `PIN_PATH = 'corpus/knowledge/userspace-oom-killers-r26.md'`
   - `PIN_SHA256 = 'a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d'`

2. Live sibling blob matches PIN_SHA256 [obs]. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -p ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:corpus/knowledge/userspace-oom-killers-r26.md | sha256sum` → `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`. Exit 0; object readable.

3. Committed lane snapshot is byte-identical [obs]. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0:.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md | sha256sum` → `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`. Snapshot dir `SNAP_DIR = '.ufo/waves/round-27/siblings/mori/'` (line 54) contains exactly this one file at the revision.

4. Mori current tip [obs]. HEAD is detached at `ac696ad3037c3071584df60d84b5bf0af9818dd6` (commit 2026-10-22 15:57:40 -0300, "round-28: wave-2 corrections (reader wording per S146/S150/S152, C2 blindness disclosure, freeze hash), wave-2 reports so far"); `master` points at the same commit (`git branch --points-at HEAD` → `* (no branch)`, `  master`). Worktree dirty only in `corpus/lessons/round-28.md` plus untracked `.scratch/` — irrelevant to the pin since `cat-file` reads the object store.

5. Mori DID change the pinned file after the pin [obs]. `git log ef9dbee136d6ed2ef98687f5cb0c0a16506a5155..HEAD -- corpus/knowledge/userspace-oom-killers-r26.md` lists commit `79ecf58` (2026-10-22 13:05:50 -0300, "round-27: routed D2-D4 (S117 description, S124 restored + S133, oomd wording), R3 SKILL rows + S134-S136, S137, lesson round-27, QUALITY 80-82, row-identity check, entry dead-seat correlation, wave-1 reports"). Diff stat: 36 insertions, 9 deletions; HEAD blob sha256 is now `94efb7cf6da5e3d1e8ec19ec83135da1d09d76b073f2d68dd166c6b3f31ee93d` ≠ PIN_SHA256.

6. Drift does not break the counter [inf]. `git merge-base --is-ancestor ef9dbee… HEAD` → exit 0, so the pin commit is reachable history (safe from GC) and `cat-file -p PIN_COMMIT:PIN_PATH` still returns the pinned bytes (finding 2). The counter's live cross-check (lines 165–170) runs `git(sib_repo, 'cat-file', '-p', '%s:%s' % (PIN_COMMIT, spath))` — it reads the pinned commit's blob, never HEAD — and compares to the snapshot; mismatch would raise `sibling-bytes-differ`. All three sources agree today, so honest rows evaluate to `sibling-verified`.

7. Sibling resolution is the real mori repo [obs]. `--siblings-root` defaults to `/home/vgpnk/Projects/shokunin` (line 367); `sib_repo = os.path.join(siblings_root, 'mori-shokunin')` (line 130) = `/home/vgpnk/Projects/shokunin/mori-shokunin`, gated on `.git` existing (line 165). Verified that repo is the one queried in findings 2 and 4–6.

8. Residual risk / unknowns [unk]. The pin is only as stable as mori's history: a force-push rewriting `ef9dbee` out of reachability would make `cat-file` fail and flip `sibling-verified` to `sibling-mismatch`/`sibling-unavailable` for every honest row. Current state gives no evidence of that (ancestor check passed). Whether `--siblings-root` can be repointed at a forged mori repo is exercised by the counter's own selftest (`sibling cross-check mismatch` case near line 345–356), outside this seat's scope.

Scope: read=git objects in tsukuroi-shokunin (rev f8e3a8f2) and mori-shokunin (pins, tip, log); wrote=.ufo/waves/round-28/w1/RevMoriPins.md; executed=git show/ls-tree/cat-file/sha256sum/rev-parse/log/merge-base/branch/status/symbolic-ref (all read-only)
Model: not exposed
Installs: none
