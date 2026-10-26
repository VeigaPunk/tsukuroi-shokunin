VERDICT: defect-found

Seat `C2PostCritBinding`, item F-10 (manual audit of the row-verdict binding), tsukuroi lane round 42 w2, 2026-10-26.
Read-only: no lane file was created or edited outside this report and my seat dir, no git/jj mutation, no host change,
no counter run. Audit window 17:26-17:43; the ten seats were dispatched 17:20 (`w2.ready`) and their reports landed
17:29-17:42 (the last, `C2RevSC3.md`, at 17:42 — it was missing for 22 minutes while agent `C2RevSC3-10`, a tenth
attempt, ran). Everything below is read from the lane at tip `a968393c` plus the seat reports as they stood during
the window; report bytes were still moving (see F-10d), so `hashes-1.txt` / `hashes-2.txt` / `hashes-3.txt` in my
seat dir pin the three states I read. All ten are audited; the table's third row is the late one.

## 1. What was checked, and how

For each of the ten counted seats the declaration names (`C2RevSC1..5` reviewer, `C2CritSC1..5` critic):

1. **First line against the declared format.** `make-w2-spec.py:40-43` requires the first line to be exactly
   ``ROW {row} VERDICT: `` followed by one word, "once in the report and once in the final answer, nowhere else".
   Checked as `^ROW SC<n> VERDICT: (holds|partly|fails)[ \t]*$`, plus BOM/CRLF/trailing-space scans (`audit.py`,
   `audit.out`).
2. **Every occurrence of the frozen pattern in the body.** The counter's pattern is unanchored
   (`tools/check-scrub-record-r42.py:66`), so the audit lists *all* matches and attributes them by row — this is
   the D1 exposure `w1/C2CritControl.md` found, re-measured on this wave's real bytes.
3. **Body vs. word.** For every seat whose word I doubted I re-derived the decisive fact myself in the pinned
   snapshot (`.ufo/waves/round-42/frozen/src/scrub.c`, sha256 `48df2e2f…f0801`, `sha256sum -c SHA256SUMS` → OK),
   and for the two POSIX claims I ran my own fixture (`posix.py`, `flockwin.py`).
4. **Mechanism.** `bindsim.py` reproduces `bound()` (`:119-136`, same regex, same membership test) over the real
   report bytes with a synthetic results entry, to say what the counter would do with each report under three
   output shapes and under the two record hazards (suffixed name, duplicate entry).

The counter's predicate is `rows==5 and quotes_ok==5 and novelty_ok==5 and host_ok>=3 and sources_ok==1 and
verdicts_ok==5 and novelty_base_hits==0`; a row's `verdict_ok` requires both seats bound, no bound `fails`, and —
when any seat reads `partly` — a bound residual reviewer `C2RevSC<n>c` reading `holds` (`:215-218`).

## 2. The table

| seat | first-line verdict (exact form?) | body consistent with the word? | risk of mis-binding |
|---|---|---|---|
| `C2RevSC1` | `ROW SC1 VERDICT: holds` (exact) | **no — unsound.** Body ends "no sentence is incomplete, overreaching, or false" after recording two "observations" that are themselves false on the pinned source (see F-10a): the `_tmp` is opened `O_WRONLY\|O_CREAT` without `O_TRUNC` (`scrub.c:517`) and never unlinked, so a shorter rewrite publishes new head + stale tail; and the writer holds `LOCK_EX` on the *record* inode between `rename` (`:534`, called `:925`) and `close` (`:931`), so "writer and reader locks never meet" is wrong. | **HIGH (record-level).** The counter will bind `holds` for SC1's reviewer while its two decisive supporting sentences are contradicted by the snapshot and by the sibling critic's measured demo. Row outcome is unaffected (critic `fails` dominates), but `per_row.SC1.verdicts.rev` records an endorsement the source does not support. |
| `C2RevSC2` | `ROW SC2 VERDICT: holds` (exact) | yes. Decisive claims re-verified: 19/19 fields in the row's order at `scrub.c:870-888` (my extraction, `audit.out` §order), version line written before the device loop (`:856-859` vs `:863`), reader rejects any other version (`:627-632`). | LOW. One hit, no other-row verdict line. |
| `C2RevSC3` | `ROW SC3 VERDICT: fails` (exact; landed 17:42 after 22 min and a tenth attempt) | yes; grounded and independent of the critic. F1: same resume-zero falsehood, derived from `_SCRUB_SUM` (`:795-796`), `scrub_resumed_stats` (`:803-827`), `sp[i].resumed = last_scrub` (`:1430-1434`) — all re-verified above. F2: "only the final write reports a failure" is false in both directions (`:1685-1699` report a mid-run failure; `:1704-1706` is `do_print`-gated, false by default `:1249`). It adds the source-level note that the `pthread_cancel`-ESRCH branch (`:1690-1693`) leaves `terr` read uninitialised at `:1696` — outside the row, and plausible from the code. | LOW. Two `fails` for SC3 from two seats that reached the same falsifier by independent routes; no other verdict line in the body (`audit.out`). |
| `C2RevSC4` | `ROW SC4 VERDICT: holds` (exact) | yes as written, but it decides the same question the critic does, the other way: it dismisses the removed-device quantifier ("`last_dev_scrub` returns the first record matching the devid … 'every device that has a record in the file' is device-granular and accurate"). | MEDIUM (definitional). Its `holds` cannot be distinguished from `partly` by the record; the pair (holds, partly) makes SC4 depend on a residual seat that does not exist (F-10b). |
| `C2RevSC5` | `ROW SC5 VERDICT: holds` (exact) | yes, and it *finds* the critic's fact: its Finding 2 states `scrub start` "writes the limit unconditionally (frozen scrub.c:1414) with `throughput_limit` defaulting to 0 and restores the previous value afterwards", then judges it "consistent with the row". | MEDIUM (definitional). Same fact, opposite word from `C2CritSC5`; `partly` from either side costs SC5 a residual that does not exist. |
| `C2CritSC1` | `ROW SC1 VERDICT: fails` (exact) | yes; grounded. I re-verified its chain: `grep -nE 'O_TRUNC\|O_EXCL\|ftruncate\|truncate'` → no hits; `unlink(` only at `:1485/:1497/:1721` (all `sock_path`); `flockwin.py` → reader `FAILED EAGAIN` in the rename→close window, `ACQUIRED` after close; `posix.py` → leftover `_tmp` 323 bytes, new record 33 bytes, renamed file 323 bytes "== new? False … endswith stale tail? True". | LOW for the word; the risk is the opposite direction — it is the seat whose `fails` kills row SC1. |
| `C2CritSC2` | `ROW SC2 VERDICT: holds` (exact) | yes; its seven attacks (A1-A7) each carry the line that defeats them, and A2 (the stale-tail branch) is correctly assigned to SC1's territory. | LOW. |
| `C2CritSC3` | `ROW SC3 VERDICT: fails` (exact) | yes; grounded. Re-verified F1: `cmd_scrub_resume` → `scrub_start(…, true)` (`:1831-1834`), `sp[i].resumed = last_scrub` (`:1430-1434`), `use = scrub_resumed_stats(&data[i], &local)` (`:864`), `_SCRUB_SUM` adds the resumed counters (`:795-796`), `t_start` from the old record (`:823`) ⇒ the first resume record is not all-zero, so "(or is resumed)" is false. F2: `error("recording progress failed: %m")` exists at `:1696-1698`; the final-write message is gated `if (ret && do_print)` (`:1704`) and `do_print = false` by default (`:1249`). | LOW; kills row SC3 on a verified falsehood. |
| `C2CritSC4` | `ROW SC4 VERDICT: partly` (exact) | **tension.** It says of S4 "**as written** … it does not [survive]" and still chooses `partly`; under `make-w2-spec.py:42-43` (`fails` = a sentence is false) that reading is `fails`. F1/F3/F2 are grounded: I confirmed the fold walks the *current* device list (`:1975`, `:1981-1986`) through `last_dev_scrub`'s first-devid match (`:1136-1150`), the socket-first open (`:1927-1930`), and `return !!err` (`:2010`). | **MEDIUM-HIGH, structural.** `partly` sends the row to `C2RevSC4c` (`:215-216`), which the dispatch does not contain (F-10b) ⇒ SC4 becomes not-ok by record arithmetic, not by the row's content. |
| `C2CritSC5` | `ROW SC5 VERDICT: partly` (exact) | **tension.** Same shape: it says the clause "claims a report that does not happen" (a false reading) and chooses `partly` because the sentence survives "under the charitable reading". Its counterexample is real: `throughput_limit = 0` (`:1275`), unconditional `write_scrub_device_limit(..., throughput_limit)` (`:1414`), read back (`:1449`), printed only when > 0 (`:1560-1563`), restore before `pthread_join` (`:1596-1598` vs `:1608`) — all confirmed in the snapshot. | **MEDIUM-HIGH, structural.** Same unarmed residual ⇒ SC5 not-ok by arithmetic. |

No seat's first line deviates from the declared format: all ten reports are byte-exact
`ROW SC<n> VERDICT: <word>` with no BOM, no CR, no trailing space (`audit.out`, ten times `fmt_ok=True`), and each
names the row the dispatch assigns it (`dispatch-seats.txt`).

## 3. Findings

### F-10a — one bound `holds` is not supported by its own body (higher than D1: no quoting needed)

`C2RevSC1.md` binds `holds` for a clause that the same wave's critic falsifies with a measured demo, and the
reviewer's two reasons for discounting it are false:

- `C2RevSC1.md` ("Overreach check"): "Visibility remains atomic old-or-new — the sentence's actual claim — so this is
  context, not a defect in SC1." My fixture (`posix.out`), using exactly the writer's flags (`scrub.c:517`
  `O_WRONLY|O_CREAT`, no `O_TRUNC`; `:483` `open(datafile, m, 0600)`; `:534` `rename`): leftover `_tmp` 323 bytes,
  next record 33 bytes, after the rename the record is 323 bytes, `record == new? False`, `endswith stale tail? True`.
  The reader therefore sees neither the old nor the new record — the sentence's universal fails.
- `C2RevSC1.md` ("Overreach check"): "Writer and reader locks never meet (different inodes: `_tmp` vs record)".
  False for the window `rename` (`:925`) → `close` (`:931`), where the writer still holds the lock on the renamed
  inode; `flockwin.out`: `reader in rename..close window: FAILED EAGAIN … reader after close: ACQUIRED`, and the
  status path turns that into `warning("failed to open status file: %m"); err = 1` (`:1931-1935`).

Severity: the predicate's outcome for SC1 is right anyway (`fails` from the critic dominates), so this is a
**record defect**, not a predicate defect — the receipt will say "SC1 reviewer: holds" for a body whose decisive
sentences the snapshot contradicts. It is also the cleanest answer to the item's third question: the unanchored
match does not *need* a quoted line to bind a wrong verdict; a self-contradictory body suffices.

### F-10b — `partly` is a word the wave cannot represent (dispatch has no residual seat)

Both `partly` seats (`C2CritSC4`, `C2CritSC5`) route their row to `bound(..., 'residual', f'C2RevSC{n}c', …)`
(`:215-216`). There is no such seat: `w2-dispatch.json` `taskCall.tasks` holds exactly
`C2RevSC1..5`/`C2CritSC1..5` plus 24 non-row seats (`dispatch-seats.txt`; no name matching `C2RevSC\dc`), and
`ls .ufo/waves/round-42 | grep -i resid` → no `residual-dispatch.json`, no `residual/` directory. So with the current
records SC4 and SC5 are `v_ok = False` no matter what their reports argue — the FMT offers three words and the
dispatch arms two. Two of five rows die on a word, not on a reading.

### F-10c — the results record is the untested half, and it is where the record can silently drop seats

Seven of the ten row seats were served by retried agents whose ids carry a suffix (`w2.ready.partial`, copied as
`ready.partial.snapshot.json`): `C2RevSC1→C2RevSC1-3`, `C2CritSC1→C2CritSC1-5`, `C2RevSC2→C2RevSC2-3`,
`C2CritSC2→C2CritSC2-2`, `C2RevSC3→C2RevSC3-10`, `C2RevSC5→C2RevSC5-2`, `C2CritSC5→C2CritSC5-2`.
`bound()` requires a `w2-results.json` entry whose `name` equals the **seat** name and whose role equals
`reviewer`/`critic`, exactly one such entry (`:124-129`). Simulated on the real reports (`bindsim.out`):

- entry named `C2RevSC1-3` instead of `C2RevSC1` → `results-entry-count=0` → verdict `null` (silent);
- two entries for the same seat (first attempt + retry) → `results-entry-count=2` → verdict `null` (silent).

`w2-results.json` does not exist yet (only `w1-results.json`, whose 43 entries are all bare seat names with no
duplicates — that is the pattern to match). Until it lands, the binding of all ten seats is unverified; this is the
single check the integrator must run before scoring.

### F-10d — a report is not frozen when it first appears

`C2CritSC4.md` changed under me after it first appeared: 15071 bytes at my 17:37 read, digest `ff7e087e…` in
`hashes-1.txt`, final 15103 bytes / `7c1d049a…` with mtime `17:38:59` (`stat -c '%s %y'`) — three contents, verdict
word stable; `C2CritSC2.md` grew 10567 → 10667 bytes between two of my audits. `bound()` reads the report with
`git show <rev>:path` (`:76-78`), so the bytes **committed** are the binding ones. Committing a report mid-write, or
after a later seat edit, silently changes or loses the bound word (any edit that drops the first line yields
`null`, not a wrong word — safe, but silent). `hashes-1.txt`/`hashes-2.txt` are what I audited; they are the values
to compare after the integration commit.

### F-10e — D1 (unanchored match) is not exercised by any report body on this wave

Every present report carries exactly one occurrence of the frozen pattern and it is its own row's first line
(`audit.out`: `unanchored_own=[<word>]`, `other_row_mentions=[]`, `n_all_hits_in_report == 1`). No report quotes the
format line in prose, so the D1 shapes (mention counted as assertion, `XROW …X` embedded, cross-row blob) do not
appear here. The exposure that remains is exactly the one I cannot see: each seat's **final answer** in
`w2-results.json`. Check it per seat: exactly one `ROW SC<n> VERDICT: <word>` occurrence, same word as the report,
before scoring; `bindsim.py` V1/V2 (output = first line; output = whole report) both bind correctly for all ten.

### F-10f — the counter's outcome on the current bytes (context for the integrator)

`rows`/`quotes`/`novelty`/`host`/`sources` are other seats' business; on verdicts alone: SC1 `not ok` (critic
`fails`), SC2 `ok`, SC3 `not ok` (both seats `fails`), SC4 `not ok` (partly, residual unarmed),
SC5 `not ok` (partly, residual unarmed) ⇒ `verdicts_ok = 1`, predicate **FAIL**. Two of those four are the rows'
own content (SC1, SC3 — falsehoods I re-derived); two are F-10b's arithmetic. Do not read `verdicts_ok = 1` as
"four rows were falsified": two rows carry a verified false sentence, two rows were lost to an unarmed residual
path. The receipt's `verdicts.rev/crit` map is what distinguishes them; the predicate's single counter cannot.

## 4. Smallest safe corrections (none requires a counter change; the counter is frozen at `dbe933ec…`)

1. **Arm the residual path or say it is unarmed.** Before scoring, dispatch `C2RevSC4c`/`C2RevSC5c` through
   `residual-dispatch.json` + `residual-results.json` + `.ufo/waves/round-42/residual/C2RevSC<n>c.md`. If not
   dispatching, record in the integration note that `partly` is a dead word this round (F-10b) — the alternative is a
   receipt whose `verdicts.rev/crit` pair means something different from what the predicate computed.
2. **Check the results names before scoring** (F-10c): ten entries, bare seat names, roles `reviewer`/`critic`,
   one per seat; a suffixed or duplicated entry must be fixed in `w2-results.json`, not worked around.
3. **Score only settled bytes** (F-10d): re-run `sha256sum .ufo/waves/round-42/w2/C2*-SC*.md` after the last seat
   stops writing and before the integration commit; compare with `hashes-2.txt` and with the committed tree.
4. **Write the bound `holds` of `C2RevSC1` as disputed, not as support (F-10a).** Cheapest honest fix, no file
   change: in the integration note, record that SC1's reviewer `holds` rests on two sentences the snapshot
   contradicts (with `posix.out`/`flockwin.out` as receipts) and that SC1's row verdict is decided by the critic.
   Do not edit a delivered report to change its word — that would be a fabricated seat record.

## 5. What I did not do

- Did not run `tools/check-scrub-record-r42.py` (the integrator's step, CPU-heavy on a loaded host). My binding
  verdicts come from a line-for-line reproduction of `bound()` (`bindsim.py`), not from a scored tree.
- Did not see `w2-results.json` (it does not exist), so no seat's **final answer** was audited — that is the half of
  the binding this report cannot certify (F-10c, F-10e).
- `w2/C2RevSC3.md` was missing for the first 22 minutes (no file, no receipts dir, ten attempts); it landed at
  17:42 and I read and audited it in the final pass (`hashes-3.txt` is the audited set of all ten). I did not see it
  as the seat was writing it, so a silent edit after 17:43 would need `hashes-3.txt` compared against the commit.
- Did not judge the rows themselves beyond the two falsifiers I re-derived for F-10a/F-10f; SC2/SC4/SC5 content
  readings belong to their seats and to the L1.
- No counterexample to `C2CritSC2`'s `holds` was sought beyond the field order and version gate I verified; the
  seat's own A1-A7 inventory is broader than what I re-ran.
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2PostCritBinding` (fixtures `demo/`, `demo2/`, `.py` drivers) removed
  after the receipts were copied. No tools installed or upgraded: `python3` 3.13, `git`, `sha256sum`, `sed` were
  already present.

Receipts: `.ufo/waves/round-42/w2/C2PostCritBinding/` — `audit.py`, `audit.out` (first-line format, all frozen-pattern
hits per report), `bindsim.py`, `bindsim.out` (binding under four output shapes + two record hazards),
`posix.py`, `posix.out` (stale `_tmp` tail), `flockwin.py`, `flockwin.out` (rename→close lock window),
`counter-binding.txt` (`check-scrub-record-r42.py:120-140`, `:214-222`), `dispatch-seats.txt` (ten seats, roles),
`ready.partial.snapshot.json` (seat→agent retry map), `hashes-1.txt`, `hashes-2.txt`, `hashes-3.txt` (report
digests I audited; `-3` is the final ten-report set).
