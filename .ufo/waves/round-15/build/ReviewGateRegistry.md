# ReviewGateRegistry — static check of SKILL registry rows (round 15)

Scope: static read-only review. No tests, builds, tool runs or verification executed. Baseline `0db618a`; SKILL.md unmodified at check time; other seats were editing `corpus/QUALITY.md` and adding `corpus/lessons/round-15.md` (not reviewed).

## Evidence: registry rows present (SKILL.md)
- `host-census` gate, L1709: `bash tools/tsukuroi-census.sh`; 0/1/2 map; `--selftest`.
- `root-dac-correction` gate, L1737: `python tools/check-root-dac-correction.py`; 0/1/2 map; `--selftest`.
- `source-scope-correction` gate, L1778: `python tools/check-source-scope-correction.py`; 0/1/2 map; `--selftest`.
- Gate standard (PROTOCOL.md L375-415) row fields: name, `gate|probe`, entry command, verdict map, self-test command/spelling, pinned-value path, write scope, owner.

## Field conformance (all three rows)
- All 8 columns present in every row; `Kind` = `gate` (valid value).
- Entry commands resolve to git-tracked files (`tools/*`); `python` -> /usr/bin/python (3.14.7) on this host.
- `--selftest` flag exists in both Python tools (argparse, `main()`); census has `--selftest` in `run_selftest`.
- Owner `tsukuroi` in all rows. Pinned-value paths name in-repo files.
- Write-scope claims: no file writes found in the two Python tools (git calls use `GIT_OPTIONAL_LOCKS=0`); census writes only under `mktemp -d /tmp/tsukuroi-r3-2-selftest.*`.

## Findings (by severity)

1. **MEDIUM, defect — exit-code misclassification in `check-root-dac-correction.py`.** Verdict map pins exit 1 = failed and says 2 = could-not-evaluate. Internal errors escape uncaught, so Python exits 1 (= "failed"):
   - `git()` (L228-230) has no `OSError` handling; missing/unexecutable `git` raises out of `main()`.
   - `main()` has no catch-all around `evaluate(docs)` (`return emit(evaluate(docs))`).
   - Valid JSON that is not an object: `json_sites` (L64-65) calls `doc.get`; `json12_issues` (L81-83) and `json13_issues` (L124-125) call `.get` / iterate on a list, raising `AttributeError`.
   - Sibling `check-source-scope-correction.py` handles all of these: `git()` maps `OSError` to `E-GIT-FAILED`, `main()` ends in `except Exception` -> CANNOT (exit 2), and has a top-level-array selftest case. The root-dac row does not match its own implementation.
   - Static reading only; not executed.
2. **LOW-MEDIUM, gap — self-test finding-ID assertion is a subset check in root-dac.** `selftest()` FAIL cases test `want - got` (missing IDs only), so extra unexpected findings pass. Source-scope uses exact set equality. Gate standard asks for a "stable expected finding-id"; subset weakens this.
3. **LOW, gap — tree-mode verdicts do not name a commit.** Root-dac emits `source=tree`; source-scope emits `revision: "worktree"`. PROTOCOL §Gate standard: "A verdict names the revision it was measured against." Recommend printing `HEAD` commit plus a dirty flag in tree mode. Applies to the C1 checker template too.
4. **LOW, classification ambiguity — `host-census` kind.** Kept as `gate`: it can fail (DEGRADED/BLOCKED) and compares against embedded baselines, which satisfies the standard's gate definition. Two issues: (a) L1709-1713 says it "does not grade mutable fleet artifacts," but the script reads live host surfaces (`pacman -Qkk`, `pacman -Qu`, `journalctl`, `systemctl --user`, `/proc/pressure`); (b) the verdict line (`TSUKUROI_CENSUS: HEALTHY|...`) names no script revision or capture time, and its selftest asserts exit code + verdict + evidence substrings (census L312-315), not stable finding IDs. Owner should either state the live-surface dependency in the row or record a lane-owned exemption. Not changed here.
5. **Probe misclassification risk (not yet present).** No probe row exists at check time; round-15 `ActiveRefs` has not edited SKILL.md. The planned C2 `tools/measure-update-recheck.py` (spec IncidentMeasure) emits exit 0 (observation completed, including `findings`/`pending_count`) and exit 2 (cannot evaluate), with no exit 1. It must be registered `probe`, with verdict map "none; exit 0 is not clean" and no self-test obligation. If it is registered as a gate, or its exit 0 is mapped to `clean`, a pending update would read as clean. The C1 checker (LocatorGate) must be `gate` with 0/1/2 and `--selftest`.

## Recommendations
- Owner (tsukuroi): align root-dac `main()`/`git()` with source-scope's exception mapping; make the root-dac self-test exact-set; print HEAD + dirty in tree mode for all three checkers.
- Owner: decide host-census classification wording (gate-with-live-surface vs probe) and state its revision/time identity.
- ActiveRefs/IncidentMeasure registration: C2 row `probe`, no verdict map, no self-test; C1 row `gate` with explicit 0/1/2 map.
- Re-run this review after the round-15 SKILL rows land (not done here).

## Sources and limits
- Files read: `SKILL.md` L1705-1785; `tools/check-root-dac-correction.py`, `tools/check-source-scope-correction.py`, `tools/tsukuroi-census.sh` (grep and targeted reads); `/home/vgpnk/Projects/shokunin/PROTOCOL.md` L375-415; `.ufo/reports/round-12/protocol.md` L116-160; `.ufo/waves/round-15/build/spec.json` (items IncidentMeasure, LocatorGate, ActiveRefs, ReviewGateRegistry).
- Limits: static reads only; no checker executed, no selftest run, no revision re-run; root-dac F1 is inferred from code paths, not observed; census behavior not executed.

## Tools
- None installed, updated or removed. Used `bash` (ls/grep/sed/git status read-only) and `python3` only to parse `spec.json`.

## Addendum — round-15 SKILL rows vs landed files (SKILL.md L1787-1835)

Re-read after ActiveRefs' IRC note. Static reads only; nothing executed.

- **C1 `locator-clarification` (gate).** Row fields complete. `tools/check-locator-clarification.py` has landed (04:53): `--revision`, `--selftest`, 0/1/2 map, tree mode emits `revision: worktree` (L656), all as the row states. Pinned constants match the row: schema `tsukuroi-locator-clarification-v1`, `R15-LOCATOR`/`R15-POSITIVE-DOMAIN`, S046 URL, and the 11-word quote (counted: 11). Also pins r14 original SHA-256s (`MD14_SHA`, `JSON14_SHA`), which the row omits; optional.
  - **Defect: selftest count is wrong in the row.** The row says `12 fixture + 2 CLI = 14`. Static count of `selftest()` cases (L549-616) is **21 fixture cases** (clean, baseline, restored-locator-json, 3 restored-locator-md variants, 3 restored-negative variants, only-values-json, extra-anchor-json15, locator-1272-json, notices-moved, notice-absent-md, notice-absent-json, notice-active-locator-number, anchor-uncovered, delete-original-md, delete-original-json, oversized-quote, malformed-json) plus 2 CLI = **23**. The tool prints `len(cases) + 2` as its total, so it will report 23 on pass, not 14. Correct the row to 21 + 2 (L1 should confirm with the single run it already owns).
  - **Not verifiable yet:** `corpus/knowledge/source-locator-clarification-r15.{md,json}` have NOT landed (absent from `corpus/knowledge`). The tool's `MD15`/`JSON15` paths therefore fail (`R15-MD-MISSING` / `R15-JSON-MISSING`) until they land. The row's "pins" for S046/quote/headings cannot be checked against landed bytes.
- **C2 `measure-update-recheck` (probe).** `tools/measure-update-recheck.py` has NOT landed; its interface (exit codes, `--revision`, no writes) cannot be verified. Classification as `probe` with no verdict map matches the recommendation in §Findings 5.
  - Landed evidence matches the row: `corpus/knowledge/partial-upgrade-recheck-r15.json` schema `tsukuroi-partial-upgrade-recheck-v1`; `snapshot_sha256` = `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`; `snapshot_captured_at` = `2026-10-20T07:44:39Z` equals `captured_at` in `.ufo/waves/round-15/build/host-snapshot.json`; `evidence_path` and `decision` = `BLOCKED_FOR_AGENT_PACKAGE_ACTION` match the row. The snapshot file has the five expected probe keys.
- **Routing.** `corpus/README.md` § Round 15 (L96-124) has the matching route. `r15_supersession` key is present in `source-scope-correction-r14.json`.
- **Unchanged from §Findings:** items 1-4 (root-dac exception mapping, subset selftest, tree-mode revision naming, host-census classification) are not addressed by the new rows. Tree mode `worktree` is disclosed in the row, so it is a residual, not a row error.

Recommendations: (a) fix the C1 selftest count to 21 fixture + 2 CLI; (b) re-review C1 and C2 interfaces after `source-locator-clarification-r15.{md,json}` and `tools/measure-update-recheck.py` land; (c) no tools installed or updated in this addendum.

## Addendum 2 — C1 row re-review against the landed pair (SKILL.md L1818)

Static reads and AST counts only; the checker was not run.

- **Selftest count: correct.** AST count of `selftest()` in `tools/check-locator-clarification.py` (current file): 2 literal cases + 15 direct `cases.append` calls, of which 2 sit in loops over 3-tuples, giving 2 + 15 + 2 + 2 = **21 fixture cases**, plus 2 CLI cases = **23**. The row matches.
- **Pinned digests: correct but mis-described.** `MD14_SHA` = sha256 of the 0db618a r14 MD after `rstrip()`; `JSON14_SHA` = sha256 of `canon()` (`sort_keys=True, separators=(",",":"), ensure_ascii=False`) of the 0db618a r14 JSON object minus `r15_supersession`. Both reproduce exactly. Raw-byte sha256 of the baseline blobs differ (MD `51e23418…`, JSON `8a162651…`). The row should say "canonical digests", not plain digests; C2 uses raw bytes, so the difference matters.
- **Row items vs landed pair:** headings at MD L7/L17/L29 (`## R15-LOCATOR`, `## R15-POSITIVE-DOMAIN`, `## QUALITY check`); openers `source:` / `verified-at:` / `recheck:` as lines 1–3; both records have exactly the seven fields; S046 + `https://man.archlinux.org/man/systemd.exec.5`; the positive quote is the exact 11-word sentence; no line number in `location` fields. All consistent.
- **Static trace of exemptions (not executed):** the withdrawn `rendered lines 1266-1267` at MD L11, JSON `corrections[0].replacement`, and the `supersedes` fields all fall under the checker's quoted+WITHDRAW or 1266-1267-only exemptions. The negative quote at MD L29 is quoted and carries "withdrawn/unsupported". I expect a clean pass; L1 must confirm.
- **Defect (content, not caught by the checker):** the R15-LOCATOR record's `quote` is a 20-word sentence, "If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit." It is not the r14 located quote. The r14 `corrections[0].quote` is the 11-word "Takes a boolean argument or the special values …". The R15-LOCATOR `replacement` says "the located quote and its proposition are unchanged", which contradicts that record's own quote field. The checker only bounds the word count (1–25) for `quote` and does not pin it, so it will not catch this. Fix: either set the LOCATOR quote to the r14 11-word sentence, or reword the replacement to say the quote is a new anchor sentence. I did not reopen S046 to check the 20-word sentence; that needs an outside reopen.
- **Row wording:** the row should note the LOCATOR quote is unpinned by the checker (only word-bounded).

Recommendation: fix the LOCATOR quote/replacement contradiction before the C1 row is treated as conformant; apply the "canonical digest" wording correction to the row.

## Addendum 3 — C2 probe row vs `tools/measure-update-recheck.py` (05:00)

Static read of the 493-line file; not executed.

Matches the row:
- Exit map: `emit()` returns 0 for `PASS`/`ABSENT`, 2 for `CANNOT_EVALUATE`; `main()` returns 0 only for `--help`; no path returns 1. No `--selftest` flag.
- `--revision` validated by `REV` (`HEAD` or 4–64 hex), `E-REVISION-INVALID` otherwise; git reads use `GIT_OPTIONAL_LOCKS=0`.
- `REQUIRED_KEYS` = schema, source_ids, observed_at, evidence_path, snapshot_sha256, observations, decision, limits.
- `REQUIRED_SOURCES` = S047, S048, S049; landed JSON `source_ids` = `["S047","S048","S049"]`. `S049` exists in `corpus/SOURCES.md:55`.
- `evidence_path` must equal `.ufo/waves/round-15/build/host-snapshot.json` exactly (L290).
- `PROBE_KEYS` = the five snapshot keys; the landed JSON `observed_at` and `snapshot_captured_at` both = `2026-10-20T07:44:39Z`.
- Snapshot digest is `sha256(raw bytes)` compared with the record's declared `snapshot_sha256` (L291–295).
- Imports are stdlib; `subprocess` is used only by the read-only git helper.

Mismatches / risks:
1. **Status word "PASS" (L404, L488).** The row says the 0-exit "is neither clean nor a health verdict", but the payload emits `"status": "PASS"` for `record_count` 1. A reader or dashboard may treat that as a clean verdict. Recommend renaming the status to a non-verdict token (e.g. `OBSERVED` / `ABSENT`) in the tool, or documenting in the row that the status string is not a verdict.
2. **Row claims a pinned digest the tool does not hold.** The row lists "raw snapshot SHA256 `b101f374…ea81`" under *Pinned values*, but the tool contains no such constant (grep: 0 hits). The value lives only in the record and is checked against the raw bytes. Row should say "digest held in the C2 JSON, checked against raw bytes; no constant in the tool".
3. **Duplicate URL.** S048 and S049 both cite `https://man.archlinux.org/man/pacman.8`; the census W04 scope-duplicate warning will fire (warning only, exit 0). Expected, not a failure.

Recommendation: fix items 1 and 2 (tool rename or row wording) before the C2 row is treated as conformant. No selftest is needed for the probe per the Gate standard, but the row should state the probe does not establish host truth.
