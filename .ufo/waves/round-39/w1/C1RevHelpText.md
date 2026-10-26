VERDICT: defect-found
Item C1-18 — census header / TSUKUROI_* override list / usage vs the round-39 mount-table rule at 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82, plus stale absent-root statements in lane docs.

Scope and method (what was checked, how)
- `tools/tsukuroi-census.sh` is byte-identical at 49cc53c7, at lane tip 2e1c2a4, at HEAD 394e1ba, and in the working tree: `git diff --stat 49cc53c..HEAD -- tools/tsukuroi-census.sh` = empty; `diff -q` of a `git show 49cc53c:...` extract against the worktree file = identical; `git status --porcelain` for the five target files lists only `M PROVINCE.md` and `M SKILL.md`. So all census.sh line numbers below are valid at the implementation commit and in the working tree.
- Docs were read in the working tree and swept repo-wide (`grep -rn` over all `*.md` outside `.ufo/`) for "absent … 0/0/0", "means no btrfs", "no btrfs is mounted", "sysfs root" variants.
- Not run (said plainly): I did not execute the census or its selftest, and did not run the frozen counters — this item is text-vs-code consistency; the code was verified by reading, not by execution.

Code baseline (what the round-39 rule actually is at 49cc53c7)
- `tools/tsukuroi-census.sh:1900-1913` (`probe_storage_arm`): the mount table is read only when `fsn -eq 0 && blocked -eq 0`; a listed btrfs mount sets `detail=mounts:btrfs-without-sysfs` (:1910); `cat` failure sets `detail=mounts:unreadable` (:1912). A root with fsid entries (fsn>0) or an already-BLOCKED root never reads the table. Table path `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}` (:460).
- Selftest pins the new readings: `storage-hidden-absent` and `storage-hidden-empty` expect `state=BLOCKED … detail=mounts:btrfs-without-sysfs`, `storage-mounts-unreadable` expects `…detail=mounts:unreadable` (:2971-2988), all with exit 0 HEALTHY (verdict-neutral, as documented at :370-372).

Finding 1 (defect, in scope) — census header contradicts its own round-39 paragraph
- `tools/tsukuroi-census.sh:377-379`: "Known limit, recorded not repaired (C1CritAbsentRoot): an ABSENT root still reads HEALTHY 0/0/0, so a namespace that hides /sys/fs/btrfs while btrfs is mounted gives a false all-clear; a /proc/self/mounts cross-check would change the frozen F06 reading and is next-round work."
- This is false at the implementation commit itself: an absent or fsid-empty root with a listed btrfs mount reads BLOCKED `mounts:btrfs-without-sysfs` (:1900-1910), and the cross-check is not "next-round work" — it is this commit's change, pinned by three selftest cases (:2971-2988). The paragraph carries no supersession marker, and "recorded not repaired" asserts the limit still stands. It directly contradicts the marked supersession in the same header at :361-368 ("An absent TSUKUROI_BTRFS_SYSFS means … (round 38; superseded round 39, R38-ABSENT-ROOT): … only when the mount table …").

Finding 2 (defect, in scope) — census header "reads sysfs only" is stale
- `tools/tsukuroi-census.sh:372`: "Live mode reads sysfs only and creates no files." Since round 39 the storage arm also reads the mount table in live mode (:1901). The "creates no files" half is still true; the "reads sysfs only" half is not, and no marker corrects it.

Finding 3 (stale doc, no supersession anywhere) — corpus/README.md
- `corpus/README.md:300-301` ("### Frontier notice — round 38"): "Known limit carried to the frontier: an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it gives a false all-clear."
- Present-tense behavior claim in the living corpus index. Neither the committed tree (HEAD 394e1ba) nor the working tree supersedes it: `git status --porcelain` shows only PROVINCE.md and SKILL.md modified. This is the one unsuperseded stale statement outside the census header.

Finding 4 (stale at the committed tip; superseded only by uncommitted working-tree edits)
- `SKILL.md:3137` — round-38 table row 1: "The sysfs root is absent. Declared as 'no btrfs mounted' … if btrfs is mounted, record `0/0/0` as an observability finding, never as clearance". Stale at 49cc53c7 (the census itself now reports BLOCKED; the recorded action text no longer matches).
- `PROVINCE.md:216-217` — round-38 promotion "Known limit: an absent sysfs root reads `HEALTHY 0/0/0` … next-round work." Same staleness.
- The working tree carries uncommitted append-only supersession sections for exactly these two: `SKILL.md:3204-3224` ("Storage integrity arm — round 39", whose intro says "Supersedes the first row of the round-38 table above …, which stays as written") and `PROVINCE.md:224-237` ("Round-39 limit closure — R38-ABSENT-ROOT", "its **Known limit** sentence is superseded here, not deleted"). Both correctly state the table rule, the override name/default, and both BLOCKED detail tokens — consistent with the code at :1900-1913. If those appends land, Finding 4 closes; at lane tip 2e1c2a4 as committed, the two statements are unsuperseded.

Clean results (no finding)
- Override list: `tools/tsukuroi-census.sh:405` — "TSUKUROI_PROC_MOUNTS (round 39: the storage arm's mount table; default /proc/self/mounts)" matches the code at :460 exactly (name, default, arm scope).
- usage()/--help (:559-572): describes the STORAGE line generically ("STORAGE (btrfs error counters) lines") and lists no env overrides at all, so nothing in it contradicts the new rule; the exit map and verdict-neutral wording remain accurate.
- `corpus/knowledge/storage-health-r26.md`: no absent-root claim exists (checked every btrfs mention; its round-38 note at :141-145 describes the census arm without stating the superseded rule). Nothing to correct.
- Historical records intentionally left as written, consistent with the lane's dated-record convention: `corpus/lessons/round-38.md:88` (R38-ABSENT-ROOT row with round-38 resolution "Not fixed … next-round work"), `corpus/lessons/round-38-verifier-spotcheck.md:63,174` (round-38 verifier notes and next-round proposal), SCORECARD.md round-38 rows. These describe the round-38 state and are not current-behavior claims.

Proposed append-only corrections (exact text)
1. census header, append directly after :379 (inside the storage paragraph block, before "# Read-only guarantee"):
```
# Round 39 (R38-ABSENT-ROOT closed, commit 49cc53c7): the Known-limit sentence above is superseded,
# not deleted — an ABSENT or fsid-empty root reads HEALTHY 0/0/0 only when the mount table lists no
# btrfs mount (else BLOCKED mounts:btrfs-without-sysfs; an unreadable table BLOCKED mounts:unreadable),
# and live mode reads the mount table too, no longer sysfs only.
```
2. `corpus/README.md`, append to the round-38 Frontier notice (after :301):
```
(Superseded round 39, R38-ABSENT-ROOT, commit `49cc53c7`: an absent or fsid-empty `/sys/fs/btrfs` reads
`HEALTHY 0/0/0` only when the mount table (`TSUKUROI_PROC_MOUNTS`, default `/proc/self/mounts`) lists no
btrfs mount; with a btrfs mount the line is `BLOCKED … detail=mounts:btrfs-without-sysfs` — see
`../PROVINCE.md` "Round-39 limit closure".)
```
3. SKILL.md:3137 and PROVINCE.md:216-217: no new draft needed if the working-tree sections (`SKILL.md:3204-3224`, `PROVINCE.md:224-237`) are committed — they already carry the supersession sentences and match the code. Should they not land, those sections' text is the draft.

Residual risk and verification gaps
- I did not execute the census/selftest or the frozen counters; a behavioral regression in the arm itself is out of this item's scope (other seats cover the counter).
- The working-tree SKILL.md/PROVINCE.md appends are uncommitted; ownership and landing are the L1's call, and this report treats them as in-flight, not landed.
- Docs under `.ufo/` (wave artifacts) were excluded from the sweep by design; lane docs elsewhere are covered by the repo-wide `*.md` grep.
- No tools were installed or upgraded for this item; no host state was touched; the lane was not modified (only the seat report and receipt dir were written).
