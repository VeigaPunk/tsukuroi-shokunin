# W2SentinelDiff — scope and sentinel findings

## Findings

### High — 16 out-of-scope paths are in the change diff

**Exploit/path:** The requested allowlist is 13 paths; `git diff --name-status 6d76fb20f6ecbc940e5c8fff36c74060c885e161 c052bb7d41ced49aa888817069afd804eccfecf1` shows 29 changed paths. Sixteen additional paths are included in the commit diff, even though none are in the specified allowlist:

- `.ufo/waves/round-36/l1/dev-claim-final.jsonl`
- `.ufo/waves/round-36/l1/dev-r33claim-final.err`
- `.ufo/waves/round-36/l1/dev-r33claim-final.jsonl`
- `.ufo/waves/round-36/l1/dev-r33claim-final2.jsonl`
- `.ufo/waves/round-36/l1/dev-r33claim-final3.jsonl`
- `.ufo/waves/round-36/l1/dev-r33claim-final4.jsonl`
- `.ufo/waves/round-36/l1/gen-w1-spec.py`
- `.ufo/waves/round-36/l1/sens-mutattr.jsonl`
- `.ufo/waves/round-36/w1-dispatch.err`
- `.ufo/waves/round-36/w1-dispatch.json`
- `.ufo/waves/round-36/w1-plan.err`
- `.ufo/waves/round-36/w1-plan.json`
- `.ufo/waves/round-36/w1-registry.json`
- `.ufo/waves/round-36/w1-spec.json`
- `corpus/knowledge/update-safety-note.md`
- `corpus/knowledge/update-safety-v2.md`

**Evidence:** Diff stat is 29 files, +3874/-20. The first 14 paths are round-36 L1/W1 artifacts; the last two are extra corpus append files. The explicit allowed set includes neither category (it allows the specified round-36 lesson/note/registry rows and only the SKILL.md NoUpgrade append).

**Impact:** The integrated change contains material beyond the reviewed scope, including run artifacts and two corpus edits; this weakens provenance and makes the landed diff broader than the authorized review surface.

**Smallest remediation:** Exclude these 16 paths from the change commit, or obtain an explicit scope expansion before treating them as part of the reviewed change. No source remediation was performed by this seat.

### Medium — LOG chronology contains a placeholder, not a timestamp

**Exploit/path:** A reader relying on the LOG integration entry for wave-1 completion chronology cannot verify when the last seat wrapped.

**Evidence:** `LOG.md:1371` says “last seat ExecProbeR36 wrapped 03:5xZ”. The `x` makes this an explicit placeholder, not a timestamp; no exact completion time is supplied there.

**Impact:** The entry asserts 32/32 settlement and integration ordering but does not provide auditable timing for the final seat. The completion assertion itself is not disproved by this; its stated chronology is unsupported.

**Smallest remediation:** Replace the placeholder with the exact recorded event timestamp, or omit the time and qualify the chronology as unknown. Do not infer a value.

## Removed-line and append-only sweep

The named append-only sweep passes: `SCORECARD.md` +76/-0, `LOG.md` +10/-0, `corpus/SOURCES.md` +3/-0; `corpus/QUALITY.md` and root `SHONEN.md` are unchanged. Thus no removed-line finding exists in any required append-only file.

All 20 removed lines are confined to the five modified tools and are replacement edits (not deletions from the append-only records). For completeness, every deletion group is:

- `tools/check-report-receipts.py` (3): inherited-GIT environment comprehension; `env.update({` opener; `})` closer. Replaced by a fixed dict (including `LC_ALL=C`).
- `tools/check-revision-binding.py` (6): two old “Only GIT_* …” security-description lines; the inherited-GIT environment comprehension; the `env.update(...)` opener/body line; its config-closing line; `return env`. Replaced by a fixed dict and updated wording.
- `tools/mutants-btrfs-space-r30.py` (3): old “No git is run…” comment; the `__import__('re').sub(` line; inherited-GIT environment comprehension. Replaced by corrected comment, top-level `re` use, and fixed dict.
- `tools/run-receipt.py` (5): two old env docstring lines; inherited-GIT environment comprehension; config `e.update(...)` line; HOME/XDG update line. Replaced by fixed environment construction and added run-private Git ceiling.
- `tools/score-census-handoff-r32.py` (3): archive subprocess line without `env`; live-view inherited-TSUKUROI filter line; default-revision subprocess line without `env`. Each is replaced by a call using `child_env()`.

No other changed existing file has deletions; all new files are additions. Machine count/path details are in `scope-audit.json`.

## Requested repository checks

- **Round-35 tarball:** tracked at the change commit. `git ls-tree` reports mode `100644`, blob `5ef93e98461758e485a8375da246ec637e8d503e`; object size is 1,934,105 bytes.
- **Untracked files outside round 36:** none at the inspected worktree, whose HEAD is the change commit. `git ls-files --others --exclude-standard` with `.ufo/waves/round-36/**` excluded returned no paths.
- **`resume_continuity_v1`:** no rejection path appears in this assigned diff; the focused search of `tools/` returned no matches (broad hits were historical wave reports). No rejection/zero-mutation case was exercised, and no safety claim is made for the canonical run-logic surface, which is not part of this assigned diff.
- No build, test, lint, or runtime probe was run.

Report: .ufo/waves/round-36/w2/W2SentinelDiff
