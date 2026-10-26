VERDICT: draft

# Item X-3 — Cross-source frontier pattern (seat ConnFrontier, tsukuroi round 39)

Assignment: compare the staged package themes in `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md`
with the lane frontier (`corpus/README.md` Frontier sections, `PROVINCE.md` Frontier) and the open leads in
`corpus/SOURCES.md` `## Leads (unopened)`; name the two best next claims (one depth, one adjacency) that a
do-nothing control could not reach, each with the surface it moves and a candidate counting command.

No scratch was created (no clones, copies, mutants or fixtures; all probes were direct read-only host
commands). Probe receipts: `.ufo/waves/round-39/w1/ConnFrontier/probes.txt`. No tools were installed
or upgraded. Nothing outside the allowed report/receipt paths was written.

## Evidence — the three source sets

### A. Staged package (shokuknow merge), not yet adopted

- `MERGE-REPORT.md:3` "Staged by `corpus-expansion-1`. **Nothing was written into the lane repo.**"; `:5`
  147 rows accepted; `:9` "lane registry currently holds **199** rows; first staged id is **S200**".
- Staged table `:20`: `corpus/knowledge/pacman-hook-timing-r25.md` — "pacman 7 hook timing, ownership, and
  the transaction order" (new file, round1 of the staged package).
- Duplicate-check section `:90-96`: staged `S201` maps to the lane's held row `S008` (alpm-hooks(5) facts:
  alphabetical order ignoring suffix, `AbortOnFail` Pre-only, `NeedsTargets` stdin, no Post hooks on failed
  transaction, `.pacnew` original-name trigger) — i.e. the staged entry walks onto sources the lane already
  holds, at a newer man-page vintage.
- The staged entry itself (`knowledge/corpus/knowledge/pacman-hook-timing-r25.md`):
  - header `:2-5`: sources are the alpm-hooks(5) man page at **Pacman 7.1.0, man date 2026-10-15**; a devblog
    (2026-08-09); alpm-install-scriptlet(5) (alpm-docs 0.13.0-1); and the **Chinese ArchWiki pacman page,
    revision 34634, tier B** — all man-page/blog/wiki-tier, none pinned git source.
  - order claims: "Ordering is alphabetical, and upstream says that is not a design"; "On upgrade, the **old**
    package version's pre-transaction hooks run first, then the new version's install-scriptlet functions,
    then the **new** version's post-transaction hooks"; the Chinese "five-step transaction order"
    (`:56-58`); new-version-first scriptlet args; `AbortOnFail` Pre-only; Post hooks skipped on failure.
- The staged package's dominant mass is CJK translation corpora (zh-cmpp rounds 11-16, manpages-mirror
  locale topology, zhwiki cache/offline) plus initramfs-hook API (EN/JA/ZH ×4), errno naming, overlayfs
  mount contract, btrfs troubleshooting, plymouth release watch, ext4 journal — i.e. it reaches into
  pacman order, snapshot-boot/rollback and errno, three surfaces the lane actively works.

### B. Lane frontier after round 39

- `corpus/README.md:296` "per-device error counters only; the scrub record and NVMe SMART stay Frontier".
- `PROVINCE.md:212-214` "**Still Frontier:** the scrub record (`btrfs scrub status`,
  `/var/lib/btrfs/scrub.status.*`, `btrfs-scrub@.timer`; SH3/SH4) and NVMe SMART/Health (`smartctl -H -A`,
  `nvme smart-log`; SH5/SH6) — no census arm reads them."
- `PROVINCE.md:176` — the written promotion condition: "The frontier becomes core when a committed read-only
  census plane reads these signals with a hermetic selftest and a registry row, and a later round admits it;
  until then the entry is the record." and "The storage-integrity reads need privilege for SMART and the
  scrub status ioctl (`sudo -n`, read-only allow-list)".
- `PROVINCE.md:234` (round-39 closure, C1 landed at commit 49cc53c7): "**Still Frontier, unchanged:** the
  scrub record and NVMe SMART. **Remaining limit:** a census that detects the counter's namespace and behaves
  honestly only there cannot be told apart on this host, whose live answer is constant (`HEALTHY 1/1/0`)".
- `SCORECARD.md:2212` — round-39 declaration: "Lowest non-retired axes: depth 8 and adjacency 8 (tied);
  C2 works depth." The next round naturally works **adjacency**; a paired depth+adjacency proposal covers both.
- Census extension points exist: `tools/tsukuroi-census.sh:404-405,459-460` env seams
  (`TSUKUROI_BTRFS_SYSFS`, `TSUKUROI_PROC_MOUNTS`), `probe_storage_arm` at `:1862`, storage selftest cases
  `:2926-2992`. No scrub/SMART probe exists (probe receipt; the only `btrfs scrub status` strings in
  `tools/` are captured text inside the round-26 knowledge checkers `check-storage-health.py:860-873` and
  `check-kernel-taint.py:887-900`).

### C. Open leads (`corpus/SOURCES.md` `## Leads (unopened)`, `:301-321`)

- `:308` limine-snapper-sync issues (errno 13, CapabilityBoundingSet, /sysroot) — but `:278` records that
  round-19 ConnFrontierLeads already screened all 18 GitLab issues for the limine.conf-rewrite proposition;
  only the errno:13-mechanism corroboration aspect stays unmined. Partially spent.
- `:315`+`:320` — btrfs scrub docs opened as S129/S139 (btrfs-progs v7.1); **btrfs-progs 7.x release notes
  and ArchWiki Fwupd remain unopened** — direct feedstock for a scrub-record claim's source rows.
- Also unopened: omarchy installer `/` 0555 origin, archinstall 3.0.5 snapshot-layout, TPM2
  (systemd-cryptenroll/pcrlock), kernel-modules-hook, arch news-gate tools, GitHub AUR mirror, mkinitcpio(8).

### D. Live probes (read-only, receipt in `ConnFrontier/probes.txt`)

- `ls -la /var/lib/btrfs/` → "No such file or directory" (no scrub status files on this host).
- `ls -l /sys/fs/btrfs/` → fsid `1d02a454-c549-4a35-b567-89d60902af8e` present.
- `systemctl list-unit-files 'btrfs-scrub*'` → `btrfs-scrub@.service static`, `btrfs-scrub@.timer disabled
  disabled`; `systemctl show btrfs-scrub@-.timer -p ActiveState,UnitFileState --value` → `inactive`,
  `disabled`. Both readable unprivileged.
- Consequence: the unprivileged-readable subset of the scrub record (shipped timer unit state + status-file
  directory) is probeable today; `btrfs scrub status` and NVMe SMART are root-gated and stay out.

## The cross-source pattern

The staged package and the lane frontier overlap on three active surfaces (pacman order, snapshot/rollback,
errno) with a **vintage/tier mismatch**: the staged entry is sourced at man-page/blog/tier-B-wiki level
(Pacman 7.1.0 man page of 2026-10-15; archlinuxcn wiki rev 34634), while the lane now holds pinned-source
claims on the same subject at pacman `54d9411` (`pacman-hook-order-r38.md` HO1-HO7 from `hook.c:443-455`
etc.; round-39 C2 TO1-TO8 on S213-S218 with own-work capture). Meanwhile the lane's own declared frontier —
the scrub record and NVMe SMART — has no census arm and a written promotion condition that is now satisfiable
for the unprivileged subset. The two best next claims:

## Proposed claim 1 — depth

**Working name D1 (storage): the scrub-record census arm (Frontier→Core for the unprivileged subset).**

- Surface moved: the census `STORAGE` line (`tools/tsukuroi-census.sh`), storage-integrity plane;
  promotes the scrub record from Frontier to Core per the written condition at `PROVINCE.md:176`, scoped to
  what is readable without privilege: the shipped `btrfs-scrub@.timer` unit state (via `systemctl show`,
  today `inactive`/`disabled`) and the scrub status files under `/var/lib/btrfs` (today absent). NVMe SMART
  and the `btrfs scrub status` ioctl remain explicitly out (root-gated; stay Frontier until a `sudo -n`
  read-only allow-list exists, per `PROVINCE.md:176`).
- Claim shape (falsifiable): the census prints a second verdict-neutral line, e.g.
  `STORAGE btrfs-scrub state=recorded|none|blocked timer=<UnitFileState>/<ActiveState> status_files=N
  [detail=…]`, where `none` (timer disabled, no status dir — this host today), `recorded` (status files
  parsed), and `blocked` (unreadable status dir) are distinguished; fixtures drive all non-live legs through
  a `TSUKUROI_SCRUB_STATE_DIR` seam plus a `TSUKUROI_SYSTEMCTL` command seam, mirroring the existing
  `TSUKUROI_BTRFS_SYSFS`/`TSUKUROI_PROC_MOUNTS` pattern (`tools/tsukuroi-census.sh:404-405,459-460`).
- Source rows: S129/S139 (held) + the still-unopened btrfs-progs 7.x release notes lead
  (`SOURCES.md:315,320`) opened as new rows pinning scrub-status file semantics.
- Candidate counting command: `python3 tools/score-storage-scrub-r40.py --revision <REV>`, predicate
  `live_match == 1 and timer_leg_matched == 1 and fixtures_matched == N and selftest_cases == M and
  smart_excluded == 1`; kill rule: any fixture leg that reports `recorded` from an empty status dir, or
  `none` from a populated one, or any read of a root-gated ioctl, kills D1.
- Why a do-nothing control cannot reach it: no arm, selftest, or counter exists; the round-26/38 text makes
  a census arm + hermetic selftest + registry rows + admission the *condition* of promotion, none of which
  re-running the frozen round-39 counters produces.

## Proposed claim 2 — adjacency

**Working name A1 (registry/staged-merge): reconciliation of the staged `pacman-hook-timing-r25.md` against
the lane's pinned sourced claims before adoption.**

- Surface moved: corpus/registry adjacency between the read-only shokuknow staged package and the lane's
  held sourced claims — exactly the MERGE-REPORT's own adopt protocol (`MERGE-REPORT.md:90-96` duplicate
  table; `:122` step 6 "fold the two entries into the one file the lane holds"). Nothing is written into
  shokuknow or the staged package; the check is read-only on both sides.
- Claim shape (falsifiable): every order/timing rule asserted by the staged entry is extracted and
  classified against the lane's frozen snapshots (`.ufo/waves/round-39/frozen/src/`, and round-38's
  hooks-capture) as `identical | adds-aspect | partly | contradicted` with both sides' pinned `file:line`;
  the staged entry's in-text source ids (its own staging S-ids, `pacman-hook-timing-r25.md:2-5`) must be
  shown to survive remap into the lane's S-space (first staged id S200 vs lane rows already at S218);
  `contradicted > 0` kills the adoption of that entry until a version-scope note (man-page/blog/tier-B
  vintage vs 54d9411 source + capture) is added. Spot expectation from reading both sides: alphabetical
  order ↔ HO1 identical; `AbortOnFail` Pre-only ↔ HO4 identical; no-Post-on-failure ↔ HO6 identical;
  new-first scriptlet args ↔ TO4 identical; the staged upgrade-order sentence (old pre-hooks → new
  scriptlets → new post-hooks) and the Chinese five-step order are `partly` against TO1/TO2/TO3/TO7
  (removal step placement; tier-B vintage dated to en:Pacman rev 808924, 2024-05-22); "a hook exists only
  while its providing package is installed" is `adds-aspect` over HO1-HO7.
- Candidate counting command: `python3 tools/check-staged-hook-reconcile-r40.py --revision <REV> --staged
  /home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md`,
  predicate `rules_extracted == rules_classified and contradictions == 0 and version_scope_noted == 1 and
  staged_ids_remapped == 1`; kill rule: any staged order rule judged `contradicted` by the pinned-source
  reviewer (same standard as the C2 kill rule, QUALITY 81) kills A1.
- Why a do-nothing control cannot reach it: every frozen counter measures in-repo artifacts only; none
  reads the staged package, so the overlap risk (two sourced order entries at different vintages entering
  one registry, with stale in-text ids) is invisible to them. This also uses the round-39 declaration's
  own axis note (`SCORECARD.md:2212`, adjacency tied-lowest) where C2 already worked depth.

## Runner-ups considered (not proposed)

1. Nonzero-counter namespace leg for the round-39 remaining limit (`PROVINCE.md:234`): build a tmpfs
   error_stats with nonzero counters inside `unshare -rm` from stdin and show the arm reports DEGRADED.
   Real but small — it deepens C1's own already-claimed surface rather than opening the next frontier.
2. limine-snapper-sync issues for errno:13 corroboration (`SOURCES.md:308`): partially spent —
   round-19 already screened all 18 issues (`SOURCES.md:278`); the remaining aspect is corroboration of an
   [inf] mechanism (`README.md:40-41`), which issue text alone cannot falsify.
3. Mori counting equivalence for ADJ-04 (MESSAGE_ID vs message-text counts over one window): genuinely
   adjacent, but one-sided without mori-side agreement on the window, and the round-33 boundary note
   already records the method difference; weaker momentum than the staged-merge reconciliation, which the
   MERGE-REPORT adopt checklist already obliges the operator to perform.

## Exact proposed text (draft for the round-40 declaration)

- **D1 (depth):** "C1 operability→depth (storage): the census gains a second verdict-neutral STORAGE line
  reading the scrub record's unprivileged subset — the `btrfs-scrub@.timer` unit state and the scrub status
  files under `/var/lib/btrfs` (seams `TSUKUROI_SCRUB_STATE_DIR`, `TSUKUROI_SYSTEMCTL`) — reporting
  recorded|none|blocked, never entering the rollup; NVMe SMART and the scrub-status ioctl stay Frontier
  (root-gated). Counter `python3 tools/score-storage-scrub-r40.py --revision <REV>`; predicate
  live_match==1 and fixtures_matched==N and smart_excluded==1. Kill: any fixture leg inverting
  recorded/none, or any root-gated read."
- **A1 (adjacency):** "C2 adjacency (registry/staged-merge): every order rule in the staged
  `pacman-hook-timing-r25.md` is classified identical|adds-aspect|partly|contradicted against the lane's
  pinned sourced claims (HO1-HO7 at 54d9411, TO1-TO8 at 54d9411) before adoption; its in-text staging S-ids
  are shown remapped into the lane's S-space. Counter
  `python3 tools/check-staged-hook-reconcile-r40.py --revision <REV> --staged <path>`; predicate
  rules_extracted==rules_classified and contradictions==0 and staged_ids_remapped==1. Kill: any staged
  order rule judged contradicted at the pinned file:line by a reviewer seat."

## Not done

- No network fetches (btrfs-progs 7.x release notes lead opened only as a registry-row proposal, not read
  live). No sudo/root-gated probes (`btrfs scrub status`, `smartctl`, `nvme smart-log`) — consistent with
  the lane's read-only boundary; this is why D1 is scoped to the unprivileged subset.
