source: S041 systemd.exec(5) namespace mechanisms — https://man.archlinux.org/man/systemd.exec.5 § ProtectSystem=, § ReadWritePaths=/ReadOnlyPaths=, § BindPaths=/BindReadOnlyPaths=, § TemporaryFileSystem=, § RootDirectory=, § RootImage= (docs, tier A, scoped namespace row in corpus/SOURCES.md); S028 systemd.exec(5) § CapabilityBoundingSet= (tier A, capability context only); S035 mkdir(2) § ERRORS (tier A, EROFS/EEXIST classes); own-work round-12 smoke fixtures under `.ufo/waves/round-12/`.
verified-at: 2026-10-20 (re-opened systemd.exec(5) online and locally — page footer systemd 262.1, host package systemd 261.2-1; compared the worktree r12 files with committed revision `70fede2a7a890cb50a72db2d4230ee541183bf7b` and confirmed the only differences are L1 append notices; re-read both round-12 smoke JSON records and `corpus/lessons/round-12-verifier-spotcheck.md`; no host mutation, no service start, no `snapper` call, no privileged probe).
recheck: on-release; procedure: `systemctl show -p ProtectSystem -p ReadOnlyPaths -p ReadWritePaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage <unit>; findmnt -n -o TARGET,FSTYPE,VFS-OPTIONS,FS-OPTIONS <mountpoint of the resolved parent directory>`; require every requested property line (missing does not mean empty), and check Markdown table widths.

**R14 supersession notice (append-only, 2026-10-20) — R14-VALUE-DOMAIN and
R14-COMMENT-ATTRIBUTION.** The active corrections in
`corpus/knowledge/source-scope-correction-r14.md` / `.json` supersede two loci
in this entry and its stale draft metadata, not the entry's technical
teaching. **R14-VALUE-DOMAIN** (S044) supersedes the “the value set is not
exhaustive” cell for r12 MD:41-42 in § Replaced round-12 B2 statements:
systemd.exec(5) documents `ProtectSystem=` as a boolean argument or the special
values `full` or `strict`, so the documented option domain is those values and
non-exhaustiveness applies to the set of unit-side read-only mechanisms.
**R14-COMMENT-ATTRIBUTION** (S045) supersedes the S042 attribution wording in
§ QUALITY check item 18 (“model triage”) and in `corpus/lessons/round-13.md`:
the #8047 comment exposes verified API account fields (`omarchybot`, type
User, association COLLABORATOR) but does not self-describe as model-generated
automated triage; its VM-execution sentence is unverified, Codex Medium is
called a second opinion, its maintainer-deferral sentence concerns #6634's
remount failure, and #8047 itself waits on the reporter's answer. S043's
#6629 execution disclaimer remains valid, and both host-cause rejections
stand. The same value-domain defect appears in the JSON twin's
`replaced_b2_claims[0].replacement` (“the option set is not an exhaustive list
of unit-side read-only mechanisms”): the non-exhaustive thing is the set of
mechanism examples, not the option's value domain or its lexical spelling
enumeration. The `sources[0]` “reserved”/`SourceRegistry` draft values and the
ten-heading `gate_contract` object are authoring residuals superseded by the
JSON `r14_supersession` object: S041 is a mined registry row in
`corpus/SOURCES.md`, and the executable checker's five-heading predicate is
its enforcement scope, not source truth. Every other line of this entry is
preserved unedited; § R14 named corrections at the end records the active
reading.

# Root-DAC unit-read-only correction (round 13)

## Supersession and preserved history

**R13-DAC-EXCLUSIVITY** supersedes the B2 unit-side read-only statement, its
`ProtectSystem=` exclusivity and the SC1/SC2 fixture attribution in
`root-dac-decision-r12.md` / `root-dac-decision-r12.json`
(`tsukuroi-dac-decision-matrix-v1`, committed revision
`70fede2a7a890cb50a72db2d4230ee541183bf7b`). The r12 bytes are historical and
are **not rewritten**; the round-13 append notice and the JSON
`superseded_by` pointer are separate append-only blocks owned by L1. Motivating
finding: `corpus/lessons/round-12-verifier-spotcheck.md` C2 rejected the
exclusive condition because it let a reader dismiss a unit-side read-only view
that `ProtectSystem=` and `ReadOnlyPaths=` do not create. This is a narrow
correction: it is not a proof of general semantic correctness and not a causal
proof of any logged `errno:13` event.

## Corrected claim (ProtectSystem= scope)

Among `ProtectSystem=` values, `ProtectSystem=full` does not cover `/`, while
`ProtectSystem=strict` mounts the entire hierarchy read-only except `/dev/`,
`/proc/` and `/sys/`, with `ReadWritePaths=` and `StateDirectory=`/
`LogsDirectory=` style settings excluding specific directories.
`BindReadOnlyPaths=`, `TemporaryFileSystem=` with the ro mount option,
`RootDirectory=` and `RootImage=` can change or restrict the unit's path view
and are not excluded by `ProtectSystem=no` and empty `ReadOnlyPaths=`. The
alternative list is illustrative and non-exhaustive; it does not close the set
of unit-side mechanisms.

`ProtectSystem=full` does not cover `/`; `ProtectSystem=strict` mounts the
hierarchy read-only except `/dev/`, `/proc/` and `/sys/`.

| `ProtectSystem=` value | `/` read-only? | effect | source |
|---|---|---|---|
| `no` | no | no read-only mount from this option | S041 |
| `yes`/`true` | no | mounts `/usr/`, `/boot/` and `/efi/` read-only; `/` not covered | S041 |
| `full` | no | also mounts `/etc/` read-only; `/` not covered | S041 |
| `strict` | yes | entire hierarchy read-only except `/dev/`, `/proc/`, `/sys/` | S041 |

The quoted interface text documents systemd 262.1; the host package is
systemd 261.2-1 (S040). The documentation does not measure host runtime
configuration. The alternatives were unmeasured in the canonical round-12
matrix's captured property set; this is not a claim that no other seat inspected them.

## Preserved exceptions

1. `/dev/`, `/proc/` and `/sys/` are excluded from `ProtectSystem=strict` and
   are to be protected with `PrivateDevices=`, `ProtectKernelTunables=` and
   `ProtectControlGroups=`.
2. `ReadWritePaths=` may exclude specific directories from being made read-only
   by `ProtectSystem=`.
3. `StateDirectory=`, `LogsDirectory=` and related directory settings also
   exclude their directories from the effect of `ProtectSystem=`.
4. With `ProtectSystem=strict` and `PrivateTmp=` enabled, `/tmp/` and
   `/var/tmp/` are writable.
5. `ReadOnlyPaths=` and related namespace settings do not extend to submounts
   created later, so the lock-down is not complete.

## Retained alternate mechanisms

For ordinary `mkdir`/`mkdirat`, the read-only indicator applies to the mount
backing the **resolved parent directory**, not to the nonexistent final path
component; an existing final target is classified separately as B4/`EEXIST`.
The old SC5 phrasing that attached read-only coverage to the target path is
superseded by this parent-scoped reading, and no syscall-wide errno ordering is
claimed.

| mechanism | intrinsically read-only | effect | discriminator |
|---|---|---|---|
| `BindReadOnlyPaths=` | yes, for its bind mount | creates a read-only bind independent of the two settings; a create attempt on a genuinely read-only resolved-parent mount is an `EROFS` indicator, subject to target existence, exceptions and other failures | `systemctl show -p BindReadOnlyPaths <unit>` |
| `TemporaryFileSystem=` | no (ro only with the option) | tmpfs mount options can include `ro`; this directive does not make its tmpfs read-only by default, and writability cannot be concluded from this setting alone | `systemctl show -p TemporaryFileSystem <unit>` |
| `RootDirectory=` | no | pivots/chroots the unit into another directory; changes the path view, not intrinsically read-only | `systemctl show -p RootDirectory <unit>` |
| `RootImage=` | no | mounts an image hierarchy as the unit root; changes the path view, not intrinsically read-only | `systemctl show -p RootImage <unit>` |

`RootDirectory=` and `RootImage=` change the unit's path view; they are not
intrinsically or inherently read-only and do not by themselves establish a
read-only view. These mechanisms are documented alternatives, not claimed
causes of any observed `errno:13`; the B2/`EROFS` mapping is API-scoped
(mkdir(2) `EROFS`, S035) and is not proof of the Btrfs subvolume ioctl or of
any historical event. B2 discriminator (non-exhaustive):
`systemctl show -p ProtectSystem -p ReadOnlyPaths -p ReadWritePaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage <unit>`
and `findmnt -n -o TARGET,FSTYPE,VFS-OPTIONS,FS-OPTIONS <resolved parent mountpoint>`.
`findmnt` reads the host namespace only; the configured properties are text,
not a live measurement.

## Replaced round-12 B2 statements

The table names the historical locus and a paraphrase; no old sentence is
reproduced verbatim, and no historical byte is edited.

| pointer | round-12 claim (paraphrase) | replacement |
|---|---|---|
| r12 MD:41-42 | hierarchy text attributed read-only coverage to the `strict` value alone without naming the ProtectSystem scope in the same clause | among `ProtectSystem=` values, `strict` is the only value that covers the hierarchy (S041); the value set is not exhaustive |
| r12 MD:53 | current-host paragraph treated the two captured properties as excluding B2 and named the `strict` value or a covering `ReadOnlyPaths=` entry as the unit-side causes | the captured `ProtectSystem=no` and empty `ReadOnlyPaths=` exclude those two mechanisms only; the four uncaptured properties leave a unit-side read-only view unexcluded (S041) |
| r12 MD:64 | worked-example step 3 asserted B2 unconfigured on this host from the two captured properties alone | B2 is unconfigured by `ProtectSystem=` and `ReadOnlyPaths=` only; the private namespace and four uncaptured properties remain unobserved |
| r12 MD:86 | R13's second sentence made the `strict` value or a covering `ReadOnlyPaths=` entry the exhaustive unit-side route to a B2-family `EROFS` for `/` | `BindReadOnlyPaths=` and `TemporaryFileSystem=` with ro can also produce it; `RootDirectory=`/`RootImage=` change the path view; `strict` remains subject to its exceptions (S041) |
| r12 JSON B2 interpretation | interpretation closed with an on-host conclusion that B2 was unconfigured from the two captured properties and listed only superblock, `ReadOnlyPaths=` or `strict` as the `EROFS` route | superblock, `strict`, covering `ReadOnlyPaths=`, `BindReadOnlyPaths=` and `TemporaryFileSystem=` with ro all map to `EROFS` (S041); the captured pair alone does not show B2 unconfigured |
| r12 JSON B2 limit | limit ended with an exhaustive unit-side ways-to-make-`/`-read-only claim naming only the `strict` value and covering `ReadOnlyPaths=` | the limit is confined to ProtectSystem values; the four alternate path-view mechanisms are independent of `ProtectSystem=` and `ReadOnlyPaths=`, so the mechanism set is not closed (S041) |
| r12 JSON decision_procedure[2] | collection step 2 named only superblock, `strict` or a covering `ReadOnlyPaths=` entry as B2 indicators | the expanded, non-exhaustive seven-property query includes `ProtectSystem`, `ReadOnlyPaths`, `ReadWritePaths`, `BindReadOnlyPaths`, `TemporaryFileSystem`, `RootDirectory`, `RootImage`; inspect the resolved parent and retain exceptions/unknowns (S041) |

Related unmapped locations: SC5's target-path phrasing is superseded by the
resolved-parent reading above; SC7 and `host_observation.unit` model only the
captured pair, so the four uncaptured properties are unobserved, not absent.

## Fixture identity: SC1/SC2 hypothetical versus executed

SC1 and SC2 specify `0555 root:root` parents as hypothetical inputs. The
executed smoke fixtures derive a **caller-owned** parent rather than record
one: `.ufo/waves/round-12/discriminator-smoke.json` was captured as uid 1000
in a `TemporaryDirectory`, then `chmod(parent,0555)`, and the early smoke JSON
does not carry a parent-UID field (a separate resumed mkdir-controls record has
`parent_uid1000`). `fixture_results[0]` records `EACCES`;
`error-order-smoke.json` `observed[0]` records `EACCES` for a new target and
`observed[1]` records `EEXIST` for an existing target. A root-owned equivalent
is a **conditional source-grounded inference** for the exact case `0555`,
base-only ACL, search for the caller, no bypass capability and no extra
filesystem denial: `EACCES` (SC1) and the documented existing-path class
`EEXIST` (SC2, S035). It is not a measured equivalence, no universal
ownership-equivalence or errno-ordering proof is claimed, and no root-owned
fixture was executed. Even the exact condition leaves a residual
filesystem-specific denial unknown, and ordinary `mkdir` controls are not the
Btrfs subvolume ioctl.

## Historical cause remains unknown

The historical cause is **unknown**; this correction establishes no historical
cause for any logged `errno:13` event. The cited evidence contains no syscall
trace, privileged probe or failure-time target state; current unit settings
do not prove failure-time settings, and the ordinary-mkdir EROFS mapping does
not explain a recorded EACCES. Even the exact `0555` plus base-ACL plus no-bypass condition
leaves a residual filesystem-specific denial unknown; ordinary `mkdir` controls
are not the Btrfs subvolume ioctl. The unit's private mount namespace remains
unknown and unobserved: it may contain read-only bind mounts or tmpfs mounts
that are invisible to a later host `findmnt`, so a host mount view cannot
exclude them.
The namespace is not "operator-only" by definition — if a live, bound issuer
PID were confirmed, its namespace metadata might be readable — but round 12
confirmed none (`ExecMainPID` was stale), so it stays unobserved here. The
safety boundary for this round is the sentinel report
`.ufo/waves/round-13/correction/SecurityBoundary.md` (bounded, read-only
evidence; no service start, `systemd-run`, `nsenter` or privileged probe), and
it supplies no historical caller certainty.

## QUALITY check

Performed on the bytes of this entry at authoring, 2026-10-20. It is an
author-side check, not independent verification, and it does not retroactively
admit round 12.

1. **Falsifiable:** every corrected claim is bounded to `ProtectSystem=` values or to a named mechanism with a re-runnable `systemctl show`/`findmnt` discriminator; the alternatives are explicitly non-exhaustive and hypothetical for this host.
2. **Measured anchor:** §"Corrected claim" carries S041 anchors and the page footer; §"Retained alternate mechanisms" carries the property names; fixture records are exact path/index references whose parent identity is marked derived, not recorded; no claim rests on oral knowledge.
3. **Observation / inference / unknown:** the man-page text is documentation, the smoke records are measured fixtures whose caller-owned parent is derived, the root-owned outcomes are labelled conditional inference, and the private namespace and historical cause are labelled unknown.
4. **Errata append-only:** the r12 bytes are not rewritten; the L1 append notice and JSON `superseded_by` are separate blocks. This entry is new and corrects the old claim by pointer, not by retroactive edit.
5. **Rejections retained:** the r12 rejections stay historical, and this entry adds R13c ("treating `ProtectSystem=` plus `ReadOnlyPaths=` as the complete set of unit-side read-only mechanisms" — rejected by S041), R13d ("`BindReadOnlyPaths=`/`TemporaryFileSystem=` caused the logged `errno:13`" — rejected as causal, uncaptured and API-scoped), and R13e ("an RO indicator checked against the final target path" — rejected; the resolved parent mount is the relevant filesystem and an existing target is B4).
6. **Pacman advice:** none; no `pacman` command or bare `pacman -Sy` appears.
7. **External citations:** namespace/ProtectSystem claims cite S041 (tier A, scoped sections in corpus/SOURCES.md); S035 supports the EROFS/EEXIST classes, not an exhaustive errno ordering; S028 supports capability context only. S041 is present as mined with this entry in used-by at integration.
8. **Unknown sweep and provenance:** the source and historical fixture/canonical-property records were read. A live namespace was not measured; the round-12 canonical record had no confirmed live issuer. This is not a claim that no live issuer exists now. The opening provenance trio and explicit-property recheck are present.
9. **Negative claims bounded:** the four alternative properties are absent from the canonical matrix's recorded capture, not absent from every seat's work. Root-owned execution is not recorded by the cited early smoke controls; caller-owned identity is derived, while the separate resumed mkdir-controls records parent_uid1000. This is not general ownership equivalence.
10. **Supersession / mention sweep:** L1's bounded grep over SKILL.md, corpus/README.md and corpus/knowledge/ found the old universal/unscoped negatives in the preserved r12 MD/JSON; the appended notices and active pointers in SKILL, corpus index, province and snapper note supersede them. No nonexistent root README is used as negative evidence. Table widths are checked at integration.
11. **LOG entry:** LOG.md contains the named round-13 R13-DAC-EXCLUSIVITY correction and its motivating outside finding in the same integration tree. The implementation hash is recorded after commit in SCORECARD and the measurement appendix; no self-referential hash is fabricated here.
12. **Unavailable tool:** no absent tool supports any mechanism claim; `man`, `systemctl` and `findmnt` are the documented interfaces, and the absence of a live unit namespace read is recorded as a limit, not inferred from a missing tool.
13. **EACCES triage fields:** the inherited observation remains target mode/owner/ACL (`555 root:root`, base ACL), unit configured `CapabilityBoundingSet`/`ProtectSystem`/`ReadOnlyPaths`/`ReadWritePaths`/`NoNewPrivileges`, with live `CapEff`/`CapPrm` unobserved. The inherited census observation that `pacman -Qkk` cannot see `/` (root-directory mode is reported separately) is carried as an observation only; this correction adds no census check and makes no package-verification claim.
14. **Performed, not promised:** this section evaluates the content above; the pointers resolve to the man page, the committed r12 revision, the fixture records and the L1 notice headings. It claims no future verification and does not pre-admit any future revision.
15. **Root metadata and denial separation:** no new mode or writability universal is introduced; the denial analysis keeps inode DAC/ACL (B1), unit namespace/path view (B2) and runtime credentials (B3) distinct, and ordinary `mkdir` controls are not used to certify the Btrfs ioctl cause.
16. **Policy sources and overrides:** the r12 tmpfiles policy reading (S039 `z` semantics, S040 `/usr/lib/tmpfiles.d/root.conf` line 10, package-owned by systemd 261.2-1, no `/etc` or `/run` override recorded) is unchanged; no health grade, drift finding or repair advice is added.
17. **Exhaustive claims:** the ProtectSystem comparison is scoped, alternatives are non-exhaustive, and captured properties do not exclude a private path view. The correction checker is bounded conformance only; source reading remains necessary.
18. **Evidence identity and authority:** root-owned scenarios remain conditional inference, caller-owned identity is derived where not recorded, and S042/S043 supersede bot-authority wording without treating model triage as maintainer acceptance.

## Sources

- **S041, tier A — systemd.exec(5) namespace mechanisms** — https://man.archlinux.org/man/systemd.exec.5, opened 2026-10-20, footer262.1. ProtectSystem= supplies the full/strict comparison and exceptions; ReadWritePaths=/ReadOnlyPaths= supplies path restrictions and exclusions; BindPaths=/BindReadOnlyPaths= says “BindReadOnlyPaths= creates read-only bind mounts.” TemporaryFileSystem= permits “mount options such as "size=10%" or "ro"”. RootDirectory=/RootImage= describe root path views. S041 is a mined registry row, not a reserved future source.
- **S028, tier A — systemd.exec(5) capability context** — § CapabilityBoundingSet=: “Capabilities listed will be included in the bounding set, all others are removed.” Cited for B3 capability context only; not used for the corrected B2 namespace claim.
- **S035, tier A — mkdir(2) § ERRORS** — `EROFS`: “path refers to a file on a read-only filesystem.”; `EEXIST`: “path already exists (not necessarily as a directory).”
- **Own work, historical** — `.ufo/waves/round-12/discriminator-smoke.json` (`fixture_results[0]` EACCES) and `.ufo/waves/round-12/error-order-smoke.json` (`observed[0]` EACCES, `observed[1]` EEXIST). Caller UID1000 and outcomes are recorded; early parent ownership is derived rather than recorded. These are not root-owned fixture executions.
- **Finding** — `corpus/lessons/round-12-verifier-spotcheck.md` C2 (exclusive unit read-only condition; SC1/SC2 basis distinction).
- **Bounded safety evidence** — `.ufo/waves/round-13/correction/SecurityBoundary.md` (wave-local sentinel report; no service start, `systemd-run`, `nsenter` or privileged probe; no historical caller certainty).

## R14 named corrections (append-only, 2026-10-20)

**R14-VALUE-DOMAIN** (S044; `corpus/knowledge/source-scope-correction-r14.md` /
`.json`) supersedes one sentence above: “the value set is not exhaustive” in
the cell for the r12 MD:41-42 row of § Replaced round-12 B2 statements
(round-13 MD:97; the current line number is shifted by this append-only
notice). systemd.exec(5) documents `ProtectSystem=` as a boolean argument or
the special values `full` or `strict`. The documented option domain is that
set; the four rows of § Corrected claim are its documented modes, and
non-exhaustiveness belongs to the set of unit-side read-only mechanism
examples, not to an open extension of the option's value domain or a
lexical-spelling enumeration. `BindReadOnlyPaths=`, `TemporaryFileSystem=`
with the `ro` option, `RootDirectory=` and `RootImage=` are separate
mechanisms, not additional `ProtectSystem=` values. The JSON twin
`replaced_b2_claims[0].replacement` (“the option set is not an exhaustive list
of unit-side read-only mechanisms”) is read the same way: mechanism examples
are non-exhaustive; the option domain and its spellings are not open.

**R14-COMMENT-ATTRIBUTION** (S045; same pair) supersedes the S042 attribution
wording in § QUALITY check item 18 and in `corpus/lessons/round-13.md`. For
comment6071740243 the API exposes login `omarchybot`, type `User` and
association `COLLABORATOR`; those are verified account metadata and do not
describe how the comment was produced. Its “I tried this on a stock Omarchy
worker VM” sentence is an unverified execution assertion, it calls Codex
Medium a second opinion, and its maintainer-deferral sentence concerns #6634's
remount failure rather than accepting #8047's diagnosis; #8047 itself ends
“This now waits on your answer.” The comment does not self-describe as
model-generated automated triage, and #6629's separate “Nothing was run on a
machine.” disclaimer (S043) is not transferred. The host-cause and
maintainer-acceptance rejections stand. No command text from either comment is
adopted here.

Nothing else is superseded: the ProtectSystem full/strict comparison, retained
alternative mechanisms, resolved-parent reading, fixture-identity limits,
unknown private namespace and unknown historical cause remain active teaching.
