VERDICT: defect-found

# R50LabParse — C1 report-parser edge cases (item C1-B8)

Frozen bytes under test: `8029cdba1049df25632c91a23c8db4eefb54be5f`. Counter copy run from that
revision: `git show 8029cdba...:tools/check-scrub-admission-r50.py`, sha256
`0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db` (read-only; the lane tree was
never touched). Reproducer receipt: `R50LabParse/repro.py` (self-contained; verified end-to-end,
23 counter runs, 1.3 s total).

## Method

Fixture (`repro.py`): under `/fast/scratch/hyaku/tsukuroi-r50/R50LabParse/` (removed after
receipts were copied) I build a wave dir of 18 synthetic seat reports
`R50RevGR{1,2,3}{a,b,c}` / `R50CritGR{1,2,3}{a,b,c}`, a matching `w1-results.json`
(`name`/`agent`/`output`) and `w1-dispatch.json` (`taskCall.tasks`), plus `--entry-file`,
`--skill-file`, `--readme-file` overrides that are the frozen entry/SKILL/README with only the
round-50 marks appended. That isolates the *report-parsing* legs: `structural_ok`, `corr_ok` and
`quotes_ok` are constant (1/1/3) in every case, and `marks_ok` is 3 in every case, so any change in
the predicate is attributable to `verdicts_ok`/`seats_ok`.

Each synthetic body is >=300 bytes and cites two distinct row source files that resolve in the
pinned snapshots (`cmdline.c:147`, `vsprintf.c:86`, `kstrtox.c:29`, `sysfs.c:2040`,
`dev-replace.c:700`, `scrub.c:3081`/`3094`, `ioctl.c:3132`, `systemd.kill.xml:5`,
`btrfs-scrub@.service:5`, `capture.txt:5`).

Controls:
- `base` (no mutation): `rc=0 PASS`, legs `1/1/3/3/18/3`, 6/6 credited in every row, `blocking []`.
- `ctl_300_rowcites` (body exactly 300 bytes, row citations): `rc=0 PASS`, 6/6 credited.
- Frozen-revision run without overrides: `structural_ok 1, corr_ok 1, quotes_ok 3, marks_ok 0,
  seats_ok 0, verdicts_ok 0` (the round-50 marks and w1 reports are not in the frozen bytes yet;
  expected, and not a parse leg).

## Item cases (each mutates only `R50RevGR1a`; other 17 reports valid)

| case | mutation | rc / verdict | failing leg | mode |
|---|---|---|---|---|
| a | CRLF (`\r\n`) throughout | 1 FAIL | `seats_ok 17` | unbound: `first line 'ROW GR1 VERDICT: holds\r'` |
| b | UTF-8 BOM before `ROW` | 1 FAIL | `seats_ok 17` | unbound: `first line '\ufeffROW GR1 VERDICT: holds'` |
| c | one leading space on line 1 | 1 FAIL | `seats_ok 17` | unbound: `first line ' ROW GR1 VERDICT: holds'` |
| d | ```` ``` ```` fence around the two lines | 1 FAIL | `seats_ok 17` | unbound: `first line '```'` |
| e | `ROW GR1 VERDICT: Holds` | 1 FAIL | `seats_ok 17` | unbound: `first line 'ROW GR1 VERDICT: Holds'` |
| f | 3rd line `ROW GR2 VERDICT: holds` | 1 FAIL | `verdicts_ok 2` | **blocking negative** (`per_row.GR1.blocking = ['R50RevGR1a']`), `seats_ok` stays 18 |
| g | 2nd `SECTION SHA256: 000…0` line after the valid hash line | **0 PASS** | **none** | invisible: 6/6 credited, no seat note |
| h | body exactly 299 bytes | **0 PASS** | **none** | silent non-credit: `report body under 300 bytes`, `seats_ok` stays 18, 5/6 credited |
| i | body exactly 300 bytes, only `entry.md:5` + `SHA256SUMS:1` | **0 PASS** | **none** | silent non-credit: `fewer than 2 distinct row source files cited`, `seats_ok` stays 18, 5/6 credited |

Declared-vs-observed:
- (a)–(e): failure mode **is** the declared one (`unbound`; `bind_seat` lines 348–352 reject any
  first line that is not a `VERDICT_RE.fullmatch`). But it is attributed to `seats_ok`, whose
  declared meaning is the results/dispatch binding, not report formatting — see F1.
- (f): the leg that fails is `verdicts_ok`, via a **blocking negative**, but not by the declared
  route. The declared rule is "a report whose first line says partly/fails blocks the row" (module
  docstring); here the first line says `holds` and the block comes from the body scan at line 354
  (`ANY_VERDICT_RE.findall('\n'.join(lines[1:]))`), which returns `'partly'` and appends the seat to
  `blocking` (line 416). So a *contradiction anywhere after line 1* is escalated to a bound-format
  negative.
- (g), (h), (i): **no leg fails** — none of the three is a declared failure mode either.

## Extra probes (same fixture, beyond the item list)

| case | mutation | rc / verdict | observation |
|---|---|---|---|
| g2 | line 2 hash = 64 zeros, correct hash on line 3 | 0 PASS | seat uncredited (`hash 000…0 != 3a2ba180…`), yet `seats_ok 18`; 5/6 credited |
| k | invalid UTF-8 byte in body | 1 FAIL | unbound: `report not UTF-8` (strict `raw.decode('utf-8')`, line 342) |
| l | trailing space on line 1 | 1 FAIL | unbound: `first line 'ROW GR1 VERDICT: holds '` |
| j | body prose: "…whose line read ROW GR1 VERDICT: fails." | 1 FAIL | **blocking negative** from prose, `verdicts_ok 2` |
| q | body prose: "…said ROW GR1 VERDICT: Holds…" | 1 FAIL | blocking negative (case-sensitive `\w+` word compare) |
| r | body prose: "…said ROW GR1 VERDICT: partly." | 1 FAIL | blocking negative |
| p | body prose: "The sibling line ROW GR1 VERDICT: holds agrees." | 0 PASS | same row + same word is tolerated |
| h4 / i4 | four of the six GR1 seats 299-byte / lane-cites-only | 1 FAIL | `verdicts_ok 2`, 2/6 credited — the body/citation legs bite only at this density |
| m | three of six GR1 seats 299-byte (`RevGR1a`, `RevGR1b`, `CritGR1a`) | **0 PASS** | 3/6 credited (`RevGR1c`, `CritGR1b`, `CritGR1c`), row still `row_ok` |
| n | three reviewers `RevGR1a..c` 299-byte | 1 FAIL | role guard: credited critics only, `verdicts_ok 2` |

## Findings

**F1 — formatting is scored as a binding failure, and silently, on any CRLF/BOM/space/fence report.**
`bind_seat` (counter lines 342–352) does `raw.decode('utf-8')` then `text.split('\n')` and
`VERDICT_RE.fullmatch(lines[0])` with no `\r` strip, no `utf-8-sig`, no `strip()`. A seat that writes
a byte-correct report with CRLF or a BOM is reported as `unbound`, i.e. it lands on `seats_ok`
(17), never on `verdicts_ok`. The declared seat contract in the docstring is byte-exact, so this is
"as declared", but the counter gives no distinct signal for it: the L1 sees `seats_ok 17` and must
read `seat_notes` to learn the cause. Evidence: receipts `a_crlf.json`, `b_bom.json`,
`c_leadspace.json`, `d_fence.json`, `e_cap.json`, `k_latin1.json`, `l_trailing_space.json`.

**F2 — body prose can produce a false blocking negative.**
`bind_seat` lines 354–356 scan every line after line 1 with `ANY_VERDICT_RE` (`\w+`, no anchoring,
no case folding) and return `'partly'` for any `ROW <other-row> VERDICT: <word>` or
`ROW <this-row> VERDICT: <other-word>`. A seat that quotes a sibling's line, an earlier withdrawn
draft, or a falsified verdict inside its prose blocks its own row (`verdicts_ok` −1) while its first
line says `holds`. Evidence: `j_prose_mention.json`, `q_prose_cap.json`, `r_prose_partly.json` all
`verdicts_ok 2` with `blocking ['R50RevGR1a']`; `p_prose_same.json` PASS. Real risk for w1: the
counted cohort is explicitly told to report contradictions, and any report that *describes* a
`partly`/`fails` verdict it found blocks the row it is judging.

**F3 — `seats_ok == 18` does not mean 18 credited seats.**
Line 435: `seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None)`. A seat whose hash
leg fails (`g2_wrong_first`) or whose body/citation legs fail (`h_299`, `i_300_lanecite`) still
contributes to `seats_ok`, because its first two lines parsed. Both of those cases PASS with
`seats_ok 18` and 5/6 credited. So the C1 claim's "a fresh 18-seat cohort re-reads GR1-GR3" is
enforced as *at most* 18 bound seats and *at least* 3 credited per row — not 18 credited.

**F4 — the row credit floor is 3 of 6, so half a row can be dropped silently.**
Lines 428–431: `row_ok = len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles and
distinct and not blocking`. `m_drop3_mixed` drops three of six GR1 seats (all uncredited, mixed
roles) and the counter **PASSes** with `credited = [R50RevGR1c, R50CritGR1b, R50CritGR1c]`. Dropping
three of one role fails (`n_drop3_same_role`). Consequence: hash, body-length and citation legs are
per-seat advisory only; only 3 credits per row are load-bearing.

**F5 — a duplicate `SECTION SHA256` line is unremarkable.** `g_dup_hash` (valid hash on line 2, a
64-zero `SECTION SHA256` line as the first body line) PASSes with 6/6 credited and no seat note;
nothing checks that the hash line is unique or that a later hash line agrees. `g2_wrong_first` shows
the converse: the second-line hash alone binds, a later correct hash does not rescue the seat.

**F6 — boundary is exact.** Body bytes are `len('\n'.join(lines[2:]).encode('utf-8'))`
(`report_citations_ok`, line 293–294): 299 bytes → `report body under 300 bytes`; 300 bytes with two
row citations → credited (`ctl_300_rowcites`, 6/6). No off-by-one.

Cosmetic, not counted: the counter identifies itself as `check-scrub-admission-r49` in its JSON
(line 437) and in the usage line (line 51), and the usage text (line 49) advertises
`--skip-anchors-check`, which `argparse` does not define (a control battery passing it exits 2).

## Proposed minimal counter text (not applied — lane is read-only for this seat)

1. F1: `text = raw.decode('utf-8-sig')` and `lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')`;
   keep `fullmatch` on `lines[0].strip()` / `lines[1].strip()`, or state byte-exactness in the seat
   dispatch. Either way give the failure its own note prefix (`format:` vs `unbound:`) so `seats_ok`
   is not the only signal.
2. F2: restrict the negative scan to whole verdict-shaped lines —
   `for ln in lines[2:]: m2 = VERDICT_RE.fullmatch(ln.strip())` — and block only when `m2` is not
   None and (`m2.group(1) != row or m2.group(2) != m.group(2)`); prose mentions then stop blocking.
3. F3/F4: add `seats_credited_ok == 18` to the predicate (or count `credited` into `seats_ok`), so
   the claim "18-seat cohort" is the thing measured; keep the 3-credit floor as the row gate.
4. F5: reject a second `SECTION SHA256:` line in the body (`if HASH_RE.search(body): uncredited`).

## Not done

- No lane, fleet or sibling write; no git/jj mutation anywhere (the counter is invoked with
  `--lane` and only `git show` runs).
- Did not probe the entry-side legs (`structural_ok`, `quotes_ok`, `corr_ok`, `marks_ok`) or the
  `--section-hash` path — outside this item. `marks_ok` was overridden to 3 by design; the frozen
  revision itself scores `marks_ok 0` (round-50 marks not yet in the bytes).
- No tool installs were needed (`python3`, `git` only).
- Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50LabParse/` removed after receipts were copied
  (free space seen: 546 G on `/fast`).
