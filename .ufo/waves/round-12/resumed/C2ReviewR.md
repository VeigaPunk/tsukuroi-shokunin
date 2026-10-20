# C2 resumed review — root EACCES decision matrix (round-12)

Seat: C2ReviewR (leaf, author-side static review; NOT independent non-author verification).
Repo: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Baseline HEAD b76b5c377eaee3e3d8d47fdddde977828d05dbd5.
Inputs reviewed: `corpus/knowledge/root-dac-decision-r12.{md,json}` (matrix now present, uncommitted),
`corpus/knowledge/snapper-eacces-mechanism.md`, `.ufo/waves/round-12/{discriminator-smoke,error-order-smoke}.json`,
inherited `.ufo/waves/round-12/C2Review.md` (historical; its "matrix not present" status is superseded and NOT carried as current).

## Verdict

**NOT PASSED.** The matrix now exists and its branch set (B1 DAC, B2 EROFS, B3 capability-bound, B4 EEXIST) is
a real discriminator set rather than advice. Three High defects block a PASS on the two judged axes:
(F1) the decision procedure has no per-operation errno priority and the stated order is wrong for the Btrfs
subvolume ioctl; (F2) B2 treats `ProtectSystem=full` as a read-only signal for arbitrary paths, which systemd.exec(5)
does not support; (F3) B3's bounding-to-effective causal link cites the wrong authority and omits the inheritable
term. Medium defects: SC1–SC3 fixture-ownership mislabel (F4), time-bounded absence exclusion (F5), unestablished
target path (F6). No privileged or state-changing command was executed by this seat.

## Commands and exit codes (all read-only; fetches are to /tmp/c2r12, outside repo)

- `curl -fsSL` raw.githubusercontent.com/torvalds/linux master: `fs/namei.c` rc=0, `fs/btrfs/ioctl.c` rc=0, `fs/namespace.c` rc=0, `kernel/capability.c` rc=0.
- `curl -fsSL` raw.githubusercontent.com/systemd/systemd main `man/systemd.exec.xml` rc=0.
- `curl -fsSL` raw.githubusercontent.com/kdave/btrfs-progs devel `libbtrfsutil/subvolume.c` rc=0.
- `curl` mkerrisk/man-pages `man/man2/access.2` rc=22 (404); access(2) read via man.archlinux.org instead.
- `curl` torvalds/linux `security/commoncap.c` rc=0 (fetched to /tmp/c2r12); `grep` of cap_capable (commoncap.c line 82): `return cap_raised(cred->cap_effective, cap) ? 0 : -EPERM;` (line 124 `int cap_capable(const struct cred *cred, …)`). Background job bg_103 completed; result read.
- Read via `read` (man.archlinux.org, rendered): mkdir(2) (footer Linux man-pages 6.19), access(2), systemd.exec(5), capabilities(7).
- Local reads: matrix md/json, both smoke fixtures, snapper note, inherited C2Review.
- Local greps only (`grep`/`_grep`); no `sed`/`perl` edits.
- NOT run: sudo, systemd-run, snapper, chmod/chown, btrfs subvolume ops, pacman (any), journalctl re-query, any build/test/lint.
- Installs/updates: none.

## Findings (by severity)

### F1 — High: decision procedure has no errno priority; step order is wrong for the Btrfs subvolume ioctl
- Matrix `decision_procedure` (JSON lines 129–136): step 1 B4 (target present → EEXIST family), step 2 B2 (ro → EROFS), step 3 B1 (DAC/search), step 4 B3, step 5 conjunction, step 6 UNCLASSIFIED. No short-circuit rule and no per-operation priority are stated; B4 is applied first for every operation.
- Source (kernel master fetched 2026-10-20; host kernel 7.2.3-arch1-3 NOT verified to match):
  - Subvolume create path, the one libbtrfsutil issues: `btrfs_util_create_subvolume_fd` → `ioctl(parent_fd, BTRFS_IOC_SUBVOL_CREATE_V2)` (libbtrfsutil/subvolume.c:773) → `btrfs_ioctl` dispatch `BTRFS_IOC_SUBVOL_CREATE_V2` → `btrfs_ioctl_snap_create_v2(file,argp,true)` (btrfs/ioctl.c:5561, 1249–1289; no `capable()` on this path) → `__btrfs_ioctl_snap_create` (1160).
  - Order inside it: `mnt_want_write_file(file)` at 1172 → EROFS **first**; name checks 1182–1185 (EEXIST for "." / "..", EINVAL for '/') → `btrfs_mksubvol` (881) → `start_creating_killable` (namei.c 3454–3464) which calls `lookup_one_common` (3114–3122) → `inode_permission(…, MAY_EXEC)` → EACCES on missing parent search **before** the existence check → `may_create_dentry` at 897 → `child->d_inode` → EEXIST (namei.c 3735–3736) **before** `inode_permission(MAY_WRITE|MAY_EXEC)` at 3742 → EACCES.
  - Resulting priority for the subvolume ioctl: **EROFS > EACCES(search) > EEXIST > EACCES(write) > success**.
  - Ordinary mkdir (`filename_create`, namei.c 5063–5135): `mnt_want_write` stored in `error` at 5084 but `start_dirop` runs first; EEXIST from `lookup_one_qstr_excl` (1822–1824) returns before `if (unlikely(error)) goto fail;`. Resulting priority: **EEXIST > EROFS > EACCES(write)**.
  - The two operations therefore disagree on EROFS vs EEXIST. The matrix's B4-first order holds only for ordinary mkdir (consistent with the isolated smoke), and the matrix's own B4 limit says not to extrapolate it to the Btrfs ioctl — yet the procedure applies it generically.
- Consequence: on the Btrfs ioctl, an existing target under a read-only mount yields EROFS, not EEXIST; an unsearchable parent with an existing child yields EACCES, not EEXIST. The procedure as written would mislabel both.
- Fix (matrix owner): state priority per operation (ordinary mkdir vs subvolume ioctl), cite the line anchors above with the kernel tag used, and make the procedure stop at the first errno in the operation's priority list, or list all firing branches explicitly.
- Smoke evidence does not cover EROFS-vs-EEXIST or search-EACCES-vs-EEXIST on either path (no ro mount; search denial not fixtured). Status: source-grounded, unfixtured.

### F2 — High: B2 treats `ProtectSystem=full` as a read-only signal for the target path; systemd.exec(5) does not support that
- Matrix B2 (JSON lines ~40–65): interpretation says "unit-side read-only remount (ProtectSystem=full/strict …)"; `expected_signal`: "ro present in the mount options, or ProtectSystem=full/strict, or ReadOnlyPaths= covering the target path".
- Source (systemd main `man/systemd.exec.xml` ~1501–1510): "mounts the /usr/ and the boot loader directories (/boot and /efi) read-only … If set to full, the /etc/ directory is mounted read-only, too. If set to strict the entire file system hierarchy is mounted read-only, except for /dev/, /proc/ and /sys/."
- So `full` does not make `/` or `/.snapshots` read-only. Only `strict` (or a `ReadOnlyPaths=` covering the target) can produce B2 for a root-level target.
- The matrix's quoted S028 `strict` sentence is accurate; the `full` mention is unsupported and must be removed from B2 interpretation, expected_signal, and any SC5-style example. Add: `full` covers only /usr, /boot, /efi, /etc.
- The ReadWritePaths= quote (systemd.exec.xml 1839–1843) is accurate: "cannot be used to gain write access to a file system whose superblock is mounted read-only".

### F3 — High: B3 causal chain cites the wrong authority and omits the inheritable term; the discriminator is configured text, not effective capability
- B3 evidence cites S028 (bounding text, accurate), S027 (accurate), and S034 access(2) DESCRIPTION ("for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities") — verified verbatim on man.archlinux.org/man/access.2.
- S034 describes access(2)/faccessat, which uses the real UID and the permitted set. It does not govern the kernel's create check. The create check uses `capable_wrt_inode_uidgid` (kernel/capability.c 490–496) → `ns_capable` (330–362) → `security_capable(current_cred(), …)` → `cap_capable` (commoncap.c 124), which tests `cred->cap_effective` (commoncap.c 82). Citing S034 as B3 support is a misapplied authority, even though the matrix's own limit paragraph half-acknowledges it.
- capabilities(7) execve rule, verified (capabilities.7 text at lines ~960–963, ~1070–1076, ~1125–1128): `P'(permitted) = (P(inheritable) & F(inheritable)) | (F(permitted) & P(bounding)) | P'(ambient)`; and "the bounding set masks the file permitted capabilities, but not the inheritable capabilities."
  - Therefore the bounding set alone does not remove CAP_DAC_OVERRIDE if it arrives via the inheritable set. The claim "bounding omits DAC_OVERRIDE ⇒ root is DAC-bound" needs the systemd-specific clearing of inheritable (systemd.exec.xml 870–871: the option "also affects the respective capabilities in the effective, permitted and inheritable capability sets") — quoted accurately by the matrix — and must cite both documents.
- The B3 interpretation states as fact that "the process's bounding, effective, permitted and inheritable sets contain only CAP_SYS_ADMIN". This is [inf] from configuration: the unit is inactive (`ActiveState=inactive`), so no CapBnd/CapInh/CapEff was read from a live process. The matrix's B3 limit says so; the interpretation does not.
- Discriminator gap: the only runnable B3 signal is `systemctl show` text. A live-process discriminator (`/proc/<pid>/status` CapBnd/CapInh/CapEff of the unit's main process while running) is named nowhere as a runnable check; the bounded-vs-unbounded same-op comparison is operator-only and not run. So B1∧B3 is not separated from alternatives by any runnable test in the matrix.
- SC4 ("uid 0 with cap_dac_override in the bounding set" → success) is correct only via the root execve rule (P'(permitted)=P(bounding)|P(inheritable)); the scenario should say so.
- Fix (matrix owner): cite capabilities(7) execve formula + systemd.exec(5) inheritable sentence for B3; drop S034 as B3 authority (keep only as the access(2) caveat); label effective/inheritable as [inf] for the inactive unit; name the live `/proc/<pid>/status` probe as the discriminator and mark it not run.

### F4 — Medium: SC1–SC3 fixture ownership does not match the recorded fixtures
- `discriminator-smoke.json` `fixture_code`: `TemporaryDirectory; chmod(parent,0555); mkdir(child); chmod(parent,0755); …`. The parent is created by the uid-1000 process and is therefore owned by uid 1000. No chown is recorded; no stat or getfacl of the fixture parent is recorded (read-only discriminators cover only `/`, `/.snapshots`, and the unit).
- Matrix SC1 and SC2: "parent 0555 root:root, base ACL entries only". SC3: "parent 0755 root:root". The fixtures tested owner-class (uid 1000 = owner, class r-x → no write → EACCES), not the other-class shape of the host (`other::r-x`, root:root). "base ACL entries only" has no fixture evidence.
- The basis strings ("actual isolated ordinary mkdir: parent 0555 + new target → EACCES") are accurate for the owner-class fixture only. Stated root:root equivalence is unsupported.
- `error-order-smoke.json` likewise records "restored ownerwrite for cleanup" with no ownership or ACL stat.
- Fixture results themselves are consistent with ordinary-mkdir kernel order (filename_create/may_create_dentry): 0555+new → EACCES; 0555+existing → EEXIST; 0755+new → success; 0755+existing → EEXIST.
- Fix (matrix owner, no privilege needed): either relabel SC1–SC3 as "owner-class (uid 1000 owns the fixture parent)", or record `stat`/`getfacl` of the fixture parent in the JSON. The root:root non-owner case remains untested and must be listed as residual (it would need a root-owned fixture; operator-only).
- Also unrecorded: "uid 1000 (no capabilities)" — no CapEff read of the fixture process.

### F5 — Medium: absence exclusion is time-bound but procedure step 1 treats it as settled
- Procedure step 1: "absent → collision excluded for create-class checks". The B4 limit says an observed errno:13 does not establish target absence for the tool's own operation, and the absence observation is dated 2026-10-19 (`/.snapshots` stat rc=1; snapper 0 rows).
- Fix: "absent at query time" must not be used to exclude B4 for the historical 2026-10-16..19 events; B4 remains open for those events unless absence is established contemporaneously (no such evidence exists).

### F6 — Medium: failing create target is not established; SC7 assumes `/.snapshots` under parent `/`
- SC7 target `/.snapshots` and parent `/` are assumptions. The journal line identifies the emitter (`Btrfs.cc(createConfig):139`, from the inherited C2 and snapper notes), not the target name or the parent passed to the ioctl. Mark as [inf]; the walk in md §4 needs the same qualifier.

### F7 — Low/Medium: independence claim holds literally, but the root observation is shared with C1
- Matrix states C2 reads no census script/output/fixture/root-metadata census field. Literally true: it reads `stat -c '%a %U:%G' /` and `getfacl -p /` directly.
- The same single reading of `/` (555 root:root, base ACL) is the observation both lanes depend on. It is one reading, not two confirmations; do not present as independent corroboration.

### F8 — Low: remediation must stay gated (carried from inherited review, still valid)
- md §5/operator options (`chmod 755 /`) is labeled operator-only; the discriminator for that action is F1/F3 dependent. Keep gated on the B1∧B3 discriminator as corrected; this seat does not judge whether `0555` is unhealthy (C1 scope).

## Branch-by-branch: is each a causal discriminator?

| Branch | Discriminator | Causal? | Blocking defect |
|---|---|---|---|
| B1 DAC write/search | stat/getfacl parent + prefixes; expected 0555 base-only | Yes for write/search denial; predicts success for 0755 (fixture SC3) | F4 fixture labels; search variant not fixtured |
| B2 EROFS | findmnt rw/ro; ProtectSystem; ReadOnlyPaths | Yes (ro predicts EROFS); host rw → excluded | F2 (`full`); F1 ordering for ioctl |
| B3 capability-bound | `systemctl show` bounding text | Only conjunct with B1; configured text not live effective | F3 (authority, inheritable, inactive unit) |
| B4 EEXIST | stat target; snapper list | Yes for EEXIST family (ordinary mkdir fixture) | F1 ordering on ioctl; F5 time-bound absence |
| B1∧B3 conjunction | none runnable without privilege | Not separated from alternatives | Operator-only `systemd-run`/live `/proc` probe not run |

## Checks the parent should run once after integration

1. Re-read `corpus/knowledge/root-dac-decision-r12.json` B2 and B3 and `decision_procedure` after the matrix owner's fixes; confirm no `ProtectSystem=full` in B2 and that per-operation priority lists exist.
2. Re-check the kernel line anchors cited (namei.c 1822–1824, 3735–3742, 5084–5100; btrfs/ioctl.c 1172, 1182–1188, 897; libbtrfsutil/subvolume.c 773) against the kernel tag the matrix names, and record the tag.
3. Confirm SC1–SC3 labels against `discriminator-smoke.json` fixture_code after relabel or added stat evidence.
4. Operator-only (not for this seat): live `/proc/<pid>/status` of the unit during a run, or the `systemd-run` bounded-vs-unbounded falsifier in `snapper-eacces-mechanism.md`.

## Residual risks and verification gaps

- Kernel source is master as of 2026-10-20, not host kernel 7.2.3-arch1-3; line anchors may drift. Host tag not verified.
- `commoncap.c` cap_capable effective-set check: RESOLVED (bg_103 completed; `cap_raised(cred->cap_effective, …)` read). Residual: the kernel tag is master 2026-10-20, not the host kernel.
- `filename_create` EEXIST-before-EROFS ordering read from master; start_dirop's internal lookup was read at 2905–2920 only, not traced to every branch.
- libbtrfsutil and btrfs-progs are devel branch, not the host-installed version.
- ProtectSystem/CapabilityBoundingSet text read from systemd main, not the host systemd version.
- The falsifier and every predicted rc in the notes remain [inf]; nothing was executed.
- Not independent non-author verification; no claim of PASS is made.
- Host journal count (9) and unit state were taken from the matrix's own observations; not re-queried by this seat.

## Sources (fetched/read 2026-10-20; /tmp/c2r12, outside repo)

- torvalds/linux master: fs/namei.c (filename_create 5063–5135; may_create_dentry 3731–3743; lookup_one_common 3114–3122; __start_dirop 2905–2920; start_creating_killable 3438–3464; lookup_one_qstr_excl 1790–1824); fs/btrfs/ioctl.c (__btrfs_ioctl_snap_create 1160–1188; btrfs_mksubvol 881–897; btrfs_ioctl_snap_create_v2 1249–1289; dispatch 5554–5561; mnt_want_write_file 1172); fs/namespace.c (mnt_want_write_file 571–580); kernel/capability.c (capable_wrt_inode_uidgid 490–496; ns_capable_common 330–341).
- btrfs-progs devel: libbtrfsutil/subvolume.c (btrfs_util_create_subvolume_fd, ioctl BTRFS_IOC_SUBVOL_CREATE_V2 at 742–773).
- systemd main: man/systemd.exec.xml (ProtectSystem= ~1501–1510; ReadWritePaths/superblock 1839–1843; CapabilityBoundingSet= 860–884 incl. effective/permitted/inheritable at 870–871).
- man.archlinux.org (rendered, footer as shown): mkdir(2) ERRORS (Linux man-pages 6.19; EACCES/EEXIST/EROFS quotes match matrix S035); access(2) DESCRIPTION and NOTES (S034 quotes match matrix); systemd.exec(5); capabilities(7) (CAP_DAC_OVERRIDE quote matches S027; execve P'(permitted) rule and bounding/inheritable note).
- Matrix S-rows cited: S027, S028, S034, S035 — all quotes checked above against fetched text; no mismatch except the F2 `full` extension (not in quotes) and the F3 authority misapplication.
