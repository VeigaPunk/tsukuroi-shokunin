VERDICT: supports

Item N-3 — sources census. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin tsukuroi` exits 0 with `ok` and only 40 W04 (same-URL across
scopes) warnings; the seven frozen manual census commands of `CORPUS.md` §Census (lines 134-147)
report **0 malformed, 0 duplicate ids, 0 enum violations, 0 missing used-by** at both
6951ead90566b2d74f7c45b4efca29246badad64 (base) and
8acf0b022586a0f3164c77659fb96ba5f90949b6 (tip), with rows 239 → 241 (the two added rows are
S240 and S241, both `mined`/tier A, both also `mined` in the maintained parser). The maintained
validator and the frozen manual commands agree on every count.

## 1. Substrate (nothing ran against the lane worktree except read-only reads)

Scratch root `/fast/scratch/hyaku/tsukuroi-r43/SourcesCensusFinal`, shared clones of the lane:

    $ git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/fx-after
    $ git -C $S/fx-after remote remove origin
    $ git -C $S/fx-after checkout 8acf0b022586a0f3164c77659fb96ba5f90949b6
    $ git -C $S/fx-after rev-parse --show-toplevel
    /fast/scratch/hyaku/tsukuroi-r43/SourcesCensusFinal/fx-after
    $ git -C $S/fx-after rev-parse HEAD
    8acf0b022586a0f3164c77659fb96ba5f90949b6
    (same recipe for fx-before at 6951ead90566b2d74f7c45b4efca29246badad64, HEAD confirmed equal)

`git show` bytes and the checkout bytes are identical, so `used-by` paths resolve against the
frozen tree and not against untracked files:

    $ git -C <lane> show 8acf0b02…:corpus/SOURCES.md | sha256sum
    b34dc1cd60ccf2eae51e4f434203216c88df2a524cf6675a2487067607691ccf
    $ cmp $S/SOURCES.8acf0b02.md $S/fx-after/corpus/SOURCES.md && echo IDENTICAL
    IDENTICAL after-checkout vs git-show 8acf0b02
    $ git -C <lane> show 6951ead…:corpus/SOURCES.md | sha256sum
    0ea5dcb6dc7d24055532e0bbd3fb3e65c464a0219280370ab2bd6efc29604971
    IDENTICAL before-checkout vs git-show 6951ead

The lane's **working tree** `corpus/SOURCES.md` is still byte-identical to the frozen tip
(sha256 `b34dc1cd…1ccf`) although lane HEAD is `64646d6e5749e0b5b6e458aa0753d39c47404e6b`
(wave-2 in flight), so the asked `validate` run below reads exactly the text under test.

Tools: GNU Awk 5.4.1, bash 5.3.20, git 2.56.0, `/usr/bin/grep` = GNU grep 3.12-modified.
`grep` is also a shell builtin in the session shell, so each command was re-run under
`env -i PATH=/usr/bin:/bin bash --noprofile --norc -x` and compared: **identical output**
(`diff $S/out.after.session $S/out.after.pristine` → empty). Nothing installed or upgraded.

## 2. Maintained validator (command as given, exit code, findings)

    $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
        --root /home/vgpnk/Projects/shokunin tsukuroi ; echo "[exit $?]"
    tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
    tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
    tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
    tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
    tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
    tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
    tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
    tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/init across scopes
    tsukuroi	W04	S082 duplicate url git-scm.com/docs/git-rev-parse/2.56.0 across scopes
    tsukuroi	W04	S087 duplicate url archlinux.org/news across scopes
    tsukuroi	W04	S089 duplicate url man.archlinux.org/man/pacman.8 across scopes
    tsukuroi	W04	S090 duplicate url man.archlinux.org/man/pacman.8 across scopes
    tsukuroi	W04	S092 duplicate url wiki.archlinux.org/title/System_maintenance?oldid=885170 across scopes
    tsukuroi	W04	S095 duplicate url gitlab.archlinux.org/…/mkinitcpio/-/merge_requests/482 across scopes
    tsukuroi	W04	S098 duplicate url gitlab.com/Zesko/limine-entry-tool/…/hooks/btrfs-overlayfs across scopes
    tsukuroi	W04	S105 duplicate url archlinux.org/news/update-to-ca-certificates-mozilla-…-attacks across scopes
    tsukuroi	W04	S106 duplicate url man.archlinux.org/man/pacman.8 across scopes
    tsukuroi	W04	S107 duplicate url man.archlinux.org/man/pacman.8 across scopes
    tsukuroi	W04	S108 duplicate url wiki.archlinux.org/title/Downgrading_packages?oldid=887421 across scopes
    tsukuroi	W04	S109 duplicate url gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/functions across scopes
    tsukuroi	W04	S111 duplicate url gitlab.archlinux.org/…/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook across scopes
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
    tsukuroi	W04	S221 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c across scopes
    tsukuroi	W04	S222 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c across scopes
    tsukuroi	W04	S223 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c across scopes
    tsukuroi	W04	S224 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc across scopes
    tsukuroi	W04	S226 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc across scopes
    tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes
    tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
    [exit 0]

(six long URLs — S058, S095, S098, S105, S109, S111 — are elided with `…` in this transcription
only; the unedited 41-line output is receipt `SourcesCensusFinal/validate.live.out`.) **exit 0**, 40 × W04, no E-code, no W01/W02/W03,
terminal `ok`. W04 is the documented warning class (`sources-census.sh:32`) and does not affect
status. No E04 (duplicate URL *and* scope) fires, so the W04s are distinct-scope reuses.
E11 (`used-by path missing on disk`, checks `mined` rows, base dir = lane dir —
`sources-census.sh:538-575`, `:721`) is silent, which also proves the run resolved paths against
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` and not the fleet root.

Same validator over both frozen trees (hermetic, explicit dir argument → lane name
`fx-after`/`fx-before`, base dir = that checkout):

    $ sources-census.sh validate $S/fx-after  > validate.after.out  ; echo "[exit $?]"
    [exit 0]   # 40 W04 + `fx-after ok …/fx-after/corpus/SOURCES.md`
    $ sources-census.sh validate $S/fx-before > validate.before.out ; echo "[exit $?]"
    [exit 0]   # 40 W04 + `fx-before ok …/fx-before/corpus/SOURCES.md`

The W04 message set is **identical** tip vs base (`comm -13 w04.before w04.after` → empty): the
two new rows add no new finding, and the live-vs-checkout finding sets diff to nothing after
normalising lane name/path (`diff live.norm after.norm` → empty).

## 3. The seven frozen manual census commands (verbatim, `CORPUS.md:134-147`)

Fidelity: the harness's command lines were diffed against `CORPUS.md` lines 134-148 with comment
and fence lines removed → **no difference** (`diff corpus.cmds script.cmds` printed only the
closing ```` ``` ```` line of the corpus block). Run from a lane root, so `corpus/SOURCES.md`
and every relative `used-by` path is the frozen tree.

    # rows (spacing-tolerant)
    grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
    # malformed rows — 11 columns means NF=13; must print 0
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
    # tier histogram
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
    # status histogram
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
    # duplicate ids — must print nothing
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
    # enum violations and tier inflation — must print nothing
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
    # mined rows whose used-by paths do not exist — must print nothing
    awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done

Observed output, `fx-after` = 8acf0b02 (`corpus/SOURCES.md` sha256 `b34dc1cd…1ccf`):

    cmd1 rows          → 241
    cmd2 malformed     → 0
    cmd3 tier          → A=226 B=5 C=10 
    cmd4 status        → mined=215 queued=5 rejected=21 
    cmd5 dup ids       → (no output)
    cmd6 enum          → (no output)
    cmd7 missing used-by → (no output)

Observed output, `fx-before` = 6951ead (`corpus/SOURCES.md` sha256 `0ea5dcb6…4971`):

    cmd1 rows          → 239
    cmd2 malformed     → 0
    cmd3 tier          → A=224 B=5 C=10 
    cmd4 status        → mined=213 queued=5 rejected=21 
    cmd5 dup ids       → (no output)
    cmd6 enum          → (no output)
    cmd7 missing used-by → (no output)

`grep -c '^missing:'` on both full xtrace logs: **0**. Raw logs (798 / 792 lines, `set -x` so
every `[ -e … ]` test is visible): `SourcesCensusFinal/census7.after.log`,
`SourcesCensusFinal/census7.before.log`.

## 4. Before/after table (both sources agree)

| metric | 6951ead (base) | 8acf0b02 (tip) | source |
|---|---|---|---|
| rows | 239 | 241 | cmd1 = `census` mode `rows` |
| malformed (NF≠13) | 0 | 0 | cmd2 |
| tier A / B / C | 224 / 5 / 10 | 226 / 5 / 10 | cmd3 = `census` `tier.*` |
| status mined / queued / rejected | 213 / 5 / 21 | 215 / 5 / 21 | cmd4 = `census` `status.*` |
| duplicate ids | 0 | 0 | cmd5 = E03 |
| enum violations / tier inflation | 0 | 0 | cmd6 = E05/E06/E07/E10 |
| missing used-by (mined rows) | 0 | 0 | cmd7 = E11 |
| duplicate URL+scope | 0 | 0 | E04 (validate) |
| W04 same-URL across scopes | 40 | 40 (same set) | validate |
| validator exit | 0 (`ok`) | 0 (`ok`) | validate |

Maintained `census` mode at the tip, for cross-check of every manual number:

    $ sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi ; echo "[exit $?]"
    tsukuroi	rows	241
    tsukuroi	tier.A	226
    tsukuroi	tier.B	5
    tsukuroi	tier.C	10
    tsukuroi	status.mined	215
    tsukuroi	status.queued	5
    tsukuroi	status.rejected	21
    FLEET	rows	241 / tier.A 226 / tier.B 5 / tier.C 10 / tier.invalid 0
    FLEET	status.queued 5 / status.mined 215 / status.rejected 21 / status.invalid 0
    FLEET	missing	0
    [exit 0]

Sum checks close: 226+5+10 = 241 and 215+5+21 = 241 at the tip; 224+5+10 = 239 and
213+5+21 = 239 at the base.

## 5. Structural checks the seven commands do not cover (all clean)

- **Column-zero assumption holds**, so the frozen regexes and the maintained 0-3-space parser
  cannot disagree: `grep -cE '^[[:space:]]+\|[[:space:]]*S[0-9]{3,}'` → **0** at both revisions.
- **Every row sits in `## Registry`**: row-shaped lines anywhere in the file = 241 (tip) / 239
  (base), equal to the in-registry count; no E12 from the validator. `## Paths` (tip line 252)
  holds prose bullets, not `S###` rows.
- **Ids are contiguous**: S001..S241 (tip) and S001..S239 (base), `diff` against `seq 1 241` /
  `seq 1 239` empty; no id gaps hiding behind the duplicate check.
- **Id shape** uniform (`S0nn`/`Snnn`); no used-by cell contains `;`, so cmd7's `[,;]` split and
  the validator's `,`-only split (`sources-census.sh:565`) see the same 83 distinct target files.
- **No used-by target is absolute and none is a directory**; all 83 distinct targets exist in the
  clean 8acf0b02 checkout.
- **Non-`mined` rows carry 9 used-by cells** (S045, S080, S147, S151, S160, S161, S170, S178,
  S179 → `corpus/knowledge/source-scope-correction-r14.md`, `corpus/lessons/round-{20,28,29,30,31,32}.md`,
  `corpus/knowledge/btrfs-space-r30.md`). All exist. Both cmd7 and E11 skip non-`mined` rows by
  design (`sources-census.sh:558`), so that class is unchecked by the frozen commands — a
  **coverage note, not a defect here** (checked manually, 8/8 distinct paths present).

## 6. Cross-claim consistency with this wave's C2 rows

The registry delta is exactly the two round-43 C2 sources, and the digest recorded in each row
matches the frozen artifact on disk (read-only `sha256sum`, working tree):

| row | line at tip | kind/tier/status | anchor digest in row | observed digest of the frozen artifact |
|---|---|---|---|---|
| S240 | 249 | code / A / mined | `7b3488f2f835…4534ba01` | `.ufo/waves/round-43/frozen/src/ioctl.c` = `7b3488f2…4ba01` ✔ |
| S241 | 250 | own-work / A / mined | `f7ecbe7c990e…1242c556` | `.ufo/waves/round-43/frozen/hostcap/capture.txt` = `f7ecbe7c…2c556` ✔ |
| S237 | 246 | code / A / mined | `48df2e2f468f…8ed8f0801` | `.ufo/waves/round-42/frozen/src/scrub.c` = `48df2e2f…f0801` ✔ |

Used-by cells: S237 → `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`;
S240 and S241 → `corpus/knowledge/btrfs-scrub-record-r43.md`. Ids and digests therefore line up
with the frozen C2 claim (S237/S240/S241, `…0801` / `…ba01` / `…c556`) and their targets exist.

## 7. What I did not do

- No network re-open of the 226 tier-A URLs; a row's `teaches`/`anchor` reachability is out of
  this item's scope and is not established by any count here.
- No content reading of the 83 used-by knowledge/lesson files — only their existence.
- Did not run `sources-census.sh selftest`, `overdue`, `shared`, or any other lane (other seats'
  items); did not touch the round-42/43 C1 counters or the C2 counter.
- Did not run the validator over all fleet lanes; only `tsukuroi` plus my two hermetic checkouts.
- The 40 W04 warnings are pre-existing at both revisions and are warnings only; I did not judge
  whether those same-URL-different-scope rows should be merged (that is a registry-curation call,
  not a census result).

## 8. Receipts

`SourcesCensusFinal/`: `census7.sh` (the seven commands, verbatim), `census7.after.log`,
`census7.before.log` (full `bash -x`), `validate.live.out`, `validate.after.out`,
`validate.before.out`, `checksums.txt`.
