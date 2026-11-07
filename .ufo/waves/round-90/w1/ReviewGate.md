# ReviewGate — round 90, wave w1 (reviewer seat)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Revision measured: `git rev-parse master` = **ce89df93e5f576c5c236d4547299e9ea954e8853** (candidate),
freeze base 6511437e7d86d3f1e7e39a45df91ade1d8293612.
Candidate under review: `tools/check-limine-pins.py`
sha256 `4780da83ba411db1dc6afc250b618edc336a42790d79578018b40a2d7593a332` (+95/−20 vs freeze).
Read-only. No lane file touched, nothing staged or committed; all fixtures under
`/fast/scratch/hyaku/tsukuroi-r90/ReviewGate/` (removed on exit). Receipts: `w1/ReviewGate/receipts.txt`.

## Verdict per assigned check

| # | check | verdict |
|---|-------|---------|
| 1 | read-only; writes only inside `--selftest`'s mkdtemp, TMPDIR honoured | **PASS** |
| 2 | `--live` never guesses the TPM (code read, not run) | **PASS** |
| 3 | exit codes vs verdicts (0/1/2/64) | **PASS** |
| 4 | `on_panic` for an unreadable conf | **PASS** (null; R10 exempts it) + F3 shape defect |
| 5 | JSON safety of every new field | **PASS** on the wire + N1 caveat |
| 6 | entry-body logic vs R9 | **PASS** + F2 label defect, N2 spec drift |
| 7 | r87 ESP-escape LP-UNRESOLVED vs the new rules | **PASS** |
| 8 | selftest 25 cases fail on a bent rule | **4/5 mutants caught** + F4 blind spot |

Independent instruments, my own scratch: `selftest PASS 25/25` (exit 0);
`families_passed 73/73 verdict met failed -` (exit 0, one run of
`limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 1`). The clone is byte-identical to
the lane gate (same sha256), so the mutant work below is against the candidate bytes.

## Findings

### F1 — MEDIUM (false green; needs an L1 rule decision, not a bare gate patch)
`tools/check-limine-pins.py:157-158`, `:188-193`.

An efi chainload entry whose image line is **not a pin** — the common unhashed shape
`path: boot():/EFI/Linux/x.efi`, no `#hash` — is reported **HEALTHY rc 0 with an empty pin list** even
when the file is absent (measured: `{"verdict": "HEALTHY", "rc": 0, "pins": []}`, and the same with
`--secure-boot-enforced 1`). Cause: R2 makes a hashless value not a pin, and R6/R9 key the panic on *a
pin on the image line*, so nothing looks at that line at all. Limine v12.9.4 does not care whether the
operator hashed the path: `chainload.c 414-435` resolves `PATH` (else `IMAGE_PATH`) and calls
`panic(true, "efi: Failed to open image with path `%s`. Is the path correct?")` when `uri_open`
returns NULL.

This is **compliant with the frozen rules** (R2/R6/R9 as the battery states them, and adding a pin
would change the 73-family pin lists), so it is a rule-set hole surfaced by the gate, not a
rule violation. Cheapest honest surface, battery-safe by the GATE OUTPUT CONTRACT ("Other extra keys
are allowed and ignored"): a top-level `unverified_image_lines` naming image lines that carry no pin.
Patch: `w1/ReviewGate/patch-F1-unverified-image-lines.diff` (applies clean, keeps 25/25 and 73/73 met;
verified output `HEALTHY 0 [3]` for the probe conf). The docstring Output line needs the new key if it
lands. If L1 prefers a status instead, that is a new frozen rule (R11) and a new battery family, which
is out of this wave's scope.

### F2 — LOW (R8 contract, real code defect)
`tools/check-limine-pins.py:139`: `entry = sanitize(... .strip()) or entry`.

Two divergences from R8 ("label = the line without its leading '/' characters, then without a leading
'+', then trimmed of spaces/tabs at both ends"):

1. A line that is just `/` has label `""`; the `or entry` fallback then reports the **previous**
   entry's label. Measured: conf `/alpha`, pin, `/`, pin → both pins report `"entry": "alpha"`;
   R8 wants `"alpha"`, `""`.
2. `.strip()` (no argument) trims `\v` and `\f`, which R8 keeps. Measured: entry line `/a\x0b` reports
   `"a"`; R8 wants `"a\x0b"`.

Patch `w1/ReviewGate/patch-F2-entry-label.diff` (one line: assignment instead of `or entry`, and
`.strip(" \t")`). Verified: `entries ['alpha', '']`, `vt entry 'a\x0b'`, selftest 25/25, battery 73/73
met. Pre-existing from r87 (`or entry` and `.strip()` are unchanged by this candidate) but on a field
the battery asserts (R8 family ENTRY-LABEL / ENTRY-LABEL-EDGES) — no fixture draws an empty or
`\v`-terminated label, which is why 73/73 does not see it.

### F3 — LOW (output contract, rc=2 path)
`tools/check-limine-pins.py:128-129`.

The unreadable-conf object is a different schema from every other result: no `schema`, `findings`,
`hash_mismatch_panic`, `measured_boot`, `tpm_present`, `secure_boot_enforced`. Measured object:
`{"error": ..., "on_panic": null, "pins": [], "rc": 2, "verdict": "CANNOT-EVALUATE"}`. A consumer that
reads `findings` raises KeyError exactly on the path that reports a broken conf — the worst place to
lose the key set. `on_panic: null` itself is right here: R10 exempts an unreadable conf and measured
boot is unknown, not absent, so it must not be derived from `secure_boot`.

Patch `w1/ReviewGate/patch-F3-unreadable-shape.diff` (full key set, `findings: []`, `on_panic` stays
null). Verified: same rc/verdict, all keys present, selftest 25/25, battery 73/73 met (the battery
skips R8/R10 for CONF-UNREADABLE, and `hash_mismatch_panic: null` is the same value a readable conf
with no such key carries). Pre-existing from r87.

## Residual risk / notes (no patch)

- **N1 — non-UTF-8 conf bytes in the two setting echoes.** `:217-220` emit `hash_mismatch_panic.value`
  and the new `measured_boot.value` **unsanitized**, while `pins[].uri`/`detail`/`entry`/`file` go
  through `sanitize()` (`:97`, used at `:162`, `:173`, `:187`). Measured with raw `0xff` in the
  value: the gate survives (`json.dumps` defaults to `ensure_ascii=True`, so stdout is pure ASCII) and
  emits `"value": "ye\udcffs"`, but a consumer that re-encodes hits
  `UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff'`. I recommend **keeping the raw
  R1 value** — R8 defines `hash_mismatch_panic.value` as "its R1 value", and sanitising to `?` would
  make a future non-UTF-8 fixture unfaithful — and documenting the lone-surrogate caveat instead. The
  two fields should at least be treated the same way, which they are today.
- **N2 — entry-line definition is looser than config.c.** The gate (and frozen R8/R9) treat a line
  whose first non-blank character is `/` as an entry line; `config.c 686-720` accepts `/` only at
  column 0 or after `\n`, and the body extends to the next such `/`. So an indented `  /Entry` starts a
  new body here and does not in Limine. The battery's own ENTRY-LABEL-EDGES fixtures indent entry
  lines, i.e. the instrument depends on the looser reading — **not patchable in the gate**; record it
  against the "follows Limine v12.9.4" phrasing of C1.
- **N3 — `--live` mixed override.** `:336-337`: `--live --conf X` without `--esp` hashes `X`'s pins
  against `/boot`. `--esp` and `--conf` default independently. Consider refusing `--live` with
  `--conf` but no `--esp` (the battery never runs `--live`, so this is free); design call for L1.
- **N4 — a valid-but-unresolvable *optional* pin forces rc 2.** `wallpaper:`/`term_font:` on
  `guid(...)`/`uuid(...)` yields LP-UNRESOLVED → CANNOT-EVALUATE, although Limine would only skip the
  wallpaper. Frozen R7 has no optional exemption; do not change it this round, but it is why a
  decorative wallpaper can mask a HEALTHY verdict.
- **N5 — the escape guard is local hardening, not Limine.** A `..`/symlink pin on an efi image line
  reports LP-UNRESOLVED/not-modelled → rc 2 (`:188` reached only after `resolve_in_esp` returns a
  target, `:102-110`), i.e. a would-be `Failed to open image` panic is reported as CANNOT-EVALUATE.
  That matches frozen R6/R7 and is the honest answer for a path the gate refuses to follow; the
  interaction with the new R9 rule is correct (no accidental DEGRADED, no false panic).

## Mutants — do the 25 selftest cases fail on a bent rule?

Each replacement was asserted unique before writing, applied to the clone copy, then `--selftest`:

| mutant | bents | selftest | battery |
|---|---|---|---|
| m1 | R4 block disabled (`if False:`) | **FAIL 23/25** (bad-resource, bad-resource-font become LP-UNRESOLVED rc 2) | — |
| m2 | R9 panic disabled | **FAIL 23/25** (efi-image-missing, measured-halt) | — |
| m3 | R10 ignores `--tpm-present` (always `halt-if-tpm`) | **FAIL 23/25** (measured-halt, measured-no-tpm) | — |
| m4 | image-line precedence swapped (`image_path` before `path`) | **FAIL 24/25** (image-path-shadowed) | — |
| m5 | R4 one-`$` drop removed | **PASS 25/25** ← blind spot | unmet 69/73 (DOUBLE-DOLLAR, GZ-RAW, ROOT-ON-BOOT, VALID-RESOURCES) |

**F4 — LOW:** the selftest has no positive `$boot()` (gzip-marker) case, so it cannot fail on the
`$`-drop rule; only the frozen battery catches it. If the selftest is meant to be a standalone
smoke test, add e.g. `case("gz-marker", ["/e", "path: $boot():/EFI/Linux/a.efi#" + ha], False, 0, [(2, "OK", "none")])`
(validated against the candidate: `$boot()` → `HEALTHY 0 [(2, 'OK', 'none')]`, so the case is
correct and fails only if the `$` drop breaks).
The authority for C1 stays the battery; the selftest is a convenience, and the four r90 clauses
(R4 block, R9 panic, R10 tpm, R9 precedence) are all covered.

## What I verified as correct (evidence in receipts.txt)

- **Read-only:** every write-capable call is inside `selftest()` under one `tempfile.mkdtemp`
  (`:238`, `:242`, `:244`, `:251`, `:308`); `check()`/`blake2b_file()`/`resolve_in_esp()` only open
  `"rb"`. With `TMPDIR` set to a fresh directory, `tempfile.gettempdir()` reports it, the selftest runs
  there, the working directory listing is byte-identical before/after, and zero `limine-pins-selftest-*`
  directories survive.
- **`--live` and the TPM (code read, not executed):** the only `/sys` open is the SecureBoot efivar
  (`:55`, `:230`); there is no `/sys/class/tpm` or `/proc` read anywhere. `tpm` comes only from
  `--tpm-present` (`:335`), so `--live` reports `halt-if-tpm` when measured boot is requested — it
  never guesses. `secure_boot_source` honesty: `efivar` / `argument` /
  `"efivar unreadable; treated as not enforced"`.
- **Exit codes = verdicts:** HEALTHY 0, DEGRADED 1 (LP-BAD-RESOURCE now in FAULTS, `:56`, so a bad
  resource alone gives 1 — checked), CANNOT-EVALUATE 2, usage 64 via `UsageParser` (checked: missing
  `--esp` → 64; `--tpm-present 2` → 64; unreadable conf → 2 with empty pins); `main()` returns `r["rc"]`.
  Faults outrank unresolved (a fault + an escape gives DEGRADED 1).
- **R9 entry-body logic:** pre-entry `protocol:`/`path:` lines belong to no entry (entry `null`,
  not-modelled); first `path` wins over a later `image_path` (m4 proves the precedence is load-bearing);
  `protocol` compared case-sensitively against `efi/uefi/efi_chainload` (`EFI` → not efi, per menu.c
  2429-2468 strcmp); an image line naming a directory is LP-MISSING + panic (R5+R9); image lines in
  non-efi entries stay not-modelled; `body` records only the first occurrence of each key
  (config_get_value index 0).
- **R10:** first `measured_boot` key line anywhere in the file wins (including inside an entry body —
  measured `halt` with `--tpm-present 1`), value compared with `==` ("Yes" → menu), Secure Boot forces
  requested (`:115-116`), `--tpm-present 0` → menu, absent → `halt-if-tpm`; `on_panic_of` is a pure
  function of (first setting, secure boot, tpm) and matches menu.c 1712-1724 + panic.s2.c 24-28,70-78,98
  (`measured_boot` clears `allow_menu`).
- **R4:** one `$` dropped then exact membership in the seven names (`$$boot`→`$boot`, `$Boot`, `bootx`,
  empty name all LP-BAD-RESOURCE; optional keys skip; else panic), resource validity checked *after*
  hash format and *before* the root test — matches uri.c 339-366 and R3/R4 ordering.

## Refused / not run

- `--live` was **not executed** (sudo forbidden; reads `/boot/limine.conf`), and no `/boot`, `/efi`,
  `/etc`, `/usr`, `/var`, `/sys` or `/proc` path was opened for writing. No host fact was needed beyond
  the committed receipt, so none is requested.
- Did not run the frozen battery `--runs 3` (C1's counting command, owned by the counter seats); my
  single run is an independent datapoint, not a re-measurement of C1. Did not judge, integrate or ship
  anything; no lane file, MANIFEST, SCORECARD, LOG or `considerthese/` write.
