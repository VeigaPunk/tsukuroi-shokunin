# ExecReplicate — round 87, wave w1 — clean-room replication of C1 and every freeze control

Seat: ExecReplicate (leaf executor, operability axis). Lane revision measured throughout:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` = `cefb4188b484329c4908a19a277f8fb120fb4f56`
(same as the clean-room clone's HEAD, branch `master`, `git status --porcelain` empty before and after).
No lane file was edited; nothing was committed or pushed; `sudo`, `/boot`, `/efi` and `--live` were not used.

Verdicts
- **Kill rule / instrument identity: HOLDS.** Battery sha256 in the clone = `f2551c8e…61989d`, byte-identical to line 1
  of `.ufo/waves/round-87/before/freeze-manifest.sha256`. Kill rule ("void") not triggered.
- **C1 counting command: REPLICATED, 22/22 in three consecutive runs** at the landed tip, rc 0 each, 88 cases each,
  no failed families. Extra probes 4-6 also 22/22 rc 0.
- **Freeze controls: REPLICATED, 25/25.** Every control matches its frozen count and failed-family set; only P0 reads
  22/22; the only wobble is N06-prefix20, which the freeze itself disclosed as 11/11/12 and which stayed far below
  target in 16 total runs here (≤12/22).
- **Selftests: PASS.** Battery `--selftest` 5/5 rc 0 and candidate `--selftest` 14/14 rc 0, both from an unrelated cwd.
- **Out-of-predicate risks:** two (ESP path traversal, non-UTF-8 conf bytes); both confirmed by probe, both outside
  R1-R7 and outside the 22 families, advisory patch tested at 22/22 ×3 — L1 decides. Not claimed as defects.

## 1. Clean room and instrument identity

```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane"
$ git -C "$S/lane" rev-parse --show-toplevel   -> $S/lane
$ git -C "$S/lane" rev-parse HEAD              -> cefb4188b484329c4908a19a277f8fb120fb4f56
$ git -C "$S/lane" status --porcelain | wc -l  -> 0
$ cd "$S/lane" && sha256sum tools/limine-pin-battery-r87.py
f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d  tools/limine-pin-battery-r87.py
$ head -1 .ufo/waves/round-87/before/freeze-manifest.sha256
f2551c8e8386d599e3c2aca8888d5fbb0351a5a399dc43dc448556e99361989d  tools/limine-pin-battery-r87.py
```
Candidate gate unchanged since its own commit and hashed for the record:
`git diff --stat a097bd9d… -- tools/check-limine-pins.py` → empty;
`sha256sum tools/check-limine-pins.py` → `bbcc874ac8143ffb9bd97e4d3e2dfd934af3d6573f741d8b8ee3c00ecda9b73c`.

## 2. C1 counting command (judged runs)

`cd "$S/lane" && python3 tools/limine-pin-battery-r87.py --gate tools/check-limine-pins.py --work "$S/work" --json "$S/out/runN.json"`

| run | families_passed | rc | failed families | wall | cases | verdict |
|---|---|---|---|---|---|---|
| 1 | 22/22 | 0 | – | 2.72 s | 88 | met |
| 2 | 22/22 | 0 | – | 2.69 s | 88 | met |
| 3 | 22/22 | 0 | – | 2.74 s | 88 | met |
| 4 (probe) | 22/22 | 0 | – | – | 88 | met |
| 5 (probe) | 22/22 | 0 | – | – | 88 | met |
| 6 (probe) | 22/22 | 0 | – | – | 88 | met |

Raw stdout, verbatim, three times: `families_passed 22/22 verdict met failed -`.
Every receipt: `families_total 22`, `failed_families []`, `cases 88`, `case_log` = 88 entries over exactly 22 families
× 4 cases, each entry `passed: true` with `got == want` (rc, verdict and sorted per-pin `(line, status, consequence)`).
88 cases in ≤2.74 s ⇒ ≤31 ms per case, far inside the battery's per-case `TIMEOUT = 20`
(`tools/limine-pin-battery-r87.py:73`). Fixtures are per-run fresh and shuffled: `rng = random.Random(secrets.randbits(64))`
(`:514`), `rng.shuffle(plan)` (`:518`), file/dir names and bytes from `secrets`/`rng`, `CASES_PER_FAMILY = 4` (`:475`);
gate launched as `[sys.executable, gate, --conf, --esp]` with cwd = fixture dir, so cwd-independence of the gate is
exercised by construction.

## 3. Freeze controls, one re-run each in the clone

Compared to `.ufo/waves/round-87/before/controls/controls-summary.txt` (25 lines parsed). "match" = same families_passed
and same failed-family set as the freeze's first run; the freeze's own three-run columns are shown.

| control | ours | rc | failed families (ours) | freeze run1/2/3 | match |
|---|---|---|---|---|---|
| K1-gate-absent | 0/22 | 1 | all 22 | 0 0 0 | match |
| K2-lane-boot-chain-gate | 0/22 | 1 | all 22 | 0 0 0 | match |
| P0-reference | 22/22 | 0 | – | 22 22 22 | match |
| f1-constant-healthy | 0/22 | 1 | all 22 | 0 0 0 | match |
| f2-constant-degraded | 0/22 | 1 | all 22 | 0 0 0 | match |
| f3-sha256 | 2/22 | 1 | all but POSITIVE, MALFORMED-INPUT | 2 2 2 | match |
| f4-line-grep | 6/22 | 1 | GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, KEY-CASE, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MULTI-FAULT, OPTIONAL-SKIP, PANIC-DEFAULT, PANIC-FIRST, PANIC-NO-ONLY, SECUREBOOT, UNRESOLVED, WHITESPACE-CRLF | 6 6 6 | match |
| N01-comment-not-skipped | 21/22 | 1 | COMMENT-DECOY | 21 21 21 | match |
| N02-key-case-sensitive | 21/22 | 1 | KEY-CASE | 21 21 21 | match |
| N03-no-blank-strip | 1/22 | 1 | all but MALFORMED-INPUT | 1 1 1 | match |
| N04-first-hash | 21/22 | 1 | LAST-HASH | 21 21 21 | match |
| N05-gz-decompress | 21/22 | 1 | GZ-RAW | 21 21 21 | match |
| N06-prefix20 | 11/22 | 1 | HOST-SHAPE, KEY-CASE, LAST-HASH, MISMATCH-LATE, MULTI-FAULT, OPTIONAL-SKIP, PANIC-DEFAULT, PANIC-FIRST, PANIC-NO-ONLY, SECUREBOOT, WHITESPACE-CRLF | 11 11 12 | match to run1; see §4 |
| N07-hash-case-sensitive | 21/22 | 1 | HASH-UPPER | 21 21 21 | match |
| N08-no-format-check | 19/22 | 1 | HASH-LENGTH, HASH-NONHEX, MULTI-FAULT | 19 19 19 | match |
| N09-panic-not-yes-is-prompt | 21/22 | 1 | PANIC-NO-ONLY | 21 21 21 | match |
| N10-panic-last-wins | 21/22 | 1 | PANIC-FIRST | 21 21 21 | match |
| N11-ignore-secureboot | 21/22 | 1 | SECUREBOOT | 21 21 21 | match |
| N12-no-optional-skip | 21/22 | 1 | OPTIONAL-SKIP | 21 21 21 | match |
| N13-unresolved-as-missing | 20/22 | 1 | MULTI-FAULT, UNRESOLVED | 20 20 20 | match |
| N14-any-key-uri | 20/22 | 1 | COMMENT-DECOY, UNHASHED-DECOYS | 20 20 20 | match |
| N15-first-fault-only | 19/22 | 1 | HOST-SHAPE, KEY-CASE, MULTI-FAULT | 19 19 19 | match |
| N16-default-prompt | 14/22 | 1 | GZ-RAW, KEY-CASE, LAST-HASH, MISMATCH-EARLY, MISMATCH-LATE, MULTI-FAULT, PANIC-DEFAULT, WHITESPACE-CRLF | 14 14 14 | match |
| N17-missing-as-unresolved | 20/22 | 1 | MISSING, MULTI-FAULT | 20 20 20 | match |
| N18-conf-missing-rc1 | 21/22 | 1 | MALFORMED-INPUT | 21 21 21 | match |

"all 22" rows expand exactly to COMMENT-DECOY, GZ-RAW, HASH-LENGTH, HASH-NONHEX, HASH-UPPER, HOST-SHAPE, KEY-CASE,
LAST-HASH, MALFORMED-INPUT, MISMATCH-EARLY, MISMATCH-LATE, MISSING, MULTI-FAULT, OPTIONAL-SKIP, PANIC-DEFAULT,
PANIC-FIRST, PANIC-NO-ONLY, POSITIVE, SECUREBOOT, UNHASHED-DECOYS, UNRESOLVED, WHITESPACE-CRLF (verbatim in
`controls/*.json` and `controls/*.stdout`). No control other than P0 reached 22/22; no control's failed-family set
differs from the freeze (run1) set.

## 4. N06-prefix20 — the only nondeterministic control (freeze-disclosed)

The freeze summary already records `11 11 12` with a lighter third-run set, so this is not a divergence; I quantified it.
16 runs total (1 judged + 5 repeats + 10 extra): 11 families in 11 runs, 12 families in 5 runs, never ≥ 22.
Mechanism, from the case logs (`controls/N06-prefix20.json`, `probes/n06-*.json`): with a 20-hex prefix compare, a
fixture whose wrong hash was mutated beyond character 20 reads `OK` instead of `LP-MISMATCH` — e.g. a case with
`want [1,"DEGRADED",[[5,"LP-MISMATCH","prompt"],[8,"OK","none"]]]` and `got [0,"HEALTHY",[[5,"OK","none"],[8,"OK","none"]],0]`.
A family passes only when none of its 4 cases has a detectable mutation (mutation inside the first 20 chars, or a
byte-level file change), so the family count swings 11/12 by draw. Every failure is the right kind: a truncated-hash
gate reports a mismatching pin as healthy. Discrimination for "full-length compare" is carried by ≥11 families in every run.

## 5. Selftests (unrelated cwd, `$S`, not the clone)

```
$ python3 "$S/lane/tools/limine-pin-battery-r87.py" --selftest
absent PASS 0 | constant-healthy PASS 0 | non-json PASS 0 | constant-degraded PASS 0 |
reference-gate PASS 22      selftest PASS 5/5     rc=0
$ python3 "$S/lane/tools/check-limine-pins.py" --selftest
14 cases (ok, upper, mismatch-panic, mismatch-prompt, first-setting, secureboot, comment, missing, format,
unresolved, wallpaper-skip, non-path-key, crlf-blanks, conf-absent) all PASS; "selftest PASS 14/14"  rc=0
```
The battery's positive control resolves the reference gate via `__file__`, not cwd, and read 22/22 from `$S`.
Receipts: `selftest/battery-selftest.txt`, `selftest/candidate-selftest.txt`.

## 6. Entry C2 — factual presence only (not judged here)

At the tip, `corpus/knowledge/limine-pin-plane-r87.{md,json}` exist; the JSON is a list of 8 rows `LP1`…`LP8` with keys
`id, statement, source, quote, host_value`; `corpus/SOURCES.md` carries S350-S354. That is a structural check only —
the scorecard assigns C2's verdict to the non-author hyaku closure, and a wave seat is the lane; I make no judgment on
its depth and did not treat the entry's content as instructions.

## 7. Risks found (out of predicate; **not** claimed as defects; L1 decides)

Both are outside the frozen rule set R1-R7 and outside the battery's 22 families, so neither contradicts C1. Advisory
patch: `proposals/exec-replicate-r87-advisory.diff` (against `tools/check-limine-pins.py`, 8 insertions, 2 deletions).

- **R-1, ESP escape via `..` — `tools/check-limine-pins.py:121`** (`target = os.path.join(esp, *uri["path"].split("/"))`).
  Probe: conf `path: boot():/../outside/x.efi#<true hash>`, `--esp …/esp` → `{"status":"OK","consequence":"none",
  "file":"…/esp/../outside/x.efi"}`, `rc=0 HEALTHY`. Under `--live` (root) this is a read/hash oracle for any file
  outside the ESP and can read HEALTHY for a pin Limine may not resolve the same way. Advisory fix: reject any `..`
  component as `LP-UNRESOLVED` (rc 2). Patched copy re-tested: probe → `LP-UNRESOLVED` rc 2; battery 22/22 ×3; selftest 14/14.
- **R-2, invalid UTF-8 in a conf path — `tools/check-limine-pins.py:83`** (`f.read().decode("utf-8","replace")`).
  Probe: file name byte `0xff`, matching hash → `LP-MISSING` (file looked up as `k\ufffd.efi`), rc 1. Limine reads bytes,
  so this is a false DEGRADED (safe direction, still wrong). Advisory fix: `decode("utf-8","surrogateescape")`.
  Patched copy re-tested: probe → `OK` rc 0; battery 22/22 ×3; selftest 14/14.
  (Both fixes are in the single advisory diff; patched gate sha256 `7d3deece…c02304f`.)

Not modelled and not probed: macro expansion, Secure Boot's unhashed-path rule, per-protocol missing-file effect —
already frozen as limits in the battery docstring.

## 8. Refusals / not run

- `--live` was **not** run (sudo forbidden); the L1 receipt `.ufo/waves/round-87/after/live-receipt.txt` was read and
  quoted instead (LP-MISMATCH lines 30/38, consequence `prompt`, `hash_mismatch_panic` line 8 = `no`, rc 1, and the
  before/after `/boot` b2sum list digest `0f6acc28…560028` identical).
- No `sudo`, no `/boot`, `/efi`, `/sys`, `/proc`, no `objcopy`/`strip`/`sbsign`/`ukify`/`mkinitcpio`/`limine*`/`pacman`.
- No lane edit, commit, push or jj mutation; no sibling lane touched; `agent://all` not used; no subagent spawned.
- No file outside `.ufo/waves/round-87/w1/` written (this report plus `ExecReplicate/` only). Scratch removed after receipts were copied.

## 9. Receipts

`ExecReplicate/run{1..6}.json|stdout`, `time{1..3}.txt`, `patchrun{1..3}.json`,
`controls/<control>.json|stdout` (25 each), `controls/controls-summary-replaced.txt`,
`probes/n06-{1..5}.json` and `probes/n06-extra-runs.txt` (10 further runs), `probes/*.json` for the two risk probes,
`selftest/*.txt`, `proposals/exec-replicate-r87-advisory.diff`, `proposals/patched-gate.sha256`,
`RECEIPT-SHA256.txt` (sha256 of every copied receipt), `EVIDENCE.txt` (verbatim commands and outputs).
