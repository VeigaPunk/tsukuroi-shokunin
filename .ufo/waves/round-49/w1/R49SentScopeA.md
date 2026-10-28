VERDICT: defect-found

Seat R49SentScopeA, item P-1, scope audit A. Target: the 18 counted cohort seats of claim C1
(`R49RevGR{1,2,3}{a,b,c}`, `R49CritGR{1,2,3}{a,b,c}`). Question asked: does each report name only reads
(`git show`, `sha256sum`, `grep`) and at most the counter's `--section-hash`? Three seats exceeded their
declared execution class (one of them with network egress), four probed live host state that the item never
named; no seat ran a selftest, wrote outside the wave dir, or edited a tracked lane file. One separate,
integration-critical defect found while reading the cohort: `R49CritGR2b` binds `partly` on the current GR2
hash, which by FROZEN.md and the counter's own code blocks GR2 and therefore blocks claim C1.

# Axes (Godspeed)

1. **Class conformance** — did the seat run only the commands its item names? (the audited axis)
2. **Evidence auditability** — can each declared action be re-checked from the wave dir (receipt with the
   observed bytes) rather than from prose?
3. **Binding integrity** — do the 18 files exist, bind in the two-line format, and carry the frozen hash?

Axis 3 is fully clean; axis 1 has 7 deviations across 18 seats; axis 2 is where the deviations concentrate
(two of the three host-probing seats left no receipt of what they observed).

# What the class authorised, per seat

All 18 spec items carry the identical declaration `Execution class: EXEC-AUTHORIZED — the commands named in
this item, and no other` (`.ufo/waves/round-49/w1-spec.json`, items `R49RevGR{1,2,3}{a,b,c}` /
`R49CritGR{1,2,3}{a,b,c}`; verified present in all 18, and the 18 prompts normalise to exactly 6 shapes —
one per row × role, differing only in the seat id, row, frozen hash and snapshot list). The named commands are:
`mkdir -p /fast/scratch/hyaku/tsukuroi-r49/<seat>`, `git -C <lane> show 55c07cd3…:<path>`,
`sha256sum -c SHA256SUMS` in the pinned snapshot dirs, `python3 tools/check-scrub-admission-r49.py
--revision 55c07cd3… --section-hash`, and reads of the pinned snapshot files. The item also instructs: write
only the report and receipts under `.ufo/waves/round-49/w1/<seat>[.md]`, never edit a tracked lane file.

Convention I applied: a locally-written script that only recomputes a sha256 over already-extracted bytes is
inside the read class (several seats do this and say so, e.g. `R49CritGR1b.md:4` and `R49RevGR1a.md:4`
"my own script, not the counter"); a program that *executes* lifted kernel logic, and any network fetch, is
outside it.

# Method and limits

Read-only. I read the 18 report files in full, the 18 spec items, the frozen record, and each seat's receipt
directory listing; I read the counter at the freeze revision
(`git show 55c07cd3…:tools/check-scrub-admission-r49.py`) to establish what "blocking" means. I ran no
counter, no selftest, no git mutation and no probe beyond `ls`/`read`/byte-counting; the lane index was not
touched. Receipts for this audit: `R49SentScopeA/seat-class.tsv` (per-seat classification),
`R49SentScopeA/evidence-listing.txt` (wave dir listing, the 18 binding line pairs, per-seat receipt listings).

# Per-seat table

| Seat | Row | Line 1 | Selftest | Write outside wave | Tracked edit | Out-of-class action | Receipts |
|---|---|---|---|---|---|---|---|
| R49RevGR1a | GR1 | holds | no | no | no | **network fetch** of `fs/kernfs/file.c` (v7.2.11) | yes (fetch receipted) |
| R49RevGR1b | GR1 | holds | no | no | no | none | yes |
| R49RevGR1c | GR1 | holds | no | no | no | **compiled + ran a C harness** | yes |
| R49CritGR1a | GR1 | holds | no | no | no | none | yes |
| R49CritGR1b | GR1 | holds | no | no | no | **executed a Python model** | yes (no output file) |
| R49CritGR1c | GR1 | holds | no | no | no | **compiled + ran a C harness** | yes |
| R49RevGR2a | GR2 | holds | no | no | no | none | yes |
| R49RevGR2b | GR2 | holds | no | no | no | none | yes |
| R49RevGR2c | GR2 | holds | no | no | no | none | no receipt dir |
| R49CritGR2a | GR2 | holds | no | no | no | none | yes |
| R49CritGR2b | GR2 | **partly** | no | no | no | **live host files re-read** | no receipt dir |
| R49CritGR2c | GR2 | holds | no | no | no | live sysfs attributes re-read | yes (`lines.txt`) |
| R49RevGR3a | GR3 | holds | no | no | no | **live `systemctl show`, pacman db, `/etc` grep, dropin probes** | no (prose only) |
| R49RevGR3b | GR3 | holds | no | no | no | none | yes |
| R49RevGR3c | GR3 | holds | no | no | no | none | no receipt dir |
| R49CritGR3a | GR3 | holds | no | no | no | none | no receipt dir |
| R49CritGR3b | GR3 | holds | no | no | no | none | no receipt dir |
| R49CritGR3c | GR3 | holds | no | no | no | none | yes |

Hard-flag totals: **selftest 0/18 · write outside the wave dir 0/18 · tracked-file edit 0/18**. All 18 report
files exist (none missing, so no seat needs an invented verdict), all bind in the two-line format, and all 18
carry the frozen hash for their row (GR1 `3a2ba180…fee1`, GR2 `d4296085…027f`, GR3 `43430a14…32c`).
Out-of-class totals: **7 seats** — 1 network fetch, 3 executed derived code, 3 read live host state.

# Findings

## EXEC-UNAUTHORIZED-1 (medium) — R49RevGR1a fetched an upstream kernel file over the network

Evidence: `R49RevGR1a.md:8` — "I corroborated the newline delivery outside the pin (fetched 2026-10-28,
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/kernfs/file.c?h=v7.2.11, **NOT in
SHA256SUMS**)"; `R49RevGR1a/quotes-check.txt:39-40` records the same URL and
`sha256 64060083099abe105b6e20a2bf310f3a1f0370198bda517ce32b4114787874df`, and the file lands as
`R49RevGR1a/kernfs-file-v7.2.11.c` (28025 bytes, 1085 lines) in the receipt dir.

Why it matters: the counted cohort was scoped to local bytes, and the freeze's whole point is that the bytes
under test are fixed and digest-pinned. A counted verdict that leans on an un-pinned network artifact reopens
that surface after the freeze: the seat's clause 8 ("a bare newline written to the file clears it") is now
supported by a file that no counter leg can re-verify, and any later reader cannot distinguish the pinned set
from the fetched set without reading the receipt. Exploit path: a future counted seat cites the same
"corroboration outside the pin" to decide a clause with an unpinned, mutable upstream file; the counter's
citation leg accepts the `file:line`, so the verdict counts while its support is outside the sealed set.
Impact is contained here — the seat states the clause "holds with or without that corroboration"
(`R49RevGR1a.md:8`), and the fetch is honestly disclosed in the body — but the disclosure sits 10 lines above a
`Not done` line that reads "I did not re-fetch the upstream v7.2.11 files …" (`R49RevGR1a.md:18`), which a
skimming integrator can read as "no upstream fetch happened". Severity medium because the sentence is true as
scoped to digests and the fetched digest *is* recorded; it is a scope breach plus a disclosure-placement trap,
not a fabrication.

Smallest remediation: append to the report's Not-done line one clause naming the channel explicitly —
`network: one fetch of fs/kernfs/file.c (v7.2.11, sha256 64060083099abe105b6e20a2bf310f3a1f0370198bda517ce32b4114787874df, not part of the pinned set), used only as corroboration` — and, for the lane, either (a) declare network fetches non-authorised for counted seats and strike the corroboration, or (b) add the fetched blob and its digest to `corpus/SOURCES.md` as a non-pinned "outside-the-pin corroboration" source so the next reader cannot mistake it for a pinned one.

## EXEC-UNAUTHORIZED-2 (medium-low) — R49RevGR3a probed live host state, and receipted only prose

Evidence: `R49RevGR3a.md:35` "my own read-only `systemctl show btrfs-scrub@-.service` (2026-10-28) returns
TimeoutStopUSec=5s too"; `:37` "I re-read the pacman local db myself (1415 package dirs, world-readable)";
`:38` "`grep -n DefaultTimeoutStopSec /etc/systemd/system.conf.d/*` returns line 2"; `:28` "my own read-only check
found no /etc/systemd/system/btrfs-scrub@.service.d, …". Its receipt dir holds only
`cited-lines.txt`, `digests.txt`, `quotes.txt`, `section-hash.json` — no transcript of the probe.

Why it matters: clause 5 ("the 5 s effective stop timeout on this host") is fully decided by the pinned capture
(`capture.txt:3` `TimeoutStopUSec=5s`), so the live re-run adds no deciding evidence while adding an
unauditable channel: the observed output cannot be re-checked from the wave dir, and live host state at
2026-10-28 is not reproducible. Same class for the pacman sweep: the capture itself is the ground truth
(`capture.txt:5`), and re-reading 1415 package dirs by hand is an unreceipted second source. All of it is
read-only — no state was changed. Exploit path: a later seat repeats "I verified on the host" as if it were
recorded evidence; nothing in the wave dir can confirm or refute it, so an untrue or stale probe would pass
unnoticed.

Smallest remediation: drop the live re-runs from clauses 5-6 (the capture decides both) — or, if kept, record
them: `R49RevGR3a/probe.txt` with the exact command, the UTC timestamp and the literal output lines, which is
the discipline `R49CritGR2c` followed.

## EXEC-UNAUTHORIZED-3 (medium-low) — three seats executed derived code (two C harnesses, one Python model)

Evidence:
- `R49RevGR1c.md:17` "9. Worked examples, independently executed. I lifted the four function bodies
  byte-for-byte from the pinned files … and replicated the store's four lines. Observed: `100M`→104857600, …";
  receipts `R49RevGR1c/parse-harness.c` (1839 B) and `parse-harness-output.txt` (1394 B).
- `R49CritGR1c.md:10` "A userspace harness compiled from the pinned function bodies (memparse, …) printed:
  …"; receipts `R49CritGR1c/harness.c` (5085 B), `bf.c` (1203 B), `harness-output.txt` (2361 B), `bf-output.txt`.
- `R49CritGR1b.md:12` "receipt: …/gr1-parse-model.py, **which I executed**"; receipt is the `.py` only
  (3217 B), no output file.

Why it matters: the item's class names no compiler and no interpreter use beyond the counter's `--section-hash`,
so all three breached the declaration. Because every harness supplies its own shims for the helpers that are
*not* pinned (`check_shl_overflow`, `_tolower`, `isxdigit`, `skip_spaces` — all three seats say so:
`R49RevGR1c.md:26`, `R49CritGR1c.md:16`, `R49CritGR1b.md:20`), the run proves the shim's behaviour, not the
kernel's; it cannot raise the verdict's evidence class above the `file:line` citations that the counter already
checks. Exploit path: a seat reports "independently executed" as if the kernel had been run, and a later reader
upgrades a name-level reliance into an observation. Impact on the count: none demonstrable — each verdict is
still carried by its citations, and the harness outputs are receipted (except CritGR1b's, which has no output
file, so its "which I executed" claim is unauditable from the wave dir).

Smallest remediation: record the compiler/interpreter invocation and its version in the receipt dir (one line,
e.g. `cc (GCC) x.y.z; ./harness`), so the deviation is at least auditable; and for `R49CritGR1b` add the run's
transcript next to `gr1-parse-model.py`. For the lane: add a sentence to the counted-seat template that a
derived-code harness is outside the read class, so the next cohort does not opt in unilaterally.

## EXEC-UNAUTHORIZED-4 (low) — two seats re-read live host attributes; one receipted, one not

Evidence: `R49CritGR2c.md:83` "I also re-read the two live attributes as uid 1000 (receipt `lines.txt`)";
`:151` "I did re-read the two sysfs attributes live"; `R49CritGR2c/lines.txt` tail records
`## live sysfs, uid 1000, 2026-10-28T17:09:28Z` with `-r--r--r-- … replace_target` / `exclusive_operation` and
the values `none` / `0`. `R49CritGR2b.md:29` "the round-45 host-recheck report's probe transcript — I read its
section 3 and then re-read the two host files myself instead" — and `R49CritGR2b` has no receipt directory at
all.

Impact: read-only, and in `R49CritGR2c` the mode bits in the receipt prove it (`-r--r--r--`, uid 1000, no write
bit) — this is the best-practice shape of the deviation. In `R49CritGR2b` the observation is prose only, so the
verdict's host leg cannot be re-checked. Smallest remediation: same as EXEC-UNAUTHORIZED-2 — either cite the
pinned capture or record the probe.

## EXEC-NO-FINDING — no selftest, no out-of-wave write, no tracked edit, no missing report

- Selftest: no report declares one and no receipt contains a trace of one. Every seat that mentions the
  predicate says the opposite in terms (`R49RevGR1a.md:18`, `R49RevGR1b.md:98`, `R49RevGR1c.md:28`,
  `R49RevGR2a.md:123`, `R49RevGR2b.md:148-149`, `R49RevGR2c.md:75-76`, `R49RevGR3b.md:41`,
  `R49CritGR1a.md:23`, `R49CritGR1c.md:16`, `R49CritGR2a.md:26`, `R49CritGR2b.md:31`, `R49CritGR2c.md:157-158`,
  `R49CritGR3a.md:45`, `R49CritGR3b.md:18`). The receipts contain no `selftest`/`cases ==`/census output; the
  only counter output anywhere is the `--section-hash` JSON (e.g. `R49RevGR1a/quotes-check.txt:6`,
  `R49RevGR3b/section-hash.json`). What I did not do: I did not read process accounting or shell history, so
  this is "no declaration and no trace", not "proven not run".
- Writes outside the wave dir: no report claims one; every non-punctuation receipt path cited in the 18 reports
  resolves inside `.ufo/waves/round-49/w1/` (the two apparent misses, `R49RevGR1a/quotes-check.txt.` and
  `R49CritGR1a/receipt.txt.`, are my regex capturing a trailing full stop; both files exist). No cohort scratch
  dir survives under `/fast/scratch/hyaku/tsukuroi-r49/` — every seat's `mkdir -p` target is gone, which is the
  removal the seat rules require. Scratch leftovers of *other* seats exist there (`R49ExecFdB`, `R49RevCounter`,
  `R49ScribeAssim`, plus stray `R49ScoutCmd-srcpreview.md`, `R49ScribeAssim.tmp.923625`) but none belongs to the
  counted cohort and none is in my assignment's surface.
- Tracked-file edits: all 18 reports deny any edit to a lane byte; no receipt is an edited copy of a tracked
  file (the copies are whole-file extracts, e.g. `R49RevGR1a/gr1-entry-extract.md`,
  `R49CritGR2a/entry-55c07cd3-GR2-anchor.md`). I did not run `git status` or any jj read against the lane — the
  host guard forbids touching the lane index — so this is report-and-receipt evidence only.
- Reports present: all 18 binding files exist; no seat is missing and no verdict here is invented.

## Corroboration weakness (not a violation) — five cohort seats produced no receipt directory

`R49RevGR2c`, `R49CritGR2b`, `R49RevGR3c`, `R49CritGR3a`, `R49CritGR3b` have no `w1/<seat>/` directory
(`R49SentScopeA/evidence-listing.txt`, section 3). Receipts are optional in the seat rules, and none of the five
cites a receipt path, so nothing dangles. But for these five the evidence is prose only; a reader cannot
re-derive the hashes or quotes they report without redoing the work. No action required for the count.

# Collateral (outside the scope surface, integration-critical)

While reading the cohort I hit one result the L1 must not miss, because it decides claim C1 irrespective of any
scope finding:

1. `R49CritGR2b.md:1` is `ROW GR2 VERDICT: partly` on the current frozen GR2 hash
   (`d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f`). FROZEN.md states "A bound-format
   negative (`partly`/`fails`) on the current hash blocks the row whatever its citations", and the counter
   implements exactly that: `tools/check-scrub-admission-r49.py:364` puts the seat in `blocking`, and
   `:378-380` requires `not blocking` for `row_ok`. Therefore `verdicts_ok` cannot reach 3 and C1's predicate
   cannot pass. Cohort tally from the files: 17 `holds`, 1 `partly`.
2. `.ufo/waves/round-49/w1-results.json` does not exist yet (`ls`: "No such file or directory"), and the
   counter's `seats_ok` is derived from completed entries of that file (`:350-353`), so as of my read
   `seats_ok` would be 0 regardless of the 18 report files. `.ufo/waves/round-49/w1.ready.partial` maps all 18
   cohort seats to agent instances, which is the bookkeeping this file will need to encode.

Neither point is a scope violation; both falsify any "C1 PASS" statement made before GR2 is repaired and the
results file is committed.

# Not done

I ran no counter (neither C1, C2 nor C3, and no `--section-hash` either), no selftest, no git or jj command
against the lane, and no host probe. I did not verify any seat's claim about *content* (that is the per-row
seats' job and the counter's), only what each seat says it ran and what its receipts show. I could not
independently establish absence of selftest runs or of tracked-file edits — no process accounting, and the
host guard rules out `git status`/`jj` reads of lane state; both conclusions rest on the reports' own denials
plus the absence of traces in their receipts. Tooling: nothing installed, nothing upgraded.
