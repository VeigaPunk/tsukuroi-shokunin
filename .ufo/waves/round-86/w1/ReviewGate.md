# ReviewGate — round 86 code review of the candidate gate

Seat: ReviewGate (reviewer, leaf). Lane master measured: `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`.
Reviewed: `git diff 2f67de80 dc884949 -- tools/check-hibernate-resume.py` (175 lines, receipt `ReviewGate/candidate.diff`).
Lane tip gate sha256 `8123d033c0ccf8e3c6bdbdd1f1bb392125d661084731a324794501239ea3f024` (identical to candidate; no lane edit).

## Verdict

- **Changed functions: correct.** No defect found in `matches` (:105), `availability` (:111), `arg` (:137), `resume_offset` (:146), `gate` (:158), `selftest` (:241), `main` (:271).
- **--selftest: real assertions, can fail.** It asserts rc and sorted finding IDs per case (13 cases). Two mutants fail it (below).
- **Docstring: states the implemented rules**, with one wording nit (finding F1).
- **Battery (C1 counting command): 30/30 met in one run at the lane tip.** Not three consecutive runs; the other two are not run by this seat.

## Checks run (verbatim exit codes)

1. `python3 tools/check-hibernate-resume.py --selftest` → rc=0, `{"cases": 13, "failed": [], "selftest": "PASS"}`; receipt `ReviewGate/selftest-tip.txt`.
2. `python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py --out …/battery-run1.json` → rc=0, `families_passed 30 / families_total 30, target 30, verdict met, failed_families [], cases 231, bases host+random0..4`. Receipt `ReviewGate/battery-run1.json`. This is run 1 of the three the declaration requires.
3. Freeze manifest, run from `round-86/before/` (my first attempt ran from the wrong cwd and reported 44 unreadable files; that was my error, not a drift): `sha256sum -c freeze-manifest.sha256` → all 45 lines `OK`, rc=0. So battery bytes equal the freeze (void rule not triggered).
4. Mutation tests on scratch copies (lane untouched; copies in `ReviewGate/`):
   - **mutA** — `matches` replaced by plain `tok.startswith(setup)` (drops `-`→`_`): `--selftest` → rc=1, `{"case": "offset-dash-digit-prefix", "findings": ["HR-OFFSET-MISSING"], "pass": false, "want": [], "want_rc": 0}`, `{"cases": 13, "failed": ["offset-dash-digit-prefix"], "selftest": "FAIL"}`. Diff `mutA.diff`.
   - **mutB** — `positive` case want_rc 0→1: `--selftest` → rc=1, `{"case": "positive", "rc": 0, "want_rc": 1, "pass": false}`, `failed ["positive"]`. Diff `mutB.diff`.
   Both fail as intended, so the rc assertion and the finding assertion are live.
5. Literal C ports vs the Python helpers (in-process differential, 1,600,000 `matches` cases over 8 setup strings, plus `resume_offset` oracle and 50,000 `arg` cases): `match_mismatch 0`, `offset_mismatch 0`, `arg_mismatch 0`. Ports: `parameqn` (kernel/params.c 86-95, `-`→`_` on both sides), `sscanf "%llu"` leading-digit rule (lib/vsprintf.c 3644-3673).
6. Kernel call path: `repair_env_string` restores `=` before `obsolete_checksetup` (init/main.c:462-463, called at :486 and :518, `obsolete_checksetup(param)` at :527). So the handler sees the full token, as the gate models.
7. Setup strings (hibernate.c:1518-1524): `noresume`, `nohibernate` (no `=`); `resume=`, `resume_offset=`, `hibernate=` (with `=`); these match the gate's `matches(...)` calls.
8. Host `CONFIG_PM_STD_PARTITION=""` and `CONFIG_HIBERNATION=y` (`zcat /proc/config.gz`, rc=0). `resume_file[256] = CONFIG_PM_STD_PARTITION` (hibernate.c:46) is empty here, so "absent `resume=` → no device" matches this host. Not a defect on this host; the gate would be wrong on a kernel with a non-empty default (see F3).
9. Kernel-truth probes on the tip gate (fact files built from the r85 host base; outputs recorded in the transcript, P1 facts in `ReviewGate/probe-P1.json`):
   - `hibernate=nocompress` → HEALTHY rc0 (correct, nocompress exempt)
   - `hibernate=no` → HR-HIBERNATE-DISABLED rc1 (correct)
   - `nohibernate=1 noresume` → HR-HIBERNATE-DISABLED only (correct, A3 suppressed by A1)
   - `resume-offset=4096` → HEALTHY (correct, `-`/`_`)
   - `resume_offset=+4096` → HR-OFFSET-MISSING (correct: sscanf rejects `+`, o None)
   - `resume_offset=0x10` → HR-OFFSET-MISMATCH + HR-SYSFS-OFFSET-MISMATCH (correct: sscanf reads `0`)
   - `RESUME=/dev/...` → HR-NO-RESUME-ARG (correct: case-sensitive)
   - `noresume=0` → HR-NORESUME-ARG + HR-NO-RESUME-ARG (correct: `resume=` absent in that fact file)
   - `hibernate=noresumex` → HR-NORESUME-ARG (correct)
   - `no-resume no-hibernate resume-offset-x=…` decoys → HEALTHY (correct)
10. Token-order probe (frozen limit, not a defect): `noresume resume=/dev/mapper/root resume_offset=999` and the reverse order both → `DEGRADED rc1 [HR-NORESUME-ARG, HR-OFFSET-MISMATCH, HR-SYSFS-OFFSET-MISMATCH]`. The gate ignores order, as the declaration states. Receipt `ReviewGate/order-probe.txt`.

## Per-function review (candidate diff)

- `matches` (:105-108): correct. Equals parameqn on the first `len(setup)` chars with `-`/`_` mapping; short tokens return False, as the kernel does. Verified by 1.6M differential cases.
- `availability` (:111-134): correct. Branch order (`nohibernate`, `noresume`, `hibernate=` → `noresume` / `nocompress` / `no`) mirrors `hibernate_setup`'s strncmp order (hibernate.c). `noresume_setup`/`nohibernate_setup` ignore their argument, as modelled.
- `arg` (:137-143): correct for its use (`resume=`, last match wins; empty treated as absent by `gate`).
- `resume_offset` (:146-155): correct. Digit prefix of the rest; rest with no leading digit is skipped and the earlier value kept. Verified against sscanf port.
- `gate` (:158-188): correct for the frozen rules. `if not arg(cmdline, "resume=")` covers both absent and empty (`resume_file` stays "" → -ENOENT, hibernate.c:982-985). Rule 2-8 are unchanged in content.
- `selftest` (:241-268): correct and fails when expected. Note it does not check that stdout is a dict (see F4).
- `main` (:271-306): `--selftest` dispatch added before any file read; no behaviour change for `--facts`/`--live`.

## Findings

- **F1 (docstring nit, low, not a defect):** the Token-parse paragraph says "the last `resume=` / `resume_offset=` wins". For `resume_offset=`, the code keeps the last *digit-led* value (`resume_offset(cmdline)`), as the next clause states. Proposed patch (NOT applied; lane file untouched), receipt `ReviewGate/proposed-docstring-patch.txt`:
  `- the last \`resume=\` / \`resume_offset=\` wins` → `+ the last \`resume=\` wins; the last digit-led \`resume_offset=\` wins`
- **F2 (limit, frozen, documented):** token order is not modelled (probe 10). Verdict is DEGRADED either way, so no verdict defect; the offset findings may be spurious when `noresume` precedes `resume_offset=`. Declared in the frozen docstring; no change proposed.
- **F3 (residual, not in host scope, unrun on other kernels):** absent `resume=` is treated as "no device" unconditionally; kernels with non-empty `CONFIG_PM_STD_PARTITION` resume from that device instead. Host config is empty (check 8), so no false result here. [INFERENCE] for other kernels; C2 row, not a C1 rule.
- **F4 (test hygiene, low):** `selftest` does `json.loads(p.stdout).get("findings")`; a non-dict stdout would raise AttributeError instead of failing cleanly. The gate always emits a dict, so no current failure. Also no fixture for `hibernate=nocompress` or for empty-then-valid `resume=`; the battery covers those.
- **F5 (integer width, [INFERENCE], unrun):** `resume_offset` uses unbounded Python `int`; kernel `%llu` (simple_strntoull) would wrap on >2^64 values. Both yield a mismatch against any realistic offset, so no verdict change expected. Not exercised.

## Residual risk and gaps

- Battery run count: 1 of 3 required runs (this seat). Runs 2-3 are not claimed.
- Live path (`--live`) not run (read-only capture not needed for this review).
- Lane tip not re-committed; no lane file edited.

## Receipts (`.ufo/waves/round-86/w1/ReviewGate/`)

`candidate.diff`, `diff-stat.txt`, `battery-run1.json`, `selftest-tip.txt`, `selftest-mutA-matches-prefix.txt`, `selftest-mutB-positive-rc1.txt`, `mutA.diff`, `mutB.diff`, `gate-mutA.py`, `gate-mutB.py`, `sha256.txt`, `probe-P1.json`, `order-probe.txt`, `proposed-docstring-patch.txt`.

Scratch `/fast/scratch/hyaku/tsukuroi-r86/ReviewGate/` removed. Free space on /fast/scratch at check: 399G.
