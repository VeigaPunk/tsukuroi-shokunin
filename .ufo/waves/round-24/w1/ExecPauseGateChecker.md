# ExecPauseGateChecker — wave-1 report (C2 counting command)

Verdict: The C2 counting tool is written, compiles, passes a 23-case selftest
that builds sandbox git repositories, passes a realistic end-to-end run against
the real l1-4 capture bytes, and returns the declared exit codes (0, 1, 2)
with one JSON object per run. The review findings of RevGateSchema-2 are all
closed in this draft.

1. [obs] The tool draft was written at
   /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py
   (executable, Python 3 standard library only). `python3 -m py_compile`
   returns 0. It imports the lane module `tools/_revision.py` (`bind`) by
   resolving the lane root from the current working directory or from the
   script location, so the identical file works when landed at
   `tools/check-pause-gate.py` and run as
   `python3 tools/check-pause-gate.py --revision <REV>` from the lane root.

2. [obs] Counting rule implemented exactly as declared in the round-24 context
   and amended per RevGateSchema-2: a premise counts only if (a) its verdict is
   one of the decided verdicts cleared, still-holds or changed — an
   `unverified` verdict is a valid schema value but does not count (the output
   carries `premises_unverified`); (b) every evidence pointer resolves at the
   bound revision — the file exists, the 1-based line is in range, the exact
   substring occurs on that line, the needle is at least 3 characters, is not
   capture boilerplate (does not start with `###` or `exit=`), and occurs
   exactly once in its file; (c) at least one pointer resolves into the capture
   section mapped to that premise (P1 pending/pending-count/pending-repos; P2
   local-newer-than-sync/boot-chain-installed/boot-chain-sync; P3
   boots/plymouth-boot0/plymouth-boot-1/boot-chain-installed/hooks-new-root/
   init-root/buildroot-symlink; P4 mirror-servers/repo-servers/sync-db-mtime/
   pacman-log-last-sync/stable-mirror-headers; P5 cache-file-count/
   cache-package-files/cache-entries/pacman-commands-since-pause/
   pacman-log-since-pause/sudo-package-commands-since-pause/foreign-new/
   paccache-runs-since-pause); and (d) every listed source id is a single,
   unique row of `corpus/SOURCES.md` at the revision whose status cell is
   `mined`, whose `used-by` cell contains `pause-lift-gate-r24`, and whose
   `opened` cell contains `2026-10-22`. Schema fields per
   `tsukuroi-pause-gate-v1`: `schema`, `captured_at`, `capture` (lane-relative
   path), `premises` (id P1..P5, premise, verdict, evidence, sources, limits).
   Missing `premise` or `limits` is a counting failure.

3. [obs] All bytes are read from the git object database at the bound revision
   via `git cat-file blob <sha>:<path>` (read-only; `_revision.clean_env()`);
   the host is never probed. Lane-relative paths are enforced (no absolute
   paths, no `..` traversal); self-referential evidence into the gate JSON or
   the companion note is rejected; duplicate JSON keys in the gate entry are
   rejected via an `object_pairs_hook` (GATE-JSON-DUPLICATE-KEY).

4. [obs] Exit codes: 0 only when `premises_verified == 5`, `premises_total ==
   5`, and the document is valid; 1 for a missing, malformed, or not-fully-
   verified gate entry; 2 for an unreadable revision (`_revision.RevisionError`
   or a read failure), with status CANNOT_EVALUATE. Each run prints exactly one
   JSON object with fields `revision`, `premises_total`, `premises_verified`,
   `premises_unverified`, per-premise `premises` results, and `findings`.

5. [obs] Selftest (`python3 tools/check-pause-gate.py --selftest`) builds real
   sandbox git repositories under /fast/scratch/hyaku/tsuku24-ExecPauseGateChecker/
   and drives the full bind-and-count path per case. It passed all 23 cases
   (status=PASS, cases=23, failed=0; summary saved at
   .ufo/waves/round-24/w1/ExecPauseGateChecker/selftest-run.txt and
   selftest.json):
   - pristine: exit 0, 5/5
   - missing-premise: exit 1, 4/4, GATE-PREMISE-SET
   - bad-verdict: exit 1, 4/5, verdict-not-in-vocabulary
   - all-unverified: exit 1, 0/5, verdict-undecided (review finding 1)
   - evidence-line-out-of-range: exit 1, 4/5
   - substring-absent: exit 1, 4/5
   - needle-short: exit 1, 4/5, evidence-needle-short
   - needle-boilerplate: exit 1, 4/5, evidence-needle-boilerplate
   - needle-not-unique: exit 1, 4/5, evidence-needle-not-unique (finding 2)
   - source-missing: exit 1, 4/5
   - source-opened-on-another-date: exit 1, 4/5
   - source-status-rejected: exit 1, 4/5, source-status-not-mined (finding 3a)
   - source-used-by-other: exit 1, 4/5, source-used-by-not-gate (finding 3b)
   - duplicate-json-key: exit 1, 0/0, GATE-JSON-DUPLICATE-KEY
   - wrong-schema: exit 1, 0/0, GATE-SCHEMA
   - capture-absent: exit 1, 0/5, GATE-CAPTURE
   - duplicate-premise-id: exit 1, 4/5, GATE-PREMISE-SET
   - limits-absent: exit 1, 4/5, limits-missing (finding 4)
   - premise-text-absent: exit 1, 4/5, premise-text-missing (finding 4)
   - section-mismatch: exit 1, 4/5, no-capture-section-fit (finding 5)
   - evidence-outside-capture: exit 1, 4/5, no-resolvable-capture-line
   - self-referential-evidence: exit 1, 4/5, evidence-self-referential
   - unreadable-revision: exit 2, E-REVISION-INVALID
   Each of the review's required failure modes is demonstrated.

6. [obs] Realistic end-to-end integration: in a sandbox clone of the lane at
   HEAD, I committed the real l1-4 capture bytes
   (.ufo/waves/round-24/capture/l1-4/capture.txt, from the working tree), a
   gate entry whose five premises carry evidence pointers chosen
   programmatically inside the correct capture sections (P1 pending line 40,
   P2 local-newer-than-sync, P3 hooks-new-root, P4 sync-db-mtime, P5
   cache-entries), and a SOURCES row S087 opened 2026-10-22 with status mined
   and used-by pause-lift-gate-r24. Running `python3 tools/check-pause-gate.py
   --revision <sha>` from the sandbox clone root: exit 0, status PASS, 5/5
   verified, 0 unverified, no findings
   (artifact: .ufo/waves/round-24/w1/ExecPauseGateChecker/integration-pass.json).

7. [obs] Negative controls on the same sandbox, against real committed bytes:
   drop-premise, bad-verdict, all-unverified, line-out-of-range,
   substring-absent, source-missing, source-other-date, and duplicate-key all
   exit 1 (duplicate-key gives 0/0 with GATE-JSON-DUPLICATE-KEY); the
   all-unverified gate reports verified 0/5 and `premises_unverified: 5`.

8. [obs] Exit-2 checks: `--revision 000...0` (40 zeros) exits 2 with
   E-REVISION-INVALID; `--revision HEAD` exits 2 (7-64 hex required);
   `--revision f169b3ba...` (readable, gate absent) exits 1 with
   GATE-MISSING; live lane at HEAD 10b45f0 exits 1 with GATE-MISSING (gate
   JSON not committed yet; the L1 must land gate JSON, the l1-4 capture and
   the round-dated registry rows atomically). Short hex and uppercase hex were
   verified on the earlier draft revision.

9. [obs] No tools were installed or updated; the tool uses only the standard
   library and the lane's `_revision` module.

10. [inf] The working tree currently carries uncommitted edits (not from this
    seat) to `tools/check-pause-gate.py` and `tools/report-red-causes.py`
    (e.g. pinning the capture to l1-4 with a `capture_sha256` field and a
    ROUND_DATE constant). My draft implements the same counting rule from the
    declared schema without a hardcoded capture path or sha256 pin: it validates
    whatever capture path the gate JSON declares. The L1 should reconcile which
    version to land. The review's content findings (finding 6: P1 pending-count
    vs checkupdates 134; P5 cache "4 entries" vs 0 package files) are for the
    gate-entry seat, not the checker.

Risks and blockers: none blocking the draft. The main external dependency is
that a committed gate entry with 5 decided premises referencing the l1-4
capture, and SOURCES rows opened 2026-10-22 with status mined and used-by
pause-lift-gate-r24, must land for the counting command to reach exit 0; until
then the tool correctly returns exit 1 with GATE-MISSING or source findings.

Scope: read=<lane files via git object db at bound revisions; capture commit
10b45f0 and f169b3ba; sandbox clone under /fast/scratch/hyaku/tsuku24-ExecPauseGateChecker/;
SOURCES.md, l1-4 capture working-tree bytes, gate drafts>; wrote=<.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py,
.ufo/waves/round-24/w1/ExecPauseGateChecker.md, .ufo/waves/round-24/w1/ExecPauseGateChecker/selftest.json,
.ufo/waves/round-24/w1/ExecPauseGateChecker/selftest-run.txt,
.ufo/waves/round-24/w1/ExecPauseGateChecker/integration-pass.json>; executed=<python3
tools/check-pause-gate.py --selftest; python3 tools/check-pause-gate.py
--revision <REV> in sandbox clones; git init/commit/rev-parse in sandbox
clones; git cat-file blob / git show read-only in lane; python3 -m
py_compile>
Installs: none
