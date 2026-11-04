# S1Scout binding — round 76 w1 (FINAL)

**Verdict: 4/4 snapshot digests reproduce on a second route; 8/8 draft quotes FOUND (word counts 9, 19,
7, 11, 11, 21, 6, 17 — all 4–25); JD3 and JD7 are PARTLY; S318's anchor range is PARTLY; host readings
consistent.** Not clean: JD3's arithmetic clause is false, JD7's function attribution is false, and S318
names two sections outside its own range. Details: `report.md` (full tables) and
`../S1Scout.md` (scoped hand-off); receipts `second-route-receipt.txt` and
`macro-v262-fundamental-macro.h`.

Checked (all completed, nothing left unchecked):

- second-route re-fetch of the four v262 URLs via `curl -sSL --fail` + `sha256sum` → all four MATCH
  `SOURCES.json` and `SHA256SUMS`; committed `before/src/` copies hash identically; the same four paths at
  tag v262.1 are byte-identical to v262 (host runs 262.1-1).
- eight draft quotes located whitespace-normalised in their named snapshots: all FOUND, 0 MISS, line
  numbers 86 / 283-284 / 170 / 179 / 304 / 313-315 / 25-26 / 954-955.
- entailment: HOLD for JD1, JD2, JD4, JD5, JD6, JD8; **PARTLY for JD3** (says "the smaller of free space and
  keep_free"; line 168 `avail = LESS_BY(vfs_avail, keep_free)` and v262
  `src/fundamental/macro.h:320-326` make it `max(0, free − keep_free)`); **PARTLY for JD7** ("in
  journal_config_set_defaults" — only rate-limit interval/burst are set there, sync and max-file defaults
  merge in `manager_merge_configs` at 133/142). Over-broad scope words named in the report.
- registry S318–S321: 11 columns each (12 pipes, no `|` in a cell), docs/code, tier A, mined, basenames
  named, all cited lines inside the recorded ranges, `used-by` = the note path (present, 10858 bytes).
  **S318 anchor PARTLY**: names `MaxFileSec=` (line 322) and `MaxRetentionSec=` (line 344) while the range
  stops at 320; fix is `243-320` → `243-364`. S319/S320/S321 HOLD.
- host readings: `df -B1 /` and `stat -f /` exactly consistent; boot count 3 correct; 148.6M = `du`
  allocated 155,832,320 B while `sum_bytes` 209,715,200 B is apparent size of the same 13 files
  (sparseness, largest file 25,165,824 apparent / 17,227,776 allocated); `SystemMaxFileSize` 256M/8 = 32M;
  effective limit = `CLAMP(760,100,634,624, min_use, 268,435,456)` = 256M with keep_free default =
  min(15% = 149,705,667,379 B, 4G cap) = 4,294,967,296 B. No draft row depends on host readings.

Self-correction on record: a first pass of the host arithmetic used the uncapped 15% keep_free
(149,705,667,379 B) as the reservation; the 4G cap applies to that default too, so `avail = free − 4G`.
The 256M conclusion is unchanged (max_use binds). Flagged by peer E2HostProbe, verified against S318
lines 281–285 and folded into `report.md` §4.

Residual unknowns: runtime `min_use` not observable from the pin; the 4G cap's code path
(`journal_reset_metrics`) is outside the four pinned files, so the cap is cited from S318, not code; v262
vs v262.1 compared for these four paths only.
