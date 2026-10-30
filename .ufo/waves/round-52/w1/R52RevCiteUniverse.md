VERDICT: defect-found

Axes: depth, C1, bindcheck.
Revision under review: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` only. Findings below refer to committed paths at that revision, not the mutable worktree. Recommendation only; no admission, edits, judgment, or integration performed.

## Medium — GR1 and GR2 omit a legitimate pinned row source from citation credit

`tools/lint-grounding-r51.py:78-85` declares `capture.txt` (S249) a row source for all three rows. GR1 actually cites it at `corpus/knowledge/btrfs-scrub-grounding-r45.md:96-97`; GR2 at `:226`. Yet `tools/check-scrub-admission-r52.py:89-91` includes it in CITE only for GR3. The admission gate at `tools/check-scrub-admission-r52.py:248-249` requires two distinct basenames in that row's CITE set **before** resolving any citation. Thus a real row-source citation earns zero distinct-source credit for GR1 and GR2.

[INFERENCE from the frozen branch logic, not a runtime trial] A >=300-byte GR1 report citing only `sysfs.c:2040` and `capture.txt:8`, or a GR2 report citing only `ioctl.c:3132` and `capture.txt:1`, has two valid pinned row-source basenames but intersects CITE in only one. Both are rejected with `fewer than 2 distinct row source files cited`. This meets the assignment's fairness-defect criterion; the frozen counter was not changed.

Important distinction: `verify_citation` itself does NOT wrongly reject those citations. Its snapshot-first branch (`tools/check-scrub-admission-r52.py:221-226`) accepts their valid lines. The wrongful exclusion is in `report_citations_ok`'s distinct-source gate. No row-body citation start was rejected by a static reproduction of `verify_citation`'s branches.

## Per-row classification

Columns: basename | CITE credit | LANE_FILES | pinned snapshot source(s). The row-specific source is in parentheses when a basename has two snapshots.

### GR1 — entry lines 14-102

| Basename | CITE | LANE_FILES | Pinned sources |
|---|---|---|---|
| `capture.txt` | no | yes | S249 |
| `cmdline.c` | yes | no | S246 |
| `kstrtox.c` | yes | no | S246 |
| `scrub.c` | yes | no | S237, S242 (row: S242) |
| `sysfs.c` | yes | no | S243 |
| `vsprintf.c` | yes | no | S246 |

Union: `capture.txt`, `cmdline.c`, `kstrtox.c`, `scrub.c`, `sysfs.c`, `vsprintf.c`.
Missing row-source credit: `capture.txt`. No nonexistent declared lane path or wrongly rejected resolving citation found.

### GR2 — entry lines 103-238

| Basename | CITE | LANE_FILES | Pinned sources |
|---|---|---|---|
| `capture.txt` | no | yes | S249 |
| `dev-replace.c` | yes | no | S247 |
| `ioctl.c` | yes | no | S240 |
| `scrub.c` | yes | no | S237, S242 (row: S242) |
| `sysfs.c` | yes | no | S243 |

Union: `capture.txt`, `dev-replace.c`, `ioctl.c`, `scrub.c`, `sysfs.c`.
Missing row-source credit: `capture.txt`. No nonexistent declared lane path or wrongly rejected resolving citation found.

### GR3 — entry lines 239-324

| Basename | CITE | LANE_FILES | Pinned sources |
|---|---|---|---|
| `btrfs-scrub@.service` | yes | no | S244 |
| `capture.txt` | yes | yes | S249 |
| `host-btrfs-progs.txt` | no | yes | none |
| `scrub.c` | yes | no | S237, S242 (row: S237) |
| `systemd.kill.xml` | yes | no | S248 |

Union: `btrfs-scrub@.service`, `capture.txt`, `host-btrfs-progs.txt`, `scrub.c`, `systemd.kill.xml`.
Missing row-source credit: none. No nonexistent declared lane path or wrongly rejected resolving citation found.

For GR3, `host-btrfs-progs.txt` is correctly a lane artifact, not a pinned row source: the entry explicitly says so at `corpus/knowledge/btrfs-scrub-grounding-r45.md:321-324`, lint allows it at `tools/lint-grounding-r51.py:87`, and counter LANE_FILES declares it at `tools/check-scrub-admission-r52.py:108`. Its absence from CITE is not a fairness defect under this assignment.

## Declared paths and snapshot integrity

Observed via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:<path>`: all 14 LANE_FILES candidate declarations (including the two aliases of the entry) exist. All 11 pinned snapshot declarations exist and their observed SHA256 values match the frozen lint constants. Exact paths, line counts, existence booleans and digest results are in the companion `R52RevCiteUniverse/citation-universe.json` receipt. No declared absent-path defect was found. `capture.txt` appears in both snapshot and lane maps; snapshot resolution takes precedence, and both declarations point to the same existing file.

## Exhaustive row-body citation inventory

Format: `source-line[-end]@entry-line`; repeated citations are retained. Colon-only continuations inherit the preceding basename within their paragraph. All quoted and prose named citations are included; ranges are retained rather than expanded. Entry-line locations are in `corpus/knowledge/btrfs-scrub-grounding-r45.md` at the frozen revision.

### GR1: 57 citation occurrences

- `capture.txt`: 9@96, 8@97, 1@97
- `cmdline.c`: 156@17, 193@23, 161-184@23, 183@24, 189@25, 191-192@26, 147@36, 156@38, 159@40, 177@42, 178@44, 183@46, 189@48, 191@50, 192@52, 193@54
- `kstrtox.c`: 30-31@19, 33@19, 35@20, 37-38@20, 70@21, 75@21, 77@21, 29@62, 30@64, 33@66, 35@68, 37@70, 38@72, 70@74, 75@76, 77@78
- `scrub.c`: 1381-1382@32, 1368-1369@33, 1400-1401@33, 1368@88, 1369@90, 1381@92, 1382@94
- `sysfs.c`: 2040@16, 2042@26, 2044@28, 2043@28, 2043@31, 2040@80, 2042@82, 2043@84, 2044@86
- `vsprintf.c`: 114@18, 86@18, 91@22, 86@56, 91@58, 114@60

### GR2: 85 citation occurrences

- `capture.txt`: 1@226
- `dev-replace.c`: 700@106, 1197@107, 1265-1268@107, 701-703@108, 1278-1279@118, 1286-1287@119, 1288-1297@119, 700@139, 701@141, 703@143, 1197@145, 1265@147, 1268@149, 1287@151, 1235@215, 309@216, 970@218, 1235@230, 309@232, 970@233, 1235-1242@234
- `ioctl.c`: 3072-3073@126, 3075-3078@126, 3080-3082@127, 3084-3085@127, 3087-3090@128, 3093-3095@129, 3109-3110@130, 3115@130, 3072@191, 3075@193, 3080@195, 3084@197, 3085@199, 3088@201, 3093@203, 3109@205, 3110@207, 3115@209, 3132@227, 3133@227, 3190@231
- `scrub.c`: 3081@109, 3094-3153@112, 3094-3095@112, 3109-3111@113, 3114-3116@113, 3250-3253@113, 3120-3123@114, 3127-3133@115, 3138-3142@116, 3147-3153@117, 3321-3336@134, 3159@134, 3222@135, 3081@153, 3094@155, 3095@157, 3109@159, 3114@161, 3120@163, 3123@165, 3127@167, 3133@169, 3138@171, 3139@173, 3142@175, 3147@177, 3148@179, 3149@181, 3153@183, 3159@185, 3222@187, 3336@189
- `sysfs.c`: 1288@211, 2015@213, 78@220, 1302@222, 2019@224, 78@229, 1302@229, 2019@229, 1288@230, 2015@232

### GR3: 53 citation occurrences

- `btrfs-scrub@.service`: 9@244, 1-10@245, 1-10@248, 9@267, 10@269
- `capture.txt`: 3@318, 4@319, 5@319, 2@320
- `host-btrfs-progs.txt`: 4@248, 2-3@257, 5-6@257
- `scrub.c`: 1292-1293@258, 1247@259, 1512@259, 1546@259, 1710@259, 439@260, 442@260, 421@261, 1546@262, 421@299, 439@301, 442@303, 1247@305, 1292@307, 1293@309, 1512@311, 1546@313, 1710@315
- `systemd.kill.xml`: 108-109@243, 84-85@243, 112@244, 101@245, 68@246, 86-87@247, 114-115@249, 91@250, 96-97@250, 68@271, 84@273, 85@275, 86@277, 87@279, 91@281, 96@283, 97@285, 101@287, 108@289, 109@291, 112@293, 114@295, 115@297

## Residual risks and verification gaps

- LSP unavailable: reading `xd://lsp` returned `No such tool`; no semantic-server references, definition, or diagnostics were available. Evidence is frozen Git bytes plus AST-extracted constants and static control-flow inspection, not semantic proof from grep.
- No admission counter, selftest, alternate runtime, or fixture report was executed; this item permits frozen citation-universe review, and the rejection witnesses above are explicitly static deductions. No counted row verdict or aggregate C1 result is asserted.
- The snapshot resolver accepts a basename against any matching snapshot (`tools/check-scrub-admission-r52.py:222-226`); both `scrub.c` snapshots are recorded rather than conflated. This does not cause a wrongful rejection among the requested citations.
- `verify_citation` checks a cited range's start because CITE_RE extracts only the first integer (`tools/check-scrub-admission-r52.py:86,245,250-251`). The inventory preserves full ranges; this review makes no claim that admission validates range endpoints.
- No tools installed or updated. No tracked lane/fleet files changed; only the assigned report and its receipt were written. Scratch removed after analysis.

Self-evaluation: accuracy 4 (static witnesses, no runtime confirmation); completeness 5 (all 195 occurrences, three universes, all lane candidates and snapshots); clarity 4 (full inventory is necessarily dense); actionability 4 (specific missing credit and gate location, frozen bytes deliberately unchanged); conciseness 4 (inventory retained for auditability). Overall 4.2/5. Highest-impact improvement outside this read-only scope: an owner-authorized regression witness for each omitted row-source basename. The user should agree this is a bounded fairness finding, not an admission verdict.
