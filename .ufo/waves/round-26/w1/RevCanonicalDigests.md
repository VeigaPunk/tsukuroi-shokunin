# Routed defect 6 check — canonical protocol digests (RevCanonicalDigests)

Verdict: holds. All seven sha256 values declared in the SCORECARD round-26 section equal the sha256sum of the current bytes of the seven files under `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/`, the kimi-shokunin checkout HEAD is `e737d2ea97f6b0198503e077676c3f2ea07974a9` with a clean worktree, the declaration commit `b13e991fb96972b423b868ba122187f75357368c` is timestamped 2026-10-22T10:41:01-03:00 (13:41:01Z), and the only files under `.ufo/waves/round-26/` in that commit are the two under `capture/`.

1. All seven digests match. [obs] `sha256sum` over the seven files returned exactly the values declared at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:880-886`:
   - `skills/shokunin/SKILL.md` → `34be71885eb8bedaf16bd27e5e62741d95500904c696ef436349ea00b7477475`
   - `skills/shokunin/protocol/PROTOCOL.md` → `622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0`
   - `skills/shokunin/protocol/PROTOCOL-APPENDIX.md` → `90fc91af3c7467a1e131a9164717f81c3ee7ddff3e7bd357cb5e5f9aad322e30`
   - `skills/shokunin/protocol/MISSION.md` → `38a8c15ab1220d4c0fad165729dce681ce2d58a6e54f807e4ceb8364ece94071`
   - `skills/shokunin/protocol/AXES.md` → `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993`
   - `skills/shokunin/protocol/CORPUS.md` → `b6ed4476b0d1a5a3176ce728e4eb44997bddfa6dfb9fdb2f1a15e81d3f0821bf`
   - `skills/shokunin/protocol/LEARNING.md` → `3ff7ab4da9f3ce448477872af62c8d74ad0671e0d5bfc29a4ca8945bd8865964`

2. kimi-shokunin checkout identity matches. [obs] `git -C /home/vgpnk/Projects/kimi-shokunin rev-parse HEAD` → `e737d2ea97f6b0198503e077676c3f2ea07974a9`; `git log -1` shows that commit at the tip of `main` (committed 2026-10-19T21:21:25-03:00).

3. The hashed bytes are the committed bytes. [obs] `git -C /home/vgpnk/Projects/kimi-shokunin status --porcelain` output is empty (exit 0), so the working tree matches the index and HEAD for the whole checkout, including all seven files hashed in finding 1. The digests therefore describe the state at `e737d2ea`, which is what the SCORECARD claims ("checkout at `e737d2ea…`", SCORECARD.md:878).

4. Declaration commit time. [obs] `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show -s --format=%cI b13e991fb96972b423b868ba122187f75357368c` → `2026-10-22T10:41:01-03:00`, i.e. 2026-10-22T13:41:01Z after timezone conversion. [inf] This is consistent with the SCORECARD's stated sequence: branch tip at dispatch 13:33:23Z, protocol files read 13:34Z–13:37Z, then the declaration committed at 13:41:01Z (SCORECARD.md:876 and :878).

5. No round-26 wave files other than capture/ existed at the declaration commit. [obs] `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only b13e991fb96972b423b868ba122187f75357368c -- .ufo/waves/round-26/` returns exactly:
   - `.ufo/waves/round-26/capture/capture.sh`
   - `.ufo/waves/round-26/capture/capture.txt`

   Nothing else under that prefix existed in commit `b13e991`, so no entry, source snapshot, checker or wave-1 report predates the declaration commit. [obs] The frozen capture also matches the path named in the assignment.

Residual risk and verification gaps:
- [inf] The digests verify the bytes now, at checkout `e737d2ea` with a clean worktree; they cannot prove what the bytes were at the moment of the 13:34Z–13:37Z read. Since the worktree is clean at that commit and the commit predates any wave-1 file, this is the strongest available form of the check and no gap in the declaration remains.
- [unk] None. All four assignment items were exercised and returned positive evidence.

Scope: read=SCORECARD.md:874-908 and grep hits at :880-886; kimi-shokunin skills tree listing; wrote=.ufo/waves/round-26/w1/RevCanonicalDigests.md; executed=sha256sum of the seven files; git rev-parse HEAD, status --porcelain, ls-files -s, log -1 on kimi-shokunin; git show -s --format=%cI and ls-tree -r --name-only on tsukuroi-shokunin (all read-only)
Model: zai/glm-5.3-flash
Installs: none
