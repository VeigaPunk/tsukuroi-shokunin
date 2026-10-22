# ExecSourcesCensus — round-28 wave-1 round-start census receipt

Verdict: done — the lane registry is clean under the maintained validator (exit 0, zero E-codes, 25 W04 warnings) and under the seven frozen `CORPUS.md` census commands (145 rows, 0 malformed, 0 duplicate ids, 0 enum violations, 0 missing used-by paths); the W04 set is 25 same-URL-across-scope advisories on rows that pair a superseded row with its `supersedes S0NN —` replacement.

Lane: `tsukuroi` → `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Registry under census: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
sha256 of the registry file: `84e0abea4fd7cdbe554b0e43ff4e8df72d9d8538e63dfc60f2091201a8c4bf63`
Lane tip under census: `f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0` (round-28 declaration commit); round base `3b9e0430b88d01415c241dd5a18b8939b8a520ac`.
Host tools: GNU bash 5.3.20(1), GNU Awk 5.4.1.

## 1. Maintained validator — `sources-census.sh validate`

Command (run from the fleet root; read-only, stdout only):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Exit code: `0`. Stderr: empty. Full stdout (26 lines, verbatim):

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
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Findings from that run:
1. [obs] Exit code 0 and a final `ok` line for the registry; 0 `E`-coded lines in the output (`grep -cE '\tE[0-9]{2}\t'` → 0), 25 `W04` lines, no `E01`–`E12`, no `W01`/`W02`/`W03`, no `unlisted` warning.
2. [obs] The validator treats W-codes as non-failing by contract (`scripts/sources-census.sh:33` "warnings do not affect clean lanes"; the same rule is asserted by the script's own selftest `checkx "W04-does-not-fail-validation" 0` at `scripts/sources-census.sh:364`), so exit 0 is consistent with 25 W04 advisories outstanding.
3. [obs] `census` mode on the same lane (`sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi`, exit 0) reports `rows 145`, `tier.A 135`, `tier.B 3`, `tier.C 7`, `status.mined 131`, `status.queued 5`, `status.rejected 9`, and `FLEET` mirrors the same numbers with `tier.invalid 0`, `status.invalid 0`, `missing 0` — i.e. under this invocation the tsukuroi lane is the only lane in the scope and it carries every fleet row counted.

## 2. Seven frozen census commands (`CORPUS.md` § "SOURCES.md — where a shokunin learns")

All seven were run from the lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, verbatim as frozen in `/home/vgpnk/Projects/shokunin/CORPUS.md` (the "Census — run from the lane root" block), against `corpus/SOURCES.md`.

| # | frozen command (abbreviated) | output |
|---|---|---|
| 1 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `145` (rows) |
| 2 | malformed rows `awk -F'|' '… && NF!=13 {n++} END{print n+0}'` | `0` |
| 3 | tier histogram `awk … t=$5 …` | `A=135 B=3 C=7` |
| 4 | status histogram `awk … s=$9 …` | `mined=131 queued=5 rejected=9` |
| 5 | duplicate ids `awk … print i' \| sort \| uniq -d` | no output (empty — no duplicate ids) |
| 6 | enum violations / tier inflation `awk … NF==13 …` | no output (empty) |
| 7 | mined rows whose `used-by` paths do not exist | no output (empty) |

Findings:
4. [obs] Row count 145; the id sequence is dense and gapless: ids run `S001`…`S145` with zero gaps (`min=001 max=145 gaps: []`), so no id was skipped or reused.
5. [obs] Malformed rows 0 — every registry row has NF=13, i.e. exactly the 11 contract columns plus the two boundary empties.
6. [obs] Duplicate ids: the frozen command printed nothing; there is no repeated `S###` id.
7. [obs] Enum violations and tier inflation: the frozen command printed nothing — every row's `kind` is in {spec,docs,paper,code,tool,dataset,talk,book,community,own-work}, `tier` in {A,B,C}, `status` in {queued,mined,rejected}; no row is `community` at tier A.
8. [obs] Missing `used-by` paths: the frozen command printed nothing — every path named by a `mined` row exists on disk relative to the lane root.
9. [obs] The frozen tier/status histograms (A=135 B=3 C=7; mined=131 queued=5 rejected=9) agree exactly with the maintained `census` mode totals in finding 3, so the frozen and maintained parsers see the same rows on this file.
10. [obs] Structural cross-check: the registry section spans `## Registry` at `corpus/SOURCES.md:3` to `## Paths` at `corpus/SOURCES.md:153`; all 145 row-shaped lines fall inside it, and an independent scan for row-shaped lines under a non-Registry heading found none (no E12 condition).
11. [obs] The registry file's bytes are identical in the lane working tree and in the exported lane tip (`git show HEAD:corpus/SOURCES.md | sha256sum` → `84e0abea…4bf63`, equal to the working-tree digest), so this receipt describes the committed tip and not an uncommitted edit.
12. [obs] Re-running the maintained validator on a read-only export of the tip (`git -C …/tsukuroi-shokunin archive f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 | tar -x -C /fast/scratch/hyaku/tsuku28/ExecSourcesCensus/tree`, then `sources-census.sh validate --file <export>/corpus/SOURCES.md --root <export>`) exited 0 and produced the same 25 W04 lines plus one `ok` line; the only difference from the lane run is the lane label (`file` instead of `tsukuroi`). The seven frozen commands on the export produced byte-identical results to the lane run (145 / 0 / A=135 B=3 C=7 / mined=131 queued=5 rejected=9 / empty / empty / empty).

## 3. The 25 W04 warnings, itemized

W04 fires when one canonical URL appears under two different `scope` values. The frozen manual census has no W04 command, so this list comes from the maintained validator, and each entry was expanded independently to show its partner rows and scopes (script: `/fast/scratch/hyaku/tsuku28/ExecSourcesCensus/w04-detail.txt`).

| W04 row | canonical URL | partner row(s) | relationship |
|---|---|---|---|
| S038 | man.archlinux.org/man/access.2 | S034 | S038 `teaches` opens `supersedes S034 —` |
| S041 | man.archlinux.org/man/systemd.exec.5 | S028, S044, S046 | S041 scopes ProtectSystem/ReadOnlyPaths/RootDirectory= on the same page S028 used for CapabilityBoundingSet |
| S042 | github.com/omacom/omarchy/issues/8047 | S036 | S042 `teaches` opens `supersedes S036 —` |
| S043 | github.com/omacom/omarchy/issues/6629 | S037 | S043 `teaches` opens `supersedes S037 —` |
| S044 | man.archlinux.org/man/systemd.exec.5 | S028, S041, S046 | S044 is the ProtectSystem= argument-domain row; S046 re-opens it as a locator refinement |
| S046 | man.archlinux.org/man/systemd.exec.5 | S028, S041, S044 | as above |
| S049 | man.archlinux.org/man/pacman.8 | S048, S089, S090, S106, S107 | five pacman(8) rows, one per option cluster |
| S058 | gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/init | S054 | S058 `teaches` opens `supersedes S054 —` |
| S082 | git-scm.com/docs/git-rev-parse/2.56.0 | S077 | same page, object-prefix vs object-type scope |
| S087 | archlinux.org/news | S001 | S001 is the archive index, S087 the dated 2026-10-01→2026-10-22 window |
| S089 | man.archlinux.org/man/pacman.8 | S048, S049, S090, S106, S107 | as S049 |
| S090 | man.archlinux.org/man/pacman.8 | S048, S049, S089, S106, S107 | as S049 |
| S092 | wiki.archlinux.org/title/System_maintenance?oldid=885170 | S010 | same revision, doctrine scope vs `pacman -Sy` repair scope |
| S095 | gitlab.archlinux.org/…/mkinitcpio/-/merge_requests/482 | S057 | same MR, purpose vs maintainer-intent scope |
| S098 | gitlab.com/Zesko/limine-entry-tool/…/btrfs-overlayfs | S021 | upstream-vs-installed comparison scope |
| S105 | archlinux.org/news/update-to-ca-certificates-mozilla-31311-1… | S088 | notice scope vs requested-version scope |
| S106 | man.archlinux.org/man/pacman.8 | S048, S049, S089, S090, S107 | as S049 |
| S107 | man.archlinux.org/man/pacman.8 | S048, S049, S089, S090, S106 | as S049 |
| S108 | wiki.archlinux.org/title/Downgrading_packages?oldid=887421 | S093 | cache-prerequisite scope vs fallback scope |
| S109 | gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/functions | S094 | symlink-creation scope vs build-root scope |
| S111 | gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook | S097 | exact-argument scope vs pkgrel-history scope |
| S126 | raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | S120 | S126 is the digest-correction re-opening of S120 |
| S136 | raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | S121 | candidate-property scope vs ManagedOOM* value scope |
| S137 | raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | S122 | service-page scope vs monitored-cgroup scope |
| S138 | raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | S118 | per-cgroup pressure/OOM-counter scope |

Findings:
13. [obs] Every W04 pair is a legitimate scope split of one source page or one issue thread, not a duplicate claim: the contract's rule 2 makes a superseding row a new row on the same URL, and rules 1 and 4 forbid collapsing scopes. The validator's E04 check (duplicate URL *within* a scope, absent `supersedes`) reported nothing, which is the paired evidence that no W04 pair is an accidental re-statement.
14. [inf] The 25 W04s therefore read as advisory noise on a conformant registry rather than a defect list; the round-28 gate question is whether the wave accepts them as-is. I do not propose edits: the contract is append-only and each W04 pair is already a documented supersession or a distinct scope.
15. [unk] Whether the L1 wants the W04 count reduced (for example by narrowing `scope` text on one row of each pair) is a curation decision outside this seat's scope; nothing in `SCOREPARD.md`'s round-28 declaration or in `CORPUS.md` requires a W04 count target.

## 4. Risks and blockers

16. [obs] No blockers: every command ran, none mutated lane state (no git/jj write command was issued against `/home/vgpnk/Projects/shokunin` or the lane; the only writes were this report and files under `/fast/scratch/hyaku/tsuku28/ExecSourcesCensus/`).
17. [obs] Lane working tree at census time carried two unrelated uncommitted items — `M tools/check-kernel-taint.py` and untracked `.ufo/waves/round-28/` — neither of which is the registry; the registry blob is identical to HEAD (finding 11), so this receipt is unaffected by them.
18. [unk] The frozen census block in `CORPUS.md` contains no W04 command, so "the W04 warnings" in this receipt are the maintained validator's advisory list; the frozen seven cannot reproduce them by construction.

Scope: read=/home/vgpnk/Projects/shokunin/CORPUS.md, /home/vgpnk/Projects/shokunin/scripts/sources-census.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-28 declaration), lane git history for corpus/SOURCES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/ExecSourcesCensus.md, /fast/scratch/hyaku/tsuku28/ExecSourcesCensus/{tree/,w04-detail.txt,validate-export.txt}; executed=sources-census.sh validate/census on the lane and on the tip export, the seven frozen CORPUS.md census commands on both trees, sha256sum/grep/awk verification of the registry, git archive export of the tip
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
