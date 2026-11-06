# ReviewGate — round 85 w1 — candidate diff review (hibernate gate v2 + capture lockdown key)

- Lane revision measured: `git rev-parse master` → `479d868b2fc8969a19a617cd55ced5c13edd84b6` (freeze `66374a4db963e5c655506e64cb0fea2d67ec9d0d`).
- Diff reviewed: `git diff 66374a4 479d868` → 2 files, `tools/check-hibernate-resume.py` (+64/−11 header comment lines net new code: availability(), lockdown validation, rule-1 change) and `tools/capture-resume-facts-r84.py` (+14/−2: `lockdown` key).
- Byte identity: `git show 66374a4:tools/resume-gate-battery-r85.py | sha256sum` → `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21` (== frozen instrument digest); `git show 479d868:tools/check-hibernate-resume.py | sha256sum` → `88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7` == working tree; `git status --porcelain tools/` empty. No lane file edited by this seat.

## Verdicts

| # | Check | Verdict |
|---|---|---|
| 1 | Gate implements exactly the frozen rule text (A1–A3, rules 1–8, rule-1 change), nothing more | **OK** (2 carried-over benign normalisations, both r84-adjudicated, unreachable from the instrument — see N1, N2) |
| 2 | Availability rules match pinned kernel snapshots | **OK with 4 Limits findings** L1–L4 (docstring↔kernel divergences, no gate defect; rule text is frozen) |
| 3 | `--live` path (absent lockdown, unreadable lockdown, writes, sudo) | **OK** |
| 4 | Malformed `lockdown` handling | **OK** |
| 5 | No regression for resume-facts consumers | **OK** (r84 instrument supersession is documented, not silent) |

No DEFECT found → no patch files; evidence in `.ufo/waves/round-85/w1/ReviewGate/` (drv.py, stub-capture.py, fixture-runs.txt, r84-vs-v2.json).

## (1) Gate vs frozen rule text — OK

Mapping (battery docstring `tools/resume-gate-battery-r85.py:14-42` ↔ gate `tools/check-hibernate-resume.py`):

- A1 `check-hibernate-resume.py:103,107-113` ↔ docstring A1: exact `nohibernate` token, or `hibernate=V` with prefix tests in kernel order `noresume` → `nocompress` → `no`. ✓
- A2 `:85-88,:93-96,:120` ↔ docstring A2: non-null lockdown, exactly one `[x]` word, blocked iff word ∈ (integrity, confidentiality). ✓
- A3 `:105,:109,:116-118` ↔ docstring A3: exact `noresume` token or `hibernate=noresume*`, suppressed iff A1 fired (`elif noresume`). ✓
- Rule 1 change `:135-137`: availability always evaluated first; `resume=` absent adds `HR-NO-RESUME-ARG` and skips only rules 2–8. ✓ (r84 gate returned `["HR-NO-RESUME-ARG"]` alone.)
- Rules 2–8 `:139-172` identical to r84 frozen text incl. the global "swaps empty → HR-NO-ACTIVE-SWAP" reading adjudicated in r84 (`.ufo/waves/round-84/w1/ExecBatteryC2.md:151-154`). ✓
- Malformed → rc2 with `findings []` via `:214-218`. HEALTHY rc0 / DEGRADED rc1 sorted dup-free via `sorted(set)`. ✓

Measured, counting command at lane tip (cwd `tsukuroi-shokunin`, TMPDIR in scratch), three consecutive runs:

```
$ python3 tools/resume-gate-battery-r85.py --gate tools/check-hibernate-resume.py
run1 rc=0 {"bases": ["host", "random0", ..., "random4"], "cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "order_head": ["HR-OFFSET-MISSING", "HR-NORESUME-ARG", "HR-NO-ACTIVE-SWAP", "POSITIVE", "HR-OFFSET-MISMATCH"], "verdict": "met"}
run2 rc=0 families_passed 20/20 verdict met  order_head ["HR-SWAP-TOO-SMALL", "HR-NO-RESUME-HOOK", "HR-SYSFS-OFFSET-MISMATCH", "PREC-NO-RESUME-ARG", "HR-SWAP-TOO-SMALL"]
run3 rc=0 families_passed 20/20 verdict met  order_head ["HR-HIBERNATE-DISABLED", "PREC-NO-RESUME-ARG", "PREC-NO-RESUME-ARG", "HR-SWAP-TOO-SMALL", "HR-NO-RESUME-ARG"]
```

Order head differs per run (OS-entropy shuffle), bases re-randomised per run — no position counter or case-order replay can pass; K5 replay control 0/20 and K6 substring sniffer 14-15/20 in the committed freeze receipts (`.ufo/waves/round-85/before/controls/controls-receipt.txt`, re-read this session: K0 0/20, K1 0/20, K3a-c 0/20, K3d/e 13/20, K4 2/20 — matches the declaration table).

Hand fixtures (26 cases on the committed host base, driver `ReviewGate/drv.py`, full transcript `ReviewGate/fixture-runs.txt`): T1-T8, T12-T15, T17-T20 all return exactly the frozen-text prediction, e.g.:

```
T2  +nohibernate +noresume              rc=1 {"findings": ["HR-HIBERNATE-DISABLED"], "verdict": "DEGRADED"}
T7  +hibernate=nofoobar                 rc=1 {"findings": ["HR-HIBERNATE-DISABLED"], "verdict": "DEGRADED"}
T17 no-resume + noresume                rc=1 {"findings": ["HR-NO-RESUME-ARG", "HR-NORESUME-ARG"], "verdict": "DEGRADED"}
T18 dup resume_offset (stale first)     rc=0 {"findings": [], "verdict": "HEALTHY"}   # docstring pins last occurrence
T20 lockdown[integrity]+noresume+no resume= rc=1 {"findings": ["HR-LOCKDOWN-BLOCKS", "HR-NO-RESUME-ARG", "HR-NORESUME-ARG"], "verdict": "DEGRADED"}
```

Nothing-more audit — two code points outside the literal rule text, both adjudicated in r84 and unreachable from the instrument (battery cannot emit either shape):

- **N1** `:152` compares `f["sys_power_resume"].strip()` where r85 docstring rule 3 says `!= sys_power_resume` with no normalisation. Benign: capture strips every /sys read (`capture-resume-facts-r84.py:86,91`); r84 clean-room differential adjudicated this exact divergence "gap, both readings defensible, unreachable from the instrument" (`.ufo/waves/round-84/w1/ExecCleanRoomGate/diffs.json`). Carry forward, not a C2 defect.
- **N2** `:139-142` raises `Malformed("resume_offset-not-int")` → rc2 for a non-integer `resume_offset=` value; docstring defines `o` as "the value of the last resume_offset= token" and is silent on non-integers. r84 adjudicated the candidate's rc2 reading "candidate right" under the wrong-type clause. Not a C2 defect.

## (2) Availability rules vs pinned kernel snapshots — OK, Limits L1–L4

Pinned: `.ufo/waves/round-85/before/src/kernel_power_hibernate.c` (sha `ae3dbeb6…f86c1`), `include_linux_security.h` (`263740c9…cfefc`), `security_lockdown_lockdown.c` (`fec032ce…4e00a`).

- **A1** `hibernate_setup` raw 1424-1439: `noresume` prefix tested first, then `nocompress`, then `no` — gate `:107-113` tests in the same order; `nohibernate_setup` raw 1447-1452; `__setup` table raw 1518-1524. ✓
- **A2** `LOCKDOWN_HIBERNATION` is enum index 5, `LOCKDOWN_INTEGRITY_MAX` 21, `LOCKDOWN_CONFIDENTIALITY_MAX` 30 (`include_linux_security.h` raw 128-158); `lockdown_is_locked_down` blocks when `kernel_locked_down >= what` (`security_lockdown_lockdown.c` raw 59-73) → `integrity` and `confidentiality` both block hibernation, `none` does not; `lockdown_param` raw 40-52 accepts only those two names; `lockdown_read` raw 96-117 prints exactly one bracketed level — the only three possible bracketed words are what the gate parses. Gate `:93-96,:120` exact. ✓
- **A3** `noresume_setup` raw 1440-1444; `hibernate=noresume*` matched before the `no` branch (raw 1425-1428); `nohibernate` sets noresume too (raw 1432-1435, 1448-1450) → A3 suppression under A1 is faithful; `software_resume_initcall` bails on `noresume || !hibernation_available()` (raw 1106-1111) so HR-NORESUME-ARG correctly marks the resume chain moot. ✓

**L1 (kernel `__setup` matching is broader than the frozen token text)** — Pinned facts: `__setup("noresume", noresume_setup)` / `__setup("nohibernate", nohibernate_setup)` register bare names (hibernate.c raw 1518, 1523) whose handlers ignore their argument (raw 1440-1452). Unpinned corroboration (v7.2 `init/main.c` not in the pinned set; v6.12 read for semantics, stable code): `obsolete_checksetup` (`init/main.c` raw 195-222) matches `parameqn(line, p->str, n)` — a byte-prefix match — and calls `setup_func(line + n)`; `repair_env_string` (raw 502-514) re-attaches `=`, so the raw token reaches the matcher. Net: `noresume=1`, `noresume=0`, `noresumefoo`, `nohibernate=1`, `nohibernateXYZ` all set the flags in a real kernel; `parameqn` (`kernel/params.c` raw 86-95) is case-sensitive with `-`≡`_`, so `NORESUME` and `foo.noresume=1` do not fire. The gate/docstring accept only the exact bare lowercase token. Measured:

```
T9  +noresume=1   [L1]   rc=0 {"findings": [], "verdict": "HEALTHY"}   # kernel would set noresume
T10 +nohibernate=1 [L1]  rc=0 {"findings": [], "verdict": "HEALTHY"}   # kernel would set both flags
T11 +noresumefoo  [L1]   rc=0 {"findings": [], "verdict": "HEALTHY"}   # kernel would set noresume
```

Recommendation (rule text is frozen; nothing for the gate alone): if the L1 wants the availability rules to track the kernel exactly, extend docstring A1/A3 wording to "a token whose first `len(name)` bytes are `noresume`/`nohibernate`" plus the `=arg` forms; a gate-side-only change would diverge from the frozen battery text and break C2 — needs a re-freeze, so L1 decides.
Severity: low for this host (host cmdline, `facts-v2.json:3`, carries none of these forms; documented boot args use the bare tokens the pinned `Documentation/admin-guide/kernel-parameters.txt` rows 1963/4479/4593 describe).

**L2** — kernel `hibernate=no` sets both `noresume = 1; nohibernate = 1;` (hibernate.c raw 1432-1435); the gate records only HR-HIBERNATE-DISABLED. No observable finding-set difference: A3 is suppressed whenever A1 fires (frozen PREC-NOHIB semantics), and noresume has no other finding surface. Limits note only.

**L3** — `resume=` with an empty value: pinned `resume_setup` raw 1402-1407 `strscpy(resume_file, str)` unconditionally (when `!noresume`), so `resume=` leaves `resume_file` empty and `software_resume` bails at `find_resume_device`; the gate `:135-137` takes `""` as "r is set" and evaluates rules 2–8, which can return HEALTHY on a boot that would not resume. The frozen sentence "r = the value of the last resume= token or None" is ambiguous for the empty value; the gate's is the more literal reading. Unreachable from the battery (`set_token` always inserts non-empty values). Limits.

**L4** — parse-order sensitivity: pinned `resume_offset_setup` raw 1409-1411 returns early `if (noresume)` — a `noresume` token earlier on the cmdline makes the kernel ignore a later `resume_offset=`; the gate is order-independent. No observable effect on the frozen findings (the resume chain is already reported moot by A3/noresume bail). Limits, cosmetic.

## (3) `--live` path — OK

- **Absent lockdown → null, no failed probe**: capture `capture-resume-facts-r84.py:99-103` — `os.path.exists` false → `rec("test -e /sys/kernel/security/lockdown", 0, "absent\n", "")`, `lockdown` stays `None`; `failed_probes` (gate `:175-189`) flags only receipts lines `rc≠0`, so the rc 0 "absent" line never fails. Stub test (stub capture writing the absent branch receipt + `lockdown: null`):
  ```
  == S absent
  {"findings": [], "verdict": "HEALTHY"}
  rc=0
  ```
- **Unreadable lockdown fails closed**: a permission-denied read records rc 1 in the receipt → `{"error": "probe-failed", "failed": ["cat /sys/kernel/security/lockdown"], "findings": [], "verdict": "CANNOT-EVALUATE"}`, rc 2 (stub mode failed-probe, verbatim above in `fixture-runs.txt`). Also: capture rc≠0 → rc2 `capture-rc1`; facts.json not JSON → rc2 `unreadable:JSONDecodeError`. All fail closed. ✓
- **Writes**: gate creates only `tempfile.mkdtemp(prefix="hibernate-resume-")` under TMPDIR (`:199`) and `shutil.rmtree`s it in `finally` (`:220-222`); measured 0 leftovers after 5 runs. Capture writes only its `--out` dir (`facts.json`, `receipt.txt`; verified by direct run into scratch). Nothing outside the scratch dir. ✓
- **sudo -n still limited**: the three inspection commands unchanged (`capture-resume-facts-r84.py:73-79`: `btrfs inspect-internal map-swapfile -r`, `lsattr`, `filefrag -v`); the diff added **zero** sudo calls — the new lockdown probe is a plain `open()` read plus an rc-0 `test -e` receipt line. Real `--live` on the host (read-only path exercised end-to-end, incl. the sudo probes): `{"findings": [], "verdict": "HEALTHY"}` rc 0. ✓
- Host stayed read-only: no hibernate/suspend/swap/sysctl//sys//proc writes by any command I ran; all state under `$TMPDIR`.

## (4) Malformed `lockdown` — OK (all rc 2, findings [])

```
T15a lockdown 0 (int)              rc=2 {"error": "type:lockdown", ...}
T15b lockdown ["none"] (list)      rc=2 {"error": "type:lockdown", ...}
T15c lockdown true (bool)          rc=2 {"error": "type:lockdown", ...}
T15d lockdown ""                   rc=2 {"error": "lockdown-selection", ...}
T15e lockdown "none integrity confidentiality" (unbracketed) rc=2 {"error": "lockdown-selection", ...}
T15f lockdown "[none] [integrity] confidentiality" (two brackets) rc=2 {"error": "lockdown-selection", ...}
T15h key dropped                   rc=2 {"error": "missing:lockdown", ...}
T14 null accepted                  rc=0 {"findings": [], "verdict": "HEALTHY"}   # = file absent
T15g "[none]" accepted             rc=0 {"findings": [], "verdict": "HEALTHY"}
```

Exactly the frozen clause (`resume-gate-battery-r85.py:38-42`: type str-or-null, exactly one `[x]` word, else rc2 findings []). Gate lines `:85-88` (`need(f, "lockdown", str, nullable=True)`; `len(selected) != 1`).

## (5) Consumer regression — OK

- `SKILL.md:5916` (capture row) documents `resume-facts/2` = `/1` plus `lockdown`, the rc-0 "absent" recording, and the unchanged sudo set. `SKILL.md:5917` (gate row) lists all 14 finding IDs incl. the three availability rules and the rc2 clause "(any schema other than `resume-facts/2`)". `SKILL.md:5918` marks the r84 battery "HISTORY ONLY since round 85: fixed case order (QUALITY 119) and `resume-facts/1` documents, which the v2 gate refuses" — the supersession is written down where consumers look.
- `grep -rn "resume-facts/1" corpus/` → zero hits. Knowledge entries reference the gate by its unchanged interface (`--live`, rc 0/1/2): `corpus/knowledge/hibernate-resume-plane-r84.md:4,8,64`, `corpus/knowledge/hibernation-availability-r85.md:4,8`. No live consumer feeds v1 documents to the v2 gate.
- Measured cross-check of the documented supersession: `python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py` → rc 1, `"verdict": "unmet"`, `"families_passed": 1` (only MALFORMED survives; every clean v1 doc is refused rc2) — `ReviewGate/r84-vs-v2.json`. Intentional and documented, not a silent regression.
- Provenance note (outside the reviewed diff): `corpus/knowledge/hibernation-availability-r85.{md,json}` (untracked) and a modification to `corpus/knowledge/hibernate-resume-plane-r84.md` exist in the worktree — the L1's in-flight C1 landing, commit `479d868` does not contain them; C1 is judged by the closure, not this seat.

## Residual risk and verification gaps

1. **L1 rests partly on an unpinned source**: v7.2 `init/main.c`/`kernel/params.c` are not in `.ufo/waves/round-85/before/src/`; the prefix/arg-matching semantics are cited from v6.12 (same upstream, `obsolete_checksetup`/`parameqn` are stable). The pinned hibernate.c functions (handlers ignore args) and the bare-token `kernel-parameters.txt` rows support the divergence claim independently.
2. The three 20/20 runs were measured at `479d868`; the declaration's target is "at the landed lane tip" — if the L1 lands further commits (e.g. the C1 entry), the counting command needs one more pass at the new tip.
3. `L3`/`L4` are unreachable from the battery and from this host's measured cmdline; no runtime verification beyond hand fixtures.
4. Not reviewed here: the C1 entry contents (closure's jurisdiction) and anything outside the two changed files.

No tool installs were needed (python3, git, curl, coreutils only).
