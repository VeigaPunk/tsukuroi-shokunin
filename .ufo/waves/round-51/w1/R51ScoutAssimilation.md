VERDICT: defect-found

Assimilation collision guard for staged `merge/tsukuroi` against the live lane registry. Adopted nothing. Read-only on `/home/vgpnk/Projects/shokuknow`. No campaign tool run there. No tool installed.

## Collision guard

Pattern (round prompt): `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` then `comm -12`.

| side | file | count | numeric range | lexical ends |
|---|---|---|---|---|
| lane registry | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` | 256 | S001–S256 | S001 .. S256 |
| staged append | `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` | 147 | S200–S346 | S200 .. S346 |
| collisions | `comm -12` | **57** | **S200–S256** | S200 .. S256 |

Collision list (contiguous, no gaps): S200 S201 S202 S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S222 S223 S224 S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238 S239 S240 S241 S242 S243 S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255 S256.

Staged ids not in the lane registry: 90 (S257–S346). Registry duplicate ids: 0. Staged duplicate ids: 0. Indented hits (1–3 leading spaces) in either real file: 0. Over-indent (`^ {4,}\|`) in either real file: 0.

`MERGE-REPORT.md:9` says the lane registry "currently holds **199** rows; first staged id is **S200**". Observed registry is 256 rows and already occupies S200–S256, so that sentence is stale and the staged S200–S256 block collides with live rows. Same ids name different sources (example: lane S200 is mount(2) at `corpus/SOURCES.md:209`; staged S200 is mkinitcpio(8) at `SOURCES.append.md:7`).

## Indent proof (scratch registry)

Scratch file (removed after copy): `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutAssimilation/scratch-registry.md`, sole content `  | S200 |` (two leading spaces). Receipt copy: `.ufo/waves/round-51/w1/R51ScoutAssimilation/proof-scratch-registry.md`.

| pattern | matches | exit |
|---|---|---|
| `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | `  \| S200` (1 line) | 0 |
| `^\|[[:space:]]*S[0-9]{3,}` (column-zero) | none (0 bytes) | 1 |

`comm -12` of the 0–3-space extract against itself yields `S200`. Column-zero extract is empty, so its collision file is 0 bytes. Proof: the 0–3-space pattern finds the indented row; the column-zero pattern finds none.

## Quarantine slice (lane `tsukuroi`)

Source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

Command (round prompt):

```
awk -F'|' -v l='tsukuroi' 'NF>=4 && $2 ~ "^ `" l "`$" { print }'
```

Data-row count: **12**. Ids (staged S-space, not the live registry's meanings):

| id | class / why |
|---|---|
| S211 | payload-absent (register:229) |
| S213 | payload-absent (register:230) |
| S225 | never checked — source unfetched (register:366) |
| S230 | never checked — no locator (register:367) |
| S231 | never checked — no locator (register:368) |
| S242 | never checked — no locator (register:369) |
| S243 | never checked — no locator (register:370) |
| S244 | never checked — no locator (register:371) |
| S249 | never checked — no locator (register:372) |
| S250 | never checked — no locator (register:373) |
| S251 | never checked — no locator (register:374) |
| S252 | never checked — no locator (register:375) |

The by-lane total `| tsukuroi | 2 |` (register:253) counts only the payload-absent section. The 12-row slice also includes the NEVER CHECKED section.

## Theme and candidates (not adopted)

Theme: **mkinitcpio hook API and the mkinitcpio-42 boot-recovery gate** (initramfs / boot health). Inside PROVINCE.md Core: "Initramfs v42 and boot recovery" (`PROVINCE.md:22`, entry `corpus/knowledge/initramfs-v42-sysroot-recovery.md`). Package context: `MERGE-REPORT.md:5-9` (147 rows, 70 knowledge entries, first staged id S200). None of the three files exist in the lane corpus today.

All three candidates' cited staged ids are inside the collision range. None of those ids are in the 12-row quarantine slice. Adoption later requires renumbering in scratch onto ids past S256 (first free staged id S257); do not reuse S200–S256.

1. `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/initramfs-hook-api-r25.md` — five runtime hook points (`run_earlyhook` … `run_emergencyhook`) and the v38 hook-migration precedent. Cites staged **S200** (mkinitcpio(8)), **S210** (Arch news, mkinitcpio hook migration). Both collide. Not quarantined. Lane files of those ids are different sources (`SOURCES.md:209` mount(2); `SOURCES.md:219` libalpm trans.c).

2. `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/mkinitcpio-42-upgrade-gate-cjk-r26.md` — Chinese mkinitcpio ≥42 TPM2/PCR re-enroll notice and Japanese emergency-shell / fallback-image notes. Cites staged **S221**, **S216**. Both collide. Not quarantined. Lane S216 and S221 are libalpm util.c (`SOURCES.md:225`, `SOURCES.md:230`).

3. `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/initramfs-hook-api-zh-r27.md` — Chinese ArchWiki mkinitcpio hook split and `SYSTEMD_SULOGIN_FORCE=1`. Cites staged **S222**. Collides. Not quarantined. Lane S222 is libalpm trans.c scriptlet staging (`SOURCES.md:231`).

## Receipts

`.ufo/waves/round-51/w1/R51ScoutAssimilation/`: `reg-ids` (256), `staged-ids` (147), `collisions` (57), `quarantine-slice` (12), `proof-scratch-registry.md`, `proof-03-match.txt`, `proof-col0-match.txt` (0 bytes), `proof-collisions` (`S200`), `proof-col0-collisions` (0 bytes). Scratch dir removed. `/fast` at run time: 428G available (`/dev/nvme1n1p2`).

Did not re-fetch cited URLs, did not open the three knowledge files past their source headers and opening sections, and did not compare staged body text to `initramfs-v42-sysroot-recovery.md`.
