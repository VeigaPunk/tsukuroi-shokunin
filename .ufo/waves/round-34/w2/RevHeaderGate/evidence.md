RevHeaderGate — read-only evidence (all reads of committed bytes at 879daa95 unless noted)

1. Gate identity: `git show 879daa95:tools/check-knowledge-header.py | sha256sum`
   = 592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919
   (same digest reported for the wave-1 artefact by ExecHeaderGate and by
   GatesAfterNoHarm finding 3; `_revision.py` blob 24f398a6b981 unchanged base→tip).

2. Spawn surface of the gate: exactly one `subprocess.run`, at
   tools/check-knowledge-header.py:110-112, with `env=_revision.clean_env()`;
   `_revision.clean_env()` (_revision.py) returns the literal allow-list
   {PATH=/usr/bin:/bin, GIT_OPTIONAL_LOCKS=0, GIT_PAGER=cat, LC_ALL=C,
   GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null}. No `os.environ`/`getenv`
   read in the gate. Sibling parity: check-recheck-commands.py:54-55 does the same
   dont_write_bytecode + `import _revision`.

3. Rule locations in the landed gate (879daa95):
   KEYS=("source","verified-at","recheck") :56; SCOPE corpus/knowledge :57;
   ISO/CADENCE/ON_RELEASE/FENCE regexes :58-61; _lane_flag :61-67;
   _default_lane :70-76; import _revision :79; git() :109-113;
   read_blob/notes_at :116-141; header_lines (column-0 keys, fence exclusion,
   LAST occurrence) :144-166; has_date/date_problem/cadence_problem :179-199;
   RULES source->None :202; evaluate (MISSING per absent key, VALUE on last
   occurrence) :205-221; run() bind + CANNOT paths :270-308; selftest 25 cases
   :355-455 (missing each key :407-421, value rules :423-436, fences/mid-line/
   indented :439-451, last-occurrence pass cases :444-448 & :453-455, binding
   refusals :457-475).

4. Multi-occurrence header keys in real notes at the tip (git grep -c '^key:'):
   19 notes have 2 source: lines, 14 have 2 verified-at:, 15 have 2 recheck:.
   Operative-vs-pointer pairs (first -> last):
   - journal-boot-plane.md: recheck :9 "Appendix probe command set..." (no date/
     cadence) -> :441 "30d; procedure: ..." (operative).
   - aur-risk-plane.md: recheck :15 pacman probe list (no cadence) -> :347 "90d".
   - adjacency-handoffs-fleet-r1.md: recheck :3 "§4 ... §5 ..." pointer -> :221
     "180d"; source :1 -> :219; verified-at :2 -> :220.
   - pause-lift-gate-r24.md: recheck :3 "after any package transaction..." (no
     ISO date or cadence token) -> :94 "...Recheck cadence: on-release.".
   So the last-occurrence rule is load-bearing: first-occurrence semantics would
   mark at least four admitted notes red. The corpus's own convention text:
   adjacency-handoffs-fleet-r1.md:222 "supersedes the pointer-only recheck: line
   above" (same phrase in aur-drift-receipt-r9.md:255, aur-risk-plane.md:348);
   check-recheck-commands.py:441-450 implements the identical "LAST recheck:
   line" rule citing the journal-boot-plane convention.

5. Sibling divergence verified: check-recheck-commands.py:448-449
   (`recheck_line`) scans `line.startswith("recheck:")` with NO fence exclusion;
   its fence logic (:461-468, :484-491, :508-514) covers headings/procedure/
   backtick spans only. The new gate's docstring (:18-20) claims "the same rule
   tools/check-recheck-commands.py applies" — true for headings, not for
   recheck: lines; the gate is stricter (fenced keys do not count). Divergence
   is fail-safe: a fenced-only key yields MISSING (red), never a pass.

6. Receipts (evidence-verified, never executed by this seat):
   - w1/ExecHeaderGate/exits.txt: base 6de666c exit 1, FAIL, 53 notes, 52
     complete, 43 clean, 11 findings; kill-oom-boundary-r33.md named for missing
     source: and missing verified-at: (findings 8-9 of that report);
     variant 30e9665f exit 0, 53/53/53, 0 findings; --selftest 25/25 PASS;
     E-REVISION-NOT-LANDED on unlanded sandbox commit; E-LANE-UNRESOLVED exit 2.
   - w2/GatesAfterNoHarm/tip-check-knowledge-header.jsonl: exit 0, PASS,
     note_count 54, complete_count 54, clean_count 54, findings [];
     coredump-count-unit-r34.md lines {source:3, verified-at:4, recheck:5};
     kill-oom-boundary-r33.md {recheck:3, source:4, verified-at:5}.
   - w2/MutHeaderGateKeys/m1-pristine.json: unmutated --selftest exit 0;
     m1-mutated.json (verified-at dropped from KEYS) exit 1 — mutant killed.
   - SKILL.md:2942 registers `knowledge-header` (gate) with its --selftest row;
     check-registry-coverage passes at the tip (GatesAfterNoHarm finding 14).

7. Seat-scope trailer rule (tools/check-seat-scope.py:59-95, selftest :363):
   the LAST `Scope: executed=` line is read; only the literal value `none`
   passes for a NO-EXEC seat; `none (read-only git show)` is
   SCOPE-TRAILER-MALFORMED and any command list without EXEC-AUTHORIZED is
   SCOPE-EXEC-UNAUTHORIZED. All commands this seat ran were read-only reads of
   committed bytes (git show/log/ls-tree/grep/diff/rev-parse, jq, sha256sum,
   comm, grep, sed), so executed=none is the truthful literal.

8. Worktree state at review time (uncommitted, untrusted): M SCORECARD.md,
   M corpus/SOURCES.md, M corpus/knowledge/coredump-count-unit-r34.md (adds
   S189 to the source: line; all three header keys stay at column 0),
   untracked .ufo wave files. The gate reads blobs at the bound revision, so
   drift does not affect its verdict.
