VERDICT: no-finding  (item C1-11: no committed file under tools/ writes under /tmp regardless of TMPDIR; two stale-comment nits and one non-/tmp hardcode noted)

Method: `git grep -nE '/tmp|mkdtemp|mktemp|tempfile|TemporaryDirectory|NamedTemporary|gettempdir|TMPDIR|/var/tmp|/dev/shm' -- tools`
plus a second `git grep` for `tempfile.tempdir|gettempdir|'tmp')|dir=_parent|parent *=|--scratch|--work`, and the omp `grep` for `/tmp`
over tools/. Lane HEAD at run time: 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf; `git status --short tools` empty (working tree == committed).
58 tracked files under tools/. Read-only; nothing written outside this report. Not done: I did not execute any tool to observe its runtime temp paths.

## 1. Files that write under /tmp regardless of TMPDIR
None. There is no `mkdtemp(dir='/tmp')`, `mktemp -d /tmp/...`, `/var/tmp` or `/dev/shm`, and no `tempfile.tempdir`/`gettempdir` override in tools/.
Every `/tmp` literal in tools/ (full list, 11 hits across 7 files):

| file:line | literal | write root? | TMPDIR honoured? |
|---|---|---|---|
| tools/boot-chain-audit.sh:179 | `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain.XXXXXX"` | yes (live work dir) | YES (fallback only when unset) |
| tools/boot-chain-audit.sh:878 | `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain-selftest.XXXXXX"` | yes (selftest) | YES |
| tools/boot-chain-audit.sh:1281 | `"${TMPDIR:-/tmp}"` in an error message | no (message) | YES |
| tools/tsukuroi-census.sh:1892 | `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX"` | yes (selftest) | YES (changed at 52ffd65; was `mktemp -d /tmp/...` at 8bd001f:tools/tsukuroi-census.sh:1828) |
| tools/tsukuroi-census.sh:370, 553 | `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*` in comments/usage | no | YES (updated at 52ffd65) |
| tools/tsukuroi-census.sh:373 | comment: "builds a /tmp fixture tree" | no (comment) | STALE WORDING, see nit 1 |
| tools/tsukuroi-census.sh:817 | `/usr/lib/tmpfiles.d/root.conf` | no (substring match "tmpfiles") | n/a |
| tools/check-boundary-contract.py:178 | `'lesson — /tmp/decoy/.ufo/'` | no (selftest fixture text, a path *string* in a mutated doc) | n/a |
| tools/check-edit-contract.py:268 | `'— /tmp/decoy/.ufo/'` | no (same) | n/a |
| tools/check-recheck-commands.py:1025 | `"... sort > /tmp/fp.txt; wc -l < /tmp/fp.txt\n"` inside a fixture doc string | no (documentation text parsed by the gate, not executed) | n/a |
| tools/check-review-snapshots.py:165 | `report="/tmp/report"` | no (negative-case manifest value) | n/a |

Census diff proof (`git show 52ffd65 -- tools/tsukuroi-census.sh | grep -nE '^[-+].*(/tmp|TMPDIR|mktemp)'`): three line pairs, comment 35/36, usage 64/65, code 118/119, each `/tmp/...` -> `${TMPDIR:-/tmp}/...`.
At the base 8bd001f the only code-level hardcoded write root in tools/ was census.sh:1828; after 52ffd65 that is gone.

## 2. Temp-dir creators that rely on the ambient TMPDIR (no dir=, no --scratch): honour TMPDIR (Python tempfile consults TMPDIR before /tmp)
mkdtemp/TemporaryDirectory with prefix only (no `dir=`): tools/_revision.py:218; check-adjacency-anchors.py:968; check-adjacency-overlap.py:232,901,908;
check-appended-notices.py:565; check-boot-chain.py:1327; check-boot-writers.py:675; check-freshness-r17.py:347,360,493,540; check-kernel-taint.py:274,292,1020;
check-knowledge-header.py:393; check-locator-clarification.py:576; check-memory-pressure.py:128,145,906; check-owed-statements-r29.py:163 (module-level import-time mkdtemp);
check-recheck-commands.py:1131; check-registry-coverage.py:24 (module-level),527; check-report-receipts.py:435; check-revision-binding.py:815,865,1183;
check-root-dac-correction.py:389; check-seat-scope.py:283; check-section-citations.py:593; check-self-assessment.py:69 (module-level),181,1032;
check-source-scope-correction.py:435; check-storage-health.py:56 (module-level),993; measure-update-recheck.py:516; mutants-adjacency-overlap.py:42;
mutants-btrfs-space-r30.py:382; mutants-kernel-taint.py:55; score-census-handoff-r32.py:866; score-pacnew-arm-r35.py:316; score-pacnew-arm-r35b.py:474.
None accepts a --scratch/--work argument; they follow TMPDIR only. With TMPDIR unset they fall to /tmp (stdlib default), which is the documented-and-honoured behaviour, not a hardcode.
Embedded shell: tools/score-pacnew-arm-r35b.py:94 `t=$(mktemp -d)` (inside the scripted census fixture); `mktemp -d` honours TMPDIR, and the harness sets TMPDIR=<work>/tmp at :372.

## 3. Tools that take --scratch DIR (or hardcode a scratch default that is not /tmp)
- score-storage-arm-r38.py:181,192-194 and score-storage-arm-r38-q82.py:90,98-100: `--scratch DIR`, else `mkdtemp(prefix=...)` -> TMPDIR; child TMPDIR pinned to `<work>/tmp` (r38.py:157,197; q82.py:109,118). Honours both.
- score-census-handoff-r32.py:826,866: `--scratch`, else mkdtemp -> TMPDIR. Honours both.
- probe-child-env-allowlist-r32/r33/r34/r36/r37.py, probe-git-child-env-r31.py, probe-git-env-leak.py, probe-git-env-residual-r30.py (e.g. r37.py:1103,1109,1112):
  `parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)` then `mkdtemp(dir=parent)`. Honours --scratch; default is a hardcoded *non-/tmp* path
  when it exists, else None -> TMPDIR. Note: this default ignores TMPDIR whenever /fast/scratch/hyaku exists (that is the host scratch plane, not /tmp).
- mutants-owed-statements-r29.py:39-41, mutants-owed-statements-r29-landed.py:39-40, run-receipt.py:80-82: same hardcoded `/fast/scratch/hyaku`-if-exists default, **no --scratch argument**, else TMPDIR.
- mutants-owed-statements-r29-v4shapes.py:31-32: `SEAT_ROOT` same pattern, no --scratch (comment at :30 says "scratch now goes to /fast/scratch/hyaku (or TMPDIR)").

## 4. Nits (not /tmp-write defects)
1. tools/tsukuroi-census.sh:373 still says "builds a /tmp fixture tree" although the code (:1892) and its sibling comments (:370,:553) now use ${TMPDIR:-/tmp}. Wording-only; the 52ffd65 diff did not touch that line (it is not in the grep of `^[-+]` lines above).
2. The `/fast/scratch/hyaku` default in section 3 is an environment-specific absolute path baked into committed tools (operability: breaks portability, ignores TMPDIR when present); tools without --scratch (mutants-owed*, run-receipt.py) cannot be redirected except by removing that dir.

## Verdict basis
Claim "no hardcoded /tmp in committed tools" holds at HEAD 5edb6c2: zero write-root /tmp literals remain; the one that did (census.sh:1828 at 8bd001f) was fixed in 52ffd65.
