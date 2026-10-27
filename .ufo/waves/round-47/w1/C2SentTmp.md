VERDICT: defect-found

# C2SentTmp — security review: the `/tmp` fallback and the cleanup trap in `run_selftest`

Seat C2-S2. Reviewed revision: lane working tree at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh` (read-only; no lane file touched). Host: Arch `7.2.11-arch1-1`, GNU coreutils 9.12-2 (`/usr/bin/rm`, `/usr/bin/chmod`), running uid 1000. All experiments under `/fast/scratch/hyaku/tsukuroi-r47/C2SentTmp/` (removed at the end; receipts copied into `.ufo/waves/round-47/w1/C2SentTmp/`). No tool installed, no package transaction, no host mutation.

## Surface under review

| where | what |
|---|---|
| `tools/tsukuroi-census.sh:452-453` | `set -euo pipefail`, `umask 077` (whole script) |
| `tools/tsukuroi-census.sh:850-864` | `root_locator_class` (absolute/empty/relative/unsafe; charset `A-Za-z0-9._/+-`) |
| `tools/tsukuroi-census.sh:2049` | `local bin fx` — **`work` is not local** |
| `tools/tsukuroi-census.sh:2055-2058` | `st_base=${TMPDIR:-/tmp}` + charset fallback to `/tmp` |
| `tools/tsukuroi-census.sh:2059` | `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` |
| `tools/tsukuroi-census.sh:2062` | `trap 'chmod -R u+rwx -- "${work:-}" 2>/dev/null \|\| true; rm -rf -- "${work:-}" 2>/dev/null \|\| true' EXIT INT TERM` |
| `tools/tsukuroi-census.sh:2063-2064, 2366` | `bin="$work/bin"`, `FX="$work/fx/$case_home"` — every fixture path derives from `$work` |
| `tools/tsukuroi-census.sh:411-412, 602` | doc claims: the selftest writes only under the mktemp dir (or `/tmp` when the charset filter fires) |

Precedent in the same lane: `tools/boot-chain-audit.sh:156-183` already implements a stricter cleanup (`guarded_rm` refuses any path outside the mktemp tree; `init_work` refuses a non-absolute created path). The census has neither guard.

---

## Q1 — does a predictable, `${-}`-free mktemp dir under `/tmp` open a symlink/race hole another local user could exploit (uid 1000)?

**No hole.** The prefix is irrelevant to safety; only the creation primitive and the parent directory matter.

1. **Creation is one atomic syscall, mode 0700.** `strace -f -e trace=mkdir,openat /usr/bin/mktemp -d 'tsukuroi-r3-2-selftest.XXXXXX'` shows exactly one creation call and no preceding stat of the candidate name:
   `mkdir("tsukuroi-r3-2-selftest.MBH9tD", 0700) = 0` (`mktemp-semantics.txt`). There is no stat-then-create window to win.
2. **A planted entry is never adopted.** `mkdir(2)` fails on any existing entry, including a dangling symlink: `/usr/bin/mkdir planted` over `planted -> /nowhere` →
   `mkdir: cannot create directory 'planted': File exists` (rc 1). `mkdtemp` therefore either gets a fresh name or `mktemp` exits non-zero.
3. **A base that cannot yield a dir fails closed.** `mktemp -d /proc/tsukuroi-r3-2-selftest.XXXXXX` → `failed to create directory via template …: No such file or directory`, rc 1. With `set -e` (`:452`) the assignment at `:2059` aborts the function before the trap at `:2062` is even installed.
4. **The fallback parent is sticky.** `stat -c '%a' /tmp` → `1777`. Another uid cannot rename or unlink an entry it does not own, so the 0700 work dir cannot be swapped out by a third party in the default case. Created dir mode observed: `700 /tmp/tsukuroi-r3-2-selftest.8WVEOJ`-style (verified in the probe run and in `fallback.strace`).
5. **No permission loosening on the work root**: the only `chmod` that touches `$work` itself is the trap's `u+rwx` (adds user bits, never removes); the 1777/0755 fixture modes are set on paths *inside* the 0700 root (`:875`, `:109`).

The `${-}` wording in the item does not apply to the current bytes: the template is a fixed literal plus six random characters (`:2059`), not shell-state entropy.

## Q2 — is `chmod -R u+rwx` / `rm -rf` on the work tree safe if `TMPDIR` were attacker-controlled?

Split verdict.

### `rm -rf` — safe
`rm -rf` never follows the operand symlink: with `$work` replaced by `ln -s victimtree $work`, the trap removed only the link; `victimtree` and its contents survived (`repro-chmod-symlink.txt`). GNU `rm -rf -- ""` is a silent no-op (rc 0) and `chmod -R … -- ""` fails `ENOENT` rc 1, so an empty/unset `$work` does not degrade to `.` — see F3 for the caveat on other implementations.

### `chmod -R u+rwx` — **not safe: F1, clickable hole**
`/usr/bin/chmod --help`: *“The following options modify how a hierarchy is traversed when the -R option is also specified. … -H is the default.”* Coreutils therefore **follows a command-line symlink to a directory** with plain `-R`:

- `chmod -R  u+rwx -- ct/lnk` (link → `ct/d`): `ct/d/f644` went `644 → 744`.
- `chmod -RP u+rwx -- ct2/lnk`: `ct2/d/f` stayed `644` (no traversal).

So if `TMPDIR` points into a directory another principal can write, that principal can swap `$work` for a symlink at any moment between `mktemp` (`:2059`) and process exit, and the exit trap recursively chmods the link target.

### `TMPDIR=/` (and any unwritable base) — safe, traced
`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=/ strace -f -e trace=file bash tools/tsukuroi-census.sh --selftest` →
```
mktemp: failed to create directory via template '//tsukuroi-r3-2-selftest.XXXXXX': Permission denied
rc=1
```
The trace contains no `mkdir`, `creat`, `unlink`, `rename` or `chmod` at all after the failed `mktemp`; `/bin/.dispatch` was never created (`stat` → `No such file or directory`). The `:2063-2064` `$bin = /bin` cascade the item worried about cannot happen because `set -e` kills the assignment first — this is load-bearing and worth a comment (see F3).

## Q3 — can an attacker-controlled `TMPDIR` make the census read/write outside the work dir?

**Writes: no.** Full 84 s run through the fallback path (`TMPDIR` containing a space → `st_base=/tmp`), 164/164 PASS, rc 0, work dir `/tmp/tsukuroi-r3-2-selftest.TF9kQK` created `0700` and removed by the trap. Syscall accounting over 31 MB of trace (`fallback-evidence.txt`):

- `chmod` outside `$work`: **0 successes**; `symlinkat`/`link`/`rename` outside `$work`: **0**; `creat` outside `$work`: **0**.
- The only successful mutating calls with an absolute path outside `$work` are bash's own here-document temp files — `openat("…/t 2/sh-thd.D8aIpJ", O_RDWR|O_CREAT|O_EXCL, 0600)` then `unlink` — i.e. bash writes into `TMPDIR` itself when the script uses `cat > … <<'STUB'`. They are `O_EXCL`, `0600`, immediately unlinked, and carry only the public fixture stub. Everything else (`mkdir("bin", 0777)`, `unlinkat(3, "blocked-…", AT_REMOVEDIR)`) is relative; the chdir is performed by `/usr/bin/mkdir -p` walking its own absolute components, not by the script, and no stray `bin`/`fx`/`healthy` appeared in the launch directory.
- Live mode is write-free in effect: `TMPDIR=/` live run → rc 2, 6 `PLANE` lines, **0 successful mutating syscalls** (`live-evidence.txt`).

**Reads: yes, by substitution — a test-integrity effect, not a confidentiality breach.** All fixture roots derive from `$work` (`:2366 FX="$work/fx/$case_home"`, and each `TSUKUROI_*` override at `:2270-2298` points inside `$FX`/`$bin`), so an attacker who swaps `$work` early makes the cases read attacker-supplied fixture content and can fabricate or spoil verdicts. In selftest mode this exposes no host secret: the census reads only the overrides (`check()` additionally fails any case whose output is not `host=fixture-host`).

---

## Findings

### F1 — [LOW, real] the exit trap's `chmod -R` follows a symlink substituted at `$work`
- **Exploit path** (reproduced with the exact trap body, uid 1000, coreutils 9.12): victim is induced to run the selftest with `TMPDIR` in a base the attacker can write (a 0777 shared build dir, a per-user dir with loose perms, an env-injection vector). Attacker lists the base for the public prefix `tsukuroi-r3-2-selftest.` (the name is listable even though the dir is 0700), runs `mv -- "$work" "$work.real"; ln -s <target-tree> "$work"`, and waits: the EXIT trap does `chmod -R u+rwx -- "$work"` (coreutils `-H` default → traverses the link) and then `rm -rf` (unlinks the link only).
- **Observed**: victim tree `755 victimtree | 400 readonly0400 | 755 sub | 600 sub/tool0600` → `755 | 700 | 755 | 700`; content unchanged; link gone (`repro-chmod-symlink.txt`).
- **Impact**: recursive *addition* of user `rwx` on any tree the running uid owns — e.g. a 0444 archive or a 0400 key becomes user-writable/executable; read-only protection inside the user's own tree is lost. No deletion, no read, no data modification, and no privilege crossing (the kernel enforces per-inode ownership, so entries the victim does not own simply fail with `EACCES`, which `2>/dev/null` hides). Not exploitable through the default `/tmp` fallback: `/tmp` is `1777` sticky, so a third party cannot rename an entry it does not own.
- **Why it matters even at LOW**: the trap is on `EXIT INT TERM` of a 40–90 s run, so the attacker's window is the whole run, not a microsecond race.

### F2 — [LOW, hygiene] the base filter accepts relative and dot-relative `TMPDIR`
`tools/tsukuroi-census.sh:2055-2058` falls back only on characters outside `A-Za-z0-9._/+-`; it never requires an absolute path. Measured with the exact five lines:
```
TMPDIR=relbase -> st_base=relbase work=relbase/tsukuroi-r3-2-selftest.0N7bO0
TMPDIR=.       -> st_base=.       work=./tsukuroi-r3-2-selftest.heDxM2
TMPDIR=..      -> st_base=..      work=../tsukuroi-r3-2-selftest.C0TbgD
TMPDIR='/x y'  -> st_base=/tmp    work=/tmp/tsukuroi-r3-2-selftest.pXRjXD
```
So a caller whose cwd is the lane repo (or the fleet root) gets an untracked fixture tree planted *there* and removed at exit — outside any temp area, and one `kill -9` away from polluting the tree. (`TMPDIR=-x` / `TMPDIR=-/…` fail closed: `mktemp: invalid option`, rc 1 — the template becomes an option; no write.) `tools/boot-chain-audit.sh:177-183` already refuses this class.

### F3 — [informational] the `${work:-}` guard is only inert under GNU coreutils, and `work` is a global
- `work` is assigned once (`:2059`) and read by the trap (`:2062`) *after* `run_selftest` returns, so it must stay global — do **not** make it `local` without moving the trap. But nothing prevents a future edit from reusing the name, which would redirect the trap to an arbitrary path.
- Empty-value behaviour is implementation-defined. With GNU coreutils 9.12 `chmod -R … -- ""` is `ENOENT` rc 1 and `rm -rf -- ""` rc 0 — inert. With the shell-builtin coreutils present in this fleet's tool shell the same calls resolved `""` to the **current directory** (`chmod -R 0600 -- ""` chmod'd the cwd; the walk then errored on `/sub`, `/marker`). No such builtin is on the host PATH (`for d in …; do -e $d/rm`; only `/usr/bin`), but the guard is doing real work on an assumption that is not portable. A non-symlink/non-empty guard (below) removes the assumption.
- Doc nit: `:411-412` says the selftest writes under the mktemp dir *“or /tmp itself”*; the code only ever writes under a mktemp dir created **inside** `/tmp`.

---

## Smallest remediation (exact proposed text)

`tools/tsukuroi-census.sh:2055-2062` — require an absolute base, and make the cleanup refuse a `$work` that is no longer the directory `mktemp` created, using `-P` so `-R` cannot traverse a substituted link (`tools/boot-chain-audit.sh:156-171` is the in-lane precedent):

```bash
  local st_base=${TMPDIR:-/tmp}
  case "$st_base" in
    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
    /*) ;;                       # absolute only: a relative base would plant the fixture
    *) st_base=/tmp ;;           # tree under the caller's cwd (boot-chain-audit.sh:177)
  esac
  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
  # A 000 fixture directory would block `rm -rf` (unlink needs write+search on the parent);
  # restore permissions on the temp tree only, never on a live path. The cleanup acts only
  # while $work is still the directory mktemp created: if the owner of an attacker-writable
  # TMPDIR base renames it away and plants a symlink, plain `chmod -R` would follow that
  # link (coreutils -R defaults to -H, measured) while `rm -rf` would not; -P pins the safe
  # policy for the tree itself. Same guard as ws/guarded_rm in tools/boot-chain-audit.sh:156.
  selftest_cleanup() {
    [ -n "${work:-}" ] && [ -d "$work" ] && [ ! -L "$work" ] || return 0
    chmod -RP u+rwx -- "$work" 2>/dev/null || true
    rm -rf -- "$work" 2>/dev/null || true
  }
  trap selftest_cleanup EXIT INT TERM
```

Verified not to weaken cleanup: against a fixture-shaped tree containing a `000` directory, a `0400` file, a dangling link, a link loop and a directory symlink, the proposed body leaves nothing behind (`work tree gone? yes-removed`). `u+rwX` (as in `guarded_rm`) is a strictly better mode expression if the L1 prefers to match that file exactly.

Residual, stated rather than hidden: the `[ ! -L ]` check is not atomic with the `chmod`, so a swap landing between the two calls is still followed — the window drops from the whole run to microseconds and the damage class is unchanged, which is the right cost/benefit for a shell cleanup. Full closure would need the tree's inode (an fd-based walk) or an explicit per-fixture `chmod` of the ~6 known `000` paths instead of `-R`.

---

## Checked and found sound (no action)

- `mktemp -d` adoption, EEXIST handling, umask race, symlink planted *at the template name before* creation — impossible (Q1.1-Q1.3).
- `TMPDIR=/` (and any unwritable/relative-to-nonexistent base): aborts at `:2059`, no trap, zero writes (Q2, traced).
- `rm -rf` against a substituted link: target survives (`repro-chmod-symlink.txt`).
- Fixture writes are all inside `$work`: 164-case run, 0 successful mutating syscalls outside `$work`, no stray dirs in the launch cwd (Q3).
- `TMPDIR` is consumed only by `run_selftest` (`:2055`); live mode has no `mktemp` at all (`:348` comment, confirmed: only one `mktemp` call site in 3645 lines) and 0 successful mutating syscalls.
- `chmod 1777`/`0755` fixture modes are unreachable from outside because the work root is 0700.

## Secondary observation (outside my surface, offered to the drivers/read-only seats)

Live mode is read-only *in effect*, not by construction: the drivers arm runs `nvidia-smi --query-gpu=…`, which opens `/dev/nvidia0`, `/dev/nvidiactl`, `/dev/nvidia-uvm` with `O_RDWR`, attempts `mkdir("/dev/nvidia-caps", 0755)` and `unlink("/dev/char/195:0")`, `…/237:0`, `…/240:1` (`live2.strace`, pid attributed to `/usr/bin/nvidia-smi`). Every one fails `EACCES` for uid 1000, so no mutation occurs unprivileged; a privileged run of the census would let nvidia-smi manage those nodes. The header claim “It never … writes anything” (`:9-10`) is therefore a claim about observed failure, not about attempted calls.

## Evidence and artifacts

- Report receipts (this seat dir, `.ufo/waves/round-47/w1/C2SentTmp/`): `fallback-evidence.txt` (164-case run tail, chmod/symlink/rename accounting, work-dir creation), `live-evidence.txt` (live-mode trace, `/dev` `/etc` attempts with errno and the attributed binary), `mktemp-semantics.txt` (coreutils 9.12 `-H is the default` text, `mkdir` over a symlink, the `mkdir(…, 0700)` creation call), `repro-chmod-symlink.txt` (before/after modes, `-RP` control, empty-operand controls).
- Commands that produced them (all re-runnable; the two `strace` runs are 84 s and 4 s and must not run concurrently with another seat's selftest):
  - `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" strace -f -e trace=mkdir,openat,unlink,rename,chmod,symlinkat -o fallback.strace bash tools/tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, rc 0.
  - `env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=/ strace -f -e trace=… -o live.strace bash tools/tsukuroi-census.sh` → `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)`, rc 2, 0 mutating successes.
- Scratch `/fast/scratch/hyaku/tsukuroi-r47/C2SentTmp/` removed after the receipts were copied; the two probe leftovers I created outside it (`/tmp/tsukuroi-r3-2-selftest.pXRjXD`, `/fast/scratch/hyaku/tsukuroi-r47/tsukuroi-r3-2-selftest.C0TbgD`) were deleted by me. The 3 remaining `/tmp/tsukuroi-r3-2-selftest.*` dirs at 06:02 belong to concurrently running sibling seats, not to this run (my dir `TF9kQK` is absent).

## Not done

- I did not re-run the C2 counting command (other seats own it); I ran exactly one full selftest, the fallback-path one above.
- I did not test a *third-uid* attacker: only uid 1000 exists in this sandbox, so the "another local user" step is modelled by an owner-writable base plus an explicit `mv`/`ln -s` substitution, and the cross-uid protections are argued from `/tmp` mode `1777` sticky + per-inode ownership enforcement, not demonstrated with a second account.
- I did not attempt an exploit against a live host path, and I made no change to `tools/tsukuroi-census.sh` (read-only lane content): the patch above is proposed text only.
