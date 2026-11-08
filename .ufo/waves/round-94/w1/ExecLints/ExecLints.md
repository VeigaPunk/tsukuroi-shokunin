# ExecLints — r94 w1 executor seat (gates & selftests at freeze tip)

Freeze commit: eb3b3e5150a63507a382003fa1a70039b190396b (lane root
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin). Instruments verified by sha256:
gate 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32,
battery d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503
(both match the frozen values in the seat brief).

No tools installed/upgraded (none needed; system python3 only). TMPDIR pinned to
/fast/scratch/hyaku/tsukuroi-r94/ExecLints; scratch tree deleted on exit (see
Cleanup below). All commands run from the lane root with absolute receipt paths;
every receipt below lives in .ufo/waves/round-94/w1/ExecLints/ (<seat>.md is
this file's trailer Report: target is .ufo/waves/round-94/w1/ExecLints.md —
the two are the same content, see Cleanup for the copy step).

## 1. Gate selftest

Command: `python3 tools/check-limine-pins.py --selftest`
Receipt: 01-gate-selftest.txt. Result: `selftest PASS 39/39`, rc=0.
Full table (each line `PASS`): ok, upper, mismatch-panic, mismatch-prompt,
first-setting, secureboot, comment, missing, format, unresolved,
wallpaper-skip, non-path-key, crlf-blanks, traversal, efi-image-missing,
image-path-shadowed, linux-missing, protocol-case, bad-resource,
bad-resource-font, measured-halt, measured-no-tpm, measured-unknown-tpm,
measured-case, v1-entry-body, v1-body-invisible, v1-body-invisible-era-b,
u1-unverified, u1-pin-not-listed, era-a-first-entry, era-b-first-entry,
era-b-global-key, era-default, era-a-measured, era-b-measured,
version-parser, era-exact-first-entry, probe-version, conf-absent.
Notable: `probe-version` covers `Limine 12.9.6` ok; `12.9.6-rc1`, `12.9.6.1`,
stderr version, bare `12.9.6`, `no version here`, exit 1, absent binary all
return None (rc=-, treated as probe failure). rc=64 refusal path is in main().

## 2. Battery selftest (+ reference leg)

Command A: `python3 tools/limine-pin-battery-r94.py --selftest`
Receipt: 02-battery-selftest.txt. Result: `selftest PASS 5/5`, rc=0.
Table: reference-gate skipped (no --reference); roster-literal PASS
families_passed=98; absent PASS families_passed=0; constant-healthy PASS 0;
non-json PASS 0; constant-degraded PASS 0.

Command B: `python3 tools/limine-pin-battery-r94.py --selftest --reference
tools/check-limine-pins.py --work /fast/scratch/hyaku/tsukuroi-r94/ExecLints/battref-work`
Receipt: 02b-battery-reference.txt. Result: `selftest PASS 18/18`, rc=0
(wall 352.6 s; first attempt without --work bg'd and hit the 300 s cap at
0 bytes — rerun with its own --work dir plus a 1200 s cap completed clean).
Table: roster-literal PASS families_passed=98; absent PASS 0; constant-healthy
PASS 0; non-json PASS 0; constant-degraded PASS 0; reference-gate PASS
families_passed=98; lie-exit-code PASS families_passed=3; lie-rc-field PASS 3;
lie-line PASS 3; lie-consequence PASS 77; lie-status PASS 73; lie-verdict PASS
89; lie-entry PASS 3; lie-panic-line PASS 70; lie-panic-value PASS 70;
lie-on-panic PASS 2; lie-bad-resource PASS 87; lie-missing-panic PASS 76.
The `reference-gate` row (98/98 against the landed gate) and the 13 `lie-*`
rows are the r94 owed checks from the r93 spot-check routed 3; the 13 lie rows
pass at 2..89 families each. This run served as the delay for the session so
could not be parallelized further.

## 3. Live run, no flag (read-only against real host)

Command: `python3 tools/check-limine-pins.py --live`
Receipt: 03-live-noflag.txt. Result: rc=2, verdict CANNOT-EVALUATE.
Fields: limine_version="12.9.4", limine_version_source="probe",
visibility_era="pre-12.9.5", secure_boot_source="efivar", on_panic=null,
pins=[], unverified_image_lines=[], error="conf unreadable: [Errno 13]
Permission denied: '/boot/limine.conf'". No findings list (no `findings`
key on this path). This is the documented uid-vs-root boundary: /boot/limine.conf
is root-only for this uid, so the probe half of the default-auto path is
exercised (12.9.4 via probe) but the conf-evaluation half stops at rc 2.
The C2 flag-free live-run claim ("prints version 12.9.4 and source probe")
matches on the version/source fields.

## 4. Live run with explicit flag against a constructed fake conf

Construction (scratch $S=/fast/scratch/hyaku/tsukuroi-r94/ExecLints):
esp tree $S/esp/EFI/Linux/a.efi containing b"kernel-a"; its blake2b digest
552cee714c…bef6 (full 128-hex in the receipt JSON); fake conf $S/fake.conf:
lines `/e` and `path: boot():/EFI/Linux/a.efi#<digest>`.
Command: `python3 tools/check-limine-pins.py --conf $S/fake.conf --esp $S/esp
--live --limine-version 12.9.6` (receipt 04-live-flag1296.txt).
Result: rc=0, verdict HEALTHY, findings=[], limine_version="12.9.6",
limine_version_source="flag", visibility_era="12.9.5+", on_panic="menu",
secure_boot_source="efivar", one pin row (line 2, OK, consequence none).
The explicit flag wins over the default auto/live probe (source stays `flag`,
era flips to 12.9.5+ for the 12.9.6 pin). Contrast (not saved): the same join
without --live gives rc 0, source flag, verdict HEALTHY.

## Cleanup

No git/jj mutations, no installs, no writes outside $S and the w1/ExecLints
receipt dir. Work dirs $S/limine-battery-selftest-*/ (stale, from the timed-out
attempt), $S/battref-work, $S/esp, $S/fake.conf, $S/hash.txt removed at end.

## Verdict

Supports C2 (operability/auto-by-default): gate selftest PASS 39/39, battery
selftest PASS 5/5 and 18/18 with reference-gate 98/98, flag-free live run
probes 12.9.4 with source `probe` (rc 2 only at the root-only conf), and the
flag overrides the default to 12.9.6 with era 12.9.5+. No evidence on C1 was
produced by this seat (REFUSAL-VERSIONS-10DIGIT / AUTO-PROBE-SHAPES are battery
families, not gate-selftest commands) — the battery tables confirm the
landed-roster 98-family count but do not isolate those two families' refusal
rows.
Receipts: .ufo/waves/round-94/w1/ExecLints/{01-gate-selftest,02-battery-selftest,
02b-battery-reference,03-live-noflag,04-live-flag1296}.txt; report
.ufo/waves/round-94/w1/ExecLints.md.
