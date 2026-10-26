VERDICT: supports

Seat AsmQuarantine, item F-3 (round 40, tip f951f288483c1af0cef4afd458488b84cf7a2165, base 53b294a274656be6479aadf2ec2fee890ded77ce). Receipts: `.ufo/waves/round-40/w1/AsmQuarantine/`. No scratch dir was used and no tool was installed. Nothing outside this report and the receipts was written.

## 1. Slice re-derivation — identical to the frozen file

Command (the §10 awk, the same text round 39 recorded at `.ufo/waves/round-39/w1/AsmCollision.md:121`). The round prompt itself was not available to this seat:

```
awk -F'|' -v l='tsukuroi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Observed:
- 12 output lines in `AsmQuarantine/slice.rederived`.
- `cmp slice.rederived .ufo/waves/round-40/assimilation/quarantine-slice` printed `IDENTICAL`.
- sha256 of both files is `a17de5fbd02bc923c9c29aa606e8561ecb5a181e58e0d09010a6817901781006`.
- The sha256 matches the round-39 slice (`.ufo/waves/round-39/w1/ScoutQuarantine.md` reports the same hash).
- The register's sha256 is `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`.
- The last shokuknow commit touching the register is `d4ab45f281572ecb353dd3c9b71eee0e9213558b`.

The awk filter keeps data rows only. The register also has a `| tsukuroi | 2 |` row in the class-count table (line 253). It is excluded because column 3 is not `roundN` and column 4 is not an S-id.

The 12 rows are register lines 229, 230 and 366-375. Full text is in `register-tsukuroi-rows.txt`.

| id | round | class | cited document (staged row, `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`) |
|---|---|---|---|
| S211 | 1 | payload-absent | https://gitlab.freedesktop.org/api/v4/projects/plymouth%2Fplymouth/repository/tags |
| S213 | 1 | payload-absent | https://docs.oracle.com/cd/F22978_01/btrfs/btrfs-UsingtheSnapperUtilityWithBtrfsSubvolumes.html |
| S225 | 3 | source unfetchable | https://wiki.archlinux.org/index.php?title=ArchWiki:Translation_Team_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87) |
| S230 | 3 | no locator | own-work `corpus/knowledge/snapper-eacces-mechanism.md` |
| S231 | 3 | no locator | own-work `corpus/knowledge/initramfs-v42-sysroot-recovery.md` |
| S242 | 4 | no locator | own-work `corpus/knowledge/boot-writers-r19.md` |
| S243 | 4 | no locator | own-work `corpus/knowledge/btrfs-space-r30.md` |
| S244 | 4 | no locator | own-work `corpus/knowledge/btrfs-repair-r31.md` |
| S249 | 5 | no locator | kernel tree `Documentation/translations/zh_TW/index.rst` @ Linux v7.2 (no URL in the row) |
| S250 | 5 | no locator | kernel tree `Documentation/translations/zh_CN/index.rst` @ Linux v7.2 |
| S251 | 5 | no locator | kernel tree `Documentation/translations/ja_JP/index.rst` @ Linux v7.2 |
| S252 | 5 | no locator | own-work `tools/check-boot-writers.py` |

The "no locator" ids carry a trailing backtick in the register (`S225\``). The slice file mirrors that. Rows 366-375 come from the second table (class `unreachable` / no locator), not from the `payload-absent` table. Document mapping: `slice-docs.tsv`.

## 2. Intersection with the documents S219-S225 cite

The documents S219-S225 cite at the tip (`corpus/SOURCES.md`, extracted in `s219-s225-docs.tsv`):
- S219 gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/meson_options.txt
- S220 gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/blob/7.1.0.r9.g54d9411-3/PKGBUILD
- S221 …/blob/54d9411/lib/libalpm/util.c
- S222 …/blob/54d9411/lib/libalpm/trans.c
- S223 …/blob/54d9411/lib/libalpm/hook.c
- S224 …/blob/54d9411/doc/alpm-hooks.5.asciidoc
- S225 `.ufo/waves/round-40/frozen/hostcap/` (own-work)

By document (URL or path), the intersection is **empty**. The slice documents sit on these hosts and paths:
- gitlab.freedesktop.org
- docs.oracle.com
- wiki.archlinux.org
- the kernel tree's `Documentation/translations/*`
- lane files `corpus/knowledge/{snapper-eacces-mechanism,initramfs-v42-sysroot-recovery,boot-writers-r19,btrfs-space-r30,btrfs-repair-r31}.md` and `tools/check-boot-writers.py`

None of these is a document S219-S225 cite. The only host S219-S225 use is gitlab.archlinux.org, and none of the 147 staged rows has a gitlab.archlinux.org document (`grep -c 'gitlab.archlinux.org' staged-docs.tsv` = 0).

**By id** there is exactly one overlap: **S225**. It is an id-only collision, not a shared document. Slice S225 is the ArchWiki Translation Team page. Lane S225 is the round-40 host exec capture (own-work). S211 and S213 exist in the lane too, but they were adopted earlier as libalpm alpm.c and add.c at pacman 54d9411 (`corpus/SOURCES.md` lines 220 and 222). They are outside S219-S225, so they are not in the intersection. This is why the item says to intersect by URL, not id.

Wider check against all 147 staged rows (`staged-docs.tsv`): no staged row cites the same document as any of S219-S225. The nearest neighbours are different documents:
- staged S201 `man.archlinux.org/man/alpm-hooks.5` is the rendered man page. S224 cites the asciidoc source at 54d9411.
- staged S217 `man.archlinux.org/man/PKGBUILD.5` is not the Arch packaging PKGBUILD.
- staged S228, S232 and S246 are PKGBUILD wiki pages.

None of these are quarantine-slice ids.

## 3. No staged row, id or text entered the lane corpus at f951f288

Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 53b294a… f951f288… -- corpus/SOURCES.md`. Receipt: `sources-diff.patch`.

Observed:
- 1 file changed, 7 insertions, 0 deletions (the `grep -c '^-[^-]'` count of removed lines is 0).
- The 7 added lines are S219-S225, each carrying the used-by `corpus/knowledge/pacman-exec-environment-r40.md`.
- `git diff --name-status … -- corpus/` shows exactly two changes (`corpus-name-status.txt`): `M corpus/SOURCES.md` and `A corpus/knowledge/pacman-exec-environment-r40.md`.

Cross-checks against `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` (147 staged rows, 70 staged knowledge targets):
- 0 of 147 staged rows appear as a full line in the tip SOURCES.md.
- 0 staged rows are identical to the lane row of the same id.
- Of 100 distinct staged URLs, none occurs in the 7 added lines.
- The 70 staged knowledge target paths were checked at both revisions. The only staged target present is `corpus/knowledge/errno-contract-variance-r37.md`. It exists at base and tip and is not in the round-40 diff. It was adopted in round 37 (commit 8936643, "round-37: assimilate sourced errno entries and quarantine gate"; MERGE-REPORT lines 59 and 104-112 map staged S279-S287 to it). It is not a round-40 entry.
- The only file added to `corpus/knowledge` in base..tip is `pacman-exec-environment-r40.md` (the lane's own C2 entry, not a staged target).
- Six staged URLs occur in tip corpus (`staged-urls-in-tip-corpus.txt`). All were already present at base and lie outside the round-40 diff. They are:
  - `man.archlinux.org/man/alpm-hooks.5` (lane S008)
  - `man.archlinux.org/man/mkinitcpio.8` (prose reference)
  - `man7.org/…/errno.3.html` (lane S202-S204)
  - `raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c` (lane S201)
  - `…/errno-base.h` (lane S205)
  - `devblog.archlinux.page/2026/on-scripts-and-hooks/` (lessons file)
  None of the six is a quarantine-slice document.

So round 40 introduced none of the staged rows, ids or text. The staged quarantine-slice documents (plymouth tags, Oracle Snapper, ArchWiki Translation Team, kernel translation indexes, gate-block-only own-work rows) are absent from corpus at f951f288 in every form (URL, row line, knowledge target).

## Not done
- The round prompt text itself was not available to this seat. I used the §10 awk command as recorded in round 39 (see section 1) and the F-3 row description in `w1-spec.json`. Its output matches the frozen slice byte for byte.
- I did not re-fetch any slice source. The slice is a register-derived list, not a verdict on those sources.
- I did not check staged rows against lane SOURCES.md for earlier-round overlaps beyond the id and URL checks above (the round-39 `assimilation/collisions` handling is outside F-3).
