# Round 31 wave 1 — SentinelChildEnv

Verdict: **fails** — the C2 fix contract (`drop GIT_*, LD_*, PYTHON*`) closes the loader/interpreter
channels it names, but leaves the whole remaining ambient environment reaching every child of all
eleven tools: 38 of 38 tested non-dropped names reach a child in every tool. Two of them change what
a child does — `BASH_ENV` to arbitrary command execution *and* to a false tool verdict, `GCONV_PATH`
to a `dlopen` of an ambient-named module inside the git child — and the `EDITOR`/`VISUAL`/`PAGER`/
`LESSOPEN`/`SSH_ASKPASS` group reaches every child as a latent channel that today is blocked only by
the tools passing `-m` and never using an ssh transport. The contract should be an allow-list, not a
prefix deny-list.

All paths below are absolute. Measurements use the sandbox clone
`/fast/scratch/hyaku/tsukuroi-r31/SentinelChildEnv/repo` at `8cff9e7cfb034b49c645d548801ac3185a827cb4`
(the base tools), plus a second sandbox tree `.../postrepo` at sandbox commit
`3cb02686ae05f8575ba7badd98f31f64e029c0a4` where I applied the C2 fix contract myself
(`os.environ` copy filtered by `k.startswith(('GIT_', 'LD_', 'PYTHON'))`) so the "after the fix"
measurements are on post-fix tools, not the base ones. Harnesses and raw outputs are in this
directory and in `outputs/`.

## 1. The deny-list does not bound the surface: 38 of 38 non-dropped names reach every child — [obs]

`reach-r31.py` runs each of the frozen eleven targets twice under `strace -f -e trace=execve -v`
(control; one canary run setting one sentinel per candidate) and reads the environment block of
every descendant execve. Result over 11 tools × 38 candidates: **every tool reached all 38**
names, with parity preserved (exit code and normalised stdout digest equal the control) for 9 of 11.

```
command: python3 reach-r31.py --revision 8cff9e7cfb034b49c645d548801ac3185a827cb4 \
           --lane /fast/scratch/hyaku/tsukuroi-r31/SentinelChildEnv/repo
result:  reach.json — rows 11, each "reached=38"
         tools/check-adjacency-overlap.py       reached=38 parity_break=False children=['git']
         tools/check-self-assessment.py         reached=38 parity_break=False children=['bash', 'git']
         tools/mutants-owed-statements-r29.py   reached=38 parity_break=True  children=['git','git-upload-pack','python3','sh']
```

Confirmed against the **landed** wave-1 integration commit `13ca52d` (the L1 integrated while this
seat ran): exporting `13ca52d` read-only (`git archive 13ca52d | tar -x -C /fast/scratch/.../landed`)
and running its `tools/check-self-assessment.py --selftest` with an ambient `BASH_ENV` canary gives
`selftest rc=0` and **17 canary executions**; and the landed `git_env()` on that same tree returns
`BASH_ENV '/tmp/b'`, `GCONV_PATH '/tmp/g'`, `PERL5LIB '/tmp/pe'`, `EDITOR '/tmp/e'` while correctly
returning `None` for `PYTHONPATH` and `LD_PRELOAD`. So the finding is about the shipped fix, not
about my simulation of it. [obs]

Provenance, stated exactly: `reach.json` records `revision 8cff9e7…` (the base tools), and all 38
candidates are **outside** the contract's three drop prefixes (`python3 -c` over
`reach.json.candidates_tested` → `inside drop prefixes: []`, `outside (therefore survives the fix): 38`).
The fix only removes names in those prefixes, so this base-tree measurement *is* the post-fix reach
result for exactly this candidate set — no candidate's reach can change when `GIT_*`/`LD_*`/`PYTHON*`
are additionally dropped. I separately confirmed the post-fix behaviour directly on the patched tree
(§2: 17 bash children sourcing the canary; §3: gconv modules loaded; and a 35-of-36 single-tool reach
check on the patched tools). [obs]

Evidence pointer: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/SentinelChildEnv/reach.json`
and `outputs/measured-findings.txt`. The 38 names reached include `GCONV_PATH`, `MALLOC_TRACE`,
`MALLOC_CHECK_`, `MALLOC_PERTURB_`, `MALLOC_MMAP_THRESHOLD_`, `GLIBC_TUNABLES`, `BASH_ENV`, `ENV`,
`PERL5LIB`, `PERL5OPT`, `PERLLIB`, `EDITOR`, `VISUAL`, `PAGER`, `LESS`, `LESSOPEN`, `SSH_ASKPASS`,
`SSH_ASKPASS_REQUIRE`, `SSH_AUTH_SOCK`, `TMPDIR`, `LANG`, `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`,
`LC_CTYPE`, `LC_NUMERIC`, `LC_TIME`, `TZ`, `TERM`, `COLUMNS`, `LINES`, `HOSTALIASES`,
`RES_OPTIONS`, `LOCALDOMAIN`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`,
`XDG_RUNTIME_DIR`.

Why this is structural, not an accident of the test: every tool builds the child environment as
`{k: v for k, v in os.environ.items() if not k.startswith(<prefixes>)}` and there is **no other
filter**. So the deny-list's coverage is exactly the set of names whose *prefix* is enumerated.
The base filters are at (base clone) `tools/check-adjacency-overlap.py:214`,
`check-freshness-r17.py:330`, `check-kernel-taint.py:253`, `check-memory-pressure.py:107`,
`check-registry-coverage.py:30`, `check-storage-health.py:62`, `check-self-assessment.py:93`,
`mutants-adjacency-overlap.py:19`, `mutants-kernel-taint.py:33`,
`mutants-owed-statements-r29.py:36`, `mutants-owed-statements-r29-landed.py:35` — each a single
`startswith` test on `os.environ`. On this host's ambient environment 263 names exist and the
contract drops exactly 4 of them (`GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT`,
`PYTHONUNBUFFERED`); the other 259 are inherited by every child.

## 2. `BASH_ENV` reaches a bash child and is sourced: arbitrary command execution — [obs], severity high

`tools/check-self-assessment.py` spawns `bash tools/tsukuroi-census.sh --selftest`
(`tools/check-self-assessment.py:185-186`), and passes it `env=git_env()` — a copy of `os.environ`
that, post-fix, still carries `BASH_ENV`. Bash sources `$BASH_ENV` for **non-interactive** shells,
so the ambient value is executed inside the tool's own child.

Proof on the post-fix tree (`postrepo` at `3cb02686`):

```
command: BASH_ENV=$PWD/bashenv.canary python3 tools/check-self-assessment.py --selftest
result:  rc=0; bashenv.log has 17 lines "BASHENV-SOURCED pid=..."
         (control without BASH_ENV: file not created)
strace evidence: 17 × execve("/usr/bin/bash", ...) each carrying
         BASH_ENV=/fast/scratch/.../eff5/bashenv.canary in its env block
```

Evidence: `outputs/bashenv-probe-executions.log` (68 lines: the same canary firing during a single
run of the *frozen probe*), and the transcript in §2.1.

### 2.1 It also changes the tool's verdict — [obs], severity high

The census child's stdout is parsed by `re.search(r"\((\d+) cases", output)` and the **first**
match wins (`tools/check-self-assessment.py:188-190`). A `BASH_ENV` file that prints one fake PASS
line therefore controls the count the tool reports:

```
command: BASH_ENV=/fast/scratch/.../postrepo/hijack.canary python3 - <<'PY'
         ...m.census_case_count('/fast/scratch/hyaku/tsukuroi-r31/SentinelChildEnv/postrepo','HEAD')...
result:  control (no BASH_ENV) -> (97, "...FAIL blocked: C1 root arm survives empty-db early return...")
         with BASH_ENV          -> (999, "...FAIL blocked: ...")
         rc=0 in both cases
```

Evidence: `outputs/bashenv-hijack.txt`. The fake line is
`TSUKUROI_CENSUS_SELFTEST: PASS (999 cases, 999 passed, 0 failed)`. This is the substantive impact:
a tool that reports the operability axis can be made to report a number of the environment's
choosing, with no crash, no non-zero exit, and no change to any file it reads.

### 2.2 The frozen C2 probe cannot see it — [obs]

`tools/probe-git-child-env-r31.py` inspects only `LD_PRELOAD`/`LD_LIBRARY_PATH`/`PYTHONPATH`
`<inject>` paths (loader-env), the four git child-contract names, and the `.git` pointer canary.
`BASH_ENV` is invisible to all three channels. Run against the post-fix commit with `BASH_ENV` set
to the executing canary:

```
command: BASH_ENV=/fast/scratch/.../bashenv_probe.canary python3 repo/tools/probe-git-child-env-r31.py \
           --revision 3cb02686ae05f8575ba7badd98f31f64e029c0a4 --lane .../postrepo \
           --only tools/check-self-assessment.py
result:  {"leaking": 0, "leaking_pairs": [], "harness_errors": []}   exit 0
         ...while the BASH_ENV canary executed 68 times during that same run
```

Evidence: `outputs/bashenv-probe-executions.log`, `outputs/measured-findings.txt`. So C2 landing as
declared would certify "leaking 0 of 33" while this channel remains open. That is a correctness
defect in the claim, not only a hardening gap.

## 3. `GCONV_PATH` reaches a git child and glibc dlopens a module from it — [obs], severity high

glibc searches `$GCONV_PATH` for its charset-conversion module map and `.so` files, and git calls
`iconv` whenever it converts a commit message encoding — a code path the tools hit through plain
`git log`/`git show` on ordinary repository content. Measured on a git child:

```
control:  git --no-pager log -1 --format=%s  -> opens /usr/lib/gconv/ISO8859-1.so
with GCONV_PATH=/fast/scratch/.../gcW/mods (a dir holding gconv-modules mapping ISO-8859-1->ISO8859-1):
          openat("$GCONV_PATH/gconv-modules") = 3
          openat("$GCONV_PATH/ISO8859-1.so")  = 3        <- dlopened
          the module's __attribute__((constructor)) ran inside the git child
          (marker file written: pid=2054116)
```

And with a module that is only large enough to be loaded, the same three git-heavy tools abort:

```
command: GCONV_PATH=.../gcW/mods python3 tools/{check-adjacency-overlap,check-self-assessment,
         mutants-owed-statements-r29-landed}.py ...
result:  rc=134 (SIGABRT), 6 opens of $GCONV_PATH/gconv-modules, 3 opens of $GCONV_PATH/ISO8859-1.so
```

Evidence commands and traces reproduced in `outputs/measured-findings.txt`. `GCONV_PATH` is not
covered by `GIT_`/`LD_`/`PYTHON`, so the contract leaves it. This is a code-execution primitive,
not a mere inheritance observation: the module is `dlopen`ed from a path the ambient environment
names. ([inf] The escaping/construction specifics are the well-known gconv mechanism; I did not
build an offensive payload — the canary only writes a marker file.)

## 4. `EDITOR`, `VISUAL`, `PAGER`, `LESSOPEN`, `SSH_ASKPASS` reach children but did not fire here — [obs] reach, [obs] no observed effect

Every tool that commits passes `-m` (`-qm`, `-qam`, `commit -q -m`), so no editor is started; and
no tool runs an ssh transport, so no askpass helper is started. Measured:

```
command: EDITOR=$PWD/ed.canary VISUAL=... PAGER=... GIT_EDITOR=... GIT_PAGER=... \
           python3 tools/check-adjacency-overlap.py --selftest    # and check-registry-coverage.py
result:  rc=0, editor.log never created
```

Evidence: transcript in this session; `[obs]`. Reach is confirmed by §1 (all 38 names appear in
the children's env blocks). This is a latent channel: the guard is the tools' own `-m` today, not
the environment contract. `GIT_PAGER`/`GIT_EDITOR` *are* dropped; `EDITOR`/`VISUAL`/`PAGER` are not.

## 5. `TMPDIR`, locale, `MALLOC_*`, `PERL5*` reach children — [obs], with one observed behaviour change

- `TMPDIR`: reaches the child env of every tool, and separately steers the **tool's own**
  `tempfile.mkdtemp()` — `strace -e mkdir` shows 5131 `mkdir` calls under the ambient `TMPDIR`
  during one `check-adjacency-overlap.py --selftest`. The round-30/31 probes already model a
  TMPDIR `.git` pointer, so this is inherited surface rather than new, but the contract does not
  name it.
- Locale (`LANG`, `LANGUAGE`, `LC_*`): reaches git children and *does* change git's messages —
  measured `LANGUAGE=de git cat-file -p deadbeef…` emits `Schwerwiegend: Not a valid object name`
  where `LC_ALL=C` emits `fatal: …`. The tools that parse git stderr are protected only because
  they pin `LC_ALL=C` themselves (`tools/check-freshness-r17.py:345,358`,
  `check-kernel-taint.py:263`, `check-memory-pressure.py:117`, `check-registry-coverage.py:41`,
  `check-storage-health.py:73`, `check-self-assessment.py:105`). `tools/check-adjacency-overlap.py`
  does **not** pin it — but its git reads key on `returncode` only (`:235`), so no verdict moved in
  my runs: `LANGUAGE=de` left its stdout digest identical (`0c664f8b…` both). [obs]
- `MALLOC_PERTURB_`, `MALLOC_CHECK_`, `GLIBC_TUNABLES`: reach children; `MALLOC_PERTURB_` measured
  to change the *content* of freed memory (`after-free` differs with `MALLOC_PERTURB_=65`), which
  is a use-after-free amplifier rather than a channel on its own. No tool output changed in my
  runs. [obs]
- `MALLOC_TRACE`: glibc ignored it for a plain program and for git (no trace file appeared), so it
  reaches but had no observed effect on this host. [obs]
- `PERL5LIB`/`PERL5OPT`/`PERLLIB`: reach git children; git's Perl helpers (`git svn` etc.) are not
  invoked by any of the eleven tools, so no effect was observed. [obs]

## 6. Two "hollow" observations worth recording (they are negatives, not findings)

- **`ENV` is not equivalent to `BASH_ENV` here** — `grep -l '"bash"'` shows only
  `check-self-assessment.py` spawns bash; the two owed-statement batteries additionally spawn `sh`
  (visible as `sh` children in `reach.json`), and `sh` (dash) reads `$ENV` only in POSIX mode, so
  the effect was not demonstrated. [obs]
- **The two owed-statement batteries break parity under the canary run** (`parity_break=True`) in
  §1 — their clone of the lane is time-sensitive, so the digest differs run to run. I verified the
  cause: two control runs of `mutants-owed-statements-r29.py` also differ from each other
  (`14ccf105…` vs `d049c379…`), and after normalising commit hashes their rows are byte-identical
  (`differing rows: 0`). So that parity break is the tool's own nondeterminism, **not** an
  environment effect. [obs]

## 7. Recommendation: make the contract an allow-list

The deny-list cannot be completed by enumeration: `GCONV_PATH`, `BASH_ENV`, `ENV`, `EDITOR`,
`VISUAL`, `PAGER`, `LESSOPEN`, `SSH_ASKPASS`, `TMPDIR`, the `LC_*` family and the `MALLOC_*`
family are each an independent channel with its own semantics, and new ones appear with new glibc
and tool releases. A prefix list is a guess that must be re-guessed forever; an allow-list is a
bound that stays a bound.

Smallest remediation, in the tools' own env builders: replace the comprehension with an explicit
allow-list of the names the child genuinely needs — `PATH`, `HOME`, `XDG_CONFIG_HOME`, `TMPDIR`
(pointed at the tool's own scratch, not the ambient value), `LC_ALL=C`, `TZ`, plus the git
contract names the tools already set (`GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_SYSTEM`, `GIT_CEILING_DIRECTORIES`, `GIT_OPTIONAL_LOCKS`, `GIT_PAGER`,
`GIT_TERMINAL_PROMPT`, `GIT_NO_REPLACE_OBJECTS` where used). Everything else is dropped by default.
That closes §2, §3 and the latent channels in §4 in one change, and it makes the contract's
guarantee independent of this host's ambient environment. A minimal immediate step, if the
allow-list cannot land this round: add `BASH_ENV`, `ENV`, `GCONV_PATH`, `EDITOR`, `VISUAL`,
`PAGER`, `LESSOPEN`, `PERL5LIB`, `PERL5OPT`, `PERLLIB`, `SSH_ASKPASS` and the `MALLOC_*`/`GLIBC_*`
prefixes to the deny-list — but note this is the guess-that-must-be-re-guessed, and it does not
cover a name nobody thought of.

Either way the C2 predicate should gain a fourth channel (an ambient-name reach channel with a
`BASH_ENV`-class and a `GCONV_PATH`-class canary), because as frozen it certifies `leaking 0` while
§2.2 shows the canary executing.

## 8. Notes on method and limits

- Every tool run used the frozen probe's own `hermetic_env`/`parse_trace`/`TARGETS` (imported
  read-only), so the target set and argv are the frozen ones; I did not modify the probe or the
  counter.
- The reach measurement's canary values are inert by construction: paths point at private empty
  directories, locales at the installed `en_US.utf8`, `MALLOC_TRACE` at a path that glibc does not
  write. The only canaries that *do* something are §2's one-line `BASH_ENV` file and §3's
  marker-writing module, and both only append to a file under my scratch directory. No offensive
  automation was built or run.
- Scratch and sandbox: `/fast/scratch/hyaku/tsukuroi-r31/SentinelChildEnv/` (clone at `8cff9e7`,
  `postrepo` clone at `3cb02686`, experiment trees). The lane repo was never written; every git
  command was prefixed `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` and read-only apart
  from `add`/`commit` inside the sandbox clone `postrepo`, which is under `/fast/scratch` and is
  not the lane.
- Out of scope by my seat: I did not test the C1 counter (depth) or the btrfs claim, and I make no
  claim about C2's own 33 pairs beyond §2.2 (that the probe is blind to this channel).

## 9. Integration note for the L1 (no git write was run in the lane)

The L1 integrated wave 1 as `13ca52d` while this seat ran. That commit already contains an earlier
version of `probe-ambient-child-env-r31.py` at this seat path; I rewrote that file after the
integration (it broke on `PYTHONHOME` and reported no reach), so the lane working tree now shows
` M .ufo/waves/round-31/w1/SentinelChildEnv/probe-ambient-child-env-r31.py`. Everything else in this
seat directory is new and untracked: `reach-r31.py`, `effects-r31.py`, `reach.json`, `outputs/`, and
this report. Nothing outside this seat path was written; no `git`/`jj` write command was run in the
lane. Suggested integration: take `reach-r31.py` + `outputs/` as the evidence, and either drop the
superseded `probe-ambient-child-env-r31.py` or replace it with the working version now on disk.

Scope: read=Lane SCORECARD.md round-31 declaration, tools/probe-git-child-env-r31.py, the eleven target tools' env builders and git call sites, tools/tsukuroi-census.sh (shell structure); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/SentinelChildEnv/{probe-ambient-child-env-r31.py,reach-r31.py,effects-r31.py,reach.json,outputs/{reach-postfix-summary.txt,measured-findings.txt,bashenv-hijack.txt,bashenv-probe-executions.log,landed-13ca52d-bashenv-executions.log,landed-confirmation.txt,SHA256SUMS.txt},SentinelChildEnv.md}; executed=strace/gcc/git/python3 experiments and the two harnesses listed above, all confined to /fast/scratch/hyaku/tsukuroi-r31/SentinelChildEnv
Model: not exposed
Installs: none
