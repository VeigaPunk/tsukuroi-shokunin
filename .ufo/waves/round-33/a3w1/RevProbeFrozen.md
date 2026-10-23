# RevProbeFrozen — review of the frozen C1 counter at 9c89ff4f (round 33, wave a3w1)

VERDICT: the frozen counter is self-consistent — checks (1)–(4) pass byte-exact; check (5) found one
moderate evasion gap (`is_git` pathname check) and several low-severity divergences where the code is
weaker or stricter than the predicate/docstring text. No finding blocks freezing; the gap in finding 5.1
means a deliberate `/bin/git` invocation evades the kept-settings and git-count clauses.

Checked object: `tools/probe-child-env-allowlist-r33.py` at commit
`9c89ff4f093d07a6f92925518310ca6a7c8a2fa0` (lane `tools/` worktree file verified byte-identical to the
blob). Line numbers cite `9c89ff4f:tools/probe-child-env-allowlist-r33.py` and
`9c89ff4f:SCORECARD.md`.

## Check 1 — predicate byte-identity: PASS [obs]

The three texts are the same 799 bytes (sha256 prefix `9726dc77fa26dac6` of each):

- docstring `FROZEN PREDICATE` sentence: probe line 81 (single physical line, `FROZEN PREDICATE: ` prefix
  stripped); the only other `FROZEN PREDICATE` occurrence is the assertion message at line 159.
- constant `PREDICATE`: probe lines 148–158 (implicit string concatenation), defined exactly once.
- SCORECARD amendment-2 quote `Frozen predicate C1 after amendment 2`: `9c89ff4f:SCORECARD.md:1372`,
  the text between the first `"` after the colon and the next `"`; nothing follows the closing quote.

The round-33 *declaration* quote at `SCORECARD.md:1345` is 714 chars and differs — it is the
pre-amendment sentence (no `GIT_CONFIG_NOSYSTEM` clause). That is correct behaviour for a history
section; the binding quote is the amendment-2 one at 1372. [obs]

Nuance [obs]: the import-time guard at line 159 is `assert PREDICATE in ' '.join(__doc__.split())` —
normalized-whitespace substring membership, not literal byte equality of the docstring line, and it
would pass on any second occurrence inside the docstring. The current bytes do match literally, so the
check holds today; the guard is weaker than its message (`docstring FROZEN PREDICATE differs from
PREDICATE`) implies. A rewrap of the docstring's predicate line would silently keep the assertion green
while changing the declared text's presentation. [inf]

## Check 2 — probe sha256: PASS [obs]

`git cat-file blob 9c89ff4f:tools/probe-child-env-allowlist-r33.py | sha256sum` →
`c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd` (independently: hashlib over
`git show` bytes). 46 077 bytes, 882 lines. The lane worktree file at `tools/probe-child-env-allowlist-r33.py`
is byte-identical to the blob (lane HEAD is `5a967ce2`, past the tool commit; the frozen bytes are
untouched).

## Check 3 — diff-stat touches only allowed paths: PASS [obs]

`git diff 1f521b93 9c89ff4f --name-only` lists exactly 59 files, all matching
`.ufo/waves/round-33/l1/dev-a2/*` or `.ufo/waves/round-33/l1/dev-candidates/*`, plus `SCORECARD.md`
(+42) and `tools/probe-child-env-allowlist-r33.py` (+882, new). `--stat` shows `1180 insertions(+),
0 deletions` — pure additions. None of the five claim targets (`tools/_revision.py`,
`tools/check-adjacency-anchors.py`, `tools/check-boot-writers.py`,
`tools/check-root-dac-correction.py`, `tools/mutants-owed-statements-r29-v4shapes.py`) appears in the
diff; no target bytes changed.

## Check 4 — exit-code mapping: PASS [obs]

Docstring lines 102–103: "Exit 0 when leaking is 0 and there is no harness error, 1 when a pair
leaks, 2 on a harness error." Code: line 878 `return 2 if errors else (1 if leaking else 0)` and line
882 `sys.exit(main())`; harness errors take precedence over leaks. Probe-level preflights also return 2:
scratch-inside-lane (776), scratch-root-inside-git-repo (782), strace missing (785), revision
unreadable (789) — each prints a JSON error line and exits 2, consistent with "harness error". `pairs`
at line 872 counts only channel results (5 targets × 3 channels = 15 when nothing is a harness error),
and `--only` reduces it by design. Unhandled exceptions (e.g. `git clone` failing at line 794) exit 1
via the interpreter without a summary line — the code cannot print a false clean summary, but exit 1 is
shared with "a pair leaks"; acceptable and worth noting only as an observer caveat. [obs]

## Check 5 — places where the code does not do what the predicate says

5.1 **MODERATE — `is_git` recognises only two pathnames** (lines 261–262): `fname == '/usr/bin/git'` or
`fname.startswith('/usr/lib/git-core/')`. The predicate's clause "any traced git execve lacks
GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null" names no pathname; a git child exec'd as
`/bin/git` (a live symlink to `/usr/bin/git` on this host), as `./git`, or as a copied binary at any
other path is invisible to `git_missing_kept` (line 312) and to the "count of successful git execs"
parity term (line 311), and — if the target then never execs `/usr/bin/git` — to the control-run
"started at least one git child" gate (line 810). A mutant `clean_env` can strip ambient names and both
kept settings, invoke git via `/bin/git`, and emit no predicate evidence at all (parity holds because
nothing changed for the observable trio if rc/stdout match). The strace still records the execve; only
the pathname filter misses it. This is a counter-evasion gap against a deliberately-evasive
implementation, not a false-positive source; natural regressions resolving `git` through `PATH` still
land at `/usr/bin/git`. [obs]

5.2 LOW — **`from tools.X import f` / `import tools.X` are not scanned** (lines 489–491, 636–644,
744–746): `_aliases` only treats `from os|subprocess|sys import` specially, `import` statements record
only the first dotted component, and the transitive walk maps imports by first component onto
`tools/<first>.py` — so a `tools/` package module referenced as `tools.helper` queues `tools/tools.py`
and is never scanned, and an env-builder imported `from tools.helper import make_env` resolves to
`tools/tools.py` and is flagged as unreadable. The docstring's `source` channel says the scan covers
"every `tools/` module it imports" (lines 43–46) and amendment 2 says builders may be "a name imported
from a tools/ module" (line 67). Direction is conservative (false positive on `from tools.*` import
style, miss on `import tools.*` attribute use); runtime channels still catch actual leakage. [obs]

5.3 LOW — **an `env=` name bound by AugAssign passes the shape rule unchecked** (line 628): in
`env_ok`, any binding that is not an `ast.expr` is rejected *unless* it is `ast.AugAssign`, in which
case it is silently accepted — so `env = build(); env |= something` lets `something` be any
expression, outside the docstring's enumeration (dict display, dict comprehension, `dict(...)`, `|` of
those, a name every binding of which is one of those). Partly mitigated: ambient reads and
hiding-constructs inside the expression are still flagged by the independent rules. [obs]

5.4 TRIVIAL — **harness gating has an undocumented third condition** (line 806): control run A must
exit 0; the CONTROL spec (lines 93–97) names only parity agreement and ≥1 git child. A target failing
at the base is a harness error rather than leak evidence — reasonable semantics, but the docstring
says "Control runs A and B must agree on parity and A must start at least one git child" and the exit-0
requirement is absent there (it is implicit in the paragraph that precedes it). [obs]

5.5 TRIVIAL — **`getattr`/`setattr`/`hasattr`/`delattr` non-string constant attribute names pass**
(lines 675–679): the flag fires when the attribute argument is not an `ast.Constant`, is `os.environ`
etc., or the call has <2 args or hits os/posix/sys — but `getattr(x, 42)` (a non-string constant) is
not flagged while the docstring says "with an attribute name that is not a constant string". Runtime
TypeError makes it harmless. [obs]

5.6 TRIVIAL — **wording-vs-code drift, all in the safe direction**: the kept-settings check (line 312)
scans *every* parsed record including `execs[0]`, where the predicate's "after the target's own first
exec" is dead code (`is_git` can never match the python execve) — harmless; `parse_trace` keeps only
successful execs (lines 250–257) while the predicate says "any traced execve" — failed execs carry no
living child, consistent; `EXCLUDED_PREFIX` uses `startswith('PYTHON')` (line 185 strips `PYTHON*` for
the control env and name generation) matching the docstring's `PYTHON*`. [obs]

## Residual risk and verification gaps

- `strace -s 65536` truncates any single environment *string* longer than 64 KiB to `...`; injected
  names/values are short, so this affects only pathological values, not the declared channels. [unk]
- Evasion requires intent: nothing in the diff exercised runtime behaviour this review; all runtime
  claims rest on code reading plus the L1's dev-run receipts cited at `SCORECARD.md:1374`, which this
  seat did not re-run (the pristine receipt belongs to seat C01Before). [obs]
- The probe asserts nothing about `os.exec*e`/`os.spawn*e` env shapes (SPAWN_ANY includes them only for
  the reference-not-called rule); consistent with the docstring's "non-`e` `os.exec*`/`os.spawn*`"
  wording — a `subprocess`-spawn-shaped `env=` passing an ambient `os.spawnve` env dict is outside the
  declared scan, matching the docstring's stated known-limit. [obs]

Scope: read=`9c89ff4f:tools/probe-child-env-allowlist-r33.py` (all 882 lines), `9c89ff4f:SCORECARD.md`
lines 1204–1374 region, `git diff 1f521b93..9c89ff4f --stat/--name-only`; wrote=.ufo/waves/round-33/a3w1/RevProbeFrozen.md, .ufo/waves/round-33/a3w1/RevProbeFrozen/predicate-frozen.txt (the 799-byte predicate plus newline), scratch copies under /fast/scratch/hyaku/tsukuroi-r33a3/RevProbeFrozen/; executed=read-only git (rev-parse, status, show, cat-file, diff) and sha256sum on the lane; no probe runs, no writes to lane refs.
Model: devin/swe-2
Installs: none
