VERDICT: defect-found

## Finding

**Assimilation: none.** The staged append is not a safe append against the present lane registry: identifier overlap is directly measured below, including the declared S242–S249 collision subset. Independently, the absent-defect register marks multiple tsukuroi rows, including S230, as having no locator, so those claims are quarantined pending source-level review rather than admitted as evidence.

## Receipts

- `MERGE-REPORT.md:5-9` reports 147 proposed rows and says the lane registry holds 199 rows with first staged id S200. `SOURCES.append.md:5-6` is the staged 11-column table.
- Quarantine extraction (register rows whose lane cell is `tsukuroi`) written to `.ufo/waves/round-45/a2w1/AsmGate/quarantine-slice`: 13 matching table rows. It contains S211 and S213 payload-absent rows, plus S225, S230, S231, S242-S244, and S249-S252 rows for which the gate named no locator. Register source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:229-230,366-375`.
- ID collision check (`reg-ids` versus `staged-ids`; normalize markdown cell whitespace/backticks, retain S-number identifiers) written to `.ufo/waves/round-45/a2w1/AsmGate/id-collisions.txt`. Observed 183 registry ids, 147 staged ids, 30 intersections: S200, S201, S202, S205, S206, S209, S210, S211, S213, S222, S223, S224, S225, S228, S230, S231, S235, S236, S237, S238, S239, S242, S243, S244, S249, S250, S251, S252, S262, S268. In particular required S242-S249 overlap subset: **S242, S243, S244, S249**.
- Guard fixture: created indented scratch markdown rows (two leading spaces) with matching S999; the 0–3-indent extraction produced `fixture_ids=S999`, proving the leading-indent branch recognizes the fixture. Scratch fixture was under `/fast/scratch/hyaku/tsukuroi-r45/AsmGate/` only.

## Reject at least

Reject staged **S230** (own-work Snapper EACCES entry) for intake pending a properly located, re-openable citation: the register’s quarantine slice explicitly says `round3 | S230` and “the gate block named no locator, so no quote was checked” (register `:367`; slice line 5). The source target named by the staged row is the lane’s own `corpus/knowledge/snapper-eacces-mechanism.md`, not an independent external source (`SOURCES.append.md:37`). This is a source-validation defect, not a conclusion that the underlying host observation is false.

**Theme fit:** none of the examined staged rows supplies evidence for this round’s three narrow surfaces (C1 census first-line robustness; scrub speed sysfs parser / device-replace behavior; systemd stop signal sequence). The staged Btrfs ioctl entry S223 is adjacent filesystem material, not the scrub-speed parser or replace/stop mechanism; its staged knowledge text itself describes interface/flags rather than behavior (`knowledge/corpus/knowledge/btrfs-ioctl-surface-r27.md:9-14,58-63`). The v7.2 upstream UAPI header likewise defines `BTRFS_SUBVOL_*` masks/flags and ioctl argument structs (URL https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/btrfs.h, accessed 2026-10-27; located declarations `BTRFS_SUBVOL_RDONLY`, `BTRFS_SUBVOL_CREATE_ARGS_MASK`, `BTRFS_SUBVOL_DELETE_ARGS_MASK`, `struct btrfs_ioctl_scrub_args`), not the current round’s sysfs parser or systemd stop semantics. The only possible foothold is broad btrfs subject overlap; it does not meet this round’s exact theme.

No campaign tools were run and no source/staged merge files were modified. No tools installed.

## Correction (round 46, R45C-ASMGATE-RECEIPT)

The id figures above ("183 registry ids, 147 staged ids, 30 intersections") do not reproduce against the bytes at
round 45's measured revision `44560592857660a20c6a2b296fa14fa7a90464b5` (`SCORECARD.md:2908`). Recounted in round 46
with the round prompt's 0-3-leading-space extractor: lane registry **249** ids (S001-S249), staged **147** ids
(S200-S346), intersection **50** (S200-S249).

```sh
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
K=/home/vgpnk/Projects/shokuknow
$ git -C "$L" show 44560592857660a20c6a2b296fa14fa7a90464b5:corpus/SOURCES.md \
    | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]{3,}' | sort -u > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$K/merge/tsukuroi/SOURCES.append.md" \
    | grep -oE 'S[0-9]{3,}' | sort -u > staged-ids
$ wc -l < reg-ids ; wc -l < staged-ids ; comm -12 reg-ids staged-ids | wc -l
249
147
50
$ sed -n '1p;$p' reg-ids ; sed -n '1p;$p' staged-ids ; comm -12 reg-ids staged-ids | sed -n '1p;$p'
S001
S249
S200
S346
S200
S249
```

The gap is not an indentation convention. At that revision every row of `corpus/SOURCES.md` starts at column 0, and
every plausible variant of the extractor returns 249: `grep -cE '^\| S[0-9]'` -> 249, `grep -cE '\| *S[0-9]{3,}'` ->
249, unique `S[0-9]{3}` tokens -> 249. A fixture carrying rows at 0, 1, 2, 3 and 4 leading spaces (plus one `- S006`
list item) shows the 0-3 branch returning `S001 S002 S003 S004` and dropping the 4-space row and the list item, so
the extractor does recognize the permitted indent and still counts 249.

The kept `AsmGate/id-collisions.txt` (30 lines) therefore does not back its own "30 intersections". Five of its ids
are not lane registry ids at that revision - **S250, S251, S252, S262, S268** (each is present in `staged-ids`) - and
it omits 25 genuine collisions: **S203, S204, S207, S208, S212, S214, S215, S216, S217, S218, S219, S220, S221, S226,
S227, S229, S232, S233, S234, S240, S241, S245, S246, S247, S248**. Only 25 of the 50 real collisions appear in it.

```sh
$ wc -l < .ufo/waves/round-45/a2w1/AsmGate/id-collisions.txt
30
$ comm -23 listed reg-ids | tr '\n' ' '   # listed, but not a lane registry id
S250 S251 S252 S262 S268
$ comm -13 listed collisions | tr '\n' ' '   # genuine collisions the kept file omits
S203 S204 S207 S208 S212 S214 S215 S216 S217 S218 S219 S220 S221 S226 S227 S229 S232 S233 S234 S240 S241 S245 S246 S247 S248
$ comm -13 listed collisions | wc -l
25
```

Cite `.ufo/waves/round-45/assimilation/collisions` - the true 50-line collision set, S200-S249, with `reg-ids` (249
lines) and `staged-ids` (147 lines) beside it in the same directory - for round 45's collision set, not this receipt.
The substantive finding above is unaffected and is understated rather than overstated: staged rows S200-S249 collide
with an existing lane registry id, which is the reason not to append the staged registry as-is.
