# RevMarkerO12 — C1 marker O12 review at 10d5288fc1051364e711203855e7c53710dfcc21

Verdict: holds. The O12 marker on row SH5 of `corpus/knowledge/storage-health-r26.json` quotes its
anchor, names the right row/field/verdict, and both basis references resolve and support the `now`
text.

## The marker

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.json:329`:

```json
{"id": "R29-OWED-O12", "row": "SH5", "field": "statement", "withdrawn_text": "FAILED! otherwise",
 "verdict": "qualified",
 "now": "The overall-health line is printed only after a successful SMART log read: with no -H, a failed Identify Controller or a failed log read, smartctl prints no overall-health line at all, so a non-zero Critical Warning byte yields the failure verdict only when that read succeeded.",
 "basis": ["corpus/knowledge/storage-health-r26.md:129",
           "S134 (smartmontools 7.5 nvmeprint.cpp lines 772-778, 786-788, 833-836: no overall-health line without -H or after a failed log read)"]}
```

## (a) Original statement unchanged — confirmed

- Frozen anchor `FAILED! otherwise` (counter ITEMS, `tools/check-owed-statements-r29.py:82-83`) is a
  verbatim substring of the SH5 `statement` field, still present at
  `corpus/knowledge/storage-health-r26.json:229` at the tip: "it prints PASSED when the controller's
  Critical Warning byte is zero and FAILED! otherwise".
- `python3 tools/check-owed-statements-r29.py --revision 10d5288fc1051364e711203855e7c53710dfcc21`
  (run read-only, GIT_* unset) reports O12 `ok: true`, `verdict: qualified`, summary `marked: 12`,
  exit 0 — i.e. M1's field-hash check against `BASE_DIGEST['O12'] =
  33c4b6d0327dba973ecb0041794bd6d8181c3176ab60fad75cdf8f42401a7664` passes, so the statement is
  byte-identical to the claim base `16e9ab2a`. [obs]

## (b) Verdict choice — `qualified` is correct

- The original sentence ("PASSED when the Critical Warning byte is zero and FAILED! otherwise") is
  not wrong about the derivation — S134.cpp:450-451 is exactly
  `(!w ? "PASSED" : "FAILED!")` — it is wrong only by implying the line always appears. The marker
  keeps the derivation and restricts its scope. `qualified` (not `corrected` or `rebutted`) matches
  that shape. The md's own wording at line 129 agrees: "'FAILED! otherwise' ... hold only after a
  successful SMART log read".

## (c) Basis references resolve and support `now`

- `corpus/knowledge/storage-health-r26.md:129` exists and is the SH5 wording bullet recording the
  same qualification (verified with `awk 'NR==129'`); it is a reviewer-note line, not a marker line.
- `S134` registry row (`corpus/SOURCES.md:140`): status cell `mined`; used-by cell lists
  `corpus/knowledge/storage-health-r26.md, corpus/knowledge/storage-health-r26.json` — the target
  file is one comma-separated entry. Snapshot `.ufo/waves/round-26/sources/S134.cpp` hashes
  `4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98`, matching the row's declared
  sha256 for the RELEASE_7_5 nvmeprint.cpp bytes.
- Cited lines map one-to-one onto the `now` conditions in `nvmePrintMain`:
  - lines 772-778: if none of the print options is set, smartctl prints only
    "NVMe device successfully opened" + the hint and `return 0` — no overall-health line;
  - lines 786-788: a failed `nvme_read_id_ctrl` prints an error and `return FAILID` — early exit
    before any health line;
  - lines 833-836: a failed `nvme_read_smart_log` prints an error and `return FAILSMART`;
  - lines 839-840: only then, under `if (options.smart_check_status)`, does
    `print_critical_warning(smart_log.critical_warning)` run, and lines 450-451 print
    `FAILED!` exactly when `w` (the Critical Warning byte) is non-zero.
  - So: a non-zero Critical Warning byte reaches the `FAILED!` verdict only when the SMART log read
    succeeded and the check-status option was requested — exactly what `now` says. [obs]
- `now` contains no numbers to recompute (word floor: 49 words / 36 distinct after anchor removal,
  anchor text not present in `now`).

## Findings

1. No defect. Marker O12 satisfies M1-M6 mechanically (counter run above) and semantically: basis
   references resolve and the cited S134 lines substantiate every clause of `now`.

## Observations / residual risk

2. [obs] Minor wording imprecision, not a defect: "`with no -H` ... prints no overall-health line at
   all" uses `-H` as shorthand for "no check-status request". smartmontools' `-a`/`-x` enable the
   same `smart_check_status` path, so `smartctl -a` prints the line without a literal `-H`
   [inf — the option-parsing file is not in the committed snapshot; only S134.cpp is]. The row's own
   flag vocabulary (`sudo smartctl -H -A`, action cell) makes the intended reading unambiguous.
3. [unk] Whether `-a`/`-x` imply `-H` is not covered by the S134 snapshot (option parsing lives in
   smartctl.cpp); the `now` claim does not depend on it — with `-A` alone the SMART log is read but
   `print_critical_warning` is never called, so no overall-health line prints, consistent with `now`.

Scope: read=SCORECARD.md declaration, tools/check-owed-statements-r29.py (ITEMS, rules), corpus/knowledge/storage-health-r26.json (SH5 row, marker), corpus/knowledge/storage-health-r26.md:129, corpus/SOURCES.md S134 row, .ufo/waves/round-26/sources/S134.cpp lines 440-485/770-840; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO12.md; executed=check-owed-statements-r29.py --revision 10d5288f... (exit 0, marked 12), awk/grep/sha256sum reads
Model: not exposed
Installs: none
