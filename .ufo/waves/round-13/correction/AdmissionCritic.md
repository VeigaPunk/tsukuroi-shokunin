# AdmissionCritic — round 13, C1 depth correction (R13-DAC-EXCLUSIVITY)

Seat: critic, author-side advice only, not admission authority. Axis: **depth**; guardrails:
calibration/adjacency must not move. Reviewed 2026-10-20 against the uncommitted worktree on
`9574a18`. At review time `corpus/knowledge/root-dac-correction-r13.{md,json}` and
`tools/check-root-dac-correction.py` **did not exist** (`ls` exit 2), so this attacks the
admission design plus the landed L1 notices/QUALITY #17/SKILL/README/PROVINCE/S041 drafts.

## Core finding — a passing guard cannot admit this claim

Round 12 was rejected precisely because a passing structural counter (C2 0→4) coexisted with a
false sentence (`round-12-verifier-spotcheck.md:136-161`). The planned gate checks "committed
constants" authored in the same wave as the prose it checks (CorrectionCheck prompt). Every
falsifier below **passes a token/notice-presence guard**. Supplement it with a
**proposition-to-source reconciliation (PSR)**, run by a non-author seat:

1. Enumerate every *active* B2-bearing proposition: r13 MD+JSON (`interpretation`, `limit`,
   `expected_signal`, `decision_procedure`, scenarios, host observation, `recheck:`), the r12
   notices, SKILL/README/PROVINCE blocks and QUALITY #17.
2. Type each one: necessity ("only"), sufficiency ("X fails writes with EROFS"), absence
   ("not configured"), errno mapping, or history.
3. Locate a verbatim quote for each in systemd.exec(5) **at the host version** (systemd
   261.2-1, `pacman -Q`; `man -P cat systemd.exec`) and in S041's 262.1 page; errno claims in
   mkdir(2) S035 EROFS. Record one agree/disagree row per proposition.
4. Reject on any closed mechanism list, unscoped absence, sufficiency without exceptions, or
   errno reclassification. Necessity and sufficiency are separate checks.

## Source facts reopened by this seat (local 261.2 page; same text in online 262.1)

Rendered with `MANWIDTH=200 man -P cat systemd.exec`; each phrase grep-matched in both the
local page and `https://man.archlinux.org/man/systemd.exec.5.txt` (footer `systemd 262.1`).
- § BindPaths=/BindReadOnlyPaths=: "BindReadOnlyPaths= creates read-only bind mounts".
- § TemporaryFileSystem=: options "such as "size=10%" or "ro""; default mount
  "nodev,strictatime,mode=0755", so **not read-only by default**.
- § ProtectSystem=: strict exceptions are `/dev/ /proc/ /sys/`, `ReadWritePaths=`,
  `StateDirectory=`/`LogsDirectory=`; "This setting is implied if DynamicUser= is set";
  "same limitations as ReadOnlyPaths="; the strict+PrivateTmp `/tmp` `/var/tmp` note is
  present locally too (no version drift for S041's caveat; hypothesis tested, refuted).
- § ReadWritePaths=, ReadOnlyPaths=…: "Sets up a new file system namespace"; host-propagated
  "writable mounts appearing on the host will be writable" under ReadOnlyPaths=; "the effect of
  these settings may be undone by privileged processes".
- § RootDirectory= / § RootImage=: root path views; no statement that they are read-only.
- § ExtensionImages=: read-only overlay over `/usr/ /opt/` (`/etc/` confext), not `/`.

Current configured unit text, unprivileged and read-only (`systemctl show -p … limine-snapper-sync.service`,
2026-10-20): `BindPaths= BindReadOnlyPaths= TemporaryFileSystem= RootDirectory= RootImage=
MountImages= ExtensionImages= ExtensionDirectories= InaccessiblePaths=` empty; `DynamicUser=no`,
`PrivateMounts=no`, `ProtectSystem=no`, `ProtectHome=yes`, `ReadWritePaths=/tmp`. This closes
r12's "not part of this capture" gap **for current configuration only**. Because
`ReadWritePaths=` sets up a namespace, the unit-private namespace is configured, not merely
hypothetical. Its runtime mount state at failure time was not observed.

## Falsifiers (each passes a presence guard; PSR rejects)

| ID | Active-content mutant / condition | Rejecting evidence |
|---|---|---|
| F1 | "Only strict, ReadOnlyPaths=, BindReadOnlyPaths= or TemporaryFileSystem=:ro can make `/` read-only". The list is longer but still exhaustive | No section declares a closed set. RootImage of a read-only image or a privileged remount are not excluded. Reject any "only" not scoped to ProtectSystem values |
| F2 | "BindReadOnlyPaths=/tmpfs ro fail mkdir with EACCES" (B2 drifts into the observed errno 13) | Read-only mount ⇒ mkdir(2) EROFS (S035). Recasting B2 as EACCES fabricates a cause for the logged errno:13 |
| F3 | "TemporaryFileSystem= makes the path read-only" | Default options are `nodev,strictatime,mode=0755`; read-only only with `:ro` |
| F4 | "RootDirectory=/RootImage= make `/` read-only" | Those sections give path views only (S041 row agrees) |
| F5 | Sufficiency sentence carried forward: r12 JSON B2 interpretation says strict or a ReadOnlyPaths= entry "fails create-class writes with EROFS" | Exceptions: ReadWritePaths=/StateDirectory=, host-propagated writable submounts, "undone by privileged processes" (unit is root with cap_sys_admin bounding) |
| F6 | "All alternate properties are empty ⇒ no unit-side read-only view / B2 excluded at failure time" | Today's `systemctl show` is current configured text, not failure-time state, drop-in history or runtime namespace state |
| F7 | Effective strict missed by reading unit text (`systemctl cat`) | DynamicUser= implies strict. Require the `DynamicUser=` property. Whether `show` reports the implied value is **[INFERENCE] unverified** |
| F9 | Baseline red only because r13 is missing (`missing-file` ID or exit 2) | Not red on the false universal. Baseline must exit 1 with **specific** IDs at r12 MD:59 current-host, :70 step 3, :92 R13 (baseline lines 53/64/86 before the header insert), JSON `branches[B2].limit` and `interpretation` "not configured", procedure step 2 |
| F8 | r13 `recheck:` copies r12 line 3's property list (ProtectSystem/ReadOnlyPaths/ReadWritePaths only) | Re-running it re-derives the false absence. r13 recheck must query at least BindReadOnlyPaths, TemporaryFileSystem, RootDirectory, RootImage and DynamicUser |
| F10 | Guard flags ProtectSystem-scoped "only `strict` mounts the entire hierarchy" (r12 MD:47-48) as false | That sentence is true. A keyword `only` regex over- and under-matches, so the guard must scope by clause |
| F11 | r12 bytes edited in place | Currently clean: `git diff --numstat` gives r12.json 2/0 and r12.md 33/0. JSON is deep-equal to HEAD except added `superseded_by` and `correction_notice`. Guard must assert zero deletions vs `9574a18` |
| F12 | `superseded_by` points to a file absent at the measured revision, or S041 lands after the report (r12 late-seat defect) | Guard must resolve the path at the same `--revision`; registry row and used-by must be in that revision |

## Notice-coverage gaps (observed, smallest fixes)

- r12 MD notice (:129-154) and JSON `correction_notice` list current-host, step 3, R13, B2
  interpretation/limit and procedure step 2. They omit the **`recheck:` procedure (MD:3)**,
  which is an active re-runnable command with the incomplete property set. Name it in the r13
  entry's supersession scope (F8).
- JSON SC5 `mount` input (r12 JSON:242) and host_observation unit string (:273) list only
  ProtectSystem/ReadOnlyPaths. They are examples and not false, but r13 scenarios must not
  inherit them as the B2 property set.

## Smallest safe admission correction

1. Keep the structural guard, but word every report and LOG line as "conformance", never
   "truth". SKILL/LOG drafts already do this; keep them that way.
2. Add one PSR table (seat report or r13 `## QUALITY check`). It needs one row per active
   proposition with a host-version (261.2) and 262.1 quote location and a verdict. Seat
   authorship counts as author-side; outside closure remains required.
3. Separate the absence and sufficiency predicates from the necessity predicate (F5/F6) in
   the r13 JSON B2 `limit`.
4. Put mutants F1–F4 and F6 into the checker selftest only if they are **sole-delta** edits of
   the r13 text. Otherwise rely on PSR and say that the guard does not cover them.

## Impacted axes

depth: blocking if any of F1–F6 or F9 holds at landing. calibration: harmed if the guard pass
is reported as semantic correctness. adjacency: unchanged; no namespace mutation or sibling
method was claimed.

Tools installed/updated: **none**. Host actions this seat took: an unprivileged
`systemctl show`, a `man` render to `/tmp`, and a read-only `curl` of the public man page. No
writes beyond this report.
