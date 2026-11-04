# R1Reviewer — scoped findings (round-74 w1, tsukuroi, hyaku run 15)

Full report: `.ufo/waves/round-74/w1/R1Reviewer/report.md`. Receipts in the same dir: `rowcheck-receipt.txt`, `rows-final-receipt.txt`, `fx_probe-receipt.txt`, `selftest-counter.txt` (harness: `rowcheck.py`, fixture proof: `fx_probe.py`).

## Headline verdict

**All six proposed UF rows (SC1Entry draft bytes) PASS** every frozen mechanical clause and are **entailed** by the pinned v262 snapshots: word counts 12–20 (≥12), token sharing 7–12 distinct tokens at ratios 0.54–1.00 (≥6, ≥0.5), row digests equal `SOURCES.json` and actual snapshot bytes, quotes verbatim at unit-file.c:416/:73, unit-file.h:25-32/:8-14, load-fragment.c:6250-6251/:6291, ids contiguous, reuse 2 per snapshot, 3 sources / 3 snapshots. Frozen counter over the exact draft bytes: `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0 met=1` rc 0 (independent fixture reproduction).

## Findings by severity

1. **HIGH (F1, C1/UF3)** — the frozen C1 claim (SCORECARD.md:6092 committed bytes) misstates v262: `unit_type_may_alias` is {service, socket, target, device, **timer, path**}, not "...device, and volume units". A row parroting the declaration would be unentailed. The landed UF3 correctly states the true set and the negative volume claim; the round record needs an erratum naming the declaration misstatement.
2. **HIGH (F2, attack/evidence chain)** — the declared base `d749a625f483c66f2a6f2005db3799630c776bc3` is not a git object (`cat-file -t` rc 128); real base is `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (parent of the declaration). Proven vacuous-pass hazard: C1 counter with the bogus hash prints the exact true-base control line (`UF_MAP absent` rc 128); C2 checker prints the exact expected `ROUTED_STALE=2 ROUTED_OK=0/2` rc 1 — both for the wrong reason (missing object). Wrong hash is in committed bytes at SCORECARD.md:6050 and in all 12 seat prompts (w1-dispatch.json / w1-spec.json).
3. **MEDIUM (F3, mechanical)** — the frozen token gate is vocabulary-strict (`UNIT_SERVICE` → `unit_service` ≠ prose "service"); canary runs show 3 of 6 committed clause wordings (UF2/UF3/UF4) would fail it as written (ratios 0.33/0.20/0.12). Verified PASSing statement shapes for all six rows were supplied and are what landed.
4. **MEDIUM (F4, authoring traps — both PROVEN against the frozen counter)** — quotes containing C `\"` break `ROW_RE` → malformed row → `met=0` (probe T1); multi-line block comments require their ` * ` continuation markers or the quote is "not located" (probe T2). Quote bounds 4–25 words; snapshot reuse cap 2; registry S309-S311 need URL in Title cell and basename in Location cell (counter parses parts[2]/parts[6]).
5. **LOW (F5)** — `--selftest` requires a non-`/tmp` `TMPDIR` (frozen hermetic guard; rc 2 otherwise); with a seat `TMPDIR`: `SELFTEST: PASS (13 cases)`.

## Open items for the integrator

- Registry rows S309-S311 were still absent from `corpus/SOURCES.md` at review close — the frozen counter over the real repo cannot return `met=1` until they land in the F4 cell layout; then run `python3 tools/count-uf-rows-r74.py` (working tree) and cite the revision.
- Cite base controls as `d749a625` / `d749a625b3054b7cb3435983fb9626ab3d0ed0c4`, never the corrupted declared full hash.
- Snapshot integrity double-checked: pinned bytes == `SOURCES.json` == `SHA256SUMS` == S1Scout's second-route re-fetches (all three sha256 equal).
