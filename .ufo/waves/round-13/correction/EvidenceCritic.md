# EvidenceCritic — round 13: SC1/SC2 same-mode transfer (root-owned hypothetical vs caller-owned fixture)

Axes: **depth** (primary), calibration (label precision). Adjacency untouched. Advisory only; no admission.

## Verdict
The owner→other transfer for **0555** is a *valid inference*, but only under premises that neither r12
nor the current r13 draft states. Draft `root-dac-correction-r13.json` `fixture_identity` (lines 142–154)
gets the headline right (`executed_root_owned_fixture: false`) but (a) overstates what the fixtures
recorded, (b) cites S035 for a rule S035 does not contain, (c) asserts an unsupported universal for SC2
("not from ownership"), and (d) its `full_discriminator` (96–104) misses a btrfs read-only path.

## What may be claimed as EXECUTION (observed, author-side, historical)
- `discriminator-smoke.json` (02:16:44Z) `fixture_results[0]`: uid 1000, parent mode 0555, new child → EACCES 13.
- `error-order-smoke.json` (02:17:56Z) `observed[0..1]`: uid 1000, 0555 + new → EACCES; 0555 + existing → EEXIST.
- Kernel identity is *derivable post hoc*: `uptime -s` = 2026-10-19 22:48:20 (`date +%z` −0300 → 01:48:20Z),
  `uname -r` = 7.2.3-arch1-3 (read 2026-10-20T04:43Z); both captures fall in this boot → same running kernel.
- **Not recorded in either smoke file:** parent uid, filesystem, ACL, caller CapEff. `error-order-smoke.json`
  has no `fixture_code` at all. Parent ownership is *derived*, not observed: the uid-1000 process ran
  `chmod(parent,…)` successfully (discriminator `fixture_code`; error-order "restored ownerwrite for cleanup"),
  which requires ownership or CAP_FOWNER. `resumed/mkdir-controls.json` records `parent_uid: 1000`, but for a
  *separate* later run (commit 70fede2), not these two captures.
- Filesystem is `[inf]`: Python's default tempdir is `/tmp`, today `tmpfs rw,nosuid,nodev,…` (`findmnt /tmp`),
  `TMPDIR` unset now; TMPDIR at capture is unrecorded. So the fixture almost certainly ran on **tmpfs**, not btrfs.

## What may be claimed as INFERENCE (root:root 0555, uid 1000) — only with these premises
- **P1 class-uniform bits.** path_resolution(7) § Permissions: owner bits if euid==owner, group bits if gid
  matches, "When neither holds, the third group is used." 0555 has identical `r-x` in all three classes, so
  reclassifying the caller owner→other changes no w/x bit. (`id`: uid 1000 not in gid 0.) **S035 does not state
  class selection**; this sentence needs a registered row (source seat assigns ID) or must be tagged `[inf]`.
- **P2 ACL-robust.** With exact mode 0555 any ACL mask equals the group bits `r-x`, so no named entry can grant
  write; "base ACL entries only" is stipulated, not fixture-observed, and is not load-bearing.
- **P3 SC2 ordering is owner-independent only because x is uniform.** Linux v7.2 `fs/namei.c`: `filename_create`
  defers `mnt_want_write` ("don't fail immediately if it's r/o", 4947–4948), the `LOOKUP_EXCL` lookup returns
  `-EEXIST` (1822–1824) before `vfs_mkdir`→`may_create_dentry`→`inode_permission(MAY_WRITE|MAY_EXEC)` (5255, 3742).
  The parent still needs search (path_resolution(7) line 41: no search → EACCES). Other class has x in 0555 → EEXIST.
- **P4 caps.** Hypothetical stipulates no CapEff DAC_OVERRIDE. The fixture's own EACCES result witnesses that
  its caller had no effective bypass; that is the only cap fact transferable.
- **P5 filesystem hook.** Transfer holds where the parent's `->permission` reduces to `generic_permission`
  (tmpfs: no `.permission` in v7.2 `mm/shmem.c`). **btrfs adds denials** (v7.2 `fs/btrfs/inode.c` 9362–9375):
  read-only subvolume → **EROFS on a rw mount**; `BTRFS_INODE_READONLY` → EACCES. The latter is absent from
  `btrfs_inode_flags_to_fsflags` (v7.2 `fs/btrfs/ioctl.c` 161–172), so r12's `lsattr -d /` "no flags" cannot
  exclude it. Observed now: `btrfs property get -ts / ro` → `ro=false` (btrfs-progs v7.1, 2026-10-20T04:43Z).

## NOT claimable
"actual"/"executed"/"fixture-observed" for any root:root parent; any btrfs or `/` outcome from these fixtures;
"same mode ⇒ same outcome" as a rule; Btrfs ioctl behaviour; any historical cause.

## Counterexamples (strongest first)
1. **Mode non-uniformity (r12's own SC3/SC9).** 0755: owner rwx vs other r-x → owner-swap flips success→EACCES.
   Any text licensing transfer by "same mode" rather than "same bits in both classes" re-admits this error.
2. **SC2 with non-uniform x.** root:root 0500 or 0550: uid 1000 (other, no x) → EACCES at lookup; caller-owned
   0500 → EEXIST. So draft line 151 "EEXIST for SC2 follows from … order, not from ownership" is a false universal;
   ownership is irrelevant *for 0555 only*.
3. **btrfs read-only subvolume on rw mount.** SC1 input `mount: rw` + root:root 0555 on btrfs with subvolume
   ro=true → EROFS, not EACCES (SC2 still EEXIST, lookup precedes permission). The tmpfs fixture cannot see this.
   Snapshot-domain relevance: snapper snapshot subvolumes are typically read-only `[inf]`.
4. **Draft `full_discriminator` (96–104) is not full.** findmnt VFS/FS options and unit properties both miss a
   ro btrfs subvolume; the `limit` names only the host-namespace gap. Labelling it "full" is premature saturation —
   the exact defect class r13 is correcting (closed list of read-only routes).

## Defects in sibling FixtureIdentity.md (read-only)
- L37/§2 table labels parent owner "uid 1000 (vgpnk)" an "Empirical Fact" — derived from chmod success, unrecorded.
- L38 attributes `tempfile.TemporaryDirectory()` to both runs; error-order-smoke records no creation method.
- L38 equates the hypothetical with "`/` or root-owned subtree" — imports btrfs/namespace factors SC1/SC2 do not state.
- L41–42/L50 ground class selection and "identical … under ordinary mkdir ordering" in S035; S035 supports neither.

## Smallest safe correction (CorrectMatrix owns the bytes)
Replace draft `fixture_identity` values (142–154), no new branch, no r12 rewrite:
- `executed_fixture_parent`: "0555 parent created and chmod-ed by the uid-1000 fixture process; parent uid derived
  from chmod success, not recorded; filesystem (default /tmp = tmpfs [inf]), ACL and CapEff unrecorded".
- add `capture_kernel`: "7.2.3-arch1-3, derived: captures 02:16–02:17Z after boot 01:48:20Z".
- `inferred_not_measured`: "root:root 0555: SC1 EACCES because owner and other classes carry identical r-x
  (path_resolution(7) § Permissions); SC2 EEXIST because the exclusive lookup precedes the write check and the other
  class retains search. Valid only for class-uniform w/x bits, no effective DAC_OVERRIDE, and a parent whose
  filesystem adds no denial (btrfs: subvolume ro=false). Not measured for any root-owned parent."
- `full_discriminator` → rename `b2_discriminator`; append to `limit`: "a read-only btrfs subvolume fails writes
  with EROFS on an rw mount and is invisible to findmnt; read `btrfs property get -ts <subvol> ro` (host `/`
  ro=false, 2026-10-20); the route set is not closed." Cite btrfs-property(8) `ro` (line 57) via a new registry row.
- Register path_resolution(7) and btrfs-property(8) (or kernel v7.2 source) via the source seat; else tag `[inf]`.

## Narrow check proposal (L1 runs; not executed here)
Predicate: every scenario whose parent contains `root:root` and whose basis cites a `*smoke*.json` must carry an
explicit inferred status and must not begin with "actual". Old bytes fail on r12 JSON SC1 (182, 190) and SC2
(196, 204); corrected r13 passes iff `fixture_identity.executed_root_owned_fixture == false`, the inference
string names the class-uniformity premise, and r12 carries `superseded_by`. Add a negative-marker scan for
"not from ownership" and for an unqualified "full_discriminator".

## Executed here (read-only, non-privileged)
`findmnt /tmp`; `python3 -c tempfile.gettempdir()`; `id`; `uname -r`; `uptime -s`; `date`; `btrfs --version`;
`btrfs property get -ts / ro`; `grep -c` of /etc/subuid|subgid (presence only); `git log` on evidence paths.
Web reads: man.archlinux.org path_resolution.7, btrfs-property.8; torvalds/linux v7.2 + master namei.c,
btrfs inode.c/ioctl.c, btrfs_tree.h, shmem.c. No fixture executed: a mkdir on host `/` is a host-root write
attempt and outside this seat's write set. An executed non-caller-owned control is feasible later via userns
with subuid mapping (subuid/subgid entries present, newuidmap present, unprivileged_userns_clone=1), but it
would still not be root:root on btrfs. Tools installed/updated: **none**.
