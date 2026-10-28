VERDICT: draft

# R50ScribeMistakes — D-3: draft `corpus/lessons/round-50.md` `## Mistakes` rows

Axes: (A) **calibration** — every number in a drafted row must trace to a measured source, not the
candidate's paraphrase; (B) **lesson** — a row names a class, a capturing instrument and a fix that
exists in bytes; (C) **non-fabrication** — candidates are accepted only where evidence supports them,
and corrected rather than rejected where the evidence narrows them. All lane bytes were read at the
freeze `8029cdba1049df25632c91a23c8db4eefb54be5f` via `git -C <lane> show`; nothing was run twice and
no census selftest or counter was executed (outside this item's EXEC-AUTHORIZED class, which named the
`git status --porcelain` sweep only; the other evidence is pre-recorded receipts and static reading).

## Findings per candidate

### Candidate 1 — the round-49 counter's citation leg — ACCEPTED, count corrected 17 → 16

Two independent measurements both say **16** of the 18 real seat reports were voided by the leg,
not 17:

- `.ufo/waves/round-49/after/c1-final.json` `seat_notes` has **16** entries, one refusal reason each
  (e.g. `"R49RevGR1a: check-scrub-admission-r49.py not a pinned snapshot file"`,
  `"R49CritGR2c: SOURCES.md not a pinned snapshot file"`). The two seats absent from the notes are
  `R49CritGR1c` (credited) and `R49CritGR2b` (blocked on `partly` *before* the citation leg —
  `check-scrub-admission-r49.py` at `55c07cd3` driver order: `partly`/`fails` → `continue` precedes
  `report_citations_ok`).
- `corpus/lessons/round-49-verifier-spotcheck.md` §7 defect 2 routes the fix, and
  `.ufo/waves/round-49/w1/R49RevCounter.md` §3 (line ~100) says "Measured on the 18 live GR reports:
  16 voided".
- Static replay (receipt `R50ScribeMistakes/cite-replay.txt`): tokenising the two survivors' bodies
  with the counter's own `CITE_RE` gives **0 non-pinned citations** in each — so both survivors are
  citation-clean and the refusal count is exactly 16.

Two corrections to the candidate's own wording:

- "which did not test a real report body" describes the **author's** battery, not the critic.
  `R49RevCounter` did test the live 18 (§0 `live-projection.txt`, §3). The author's K-pass used
  synthetic template bodies citing only `CITE[row]` (pinned snapshot files):
  `.ufo/waves/round-49/controls/battery.py:74-96` `report()` builds
  `f'{seat} read row {row} ... at {cite}'` — no real body, so the over-restriction never fired.
- The frozen round-50 counter's docstring itself repeats the wrong count:
  `tools/check-scrub-admission-r50.py:16` at `8029cdba` reads "the round-49 leg refused 17 of 18 real
  reports". Off by one — measured 16 (see drafted row 4 below).

The fix exists and is shown able to fail: `verify_citation` lane fallback +
`LANE_FILES` (`check-scrub-admission-r50.py:121-133`, `:279-289`, `:13-18`) bind lane/evidence
artifacts while requiring ≥2 distinct row-source files; control **K7** in
`.ufo/waves/round-50/controls/battery-summary-r50-c1.jsonl` — `{"control": "K7 lane-artifact citations
only", "expected": "FAIL", "got": "FAIL", ...}` — fails a cohort that cites only lane artifacts, and
K-pass `{"expected": "PASS", "got": "PASS"}` binds 18 valid reports.

### Candidate 2 — the census selftest false-fail — ACCEPTED, mechanism upgraded [INFERENCE] → measured

Evidence `.ufo/waves/round-49/w1/R49ExecSelfAssess.md` §4 (lines 58-112): a passing selftest printed a
self-contradicting `FAIL degraded: 4002 update candidates ... (R42-C1): plane evidence missing` while
the emitted `got:` line matched the reported-missing regex (verified `grep -qE` → rc=0 on the
extracted line). The seat left two candidate causes `[INFERENCE]`: (a) the `printf | grep -q` arm
under `pipefail` (`:2390`,`:2421` at `55c07cd3`), measured 4/20 false misses at 64 KiB and 11/20 at
96 KiB on the seat's standalone probe; (b) a transient `grep` failure.

Round-50 evidence settles (a): the C2 counter's own sensitivity probe (`check-selftest-matcher-r50.py`
`:17-29`,`:59-64` — same base idiom, 20 trials, 200 KB mid-stream buffer) scored `base_misses 20` for
the `printf | grep -q` idiom and `full_misses 0` for the full-read `awk`/`ENVIRON` idiom
(`battery-summary-r50-c2.jsonl` K0: `{"base_misses": 20, "cases": 167, "idiom_sites": 7}`; K-pass:
`{"idiom_sites": 0, "cases": 168, "case_ok": 1}`). My own grep confirms 7 live `printf ... | grep -q`
forms at `55c07cd3` (`:2373`,`:2379`,`:2390`,`:2421` for `"$out"`, plus 3 other buffers) and **0 live
forms** at `8029cdba` (only comments at `:732`,`:2230`,`:2569`,`:3646` name the idiom). The fix in
bytes: `buf_has`/`out_has` `tools/tsukuroi-census.sh:2236-2239` and the pinning case `(R50-C2)`
`:3643-3660`.

### Candidate 3 — misroot sweep — REPORTED, no mistakes row accepted

Command (receipt `R50ScribeMistakes/gitstatus.txt`):

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261028-hyaku-run11.md
?? .scratch/closure-mado-r50.json
?? .scratch/closure-r54/
?? .scratch/kasegi-r44/
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-50/tsukuroi.md
?? lane3/
?? o.bin
?? oldrep1.out
?? oldrep2.out
```

Exactly **one** untracked fleet-root file names this lane and round: `.ufo/reports/round-50/tsukuroi.md`
(2 `tsukuroi`, 4 `round-50` tokens). It is **not** a misroot: `.ufo/reports/<round>/<lane>.md` is the
fleet's tracked lane-report convention (871 tracked lane reports; `round-50/` already holds 10 tracked
sibling reports — `git ls-files .ufo/reports/round-50 | wc -l` → 10 — and tsukuroi.md is simply
uncommitted pending the L1's integration). A row asserting "this lane's report lives outside the lane"
would fabricate a defect; the file is where it belongs.

Misroot-*shaped* material found, none naming tsukuroi round 50:

- `lane3/` — a full `kengaku-shokunin` clone inside the fleet working tree (`remote url =
  /home/vgpnk/Projects/shokunin/kengaku-shokunin`, HEAD `297e179` "round-50: receipt notes…"):
  a sibling lane checkout at the fleet root.
- `.scratch/kasegi-r44/` — kasegi r44 seat dirs (`R44Critic5`, `R44Scribe5`); `.scratch/closure-*
  ` — mado r50 / r54 closure records; **no** tracked `closure` files exist under `.scratch`
  (`git ls-files .scratch | grep -c closure` → 0), so these are not a tracked convention.
- `oldrep1.out`/`oldrep2.out` (15 314 B each) — `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases...)`
  captures at the fleet root: tsukuroi tool output, but they name no round and predate round 50.
- `o.bin` — Cloudflare challenge HTML, zero lane/round hits.

### Found this sweep — the frozen docstring's off-by-one (extra row, optional)

While verifying candidate 1 the frozen counter's own docstring mis-states the measured count
(`check-scrub-admission-r50.py:16` "17 of 18" vs measured 16 — evidence above, three routes agree).
The row is a mistake of this round: an unmeasured count copied into a frozen docstring. It is not
correctable this round (the docstring is inside the bytes under test); the fix column records the
correction for a later revision.

## Drafted rows for `corpus/lessons/round-50.md` `## Mistakes`

Exact text to append to the existing table (`| class | evidence pointer | captured-by | fix |`):

```markdown
| Counter over-restricts the citation syntax of the reports it claims to grade: `check-scrub-admission-r49.py` `report_citations_ok` refused a report on the first `file.ext:NNN` token that was not a pinned snapshot file, so 16 of the 18 real round-49 seat reports earned nothing despite citing their row's sources | `.ufo/waves/round-49/after/c1-final.json` `seat_notes` (16 entries; the two citation-clean survivors replayed in `w1/R50ScribeMistakes/cite-replay.txt`); `corpus/lessons/round-49-verifier-spotcheck.md` §7 defect 2; `w1/R49RevCounter.md` §3 "16 voided" | `R49RevCounter`, measuring the live cohort; the author's K-pass battery used only template bodies citing `CITE[row]` (`round-49/controls/battery.py:74-96`), so the restriction never fired | `check-scrub-admission-r50.py` `verify_citation` + `LANE_FILES` (`:13-18`, `:121-133`, `:279-289`) binds lane/evidence artifacts and still requires >=2 distinct row sources; control K7 (`battery-summary-r50-c1.jsonl`) fails a lane-artifact-only cohort |
| Assertion idiom under pipefail cannot distinguish "evidence absent" from "reader died of SIGPIPE": the selftest's must-match arms `printf '%s\n' "$out" \| grep -qE` let `grep -q` exit on first match, killing the writer; a passing case printed a self-contradicting FAIL whose `got:` matched the reported-missing regex | `.ufo/waves/round-49/w1/R49ExecSelfAssess.md` §4 (lines 58-112); probe measured 4/20 false misses at 64 KiB, 11/20 at 96 KiB; round-50 C2 K0 control: `base_misses 20` for the idiom at 200 KB, `full_misses 0` (`battery-summary-r50-c2.jsonl`) — mechanism (a) settled | `R49ExecSelfAssess` (a self-assess seat; no gate read the counter's last captured line) — left as two `[INFERENCE]` candidates until the round-50 probe | `buf_has`/`out_has` full-read matcher `tools/tsukuroi-census.sh:2236-2239` + pinning case `(R50-C2)` `:3643-3660`; 7 live `printf \| grep -q` forms at `55c07cd3` → 0 at `8029cdba` (`idiom_sites 7 → 0`, `cases 167 → 168`) |
| Prose in a frozen docstring carried an unmeasured count: `check-scrub-admission-r50.py:16` says "refused 17 of 18 real reports"; three measurements agree on 16 | counter docstring at `8029cdba`; `c1-final.json` `seat_notes` (16); `R49RevCounter` §3 "16 voided"; replay of both survivors (`w1/R50ScribeMistakes/cite-replay.txt`) — `R49CritGR2b` exits the driver before the citation leg on its `partly` verdict, so it never reached `report_citations_ok` | this seat (D-3 sweep) | correct "17 of 18" → "16 of 18" in a later revision of the counter; the docstring is frozen for this wave |
```

No row drafted for the misroot sweep (candidate 3): the only naming hit is the correctly-placed fleet
report — the observation is recorded above and in `w1/R50ScribeMistakes/gitstatus.txt` for the L1's
attention, but a "misroot" mistakes row would assert a defect that does not exist for this lane/round.

## What I did not do

- Did not run the census `--selftest` or either counter (outside the item's authorized commands); all
  counter legs above are quoted from the recorded pre-data batteries, not re-executed.
- Did not edit `corpus/lessons/round-50.md` — this is the draft text for the integrator; the file's
  existing `## Mistakes` table (3 rows) is unchanged.
- No scratch dir used (no clones/fixtures needed); receipts written under `w1/R50ScribeMistakes/`.
- No tool installs.

Receipts: `w1/R50ScribeMistakes/gitstatus.txt`, `w1/R50ScribeMistakes/cite-replay.txt`.
