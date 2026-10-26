VERDICT: draft

# C2-22 — append-only README section draft for round 39 (transaction order; hidden storage root)

Draft only. `corpus/README.md` is unmodified (`git status --porcelain corpus/README.md` empty at
HEAD `394e1ba`; `wc -l` 301). I wrote only this report and
`.ufo/waves/round-39/w1/C2ScribeReadme/receipts.txt`. No counter, selftest or census was run; no
mutating git or package command was run (only read-only `git show`/`git log`/`git status`/`git ls-files`).
Every number below is read from committed artifacts or a read-only file read. No
scratch directory was needed: no clone, fixture or mutant was made under
`/fast/scratch/hyaku/tsukuroi-r39/`. Observed working-tree state (`M PROVINCE.md`, `M SKILL.md` — the
latter a sibling seat's uncommitted round-39 section, `?? .ufo/waves/round-39/w1/`,
`?? .ufo/waves/round-39/w1-dispatch.err`) was not touched.

## What the draft rests on (checks I ran)

| Fact used in the draft | Command / path | Observed |
|---|---|---|
| README ends at the round-38 Frontier notice; no round-39 section | `wc -l corpus/README.md`; `read corpus/README.md:285-301` | `301`; last text is the round-38 `Known limit … absent /sys/fs/btrfs reads HEALTHY 0/0/0` sentence |
| round-38 table shape to mirror | `corpus/README.md:285-292` | lead line, 3-column `\| Note \| Holds \| Sources \|`, one row per note, `### Frontier notice — round 38` |
| round-38 limit line quoted by the new notice | `corpus/README.md:300-301` | `` Known limit carried to the frontier: an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it gives a false all-clear. `` |
| C2 note rules TO1–TO8 and host columns | `corpus/knowledge/pacman-transaction-order-r39.md:20-31` | eight rows read in full; end-to-end order `:33-42`, boundaries `:46-52` |
| note bytes at the measured commit equal HEAD | `git show 4078eb2:corpus/knowledge/pacman-transaction-order-r39.md \| sha256sum` vs `sha256sum corpus/knowledge/pacman-transaction-order-r39.md` | both `701a462dfe9c3d03fba0366719e772e081d6cb181e25398d78c0f1ebf5b0d74a` |
| source rows exist and S217 supersedes S210 | `corpus/SOURCES.md:217,222-227` | S213 add.c, S214 sync.c, S215 remove.c, S216 util.c, S217 trans.c (“supersedes S210 — …”), S218 own-work; S208 hook.c `:217` |
| counter digest matches the declaration | `sha256sum tools/check-transaction-order-r39.py` | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` |
| C2 after receipt PASS | `.ufo/waves/round-39/after/c2-after-4078eb2.jsonl` | `rules_verified 8`, `duplicate_rows 0`, `duplicate_headings 0`, `source_ok 1`, `counts_ok 2`, `oracle_violations 0`, `result PASS`, `exit 0` |
| host counts in the row | `grep -c` on `.ufo/waves/round-39/frozen/txcapture/pacman.log`; `awk`/`wc` on `hook-when.tsv` | `86` `[PACMAN] Running`, `60` `transaction started`, `28` `[ALPM] removed `, `441` `[ALPM-SCRIPTLET]`, `17` PreTransaction rows of `70` hook rows |
| 252 of 441 tag lines outside a commit; 0 running lines inside one | C2 receipt `host` block | `scriptlet_tag_outside_commit 252`, `scriptlet_tag_total 441`, `running_inside_commit 0` |
| capture integrity | `sha256sum -c MANIFEST.sha256` in `.ufo/waves/round-39/frozen/txcapture/` | `capture-meta.txt: OK`, `hook-owners.tsv: OK`, `hook-when.tsv: OK`, `pacman.log: OK`; MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` |
| C1 arm behaviour | `tools/tsukuroi-census.sh:1862-1930`; contract `:355-369` | absent/empty root reads the mount table only when `fsn == 0`; `mt > 0` → `BLOCKED … detail=mounts:btrfs-without-sysfs`; unreadable table → `detail=mounts:unreadable`; a root with fsid entries never reads it |
| census bytes at the measured commit equal HEAD | `git show 49cc53c:tools/tsukuroi-census.sh \| sha256sum` vs `sha256sum tools/tsukuroi-census.sh` | both `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d` |
| four round-39 selftest cases | `grep -n "case_home='storage" tools/tsukuroi-census.sh` | new cases `storage-hidden-absent` `:2974`, `storage-hidden-empty` `:2979`, `storage-mounts-unreadable` `:2984`, `storage-mounted-populated` `:2989`; receipt `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)` |
| C1 counter digest matches the declaration | `sha256sum tools/score-storage-hidden-r39.py` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` |
| C1 after receipt PASS | `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl` | `hidden_matched 2`, `views_matched 3`, `fixtures_matched 5`, `live_match 1`, `six_planes_all 1`, `result PASS`, `exit 0`; both hidden legs read `BLOCKED … detail=mounts:btrfs-without-sysfs` |
| Core/limit wording | `PROVINCE.md:225-237` | “**Core now** additionally holds that one read of the mount table … not a new owned surface”; “**Still Frontier, unchanged:** the scrub record and NVMe SMART”; remaining-limit sentence |
| v1 counter side effect | `SCORECARD.md:2232-2234`; the same text in the working-tree `SKILL.md:3223` (a sibling's uncommitted section, not at HEAD) | F06 encodes the superseded rule; `score-storage-arm-r38.py` “FAILs 9/10 by construction” after `49cc53c7` |
| declaration rows for the section's Sources cell | `SCORECARD.md:2209-2240` | C1 and C2 declaration rows, both counter digests, “Measured revision … declared before the after-run” |
| proposed table keeps the 3-column shape and delimiters (QUALITY 10) | counted `\|` per table line in the fenced block | header, separator and row all 3 columns |

## Findings

1. **No `corpus/lessons/round-39.md` and no `SCORECARD.md` “Round 39 — measured outcome” section exist
   at drafting** (`ls corpus/lessons/ | tail` ends at `round-38.md`; `grep -n "Round 39 — measured
   outcome" SCORECARD.md` is empty). The round-38 row pointed its Sources cell at `lessons/round-38.md`
   Gate; this draft cannot. It cites the committed capture plus `SCORECARD.md` “Round 39 — declaration”
   instead, and the notice names the author receipt (`.ufo/waves/round-39/after/…`, tracked) rather than
   a future outcome section. If the Gate lands a lesson, the landing author may prefer that pointer.
2. **The round-38 v1 counter will go red for a correct reason.** `score-storage-arm-r38.py` fixture F06
   encodes the superseded absent-root rule and fails 9/10 at post-C1 revisions by construction
   (`SCORECARD.md:2232-2234` predicted it in the declaration; the same text sits in the working-tree
   `SKILL.md:3223`, a sibling's uncommitted section). The draft states
   this in the frontier notice so the 9/10 red is not read as a regression.
3. **TO5's 17-hook host column is consistency, not proof** (`pacman-transaction-order-r39.md:28`: “This
   is consistent with the rule, not a proof of it”). The drafted row carries the boundary marker.
4. **The note's own counts reproduce.** I re-derived 86 / 60 / 28 / 441 / 17 from the frozen capture and
   all matched (`receipts.txt`); the two counts the counter checks (`60 transactions`, `252 of 441`) are
   in the committed PASS receipt. I found no falsifying divergence; the TO1–TO8 rule truth itself was
   not judged (below).
5. **Append-only is respected.** The draft adds a section after `corpus/README.md:301`; it rewrites no
   earlier row or bullet. The round-38 table row for `probe_storage_arm` stays as written; only its
   trailing “Known limit” notice sentence is superseded, and the draft says so with the quoted line.

## Touched surfaces and gates

- Wrote: this report; `.ufo/waves/round-39/w1/C2ScribeReadme/receipts.txt`. No lane product file, no
  `corpus/README.md` byte, no `SKILL.md`/`PROVINCE.md`/`SOURCES.md` edit, no index or jj change.
- Gates run: none. The C1/C2 counters and the census selftest were read from committed receipts, not
  executed. No host action, no mount outside a private namespace (none was created), no sudo, no install.
- Out of scope: judging TO1–TO8 rule truth (reviewer seats); committing the README section; counter or
  selftest reruns; any SKILL/PROVINCE redraft owned by sibling seats.

## Not done (limits)

- No counter run, no `--selftest`, no census run. All figures are from committed receipts/capture or
  read-only reads; an unrun check has not passed.
- I did not judge TO1–TO8 against the libalpm snapshots at the cited lines; the counter verifies
  quote-location only, and the round-39 kill rule assigns rule-truth judgment to reviewer seats. The
  report therefore emits no `TO<n>: holds|partly|fails` lines.
- No live pacman/transaction behaviour measured; the note's boundaries (`:46-52`) are inherited, not
  re-proven.
- No tool install or upgrade was needed, so nothing is recorded under the tooling directive.

## Proposed text (exact; insert one blank line after `corpus/README.md:301`, then append this block)

```markdown
## Round 39 — transaction order; hidden storage root

Append-only; the coverage map and Frontier bullets above stay as written. The C2 entry deepens the held
update-safety plane (`../PROVINCE.md` Core) and is not new coverage; the C1 change is an operability repair
inside the round-38 storage arm above, not a new coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/pacman-transaction-order-r39.md` | The libalpm transaction order TO1–TO8 at pacman `54d9411` (installed `7.1.0.r9.g54d9411-3`), deepening the update-safety plane whose within-phase hook order is `knowledge/pacman-hook-order-r38.md` (HO1–HO7): Pre hooks before `transaction started`, Post after `transaction completed` (TO1); sync removals before adds (TO2); per package `pre_install`/`pre_upgrade` → files and database entry → `installed`/`upgraded` line → `post_install`/`post_upgrade` (TO3); new version first, old second in scriptlet arguments (TO4); hook directories re-read per phase, so a hook first installed in a transaction is no Pre candidate (TO5); `ldconfig` once, skipped on an interrupted commit (TO6); removal order `pre_remove` → files → `removed` → `post_remove`, with neither scriptlet nor `removed` line for an upgrade's old half (TO7); every chroot child's output line tagged `ALPM-SCRIPTLET`, which is not "install scriptlet" (TO8). Frozen capture: 86 `[PACMAN] Running` windows, 60 started transactions, 28 `removed` lines, 252 of 441 `ALPM-SCRIPTLET` lines outside commit phases, 17 Pre hook files owned by packages first installed in a transaction (consistency, not proof), 0 of 60 transactions mixing removals and adds; S217 supersedes the round-38 S210 anchor | S208, S213–S218; `.ufo/waves/round-39/frozen/txcapture/` (MANIFEST pinned in the note's `source:` line); `../SCORECARD.md` "Round 39 — declaration" |

### Frontier notice — round 39

The round-38 notice above (`corpus/README.md:300-301`) carried one known limit — "an absent `/sys/fs/btrfs` reads `HEALTHY 0/0/0`, so a namespace that hides it gives a false all-clear" — and C1 closes it for a btrfs mount that the process's mount table lists: since `../tools/tsukuroi-census.sh` `probe_storage_arm` at commit `49cc53c7`, a sysfs root that is absent or holds no fsid entry reads `HEALTHY 0/0/0` only when the mount table (`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`) lists no btrfs mount; with one listed the STORAGE line is `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`, and an unreadable table is `state=BLOCKED … detail=mounts:unreadable` (`../PROVINCE.md` "Round-39 limit closure — R38-ABSENT-ROOT"). Core now additionally holds that one read of the mount table, read for this guard only and not a new owned surface, and the line stays verdict-neutral; `../tools/score-storage-hidden-r39.py` counts it under the frozen predicate — hidden 2/2, three views built on tmpfs inside `unshare -rm` from stdin (closing R38-Q82-LEAK), fixtures 5/5, live 1, six planes 1 — with the author receipt `.ufo/waves/round-39/after/c1-after-49cc53c.jsonl` PASS. **Still Frontier, unchanged:** the scrub record and NVMe SMART (`../PROVINCE.md:234-235`). **Remaining limit:** the namespace-sensitive behaviour cannot be told apart on this host, whose live answer is constant `HEALTHY 1/1/0`, and no host-side injection is authorized; the round-38 v1 counter's fixture F06 encodes the superseded rule and fails 9/10 at post-C1 revisions by construction (`../SCORECARD.md:2232-2234`).
```

Artifacts: this report; `.ufo/waves/round-39/w1/C2ScribeReadme/receipts.txt` (commands and observed
outputs quoted above).
