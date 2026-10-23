# SentinelAllowKeep — C2 design input: which ambient names may reach a child

Verdict: the candidate keep-list is not minimal and it admits three live injection channels
(HOME, LANGUAGE, TZ) and four behaviour channels (PATH, TMPDIR, TERM, LANG/LC_*) into git 2.56.0,
python 3.14 and bash 5.3 children; the frozen C2 counter scores the candidate keep-list
`leaking 0 of 11` with exit 0, so the counter cannot certify the keep-list and the lane must
justify it from source.  My recommendation is the empty ambient keep-list: every name the eleven
targets and `tools/check-owed-statements-r29.py` need is already set by the builder itself
(PATH, HOME, XDG_CONFIG_HOME, GIT_* contract), and LC_ALL=C should be added to the six builders
that lack it.

Scores I ran in the sandbox (frozen counter bytes, sha256 `2521711b…`, the declared probe):

| Variant (sandbox commit) | predicate `leaking` | exit |
|---|---|---|
| candidate keep-list {PATH,HOME,LANG,LANGUAGE,TZ,TMPDIR,USER,LOGNAME,TERM}+LC_* (2f90dbdb) | 0 of 11, `harness_errors` [], parity clean | 0 |
| no ambient names at all, `env = {}` (32374190) | 0 of 11, `harness_errors` [], parity clean | 0 |

Both receipts are in the seat directory: `probe-candidate-keeplist.jsonl` (sha256 `d3a750c1…`,
patch `candidate-keeplist.patch` sha256 `ab8b6287…`) and `probe-empty-ambient.jsonl`
(sha256 `099feaf1…`, patch `empty-ambient.patch` sha256 `207e69e1…`).  In both receipts all 11
(channel, target) rows have `reached` `{}`, `parity_diffs` `[]` and `channel_rc` 0, the smallest
git-child count is 116, and `harness_errors` is `[]`.  The first row is the point of this report:
the counter accepts the dangerous list exactly as happily as the empty one.

## 1. The counter is blind to the keep-list's contents (highest severity for this round) [obs]

`tools/probe-child-env-allowlist-r32.py:103-104` (at fe1ae02, sha256 `2521711b…`) sets
`EXCLUDED_PREFIX = ('LC_', 'GIT_', 'XDG_', 'LD_', 'PYTHON')` and
`EXCLUDED_EXACT = frozenset(('PATH','HOME','LANG','TZ','TMPDIR','USER','LOGNAME','TERM','SHELL','PWD','IFS'))`,
and `random_names()` (same file, 250-272) skips every such name when it draws the eight injected
names.  Those exclusions are exactly the candidate keep-list.  Consequence, measured: my sandbox
commit 2f90dbdb keeps all ten candidates from ambient and still reads `leaking` 0 of 11, exit 0
(`probe-candidate-keeplist.jsonl`, last line).  So a fix that keeps HOME, LANGUAGE and TZ passes
the frozen target without being tested for them — the C2 after-value proves only that ambient
names *outside* the excluded sets are dropped.

`LANGUAGE` is the single candidate that is in neither exclusion set, so it is the one member whose
leak the counter could see: a random drawn name would have to be exactly `LANGUAGE`
(probability about 8 × 52⁻¹ × 62⁻⁷ ≈ 4.6e-13 per run).  Keeping LANGUAGE therefore also adds a
collateral false-positive risk to the counter, on top of being a real channel (§3).

## 2. HOME — code execution in python children; must be set, never inherited [obs]

Device 1 (RCE): a python child started with an attacker-controlled HOME executes every `.pth`
line that begins with `import` from `$HOME/.local/lib/python3.14/site-packages`.  Sandbox:
`demos/home_canary.txt` contains `HOME_PTH_RAN`, written by
`fakehome/.local/lib/python3.14/site-packages/evil.pth` during `HOME=<fakehome> python3 -c pass`
(`demos/home-git-and-python.txt` records the same run).  `python3 -c 'import site; …'` with the
same HOME lists that site dir on `sys.path`.

Device 2 (git config): ambient HOME plus `$HOME/.gitconfig` reaches git unless
`GIT_CONFIG_GLOBAL` is set — `demos/home-git-and-python.txt`: `git config --get user.email`
returns `evil@example.invalid` with ambient HOME and rc=1 with `GIT_CONFIG_GLOBAL=/dev/null`;
ambient `XDG_CONFIG_HOME` behaves the same (`xdg@evil.invalid` vs rc=1).  Every builder already
sets `GIT_CONFIG_GLOBAL=os.devnull`, so this second device is closed today — but it is closed by
the GIT_* contract, not by HOME.

Device 3 (HOME unset is not isolation): with HOME unset python still resolves the user site dir
through the passwd entry — `env -u HOME python3 -c 'import site; print(site.getusersitepackages())'`
prints `/home/vgpnk/.local/lib/python3.14/site-packages`, `ENABLE_USER_SITE` True.  So dropping
HOME from the child env would not close device 1; HOME must be set to a private, empty directory.

Where ambient HOME survives a naive allow-list fix: `tools/check-owed-statements-r29.py:150-169`
(at fe1ae02) copies the ambient HOME and the ambient XDG_CONFIG_HOME into every child env
(`home = os.environ.get('HOME')`, then `env['HOME'] = home`, `env['XDG_CONFIG_HOME'] =
os.environ.get('XDG_CONFIG_HOME', …)`).  That is the one place in scope where HOME is not
overridden, and it is also the file reachable as a grandchild of the probe's
`mutants-owed-statements-r29*` targets.  Smallest remediation: give it a private HOME like the
other eleven builders (tempfile dir), and pin XDG_CONFIG_HOME under it.

Recommendation: HOME is a name the builder must *set* (private empty dir), never a name it copies.
My sandbox 2f90dbdb copies HOME but every builder overrides it, which is why it scores 0; that
safety is an ordering property, not an allow-list property.

## 3. LANGUAGE — path-naming channel into gettext catalogues [obs]

glibc gettext builds `<localedir>/<LANGUAGE>/LC_MESSAGES/<domain>.mo` and does not reject `..` in
the LANGUAGE list.  Sandbox, git 2.56.0:
`LANGUAGE=../../../../fast/scratch/…/evilcat git checkout` makes git
`openat(AT_FDCWD, "/usr/share/locale/../../../../fast/scratch/…/evilcat/LC_MESSAGES/git.mo", O_RDONLY)`
(`demos/lang.strace`, exit -1 ENOENT).  Two consequences: a child opens a file whose path an
ambient name composes, and a planted valid catalogue replaces git's message text — which matters
because `tools/check-freshness-r17.py:377-380` and `tools/check-self-assessment.py:188` put git
stderr into their verdicts.

`LANGUAGE` is neutralised when LC_ALL is C or POSIX: the same command with `LC_ALL=C` produced
zero opens of the traversed path (`demos/lang2.strace`, grep count 0).  Note LANG and the LC_*
names are *not* traversal channels — `LANG=../../..`, `LC_ALL=../../..`, `LC_MESSAGES=../../..` and
`LC_CTYPE=../../..` each produced 0 opens of the traversed path; glibc validates them as locale
names (only `LANG=xx_YY` shows the harmless `/usr/lib/locale/xx_YY/LC_CTYPE` lookup).

Recommendation: drop LANGUAGE; set LC_ALL=C in every builder.  LC_ALL=C also makes LANGUAGE inert,
which is the cheapest closure of this channel.

## 4. TZ — glibc opens the file TZ names, and dates change [obs]

`TZ=<absolute path>` makes glibc open and parse that file as a tzfile:
`env TZ=<seat>/dem/tzfile python3 -c 'import time; time.tzset()'` produced
`openat(AT_FDCWD, "<seat>/dem/tzfile", O_RDONLY|O_CLOEXEC) = 3` (`demos/tz.strace`).  This is an
attacker-chosen file open in every libc child.  TZ is also a behaviour channel for git:
`git log --date=local --format=%cd` gives `Fri Oct 23 02:03:54 2026` under `TZ=UTC` and
`Fri Oct 23 11:03:54 2026` under `TZ=Asia/Tokyo` (same unit, +9h), and `git --version` alone does
not read the file (`demos/gitz.strace`, 0 hits), so the channel fires only in children that touch
local time.  No target needs TZ: none of the twelve renders the current time or a local-time date
(`grep -c 'time\.time|datetime|strftime|localtime|--date'` is 0 in eleven of them;
`tools/check-owed-statements-r29.py:248-255` only parses ISO date strings out of the register,
without localising them), and the census pins its own comparisons.  Recommendation: drop TZ; if a fixed value is wanted for reproducibility, set
TZ=UTC explicitly (a fixed value, not an inherited one).

## 5. TMPDIR — steers where a child writes [obs]

`env TMPDIR=<attacker dir> python3 -c 'import tempfile; f=tempfile.NamedTemporaryFile()'` created
`<attacker dir>/tmpj_hjazqb`, and `tempfile.mkdtemp()` created `<attacker dir>/tmpqkc6ydny`
(`demos/tmp.strace`, `demos/tmp2.strace`, two opens each).  A child that writes scratch files does
so in a directory the ambient environment chose — pre-created files and symlinks are then a
child-side write hazard.  No target needs an ambient TMPDIR: the twelve builders create their own
directories with `tempfile.mkdtemp`/`TemporaryDirectory` in the parent process, and children that
need scratch (git, python) fall back to `/tmp` when TMPDIR is absent.  Recommendation: drop TMPDIR
from the inherited set; each builder that wants hermetic scratch should set TMPDIR to the private
directory it already creates (e.g. the `temp_dir` argument of the `git_env(temp_dir)` builders).

## 6. PATH — binary selection; must be pinned, never inherited [obs]

Ambient PATH decides which `git` runs: with `PATH=<roguebin>:/usr/bin:/bin` the child executed
`execve("<seat>/dem/roguebin/git", ["git","--version"], …) = 0` and printed `ROGUE_GIT_RAN`
(`demos/path.strace`).  All twelve builders already set `PATH: '/usr/bin:/bin'` after the copy
(e.g. `tools/check-adjacency-overlap.py:221` at fe1ae02), so the ambient value is dead today —
again an ordering property.  Recommendation: PATH stays out of the inherited set; the pinned
literal stays.  A keep-list that "keeps PATH from ambient" is a regression waiting for one
reordered line.

## 7. LANG and LC_* — behaviour channels; six of twelve builders do not pin LC_ALL [obs]

LC_COLLATE changes ordering: `printf 'a\nB\n' | LC_ALL=C sort` gives `B a`, the same input under
`env -u LC_ALL LANG=en_US.UTF-8 sort` gives `a B`; `LC_ALL=C` overrides `LC_COLLATE=en_US.UTF-8`
(`B a`).  LC_MESSAGES/LANGUAGE select the message catalogue (§3).  So an inherited LANG/LC_* makes
child output host-dependent.  At fe1ae02 the builders that do **not** set LC_ALL=C in their child
env are: `tools/check-adjacency-overlap.py` (git_env, 213-224), `tools/check-freshness-r17.py`
(git_env 329-341; LC_ALL only in git_in/revision_call), `tools/mutants-adjacency-overlap.py`
(19-26), `tools/mutants-kernel-taint.py` (33-40), `tools/mutants-owed-statements-r29.py` (36-48),
`tools/mutants-owed-statements-r29-landed.py` (35-47).  The other six set it
(check-kernel-taint.py:263, check-memory-pressure.py:117, check-registry-coverage.py:42,
check-storage-health.py:74, check-self-assessment.py:105, check-owed-statements-r29.py:164).
Recommendation: drop LANG, LANGUAGE and the LC_* family from the inherited set and add
`LC_ALL: 'C'` to the six builders above.  The three-place census logic already uses
`LC_ALL=C sort`/`env LC_ALL=C stat` (`tools/tsukuroi-census.sh:765,774,1069,1901`), so C locale is
the lane's own convention.

## 8. USER and LOGNAME — weak behaviour channel, not needed [obs]

python's `getpass.getuser()` honours them: `LOGNAME=eviluser python3 -c 'import getpass; print(getpass.getuser())'`
printed `eviluser`.  git does not use them for identity: `git var GIT_AUTHOR_IDENT` was unchanged
by `USER=eviluser`/`LOGNAME=evillogname`, and the failure message with an empty HOME reported the
passwd entry (`got 'vgpnk@plazir27.(none)'`).  No tool in scope calls getpass, and every fixture
commit passes `-c user.name=… -c user.email=…` explicitly (check-kernel-taint.py:1026-1028,
check-memory-pressure.py:911-913, check-storage-health.py:1001-1003,
check-registry-coverage.py:481-483, check-self-assessment.py:1024-1025,
mutants-owed-statements-r29.py:63-64).  Recommendation: drop both.

## 9. TERM — terminfo file selection, not needed [obs]

`TERM=xterm-256color python3 -c 'import curses; curses.setupterm()'` produced
`openat(AT_FDCWD, "/usr/share/terminfo/./x/xterm-256color", O_RDONLY) = 3` (`demos/term2.strace`);
`TERM=../../../../etc/passwd` is rejected by ncurses (setupterm error, no traversal open).  So TERM
selects a terminfo entry but does not compose an arbitrary path.  None of the twelve children is a
curses program; git is run with `--no-pager`/`GIT_PAGER=cat` and stdout is a pipe, and bash
non-interactive does not consult terminfo.  Recommendation: drop TERM.

## 10. The four named injections are live at the base, and the allow-list closes them [obs]

`BASH_ENV` is a real code-execution channel for this lane, because
`tools/check-self-assessment.py:186-188` runs `bash tools/tsukuroi-census.sh --selftest` with
`env=git_env()`, and the base builder copies ambient names.  Sandbox:
`env BASH_ENV=<seat>/be/bashenv.sh python3 tools/check-self-assessment.py --selftest` in a pristine
clone of fe1ae02 wrote three `CENSUS_BASH_ENV_RAN marker=…` lines (`demos/bashenv-canary.log`),
while the same command in the candidate-keep-list clone wrote none and produced a byte-identical
selftest output (both `.out` files sha256 `35e28764…`).  `GCONV_PATH` is a module-load path for
glibc: `GCONV_PATH=<dir>` makes `iconv_open` look for `<dir>/gconv-modules` first
(`demos/gconv.strace`), i.e. an ambient name selects shared objects.  `ENV` is the sh analogue of
BASH_ENV and `PERL5OPT` injects perl options.  All four are excluded by an allow-list by
construction; none is on the candidate list.

## 11. Minimal keep-list, recommended

Copy nothing from ambient.  Build each child env from builder-owned constants:

- `PATH = '/usr/bin:/bin'` (already in all twelve; needed to find `git`, and `bash` for the census child);
- `HOME = <private empty dir>` (needed to suppress python's user-site `.pth` channel and to keep git
  off `$HOME/.gitconfig`; `check-owed-statements-r29.py` must stop reading `os.environ['HOME']`).
  QUALITY 78 already requires "pointing `HOME` at a private empty dir", so this is the existing
  contract, not a new one;
- `XDG_CONFIG_HOME = <private home>/.config` (already in eleven; `check-owed-statements-r29.py` must
  stop reading the ambient value);
- `LC_ALL = 'C'` (add to the six builders listed in §7);
- the builder's GIT_* contract exactly as today (GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null,
  GIT_CONFIG_SYSTEM=/dev/null, GIT_CEILING_DIRECTORIES, GIT_OPTIONAL_LOCKS=0, GIT_PAGER=cat,
  GIT_NO_REPLACE_OBJECTS, GIT_TERMINAL_PROMPT=0 where present) — the GIT_* names are set, never inherited;
- optionally `TMPDIR = <same private dir>` and `TZ = 'UTC'` as fixed values if deterministic dates
  or hermetic scratch are wanted.

That is an allow-list of *names the builder sets*, with an empty set of *names copied from
ambient*.  Both sandbox variants score 0 of 11, so the empty set costs nothing against the counter
and removes every channel above.

## 12. Limits of this report [obs]/[unk]

- [obs] The receipts above were produced with the declared frozen probe bytes (`2521711b…`, fe1ae02).
  They are plain probe output, not `tools/run-receipt.py` form, so under QUALITY 73/77 they are
  development/design evidence and not a measured claim value; the data wave must re-issue any
  scored variant through `run-receipt.py`.
  The lane working tree at HEAD 462e40a holds a v2 probe (`d43f95e…`, amendments 44c8eee) whose
  random-name lengths are 2-200; the same exclusions are present at `tools/probe-child-env-allowlist-r32.py:103-104`
  in that file, so the blindness in §1 is unchanged by the amendment.
- [obs] Both scored variants passed control A and B with rc 0 and at least 116 git children per
  target, and no parity diffs, so the empty keep-list does not break the eleven targets.  The
  self-assessment selftest output is byte-identical between base and allow-list
  (sha256 `35e28764…`).
- [unk] I did not exhaustively test every consumer of these envs outside the eleven targets; other
  lane tools that import `tools/_revision.py` inherit its `clean_env()` (which filters only `GIT_`;
  `tools/_revision.py:62-66`), and that file is outside the C2 declared surface.  If a later wave
  widens C2 to `_revision.py`, it needs the same treatment, because `BASH_ENV`/`GCONV_PATH` reach a
  child through it unchanged.
- [obs] My role text carries a `resume_continuity_v1` zero-mutation clause; this lane has no such
  predicate (`grep -r resume_continuity` finds only a round-23 lesson reference at
  `.ufo/waves/round-23/build/Review23Receipts.md:288`), and C2's surface is an env dict, so there
  is no rejection path to verify here.  No host state was mutated by this seat.

Scope: read=SCORECARD round-32 declaration at fe1ae02, hyaku addendum §9, corpus/QUALITY.md 70-82, round-31/round-30 spot-checks, the 12 env builders at fe1ae02, tools/probe-child-env-allowlist-r32.py (fe1ae02 and HEAD), tools/_revision.py, tools/tsukuroi-census.sh; wrote=.ufo/waves/round-32/w1/SentinelAllowKeep.md and .ufo/waves/round-32/w1/SentinelAllowKeep/ (two probe receipts, two patches, demos/); executed=cd /fast/scratch/hyaku/tsukuroi-r32/SentinelAllowKeep (git clone x3, git checkout/commit in my own clones only), python3 probe-child-env-allowlist-r32.py (frozen bytes) twice, strace runs in /fast/scratch, python3/bash/git version checks, the demo commands quoted above
Model: not exposed
Installs: none
