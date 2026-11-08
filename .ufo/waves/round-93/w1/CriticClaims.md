# CriticClaims — r93 w1: claim-wording review

Scope: falsify the CLAIMS' wording, not their arithmetic (Amendment 59). Read
`.ufo/plans/round-93.md`, `.ufo/waves/round-93/claims.json`, SCORECARD "Round 93 — declaration",
the landed gate (`tools/check-limine-pins.py`), the r93/r92 batteries, the after receipts and the
w1 executor/critic receipts. Raw commands and outputs: `w1/CriticClaims/evidence.md`.
Scratch deleted at exit; no lane writes except this file and `w1/CriticClaims/`.

## F1 — C1 item 1: "four families the r92 roster did not have" — **neutral**

Exact sentence (`claims.json` C1 predicate, same in `plans/round-93.md`): `four families the r92
roster did not have — ERA-EXACT-125 (version exactly 12.9.5; a first-line-entry config's
hash_mismatch_panic: no is invisible, so its mismatch pin's consequence is panic), ERA-B-FIRST-BODY
(12.9.6; a hash_mismatch_panic: no key on the line immediately after the first entry label is
invisible, so the mismatch consequence is panic), ERA-B-U1 (12.9.6; an unhashed efi image line
inside an entry body appears in unverified_image_lines) and REFUSAL-VERSIONS (each of ten values
outside X.Y.Z exits 64 with empty stdout and no verdict)`.

- r92 roster lacks all four: `grep -c` 0 each in `before/controls/do-nothing-battery-r92.py`;
  r92 89 families, r93 96; `w1/ExecBends/summary.json` `in_r93_not_r92` is exactly the 7 new names,
  `in_r92_not_r93` empty; `after/do-nothing-roster.txt`.
- The claim's first sentence (r92 names three era limits it does not sample; 12.9.5 is passed only
  to an era-invariant family) is true: the only r92 family at 12.9.5 is `ERA-GLOBAL-KEY-A`
  (`_era_global_key(c, "12.9.5")`, line 1588; `prompt` in both eras), and r92 M02/M13/M18 name the
  three limits (`.ufo/plans/round-92.md:171-184`).
- ERA-EXACT-125 dump: line 1 is the entry, line 3 the mismatch pin, line 4 the key; want
  `(1, DEGRADED, [(3, LP-MISMATCH, panic), ...])`. ERA-FLE-PANIC-B (same seed) has the same 7-line
  shape and the same expected answer; only the `--limine-version` argument differs (12.9.5 vs
  12.9.6). The boundary is isolated by the *input version*, not by a different expected answer; the
  claim does not say otherwise. N01 (strict `>`) kills only ERA-EXACT-125 (95/96 ×3).
- ERA-B-FIRST-BODY dump: line 1 `/haf-cfgwpbbb`, line 2 `hash_mismatch_panic: no` — literally the
  line immediately after the first entry label; line 4 pin; want `panic`; the key is in the entry
  body (no global section).
- ERA-B-U1 dump: lines 1–2 header, line 3 entry, line 4 `protocol: efi`, line 5
  `path: 43jflha65p.efi` (unhashed, first path of the entry, inside the body), line 6 pin;
  `want_unverified == [5]`; the shape is reported and changes no pin verdict.
- REFUSAL-VERSIONS is one Case with `usage` = exactly the ten values; `run_battery` routes it to
  `run_usage` as ONE `case_log` entry and loops all ten; the landed c1-canonical rows are all
  rc 64 / stdout 0 bytes. N04 (refusal deleted) rows are rc 1 / stdout 0 bytes — an uncaught
  traceback — so the family's `rc == 64` test distinguishes the refusal from the crash.
- No narrowing. Note for the L1: the expected answer of ERA-EXACT-125 equals ERA-FLE-PANIC-B's;
  a reader must not expect the "boundary" to be visible in the expected answer. The family is a
  version-argument twin of the r92 first-line case, which is exactly the named limit.

## F2 — C1 item 2: "0 error rows" — **neutral**

Exact: C1 target `every case row error null`; C1 kill `unmet if any case row carries a non-null
error`; SCORECARD "0 error rows"; `count-runs.py` counts `e.get("error") is not None`.

- JSON, `count-runs.py` and the claim use the same definition: the `case_log[]` `error` field,
  non-null.
- A family cannot pass with a non-null error: in `run_battery` a non-usage case with `err` has
  `got is None`, so `ok` is False and the family cannot be in `passed`; a `met` run with one
  non-null error row is impossible from `run_battery`. The kill rule and `count-runs.py` both read
  such a run `unmet`.
- All after receipts (landed c1-canonical, every bend) have 0 error rows. The only 8-error receipt
  is `after/c2-donothing-r92-gate.json` (four AUTO-ERA-A + four AUTO-ERA-B bad-output rows), which
  is the do-nothing control, not a claim target.
- No narrowing. Caveat for the L1: usage-family failures always carry `"error": None` (the failure
  is in `rows`/`got`; N04's ten refusal rows are `ok:false`, rc 1), so "0 error rows" is NOT
  equivalent to "no failed case". The `failed_families` / named-family clause proves the usage
  family; do not cite "0 error rows" alone as a clean-case proof.

## F3 — C2 item 3: source field on every JSON path — fields **neutral**; the `--live` `rc 1` parenthetical **falsifies-wording**

Exact: `records the resolved value in JSON limine_version and its origin in
limine_version_source: probe, selects the visibility era from that value, and refuses (rc 64, empty
stdout, no verdict) when the probe fails`; and `python3 tools/check-limine-pins.py --live
--limine-version auto on this host prints limine_version 12.9.4 with limine_version_source probe
(rc 1, the two operator-owned pin mismatches at /boot/limine.conf lines 30 and 38)`.

Field presence (no narrowing): `check()` has exactly two returns, both carry `limine_version` and
`limine_version_source`; `main` passes `(probed, "probe")` into both. The unreadable-conf path with
`auto` prints `{"limine_version": "12.9.4", "limine_version_source": "probe", "rc": 2,
"verdict": "CANNOT-EVALUATE"}`; the unprivileged `--live` run prints the same two fields with rc 2;
the probe-fail path prints no JSON, which the claim's "rc 64, empty stdout, no verdict" covers. The
claim does not demand the fields where it says there is no verdict.

Live rc-1 parenthetical (falsifies-wording): `/boot` is `drwx------ root root`; uid 1000 cannot
stat `/boot/limine.conf`. The named command as the lane user prints rc 2 `CANNOT-EVALUATE` with
`error: conf unreadable: [Errno 13] Permission denied` — and still `limine_version 12.9.4`,
`limine_version_source probe`. The rc-1 result with `LP-MISMATCH line 30/38` is
`after/live-c2.json`, whose pins carry blake2b of `/boot/EFI/Linux/*.efi`; it must have been produced
with root read access (the lane seats hold no sudo; `w1/ExecLive.md` says the seat cannot read
`/boot` and "the root live receipt stay with the L1"). `after/live-boot-digest-before.txt` equals
`...-after.txt`, so the privileged run was read-only. The live *target* (fields/version/source) is
met unprivileged too; only the rc-1/pin parenthetical is privilege-specific.

Narrowing the L1 must record: amend the predicate to "the root live receipt, produced with read
access to the 0700 `/boot`, prints ... rc 1, the two pin mismatches at lines 30 and 38; the
unprivileged lane invocation prints the same `limine_version`/`limine_version_source` with rc 2
`CANNOT-EVALUATE`", and record the producer/context (the L1/root, not a seat). Artifacts:
`claims.json` C2; `plans/round-93.md` C2; `after/live-c2.json`; `after/live-boot-digest-*.txt`;
`w1/ExecLive/live.stdout`; `w1/ExecLive.md`.

## F4 — C2 item 4: probe grammar, timeout attribution, execution — **falsifies-wording**

Exact: `resolves the installed bootloader by running limine --version read-only (PATH lookup, 5 s
timeout, the first X.Y.Z in its output)`; and the Named limits sentence `the probe's 5 s timeout and
first-X.Y.Z parse are certified by the gate's selftest rows (probe-version), not by a battery
family`.

- The code is `re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b", p.stdout)` — the first X.Y.Z
  *immediately following the word `limine`* (optional `v`), not the first X.Y.Z in the output.
  Counterexamples (read-only fake scripts, `w1/CriticClaims/evidence.md` §5):
  `12.9.6` -> `None` (rc 0, the first X.Y.Z, no other text); `Limine version: 12.9.6` -> `None`;
  `gcc 13.2.1` + `Limine 12.9.6` -> `12.9.6` (the second X.Y.Z). `w1/CriticForgers/summary.json`
  A4 states the same: independent docstring-literal = "first bare `X.Y.Z` anywhere", landed gate =
  "requires a `limine` token before the version", and **no family samples it** (every fake prints
  `Limine X.Y.Z`). `w1/ExecLive.md` repeats the overbroad "parses the first `X.Y.Z`" while its own
  `h` (version only on stderr) returns None and `f` (v-prefix) returns 12.9.5.
- The timeout is implemented (`timeout=5`, `TimeoutExpired` is a `SubprocessError`) and exercised in
  `w1/ExecLive/probe-isolated.json` `d_fake_sleep6` -> `None` at 5.012 s. The `probe-version`
  selftest row (`check-limine-pins.py:452-459`) tests `Limine 12.9.6`, `Limine 12.9.4`+license,
  `exit 1`, `no version here`, absent — **no timeout**. The Named-limits attribution is false; the
  behavior is not uncertified, it is certified by a different receipt.
- Execution: `w1/CriticForgers.md` §3 / `summary.json` `survivors:["f6"]`, `leakage`: `f6` reads
  `<cwd>/bin/limine` source and reads 96/96 `met` (384 cases, 0 errors; AUTO-ERA-A/B and
  AUTO-PROBE-FAIL all pass) **without executing `limine --version`**. The fake source is
  `echo "Limine <expected>"` or `exit 1`, so the case directory carries the expected
  version/refusal; the battery docstring's "Fixtures carry no answer ... no expected value on disk"
  is false for the three AUTO families. The auto families certify the JSON/era result, not the
  probe mechanism.

Narrowing the L1 must record: (a) the parse clause -> "the first `X.Y.Z` immediately following
`limine` (case-insensitive, optional `v`); a bare `X.Y.Z` or a version after other text is a probe
failure"; (b) the timeout -> "implemented and exercised by `w1/ExecLive/probe-isolated.json`
`d_fake_sleep6` (5.012 s), not by the `probe-version` selftest row"; (c) the C2 assurance -> "the
auto families certify the era selection and JSON result, not that the gate executed `limine
--version`; `f6` passes 96/96 by reading the fake's source; the fake source leaks the expected
version/refusal." The C2 target numbers (auto families met, N05/N06 unmet, live JSON fields) are
not falsified. The smallest safe correction is an amendment (A3) plus the battery-docstring /
`probe_limine_version` docstring wording; a later round that adds a bare-version family and a fake
marker would close the gap.

## F5 — C2 item 5: the do-nothing legs — **neutral; A1 is the correct narrowing**

Exact: `the r92 gate ... rejects auto with rc 64, so all three auto families fail on it — measured,
not asserted` (plan C2 do-nothing); A1.

- `after/c2-donothing-r92-gate.json`: 94/96 `unmet`, failed `AUTO-ERA-A,AUTO-ERA-B`, 8 error rows;
  `w1/ExecBends/do-nothing-gate.json` the same, `auto_probe_fail [4,0]` (the family **passes** on
  the r92 gate). A gate that refuses every `auto` satisfies a family that expects a refusal when the
  probe fails. A1's correction is accurate: the control proves the 96/96 target unreachable on the
  r92 gate via the two era families; `AUTO-PROBE-FAIL` is vacuous there and N06 is its anti-vacuity
  (probe failure -> 12.9.4; canonical after 3, clone `w1/ExecAutoReplicate/n06.json` 3, `unmet`,
  `AUTO-PROBE-FAIL`).
- The SCORECARD C2 do-nothing cell (`the r92 gate (rejects auto with rc 64); N05/N06`) does not
  contain the false "all three fail" sentence; the false sentence lives in the plan's frozen
  do-nothing paragraph, and A1 narrows it. No new narrowing beyond A1; the L1 should cite A1, never
  the frozen sentence.
- The C1 do-nothing (r92 battery 89 families, none of the four; `grep -c` 0;
  `w1/ExecBends/do-nothing-battery.json` 89/89 `met` on the landed gate) is an instrument-level
  control: the old battery cannot report the 96/96 target. It does not prove the gate lacks the C1
  behavior; the bends N01-N04 do. The plan's sentence "the pre-change instrument cannot reach the
  target" is true.
- Answer to the item's question: the r92-gate leg proves the *pre-change gate* cannot reach
  96/96; it does not prove "no V3-free gate" fails (a different gate could, in principle, pass two
  of the three auto families by other means), and it does not prove `AUTO-PROBE-FAIL` is
  non-vacuous — N06 does. A1's "unreachable without V3" should be read as "on the r92 do-nothing
  gate", which is what the receipt measures.

## F6 — both claims: the freeze-manifest void rule is already red on the plan line — **falsifies-number / falsifies-wording**

Exact: C1 kill `void if any instrument byte differs from
.ufo/waves/round-93/before/freeze-manifest.sha256 at scoring time`; C2 kill `void if any instrument
byte differs from the freeze manifest at scoring time`; SCORECARD C2 kill `void on a
freeze-manifest mismatch`.

- `sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` (lane root) exits 1: 13 lines
  OK, `.ufo/plans/round-93.md: FAILED`. Manifest line 4 is `4600cfa3…` = the plan at the freeze
  commit c633f49 (`git show c633f49:.ufo/plans/round-93.md | sha256sum` = `4600cfa3…`); the current
  plan is `3668f0e8…`; `git diff` is exactly the 14-line Amendment A1 append.
  `before/instruments.sha256` has the 13 non-plan lines and all are OK; `w1/ExecBends/freeze-check.txt`
  reports the same; `w1/ExecBends/summary.json` has `instrument_hashes_manifest_ok: true` and
  `manifest_plan_mismatch` cause "post-freeze Amendment A1 appended". The clone at c633f49 passes
  all 14 (`w1/ExecReplicate/clone-identity.txt`).
- The plan's own preamble authorizes appended amendments, and the plan is the *declaration*, not one
  of the 13 instruments; the 13 instrument bytes do not differ. But the claim's kill rule and the
  SCORECARD's unconditional "void on a freeze-manifest mismatch" are written as if the manifest
  were the 13 instruments, while the frozen file has 14 lines (the seat spec's "13 lines" is this
  miscount: 13 instruments + the plan = 14). A literal `sha256sum -c` / a validator that voids on
  any manifest failure voids the round on the authorized A1 append.
- Narrowing (A2): the void set is the 13 lines in `before/instruments.sha256` (all OK); the
  freeze-manifest line 4 is the pre-A1 declaration snapshot, exempt because the plan's amendment
  clause authorizes the append; do not re-stamp the frozen manifest in place. The L1 must record
  the exact red line, the A1 diff and the exemption; the C1/C2 predicates and numbers are
  unaffected. Receipts: `w1/ExecBends/freeze-check.txt`, `w1/ExecBends/summary.json`,
  `w1/ExecReplicate/clone-identity.txt`, `w1/CriticClaims/evidence.md` §7.

## F7 — C1 target: the clone bend "×3 both layouts" is 1/3 in the read receipts — **falsifies-number / evidence gap**

Exact: C1 target `N01 failed_families contains ERA-EXACT-125; N02 contains ERA-B-FIRST-BODY; N03
contains ERA-B-U1; N04 contains REFUSAL-VERSIONS; each x3 both layouts`; kill `unmet if any named
bend does not read unmet in all three runs in both layouts`.

- Canonical `after/bend-N01..N04.json`: 3 runs each (95/96, 88/96, 95/96, 95/96), named family
  present, 0 error rows; `after/bend-family-matrix.txt` confirms the 3-run matrix.
- Clone `w1/ExecReplicate/N01..N04.json`: **1 run each** (95/96, 88/96, 95/96, 95/96, named
  family, 0 error rows); `compare-clone-vs-canonical.txt` says `mine_runs=1 canonical_runs=3`,
  `OVERALL_MATCH=True`. The clone landed-gate `w1/ExecReplicate/c1-gate.json` is 3 runs 96/96
  `met`; the clone C2 bends `w1/ExecAutoReplicate/n05.json`/`n06.json` are 3 runs each; the canonical
  C2 bends are 3 each. The missing leg is exactly the four C1 bends in the clone.
- `w1/ExecReplicate-6` (the sub-seat "Verifying bends and freeze manifest in clone") has no directory
  on disk at this review; its three-run-per-bend output is not in the read receipts. The
  `ExecBends` canonical bend JSONs are 1 run each (extra cross-checks, not the claim's leg).
- The claim's "×3 both layouts" is therefore not evidenced for N01-N04 in the clone: 1 run each is
  not "all three runs in both layouts", and the kill rule would read the C1 target `unmet` if scored
  from the read receipts. The L1 must attach the `ExecReplicate-6` sub's 3 clone runs per bend (or
  run the two missing per bend in the clone) before scoring C1 `met`; the canonical 3 + clone
  c1-gate 3 + clone C2 3 are fine.

## Verdict

**C1 — supported on its predicate/families; not falsified on wording; the target is not yet fully
evidenced.** The four new families are real (r92 89 / grep 0; ERA-EXACT-125 line/answer dump;
ERA-B-FIRST-BODY line 2; ERA-B-U1 body image line; the ten-value one-case refusal; N04 rc 1 vs the
rc-64 test), the landed gate is 96/96 `met` ×3 canonical and ×3 clone, N01–N04 are `unmet` ×3
canonical with their named family and 0 error rows, and the "0 error rows" definition is consistent
(F1/F2). The clone bends are 1 run each, not ×3 (F7), and the freeze manifest's plan line is red
from the authorized A1 append (F6); the L1 must land the missing clone runs and record the
13-instrument/A1 exemption before C1 can be scored `met`. Receipts: `after/c1-canonical.json`,
`after/bend-*.json`, `after/bend-family-matrix.txt`, `w1/ExecReplicate/*`, `w1/ExecAutoReplicate/*`,
`w1/ExecBends/*`, `w1/CriticClaims/evidence.md`.

**C2 — supported on the field presence, the auto-family numbers (96/96 ×3 canonical + clone
`c1-gate` ×3), N05/N06 ×3 both, and the live JSON's 12.9.4/`probe`; two predicate clauses are
falsified as worded.** (i) The live `(rc 1, ...)` parenthetical is the root/L1 receipt, not the
unprivileged lane command, which returns rc 2 `CANNOT-EVALUATE` with the same two fields (F3);
(ii) the `first X.Y.Z` parse is actually the first X.Y.Z immediately after `limine`, no family
samples a bare version, the 5 s timeout is exercised by `w1/ExecLive/probe-isolated.json`
`d_fake_sleep6` and not by the `probe-version` selftest row, and `f6` reads 96/96 without executing
the probe (the fake's source carries the expected version), so the auto families certify the
JSON/era result, not the mechanism (F4). The C2 target numbers are not falsified; the L1 must amend
the predicate and the Named limits (A3), record the `f6` leakage, and record the A2 manifest
exemption. The do-nothing legs are correctly narrowed by A1 (F5). Receipts:
`after/c1-canonical.json`, `after/live-c2.json`, `after/live-boot-digest-*.txt`,
`w1/ExecLive/*`, `w1/ExecAutoReplicate/*`, `w1/ExecReplicate/c1-gate.json`,
`w1/CriticForgers/{summary.json,f6.json,CriticForgers.md}`, `w1/CriticClaims/evidence.md`.
