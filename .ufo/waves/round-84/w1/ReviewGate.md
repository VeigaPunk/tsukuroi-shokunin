# ReviewGate — round 84 w1 — review of the C2 gate and capture script (read-only)

Lane revision measured: `git rev-parse master` = `f19e73f3aa9817e76044e4e43a343c6ca6d929df`
(pre-round tip 64f45b79; C1 re-declaration 69915b86; candidate c6ee78b2). `tools/check-hibernate-resume.py` has one
commit in history (c6ee78b2) and is byte-identical since. Lane worktree: `git status` shows only the L1's own
uncommitted wave files; no lane file was edited by this seat.

Instrument sha256 (`sha256sum`, receipt `w1/ReviewGate/live-and-hashes.txt`):

| file | sha256 | vs freeze |
|---|---|---|
| tools/count-resume-rows-r84.py | cb70d435…8309 | matches declaration |
| tools/resume-gate-battery-r84.py | 00310ac2…0964 | matches declaration |
| tools/capture-resume-facts-r84.py | cec27b9d…6cea23 | matches declaration |
| tools/check-hibernate-resume.py | 3d2e1cf5…4556 | not pinned by the declaration (gate sha is not in the freeze table) |

## Measured results

1. Battery, the counting command (`python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py`, run from lane root), rc=0.
   `families_passed: 13`, `families_total: 13`, `verdict: met`, `failed_families: []`, bases `host, random0..random4`, 0 failing cases.
   Output file: `w1/ReviewGate/battery-out.json`; stderr `battery-err.txt` (empty).
2. Live gate, `python3 tools/check-hibernate-resume.py --live`, rc=0, stdout:
   `{"findings": [], "verdict": "HEALTHY"}`. Host facts agree internally: cmdline `resume_offset=3795013`,
   `btrfs map-swapfile -r` = 3795013, `/sys/power/resume_offset` = 3795013, `/sys/power/resume` = `253:0` = `stat -L /dev/mapper/root`,
   `lsattr` has `C`, free swap 31722876−11942400 KiB ≈ 20.5 GB > image_size 12835467264, state contains `disk`, HOOKS has `resume` after `encrypt`.
   The fail-open findings below do not fire on this host because every probe succeeded; they fire when a probe fails.
3. Malformed-input matrix (`w1/ReviewGate/malformed-matrix.txt`, 58 cases, 0 violations): every case prints exactly one JSON line; no traceback on
   `{}`, `[]`, `null`, empty file, non-JSON, truncated JSON, non-UTF-8, directory path, nonexistent path, wrong types for every
   key (bool-as-int, str-as-int, list-vs-str, element types), missing key for every required key. All return rc2 `CANNOT-EVALUATE`, findings `[]`.
4. Precedence probes: rule 1 short-circuit (no `resume=`) → exactly `[HR-NO-RESUME-ARG]`, rc1; duplicated `resume_offset=` →
   last occurrence used (kernel behaviour assumed, not verified here [INFERENCE]); findings are sorted; file-only rules skip on
   partition-swap facts; HR-NO-DISK-STATE fires on empty `sys_power_state`.

## Findings (severity, file:line, evidence, proposed patch)

Line numbers are for the lane at f19e73f3.

### F1 — High (operability) — `--live` reports HEALTHY rc0 when capture probes fail (fail-open)
- `tools/capture-resume-facts-r84.py:57` `rec()` only logs `rc`; no probe failure is recorded. `:119` `return 0` unconditionally.
  The `sudo -n` probes at `:73`, `:76`, `:79` and the `stat -L` (`:85` area), `/sys` reads and HOOKS bash (`:95` area) all feed sentinels (`None`, `-1`, `""`) into facts.json, and the gate at `check-hibernate-resume.py:138-139` only checks capture's rc, which is always 0.
- Evidence: scratch copy of the lane tools with `"sudo"` replaced by a missing binary (`w1/ReviewGate/failpath-probes.txt`):
  `L1 --live with sudo missing  rc=0 out={"findings": [], "verdict": "HEALTHY"}`; `L2 capture rc with sudo missing rc=0`;
  `L2 facts: map_swapfile_offset None, swapfile_attrs None, resume_swapfile '/swap/swapfile'`.
- Proposed patch (capture; keeps the frozen rule set; the gate's existing `p.returncode != 0` branch then yields rc2 CANNOT-EVALUATE):
  ```diff
  --- a/tools/capture-resume-facts-r84.py
  +++ b/tools/capture-resume-facts-r84.py
  @@
  -    def rec(label, rc, out, err):
  +    failed = []
  +    def rec(label, rc, out, err, required=False):
  +        if required and rc != 0:
  +            failed.append(label)
   ...
  -        rec(f"sudo -n btrfs inspect-internal map-swapfile -r {swapfile}", rc, out, err)
  +        rec(f"sudo -n btrfs inspect-internal map-swapfile -r {swapfile}", rc, out, err, required=True)
  ...  (same `required=True` on: `sudo -n lsattr`, `stat -c '%W %i %s'`, `stat -L -c '%t %T'`,
  ...   `cat /sys/power/resume`, `resume_offset`, `state`, `disk`, `image_size`, the HOOKS bash line)
  @@
  +    if failed:
  +        print(json.dumps({"capture_failed": failed}), file=sys.stderr)
  +        return 3
       return 0
  ```
  (`filefrag -v` stays non-required: the gate never reads it.) Gate side unchanged, because `check-hibernate-resume.py:139-140` already returns CANNOT-EVALUATE on a nonzero capture rc.

### F2 — Medium (operability; frozen-rule text) — `--facts` path is fail-open on sentinel or None values
- `check-hibernate-resume.py:93-96` rule 2: `elif f["map_swapfile_offset"] is not None and o != ...` — with `map_swapfile_offset: null` and a resume_swapfile set, no finding fires. Frozen text says the same ("o, map_swapfile_offset set, differ"), so this is a rule-text defect, not an implementation deviation.
- `:97-98` COW check skipped when `swapfile_attrs` is None (frozen text: "swapfile_attrs set, no 'C'").
- `:115` rule 7 `free < f["image_size"]` with capture's sentinel `image_size: -1` never fires; `:113` skipped when swaps empty.
- `:85-119` rule 3 skipped when `resume_dev_majmin: null` (stat failed).
- Evidence (`failpath-probes.txt`): F1 map=None with wrong offset → HEALTHY; F2 attrs=None → HEALTHY; F3 image_size=-1 → HEALTHY; F5 majmin=None → HEALTHY.
- Not patched here: fixing this changes the frozen rule set and needs a re-declaration (L1 decision). Option A (re-declare): treat a
  required-but-null probe or any negative `image_size`/`sys_power_resume_offset` sentinel as `Malformed` → rc2. Option B: accept and document
  that the gate reads only what the capture reports, with F1's capture fix closing the live path. F1's patch alone does not close `--facts`.
  Proposed Option A diff for `validate()` (for the L1 to take or not):
  ```diff
  +    if f["image_size"] < 0 or f["sys_power_resume_offset"] < 0:
  +        raise Malformed("unreadable-sentinel")
  ```
  plus rc2 when `resume_swapfile` is set and `map_swapfile_offset`/`swapfile_attrs` is None.

### F3 — Medium (contract) — uncaught RecursionError on deeply nested JSON: traceback, rc1
- `check-hibernate-resume.py:145` `except (OSError, ValueError)` does not cover `RecursionError`.
- Evidence (`w1/ReviewGate/deep-json.txt`): 100 000 `[` → `RecursionError: Stack overflow ... while decoding a JSON array`, `rc=1`. Lead requirement is rc2, never a traceback.
- Proposed patch:
  ```diff
  -        except (OSError, ValueError) as e:
  +        except (OSError, ValueError, RecursionError) as e:
  ```

### F4 — Medium (operability) — `--live` hang: uncaught `subprocess.TimeoutExpired`, traceback, rc1
- `check-hibernate-resume.py:138` `subprocess.run(..., timeout=120)` has no `except subprocess.TimeoutExpired`; the `finally` still removes the temp dir, so only the report contract is broken.
- Evidence (`w1/ReviewGate/hang-timeout.txt`, scratch copy whose capture sleeps forever): `HANG_RC=1`, `subprocess.TimeoutExpired: ... timed out after 120 seconds`.
- Proposed patch:
  ```diff
  -            p = subprocess.run([sys.executable, CAPTURE, "--out", tmp], capture_output=True, text=True, timeout=120)
  +            try:
  +                p = subprocess.run([sys.executable, CAPTURE, "--out", tmp], capture_output=True, text=True, timeout=120)
  +            except subprocess.TimeoutExpired:
  +                return emit("CANNOT-EVALUATE", [], 2, error="capture-timeout")
  ```

### F5 — Low (contract) — usage errors: rc2 with empty stdout, violating "stdout is exactly one JSON object"
- `check-hibernate-resume.py:128-132` argparse prints usage to stderr and exits 2; stdout empty (`noargs.out` empty; `NOARGS_RC=2`).
- Proposed patch: subclass the parser so `error()` emits JSON:
  ```diff
  -    ap = argparse.ArgumentParser()
  +    class _P(argparse.ArgumentParser):
  +        def error(self, message):
  +            emit("CANNOT-EVALUATE", [], 2, error="usage")
  +            raise SystemExit(2)
  +    ap = _P()
  ```

### F6 — Low (ambiguity in frozen text; untested) — validation runs before the rule-1 short-circuit
- `check-hibernate-resume.py:86` `cmdline = validate(f)` runs before `:87` `arg(cmdline,"resume") is None`. A document with no `resume=` and a wrong-typed field returns rc2 CANNOT-EVALUATE, not DEGRADED `[HR-NO-RESUME-ARG]`. Evidence: `F9 no resume= + image_size bad type rc=2`.
- Frozen rule 1 says "exactly [HR-NO-RESUME-ARG]; nothing else is evaluated"; the schema rule says "wrong type → rc2". The two lines conflict for this input, and the battery's MALFORMED family never builds a no-resume document, so the battery cannot tell. L1 decides which line governs; the gate matches the schema reading.

### F7 — Low (rule text; untested) — empty `resume=` counts as present
- `check-hibernate-resume.py:87` `arg()` returns `""`, not None, for `resume=`. Evidence `F7 resume= empty value rc=0 HEALTHY`. The kernel's behaviour for an empty `resume=` is not verified here [INFERENCE: the hibernate resume device is then unset, so HR-NO-RESUME-ARG is the likelier intent].
- Proposed patch: `if not arg(cmdline, "resume"):` (one line; behaviour change only for the empty-value case).

### F8 — Low (battery coverage gap; gate follows the frozen text more broadly)
- `resume-gate-battery-r84.py` FILE_ONLY includes `HR-SYSFS-OFFSET-MISMATCH`; the frozen rule 4 does not restrict it to file-type swaps, and the gate applies it whenever `resume_offset=` is set. Evidence F8: partition swap with `resume_offset=` set and sysfs differing → fires `HR-SYSFS-OFFSET-MISMATCH` (and HR-SWAP-TOO-SMALL from my synthetic size). The battery never builds this case, so the broader behaviour is unmeasured.
- Also `HR-NO-ACTIVE-SWAP` is applied unconditionally (`:113`-area) while the docstring nests it under rule 2's file-type condition. Battery and gate agree; the docstring is ambiguous.
- Not a gate defect; for the L1's next declaration.

### F9 — Low (residual scope) — rule 6 checks only the literal `encrypt`
- `check-hibernate-resume.py:111` ignores `sd-encrypt`, which the battery's own systemd-hook generator emits (`battery` `random_base`, hooks list). A systemd-initramfs HOOKS with `resume` before `sd-encrypt` is not flagged. Frozen text says `encrypt`, so this is a residual, not a freeze violation. Flag for a future round.

### F10 — Low (safety, documentation) — capture sources `/etc/mkinitcpio.conf` and `conf.d` in a child bash
- `capture-resume-facts-r84.py:43-47` `HOOKS_SH` runs `source /etc/mkinitcpio.conf` and sources each `/etc/mkinitcpio.conf.d/*.conf`. Sourcing executes arbitrary shell as the invoking user. Mitigation present: the child bash gets `env=ENV` (`:29`), so no BASH_ENV/HOME leakage, and `bash -c` reads no rc file. Host ownership (read-only `stat`): `/etc/mkinitcpio.conf` `root:root 644`, `/etc/mkinitcpio.conf.d` `root:root 755`. Risk is low on this host; the docstring's "read-only" claim does not cover sourced code.
- Proposed patch (no shell execution; parse the last `HOOKS=(...)` assignment in the same file order with `shlex`):
  Not written here: the file list order and multi-line arrays need a design call. L1 decides whether it is worth a patch.

### F11 — Low (robustness, unrealistic input) — unguarded `int()` on kernel-produced text
- `capture-resume-facts-r84.py:~93` `int(ma, 16)` / `int(mi, 16)` and `:~60` `int(f[2])`, `int(f[3])` on /proc/swaps lines: a ValueError would traceback. Kernel output makes this unlikely. Not reproduced. Patch: wrap in `try/except ValueError` → treat as capture failure (see F1).

### Clean (checked, no defect)
- Rules 1–8 implemented as the frozen text states, with the exceptions above (F2 rule 2/7; F6 rule 1 ordering; F9 rule 6 literal).
- Exit codes 0/1/2 match HEALTHY/DEGRADED/CANNOT-EVALUATE; findings sorted; stdout one JSON line on all `--facts` paths probed (malformed matrix).
- Non-UTF-8, directory path, missing file, empty file, truncated JSON, wrong-type and missing-key inputs: rc2, no traceback.
- Capture subprocess inventory: every argv is a list (no `shell=True`); the only `bash -c` is the constant HOOKS string; `sudo -n` appears exactly three times (`map-swapfile -r`, `lsattr`, `filefrag -v`); the other probes are `cat`, `stat`, `systemctl --version`. All are read-only. No write to /sys, /proc, /boot, swap state.
- Environment: capture scrubs children to `PATH`, `LC_ALL`, `LANG` (`:24`, `:29`). Gate's own `--live` subprocess inherits the full environment before capture scrubs its children (info only).
- No `/tmp` hardcoding: capture writes only into `--out`; gate uses `tempfile.mkdtemp` (honours TMPDIR) and removes it in `finally`.

## Verification gaps (named)
- Kernel semantics for duplicate and empty `resume=` / `resume_offset=` are not verified here (F7 is [INFERENCE]).
- The `sudo -n` probes were not exercised with sudo denied on the real host (read-only rule); the failure was simulated in a scratch copy with the binary replaced (F1).
- The hung-capture case was simulated in a scratch copy (F4), not on the host.
- Battery and gate were run once each; no lane file was edited.

## Receipts (under `.ufo/waves/round-84/w1/ReviewGate/`)
- `battery-out.json`, `battery-err.txt` — battery run, rc0, 13/13.
- `live-and-hashes.txt` — `--live` output rc0 and the instrument sha256 table.
- `malformed-matrix.txt` + `malformed_matrix.py` — 58-case matrix (0 violations).
- `failpath-probes.txt` + `failpath_probe.py` — F1–F11 probe outputs.
- `hang-timeout.txt`, `deep-json.txt` — F3, F4 evidence.

Scratch root `/fast/scratch/hyaku/tsukuroi-r84/ReviewGate` removed after receipts were copied. No package install; no pacman; no host write; no git mutation.
