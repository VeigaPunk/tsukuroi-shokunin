# ReviewGate — code review of candidate gate, round 91

Lane revision measured: `b516d6ae13ec0bba3ef89589ac1cac86f73a9632`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`, rc 0).
Scope: `tools/check-limine-pins.py`, diff against the r90 landed gate
(`git -C ... diff 6511437e7d86d3f1e7e39a45df91ade1d8293612 master -- tools/check-limine-pins.py`,
rc 0, 127 insertions / 22 deletions). Receipts in
`.ufo/waves/round-91/w1/ReviewGate/` (diff, selftest base, 3 mutants, 2 proposed patches).

Axes: operability (read-only contract, exit/verdict honesty) + freshness (V1/U1 rule fidelity, JSON safety).

## Findings by severity

### S1 — MEDIUM: surrogateescaped values leak raw into JSON (`measured_boot.value`, `hash_mismatch_panic.value`)

- `tools/check-limine-pins.py:97-99` defines `sanitize()`, and it is applied to
  pin `uri` (`:191`), `file` (`:216`), `entry` (`:157`), and two `detail` strings,
  but NOT to the two top-level setting values built at `:246-249`:
  `{"line": ..., "value": panic_setting[1]}` / `{"line": ..., "value": measured_setting[1]}`.
  The conf is decoded with `errors="surrogateescape"` (`:126`), so a non-UTF-8
  byte survives as a lone surrogate and is emitted verbatim into stdout JSON.
- Reproduced (verbatim): conf bytes `measured_boot: \xff\xfe\n/e\nprotocol: efi\npath: boot():/f#<128 hex>\n`,
  run `python3 tools/check-limine-pins.py --conf <c> --esp <esp>` → rc 1,
  stdout contains `"measured_boot": {"line": 1, "value": "\udcff\udcfe"}`
  (raw stdout bytes show the `\udcff` escapes). `json.loads` recovers the
  surrogates as a Python string, which strict JSON (RFC 8259) consumers and many
  JSON parsers reject or corrupt. Battery r91 passes this case because it decodes
  stdout with `text=True` and compares surrogate strings in Python (battery
  `r8_ok`, `tools/limine-pin-battery-r91.py:1669-1670`), so the battery alone
  will not catch a strict-consumer failure. `hash_mismatch_panic.value` shows the
  same shape (`"value": "\udcff"`).
- Proposed patch: `.ufo/waves/round-91/w1/ReviewGate/patch-json-sanitize.diff`
  (sanitize the two `value` fields at output; prompt compare logic unaffected —
  it reads the pre-sanitize setting at `:188`).

### S2 — LOW: selftest cannot catch a bent V1, U1, or first-wins rule (25/25 PASS on all mutants)

- Evidence: three functional mutants written in a `git clone --shared` copy
  (clone rc 0, top-level verified). Each mutant changes `check()` output on its
  discriminator (proven with direct calls), yet `python3 <mutant>.py --selftest`
  returns rc 0 with `selftest PASS 25/25`:
  - `m1_whole_file.py` — V1 bent (drop `in_global` guard): on
    `timeout: 5` + entry-internal `hash_mismatch_panic: no` + mismatch, base gives
    `LP-MISMATCH panic`, mutant gives `LP-MISMATCH prompt`; measured variant flips
    `on_panic menu → halt`.
  - `m2_no_unverified.py` — U1 bent (clear list): on
    `/e / protocol: efi / path: boot():/EFI/BOOT/BOOTX64.EFI` (no `#`), base gives
    `unverified_image_lines [3]`, mutant `[]`.
  - `m3_last_wins.py` — R9 body bent (last protocol wins): on
    `protocol: efi` then `protocol: linux` + missing image, base gives
    `LP-MISSING panic`, mutant `not-modelled`.
- The 25 shipped cases (`tools/check-limine-pins.py:288-336`) cover r90 R4/R9/R10
  but contain no post-entry panic/measured, no first-line-is-entry exception,
  no unverified line, and no duplicate protocol/path case. The battery covers all
  of these; the selftest is a smoke test only. Proposed coverage patch:
  `.ufo/waves/round-91/w1/ReviewGate/patch-selftest-coverage.diff`. Full evidence:
  `.ufo/waves/round-91/w1/ReviewGate/mutants-report.txt`, baseline
  `.ufo/waves/round-91/w1/ReviewGate/selftest-base.txt` (`selftest PASS 25/25`, rc 0).

### S3 — INFO: entry-body semantics match battery R9; dead `pass` block is a readability hazard only

- Body tracking (`:133-159`, `:169-175`): `body` is created fresh per entry line,
  accumulates only the first `protocol`/`path`/`image_path` key lines, and lines
  before the first entry belong to no body (`body is None` → skipped). Protocol
  compare is exact-string against `efi/uefi/efi_chainload` (`:58`, `:175`);
  image line prefers first `path` else first `image_path` (`:175`). A probe with
  `protocol: efi` + `path: ...` before the first entry correctly ignores them
  (gate returns `LP-MISMATCH` pins only, `entry: null` for the pre-entry pin) —
  matches battery R9 (`tools/limine-pin-battery-r91.py:82-92`, `:374-395`).
- Dead block (`:148-151`): `if first_entry is not None and first_entry != 1: pass`
  does nothing; the actual flip happens at `:155-156`. Behaviour is correct
  (global = lines before the first entry, or the whole file when the first entry
  is line 1 — matches battery `global_lines`, `:265-277`), but the dead branch
  invites a future "fix" that breaks it. Suggest deleting lines 149-151.

### S4 — INFO: U1 comment overstates the empty-path case (code is correct)

- Comment at `:177-179` lists "empty path" among unverified shapes. Code is right:
  `parse_uri` (`:74-86`) treats `boot():/#<hash>` (empty path, `#` present) as a
  pin, matching R2 ("an empty path is still a pin", battery `:43-44`, `:290-316`).
  Only `boot():/` with empty tail (no `#`) is unverified. The battery's
  `want_unverified` (`:313-315`) agrees: `tail == "" or "#" not in tail` → unverified.
  Fix the comment, not the code.

## Checked and clean (no finding)

- Read-only surface: conf read `"rb"` (`:125`), ESP files read via `os.path.isfile`
  + `open(path, "rb")` (`:91`, `:217`), efivar read `"rb"` (`:260`). The only
  writes are inside `selftest()` (`:268-282`, `mkdtemp` + `shutil.rmtree :338`)
  which honours `TMPDIR` via `tempfile.mkdtemp` (no `TMPDIR` override anywhere in
  the file). Top-level `check()` has no writes.
- `--live` path (code-read only, not run): `sb` from `live_secure_boot()` or the
  flag (`:368`); `tpm` only from `--tpm-present` (`:365`), never probed from
  `/sys/class/tpm` or elsewhere — matches the "never guesses the firmware TPM"
  contract (`:28-29`). `sb=None` → `secure_boot_enforced: false` + explicit
  source string (`:369-372`). No sudo/host mutation in the path.
- Exit codes vs verdicts: `check()` maps FAULTS → DEGRADED/1, else LP-UNRESOLVED →
  CANNOT-EVALUATE/2, else HEALTHY/0 (`:238-244`); `main` returns `r["rc"]` (`:379`);
  usage errors exit 64 via `UsageParser.error` (`:346-351`), distinct from
  CANNOT-EVALUATE rc 2 (verified: `--badflag` → rc 64).
- Unreadable conf: returns `on_panic: None`, `unverified_image_lines: []`, rc 2,
  `pins: []` (`:127-130`). Battery `run_gate`/`want_on_panic`/`u1_ok` skip
  `on_panic` and `unverified` checks for missing/dir confs
  (`tools/limine-pin-battery-r91.py:1675-1676,1699`), so the contract holds.
- V1 first-entry detection: physical-line scan with `\r` removal and space/tab
  trim (`:144-147`) matches battery `global_lines` (`:269-277`), including the
  blank-line-before-entry cut case.
- ESP-escape × U1: `LP-UNRESOLVED` from `resolve_in_esp` (`:102-110`, `:210-215`)
  only arises for parseable pins, which by U1 are never in `unverified_image_lines`
  (battery `:125-126`); non-pin image lines produce no pin record, so the round-87
  hardening cannot change a verdict. No interaction defect.
- Docstring freshness: header still says "rounds 87 and 90" / "battery-r90"
  (`:2,5-7`) while V1/U1 are r91. Cosmetic; suggest updating on land.

## Residual risk and verification gaps

- Residual risk is low: the gate's V1 guard, first-wins bodies, and U1 list are
  correct against the battery's reference implementations. The two real risks are
  (a) S1 JSON strictness — invisible to the battery as written, visible to any
  non-Python consumer of stdout; (b) S2 selftest — a future "whole-file" regression
  would pass the selftest silently (the battery would still catch it, since the
  r91 battery inversions are the frozen target).
- Unrun checks (not passes): `--live` was intentionally not executed (sudo
  forbidden; code-read instead); full battery `--runs 3` was not re-run in this
  seat (reference point: base `--selftest` 25/25 rc 0 verified here). The L1
  should confirm 82/82 met in both layouts plus 3/3 `unmet` on K1/N01-N10 before
  landing, then apply (or consciously reject) the two patches.
