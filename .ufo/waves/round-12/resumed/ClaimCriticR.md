# ClaimCriticR — round 12 resumed, C1 falsification (root metadata census arm)

Seat: critic, author-side seat review. This is **not** independent non-author verification. I used static evidence and non-root reads only: no sudo, no host writes, no installs, no tests, selftest, build, lint or census runs. The only file I wrote is this one.
Axes: operability (the gate gives a correct verdict that does not depend on who runs it) and depth (claims are grounded, with no policy overclaim).

## 0. State at review time (2026-10-20)

| # | Command (uid 1000, read-only) | rc | Observation |
|---|---|---|---|
| R0 | `git status --short`; `git log -1 --format=%H` | 0 | HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`; `tools/tsukuroi-census.sh` **unmodified** (not in status) |
| R0b | `sha256sum`/`wc -l tools/tsukuroi-census.sh` | 0 | `1045244387ffcd5d…`, 2402 lines, the same blob as the inherited baseline |
| R0c | grep `root_mode\|root_uid\|ROOT_DIR\|TSUKUROI_ROOT\|root_meta\|root_owner` in `tools/` | — | 0 matches. **C1 has not landed.** No `resumed/Census.md` exists. |

Every finding below therefore targets the contract: the `CensusR` prompt in `resumed/spec.json` ("worsen verdict for missing owner write/search as named DEGRADED, unavailable/non-directory BLOCKED, no unsupported default 0755 requirement"). It also covers the competing seat designs. A re-review is required once the arm lands. **Nothing here is a PASS.**

## 1. Re-verified inherited observations (fresh runs this pass)

| # | Command | rc | Observation (now) | Inherited id |
|---|---|---|---|---|
| V1 | `/usr/bin/stat -c '%a %A %f %u:%g %F %n' / /proc /sys /tmp /root /boot` | 0 | `/` `555 dr-xr-xr-x 416d 0:0 directory`; `/proc`, `/sys` 555; `/tmp` `1777 drwxrwxrwt`; `/root` 750; `/boot` 700 | E1 reused |
| V2 | `findmnt -no SOURCE,FSTYPE,OPTIONS /` | 0 | btrfs `rw,…,subvol=/@`. 0555 is not an ro mount. | E4 reused |
| V3 | `grep -E '^(Uid\|CapPrm\|CapEff\|CapBnd\|NoNewPrivs)' /proc/self/status` | 0 | Uid 1000, CapPrm/CapEff 0, CapBnd `000001ffffffffff` | E6 reused |
| V3b | same fields from `/proc/1/status` | 0 | Uid 0, CapPrm/CapEff `000001ffffffffff` | E6 reused |
| V4 | `systemctl show -p User,CapabilityBoundingSet,AmbientCapabilities,ProtectSystem,ReadWritePaths,NoNewPrivileges limine-snapper-sync.service` | 0 | `User=root`, `CapabilityBoundingSet=cap_sys_admin`, `AmbientCapabilities=` (empty), `ProtectSystem=no`, `ReadWritePaths=/tmp`, `NoNewPrivileges=yes` | E7 reused, extended |
| V5 | `getfacl -p /` | 0 | root:root; `user::r-x group::r-x other::r-x`; no extended entries | E8 reused |
| V6 | `pacman -Q filesystem coreutils systemd`; `pacman -Qo /` | 0 / 1 | filesystem `2025.10.12-1`, coreutils `9.11-2`, systemd `261.2-1`; `error: No package owns /` | E9 reused |
| V7 | `zcat …/filesystem-*/mtree \| grep -nE '^/set\|^\./(proc\|sys\|tmp\|root\|…) '` | 0 | no `./` entry; `./proc`, `./sys` `mode=555`; `./tmp`, `./var/tmp` `mode=1777`; `./root` `mode=750`; line 2 `/set … mode=755` | E2/E3 reused |
| V8 | `/usr/bin/stat -c '%04a\|%#a\|%a' /tmp /` (GNU stat 9.11) | 0 | `1777\|01777\|1777`; `0555\|0555\|555` | new |
| **N1** | `grep -rnE '^[a-zA-Z]+[!+-]* +/ ' /usr/lib/tmpfiles.d/ /etc/tmpfiles.d/` | 0 | **`/usr/lib/tmpfiles.d/root.conf:10:z / 555 - - -`** | **new** |
| N2 | `pacman -Qo /usr/lib/tmpfiles.d/root.conf`; `systemd-tmpfiles --cat-config \| grep …` | 0 | `owned by systemd 261.2-1`; effective merged config line 338 `z / 555 - - -`; no `/etc/tmpfiles.d` override | new |
| N3 | `systemctl show -p ExecStart,ActiveState,Result systemd-tmpfiles-setup.service` | 0 | `systemd-tmpfiles --create --remove --boot --exclude-prefix=/dev`; `active`/`success`; started this boot 2026-10-19 22:48:23 -03 | new |
| N4 | `grep -nE '\] (upgraded\|installed) (systemd\|snapper\|limine-snapper-sync) \(' /var/log/pacman.log` | 0 | systemd 261.1-1 installed 2026-10-03 (install day), upgraded to 261.2-1 on 2026-10-11; snapper and limine-snapper-sync were installed the same install day | new |

Opened sources (≤25-word located quotes). This seat assigns no S-id; the registry belongs to the Sources lane.
- **T1** tmpfiles.d(5), https://man.archlinux.org/man/tmpfiles.d.5.txt (footer `systemd 262.1`). Lines 327–331, `z`: “Adjust the access mode, user and group ownership … of a file or directory, if it exists.” Lines 508–509, Mode: “the access mode of listed inodes is set to the specified mode regardless of whether it is created anew, or already existed.”
- **T2** systemd NEWS, https://raw.githubusercontent.com/systemd/systemd/main/NEWS, section `CHANGES WITH 261:` (header line 1015), lines 1282–1283: “A new tmpfiles.d/root.conf has been added that sets permissions on the root directory (/) to 0555.” Lines 1284–1286 add: “useful as a general safety net.” The upstream commit is `7b2a10b594d7` (2026-04-08), which only adds `tmpfiles.d/root.conf`. GitHub compare `v261...7b2a10b5` reports `behind`, ahead 0, so the commit is in v261.
- **T3** stat(2), https://man.archlinux.org/man/stat.2.txt (Linux man-pages 6.19, 2026-02-08), lines 40–42: “No permissions are required on the file itself, but … execute (search) permission is required on all of the directories in path that lead to the file.”
- **T4** inode(7), https://man.archlinux.org/man/inode.7.txt (man-pages 6.19). Line 226: `S_ISUID 04000 set-user-ID bit (see execve (2))`, with no directory meaning given. Lines 246–250: setgid on a directory: “files created there inherit their group ID from the directory.” Lines 256–258: sticky on a directory: a file “can be renamed or deleted only by the owner of the file, by the owner of the directory, and by a privileged process.”
- I reused path_resolution(7) and capabilities(7) (S027) quotes from the inherited S2/S3 without reopening them this pass. Treat them as inherited.

## 2. Reuse / reject / correct the inherited `ClaimCritic.md`

| Inherited item | Ruling | Why |
|---|---|---|
| CX1 “0555 not intrinsically unhealthy” (Fedora `%attr(555,root,root) /`) | **REUSE, strengthened** | The host itself now supports it: N1–N3 + T1/T2 show systemd ≥261 declares `/` 0555 here, not just Fedora |
| CX1 “On Arch … the expected mode is *unspecified*” | **CORRECT** | The intended mode is unspecified only by **pacman/filesystem mtree** (V6/V7). systemd 261.2's tmpfiles `z / 555` specifies it, and that rule is effective in the merged config (N2). The live 0555 matches the host's declared state. |
| Recommended wording `[unknown: no package baseline for /; …]` | **REJECT** | It is literally true about pacman, but false by omission: a package-shipped baseline (systemd) exists and says 0555 |
| CX2 (no access(2)/`test -w` probe; bits only) | REUSE | V3/V3b are unchanged |
| CX3 (do not grade on uid; fixtures are invoker-owned) | REUSE | — |
| CX4 (octal parse, 4-digit normalize) | REUSE + refine | V8: GNU `%04a` gives `0555`/`1777` directly, so no printf re-format is needed. Still validate as `[0-7]{4}` before `$((8#…))` (Security S8). |
| CX5 (other-search/group-write gaps) | REUSE as a coverage gap | — |
| CX6 (symlink consistency) | REUSE | `C1Review` F7 (`stat -L`) and `Security` S5 (lstat, symlink→BLOCKED) conflict. Either is safe if only one call decides; the parent must pick one and the selftest must pin it |
| CX7/CX8 (hermetic unreadable case; explicit chmod) | REUSE | — |
| CX9 (mount state orthogonal) | REUSE | V2 |
| E10 “man pages absent locally” | Historical | Not re-checked. This pass used man.archlinux.org text. |

## 3. Counterexamples to C1 as contracted

### K1 — HIGH (operability + depth): the contracted DEGRADED on this host is permanent and not actionable
- The contract says “missing owner write/search → named DEGRADED”. Live `/` is `0555 0:0` (V1), so C1 prints DEGRADED on every live run.
- The state is not drift. systemd-tmpfiles-setup runs `--create … --boot` every boot (N3) and applies `z / 555` “regardless of whether it … already existed” (T1 508–509). [inf, not executed] An operator `chmod 755 /` would be set back to 0555 at the next boot unless `/etc/tmpfiles.d/root.conf` masks it.
- Today the live rollup does not move: packages is already DEGRADED from `drift=2` (`before.json:6`, `CensusScribeR.md:37`). Once drift clears, the packages plane would still stay DEGRADED, and only by overriding a systemd-shipped default could anyone clear it. That is an alarm with no clean remediation.
- **Impact:** if the arm worded this as a defect, it would be the “unsupported default requirement” the contract forbids, moved from 0755 to the owner bit (`QUALITY.md` #15: “not universal mode policy or process writability”).

### K2 — HIGH (depth, sibling corpus, outside my write scope): the current knowledge note recommends a self-reverting fix
- `corpus/knowledge/snapper-eacces-mechanism.md:13` says “no package metadata baseline for `/`'s mode”. That is true for pacman only (see the K1 correction).
- `:34` suggests “restore the expected owner-write permission (for example, `chmod 755 /`)” and “determine why `/` is `0555`”. The *why* is now answered by N1/T2. The suggested fix contradicts the systemd-declared mode and is reverted at boot [inf, T1+N3].
- [inf] Reframed mechanism: on this host, the incident is the interaction between systemd's 0555 `/` (installed since day 0, N4) and a root unit whose bounding set lacks `CAP_DAC_OVERRIDE` (V4). The unit's capability set relative to the declared root mode is the actionable surface, not the mode. The causal link is still unproven; the falsifier at `:23–30` was not run.
- QUALITY #10 sweep is required before any correction. This seat does not edit that file.

### K3 — HIGH (operability): an invoker-conditioned verdict is a regression
- `C1Review.md:34` / `OverlapHost.md:101` propose DEGRADED only when probe euid == owner uid, otherwise HEALTHY.
- Counterexample: the same `/` (0555 0:0) gives HEALTHY under uid 1000 and DEGRADED under `sudo`. The verdict then depends on the invoker, not on the host, which is the CX2 failure in a new form.
- Reject this design. The verdict must be a function of `(mode, type, stat rc)` only. `root_uid` stays a printed fact.

### K4 — MEDIUM (operability): the live BLOCKED arm is effectively unreachable by DAC
- T3: `stat` needs search permission only on the directories *leading to* the path. `/` has none, so DAC can never make `stat /` fail with EACCES.
- The live BLOCKED arm is reachable only through an override path, a missing binary, or [inf] an LSM getattr denial (none tested).
- Consequence: “unreadable metadata” discrimination is a fixture-only property. Its proof must be hermetic, using a missing path and a regular file, plus an existing directory with a stat-failure shim (MutationPlan M3). A live run cannot show it. Do not claim live coverage of the BLOCKED arm.

### K5 — MEDIUM (operability): fixture mutation detection is blind to directory mode
- `tools/tsukuroi-census.sh:1748`: `fx_hash` is `find "$1" -type f -exec sha256sum`, which covers regular-file **content** only.
- Counterexample: a buggy arm that `chmod`s `$FX/root`, or an empty root fixture whose mode changes, passes `fx_no_mutation` (`:1750-1753`) unchanged.
- The resumed CensusR prompt explicitly asks for “fixture metadata mode/digest mutation detection”. That needs a mode/owner component, e.g. `find "$1" -printf '%M %U %G %p\n'` folded into the digest. This is not present at HEAD.

### K6 — LOW (operability): token format drift across seats
- `MutationPlan.md:27` expects `root_mode=755`; the inherited ClaimCritic, AclSemantics and Security designs expect `root_mode=0555`/`%04a`.
- Pin one format, preferably `%04a` (V8). Selftest regexes should anchor `root_mode=0555( |$)`, so that `0555` vs `555` mismatches and the live-root leak (`0555 0:0`) cannot pass by substring.

### K7 — LOW (depth): special bits
- Per T4, S_ISUID has no documented directory meaning. Setgid changes group inheritance of new entries, and sticky limits rename/delete. None of the three changes the owner write/search bits.
- Counterexample to string matching: `1755` (sticky) and `2755` (setgid) must read owner-write *present*; `1555` must read *absent*. Only `$((8#$m & 0200))` / `0100` on the validated 4-digit value is correct. The special bits are printed and verdict-neutral; no source grounds them as unhealthy on `/`.

### K8 — LOW (depth): owner is not necessarily root
- Fixtures are invoker-owned (uid 1000, or 0 under sudo). A container or user-namespace `/` can show an overflow or mapped uid.
- No source gives a health rule for a non-root owner of `/`. Print the owner and do not grade it this round. An invoker-independent “non-root owner” fixture cannot be built without `CAP_CHOWN`, so record it as a named skip, never a pass.

## 4. Recommended threshold and failure arm (smallest safe correction)

Fields, always on the `PLANE packages` line, composed in `main`, so that the early returns at `:536-570` cannot erase them:
`root_mode=<%04a> root_uid=<n> root_gid=<n> root_owner_write=<present|absent> root_owner_search=<present|absent>`, plus `root_meta=<ok|unavailable(<cls>)|non-directory>`.

| Condition (one `LC_ALL=C stat` call; mode validated `[0-7]{4}`; bits by octal mask) | Arm | Wording bound |
|---|---|---|
| stat rc≠0, empty or unparseable output | **BLOCKED** | `root_meta=unavailable(<cls>)`, never HEALTHY |
| type ≠ directory | **BLOCKED** | `root_meta=non-directory` |
| `m&0200==0` or `m&0100==0` | **DEGRADED** (contract) as a *named unknown*, not a defect | `root_owner_write=absent [unknown: intended mode not assessed by census]`. Do **not** print “no baseline”, “unspecified”, “wrong”, “should be 0755”, “read-only” or “not writable” (K1/K2, V2) |
| otherwise | HEALTHY for this arm | a metadata fact; never “writable” |
| setuid/setgid/sticky, other-search, group/other write, uid≠0, probe euid | verdict-neutral | printed facts only |

**Tradeoff the canonical judge must rule on, not fix here:** the contract-literal DEGRADED arm is permanent on this host because systemd re-asserts 0555 (K1). I see two defensible outcomes:
- (a) Accept a permanent named-unknown DEGRADED as an honest “intent not assessed” and record the expected live change explicitly. NoOralReview risk 1 asks for this.
- (b) Narrow the arm to reporting only for owner-write, keeping BLOCKED for unavailable/non-directory and keeping the selftest discrimination through printed fields plus BLOCKED. This changes the claim's contract, which is the parent's call.

I do not recommend a third option, a census-side tmpfiles read that suppresses the verdict. It adds a new probe surface and policy inference beyond C1.

## 5. Verdict (critic scope)

- **C1 falsified as a health claim:** “0555 on `/` is unhealthy” is false on this host's own declared policy (N1–N3, T1, T2). C1 survives only as an **observation arm** worded as an unknown (§4).
- **C1 not yet assessable as an implementation:** the arm has not landed (R0). The landed revision needs re-review against K3, K5, K6 and K7 and inherited CX2, CX4, CX6, CX7 and CX8.
- **Fixable defects:** K5 (the hash omits mode), K6 (format), K3 (reject the invoker-conditioned verdict), plus the inherited shape defects.
- **Tradeoffs for the judge:** K1 (permanent DEGRADED), K4 (BLOCKED is fixture-only in proof).
- **Cross-lane:** K2 (stale knowledge note and remediation) belongs to the Matrix/Sources/parent lanes. The tmpfiles.d(5) + NEWS v261 + `/usr/lib/tmpfiles.d/root.conf` triad needs an S-id from Sources if anyone cites it.
- **Unrun:** selftest, live census, any privileged discriminator, chmod/reboot revert behaviour (K1/K2 revert is [inf] from T1+N3).
- **Installs:** none.
