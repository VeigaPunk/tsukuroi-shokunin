VERDICT: defect-found
SCOPE CHECK (the C1-K3 kill rule) PASSES: GR1 and GR3 section hashes at IMPL are byte-identical to base; only GR2's bytes changed inside the row extents; no `## ` line exists inside any row at either revision; the three admission marks are absent at IMPL. The defect is in the CONTENT of one changed GR2 hunk (the suspend-path attribution), reported below as an advisory for the counted GR2 seats and the L1 — it is not a scope failure.

## 1. Section hashes at base and at IMPL (the frozen counter, `--section-hash`)

Counter: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py`.
Frozen digest verified: worktree and `git show 77e9e2b2:tools/check-scrub-admission-r47.py` both
`sha256 e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b` (matches the declared
frozen sha256). Base copy differs (`5577bb9f110ab61b0eec0adfa838dd2948abdb5baf9acbc2ada50a05cb348956`) —
the counter is new in round 47, added by `3629c46a`.

Command (base):
`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py --revision 916019057147d7e9ba6b137647b2cee26decf4b8 --section-hash` -> rc 0
```json
{"entry": "corpus/knowledge/btrfs-scrub-grounding-r45.md", "problems": [], "revision": "916019057147d7e9ba6b137647b2cee26decf4b8", "section_sha256": {"GR1": "fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8", "GR2": "4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da", "GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"}, "structural_ok": 1}
```

Command (IMPL):
`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` -> rc 0
```json
{"entry": "corpus/knowledge/btrfs-scrub-grounding-r45.md", "problems": [], "revision": "77e9e2b2e96b85d8f048ae2087e246a542b71611", "section_sha256": {"GR1": "fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8", "GR2": "909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2", "GR3": "43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c"}, "structural_ok": 1}
```

| row | base hash | IMPL hash | equal to base? |
|---|---|---|---|
| GR1 | fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 | fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 | YES |
| GR2 | 4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da | 909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2 | no (amended, as declared) |
| GR3 | 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c | 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c | YES |

Kill rule "GR1/GR3 section hashes equal to base" holds. Independently reproduced (my own extent
computation over `git show <rev>:corpus/knowledge/btrfs-scrub-grounding-r45.md`, sha256 of the
joined extent lines): GR1 and GR3 extent bytes are *identical strings* base vs IMPL
(GR1 2242 bytes both, GR3 3291 bytes both); GR2 grew 4983 -> 5105 bytes.

## 2. Diff stat

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 916019057147d7e9ba6b137647b2cee26decf4b8 77e9e2b2e96b85d8f048ae2087e246a542b71611 -- corpus/knowledge/btrfs-scrub-grounding-r45.md`
```
 corpus/knowledge/btrfs-scrub-grounding-r45.md | 29 +++++++++++++++++----------
 1 file changed, 18 insertions(+), 11 deletions(-)
```
Repo-wide the same range touches 13 files (+1062/-14); the entry is the only corpus/knowledge file.

## 3. Every changed hunk, classified against the row extents

Row extents (1-based, inclusive start, exclusive end of the next expected header), computed from
the counter's own rule (`## GR<n>` .. next expected header; any other `## ` inside fails closed):

| row | base extent | IMPL extent |
|---|---|---|
| GR1 | 14..54 (next header `## GR2` at 55) | 14..54 |
| GR2 | 55..137 (next header `## GR3` at 138) | 55..140 (next header `## GR3` at 141) |
| GR3 | 138..183 (next header `## How this changes OS triage` at 184) | 141..186 (next header at 187) |

`git diff -U0` yields exactly FOUR hunks (deletions 8+3+0+0 = 11, insertions 10+2+2+4 = 18 — the
counts reconcile with the stat, so no change exists outside these hunks):

**H1 — GR2 statement, ordering fix (base 60-67 -> IMPL 60-69), inside GR2's extent.**
Old: "Inside `btrfs_scrub_dev`, a call with `is_dev_replace` false is refused with `-EINPROGRESS`
while `btrfs_dev_replace_is_ongoing` is true ... Both refusals come after the function has
allocated its scrub context and taken the scrub workers ... and after three device checks that also
answer first ...".
New: "Inside `btrfs_scrub_dev`, after a filesystem-closing check that returns `-EAGAIN` first
(`btrfs_fs_closing`), the function allocates its scrub context and takes the scrub workers
(`scrub_setup_ctx`, `scrub_workers_get`), whose errors return first; then three device checks
answer ... Only after those checks is a call with `is_dev_replace` false refused with `-EINPROGRESS` ...".
Fidelity check against the pinned snapshot S242 (`.ufo/waves/round-44/frozen/src/scrub.c`, sha256
f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8): `btrfs_fs_closing` at
scrub.c:3094 with `return -EAGAIN;` at :3095 precedes `scrub_setup_ctx` (:3109) and
`scrub_workers_get` (:3114); the device checks answer -ENODEV (:3123), -EROFS (:3133), -EIO
(:3139/:3142); the -EINPROGRESS test `dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))`
is at :3147-3153, i.e. after all three device checks. The new ordering matches the pinned source and
the correction the round-46 residual critic demanded.

**H2 — GR2 statement, suspend sentence narrowed (base 71-73 -> IMPL 73-74), inside GR2's extent.**
Old: "A suspended replace requests the cancellation of its scrub (the suspend path calls
`btrfs_scrub_cancel`); once that scrub has returned and cleared the device's scrub context, the query
answers `-ENOTCONN`".
New: "When the unmount suspend path runs, it calls `btrfs_scrub_cancel`; once the scrub returns and
clears its context, the progress query returns `-ENOTCONN`".
See §6 — the new wording's attribution does not match the pinned source, unlike H1 which does.

**H3 — GR2 quotes, two lines added (IMPL 91-92), inside GR2's extent.**
```
**Quote.** `S242` scrub.c:3094: "if (btrfs_fs_closing(fs_info))"
**Quote.** `S242` scrub.c:3095: "return -EAGAIN;"
```
Both verified verbatim against S242 scrub.c lines 3094 and 3095. GR2 quote count 26 -> 28; the
counter's quote leg at IMPL: GR1 12/12, GR2 28/28, GR3 12/12, `quotes_ok 3`, `bad: []`.

**H4 — appended bullet in `## Limits` (IMPL 217-220), OUTSIDE every row extent.**
```
- GR2's filesystem-closing `-EAGAIN` check (scrub.c:3094-3095) and the unmount-only wording of the suspend-path
  cancellation were added at the round-47 integration after the counted round-46 residual critic read `partly`
  (`.ufo/waves/round-46/r1/V46ResCritGR2.md`); the amended row was re-read by the counted round-47 seats
  (`tools/check-scrub-admission-r47.py`, wave `w1` of `.ufo/waves/round-47/`).
```
Precision on the item's phrasing: this bullet is NOT inside a row extent. At IMPL the `## Limits`
heading is at line 200 and `## Gate status — round 45` at 222, so lines 217-220 sit in `## Limits`,
past GR3's extent end (186). That placement is precisely why GR3's hash is unchanged by this hunk.
The cited round-46 residual file exists at IMPL and does read `partly`
(`git show 77e9e2b2:.ufo/waves/round-46/r1/V46ResCritGR2.md`, first line `ROW GR2 VERDICT: partly`,
second `SECTION SHA256: 4bf28bcf…` = the base GR2 hash).

## 4. Confirmations requested

- **No `## ` line inside a row.** At both revisions, for all three rows, the set of `## ` lines
  strictly inside each extent is empty (`inner_##=[]`); the counter reports `structural_ok 1`,
  `problems: []` at base and at IMPL. F1 fail-closed behaviour is therefore not triggered.
- **Marks absent at IMPL.** `python3 …/check-scrub-admission-r47.py --revision 77e9e2b2…` (full run)
  returns `"marks": {"entry": false, "readme": false, "skill": false}, "marks_ok": 0`, verdict FAIL,
  `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0` (rc 1; verdicts are 0 because no
  round-47 dispatch/results/report is committed yet). Direct greps at IMPL confirm absence in the
  three marked files: `## Gate status — round 47` is not in `corpus/knowledge/btrfs-scrub-grounding-r45.md`,
  `## Scrub grounding — round 47 admission` is not in `SKILL.md`, `admitted round 47` is not in
  `corpus/README.md`. The same strings appear only in `tools/check-scrub-admission-r47.py`,
  `.ufo/waves/round-47/controls/battery.py` (control fixture), `SCORECARD.md` and the round-46
  `ConnFrontier.md` — i.e. in the counter, in a control, and in prose, never in the marked files.
- **Nothing else in the entry changed.** The `## How this changes OS triage` section is byte-identical
  base vs IMPL; the `## QUALITY check` section is byte-identical base vs IMPL (diff of the two
  slices empty); `SKILL.md` and `corpus/README.md` are byte-identical base vs IMPL
  (`git diff --numstat` on both paths prints nothing).

## 5. Counter state at IMPL (context for the L1, not a verdict)

Full counter at IMPL: `verdict FAIL`, `structural_ok 1`, `quotes_ok 3`, `verdicts_ok 0`, `marks_ok 0`,
`waves_seen: []` (no `*-dispatch.json` is committed under `.ufo/waves/round-47/` at IMPL — the tree
holds only `before/`, `controls/`, `frozen/`), `bound_on_current` 0 for all three rows, every seat
detail `dispatched 0 times`. So the counts can only rise once the wave commits its dispatch,
results and the seats' report files.

## 6. ADVISORY DEFECT (content, not scope): GR2's suspend sentence attributes the `btrfs_scrub_cancel` call to the wrong function

The narrowed GR2 sentence at IMPL lines 73-74 reads "When the unmount suspend path runs, it calls
`btrfs_scrub_cancel`". The pinned snapshot S247
(`.ufo/waves/round-45/frozen/src/dev-replace.c`, sha256 f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a)
shows otherwise:

- `grep -n btrfs_scrub_cancel` on S247 returns exactly two call sites: **:1111** and **:1144**.
- :1144 sits inside `btrfs_dev_replace_cancel` (function header `int btrfs_dev_replace_cancel(struct
  btrfs_fs_info *fs_info)` at dev-replace.c:1085, closing brace at :1169), in the
  `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` branch (:1126), guarded by the comment at :1143
  `/* Scrub for replace must not be running in suspended state */`.
- The unmount suspend path itself is a different function: `void btrfs_dev_replace_suspend_for_unmount(struct
  btrfs_fs_info *fs_info)` at dev-replace.c:1171..1195. Its body only switches the replace state to
  `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` (:1185-1186) and logs `suspending dev_replace for unmount`
  (:1189); `sed -n '1171,1195p' … | grep scrub` prints nothing — it contains no scrub call at all.

So under the pinned evidence the sentence "the unmount suspend path runs, it calls `btrfs_scrub_cancel`"
names the wrong function: the call is in the *cancel* path for an already-suspended replace. A
sympathetic reading (the unmount-suspend scenario ends in a cancel of the suspended replace, which
then cancels the scrub) makes the sentence defensible, but it is not what the pinned file says, and
the row's own quoted lines (dev-replace.c:1143, :1144) sit inside `btrfs_dev_replace_cancel`.

The counter cannot catch this: its entry-side leg (`quote_legs`) only checks that each `**Quote.**`
line matches its cited snapshot line (K22), not that the prose around a quote attributes the call to
the enclosing function. GR2's quote leg is 28/28 at IMPL.

Origin: the wording was prescribed by the round-46 residual critic, `.ufo/waves/round-46/r1/V46ResCritGR2.md`:
"the assertion that a suspended replace 'requests the cancellation' is supported at dev-replace.c:1143-1144
only for the unmount suspend path in that code context … Narrow to 'When the unmount suspend path runs, it
calls `btrfs_scrub_cancel`; once the scrub returns and clears its context, the progress query returns
`-ENOTCONN`.'". The amendment adopted that sentence verbatim; the attribution problem is inherited from
the critic's phrasing, which itself mis-locates :1143-1144.

Why it matters for C1: the counted GR2 seats must bind `holds` on these bytes. A critic reading the
pinned source will see `btrfs_scrub_cancel` in the cancel function and may read `partly` again, which
holds admission of all three rows (the predicate needs `verdicts_ok 3`). Possible one-line fix if the
L1 re-amends before the counted seats bind — attribution by function rather than by scenario:

> "When a replace that is already suspended (a replace suspended by an unmount, dev-replace.c:1185-1186)
> is cancelled, the cancel path calls `btrfs_scrub_cancel` (dev-replace.c:1143-1144); once the scrub
> returns and clears its context, the progress query returns `-ENOTCONN`."

(That text is a proposal only. I did not modify any tracked lane file; I write no draft into the
entry.)

## 7. Second advisory observation, outside this item's scope: SKILL.md still carries the pre-amendment GR2 ordering

`SKILL.md` is byte-identical base vs IMPL, so its parallel GR2 summary was not updated with the
amendment. `SKILL.md:4304` still says "inside `btrfs_scrub_dev` three device checks answer first —
unknown or missing device `-ENODEV`, non-writeable device on a writing call `-EROFS`, device outside
the metadata or the replace target `-EIO` (S242 scrub.c:3120-3143) — then any call is refused
`-EINPROGRESS` while the device carries a scrub context (:3147) and a non-replace call while
`btrfs_dev_replace_is_ongoing`", with no mention of the leading `-EAGAIN` on a closing filesystem, and
still says "for a suspended replace, whose scrub the suspend path cancels (S247 dev-replace.c:1143-1144)"
(the pre-amendment wording). The amended entry row (H1) now leads with the fs-closing `-EAGAIN`.
The SKILL.md round-47 mark (`## Scrub grounding — round 47 admission`) is written post-wave by the L1;
if it is added next to that stale row without amending it, the two surfaces will disagree on GR2's
ordering. Flagged for the L1's integration decision; not acted on by me.

## 8. Method, limits, and what I did not do

- All commands were read-only against the lane; no git mutation, no `git add/commit/checkout/reset`,
  no jj, no package/service/unit/sysfs action, no `btrfs` command, no `sudo`, no write to
  `~/.local/bin` or any PATH directory, no file written at the fleet root. The lane working tree
  shows only pre-existing modifications/untracked files from other seats (e.g.
  ` M .ufo/waves/round-47/w1.ready.partial`, `?? .ufo/waves/round-47/w1/R47*.md`) — I created none
  of them; my only writes are this report and my receipt directory.
- Scratch used: `/fast/scratch/hyaku/tsukuroi-r47/C1ExecEntryDiff/` (removed on exit); no fixture
  repo was needed, since the item is a read-only comparison of two committed revisions and no
  mutation of the entry was attempted.
- The "marks absent at IMPL" statement is about the committed IMPL tree only; uncommitted worktree
  state was not treated as evidence.
- I did not run the census selftest, the battery controls, or the C2 side — out of this item's scope.
- No tool was installed or upgraded for this item, so the tooling-authorization record is empty
  (no pacman/uv/npx/npm/cargo transaction was made).

## 9. Receipts (my seat directory, `.ufo/waves/round-47/w1/C1ExecEntryDiff/`)

- `entry-base-91601905.md` — the entry file at base (`git show 91601905:corpus/knowledge/btrfs-scrub-grounding-r45.md`).
- `entry-impl-77e9e2b2.md` — the entry file at IMPL.
- `entry-diff-base-to-impl.patch` — the `git diff` of the entry, base -> IMPL.
- `entry-diff-U0.patch` — the same diff at `-U0` (the four hunks quoted in §3).
- `section-hash-base.json`, `section-hash-impl.json` — the two `--section-hash` outputs quoted in §1.
- `counter-impl-full.json` — the full counter run at IMPL quoted in §5.
