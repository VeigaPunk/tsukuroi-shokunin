Verdict: Clean baseline at the claim base: 114 registry rows, 0 malformed, 0 duplicate ids, 0 enum or tier-inflation violations, 0 missing used-by paths, 21 advisory W04 warnings, and validator output byte-identical to census-before.txt with every exit code 0.

Identity: the lane HEAD is 6c580b155840c8750a7bb5f14dcb8e48913d0073 (the declaration commit). The claim base b9046016831237cd04d38da11ba76e50d5380c53 is its ancestor. corpus/SOURCES.md has identical bytes in the working copy, at the base and at the declaration: sha256 bfb9f48e20060877f40910db2b6a53bb205b4b9a8cbc365f739d56fa9c4de2a0, 115,719 bytes. This census therefore describes all three.

Axes read: integrity (malformed rows, duplicate ids, enum violations, missing used-by paths), warnings (W04), identity (base, declaration, working copy), and agreement (validator, frozen manual commands, census mode). Every axis is clean except the advisory W04 count, which matches the before file.

## Findings

1. [obs] Validator output matches the frozen before file byte for byte. Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`, run from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Exit 0. Stdout has 22 lines: 21 `W04` lines and one `ok` line naming `corpus/SOURCES.md`. Saved with its exit line as `.ufo/waves/round-25/w1/RevCensusBefore/validate-now.txt`. `cmp` against `.ufo/waves/round-25/measure/census-before.txt` (23 lines, last line `exit=0`) returned 0. No E01 to E12 codes appear. W01, W02 and W03 do not appear.

2. [obs] The seven frozen manual census commands all exit 0. They were parsed verbatim from `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 133 to 148 and run with bash from the lane root. Each left stderr empty. Raw output: `.ufo/waves/round-25/w1/RevCensusBefore/manual-census-now.txt`.

| Command | CORPUS.md line | Output | Exit |
|---|---|---|---|
| M1 rows | 135 | 114 | 0 |
| M2 malformed rows (NF is not 13) | 137 | 0 | 0 |
| M3 tier histogram | 139 | A=106 B=1 C=7 (sum 114) | 0 |
| M4 status histogram | 141 | mined=100 queued=5 rejected=9 (sum 114) | 0 |
| M5 duplicate ids | 143 | none | 0 |
| M6 enum violations and tier inflation | 145 | none | 0 |
| M7 mined rows with missing used-by paths | 147 | none | 0 |

3. [obs] Census mode agrees with the manual commands. `sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi` exited 0 and printed rows 114; tier.A 106, tier.B 1, tier.C 7, tier.invalid 0; status.mined 100, status.queued 5, status.rejected 9, status.invalid 0; missing 0. Saved as `.ufo/waves/round-25/w1/RevCensusBefore/census-now.txt`.

4. [obs] Used-by paths are clean for every row, not only mined rows. M7 and validator E11 both check used-by paths only for `mined` rows (validator line 559 skips other rows). I also checked every named path in every row. 102 rows name at least one path other than the dash, and every named path exists. The two non-mined rows with paths are S045 (rejected; `corpus/knowledge/source-scope-correction-r14.md`) and S080 (rejected; `corpus/lessons/round-20.md`). Pointers: the rows with those ids in `corpus/SOURCES.md`.

5. [obs] The 21 W04 warnings are the same ids the validator printed. W04 means that the same normalized URL appears again under a different scope. I re-implemented the validator's URL normalization (validator lines 600 to 605) and its W04 test (lines 644 to 645). The re-implementation reproduces the same 21 ids. Fifteen URL groups hold more than one row (36 rows in total). Two are large: the `pacman.8` group (S048, S049, S089, S090, S106, S107) and the `systemd.exec.5` group (S028, S041, S044, S046). The first-row column below is derived, so it is marked [inf]. Status: 19 mined, 2 rejected (S042, S043).

   | W04 id | Status | First row with same URL [inf] | Opens `supersedes` (superseded row) | Normalized URL |
   |---|---|---|---|---|
   | S038 | mined | S034 | yes (S034) | man.archlinux.org/man/access.2 |
   | S041 | mined | S028 | no | man.archlinux.org/man/systemd.exec.5 |
   | S042 | rejected | S036 | yes (S036) | github.com/omacom/omarchy/issues/8047 |
   | S043 | rejected | S037 | yes (S037) | github.com/omacom/omarchy/issues/6629 |
   | S044 | mined | S028 | no | man.archlinux.org/man/systemd.exec.5 |
   | S046 | mined | S028 | no | man.archlinux.org/man/systemd.exec.5 |
   | S049 | mined | S048 | no | man.archlinux.org/man/pacman.8 |
   | S058 | mined | S054 | yes (S054) | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init |
   | S082 | mined | S077 | no | git-scm.com/docs/git-rev-parse/2.56.0 |
   | S087 | mined | S001 | no | archlinux.org/news |
   | S089 | mined | S048 | no | man.archlinux.org/man/pacman.8 |
   | S090 | mined | S048 | no | man.archlinux.org/man/pacman.8 |
   | S092 | mined | S010 | no | wiki.archlinux.org/title/System_maintenance?oldid=885170 |
   | S095 | mined | S057 | no | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 |
   | S098 | mined | S021 | no | gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs |
   | S105 | mined | S088 | yes (S088) | archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks |
   | S106 | mined | S048 | yes (S089) | man.archlinux.org/man/pacman.8 |
   | S107 | mined | S048 | yes (S090) | man.archlinux.org/man/pacman.8 |
   | S108 | mined | S093 | yes (S093) | wiki.archlinux.org/title/Downgrading_packages?oldid=887421 |
   | S109 | mined | S094 | yes (S094) | gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions |
   | S111 | mined | S097 | yes (S097) | gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook |

   [inf] Ten of the 21 rows open with the correction form that the contract asks for, `supersedes S0NN —` (CORPUS.md lines 117 to 118). The validator's E04 check exempts those rows from its duplicate test (validator line 648), but W04 does not, so they still warn. The other 11 reuse a URL that an earlier row already cites under another scope. W04 is advisory: only E-codes change the status (validator line 739; header lines 31 to 33).

6. [inf] The W04 count rose after round 20. `LOG.md` line 997 records round 19 starting at 65 rows and eight W04 warnings. `LOG.md` line 1061 records round 20 ending at 80 rows with eight existing W04 duplicates. The eight W04 ids at or below S080 (S038, S041, S042, S043, S044, S046, S049, S058) match that count. The other 13 ids (S082 to S111) fall in rows added after round 20. Nothing fails because of this: W04 is a warning.

7. [obs] Registry identity holds across base, declaration and working copy. `git --no-optional-locks merge-base --is-ancestor b9046016831237cd04d38da11ba76e50d5380c53 6c580b155840c8750a7bb5f14dcb8e48913d0073` exited 0. `git --no-optional-locks diff --stat` of `corpus/SOURCES.md` between those two commits printed nothing. `git --no-optional-locks status --porcelain -- corpus/SOURCES.md` printed nothing. The base blob, the declaration blob and the working file share one sha256.

8. [obs] Ids are contiguous, and the next free id is S115. The 114 distinct ids run from S001 to S114 with no gaps. The file names no id that lacks a row, and no id from S115 upward appears. This matches the next free id named in the assignment.

9. [obs] Dates are clean, and 28 rows were opened on 2026-10-22. `opened` runs from 2026-10-19 to 2026-10-22, so validator E08 is clean against `--today` 2026-10-22 (the default is `date -u +%F`, validator line 90). Rows S087 to S114 (28 rows) carry 2026-10-22. [inf] The C2 route through an opened-today row needs a `mined` row whose `used-by` names the new entry. An existing row would therefore need a `used-by` edit to qualify. Rule 2 requires any in-place `used-by` change to be logged old to new in the round lesson (CORPUS.md lines 116 to 118).

10. [obs] Recheck values: `on-release` 79, `90d` 16, `180d` 15, `30d` 3, `every capture` 1 (row S101, mined, tier A). The validator accepts `every capture` as a symbolic cadence (validator lines 582 and 665; no E09). The contract's examples are `90d`, `180d` and `on-release` (CORPUS.md lines 105 to 106). [unk] The contract text does not say whether that example list is closed. If it is closed, S101 departs from the contract and the validator does not catch it.

11. [obs] Tier, kind and status profile. Kinds: docs 60, own-work 23, code 22, community 5, tool 2, dataset 2 (sum 114). Tier by status: A mined 99, B mined 1, C rejected 7, A queued 5, A rejected 2. No community row is tier A (E10 clean). No tier-C row is mined (W01 clean). The shortest rejected `teaches` is 180 characters (W02 clean).

12. [inf] Three rejected rows open with the correction form, not with `REJECTED:`. Rows S042, S043 and S045 begin `supersedes S0NN — REJECTED: ...`, and each also contains `; flip:`. The other six rejected rows (S029, S030, S033, S036, S037, S080) begin `REJECTED:`. The contract gives both openers (CORPUS.md lines 101 to 102 for rejected rows, lines 117 to 118 for corrections) and does not say which wins for a rejected correction. The validator checks neither opener. Low severity; a future contract version should settle it.

13. [obs] One stale count sits in the Capabilities table, outside the C1 check set as written. `SCORECARD.md` line 161 (the `sources-registry` row) says "34 rows, malformed 0" and cites `.ufo/evidence/round-1-kaika/after.md`, which exists. The registry now holds 114 rows. The row is anchored to round 1, so the figure is historical rather than a current claim. [inf] The C1 check set (SCORECARD.md line 795, K16 to K19) tests only repository paths and the host-census-gate case count, so this figure falls outside K01 to K23 as written. Reported for the L1; not edited.

14. [obs] Tool provenance. `scripts/sources-census.sh` sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30. `census-before.txt` sha256 2eb5c00f67ebd6974f26108efff49f6017d1183535db2e8b255b8a49a8c7258e. Registry sha256 bfb9f48e20060877f40910db2b6a53bb205b4b9a8cbc365f739d56fa9c4de2a0. Runtime: GNU Awk 5.4.1 at /usr/bin/gawk and GNU bash 5.3.20. [inf] The before file records no script hash, so the byte match shows that the present script reproduces the before output. It does not prove which script wrote the before file.

15. [unk] No frozen comparator exists for the manual numbers. census-before.txt holds validator output only: no row, tier, status, duplicate or used-by values. The only frozen comparison is the validator output, plus the identical registry bytes at base and declaration.

16. [obs] Installs: none. No tool was installed or updated. No lane file was edited. The only files written are this report and four outputs in `.ufo/waves/round-25/w1/RevCensusBefore/`.

## Residual risk and verification gaps

- The first-row column in finding 5 comes from my re-implementation of the validator's URL normalization. The 21 ids match the validator's output exactly, so only the pairings are derived.
- The `overdue` and `shared` modes were not run. They sit outside this census.
- No LSP query was made. The inputs are one markdown table and one bash script, so no code caller or definition check applied.
- E08 depends on the date. It is clean at 2026-10-22, the default UTC date used by the validator.

Scope: read=CORPUS.md 64-200 (SOURCES contract and census block); SCORECARD.md 784-801 and a grep of lane docs for SOURCES counts; census-before.txt 1-23; scripts/sources-census.sh 1-300 and 538-693 plus a grep; corpus/SOURCES.md through the validator and Python; LOG.md 997 and 1061; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevCensusBefore.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevCensusBefore/validate-now.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevCensusBefore/census-now.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevCensusBefore/manual-census-now.txt, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevCensusBefore/w04-pairs-now.txt; executed=sources-census.sh validate and census (exit 0 each); the seven CORPUS.md census commands (exit 0 each); read-only git with --no-optional-locks (rev-parse, show, merge-base --is-ancestor, diff --stat, status --porcelain); cmp; date -u +%F; command -v gawk awk mawk; gawk --version; bash --version; test -e on the round-1 evidence path; grep over lane docs; Python re-implementation of the W04 test and registry tallies
Model: anthropic/claude-haiku-5-5 (host context field; not independently verified)
Installs: none
