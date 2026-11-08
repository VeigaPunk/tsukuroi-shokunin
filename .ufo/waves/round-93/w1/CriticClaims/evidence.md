# CriticClaims — raw evidence (r93 w1)

All commands read-only; scratch under /fast/scratch/hyaku/tsukuroi-r93/CriticClaims (deleted at exit).
Lane root: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin; HEAD c633f49aa512e1c8a0e0464b7fb5d354c70096cf.

## 1. Rosters
`grep -c` in `before/controls/do-nothing-battery-r92.py`:
ERA-EXACT-125 0, ERA-B-FIRST-BODY 0, ERA-B-U1 0, REFUSAL-VERSIONS 0,
AUTO-ERA-A 0, AUTO-ERA-B 0, AUTO-PROBE-FAIL 0.
r92 FAMILY_ROSTER 89 / FAMILIES 89; r93 FAMILY_ROSTER 96 / FAMILIES 96.
r92 Case has no `usage` attribute. The only r92 family at 12.9.5 is `ERA-GLOBAL-KEY-A`
(`_era_global_key(c, "12.9.5")`, line 1588; want `(1, 'DEGRADED', prompt)`, global lines [1,2,3] —
era-invariant by its own docstring). r92 plan M02/M13/M18 names the three era limits
(`.ufo/plans/round-92.md:171-184`). `after/do-nothing-roster.txt` and
`w1/ExecBends/summary.json` `in_r93_not_r92` = the 7 new names; `in_r92_not_r93` = none.

## 2. Fixture dumps (battery module imported read-only; random.Random(1234))
ERA-EXACT-125 (version 12.9.5, era_b True, global_lines []):
  1 /haf-cfgwpbbb
  2   protocol: efi
  3   path: boot():/...efi#<128hex>        (LP-MISMATCH)
  4 hash_mismatch_panic: no
  5 /eavj4ykde-5ke
  6 \tprotocol: efi
  7   path: boot():/...efi#<128hex>        (OK)
  want (1, DEGRADED, [(3, LP-MISMATCH, panic), (7, OK, none)]), meta r1_panic None.

ERA-FLE-PANIC-B (same seed; version 12.9.6): the same 7-line shape and the same want
((3, LP-MISMATCH, panic)); only the pin blob bytes differ. The isolating input is the
`--limine-version` argument, not a different expected answer.

ERA-B-FIRST-BODY (12.9.6): line 1 `/haf-cfgwpbbb`, line 2 `hash_mismatch_panic: no`,
line 3 `  protocol: efi`, line 4 pin LP-MISMATCH, line 5 next entry, line 7 pin OK.
want (1, DEGRADED, [(4, LP-MISMATCH, panic), (7, OK, none)]); r1_panic None; global_lines [].

ERA-B-U1 (12.9.6): line 1 `timeout: 7`, line 2 `### generated header ...`, line 3 `/-cfgwp`,
line 4 `protocol: efi`, line 5 `  path: 43jflha65p.efi` (unhashed; image line, inside the
entry body), line 6 `  path: boot():/...#<128hex>` (OK). want_unverified [5];
want (0, HEALTHY, [(6, OK, none)]); global_lines [1,2].

REFUSAL-VERSIONS: one Case; `usage` = ("12.9", "12.9.5.1", "abc", "", " 12.9.5", "12.9.5 ",
"+12.9.5", "12..5", "12.9.5-rc1", "9"*5000 + ".0.0"); conf is one empty line.
`run_battery` routes it to `run_usage` as ONE case_log entry, looping all ten.
Landed c1-canonical rows: each version rc 64, stdout_bytes 0, ok True.

AUTO-PROBE-FAIL: conf lines 1-5, header `/entry`/pin; `auto="fail"`, fake `bin/limine` = `exit 1`;
`run_usage` values ["auto"] -> expect rc 64, empty stdout.

## 3. N04 (refusal deleted) rows
`after/bend-N04-accept-any.json`, all 3 runs, REFUSAL-VERSIONS: passed False, error None;
each of the ten rows `rc 1 stdout_bytes 0 ok False`; `got` string lists rc=1 stdout=0.
The family tests `rc == 64 and stdout.strip()==""`; rc 1 (uncaught traceback) is not a refusal,
so rc 64 separates it. The failure is in `rows`/`got`; the `error` key stays None.

## 4. Error-row definition
`count-runs.py`: `errors = sum(1 for e in r.get("case_log", []) if e.get("error") is not None)`.
Non-usage case in `run_battery`: `got, err = run_gate(...)`; `ok` requires `got is not None`, so a
non-null error -> got None -> case failed -> family failed -> verdict unmet.
Usage case: `log.append({..., "error": None})` always; pass/fail is `ok` from `run_usage`
(failure detail in `rows`/`got`). No case can pass with a non-null `error`; a `met` run with a
non-null error row is impossible from `run_battery`; count-runs and the kill rule read it unmet.
All after c1-canonical/bend JSONs: 0 error rows (the c2-donothing r92 gate has 8, from the four
AUTO-ERA-A + four AUTO-ERA-B bad-output rows).

## 5. Gate probe (tools/check-limine-pins.py)
`probe_limine_version`: `subprocess.run([executable, "--version"], capture_output=True, text=True,
timeout=5)`; catches `(OSError, subprocess.SubprocessError)`; `re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b",
p.stdout)`.
Fake scripts (read-only import; /fast scratch):
  "12.9.6"                          -> None       (rc 0, first X.Y.Z in output, no `limine` token)
  "Limine version: 12.9.6"          -> None
  "gcc 13.2.1"; "Limine 12.9.6"     -> "12.9.6"   (the second X.Y.Z in the output)
  "Limine 12.9.6-rc1"               -> "12.9.6"
  "Limine 12.9.5.1"                 -> "12.9.5"
  "Limine 12.9.6"                   -> "12.9.6"   (control)
  sleep 6                           -> None after 5.01 s
`w1/ExecLive/probe-isolated.json`: a 12.9.4; b "Limine 12.9.6" 12.9.6; c exit1 None; d sleep6
None 5.012 s; e "no version" None; f "Limine v12.9.5 (x86_64)" 12.9.5; g absent None; h stderr-only
None. `w1/CriticForgers/summary.json` A4: independent docstring-literal = "first bare X.Y.Z
anywhere"; landed gate = "requires `limine` token before the version"; family that samples it: none.
`w1/CriticForgers.md` §3: f6 reads `<cwd>/bin/limine` source, never executes `limine --version`,
96/96 met; the fake source is `echo "Limine <expected>"`/`exit 1`.
Selftest `probe-version` row (gate lines 452-459): "Limine 12.9.6", "Limine 12.9.4"+license,
exit 1, "no version here", absent — no timeout case.
`after/battery-selftest-noref.txt`: constant-healthy families_passed=0; selftest 5/5.

## 6. Live
Host: `/boot` = `drwx------ root root`; `/boot/limine.conf` stat = Permission denied; uid 1000;
`limine --version` = "Limine 12.9.4". `w1/ExecLive.md`: the seat cannot read /boot.conf (EACCES),
holds no sudo; "the root live receipt stay with the L1".
Unprivileged run of the named command:
`python3 tools/check-limine-pins.py --live --limine-version auto`
-> one JSON: {"error": "conf unreadable: [Errno 13] Permission denied: '/boot/limine.conf'",
"limine_version": "12.9.4", "limine_version_source": "probe", "rc": 2,
"verdict": "CANNOT-EVALUATE", "visibility_era": "pre-12.9.5", "secure_boot_source": "efivar"}.
`after/live-c2.json`: rc 1, DEGRADED, version 12.9.4, source probe, findings
["LP-MISMATCH line 30", "LP-MISMATCH line 38"], pins' blake2b of /boot/EFI/Linux/*.efi;
`after/live-boot-digest-before.txt` == `after/live-boot-digest-after.txt` (identical).
`check()` has two returns; both carry limine_version/limine_version_source. Unreadable-conf with
auto (rc 2) also carried both. The rc-64 probe-fail path prints usage/stderr and no JSON.

## 7. Freeze manifest
`sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` (lane root): 13 lines OK,
`.ufo/plans/round-93.md: FAILED`; rc 1.
manifest line 4 = 4600cfa32563d267ca2ded47168e55b63f4d2c60e4b11aadfb87ecb706d28002;
`git show c633f49:.ufo/plans/round-93.md | sha256sum` = 4600cfa3…; current plan = 3668f0e8…;
`git diff` = 14 added lines (Amendment A1 only). `before/instruments.sha256` = 13 lines
(everything except the plan) all OK. `w1/ExecBends/freeze-check.txt` reports the same;
`w1/ExecBends/summary.json` `instrument_hashes_manifest_ok: true`, `manifest_plan_mismatch` cause
"post-freeze Amendment A1 appended 03:10:09 vs manifest 03:04:56". The clone at c633f49 passes all
14 (`w1/ExecReplicate/clone-identity.txt`).

## 8. Run counts
Canonical after: c1-canonical 3 runs 96/96 met; bend-N01 3 (95/96, ERA-EXACT-125),
N02 3 (88/96, incl. ERA-B-FIRST-BODY), N03 3 (95/96, ERA-B-U1), N04 3 (95/96, REFUSAL-VERSIONS),
N05 3 (95/96, AUTO-ERA-B), N06 3 (95/96, AUTO-PROBE-FAIL); 0 error rows each.
Clone `w1/ExecReplicate`: c1-gate 3 runs 96/96 met; N01-N04 **1 run each** (95/96, 88/96, 95/96,
95/96, named family); `compare-clone-vs-canonical.txt` `mine_runs=1 canonical_runs=3`,
OVERALL_MATCH=True. Clone `w1/ExecAutoReplicate`: c2-gate 1 run 96/96; n05 3 runs unmet
(AUTO-ERA-B); n06 3 runs unmet (AUTO-PROBE-FAIL). `w1/ExecBends`: canonical bend JSONs 1 run each
(95/96, 88/96, 95/96, 95/96, 95/96, 95/96); do-nothing-gate 94/96 8 errors
(AUTO-ERA-A, AUTO-ERA-B; AUTO-PROBE-FAIL 4/4 pass); do-nothing-battery (r92 89 roster) 89/89 met on
the landed gate. `after/c2-donothing-r92-gate.json` 94/96, failed AUTO-ERA-A,AUTO-ERA-B, 8 errors.
`w1/ExecReplicate-6` directory absent at this review (the sub-seat is running).
