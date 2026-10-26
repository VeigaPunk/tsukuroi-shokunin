VERDICT: defect-found

Seat C2RevSourcesRows — item C2-16: review of `corpus/SOURCES.md` rows S213–S218 and the S208 used-by change at commit 4078eb236c7c67f343c76956c587d0a356e0bf5c.

Summary: S213–S218 **agree** on every checked cell (11 cells; tier/kind fit; anchor line ranges against `.ufo/waves/round-39/frozen/src/`; teaches true and not overclaiming; used-by exactly the citing entries; S218 digest). One defect: **S208's used-by cell is not "exactly the citing entries"** — `corpus/knowledge/boot-writers-r19.md:176-177` cites S208 (`hook.c:540`, `:588-590`) and is absent from the cell. That omission predates the reviewed change (introduced by round-38 commit b0005ae, which both created S208 and added the boot-writers citation); the 4078eb2 change itself (appending the round-39 entry, touching only that cell) is correct.

Reviewed bytes pinned: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse 4078eb2…:corpus/SOURCES.md HEAD:corpus/SOURCES.md` → `20852343879288e99023d8df8b14c26c49a2d767` twice, `git status --porcelain -- corpus/SOURCES.md` clean; same for `corpus/knowledge/pacman-transaction-order-r39.md` → `ba8b228df8a1ca7efd5ab15056287bc42be5b851` twice. Working tree = reviewed commit.

## Method

Read-only throughout: `git show`/`rev-parse`/`log -S`/`status` in the lane (no add/commit/checkout/reset), file reads, `sha256sum -c`, gawk counts, the census validator, and the frozen C2 counter run at the pinned revision. No tool installs (none needed — record: zero installs/updates). No pacman, no sudo, no host mutation. Scratch `/fast/scratch/hyaku/tsukuroi-r39/C2RevSourcesRows/` used for one parent-revision copy and removed at the end. Receipts: `.ufo/waves/round-39/w1/C2RevSourcesRows/` (census-validate.txt, counter-4078eb2.txt, host-counts.txt, manifest-and-cell-counts.txt, s208-cell-diff.txt, diff-sources-4078eb2.txt).

## Census validate (required paste)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` — full output (34 W04 advisory lines, then the summary):

```
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init across scopes
tsukuroi	W04	S082 duplicate url git-scm.com/docs/git-rev-parse/2.56.0 across scopes
tsukuroi	W04	S087 duplicate url archlinux.org/news across scopes
tsukuroi	W04	S089 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S090 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S092 duplicate url wiki.archlinux.org/title/System_maintenance?oldid=885170 across scopes
tsukuroi	W04	S095 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 across scopes
tsukuroi	W04	S098 duplicate url gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs across scopes
tsukuroi	W04	S105 duplicate url archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks across scopes
tsukuroi	W04	S106 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S107 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S108 duplicate url wiki.archlinux.org/title/Downgrading_packages?oldid=887421 across scopes
tsukuroi	W04	S109 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions across scopes
tsukuroi	W04	S111 duplicate url gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook across scopes
tsukuroi	W04	S126 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml across scopes
tsukuroi	W04	S136 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml across scopes
tsukuroi	W04	S137 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S138 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst across scopes
tsukuroi	W04	S149 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S155 duplicate url raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst across scopes
tsukuroi	W04	S158 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c across scopes
tsukuroi	W04	S182 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S184 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S185 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst across scopes
tsukuroi	W04	S203 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	W04	S204 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	W04	S217 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Exit code: **0**. The one W04 introduced by this round is S217 (shares the trans.c URL with S210, different scope; S217's teaches records the supersedes) — advisory only per the script header ("W-codes and unlisted lanes never change status", scripts/sources-census.sh:31) and lane precedent (`corpus/lessons/round-38.md:66-67`: W04 duplicate-URL advisories non-blocking, S202/S203 precedent).

## Counter corroboration (extra, read-only)

`python3 tools/check-transaction-order-r39.py --revision 4078eb236c7c67f343c76956c587d0a356e0bf5c` → `rules_verified 8, duplicate_rows 0, duplicate_headings 0, source_ok 1, counts_ok 2, oracle_violations 0, result PASS, exit 0`; host `{windows 86, transactions_started 60, scriptlet_tag_outside_commit 252, scriptlet_tag_total 441, running_inside_commit 0}` (receipt counter-4078eb2.txt). Matches the declared predicate.

## Per-row review

Schema: header `corpus/SOURCES.md:5` — `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by` (11 cells). Cell count machine-checked for all seven rows: `gawk -F'|'` → `S208/S213/S214/S215/S216/S217/S218 NF=13 cells=11` (receipt manifest-and-cell-counts.txt); census E01 (NF!=13) silent. Kind enum includes `code` and `own-work` (scripts/sources-census.sh:655); tier `[ABC]` (:657); E10 bars only community-at-A (:668) — so `code`/A and `own-work`/A are contract-valid, and both match the admitted round-38 precedents S208–S211 (code/A) and S212 (own-work/A).

### S208 (used-by change) — change agree; cell exactness DEFECT (minor, pre-existing)

- The commit's only S208 change is cell 12: `git show 4078eb2 -- corpus/SOURCES.md` = 7 insertions, 1 deletion; cell-wise comparison of parent vs reviewed row shows **only** `CELL 12 DIFFERS` — old `corpus/knowledge/pacman-hook-order-r38.md` → new `corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md` (receipt s208-cell-diff.txt). No immutable cell touched.
- The added entry is a genuine citing entry: `corpus/knowledge/pacman-transaction-order-r39.md:1` `source: S208, S213, S214, S215, S216, S217, S218 …`; TO5 cites `S208 hook.c:532-560`, TO8 cites `S208 hook.c:525-528` (:28, :31). Change **agree**.
- **DEFECT (disagree on exactness):** `corpus/knowledge/boot-writers-r19.md:176-177` cites S208 directly — "`HO2 in corpus/knowledge/pacman-hook-order-r38.md; S208 hook.c:540, :588-590; S211 alpm.c:56-62`" — and is **not** in S208's used-by cell. Lane practice puts such inline citations in used-by: S007 and S008 list `corpus/knowledge/boot-writers-r19.md` in their used-by cells (`corpus/SOURCES.md:13-14`) for exactly that file's inline citations (`boot-writers-r19.md:37,115` cite S008/S007); a round-17 seat report treats even a QUALITY-section citation as justifying the used-by link (`.ufo/waves/round-17/build/SourcesRecheckDraft.md:51`); the round-24 census check enforces the used-by→citation direction (`.ufo/waves/round-24/w2/RevCensusEnd/checks-output.txt:22`). The boot-writers citation was added by b0005ae (`git log --oneline -S 'S208' -- corpus/knowledge/boot-writers-r19.md` → single commit `b0005ae round-38: integrate wave 1 …`), the same round-38 integration that created S208 — so the gap predates 4078eb2 and is not introduced by the reviewed change, but the cell as it now stands is incomplete.
- Proposed exact used-by cell (not a requested draft; for the used-by owner as a mutable change): `corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/boot-writers-r19.md, corpus/knowledge/pacman-transaction-order-r39.md`
- Anchors spot-rechecked against the frozen snapshot (inherited row): `_alpm_hook_cmp` 443-455 exact (def :443, `/* exclude the suffixes from comparison */` :449, `strncmp` :450, tie `return l1 < l2 ? -1 : 1;` :452, close :455); `_alpm_hook_run` 532-683 exact (def :532; hookdirs walk :540; `opendir` :554; abort-on-fail :660; file ends :683 inside this function); validate 116-147 = body of `_alpm_hook_validate` (def :113-115, triggerless `return 0` :118-122, `return ret;` :147). Snapshot sha256 `99f1044b…` = frozen/src/SHA256SUMS line 2; `sha256sum -c SHA256SUMS` → all six `OK`.

### S213 — agree

- kind=code, tier=A ✓; opened 2026-10-26 (past/present), recheck on-release ✓ (E08/E09 silent).
- Anchor vs frozen/src/add.c (sha256 `fd313629…` = SHA256SUMS line 1): `commit_single_pkg` 466-474 — pre-scriptlet block is :467 comment `/* pre_install/pre_upgrade scriptlet */`, :468-470 guard/name, :472-473 `_alpm_runscriptlet(…, 1)`, :474 close; range starts one line early (:466 is the tail of the preceding `%s package %s-%s` debug log) — nit, taught block fully contained. 616-648 — logaction switch :616-632 (`installed` :618, `downgraded` :622, `reinstalled` :626, `upgraded` :630) + post-scriptlet block :638-647 (`/* run the post-install script if it exists */` :638, `_alpm_local_db_pkgpath(db, newpkg, "install")` :641, run :644-645). `_alpm_upgrade_packages` 655-695 — def :655, add loop :670-688, `_alpm_ldconfig(handle)` :691, `return ret;` :694, close :695. All taught content inside the ranges.
- Teaches true: pre scriptlet runs from the package file (`pkgfile = newpkg->origin_data.file` add.c:463) before extraction (archive open/extract loop later in the function); post scriptlet after the installed/upgraded log line (:638-647 after :616-632); new version first (:473 `newpkg->version, oldpkg ? oldpkg->version : NULL`); ldconfig once after all adds (:691, after the :670-688 loop). No overclaim (the failure/skip path belongs to TO6, not claimed here).
- used-by exact: lane-wide grep for `S21[3-8]` over *.md/*.py/*.sh (excluding my own wave dir) finds the only corpus citing entry = `corpus/knowledge/pacman-transaction-order-r39.md` (source: line :1; TO3/TO4/TO6). Other hits are SOURCES.md itself, `corpus/lessons/round-38.md:42,66` (campaign-numbering / staged-entry context, not registry citations), round-37/38 wave artifacts, `make-w1-spec.py`, `SCORECARD.md:2228,2237` (declaration/control text).

### S214 — agree

- Anchor vs frozen/src/sync.c (sha256 `6b297364…` = SHA256SUMS line 4): `_alpm_sync_commit` 1336-1356 — def :1336, removal comment :1341-1343, `_alpm_remove_packages(handle, 0)` :1345, "installing packages" :1353, `_alpm_upgrade_packages(handle)` :1354, error return :1355-1356. Taught order fully inside.
- Teaches true: removals (:1341-1350) strictly before adds (:1352-1354). No overclaim.

### S215 — agree

- Anchor vs frozen/src/remove.c (sha256 `a052d455…` = SHA256SUMS line 3): `_alpm_remove_single_package` 699-733 — def :685; range opens at the `if(newpkg)` upgrade-half branch (:698-699, the guard that makes the second teaches clause true) and covers pre_remove :711, file removal :718, `removed %s (%s)` :722, post_remove :731, close :733.
- Teaches true: whole-package removal (newpkg == NULL) runs pre_remove (else branch :701-714), files (:716-719), removed log (:721-724), post_remove (:726-733); the old half of an upgrade gets none of those three (each guarded on `newpkg`/`!newpkg`), while files are still removed — "none of the three" matches the scope cell ("which removals log a line or run scriptlets"). Precise, no overclaim.

### S216 — agree

- Anchor vs frozen/src/util.c (sha256 `381618b6…` = SHA256SUMS line 6): `_alpm_chroot_process_output` 521-528 — def :521, `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line)` :527, EVENT :528; `_alpm_run_chroot` :610 (def); `_alpm_ldconfig` :820 (def). Exact.
- Teaches true: every output line read from a chroot child reaches `_alpm_chroot_process_output` (:544, :554, :561, :570, :763) which logs under ALPM-SCRIPTLET (:527); hooks reach it via `_alpm_run_chroot` (hook.c:525/:528), install scriptlets via `_alpm_runscriptlet` → `_alpm_run_chroot` (trans.c:337 def; `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)` trans.c:404), ldconfig via `_alpm_run_chroot` (util.c:833). The tag therefore does not mean "install scriptlet" — corroborated by the capture (252 of 441 tagged lines outside commit phases). No overclaim.

### S217 — agree

- Anchor vs frozen/src/trans.c (sha256 `637c1165…` = SHA256SUMS line 5, same digest as S210 — same file, expected): `alpm_trans_commit` :167 exact (`int SYMEXPORT alpm_trans_commit(alpm_handle_t *handle, alpm_list_t **data)`); Pre phase 201-204 exact (:201 NOHOOKS if, :202 `_alpm_hook_run(handle, ALPM_HOOK_PRE_TRANSACTION)`, :203 `RET_ERR(… ALPM_ERR_TRANS_HOOK_FAILED …)`, :204 close); `transaction started` :208 exact; `transaction completed` + Post 232-239 exact (:233 `ALPM_EVENT_TRANSACTION_DONE`, :235 completed log, :237-238 Post `_alpm_hook_run`).
- Teaches true: supersedes claim verified — `_alpm_trans_commit` matches nothing in trans.c at 54d9411 (grep: no matches), the commit function is `alpm_trans_commit` at :167, and S210's anchor cell does say `_alpm_trans_commit` (`corpus/SOURCES.md:219`); Pre before :208, Post after :235. No overclaim.
- W04 advisory (URL shared with S210) expected and non-blocking (see Census section).

### S218 — agree

- kind=own-work, tier=A ✓ (S212 precedent); recheck 30d ✓.
- Digest: anchor sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` == `sha256sum .ufo/waves/round-39/frozen/txcapture/MANIFEST.sha256` → `cb5cb4f4…cb4  …/MANIFEST.sha256` (observed). Capture integrity: `sha256sum -c MANIFEST.sha256` → capture-meta.txt/hook-owners.tsv/hook-when.tsv/pacman.log all `OK`.
- Teaches counts independently reproduced from the frozen pacman.log with a gawk state machine implementing the counter's rules (window opens at `[PACMAN] Running`; commit phase = `transaction started`..completed/failed/interrupted): `windows=86 started=60 tagged=441 outside=252 violations=0` (receipt host-counts.txt) — all four teaches numbers match (86 command windows, 60 started transactions, 441 ALPM-SCRIPTLET lines, 252 outside every commit phase). `grep -c` corroboration: `transaction started` = 60, `ALPM-SCRIPTLET` = 441.
- Scope/timestamp: `capture-meta.txt:1` `# captured 2026-10-26T05:42:12Z host=plazir27 read-only by TsukuroiR39`, :2 pacman.log copy, :3-:5 hook-owners/hook-when commands, :4 `pacman 7.1.0.r9.g54d9411-3` — matches the scope and anchor cells. No overclaim.

## used-by exactness sweep (S213–S218)

Citing entries found (lane-wide, see S213 section): only `corpus/knowledge/pacman-transaction-order-r39.md`, which cites all six (source: line :1; TO1 S217, TO2 S214, TO3/TO4/TO6 S213, TO5 S208, TO7 S215, TO8 S216+S208). used-by cells of S213–S218 name exactly that entry ✓. No other corpus file cites any of S213–S218.

## What I did not do

- Did not re-fetch upstream gitlab: anchors verified against the frozen snapshots, their SHA256SUMS (`sha256sum -c` all OK), and FETCH.txt provenance (`fetched 2026-10-26T05:42:12Z by TsukuroiR39 (L1), read-only; base URL …/raw/54d9411/lib/libalpm/<file>; installed: pacman 7.1.0.r9.g54d9411-3`).
- Did not independently re-derive TO5's host cell join (the "17 PreTransaction hook files owned by a package first installed in some transaction; none of the 17 ran in that transaction's Pre phase" claim). I verified only the 17 count (`gawk` over hook-when.tsv → `PreTransaction hooks: 17`); the entry itself bounds that cell as "consistent with the rule, not a proof" (`pacman-transaction-order-r39.md:28` and Boundaries section).
- Did not judge S210/S211/S007 rows (outside item); no mutating git/jj command; no pacman/sudo/host change; no tool installs.

## Observations outside the item (same defect class / drift)

- Same used-by gap class: S211's used-by lists only `corpus/knowledge/pacman-hook-order-r38.md` while `boot-writers-r19.md:177` cites `S211 alpm.c:56-62`; S007's used-by lists `degraded-triage-r4.md, boot-writers-r19.md` but not `pacman-hook-order-r38.md`, whose HO2 cites "S007 (HookDir)" (`corpus/knowledge/pacman-hook-order-r38.md:22`). Both predate 4078eb2.
- `corpus/lessons/round-38.md:66` says "`S214`/`S220` match no row today" — historical round-38 statement about the refused staged entry's citations; registry S214 now exists (unrelated source). Flagged so a future reader does not read that sentence's S214 as this row.

TO1: holds — .ufo/waves/round-39/frozen/src/trans.c:201-208
TO2: holds — .ufo/waves/round-39/frozen/src/sync.c:1336-1356
TO3: holds — .ufo/waves/round-39/frozen/src/add.c:466-474,616-648
TO4: holds — .ufo/waves/round-39/frozen/src/add.c:470-474
TO5: holds — .ufo/waves/round-39/frozen/src/hook.c:532-560
TO6: holds — .ufo/waves/round-39/frozen/src/add.c:676-692
TO7: holds — .ufo/waves/round-39/frozen/src/remove.c:699-733
TO8: holds — .ufo/waves/round-39/frozen/src/util.c:521-528
