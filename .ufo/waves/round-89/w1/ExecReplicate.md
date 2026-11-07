# ExecReplicate — clean-room replication of C1 (Tsukuroi round 89, wave w1)

Lane measured: `665408cc45a88ed49717e22f4593e8e6152ac665` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`).

## 1. Clone fixture
- `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r89/ExecReplicate/lane` — done.
- `git -C "$S/lane" rev-parse HEAD` → `665408cc45a88ed49717e22f4593e8e6152ac665` (matches lane master).
- `git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/tsukuroi-r89/ExecReplicate/lane`. Asserted before any mutation; no mutation made.
- `sha256sum -c .ufo/waves/round-89/before/freeze-manifest.sha256` from clone cwd → **rc=0**, every line `: OK` (0 mismatches). Counter/roster/battery digests in c1 receipt match freeze: counter `c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5`, manifest `f95bdbfe1947a0ee830a011838261af6a14815c1213b476aabd9c71a478e5387` (see oracle JSON headers).

## 2. Battery selftest from unrelated cwd
Command: `cd /fast/scratch/hyaku/tsukuroi-r89/ExecReplicate && python3 "$S/lane/tools/limine-pin-battery-r89.py" --selftest` (cwd = scratch root, not the lane).
Exit: **rc=0**. Verbatim output:
```
roster-literal     PASS families_passed=50
absent             PASS families_passed=0
constant-healthy   PASS families_passed=1
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
reference-gate     PASS families_passed=50
lie-exit-code      PASS families_passed=3
lie-rc-field       PASS families_passed=3
lie-line           PASS families_passed=3
lie-consequence    PASS families_passed=41
lie-status         PASS families_passed=46
lie-verdict        PASS families_passed=44
lie-entry          PASS families_passed=3
lie-panic-line     PASS families_passed=35
lie-panic-value    PASS families_passed=34
selftest PASS 15/15
rc=0
```
Result: **PASS 15/15.**

## 3. Counting command (C1)
**Gate C1-count: REPLICATED (see §3b below for completed result).** First attempt with the spec's own `--scratch "$S/work"` (`S=/fast/scratch/hyaku/tsukuroi-r89/ExecReplicate`) fails in the counter thread with `OSError: AF_UNIX path too long` at `tools/battery-discrimination-r89.py` line 216 `sock.bind(sp)`, rc=1. This is an operability blocker on the scratch-root length, not a roster/battery failure: socket path `…/ExecReplicate/work/…` exceeds `sun_path`. Retried identically with a short scratch root `S2=/fast/scratch/hyaku/rf` (`--scratch "$S2/work"`, `--jobs 4`, cwd = clone, `--json` → `w1/ExecReplicate/c1.json`) Per-run lines and rc: §3b.

**Note for L1:** the counting command as written in C1 assumes a scratch root short enough for Unix sockets. Documenting the root-name constraint is a proposed (non-landing) defect: scratch root names should be kept short; `AF_UNIX path too long` is not an error row and voids nothing.

## 4. Freeze controls re-run through the counter (1 run each, from clone, short scratch)
Mirror of `controls-summary.txt` methodology; 1 run instead of the freeze receipts' 3.

### roster-oracle
`python3 tools/battery-discrimination-r89.py --battery .ufo/waves/round-89/before/controls/roster-oracle.py --runs 1 --jobs 4 --scratch "$S2/work-o1" --json w1/ExecReplicate/oracle-roster.json` → **rc=1**.
Verbatim stdout (truncated line noted in evidence):
```
run 1 positives 3/3 negatives 0/62 errors 0 failures N-f01-any-whitespace-blank-class,N-f03-optional-missing-skip,N-f06-empty-pin-list-cannot-evaluate,N-f07-dollar-lstrip-all,N-f08-entry-label-trailing-plus,N-f12-panic-value-raw-trailing-blanks,N-f14-cr-stripped-only-trailing,N-f16-optional-unresolved-skip,N-f18-resource-case-insensitive,N-f19-entry-label-not-trimmed,N-g00-trailing-cr-only,N-g01-loose-key,N-g02-no-paren,N-g03-format-after-resolve,N-g04-hashformat-optional-panic,N-g05-last-uri-sep,N-g06-any-empty-root,N-g07-panic-key-case,N-g08-sb-presence,N-g09-nohash,N-g10-raw-panic-scan,N-g11-first-hash-control,N-g12-any-non-yes-control,N-g13-constant-panic-control,N-g14-eacces-rc1,N-g15-no-cr-strip,N-g16-drop-global-dtb,N-h01-key-sep-equals,N-h10-empty…
verdict unmet
```
Row detail (`oracle-roster.json`, runs[0]): positives_ok 3/3, negatives_ok 0/62, error rows 0, `families_passed` distribution **{-1: 65}** — i.e. 0 hits (999) and 65 misses (-1), matching the freeze receipt's `65 misses` line. Expected shape for this control: positives 3/3, negatives 0/62, 0 errors, rc=1 (control profile, not a target hit).

### fingerprint-oracle
Identical invocation with `fingerprint-oracle.py` → `oracle-fingerprint.json`, **rc=1**, verbatim stdout identical in form: `run 1 positives 3/3 negatives 0/62 errors 0 … verdict unmet`.
Row detail: positives_ok 3/3, negatives_ok 0/62, error rows 0, `families_passed` distribution **{-1: 65}** — 0 hits, 65 misses, matching freeze `65 misses`.

### Interpretation
Both oracles see 0 hits inside the counter sandbox (`families_passed=-1` on all 65 rows) and answer the roster label only outside it (potency receipt: `oracle roster-oracle.py gates 65 correct 65 hits 65`, same for fingerprint-oracle). As freeze controls: **below target, as designed** — they demonstrate the oracles are potent outside the counter and 0-hit inside, not counter failures. Verdict on re-run: **replicated**.

## 5. Verdict (so far)
- Manifest: **PASS** (rc=0, all OK).
- Selftest: **PASS 15/15** from unrelated cwd.
- Controls re-run: **replicated** (0-hit inside, full potency outside; below target by design).
- C1 counting command: **REPLICATED** — 3/3 POSITIVE, 62/62 NEGATIVE, 0 error rows, 3 runs, `verdict met`, rc=0 (see §3b). Receipts `c1.json`, `oracle-roster.json`, `oracle-fingerprint.json` in `w1/ExecReplicate/`.
- Risk: the scratch-root-length constraint should be recorded in the wave doc (operability note above); no lane file defects found in this seat's scope.

## Snapshots
- Clone HEAD: 665408cc45a88ed49717e22f4593e8e6152ac665.
- Counter sha256: c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5.
- Manifest sha256: f95bdbfe1947a0ee830a011838261af6a14815c1213b476aabd9c71a478e5387.
- Roster sha256: 799b1fb47587432f7fb47d171e312892a3dfb439bc2980077dbfb8642f3415cc.
- Battery (oracle-roster.py) sha256: 48b0d3a1cafc2317586431b1b900fbb7a9e96a77c3f1339b99db3453346c3711; (fingerprint-oracle.py) 5eced8fe7d645d1523bf3121c1823787434ef0a58a4ec1f52210ef619a0f8339.

Report: .ufo/waves/round-89/w1/ExecReplicate.md

## 3b. Counting command — RESULT (completed after provisional write)

Job bg_3811, short scratch root `S2=/fast/scratch/hyaku/rf` (`--scratch "$S2/work"`), cwd = clone, `--json w1/ExecReplicate/c1.json`. the first attempt under the spec's own `--scratch "$S/work"` (`S=/fast/scratch/hyaku/tsukuroi-r89/ExecReplicate`) crashed before any battery ran: `OSError: AF_UNIX path too long` at `tools/battery-discrimination-r89.py:216 sock.bind(sp)`, rc=1 (verbatim, see §3). Operability blocker = scratch-root name length vs `sun_path`, not a roster/battery defect. Documented as a scratch-naming constraint, not a freeze defect.

Verbatim job output:
```
run 1 positives 3/3 negatives 62/62 errors 0 failures -
run 2 positives 3/3 negatives 62/62 errors 0 failures -
run 3 positives 3/3 negatives 62/62 errors 0 failures -
verdict met
rc=0
Wall time: 2318.76 seconds
```

Receipt detail (`w1/ExecReplicate/c1.json`): battery `/fast/scratch/hyaku/tsukuroi-r89/ExecReplicate/lane/tools/limine-pin-battery-r89.py`; counter `c666323a…`, roster `799b1fb4…`, manifest `f95bdbfe…`; `isolation: isolated`; each run: `positives_ok 3`, `negatives_ok 62`, 65 rows, **error rows 0** (`errors: []`).

**C1-count: REPLICATED** — 3/3 POSITIVE met, 62/62 NEGATIVE unmet, 0 error rows, 3 runs, `verdict met`, rc=0. Exactly the claimed target. Receipts in `w1/ExecReplicate/`; scratch clone and counter roots left in place for L1 inspection.
