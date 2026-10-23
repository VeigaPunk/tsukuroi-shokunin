# ConnSiblingOverlap — round 34 w1

Verdict: sibling scan complete; no hit contradicts C1 or C2. Mori and tabi already use fixed child-process environments, which supports C1 as precedent rather than refuting it; mori's signal-11 coredump classification is adjacent ownership, not a duplicate of tsukuroi's journal-entry count.

## Findings

1. Mori already uses a fixed allow-list for git child processes.
   - Repo/commit: `mori-shokunin` @ `f2d28711ee723c969b6c2008d32df498192f9e7b`
   - Path:line: `tools/mori-freeze-order.py:17,28-36`
   - Quote: "`_ENV_ALLOWLIST = (\"PATH\", \"LANG\", \"LC_ALL\", \"LC_CTYPE\", \"TZ\")`"; "`env = {name: os.environ[name] for name in _ENV_ALLOWLIST if name in os.environ}`"
   - Relation to C1: does not contradict; it is prior art for a fixed allow-list. It does not duplicate C1 because it is a different lane/tool set.

2. Tabi uses a fixed environment for git child processes.
   - Repo/commit: `tabi-shokunin` @ `e3cf4e0d30bb835532ff44b118c5ad52e09eb76d`
   - Path:line: `scripts/check-round-contract.mjs:67-77`
   - Quote: "`const env = { GIT_CONFIG_NOSYSTEM: '1', GIT_CONFIG_GLOBAL: '/dev/null', ... TZ: 'UTC' };`", with "`if (process.env.PATH !== undefined) env.PATH = ...`"
   - Relation to C1: supports the same pattern in JavaScript; not a duplicate of the nine Python tools.

3. Kama uses a fixed child environment for a non-git subprocess.
   - Repo/commit: `kama-shokunin` @ `75b78bb`
   - Path:line: `tools/kama-context-capacity.py:64,300-303`
   - Quote: "`CHILD_ENV_KEYS = ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR')`"; "`child_env = {key: os.environ[key] for key in CHILD_ENV_KEYS if key in os.environ}`"
   - Relation to C1: adjacent precedent only; it is not a git child environment.

4. Souji strips six repository-selecting variables but is not a fixed allow-list.
   - Repo/commit: `souji-shokunin` @ `4edb25dfe262515d0da63224bbba71e02e36cba5`
   - Path:line: `tools/souji-landing-gate.py:169-185`
   - Quote: "`GIT_ENV = { k: v for k, v in os.environ.items() if k not in (\"GIT_DIR\", \"GIT_WORK_TREE\", \"GIT_INDEX_FILE\", \"GIT_OBJECT_DIRECTORY\", \"GIT_ALTERNATE_OBJECT_DIRECTORIES\", \"GIT_COMMON_DIR\") }`"
   - Relation to C1: closer to tsukuroi's current minus-`GIT_*` behavior than to the requested fixed allow-list; no contradiction.

5. Mori owns signal-11 coredump classification via a systemd-coredump journal message ID.
   - Repo/commit: `mori-shokunin` @ `f2d28711ee723c969b6c2008d32df498192f9e7b`
   - Path:line: `PROVINCE.md:8,24`; `tools/mori-census.sh:1076`
   - Quote: "`kill/OOM-related catalog-ID records and signal-11 coredump records`"; "`JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1`"
   - Relation to C2: adjacent, not duplicate. Mori classifies by crash cause; tsukuroi's C2 must remain a count of its own journal arm and ADJ-04 handoff value, with no crash-cause classification.

6. Audio counts coredumps with coredumpctl rather than journal entries.
   - Repo/commit: `audio-shokunin` @ `7a2fcd4f08831154686e4e323031f41fffdb077f`
   - Path:line: `corpus/live/r86-boundary/r86b_probe.py:596,632,760`
   - Quote: "`r[\"core_count_before\"] = sh(\"coredumpctl list --no-pager 2>/dev/null | wc -l\")`"
   - Relation to C2: different unit (`coredumpctl`), so it does not duplicate tsukuroi's `systemd-coredump` journal-entry count.

Scope: read=git tips and targeted git grep across sibling lane repos; wrote=.ufo/waves/round-34/w1/ConnSiblingOverlap.md; executed=git log/grep/sed only.
Model: not exposed.
Installs: none.
