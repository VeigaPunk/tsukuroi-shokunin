# Round 36 w1 — ReviewC1Design: review of the C1 patch design

Seat `ReviewC1Design` (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, read-only.
Base `6d76fb20f6ecbc940e5c8fff36c74060c885e161`. Written 2026-10-24T02:59:02Z (`date -u` at write time).

## 0. Artifact — two revisions, this review is of the second

Primary input reviewed: `.ufo/waves/round-36/w1/ExecC1Design/c1-five-tools.diff`,
**sha256 `2287b83f5ea5d3a47e125d2fb1e5a93063c7a5110a31d23ac49f0988595b5205`, 4622 bytes, 114 lines.**
Pin this digest if the L1 lands the diff.

A first revision (4851 bytes, 23:52 local) was mechanically corrupt and was **superseded while this
review ran**. It is recorded only for provenance: `git apply --check` → `error: corrupt patch at
…c1-five-tools.diff:64`; `patch -p1 --dry-run` → `patch: **** malformed patch at line 64:
@@ -786,3 +796,3 @@`; three hunk bodies disagreed with their headers (`@@ -771,3 +771,13 @@` body old=4;
`@@ -841,5 +851,5 @@` body old=6 new=7; `@@ -359,6 +359,11 @@` body old=5 new=10). The reviewed revision
has consistent counts on all eight hunks, and the applied tree is **byte-identical** to an
independent reconstruction I built from the hunks' intent (five files compared with `cmp`).

Application mechanics (F4, minor): `patch -p1` applies it; `git apply` needs `--unidiff-zero`
because two hunks carry no context (`@@ -440,1 +440,1 @@`, `@@ -771,1 +771,10 @@`). Without the flag
`git apply` reports `patch does not apply` at `score-census-handoff-r32.py:440`.
With it: `Applied patch … cleanly` for all five files.

## 1. Method and limits

No LSP server device is mounted in this runtime (`read xd://lsp` → `No such tool: xd://lsp. Mounted
devices: ast_edit, debug`), so this review is syntactic: grep over the base extract
(`/tmp/revc1-base`), the applied tree (`/tmp/revc1-final`) and line-range reads, plus `py_compile`
and an AST duplicate-key scan. No production file was edited; no git write. Machine evidence:
`.ufo/waves/round-36/w1/ReviewC1Design/spawn-inventory.json` (base inventory + patched state) and
`.ufo/waves/round-36/w1/ReviewC1Design/patched-state.txt` (command outputs).

## 2. Per-tool verdicts (against the patch as applied)

### 2.1 `tools/check-revision-binding.py` — PASS

`clean_env()` becomes a literal dict (`:103-111`): `PATH=/usr/bin:/bin`, `LC_ALL=C`,
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=os.devnull`, `GIT_OPTIONAL_LOCKS=0`, `GIT_PAGER=cat`.
All six real spawns stay on it — `:112-115` (`git --no-pager -c core.hooksPath=/dev/null`),
`:186-188`, `:223-226`, `:365-369` (sandbox tool), `:415-417`, `:1114-1116` — so **6/6 spawns are
env-bound** (the 7th `subprocess.run` match is the `STUB` string at `:1016-1020`, not a spawn site).
No `os.environ`/`getenv` remains in the file. Retained values exactly as declared; `PATH` is new
(absent at the base) and resolves `git` to `/usr/bin/git` [inf].

### 2.2 `tools/check-report-receipts.py` — PASS, one spec-fidelity defect (F2)

`find_receipts` replaces the ambient comprehension with a literal dict (`:313-321`) that keeps **all
seven** pre-existing values: `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_CONFIG_SYSTEM=/dev/null`, `HOME=<temp>/home`, `XDG_CONFIG_HOME=<home>/.config`,
`PATH=/usr/bin:/bin`, `GIT_CEILING_DIRECTORIES=dirname(abspath(temp_dir))`. The single spawn
(`:326-327`) is env-bound; no ambient read remains. **`LC_ALL=C` is not added** — the declaration's
fixed display lists `LC_ALL=C` as a member for each of the five; the other four have it (F2).

### 2.3 `tools/score-census-handoff-r32.py` — PASS; the two inheriting spawns are fixed

New `child_env()` (`:774-780`: `PATH`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=os.devnull`) is used at **all three** spawn sites: `:440` (`git archive` in
`export_census`), `:795` (live-check engine), `:852` (`git rev-parse HEAD` in `main`). **3/3
env-bound**; this closes the exact gap I flagged against the base (both git children previously
inherited the whole ambient environment). The filtered live view survives: `fenv = dict(env,
TSUKUROI_JOURNALCTL=wrapper)` at `:808`, so the fixed dict remains a plain extendable dict. The
fixture env `census_env` (`:454-483`) is untouched, as it should be — it was already a literal dict.

### 2.4 `tools/mutants-btrfs-space-r30.py` — PASS

Literal dict at `:362-367` (`PATH`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL`);
single spawn (`:368-369`) env-bound; no ambient read remains. The dict matches the round-34
canonical builder shape used by the child `check-btrfs-space-r30.py:95-98`, which is a good
consistency signal (M8).

### 2.5 `tools/run-receipt.py` — PASS, with a new value to disclose (F1/F3)

`env(home=None)` (`:36-47`) becomes a literal dict with `PATH`, `LC_ALL=C`,
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, plus
`HOME`/`XDG_CONFIG_HOME` when `home` is passed — and now also **`GIT_CEILING_DIRECTORIES =
dirname(abspath(home))`**. All six spawns stay env-bound: `:56`, `:85`, `:87`, `:90`, `:100`
(`env()`), `:107` (tool under receipt, `env(home)`). No ambient read remains.

Scope of the new ceiling: only `env(home)` carries it, and `env(home)` is used only for the child
tool (`:107`); the six git spawns use `env()`, so `resolve(lane, rev)`/`for-each-ref` are
**unaffected** — the breakage I warned about for lanes outside the ceiling does not occur. The
residual fact is that the ceiling is a **new child-env value** for tools under receipt.

## 3. Blocking findings

**F1 — the declaration misstates `GIT_CEILING_DIRECTORIES` as pre-existing in `run-receipt.py`.**
Declaration sentence: "retaining only each tool's existing run-private computed settings
(`HOME`/`XDG_CONFIG_HOME` to a private empty dir and `GIT_CEILING_DIRECTORIES` to the run's scratch
parent in `check-report-receipts.py` and `run-receipt.py`)". At the base, `grep
GIT_CEILING_DIRECTORIES` finds it only at `check-report-receipts.py:321`; the patch **introduces**
it in `run-receipt.py:47`. As written, the claim's "retained settings are the pre-existing fixed
values" is false for one of the five. The declaration is pre-freeze: reword it to "adds
`GIT_CEILING_DIRECTORIES` to the tool-child environment in `run-receipt.py`" (the intent is already
named there), or drop the value. No code change required if the text is corrected — the value is
harmless in the observed paths (see F3).

**B3 — the `livefive` per-target argv/mode mapping is still unestablished.** The r36 probe does not
exist yet, and the r34 probe docstring (`tools/probe-child-env-allowlist-r34.py:8-18`) records
three of these five as *excluded* from its own claim set for harness reasons:
`check-report-receipts --selftest` "starts no git child", `check-revision-binding --selftest`
"control run still unfinished after 45 minutes; the per-run limit is 1200 s",
`mutants-btrfs-space-r30` "(no mode starts git)"; `score-census-handoff-r32` and `run-receipt` have
no r34 entry at all. The declared after-condition requires `harness_errors` empty and before > 0 on
all five, so the probe must fix a per-target argv that starts traced children inside
`TIMEOUT = 1200` (`:189`) and measure it at the base. Candidate argv from the base-mode reading
(unverified, [inf] until ExecBeforeDesign/ExecC1Design measures them):
`check-revision-binding --tools-revision {rev}` (normal mode clones at `:861-863`, spawns at `:365`,
unlike `--selftest`); `check-report-receipts --report <report> --lane {clone} --revision {rev}`
(real mode reaches `find_receipts`; exit 1 when a citation is unreceipted);
`score-census-handoff-r32 --revision {rev} --lane {clone}`; `mutants-btrfs-space-r30` with no args
(full battery spawns one child per case); `run-receipt --revision {rev} --out <file> -- <tracked
tool> [args]` (`--out` is required).

## 4. Minor findings

- **F2 — `LC_ALL=C` missing from the `check-report-receipts` fixed dict.** The declaration's fixed
  display lists it for each of the five; this tool's dict lacks it. The probe has no LC_ALL clause,
  so the after-value cannot catch the omission. Cheap fix now (add it) or amend the declaration
  sentence — do one before the freeze.
- **F3 — new `GIT_CEILING_DIRECTORIES` value in `run-receipt.py`.** Applies only to the tool child
  (`env(home)`), never to run-receipt's own git calls; derived from `dirname(home)`, which equals
  the scratch parent in both branches (`/fast/scratch/hyaku` or the system temp dir). No observed
  gate introspection of this variable [inf]; disclose it in the change note as required by the
  "no behaviour change" claim if the declaration text is not amended (F1).
- **F4 — two zero-context hunks.** `@@ -440,1 +440,1 @@` and `@@ -771,1 +771,10 @@`: `git apply`
  needs `--unidiff-zero`; GNU `patch -p1` applies. The L1 should use one of these explicitly (and
  the applied tree should be byte-compared against the reconstruction check I ran).
- **M2 — the live census's host-tool discovery narrows to `/usr/bin:/bin`.** `tsukuroi-census.sh`
  probes optional tools with `have() { command -v "$1" … }` (`:548`; call sites `:619,:881,:952,
  :966,:1004,:1014,:1080,:1522,:1676,:1688`), so `/usr/local/bin` and `~/.local/bin` become
  invisible. All eight probed tools resolve under `/usr/bin` on this host [inf]. Bound it by
  diffing the after live view against the before live baseline (`ExecSelftestNoHarm/02-census-live.txt`,
  `TSUKUROI_CENSUS: DEGRADED … DRIFT pacnew-plane pacnew=3 …`).
- **M3 — `run-receipt` narrows its child contract.** A caller-supplied `TSUKUROI_*` (e.g. a census
  seam) used to reach the tool under receipt; it no longer does. No committed gate does this —
  round-30 gates sanitize only `GIT_*` (`.ufo/waves/round-30/w1/ExecGatesStart.md:3`) and the
  census gate "ran directly" — so no observed change; state the narrowing in the change note.
- **M7 — stub invariant in `check-revision-binding`.** The `STUB` text's `git()` inherits; it is
  safe only while every stub execution goes through `:365`/`:1114`. Keep both on the fixed dict.
- **M8 — consistency.** The new builders match the round-34 canonical shape
  (`check-btrfs-space-r30.py:95-98`) and use `os.devnull` (= `/dev/null` on POSIX) rather than a
  literal, so the declaration's `/dev/null` wording and the code agree in value.
- **M1 — `LC_ALL=C` is a new value in four tools** (score-census, mutants, run-receipt, and it is
  the declared add for check-report-receipts). Declared; an observable locale delta for children
  that format or sort (notably tools under receipt). No probe effect.

## 5. Criterion checks

1. **Every spawn path gets the fixed dict — PASS.** Applied tree: **zero** `os.environ`/`getenv`
   occurrences in the five files; spawn/env binding 6/6, 1/1, 3/3, 1/1, 6/6 (check-revision-binding's
   extra `subprocess.run` is the stub string).
2. **Retained settings exactly the pre-existing fixed values — PASS on the code, one text error.**
   Retained and verified in the applied bytes: check-revision-binding `GIT_OPTIONAL_LOCKS`/`GIT_PAGER`
   (`:109-110`); check-report-receipts `GIT_CONFIG_SYSTEM` (`:316`), `HOME`/`XDG_CONFIG_HOME`
   (`:317-318`), `GIT_CEILING_DIRECTORIES` (`:320`); run-receipt `GIT_CONFIG_SYSTEM` (`:43`) and
   conditional `HOME`/`XDG_CONFIG_HOME` (`:46`). No dropped protection; no new ambient dependence
   (no dict reads `os.environ`). F1 (declaration text) and F2 (LC_ALL) are the only gaps.
3. **No behaviour change — PASS.** Spawn/argv lines are identical base↔patched modulo line-number
   shift (`ARGV-IDENTICAL` for all five); control flow is unchanged (dict construction only; the
   `if home:` branch is kept); every pre-existing fixed value keeps its value. Declared additions:
   `PATH`, `LC_ALL` (except F2's omission), `GIT_CONFIG_SYSTEM` only where already present, and the
   run-receipt ceiling (F3).
4. **Scope — PASS.** Exactly the five declared files change; `diff -rq` against the base shows no
   other file.

## 6. What the after-value will see

For every git execve of all five targets the applied code supplies `GIT_CONFIG_NOSYSTEM=1` and
`GIT_CONFIG_GLOBAL=/dev/null`, satisfying the frozen amendment-2 clause (r34 probe `:101`,`:115-118`);
no fixed dict carries an ambient name, and the only path values are `/usr/bin:/bin`, a run-private
`HOME`/`XDG_CONFIG_HOME`, and a `GIT_CEILING_DIRECTORIES` derived from the run's own scratch dir.
`leaking_pairs` 0 on all five is therefore structurally plausible **conditional on B3** (a viable
per-target mode with `harness_errors` empty). The mutants target's grandchildren already spawn git
through the child tool's own round-34 fixed builder, which also carries both git settings.

## 7. Verdict

The patch **does what C1 declares** and is safe to land **after two pre-freeze conditions**:
(1) fix the declaration's `GIT_CEILING_DIRECTORIES` sentence (F1); (2) either add `LC_ALL=C` to
`check-report-receipts` or amend the declared display (F2). Apply with `patch -p1` or
`git apply --unidiff-zero` (F4) and pin sha256 `2287b83f…`. C1's after-state additionally requires
B3 resolved by the probe owner before any after-value is scored. No blocker found in the code
semantics: all 17 spawn sites are env-bound with a fixed dict, every pre-existing protection is
retained, and argv/control flow are unchanged.

Scope: read = SCORECARD.md Round-36 declaration and LOG.md entry at `6d76fb20`, the five tools at
`6d76fb20` and patched, `tools/check-btrfs-space-r30.py`, `tools/tsukuroi-census.sh`,
`tools/probe-child-env-allowlist-r34.py`, `.ufo/waves/round-36/w1-plan.json`, sibling captures
(`ExecBeforeDesign/harness-dry.jsonl`, `ExecSelftestNoHarm/*`), `.ufo/waves/round-30/w1/ExecGatesStart.md`;
wrote = this file, `ReviewC1Design/spawn-inventory.json`, `ReviewC1Design/patched-state.txt`;
executed = read-only `git archive/show/ls/status`, grep/sed/line reads, `git apply`/`patch` in
`/tmp` copies, `python3 -m py_compile`, `date -u`. No tool installed or updated. No production edit,
no git write.
