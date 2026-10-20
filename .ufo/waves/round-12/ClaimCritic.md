# ClaimCritic — round 12, C1 (root metadata census arm)

Seat: critic (author-side review, **not** independent non-author verification). Static evidence plus
read-only, non-root host reads only. No host writes, no sudo, no installs. Census implementation had
**not landed** at review time (`grep -n 'root_mode|root_uid|ROOT_DIR|TSUKUROI_ROOT' tools/` → 0 matches;
no `.ufo/waves/round-12/Census.md`). Every finding below targets the baseline contract: the Census
prompt in `.ufo/waves/round-12/spec.json` (`.items[] | select(.name=="Census")`).

Axes: operability (gate gives a correct, invocation-independent verdict), depth (claims grounded, no
policy overclaim).

## Evidence collected (commands, exit codes)

| # | Command (read-only, uid 1000) | rc | Observation |
|---|---|---|---|
| E1 | `stat -c '%a %f %u:%g %F %n' / /proc /sys /tmp /root /boot` | 0 | `/` `555 416d 0:0 directory`; `/proc` `555`; `/sys` `555`; `/tmp` `1777 43ff`; `/root` `750`; `/boot` `700` |
| E2 | `zcat /var/lib/pacman/local/filesystem-*/mtree \| grep -E '^\./(proc\|sys\|tmp\|root\|var/tmp\|srv\|boot\|home\|usr\|etc) '` | 0 | Arch `filesystem 2025.10.12-1` ships `./proc mode=555`, `./sys mode=555`, `./tmp mode=1777`, `./var/tmp mode=1777`, `./root mode=750`; no `./` entry (confirms `snapper-eacces-mechanism.md:13`) |
| E3 | same mtree, `grep -nE '^/set\|^\./(boot\|usr\|proc\|sys) '` | 0 | line 2 `/set type=file uid=0 gid=0 mode=755` is a default for **listed** entries only; `/` is not listed |
| E4 | `findmnt -no SOURCE,FSTYPE,OPTIONS /` | 0 | `/dev/mapper/root[/@] btrfs rw,...,subvol=/@` — `/` is a rw btrfs subvolume, not an ro mount |
| E5 | `findmnt -no FSTYPE,OPTIONS /boot` | 0 | `vfat ... fmask=0077,dmask=0077` → `/boot` mode `700` (E1) is mount-option-synthesized, not stored inode metadata |
| E6 | `grep -E '^(Uid\|CapPrm\|CapEff\|CapBnd)' /proc/self/status /proc/1/status` | 0 | self: `Uid 1000`, `CapPrm/CapEff 0000000000000000`; PID 1: `Uid 0`, `CapPrm/CapEff 000001ffffffffff` |
| E7 | `systemctl show -p User,CapabilityBoundingSet,ProtectSystem,ReadWritePaths limine-snapper-sync.service` | 0 | `User=root`, `CapabilityBoundingSet=cap_sys_admin`, `ProtectSystem=no`, `ReadWritePaths=/tmp` |
| E8 | `getfacl -p /` | 0 | owner `root`, group `root`; `user::r-x group::r-x other::r-x`; no extended entries |
| E9 | `pacman -Q filesystem` | 0 | `filesystem 2025.10.12-1` |
| E10 | `man 7 capabilities \| grep ...` (and path_resolution, mkdir) | 1 | local man pages absent (`ls /usr/share/man/man7/capabilities.7*` rc=2); primary text read from man.archlinux.org instead (S1–S3) |

Sources opened 2026-10-19 (≤25-word located quotes):

- **S1** Fedora `filesystem.spec` — https://src.fedoraproject.org/rpms/filesystem/raw/rawhide/f/filesystem.spec, `%files` lines 408–409: “`%defattr(0755,root,root,0755)` / `%dir %attr(555,root,root) /`”; also line 412 `%attr(555,root,root) /boot`, line 443 `/usr/bin` 555. Tier: distro packaging source (not Arch).
- **S2** path_resolution(7) — https://man.archlinux.org/man/path_resolution.7.en § Permissions: “The first group of three is used when the effective user ID of the calling process equals the owner ID of the file.” § Bypassing: “The **CAP_DAC_OVERRIDE** capability overrides all permission checking”; “**CAP_DAC_READ_SEARCH** capability grants read and search permission on directories”. § Step 2: “If the process does not have search permission on the current lookup directory, an **EACCES** error is returned”. Footer: Linux man-pages 6.19, 2026-02-08.
- **S3** capabilities(7) (= S027) — https://man.archlinux.org/man/capabilities.7.en § CAP_DAC_READ_SEARCH: “Bypass file read permission checks and directory read and execute permission checks”. § CAP_FOWNER: “Bypass permission checks on operations that normally require the filesystem UID of the process to match the UID of the file (e.g., chmod(2)…)”.

No S-id assigned to S1/S2 by this seat (registry is Sources' lane).

## Counterexamples to C1 as specified

### CX1 — 0555 on `/` is a shipped distro default, not intrinsically unhealthy (impacts depth)
S1 line 409: Fedora's `filesystem` package **owns `/` at mode 555** by policy. Arch's own package
ships 555 for `/proc` and `/sys` (E2). So `owner-write absent ⇒ defect` is false as a general rule.
On Arch the package declares **no** baseline for `/` (E2/E3; `snapper-eacces-mechanism.md:13`): the
expected mode is *unspecified*, not "0755". The mtree `/set ... mode=755` (E3) is a default for
listed entries and must not be cited as Arch's `/` baseline.
**Impact:** any DEGRADED wording of the form “mode wrong / should be 0755 / unhealthy root” is a
policy overclaim. The Census prompt already forbids an “unsupported default 0755 requirement”; this
is the source that makes the prohibition load-bearing.

### CX2 — whether 0555 blocks a writer depends on the process, not the mode (operability + depth)
E6: PID 1 holds full `CapEff` → CAP_DAC_OVERRIDE → S2 “overrides all permission checking”; 0555 is
irrelevant to it. The census shell (uid 1000, `CapEff=0`) is governed by the **other** triplet
(S2 § Permissions), so owner bits are irrelevant to it too. Only processes whose fsuid equals the
owner **and** lack CAP_DAC_OVERRIDE are affected — on this host, E7's `User=root` +
`CapabilityBoundingSet=cap_sys_admin` unit is exactly that class.
**Counterexample to an implementation shape:** an arm that uses `[ -w "$ROOT" ]`/`test -w`/access(2)
flips its verdict by invoker: non-root → always “not writable” (even at 0755); `sudo` → always
“writable” (even at 0555). Verdict must come from mode **bits** only, never from an access probe.

### CX3 — owner is not necessarily root; owner-bit checks mean different things per owner (depth)
- Fixtures created by the selftest are owned by the invoking user (uid 1000 normally, 0 under sudo).
  Any `uid==0` grading makes every fixture fail or makes the suite invoker-dependent.
- For a non-root owner, missing owner-write is not a lock: the owner may `chmod` its own file (S3
  CAP_FOWNER text — the UID-match rule). The real hazard there is the ownership itself, which a
  bits-only rule reports as HEALTHY at 0755.
- In user-namespaced/containers an unmapped owner surfaces as the overflow uid; the census has no
  baseline for that either.
**Correction:** print `root_uid`/`root_gid` always; **do not grade on uid this round** (no sourced
policy; fixtures cannot be chowned without privilege, so a non-root-owner case is fixtureable only
as “owned by invoker”, which is non-hermetic across uid 0 vs 1000).

### CX4 — special bits and string matching (operability)
E1 shows `/tmp` → `%a`=`1777`. `stat -c %a` yields 3 or 4 digits (setuid 4000, setgid 2000, sticky
1000). An implementation that string-matches `555`/`755`, or slices the last 3 characters after
assuming width, misclassifies `1755`, `2755`, `0555` vs `555`. setgid on `/` changes group
inheritance of new top-level entries; sticky on `/` restricts deletion — neither has a sourced
health baseline.
**Correction:** parse once as octal (`m=$((8#$mode))`) and test masks (`m & 0200`, `m & 0100`);
emit a normalised 4-digit `root_mode=%04o`; special bits verdict-neutral (reported, not graded).

### CX5 — bits-only owner check passes clearly worse states as HEALTHY (operability)
Plan grades only owner write/search. Then:
- `0750`/`0700` (other-search absent) → HEALTHY, yet S2 Step 2 says every non-root lookup through `/`
  returns EACCES — worse than 0555 for a desktop host.
- `0777`/`0775` (group/other write, no sticky) → HEALTHY, yet any local user could rename top-level
  entries.
These are not required by C1's acceptance (0755/0555/unreadable discrimination), so they are a
**coverage gap, not a C1 defect**. Smallest safe move: report `root_other_search=` and
`root_group_other_write=` as printed facts; grading them is a separate claim.

### CX6 — symlink/override validation can fake a pass (operability)
`[ -d "$TSUKUROI_ROOT_DIR" ]` follows symlinks; `stat -c %a` (no `-L`) reports the link itself
(`777`). A symlink-to-dir override then validates as a directory and reads owner-write present →
HEALTHY on a link mode that is meaningless. Also a vfat mount root (E5) reports mount-option-derived
modes. **Correction:** one `stat -c '%F %a %u %g'` call; validate `%F == directory` from that same
call (`-L` explicitly or not, but consistent); call the printed value the *observed* mode, not a
*stored* or *intended* mode.

### CX7 — “unreadable metadata” fixture is not hermetic under root (operability)
A chmod-000-parent fixture yields EACCES for uid 1000 but succeeds under sudo (S3
CAP_DAC_READ_SEARCH; S2). The fixture tree is also hashed by `fx_hash` (`tools/tsukuroi-census.sh:1750-1753`),
which may itself fail on a 000 dir. **Correction:** model unavailable metadata with a **missing path**
(stat rc≠0) and non-directory with a **regular file**; skip or guard any permission-based case with
`[ "$(id -u)" -ne 0 ]` and record the skip in output.

### CX8 — default fixture mode depends on umask (operability)
`mktemp -d` creates 0700; `mkdir -p` honours umask. A fixture that asserts `root_mode=0755` without
an explicit `chmod 0755` is umask-dependent. **Correction:** `chmod 0755` the default root fixture,
`chmod 0555` the 0555 case, explicitly.

### CX9 — mount state is orthogonal (depth)
E4: `/` is rw btrfs here, so 0555 is not an ro mount; conversely a 0755 `/` on an ro mount (EROFS) or
with an immutable inode flag is still unwritable. A HEALTHY root arm must not be worded as
“writable”. The plan's “no mount inference” is correct; keep the printed field a DAC-metadata fact.

## Recommended threshold and failure arm (smallest safe correction)

Packages-note fields, always printed, including on every packages BLOCKED early-return path:
`root=<path> root_type=<%F> root_mode=<%04o> root_uid=<n> root_gid=<n>`.

| Condition (from one `stat` call, bits by octal mask) | Arm | Named reason (wording bound) |
|---|---|---|
| stat rc≠0, empty or non-numeric output | BLOCKED | `root_meta=unavailable` — never HEALTHY |
| `%F` ≠ `directory` | BLOCKED | `root_meta=non-directory` |
| `m & 0200 == 0` or `m & 0100 == 0` | DEGRADED | `root_owner=no-write|no-search [unknown: no package baseline for /; capability-bounded owner processes denied]` — an **unresolved unknown** per the census vocabulary (`tools/tsukuroi-census.sh:51`), **not** “wrong mode” |
| otherwise | HEALTHY for this arm | metadata fact only; not a writability claim |
| setuid/setgid/sticky, other-search, group/other write, uid≠0 | verdict-neutral | printed facts only this round |

Justification for DEGRADED-as-unknown rather than defect: CX1 shows 0555 can be intended; the host
does run a capability-bounded root writer (E7) with a recorded errno 13 history
(`snapper-eacces-mechanism.md:11`), so the fact is operationally relevant here, but its causal link
remains `[inf]` per that note's falsifier (lines 23–30, not run). The arm must not cite the journal
count as proof.

## Verdict on C1 (critic scope)

- Not falsified **if** the implementation follows the table above; falsified-in-shape by CX2 (access
  probe), CX4 (string match), CX6 (symlink validation), CX7/CX8 (non-hermetic fixtures) if any of those
  shapes lands. Re-review needed once `tools/tsukuroi-census.sh` changes land; nothing here is a PASS.
- Fixable defects: CX2, CX4, CX6, CX7, CX8 (implementation shape). Tradeoffs the judge should hold:
  CX1/CX3 (DEGRADED must be worded as unknown, not policy), CX5 (coverage gap, separate claim).
- Unrun: selftest, live census, any privileged discriminator. Installs: none.
