# Round 12 — Security seat: root-metadata path override (`TSUKUROI_ROOT_DIR`) and probe

Seat: `Security` (UFO-FSD sentinel). This is an author-side seat review, **not** independent
non-author verification. Scope: the C1 proposal in `spec.json` item `Census` (read `/`
metadata via `stat`; `TSUKUROI_ROOT_DIR` override, default `/`; BLOCKED for unavailable or
non-directory; named DEGRADED when the owner lacks write or search; selftest wiring and
fixtures). Reviewed against starting HEAD `b76b5c3` before any implementation: `git diff --stat`
was empty when this review ran, so this file reviews the **proposal and its integration
points**, not landed code. Re-review is needed once Census lands.

Installs/updates: **none**.
Host writes: none outside a user-owned `mktemp -d /tmp/tsukuroi-sec-r12.XXXXXX` scratch
directory, which is the selftest's own `/tmp` convention. All four scratch directories were
removed, and each run printed `cleaned`. No sudo, no package operations, no environment dump,
no argv or credential reads. Stat targets were only `/`, `/bin`, `/tmp`, `/proc/version`,
nonexistent paths, `/root/x` (expected to fail with EACCES) and the scratch directories.

## Verdict

The proposal is **safe to land only with the boundary in §4**. As written, it has no inherent
command-injection or secret-read path. It does leave six concrete ways to get a wrong
verdict: one false-pass/forgery path, one hermeticity hole, one locale false-BLOCKED, one
symlink ambiguity, one selftest self-abort, and one root-run inversion if the gate uses
access tests. No PASS is claimed. The implementation is unrun and unreviewed.

## 1. Commands run (author-side, read-only unless noted)

| # | Command (sanitized) | Exit | Observation |
|---|---|---|---|
| P1 | `/usr/bin/stat -c 'a=%a f=%f u=%u g=%g F=%F A=%A' -- /` | 0 | `a=555 f=416d u=0 g=0 F=directory A=dr-xr-xr-x` |
| P2 | `/usr/bin/stat -c 'a=%a F=%F' -- /bin` ; `… -- /bin/` | 0 ; 0 | `a=777 F=symbolic link` ; `a=755 F=directory` (trailing slash follows the link) |
| P3 | `[ -d /bin ]` ; `[ -L /bin ]` | 0 ; 0 | `test -d` follows the symlink while `stat` does not, so the two disagree |
| P4 | `/usr/bin/stat -c 'a=%a f=%f' -- /tmp` | 0 | `a=1777 f=43ff` (`%a` is 4 digits when the sticky, setuid or setgid bit is set) |
| P5 | `/usr/bin/stat -c %a -- /root/x` ; `/proc/version/x` ; `/nonexistent-tsk` | 1 ; 1 ; 1 | stderr `…: Permission denied` / `Not a directory` / `No such file or directory`; **the stderr text contains the path** |
| P6 | `/usr/bin/stat -c %a -L /` (no `--`) | 0 | `555`: a leading-dash operand is parsed as an option |
| P7 | `LANGUAGE=de LC_ALL=en_US.UTF-8 /usr/bin/stat -c F=%F -- / /bin /proc/version` | 0 | `F=Verzeichnis`, `F=symbolische Verknüpfung`, `F=reguläre leere Datei` (**`%F` is localized**); the same call with `LC_ALL=C` prints `F=directory` |
| P8 | `stat --version` in this harness shell ; `type -a stat` ; clean `env bash --norc -c 'type -a stat'` | 0 | harness: `stat is a shell builtin`, `stat 0.8.0`; clean bash: `/usr/bin/stat`, owned by `coreutils 9.11-2`; the harness builtin `stat -c %a -- ''` printed `755` rc=0 (the cwd's mode), while GNU `stat -- ''` gives `cannot statx ''` rc=1 |
| P9 | scratch (write, `/tmp`): empty `chmod 000` parent, then `/usr/bin/stat -- <W>/locked/root` | 1 | `Permission denied`; `rm -rf` of an **empty** 000 dir succeeds (rc 0, cleaned) |
| P10 | scratch: 000 dir **inside** the hashed tree, with the selftest's own `fx_hash` under `set -euo pipefail` | 1 | `find: '<W>/fx/locked': Permission denied`; the harness aborts before `echo reached` |
| P11 | scratch: `rm -rf` of a **non-empty** 000 dir | 1 | `cannot remove '<W>/locked': Permission denied`; residue persisted until a manual `chmod` |
| P12 | scratch: `rm -rf` of an empty 0555 dir | 0 | removed |
| P13 | in-memory string: forged `\nTSUKUROI_CENSUS: HEALTHY (` inside a PLANE note, piped to `grep '^TSUKUROI_CENSUS:' \| head -n1` and to `check()`'s verdict regex | 0 | consumer sees `TSUKUROI_CENSUS: HEALTHY (forged)`; the `check()` HEALTHY regex matches |
| P14 | `bash -c` with `m='x[$(echo ARITH-EXEC >&2)]'`: `$((m))` ; `[[ $m -lt 1 ]]` ; `[ "$m" -lt 1 ]` | 2 | first two print `ARITH-EXEC` (the substitution executed); `[` rejects with `integer expected` |
| P15 | `env A=base A=case bash -c 'echo $A'` | 0 | `A=case`: the later assignment wins, so `EXTRA_ENV` placed after the base list overrides per case |
| P16 | `[ -w / ]`, `[ -x / ]` as uid 1000 | 1 ; 0 | a non-root `-w /` is false on any root-owned `/`, whatever the mode |
| P17 | `man 5 acl` lines 80-84, 124-132 | 0 | "the owner permissions correspond to the permissions of the ACL_USER_OBJ entry"; owner access uses `ACL_USER_OBJ` |

Code anchors (HEAD `b76b5c3`, `tools/tsukuroi-census.sh`): `umask 077` :321; probe-surface
overrides :327-355; `cap()` runs `"$@"` with no shell re-evaluation :456-461; packages early
returns overwrite `PKG_NOTE` at :536, :541, :549, :556; selftest `mktemp`/`trap rm -rf`
:1573-1574; `fx_hash` (`find … | sort | sha256sum`) :1748; `check()` is `env` **without `-i`**
and has no root var in its base list :1763-1788; the only hermeticity tripwire is
`host=fixture-host` :1793; output is `printf 'PLANE …: %s (%s)\n'` :2377-2382, then the verdict
line :2392.

## 2. Findings

| ID | Severity | Exploit / failure path | Evidence | Impact | Smallest remediation |
|---|---|---|---|---|---|
| S1 | **High** (false-pass) | `check()` inherits the caller's environment (`env` without `-i`, :1763). If `TSUKUROI_ROOT_DIR` is not in the base list, every selftest case stats the **host `/`**. On this host (`555`, P1) that makes each healthy case DEGRADED. After an operator `chmod 755 /`, the same suite passes against host state. The `host=fixture-host` tripwire (:1793) cannot see this leak. | :1763-1788, :1793; P1 | The selftest becomes host-dependent and silently non-hermetic, against the header claim at :293-295 | Add `TSUKUROI_ROOT_DIR="$FX/root"` (explicit `chmod 0755`) to the `check()` base list, before `"${EXTRA_ENV[@]}"` so cases can override it (P15). Add a tripwire: every `check()` asserts `root_src=override` in the output, like the hostname check. |
| S2 | **High** (forgery) | If the note echoes the override path or any `stat` stderr, which contains the path (P5), a value carrying `\nTSUKUROI_CENSUS: HEALTHY (` puts a verdict line before the real one (:2377 prints notes before :2392). Consumers that use `grep '^TSUKUROI_CENSUS:' \| head -n1` and the selftest verdict regex accept it (P13). | P5, P13; :2377-2392 | A fabricated HEALTHY verdict. The trust model is env-trusted, but a stale or crafted export reaches every downstream log reader. | Never print the path or `CAP_OUT`. Emit only fixed tokens: `root_src=default\|override`, `root_mode=<validated octal>`, `root_uid=<digits>`, `root_gid=<digits>`, `root_meta=<fixed class>`. Same stance as the existing `base_state=file(N)`, which never prints the baseline path (:600). |
| S3 | **Medium** (false-pass in live mode) | A stale exported `TSUKUROI_ROOT_DIR` (for example, left over from a fixture session) makes the **live** census report a 0755 fixture dir as `/`. On this 0555 host, that hides the exact C1 finding. | :327-355 (all overrides are live-honoured); P1 | Fabricated readiness for the one claim C1 is about | The `root_src=override` token from S2 makes it visible in every PLANE line. No new policy is needed. |
| S4 | **Medium** (false-BLOCKED) | Testing `%F = directory` fails under a non-C locale: `Verzeichnis` (P7). `/` would then be BLOCKED as "non-directory" for any operator with a localized `LANGUAGE`/`LC_*`. The script never sets `LC_ALL` for probes (it appears only at :1748). | P7 | A false BLOCKED (exit 2) on a healthy root | Use `LC_ALL=C` on the stat call **and** derive the type from `%A` char 0 (`d`/`l`/other) or `%f` & `0xF000`, never from `%F`. `LC_ALL=C` also fixes the stderr class matching in §4. |
| S5 | **Medium** (ambiguity) | Symlink override: `[ -d ]` follows it (P3), `stat` without `-L` does not (P2), and a trailing slash makes `stat` follow (P2). Under `test -d` plus `stat`, a link to a 0555 dir passes `-d` and then reports `777` (`a=777`, P2), which gives a **false owner w+x**. Two separate calls are also a TOCTOU window. | P2, P3 | A false HEALTHY for a symlinked override; inconsistent results with and without the trailing `/` | Make one `stat` call with no `-L` and no separate `test -d`. Type `l` → `BLOCKED root_meta=non-directory(symlink)`; any other non-`d` type → `non-directory`. Reject override values that are not absolute or that end in `/` (except exactly `/`) as `BLOCKED root_meta=invalid-override`. The real `/` cannot be a symlink, so live mode loses nothing. |
| S6 | **Medium** (selftest self-abort / leak) | An "inaccessible metadata" fixture built as a 000 dir **inside `$FX`** makes `fx_hash`'s `find` exit 1. Under `pipefail` + `set -e`, the whole selftest aborts at `before=$(fx_hash "$FX")` (P10). A **non-empty** 000 dir also defeats the `trap rm -rf` cleanup, leaving residue in `/tmp` (P11). | :1748-1761, :1574; P10, P11 | The selftest dies or leaks scratch dirs | Put the locked parent **outside `$FX`** (for example `$work/locked-<case>`), keep it **empty**, and point `TSUKUROI_ROOT_DIR` at `<locked>/root`: stat gives EACCES (P9) and `rm -rf` succeeds (P9). A 0555 fixture must be an empty dir (P12). |
| S7 | **Medium** (inversion if an access test is used) | Deciding owner write/search with `[ -w ]` / `[ -x ]` or `access(2)` measures the **caller**, not the owner. As uid 1000, `-w /` is false on any root-owned `/` (P16), so every live run is DEGRADED. As unbounded root, `CAP_DAC_OVERRIDE` (S027) / `access(2)` permitted caps (S034) pass `-w` on 0555, which masks the incident. A read-only mount gives EROFS, which is mount inference the spec forbids. | P16; `corpus/SOURCES.md` S027, S034; `snapper-eacces-mechanism.md:14` | Inverted verdicts depending on who runs the gate | Decide only from the owner mode bits in `stat`. `%A` char 2 = `w`, char 3 ∈ {`x`,`s`}; `S` = setuid without search. This is ACL-complete for the owner, because owner bits = `ACL_USER_OBJ` (P17). |
| S8 | **Low** (code injection if a pattern is copied) | Bash arithmetic re-evaluates its operand: `$((m))` and `[[ $m -lt … ]]` executed an embedded `$(…)` (P14). Parsing `%a`/`%f` with `$((8#…))`/`$((16#…))`, or comparing uid with `[[ -eq ]]`, on unvalidated text becomes command execution if `stat` is ever made override-able via a dispatcher stub (the "every probe command override-able" convention, :326). | P14 | Fixture content (or env) executes code | `case`-validate before any numeric use (existing pattern :1337-1339): mode `[0-7][0-7][0-7]` or 4 digits, uid/gid `''\|*[!0-9]*` → invalid. Prefer `%A` string positions, with no arithmetic. Use `[ ]`, not `[[ ]]`, for integer compares. |
| S9 | **Low** (format) | `%a` has 4 digits when the sticky, setuid or setgid bit is set (`1777`, P4), so reading "first digit = owner" is wrong for 4-digit modes. | P4 | A wrong owner bit (false DEGRADED or false HEALTHY) | Use `%A` positions (S7), or take the last 3 digits after validation. |
| S10 | **Low** (provenance) | In this harness shell, `stat` is a **builtin** (`stat 0.8.0`) that is not GNU. With an empty path it returned the cwd's mode, rc 0 (P8). The census runs under clean `bash`, which resolves `/usr/bin/stat` (GNU 9.11), so it is unaffected. Author-side probes from harness shells (for example RootLive's `stat -c …`) are not GNU-coreutils evidence unless they call `/usr/bin/stat`. | P8 | Mislabelled evidence; an empty override is read as the cwd in harness reproductions | Guard against an empty `ROOT_DIR` in the gate (`${TSUKUROI_ROOT_DIR:-/}` plus the absolute-path check). Peer probes should cite `/usr/bin/stat`. |
| S11 | **Info** (note loss) | Packages early returns *assign* `PKG_NOTE=` (:536, :541, :549, :556). Root tokens computed earlier are overwritten, and the blind spot disappears exactly when pacman fails. | :536-556 | C1 is not visible on the pacman-failure path | Compose the root tokens into the note at print time, or prefix them in every early-return assignment. Fold `ROOT_V` with `worse` so a pacman BLOCKED cannot be lifted. |

No finding: `cap()` runs `"$@"` without `eval`/`sh -c` (:456-461), so a quoted
`"$ROOT_DIR"` after `--` cannot inject shell. `stat` reads only inode metadata, which any
user can already read for `/`, so there is no secret-content read. An override can only
reveal mode/uid/gid that the caller could stat itself, as long as the path is never printed
(S2). `stat` is not a write, and the default path `/` is fixed.

## 3. Residual risks (not demanded by the spec; reported, verdict-neutral)

- R1 [INFERENCE from `man 5 acl` owner/ACL_USER_OBJ semantics and directory write semantics]:
  a `/` owned by a non-root uid, or a `/` that is group/other-writable without the sticky bit,
  lets that uid or group rename top-level entries such as `/etc`. That is a privilege hazard
  worse than 0555. The spec forbids an unsupported default-0755 requirement, so this stays
  evidence-only (`root_uid=`, `root_mode=`). Selftest fixtures are owned by the test uid (1000),
  so a uid≠0 rule would also turn every fixture DEGRADED. Leave it verdict-neutral and record it.
- R2: QUALITY #13 asks for owner/mode/**ACL**. Owner write/search is ACL-complete through
  owner bits (P17), but **ACL presence** is not visible to `stat`. Leave it unclaimed rather
  than infer it.
- R3: when the selftest runs as EUID 0, the EACCES fixture (S6) is not inaccessible, because
  root has CAP_DAC_OVERRIDE (S027), so the case flips. Either assert the ENOENT variant (missing
  path, uid-independent) as the primary "unavailable" case, or mark the EACCES case
  `unrun (euid=0)` rather than faking a pass.
- R4: the env-trusted model is unchanged. Exported `BASH_FUNC_stat%%`/`BASH_ENV` can replace
  `stat`, just as `TSUKUROI_PACMAN` can already replace pacman. This is not new with C1.

## 4. Recommended safe boundary (concrete; for Census to adopt, not applied here)

```bash
ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}                       # empty -> default (S10)
ROOT_SRC=default; [ -n "${TSUKUROI_ROOT_DIR:-}" ] && ROOT_SRC=override   # S3
probe_root_meta() {                                    # sets ROOT_V ROOT_NOTE; never prints the path (S2)
  local a m u g cls
  case "$ROOT_DIR" in
    /) ;; */) ROOT_V=BLOCKED ROOT_NOTE="root_meta=invalid-override root_src=$ROOT_SRC"; return ;;
    /*) ;; *) ROOT_V=BLOCKED ROOT_NOTE="root_meta=invalid-override root_src=$ROOT_SRC"; return ;;
  esac
  cap env LC_ALL=C stat -c '%A %a %u %g' -- "$ROOT_DIR"  # one lstat, no -L, no test -d (S4,S5)
  if [ "$CAP_RC" -ne 0 ]; then                          # classify; never forward CAP_OUT
    case "$CAP_OUT" in *'Permission denied'*) cls=eacces ;; *'No such file or directory'*) cls=enoent ;;
      *'Not a directory'*) cls=enotdir ;; *) cls=error ;; esac
    ROOT_V=BLOCKED ROOT_NOTE="root_meta=unavailable($cls) root_src=$ROOT_SRC"; return
  fi
  case "$CAP_OUT" in *$'\n'*) ROOT_V=BLOCKED ROOT_NOTE="root_meta=unavailable(parse) root_src=$ROOT_SRC"; return ;; esac
  read -r a m u g <<<"$CAP_OUT"
  case "$a" in ??????????) ;; *) a=invalid ;; esac      # %A is exactly 10 chars
  case "$m" in [0-7][0-7][0-7] | [0-7][0-7][0-7][0-7]) ;; *) a=invalid ;; esac
  case "$u$g" in '' | *[!0-9]*) a=invalid ;; esac       # S8: validate before any numeric use
  case "$a" in
    invalid) ROOT_V=BLOCKED ROOT_NOTE="root_meta=unavailable(parse) root_src=$ROOT_SRC"; return ;;
    l*) ROOT_V=BLOCKED ROOT_NOTE="root_meta=non-directory(symlink) root_src=$ROOT_SRC"; return ;;
    d*) ;; *) ROOT_V=BLOCKED ROOT_NOTE="root_meta=non-directory root_src=$ROOT_SRC"; return ;;
  esac
  ROOT_V=HEALTHY; cls=''
  [ "${a:2:1}" = w ] || cls="${cls}write,"              # S7/S9: owner bits from %A, never access()
  case "${a:3:1}" in x | s) ;; *) cls="${cls}search," ;; esac
  [ -n "$cls" ] && ROOT_V=DEGRADED
  ROOT_NOTE="root_mode=$m root_uid=$u root_gid=$g root_src=$ROOT_SRC${cls:+ root_owner_missing=${cls%,}}"
}
```

Selftest boundary: add `TSUKUROI_ROOT_DIR="$FX/root"` to the `check()` base list and
`chmod 0755` it in `fx_default` (`umask 077` :321 would otherwise make it `700`). Every case
asserts `root_src=override` (S1). 0555 = an empty dir with `chmod 0555`. EACCES = an empty
000 parent **outside `$FX`** (S6, R3). ENOENT = a missing path. Non-directory = a regular
file and a symlink to a 0555 dir, which must come out BLOCKED and not 777-HEALTHY (S5). The
fixture tree must stay `fx_hash`-able.

## 5. Not done / unrun

- No implementation existed to review (`git diff --stat` empty). Re-review of Census's diff is
  **unrun**.
- `--selftest` and the live census were **not run** (the parent owns checks).
- The capabilities(7) and access(2) man pages are not installed locally. S027/S034 are cited
  from `corpus/SOURCES.md` and were not re-opened by this seat.
