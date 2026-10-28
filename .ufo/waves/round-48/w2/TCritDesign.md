VERDICT: defect-found

Seat TCritDesign, C1-R3 (design attack on the /proc/self/fd TMPDIR alias, item: alternatives, trust surface, classification correctness, /proc dependency). All paths below are at freeze ae99f021b76f8eb1c8805d32d80644464afb1ff6; line numbers refer to tools/tsukuroi-census.sh extracted to my scratch (identical bytes, sha256 375aa737... confirmed by the declaration). Receipts: .ufo/waves/round-48/w2/TCritDesign/{fn.sh,probe.sh,rel.out,rel.err}.

# Strongest argument FOR the chosen design

It is the only alternative that (a) never writes outside TMPDIR, (b) is race-free, and (c) preserves the "fixture tree lands inside the caller's TMPDIR" contract under every character set. The alias is a *string-level* laundering: `/proc/self/fd/240` is a canonical, whitespace-free, `=`-free path that the kernel guarantees resolves to the directory the fd is open on. Directory fds are not closed by O_CLOEXEC-relevant mechanics and are inherited by all selftest children, so `TSUKUROI_ROOT_DIR=/proc/self/fd/240/...` resolves inside TMPDIR in every child process without the child needing to know the real name. The high band 240-249 avoids the observed collision with `exec 10<...` fixture children and stays below bash's own script-descriptor band (255) (L2063-2070). This is strictly better than alternative (i) (a symlink inside TMPDIR is a write outside the fixture tree the caller must tolerate, is racy with a same-name attacker, and dies if TMPDIR is read-only-but-describable), better than (iii) (`cd "$TMPDIR"` + relative base *cannot* work at all — every fixture root is handed to root_locator_class which classifies non-`/` paths 'relative', so the fixture override itself would be refused; verified empirically below), and better than (iv) (making the classifier accept a spaced path is exactly the token-forgery hole the charset exists to close, L851-863 comment: "`=` and whitespace are rejected so a path like `/x root_mode=0755` can neither forge a token nor reach stat"). The round-47 `st_base=/tmp` fallback (baseline 5fdf062 L2055-2058) was the actual wrongness; removing it was mandatory, and between the two surviving candidates — (ii) fail fast and the fd alias — the alias is the less surprising *behaviorally* (caller's TMPDIR honored, all 166 cases still run, nothing silently skipped) while (ii) is the less surprising *mechanism* (no /proc trickery). For a selftest whose job is to exercise every verdict arm, refusing to run on a spaced TMPDIR would hide exactly the class of environment bug the selftest exists to catch, so the alias is the right trade.

# Does /proc/self/fd/N classify 'absolute' for the RIGHT reason?

Yes. root_locator_class (L851-863) is a *syntax gate*, not a semantic gate: `case "$1" in /*)` then a charset check `[!A-Za-z0-9._/+-]`. It answers "may this string be stat'd and echoed without forging a `key=val` token or smuggling a second argument," not "is this a trustworthy directory." `/proc/self/fd/240` contains only `/`, letters, digits — it passes for the same reason `/tmp/x` does, and produces the same observable behavior in probe_root_meta: `stat -L` resolves the kernel symlink to TMPDIR, `stat -c %F` reports `directory`. The trust surface is NOT widened: the override path that reaches `stat` is caller data in both cases; the alias only laundered the *spelling* of TMPDIR inside a process the operator already controls. A spaced TMPDIR is no more hostile than a clean one — both are writable by the operator who ran the selftest. What the classifier still protects (live census arm): an *attacker-influenced* TSUKUROI_ROOT_DIR string — that surface is unchanged because the classifier's rule did not change; only the selftest's internal base string got a conforming spelling. Countercheck run: `TSUKUROI_ROOT_DIR=/proc/self/fd/N` was already 'absolute' and stat'able before this change — the alias widens *nothing* the caller couldn't already do by naming /proc paths directly.

# /proc dependency acceptable on this host class?

Yes. The script already hard-requires procfs: `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}` (L492) and the R46 --identity arm re-opens the script bytes through `/proc/$$/fd/<n>` and reads `/proc/$$/fdinfo/<n>` (L3568-3578). A chroot/container without /proc makes the dirty-TMPDIR branch fail with the explicit message (L2101-2104 "selftest: TMPDIR <x> cannot host the fixture tree (no /tmp fallback, R48-C2)"), while a clean TMPDIR still runs — graceful, not a new hard dependency. Non-Linux: already unportable for the same reasons.

# Empirical probing of selftest_base_dir edge cases

Extracted L2058-2090 (fn.sh) and drove 12 cases in subshells (probe.sh), each `cd`'d to scratch, results:

| TMPDIR | result |
|---|---|
| absolute clean | rc=0 base=path fd= (clean path) |
| `rel` (relative, exists) | rc=0 **base=rel** — see defect |
| `rel/` | rc=0 base=rel/ |
| absolute + space | rc=0 base=/proc/self/fd/240, readlink -f lands inside the real dir |
| `=` / newline / `:` in name | rc=0 fd alias each time |
| `sp ace` (relative+dirty) | rc=0 fd alias bound to rel dir — *works* because fd alias is absolute |
| trailing `/`, `//` | rc=0 clean path (trailing slashes tolerated; fixture roots become `...//fx/...` which still classify absolute — cosmetics only) |
| unset/empty | rc=0 base=/tmp (declared contract) |
| `/proc/self/fd/0` (fd0=/dev/null) | rc=0 base=/proc/self/fd/0 → mktemp would fail under `set -e` (L452) → abort. Acceptable fail-fast, slightly cryptic. |
| `sp ace/../rel` (dirty + dotdot) | rc=0 fd alias → canonical = rel dir. Correct. |
| nonexistent clean TMPDIR | rc=0 base=path → mktemp fails → `set -e` abort (silent-ish). Counter only covers nonexistent *dirty* (failfast_ok=2). Behavior: still fails, never /tmp — contract preserved, message missing. |

# DEFECT (real, out-of-C1-scope but worth the L1's restatement): relative TMPDIR mass-fails

`selftest_base_dir` only reroutes the *dirty* branch; a charset-clean **relative** TMPDIR (`TMPDIR=relt`, or from a chdir'd caller) returns `ST_BASE_DIR=rel` unchanged. `mktemp -d rel/tsukuroi-...` succeeds relative to cwd, then every fixture root (`rel/.../fx/<case>/root`) classifies **relative** → `root_status=unavailable(override=relative)` → packages BLOCKED → exit 2. Observed (receipt rel.out/rel.err): `TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 14 passed, 152 failed)`; also 34 "configured root not asserted at a field boundary ... possible live-root read" harness aborts — the failure report is maximally misleading (reads like a live-root leak, is actually a TMPDIR spelling issue). It is a *safe* failure — never writes outside the intended tree, never /tmp — but a caller who follows common usage (`TMPDIR=tmp/ ./tsukuroi-census.sh --selftest`) gets 152 red lines and no hint why. Baseline had the same bug silently masked (relative TMPDIR stayed relative but fixtures still classified relative → identical failure; so this is pre-existing, not a regression, but the R48 rewrite was the natural place to fix it).

Smallest safe correction — route relative TMPDIR through the same fd alias (two-line change in selftest_base_dir, L2074-2087): change the dirty-branch match from `*[!A-Za-z0-9._/+-]*)` to `*[!A-Za-z0-9._/+-]* | [!/]*)` (or equivalently `case "$base" in /*[!A-Za-z0-9._/+-]*)|!(/*) ;; /*) ST_BASE_DIR=$base ;; *) <fd-alias branch> ;; esac`). A relative dir opened `exec 240<"$base"` yields `/proc/self/fd/240` — absolute, canonical, cwd-independent — and simultaneously hardens the edge where the fixture tree would otherwise be built relative to whatever cwd the caller happened to have. Alternatively fail fast on `[!/]*` with a printed message if the L1 prefers no behavioral widening; both beat the current 152-red-line outcome. NOT a C1-claim breach: the frozen predicate names only the four TMPDIR legs, all absolute.

# Minor observations (no correction needed)

1. ST_BASE_FD leak: the main-resolution fd is never closed (only the probe fd r48_fd is, L3549). Harmless — exit flushes it — and *required* for children (see "FOR"), but a one-word comment "fd intentionally survives; children resolve the alias" would preempt future "bug" reports.
2. Seven `drwx------` `tsukuroi-r3-2-selftest.*` dirs exist in real /tmp (timestamps 08:28–09:01 today, owner vgpnk). Not mine (my run's tree was `relt/...`, cleaned; verified `find relt -name 'tsukuroi*'` empty). Consistent with other seats' TERM'd runs where the r46-era trap existed — or pre-trap runs. Flagging for the L1 only; no defect in frozen bytes observed from this.
3. fd-band scan `[ -e /proc/self/fd/$fdn ]` correctly skips held descriptors; an exhausted 240-249 returns 1 → clean fail-fast message.
4. `eval "exec ${fdn}<\"\$base\""` — fdn is a fixed literal, `$base` is quoted inside eval; no injection path.

# Net judgment on the axes

- operability: alias keeps all 166 cases running under every declared leg — strongest for it; the relative-TMPDIR defect is the one real surprise found and is a *fail-noisily* never a *write-wrongly*.
- C1 claim scope: unaffected — the defect lies outside the four declared legs and the frozen predicate.
- design: the fd alias is the least-surprising of the candidates that keep TMPDIR honored; the only true rival (fail-fast, option ii) is simpler but forfeits coverage and would itself still need a fix for the relative-TMPDIR hole. Recommend the L1 apply the two-line reroute (or its fail-fast equivalent) in the end-of-round SCORECARD restatement pass.
