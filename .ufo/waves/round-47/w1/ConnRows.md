VERDICT: defect-found

# Item F-9. Cross-Row Consistency Read (ConnRows)

## 1. Declared Axes
- **Axis 1 (Depth):** Accurate grounding of Linux v7.2.11 btrfs scrub/dev-replace call paths, check orderings, and ioctl contracts.
- **Axis 2 (C1 Admission):** Satisfying `tools/check-scrub-admission-r47.py` predicate `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`.
- **Axis 3 (Consistency):** Substrate, knowledge corpus (`btrfs-scrub-grounding-r45.md`, `btrfs-scrub-record-r44.md`), and operational reference (`SKILL.md`) synchronization across amendment revisions.
- **Axis 4 (Host Guard & Non-Harm):** Strictly read-only lane and host execution; receipts isolated to `.ufo/waves/round-47/w1/ConnRows/`.

---

## 2. Evidence & Scope of Reading
- **Impl Freeze Revision:** `77e9e2b2e96b85d8f048ae2087e246a542b71611` (base `916019057147d7e9ba6b137647b2cee26decf4b8`).
- **Files Evaluated:**
  1. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/btrfs-scrub-grounding-r45.md` (amended `## GR2`, `## How this changes OS triage`, `## Limits`).
  2. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/btrfs-scrub-record-r44.md` (SR7, SR8, SR9, `## How this changes OS triage`, `## Limits`, `## Round-45 grounding and gate status`, `## Round-45 qualification — the stop outcome`).
  3. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md` (all scrub sections: `## Scrub-record census arm — round 44`, `## Scrub record — round 44 rows`, `## Scrub grounding — round 45 rows`, `### Correction — the round-44 scrub rows`, `## Scrub record — round 44 status note`, and Gate Registry tables).
  4. Pinned sources: `S242` (`scrub.c`), `S243` (`sysfs.c`), `S247` (`dev-replace.c`), `S248` (`systemd.kill.xml`).
  5. Counter: `tools/check-scrub-admission-r47.py` (sha256 `e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b`).

---

## 3. Surface-by-Surface Consistency Findings

### Surface A: Amended GR2 vs `## How this changes OS triage` (`btrfs-scrub-grounding-r45.md:187-199`)
- **Command Run:**
  ```bash
  python3 -c '
  with open("corpus/knowledge/btrfs-scrub-grounding-r45.md") as f:
      lines = f.readlines()
  print("".join(lines[186:199]))
  '
  ```
- **Finding:** **none** (no contradictions).
  - Triage bullet 2 (`:192-195`) addresses `EINPROGRESS`:
    > "`EINPROGRESS` from a scrub start does not by itself say why: the kernel returns it when that device already carries a scrub context (a scrub, or a replace copying from it) and when a non-replace scrub is asked for while a replace is started or suspended (GR2). Read the unprivileged `exclusive_operation` and `replace_target` sysfs files first; starting or cancelling either operation stays operator-owned."
  - This matches amended GR2 lines 66–69: `btrfs_dev_replace_is_ongoing` holds for both started and suspended states (unmount suspend included), and device context attachment triggers `EINPROGRESS`. Triage focuses solely on differentiating the causes of `EINPROGRESS` via unprivileged sysfs reading; it makes no claim about `-EAGAIN` or device check orderings, maintaining complete consistency.

### Surface B: Amended GR2 vs `## Limits` (`btrfs-scrub-grounding-r45.md:200-221`)
- **Command Run:**
  ```bash
  python3 -c '
  with open("corpus/knowledge/btrfs-scrub-grounding-r45.md") as f:
      lines = f.readlines()
  print("".join(lines[199:221]))
  '
  ```
- **Finding:** **defect-found** (omission / defect at `corpus/knowledge/btrfs-scrub-grounding-r45.md:213-216`).
  - `btrfs-scrub-grounding-r45.md:213-216` states:
    > "Three registrations of older rows stay as they are: S242's declared ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337) do not list `scrub.c:3081`, 3123, 3133 or 3139; S243's (72-74, 2021-2049, 2113) do not list `sysfs.c:1288` or 2015; S237's do not list `scrub.c:421`."
  - **The Defect:** GR2 now quotes `S242 scrub.c:3094` and `scrub.c:3095` (the round-47 amendment lines: `btrfs_fs_closing` check and `return -EAGAIN;`), plus earlier additions `scrub.c:3109` (`scrub_setup_ctx`), `scrub.c:3114` (`scrub_workers_get`), and `scrub.c:3138` (`test_bit(BTRFS_DEV_STATE_IN_FS_METADATA)`). All of these lines lie outside S242's declared ranges `(1365-1385, 3140-3162, 3215-3226, 3321-3337)`. The text at line 214 lists `scrub.c:3081, 3123, 3133 or 3139` but fails to list `3094, 3095` (the exact amendment quotes), `3109`, `3114`, or `3138`.
  - While line 215 notes that file digests cover whole snapshots, line 214 remains an incomplete, defective catalogue of out-of-range quotes.
  - Regarding line 212 ("and no seat has read that last narrowing"): this describes the round-45/46 history and is appropriately superseded by lines 217–220 documenting the round-47 amendment and re-read.

### Surface C: Amended GR2 vs Round-44 Entry (`corpus/knowledge/btrfs-scrub-record-r44.md`)
- **Command Run:**
  ```bash
  python3 -c '
  with open("corpus/knowledge/btrfs-scrub-record-r44.md") as f:
      for i, l in enumerate(f, 1):
          if any(k in l for k in ["GR1", "GR2", "GR3", "Round-45"]):
              print(f"{i}: {l.strip()}")
  '
  ```
- **Finding:** **none** (no contradictions).
  - SR7 (`:17-29`): Notes that `btrfs_scrub_dev` attaches context after refusal checks and before work (`:3159`), clears at `:3222`, and serves both scrub and replace. The replace caller was marked `[inference]` at `:21-23` and grounded by GR2 at `:159-161`.
  - SR8 (`:56-90`): `memparse` size suffixes marked `[inference]` at `:62-63` are grounded by GR1 at `:159-161`.
  - SR9 (`:91-133`): `systemctl stop` signals and timeout marked `[inference]` at `:150-151` are grounded by GR3 at `:159-161` and qualified by `## Round-45 qualification — the stop outcome` (`:163-173`).
  - Gate status (`:155-159`): Accurately records that SR7–SR9 failed their round-44 depth gate (`verdicts_ok 0`) and remain pending until bound by counted non-author reads. Admitting GR1–GR3 fulfills their grounding role without contradicting SR7–SR9's gate status.

### Surface D: `SKILL.md` Scrub Section — Stale Lines When Rows Admit
When GR1–GR3 admit under `tools/check-scrub-admission-r47.py`, the following lines in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md` become stale:

1. **`SKILL.md:4288-4290`**:
   > "Gate status (round 45): the depth gate FAILED — `verdicts_ok` 0, no counted verdict bound (`SCORECARD.md` "Round 45 — measured outcome"). GR1-GR3 are pending, not admitted: read the rows below as source-checked statements that no counted seat has bound, and GR2 as corrected after two `partly` reads that no counted seat has re-read."
   - **Why Stale:** Upon admission of GR1–GR3 in round 47, asserting that GR1–GR3 are pending, not admitted, and that no counted seat has bound them is obsolete and false.

2. **`SKILL.md:4304` (Table row for GR2 in `## Scrub grounding — round 45 rows`)**:
   > "| a scrub start answers `EINPROGRESS` on a filesystem where no scrub was started, or a privileged `scrub status` shows the source device of a replace as running | a device replace copies through the scrub code: `btrfs_scrub_dev(fs_info, src_device->devid, …, false, true)` at start (S247 dev-replace.c:701-703) and on continuation (:1265-1268); inside `btrfs_scrub_dev` three device checks answer first — unknown or missing device `-ENODEV`, non-writeable device on a writing call `-EROFS`, device outside the metadata or the replace target `-EIO` (S242 scrub.c:3120-3143) — then any call is refused `-EINPROGRESS` while the device carries a scrub context (:3147) and a non-replace call while `btrfs_dev_replace_is_ongoing`, i.e. a replace started or suspended (sysfs.c:1288, dev-replace.c:1287,1235); progress query for the replace source device answers 0 while running, and `-ENOTCONN` when suspended (S242 scrub.c:3336; S247 dev-replace.c:1143-1144) | read `exclusive_operation` and `replace_target` sysfs files (mode 444, unprivileged) before starting or cancelling a scrub |"
   - **Why Stale:**
     - Omits the `btrfs_fs_closing` check returning `-EAGAIN` first (`scrub.c:3094-3095`) and context/workers allocation errors (`:3109-3114`), which precede the three device checks in the admitted row.
     - Retains the broad unamended suspend wording (`-ENOTCONN when suspended`), whereas the admitted row narrows this to the unmount suspend path.

3. **`SKILL.md:4307-4318`**:
   > "Counter: `python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>]` ... binds the counted seats `C2RevGR<n>` ... and `C2CritGR<n>` of wave `a2w1` ..."
   - **Why Stale:** Describes the round-45 verification counter and wave seats that failed to bind. Admission in round 47 is governed by `tools/check-scrub-admission-r47.py` and round-47 w1 seats.

4. **`SKILL.md:4325-4327`**:
   > "GR2 was corrected at the integration after its two counted seats read `partly` (earlier device checks, the suspended state, the unprivileged sysfs view) and was read by the uncounted residual seats `ResRevGR2` and `ResCritGR2` (wave `a2r1`; the counter binds only a seat named `C2ResGR2`, which was not dispatched because no counted verdict bound); the verdicts are seat verdicts of this lane, not outside review;"
   - **Why Stale:** References the round-45 review history; GR2 was subsequently re-evaluated in round 46, amended in round 47 to lead with `-EAGAIN`, and evaluated by counted round-47 seats.

5. **`SKILL.md:4462-4464`**:
   > "...so SR7, SR8 and SR9 stay **pending**, not admitted: read them as source-checked statements that no counted seat has bound (their grounding rows GR1-GR3 are the round-45 entry's, gated separately)."
   - **Why Stale:** The parenthetical note asserting that GR1–GR3 are gated separately must reflect that their grounding rows have now been admitted.

6. **`SKILL.md:4544, 4546` (Gate and probe registry — round46 table)**:
   > `| scrub-grounding-r45 | gate | python3 tools/check-scrub-grounding-r45.py ...`
   > `| scrub-admission-r46 | gate | python3 tools/check-scrub-admission-r46.py ...`
   - **Why Stale:** When rows admit in round 47, these rows are superseded by `scrub-admission-r47` (`tools/check-scrub-admission-r47.py`), which requires `MARK_SKILL = '## Scrub grounding — round 47 admission'` (`tools/check-scrub-admission-r47.py:76`).

---

## 4. Second-Order Implementation Contradiction (GR2 Statement vs S247 Source)
- **Observation:** In amended GR2 lines 73–74:
  > "When the unmount suspend path runs, it calls `btrfs_scrub_cancel`; once the scrub returns and clears its context, the progress query returns `-ENOTCONN`"
- **Contradiction with Pinned Source S247:**
  - In `S247` `fs/btrfs/dev-replace.c:1171-1194`, `btrfs_dev_replace_suspend_for_unmount` modifies `replace_state = BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED`, records `time_stopped`, and releases locks. It **never calls** `btrfs_scrub_cancel`.
  - The cited line `btrfs_scrub_cancel(fs_info)` at `dev-replace.c:1143-1144` is in `btrfs_dev_replace_cancel` under `case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:` (canceling an already-suspended replace).
  - This cross-row contradiction between the text claim and the pinned snapshot line was independently identified by counted seats `C1RevAmend` and `R47CritGR2a/b`.

---

## 5. Non-Obvious Move: Unified Substrate Reconciliation Proposal

### Proposed Move
Draft an integrated amendment note for the L1 integrator that reconciles `## Limits:214` in `corpus/knowledge/btrfs-scrub-grounding-r45.md` and pre-formats the append-only `## Scrub grounding — round 47 admission` section in `SKILL.md` (satisfying `MARK_SKILL` in `check-scrub-admission-r47.py:76`), resolving the stale references without mutating round-44 or round-45 historical blocks.

### Exact Proposed Text

#### A. Amendment to `corpus/knowledge/btrfs-scrub-grounding-r45.md` `## Limits:213-216`
```markdown
Three registrations of older rows stay as they are: S242's declared ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337)
do not list `scrub.c:3081`, 3094, 3095, 3109, 3114, 3123, 3133, 3138 or 3139; S243's (72-74, 2021-2049, 2113) do not
list `sysfs.c:1288` or 2015; S237's do not list `scrub.c:421`. The file digests cover the whole snapshots.
```

#### B. Append to `SKILL.md` (at `MARK_SKILL` anchor)
```markdown
## Scrub grounding — round 47 admission

Appended 2026-10-27 (round-47 C1; integrated by the L1).
Entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1, GR2, GR3 admitted by counted seat verdicts
bound under `tools/check-scrub-admission-r47.py` (predicate `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`).

Supersession:
- In `## Scrub grounding — round 45 rows` above, the gate status block (:4288-4290) and table row for GR2 (:4304)
  are superseded. GR2 check ordering leads with the filesystem-closing `-EAGAIN` check (`scrub.c:3094-3095`),
  followed by context and worker allocation errors, prior to device check refusals (`-ENODEV`, `-EROFS`, `-EIO`)
  and `EINPROGRESS`.
- The counter reference (:4307-4318) and review notes (:4325-4327) are superseded by `tools/check-scrub-admission-r47.py`.
- In `## Scrub record — round 44 status note` (:4462-4464), grounding rows GR1-GR3 are now admitted.
- In the Gate Registry, `scrub-admission-r47` supersedes `scrub-admission-r46`.
```

---

## 6. Risks & Second-Order Tracing
- **Runtime Surface:** Zero runtime regressions; census probes and tools do not parse `Limits` or descriptive markdown tables.
- **Contract Surface:** The draft directly aligns `SKILL.md` with `MARK_SKILL` required by `check-scrub-admission-r47.py`, enabling `marks_ok == 3` to resolve cleanly once all three admission marks are committed.
- **Verification Surface:** Resolves out-of-range quote citations in `Limits` without altering line hashes of the active `## GR1`, `## GR2`, or `## GR3` sections (hashes bound by counted seats: GR1 `fe77ac76...`, GR2 `909830c8...`, GR3 `43430a14...`).

---

## 7. Verification Receipts
Receipts captured in `.ufo/waves/round-47/w1/ConnRows/`:
- `diff_gr2.txt` (5.0 KB): Full git diff of GR2 between base and freeze commit `77e9e2b2e96b85d8f048ae2087e246a542b71611`.
- `section_hashes.txt` (433 B): JSON output of `tools/check-scrub-admission-r47.py --section-hash`.
- `s242_quotes_check.txt` (269 B): Extraction of all S242 quotes in GR2 showing 9 quotes outside declared ranges.
- `skill_stale_search.txt` (2.8 KB): Scripted sweep of obsolete gate and status phrases in `SKILL.md`.
- `r44_record_check.txt` (556 B): Scripted extraction confirming absence of contradictions in round-44 entry.
- Scratch directory `/fast/scratch/hyaku/tsukuroi-r47/ConnRows` purged at task completion.
