# ExecDoNothing — round 95 / w1 — C1's do-nothing legs

Seat: ExecDoNothing (executor). Lane: tsukuroi-shokunin. Round 95, wave w1.
Lane root for every command below: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Ran: 2026-11-08T06:55–06:58-03:00. Host: linux 7.2.11-arch1-1 x64; `python3` 3.14.8;
`bwrap` `/usr/bin/bwrap`; scratch `/fast/scratch/hyaku/tsukuroi-r95/ExecDoNothing` (deleted at
the end of the seat). No package was installed or upgraded (no tool/version/channel change to
record). No mutating `git`/`jj` command was run; no file outside this seat's dir was written.

Axis moved: depth — the blindness leg of C1 (the r94 roster must not see the r95 bend) and the
instrument-identity leg of C1's void rule.

## Step 1 — the do-nothing pairs are byte-identical to the landed instruments

Command:

```
sha256sum tools/limine-pin-battery-r94.py .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py \
          tools/check-limine-pins.py .ufo/waves/round-95/before/controls/do-nothing-gate-r94.py
```

Raw output:

```
d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503  tools/limine-pin-battery-r94.py
d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503  .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  .ufo/waves/round-95/before/controls/do-nothing-gate-r94.py
```

The four hashes, against `.ufo/waves/round-95/before/instruments.sha256`:

| file | sha256 | manifest |
|---|---|---|
| `tools/limine-pin-battery-r94.py` | `d66b4a59…bb503` | `d66b4a59…bb503` ✔ |
| `before/controls/do-nothing-battery-r94.py` | `d66b4a59…bb503` | same line ✔ |
| `tools/check-limine-pins.py` | `7d79ac29…d32` | `7d79ac29…d32` ✔ |
| `before/controls/do-nothing-gate-r94.py` | `7d79ac29…d32` | same line ✔ |

**PASS**: each control is byte-identical to its landed instrument, and both land on the frozen
manifest lines. Re-measured after the two battery runs (`sha256sum -c
.ufo/waves/round-95/before/instruments.sha256` → 9 × `OK`, exit 0), so no run moved an instrument.

Side observation (no severity): `N05-strict-8.py` differs from the landed gate in exactly one
logical line, `len(p) <= 9` → `len(p) <= 8  # N05 (bound bent to <=8)` at line 99 of the landed
gate; `diff` exit 1, one changed line, no other hunk.

## Step 2 — the r94 battery on the N05 bend (the blindness leg)

Command:

```
python3 .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py \
        --gate .ufo/waves/round-95/before/controls/bends/N05-strict-8.py \
        --runs 3 --work /fast/scratch/hyaku/tsukuroi-r95/ExecDoNothing/work-n05 \
        --json .ufo/waves/round-95/w1/ExecDoNothing/dn-n05.json
```

Raw output (three lines, `EXIT=0`; wall 1m16s):

```
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
```

Re-parse of `dn-n05.json` (script in this seat's transcript; `json.load`, `case_log` walked):

```
1 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 any_9digitsubstr 0
2 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 any_9digitsubstr 0
3 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 any_9digitsubstr 0
gate_field: .../.ufo/waves/round-95/before/controls/bends/N05-strict-8.py
schema: tsukuroi-limine-pin-battery-r94-v1
distinct_families 98, per-family count 4 in all 98 families, 392/392 rows passed (each run)
REFUSAL-VERSIONS rows: 4/4 passed (each run)
```

`count-runs.py … --family REFUSAL-VERSIONS-9DIGIT` on the same file → `verdict met`, `error_rows
0`, `named {}` (the named family has **no** rows), exit 0.

Expected (claims.json C1 target, as narrowed by plan A1): `met` 98/98 in each of 3 runs, 0 error
rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows. **PASS** on every clause. The r94 battery cannot see the
`<= 8` bend: all 98 of its families pass on the bent gate.

## Step 3 — the r94 battery on the landed gate (the unchanged-gate leg)

Command:

```
python3 .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py \
        --gate tools/check-limine-pins.py \
        --runs 3 --work /fast/scratch/hyaku/tsukuroi-r95/ExecDoNothing/work-gate \
        --json .ufo/waves/round-95/w1/ExecDoNothing/dn-gate.json
```

Raw output (`EXIT=0`; wall 1m44s):

```
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
families_passed 98/98 verdict met failed -
```

Re-parse of `dn-gate.json`:

```
1 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 distinct_families 98 per_family!=4 {}
2 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 distinct_families 98 per_family!=4 {}
3 verdict met passed 98 / 98 failed [] cases 392 case_log 392 error_rows 0 9digit_rows 0 distinct_families 98 per_family!=4 {}
gate_field: .../tsukuroi-shokunin/tools/check-limine-pins.py
```

`count-runs.py … --family REFUSAL-VERSIONS-9DIGIT` → `met`, `error_rows 0`, `named {}`, exit 0.

Expected (A1): `met` 98/98 ×3, 0 error rows, 0 `REFUSAL-VERSIONS-9DIGIT` rows. **PASS** on every
clause.

## Step 4 — the two rosters, read from source (no battery executed)

Method: `ast.parse` each file, take the `FAMILY_ROSTER` tuple literal and the `FAMILIES` dict's
keys; no module import, no battery run.

```
r95  tools/limine-pin-battery-r95.py                                roster_len 99  unique 99  FAMILIES map 99
     roster_has_9digit true   families_map_has_9digit true   roster vs map diff []
r94  .ufo/waves/round-95/before/controls/do-nothing-battery-r94.py  roster_len 98  unique 98  FAMILIES map 98
     roster_has_9digit false  families_map_has_9digit false  roster vs map diff []
```

**PASS**: 99 distinct family names in the r95 roster with `REFUSAL-VERSIONS-9DIGIT` present (and
present in the dispatch table, so the literal-roster usage check at `main()` cannot reject it);
98 distinct family names in the r94 roster with the name absent from both the roster and the
dispatch table. Both rosters equal their own `FAMILIES` key sets (no orphan name on either side).

Supporting source reads (static, no execution):

- The r94 run-roster version enumeration is `REFUSAL_VERSIONS = ("12.9", "12.9.5.1", "abc", "",
  " 12.9.5", "12.9.5 ", "+12.9.5", "12..5", "12.9.5-rc1", "9"*5000 + ".0.0")` — ten out-of-range or
  five-thousand-digit values and no in-bound 9-digit component.
- The r94 file declares `REFUSAL_DIGIT9 = "9"*9 + ".9.9"` once and references it nowhere (grep
  count 1, the declaration line 1684) — the declared-and-unused constant the r94 spot-check routed
  (item 8). The r95 battery references it twice (`fam_refusal_versions_9digit` uses it at line
  1715), i.e. the constant is now live.
- The only `999999999` in the r94 battery is `("999999999.0.0", 0)` inside `usage_check()` (line
  2278), a separate CLI mode that `--gate … --runs` never reaches.

## Supplementary (outside the claim's counting command): where the blindness actually lives

`usage_check()` is not a roster family, so the reading above does not touch it — but it is the
honest limit of "the r94 battery is blind". Measured, both ~1.3 s:

```
python3 .../do-nothing-battery-r94.py --gate .../bends/N05-strict-8.py --usage-check --work <scratch>/work-n05-usage
  → verdict unmet, 15 rows, failing = [('999999999.0.0', want_rc 0, rc 64, ok False)]
python3 .../do-nothing-battery-r94.py --gate tools/check-limine-pins.py --usage-check --work <scratch>/work-gate-usage
  → verdict met, 15 rows, failing = []; 999999999.0.0 → rc 0
```

So the r94 instrument *does* carry one in-bound 9-digit probe, in a non-family mode that the
claim's counting command does not execute; the `<= 8` bend fails exactly that row. Read strictly
as the claim words it (the run battery, `--runs 3`), blindness holds and this seat's Step 2 is the
proof; the sharper statement is that the r94 *family roster* has no in-bound 9-digit case, which is
what let `M13`/`N05` survive it. This is the expected result of plan A1's mechanism account, not a
deviation from any frozen line — recorded so a later reader does not over-read "blind".

## Expected-line ledger

| # | expected | measured | verdict |
|---|---|---|---|
| 1a | r94 battery == do-nothing-battery-r94 | `d66b4a59…` both | PASS |
| 1b | gate == do-nothing-gate-r94 | `7d79ac29…` both | PASS |
| 1c | both pairs on the freeze manifest | `sha256sum -c` 9 OK, exit 0 | PASS |
| 2a | r94 × N05: met 98/98 ×3 | met 98/98 ×3 | PASS |
| 2b | r94 × N05: 0 error rows | 0/0/0 | PASS |
| 2c | r94 × N05: 0 `REFUSAL-VERSIONS-9DIGIT` rows in `case_log` | 0/0/0 (substring count too) | PASS |
| 3a | r94 × landed gate: met 98/98 ×3 | met 98/98 ×3 | PASS |
| 3b | r94 × landed gate: 0 error rows | 0/0/0 | PASS |
| 3c | r94 × landed gate: 0 `REFUSAL-VERSIONS-9DIGIT` rows | 0/0/0 | PASS |
| 4a | r95 roster 99 names | 99, unique 99 | PASS |
| 4b | r95 roster has `REFUSAL-VERSIONS-9DIGIT` | present in roster and dispatch table | PASS |
| 4c | r94 roster 98 names | 98, unique 98 | PASS |
| 4d | r94 roster lacks `REFUSAL-VERSIONS-9DIGIT` | absent from both | PASS |

Deviations: none. The one qualifier is the supplementary `--usage-check` reading above, which is
not a frozen expected line and is reported rather than scored.

## Receipts (paths relative to the lane root)

| receipt | sha256 | size |
|---|---|---|
| `.ufo/waves/round-95/w1/ExecDoNothing/dn-n05.json` | `9c8cfd89969946547c9332b251064237f0c7332ea0305618398b74bc56b7c151` | 690906 B |
| `.ufo/waves/round-95/w1/ExecDoNothing/dn-gate.json` | `4b165aa965ff4cd387a239eba9b18125640b634e4d36abc6e6c5725a9f544986` | 690588 B |
| `.ufo/waves/round-95/w1/ExecDoNothing/dn-n05-usagecheck.json` | `b39a8cebed0cd8c0b878fe5301d0973a5282cb68162e44d1f180933eb1ca97fc` | 6376 B |
| `.ufo/waves/round-95/w1/ExecDoNothing/dn-gate-usagecheck.json` | `f3b580f267a29a29301beed6ffc9bf7858c1a0f25aaf1e24e5d299c1cd47d3d2` | 6341 B |
| `.ufo/waves/round-95/w1/ExecDoNothing/dn-n05-usagecheck.err` / `dn-gate-usagecheck.err` | `e3b0c442…b855` (empty) | 0 B |

Every number above comes from one of these files or from a command printed in this report.
Scratch `/fast/scratch/hyaku/tsukuroi-r95/ExecDoNothing` was removed after the runs (the battery
cleans its own `tempfile.mkdtemp` case dirs; the two work roots were `rm -rf`'d).

## Risks / blockers

- None blocking. The r94 battery's `--usage-check` leg is not blind to N05 (see Supplementary);
  the claim does not use that mode, and the r95 family moves the in-bound 9-digit case into the
  run roster where it does bite. Flagged for the reviewer/critic rather than fixed here (I may not
  edit instruments).
- `pool`/host dependence unchanged: the `AUTO-*` families read the sandbox's real `/usr/bin/limine`
  (`12.9.4`), as the r94 docstring states; host bootloader drift would move those families, not
  these.

{"seat":"ExecDoNothing","verdict":"met","notes":"both do-nothing pairs byte-identical to the landed instruments and on the freeze manifest (d66b4a59 battery, 7d79ac29 gate); r94 battery x N05 reads met 98/98 x3 with 0 error rows and 0 REFUSAL-VERSIONS-9DIGIT rows (blindness holds for the run battery); r94 x landed gate met 98/98 x3, 0 error rows, 0 nine-digit rows; r95 roster 99 unique names incl REFUSAL-VERSIONS-9DIGIT, r94 roster 98 without it; supplementary --usage-check mode is not blind to N05 (999999999.0.0 want 0 got 64) and is outside the claim's counting command"}
