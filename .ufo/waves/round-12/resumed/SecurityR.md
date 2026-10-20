# Round 12 (resumed): Security seat SecurityR, root-metadata override/probe and wave sanitization

Seat: `SecurityR` (UFO-FSD sentinel). This is **author-side seat evidence**, not independent
non-author verification. No PASS is claimed.

Scope:
1. C1 root-metadata path override (`TSUKUROI_ROOT_DIR`) and the probe. Checked for secret
   reads, command injection, symlink and non-directory ambiguity, and the host read-only
   contract.
2. Parent IRC addendum: a sanitization scan of the round-12 wave directory (inherited and
   resumed) for credential, argv and raw-config material before L1 commits it.

Source state reviewed:
- HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`.
- At the start of this pass, `tools/tsukuroi-census.sh` was baseline: grep `ROOT_|root_meta|root_src|root_mode|probe_root` returned 0 matches.
- Mid-pass, Census's **in-flight, uncommitted** draft appeared: `git diff --stat` = `117 insertions(+), 6 deletions(-)`; sha256 `f08412c74d69eb9a…` at review time. The file tag changed again during the read (3EB0 → BFA3), so the draft is still moving.
- §3 reviews that snapshot statically. A re-review of Census's final revision is **unrun**.

Writes: this file, plus two agent messages (to CensusR with remediation items; to TameshiR12
declining an off-wave write redirect). No scratch dirs, no `/tmp` writes, no sudo, no package
operations, no service actions, no env dump, no argv or credential reads.
Installs/updates: **none**. Tests, selftest, census runs, builds, lint: **not run** (parent owns checks).

## 1. Commands run this pass (read-only)

All host probes ran under `env -i /usr/bin/bash --norc --noprofile` so that GNU binaries are
used rather than harness builtins (see Q1/Q16).

| # | Command (sanitized) | Exit | Observation |
|---|---|---|---|
| Q1 | clean bash `type -a stat`; `/usr/bin/stat --version` | 0 | `/usr/bin/stat`, GNU coreutils 9.11 |
| Q2 | `/usr/bin/stat -c '%A %a %u %g %F' -- /` | 0 | `dr-xr-xr-x 555 0 0 directory` |
| Q3 | same, for `/bin`; `/bin/`; `/bin/.` | 0;0;0 | `lrwxrwxrwx 777 0 0 symbolic link`; `drwxr-xr-x 755 …directory` ×2. A trailing `/` or `/.` resolves the link. |
| Q4 | same, for `/tmp`; `/dev/null` | 0;0 | `drwxrwxrwt 1777`; `crw-rw-rw- 666 … character special file` |
| Q5 | `/usr/bin/stat -c '%A %a' -- ''` | 1 | `cannot statx '': No such file or directory` |
| Q6 | `/usr/bin/stat -c %a -L /` (no `--`) | 0 | `555`: a leading-dash operand is parsed as an option |
| Q7 | `[ -d /bin ]`, `[ -L /bin ]`, `[ -w / ]`, `[ -x / ]` as uid 1000 | 0,0,1,0 | `test -d` follows links; `-w /` is false for a non-owner at any mode |
| Q8 | `LC_ALL=C stat -- /root/x`; `/proc/version/x`; `/nonexistent-tsk` | 1;1;1 | `…: Permission denied` / `Not a directory` / `No such file or directory` |
| Q9 | `LC_ALL=C stat -- '/nonexistent-tsk/x: Permission denied'` | 1 | `cannot statx '/nonexistent-tsk/x: Permission denied': No such file or directory`. The **path text reaches stderr**, so a substring match on `Permission denied` misclassifies ENOENT. |
| Q10 | `LC_ALL=C stat -- $'/nonexistent-tsk\nTSUKUROI_CENSUS: HEALTHY (forged)'` | 1 | stat escapes the newline in its own stderr (`'…'$'\n''…'`) |
| Q11 | `LANGUAGE=de LC_ALL=C stat -c F=%F -- / /bin /nonexistent-tsk` | 1 | English output: `directory`, `symbolic link`, English strerror. `LC_ALL=C` overrides `LANGUAGE`. |
| Q12 | `LANGUAGE=de LC_ALL=en_US.UTF-8 stat -c F=%F -- …same` | 1 | `Verzeichnis`, `symbolische Verknüpfung`, German strerror (`…nicht gefunden`) |
| Q13 | `m='x[$(echo ARITH-EXEC-1 >&2)]'`: `$((m))`; `[[ $m -lt 1 ]]`; `[ "$m" -lt 1 ]`; `$((8#$m))`; `$((8#0[$(…)]))` | 0;0;2;1;1 | the first two printed `ARITH-EXEC-1` (**executed**); `[` → `integer expected`; both `8#` forms → `value too great for base` / `arithmetic syntax error`, **no execution** |
| Q14 | `set -euo pipefail; m=q; (x=$((8#$m)); …); …` | 1 | the **whole script terminated with rc 1** and no later line ran. rc 1 is the census DEGRADED code and no rollup line is printed. |
| Q15 | in-memory: `PLANE …` line whose note embeds `\nTSUKUROI_CENSUS: HEALTHY (forged` piped to `grep '^TSUKUROI_CENSUS:'` → first line | 0 | `first=TSUKUROI_CENSUS: HEALTHY (forged)` |
| Q16 | harness `find --version`; clean bash `/usr/bin/find --version`; `find tools -maxdepth 0 -printf '%y %m %U %G %P\|'` | 0;0;0 | harness: `find 0.8.0` (**builtin**, not GNU); clean: GNU findutils 4.11.0; `d 755 1000 1000 \|` |
| Q17 | `getfacl -p /var/log/journal`; `/usr/bin/stat -c '%A\|%a'`; `ls -ld` | 0;0;0 | named-group ACL entries present; stat `drwxr-sr-x\|2755` (10 chars, **no `+`**); ls `drwxr-sr-x+`. ACL presence is invisible to `stat`, but the owner bits are still exact (ACL_USER_OBJ). |
| Q18 | `env A=base A=case bash -c 'echo $A'` | 0 | `A=case` (later assignment wins) |
| Q19 | bash `${p@Q}` for `p=$'/x\nTSUKUROI_CENSUS: HEALTHY (forged'`; `q='/nonexistent root_mode=0755 root_status=ok'`; ESC/TAB; then the draft BLOCKED note with `${q@Q}` piped to `grep -oE '\broot_mode=[0-9]+'` | 0 | newline/ESC/TAB → `$'…\n…'` / `\E` / `\t` (single line, **no newline forgery**); `q` → `'/nonexistent root_mode=0755 root_status=ok'`; grep prints `root_mode=0755` (**token spoof**) |
| Q20 | `sha256sum tools/tsukuroi-census.sh`; `git diff --stat -- tools/tsukuroi-census.sh` | 0;0 | `f08412c7…`; `117 insertions(+), 6 deletions(-)` (in-flight draft) |

Sanitization scan commands (§4) are `grep`-tool regex sweeps over `.ufo/waves/round-12/**`
(gitignore off) and one `jq` path sweep over the wave JSON. The patterns are listed in §4.

## 2. Inherited `.ufo/waves/round-12/Security.md`: reuse, reject, correct

This file is treated as historical. It was not edited.

- **Reused, re-observed this pass:** P1→Q2, P2/P3→Q3/Q7, P4→Q4, P5→Q8, P6→Q6, P7→Q12, P8→Q1/Q5, P13→Q15, P14→Q13, P15→Q18, P16→Q7.
- **Reused, NOT re-run (historical only):** P9–P12 (scratch `chmod 000`/`0555` and `rm -rf` behaviour, `fx_hash` abort on a 000 dir). This pass made no host writes. P17 (`man 5 acl`) was not re-opened; Q17 independently confirms that `stat` mode bits omit ACL presence.
- **Corrected S8:** `$((8#$mode))` on unvalidated text does **not** execute code (Q13). It **aborts the whole script with rc 1** (Q14): no verdict line, and the exit code reads as DEGRADED. That is a fail-open exit-map defect, not injection. `$((var))` and `[[ $var -lt … ]]` do still execute (Q13).
- **Corrected §4 boundary (stderr class):** substring `*'Permission denied'*` is spoofable by path text (Q9). Match the suffix instead (`*": Permission denied"`). GNU stat escapes newlines in its own stderr (Q10), so stderr alone is not a line-forgery vector. The script printing a raw path is (S2).
- **Corrected S10:** `find` is also a harness builtin (Q16). Peer probes of `find`/`stat` taken from the harness shell are not GNU evidence. FixtureReview's "findutils 4.11.0 `-printf`" holds for `/usr/bin/find` (Q16).
- **Peer conflicts resolved (inherited files, read-only):**
  - C1Review F7 (`stat -L` everywhere) vs ClaimCritic CX6 / Security S5 (one stat call, no `-L`). Both are safe **iff** type and mode come from the same single call and no `[ -d ]` is mixed in. The draft uses `-L` (§3). Accepted.
  - ClaimCritic §`root=<path> root_type=<%F>`: `root_type=%F` is safe only under `LC_ALL=C` (Q11/Q12). A printed path must not be able to form tokens (Q19, §3 D1).
  - FixtureReview U2 (000 dir **inside** `$FX`) and "redirect find stderr → no false pass": rejected. The stderr redirect does not change find's rc. Under `pipefail` + `set -e`, `before=$(fx_hash "$FX")` still aborts (inherited P10, not re-run). Keep the locked parent outside `$FX`, or group `{ find … 2>/dev/null || true; }` and accept that the unreadable subtree is unhashed.
  - MutationPlan M4 ("scoped `stat` shim"): making `stat` overridable turns stat output into env-controlled text. Then S8-style validation before any arithmetic becomes mandatory. The draft does validate first (§3).

## 3. Review of the in-flight Census draft (static; snapshot `f08412c7…`)

Anchors refer to that snapshot:
- `probe_root_meta` :720-771
- `ROOT_DIR=${TSUKUROI_ROOT_DIR:-/}` :353
- integration :2459-2469 (`PKG_V=$(worse …)`, `printf 'PLANE packages: %s (%s; %s)\n' … "$ROOT_NOTE"`)
- fixture root :1758-1761 (`chmod 0755 "$d/root"`)
- `check()` base env `TSUKUROI_ROOT_DIR="$FX/root"` :1866
- `fx_hash` :1837
- trap :1660

**Closed by the draft (inherited finding → status):**
- S1: root override is in the `check()` base list before `EXTRA_ENV`. **Closed.**
- S4: `cap env LC_ALL=C stat …` (Q11). **Closed.**
- S5: a single `stat -L -c '%a %u %g %F' -- "$ROOT_DIR"`, no `[ -d ]`; the second plain `stat` runs only on failure, as a verdict-neutral label. **Closed.**
- S6 partial: the `$d/root` fixture is an empty 0755 dir. **OK** so far.
- S7: owner bits come from mode, never `access()`. **Closed.**
- S8: the mode is validated with `*[!0-7]*` before `$((8#$mode))`, so Q14's abort cannot be reached through mode text. **Closed.**
- S9: an octal mask handles 4-digit modes. **Closed.**
- S10: an empty override falls back to `/` (`:-`). **Closed.**
- S11: the root note is composed at print time and survives every packages early return. `worse` folds it. **Closed.**
- S2 newline forgery: `${ROOT_DIR@Q}` escapes newline/ESC/TAB (Q19). **Closed for line forgery.**
- S3: the printed `root_dir=` exposes a stale override. **Closed.**

**Still open in the draft:**

| ID | Severity | Exploit / failure path | Evidence | Impact | Smallest remediation |
|---|---|---|---|---|---|
| D1 | **Medium** (measurement forgery) | Override `TSUKUROI_ROOT_DIR='/nonexistent root_mode=0755 root_status=ok'`. stat fails → BLOCKED note `root_status=unavailable(…) … root_dir='/nonexistent root_mode=0755 root_status=ok'`. A `\broot_mode=` counter matches the spoofed token (Q19). | Q19; draft :739, :746, :752, :769; CensusScribe gate (`\broot_mode=` count == 1) | The red/green gate goes green on a BLOCKED arm. Regex consumers and selftest pins (`root_status=ok`) can be satisfied by path text. The verdict word itself is not forged. | Print `root_src=default\|override` instead of the path. Or print the path only when it matches `^/[A-Za-z0-9._/+-]*$` (no `=`, space or quote), else `root_dir=unsafe`. |
| D2 | Low (mislabel) | The errno class at :729-733 is a substring match, and stat stderr contains the path (Q9). An ENOENT override whose name contains `Permission denied` is labelled `errno=permission-denied`. | Q9; :730-732 | A wrong errno label. Still BLOCKED (fail-closed). | Suffix patterns: `*": Permission denied"`, `*": No such file or directory"`, `*": Too many levels of symbolic links"`, plus `*": Not a directory"` → `not-a-directory` (Q8, currently `unknown`). |
| D3 | **Medium** (zero-mutation blind spot) | `fx_hash` (:1837) hashes `find -type f` content only. The root fixture is an **empty directory**, so it contributes nothing. A census run that chmods or replaces `$FX/root` passes `fx_no_mutation`. | :1837; FixtureReview A6 (inherited) | The "fixture byte-unchanged" claim does not cover the one new C1 input. Spec asks for mode/digest mutation detection. | Add `find "$1" -printf '%y %m %U %G %P\n' \| LC_ALL=C sort` to the digest (GNU 4.11, Q16). Hash any out-of-tree locked fixture separately with `stat -c '%A %u %g'`. |
| D4 | Medium (selftest abort/leak, pending cases) | No root-specific cases exist yet in this snapshot (grep `root_` in the selftest → only :1758-1761, :1866). If a 000 or non-empty 0555 fixture is added inside `$FX`, `fx_hash` aborts the suite (inherited P10) and the trap `rm -rf` (:1660) leaks residue (inherited P11). | :1660, :1837; inherited P9–P12 | The suite dies or leaves `/tmp` residue | Keep the 000 parent **outside `$FX`** and **empty** (`$work/locked-<case>`, seam `<locked>/root`). Keep 0555 fixtures empty. Or change the trap to `chmod -R u+rwx -- "$work" 2>/dev/null; rm -rf -- "$work"`. |
| D5 | Low (EUID 0 inversion of a fixture) | Under EUID 0, CAP_DAC_OVERRIDE makes the EACCES fixture readable, so the case flips. | inherited R3; S027 | False FAIL, or a vacuous case | Use ENOENT / dangling link as the uid-independent "unavailable" case. Run the EACCES case only when `[ "$(id -u)" -ne 0 ]`, else emit a named skip, never a pass. |
| D6 | Low (path ambiguity) | A relative override is stat-ed against the cwd. `/x/.`, `/x/..` and intermediate symlinks are resolved (Q3: `/bin/.` → the target dir). | Q3; :353, :726 | A cwd-dependent reading. The printed path then misstates which inode was measured. | Reject a non-absolute override as `root_status=invalid-override` (BLOCKED). Optionally also reject `*/./*\|*/../*\|*/.\|*/..\|*//*`. |
| D7 | Info | `%a` and `%A` omit ACL presence (Q17). The owner class is still exact (ACL_USER_OBJ). | Q17 | QUALITY #13's "ACL" is not covered by this arm | Do not claim ACL coverage. Owner bits are complete for the owner class; ACL presence stays unclaimed. |
| D8 | Info | The draft DEGRADEs on owner-bit absence "regardless of the probing uid" (:97-100, :717-719). This is a parent ruling, not a security defect. It does mean the live host `/` (555, uid 0) reads DEGRADED for a uid-1000 run. | :97-100; Q2 | An operability/judgment item for the parent | None from this seat. Keep the wording "review finding, never writability" as drafted. |

**No finding:**
- **Secret reads:** `stat` issues `statx` (metadata only) and never opens the file. An override reveals only the mode/uid/gid tokens that the caller could already stat. Running under sudo grants nothing that root lacks.
- **Command injection:** `cap()` runs `"$@"` with no `eval` (baseline :456-461). `--` precedes the path (Q6 shows why it is needed).
- **Host writes:** none in live mode. [INFERENCE] `statx` on a hung network or automount path could block. That risk is env-trusted and unchanged from the other path overrides; no timeout exists elsewhere in the census.
- **Non-root-owned fixture:** not fixtureable without chown/sudo (forbidden). The default fixture is already owned by the test uid, so pin `root_uid=$(id -u)`.

## 4. Wave sanitization scan (parent addendum): `.ufo/waves/round-12/**`, inherited and resumed

Patterns swept (regex, case-insensitive):
- Private-key headers; `ghp_`/`github_pat_`/`gh[ousr]_`; `sk-…`; `AKIA…`; `xox[abp]-`; `Bearer …`; `Authorization:`; `password|passwd|secret|api_key|token` followed by `=`/`:`; `cookie:`; JWT `eyJ…`.
- `/proc/*/cmdline|environ`; `ExecStart=`/`Environment=`/`EnvironmentFile=`; `systemctl cat`; `journalctl -o cat|verbose|json-pretty`; `_CMDLINE`/`_EXE`/`_PID`; `MESSAGE`; `printenv`; `SSH_AUTH_SOCK`/`DBUS_SESSION_BUS_ADDRESS`/`XDG_RUNTIME_DIR`; `~/.ssh|.gnupg|.netrc|id_rsa|id_ed25519`; `/etc/shadow`.
- Unit section headers `[Service]|[Unit]|[Install]`; env keys `PATH/HOME/USER/SHELL`.
- Machine/boot IDs (32-hex); IPv4/MAC; emails; hostname; `name[PID]:` journal prefixes.
- Mixed-case high-entropy strings of ≥32 characters.
- `jq` key sweep for `env|argv|cmd|stdout|stderr|secret|token|pass` across all 19 wave JSON files.

**Result: no credential or secret material found.**
- The only credential-pattern hit is the prose phrase "Upgrade Authorization" (`BootBoundary.md:122`).
- High-entropy hits are public GitLab API URLs and commit/sha256 hashes (`SourceReview.md:19,21`; `resumed/UnitLive*.md:91,93`).
- JSON `stdout`/`stderr` fields hold only probe outputs: stat/getfacl/findmnt/`systemctl show -p` property projections in `discriminator-smoke.json`, the source-census `0`/ok output, and registry text.
- `resumed/task-result.json` `tokens` fields are **numeric usage counts** (`jq` type `number`).
- No `ExecStart=`/`Environment=` lines, no env dumps, no `/proc/*/cmdline|environ` reads, no unit-file section dumps.

**Contract-shape deviations.** None of this is secret. All of it is non-secret host-identifying material. Old evidence was not edited; the parent decides.

| Sev | File:lines (inherited unless marked) | Material | Why flagged |
|---|---|---|---|
| Low-Med | `Issue6629.md:71-81` | `journalctl -u … -n 25` trail: boot ID (32-hex) at :72; 9 verbatim journal lines with PIDs `[1386]`/`[1520]` at :73-81 | Closest to "raw journal bodies". The contract asks for sanitized metadata only. |
| Low | `RootLive.md:80` | One full journal line with hostname `plazir27`, PID `[1520]` and message | Raw journal line plus hostname |
| Low | `MatrixCritic.md:26-27` | Journal field names (`_SYSTEMD_UNIT`, `SYSLOG_IDENTIFIER`, `_UID`) and an `-o cat` message line | Journal body excerpt, short |
| Low | `C2Review.md:24` | One emitter message line | Journal body excerpt, short |
| Low | resumed: `resumed/RootLiveR.md:130-132`, `resumed/OverlapHostR.md:47` | Journal lines with hostname and PID | Same shape. Not inherited; the owning seats are still live. |
| Info | `BootBoundary.md:15`; `PackageBlind.md:31,168,286`; `resumed/BootBoundaryR.md:33`, `resumed/OverlapHostR.md:36`, `resumed/PackageBlindR.md:43,186` | Hostname `plazir27` | Host identifier (not secret) |
| Info | `AclSemantics.md:69`; `resumed/AclSemantics*.md:78` | `uid=1000(vgpnk) gid=1000(vgpnk)` | Local username (not secret) |
| Info | `AdmissionCritic.md:40` | git `user.email tsukuroi@shokunin.local` | Local lane identity |
| Info | `BootBoundary.md:23`; `AclSemantics.md:68`; `discriminator-smoke.json` findmnt stdout; `resumed/AclSemantics*.md:77`, `resumed/OverlapHostR.md:42` | Root mount options incl. `subvolid=256,subvol=/@` | Layout metadata. C2Review records that it redacted the subvol. |
| Info | `PackageBlind.md:182-188` | `pacman -Qkk` warnings naming `/etc/shadow`, `/etc/gshadow`, `/etc/crypttab` | **File names only** (checksum-failed as non-root). No content. |
| Info | `Issue6629.md:62-66`, `:84-97`; `AclSemantics.md:70`; `MountErrors.md:141`; `RootLive.md:36` | Unit property projections (`User=`, `CapabilityBoundingSet=`, `Protect*=`) and quoted lines of the package-shipped watcher script | Sanitized property subsets and package code. Not host secrets, not ExecStart/Environment. |

Scan limits: the scan is regex and heuristic, not an exhaustive entropy or PII audit. It found no
secret material. Resumed files are still being written by live seats; the scan reflects their
state at scan time.

## 5. Recommended safe boundary (delta on the draft; for Census, not applied here)

```bash
ROOT_SRC=default; [ -n "${TSUKUROI_ROOT_DIR:-}" ] && ROOT_SRC=override
case "$ROOT_DIR" in /*) ;; *) ROOT_V=BLOCKED ROOT_NOTE="root_status=invalid-override root_src=$ROOT_SRC"; return ;; esac   # D6
# … existing single `cap env LC_ALL=C stat -L -c '%a %u %g %F' -- "$ROOT_DIR"` …
case "$CAP_OUT" in                                                     # D2: suffix, not substring
  *": Permission denied") why=permission-denied ;; *": No such file or directory") why=no-such-path ;;
  *": Too many levels of symbolic links") why=symlink-loop ;; *": Not a directory") why=not-a-directory ;;
esac
# D1: every ROOT_NOTE ends with `root_src=$ROOT_SRC`, never with the raw path; if a path is wanted:
case "$ROOT_DIR" in *[!A-Za-z0-9._/+-]*) rd=unsafe ;; *) rd=$ROOT_DIR ;; esac   # no '=', space, quote
```

Selftest:
- D3: `fx_hash` adds `find "$1" -printf '%y %m %U %G %P\n' | LC_ALL=C sort` to the digest.
- D4: keep the 000 parent outside `$FX` and empty; keep 0555 fixtures empty.
- D5: EUID-0 runs get a named skip for the EACCES case. The uid-independent unavailable cases are ENOENT and a dangling link.
- Pin `root_uid=$(id -u)` and `root_mode=0755` in the healthy cases, so a leak to the host `/` (555/0) fails.

## 6. Not done / unrun

- The final Census revision has not been re-reviewed. §3 is a static review of an in-flight snapshot (`f08412c7…`).
- `--selftest`, the live census, and the red/green gate were **not run**.
- Inherited P9–P12 (scratch-write probes) were not re-run. They are historical only.
- `capabilities(7)`/`access(2)` were not re-opened. S027/S034 are cited via `corpus/SOURCES.md`.
