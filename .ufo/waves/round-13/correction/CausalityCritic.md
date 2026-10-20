# CausalityCritic — round 13 correction (critic seat, author-side, not admission)

Axes judged: **depth** (primary); calibration and adjacency watched for harm.
Target: the r13 correction must narrow the false "only strict / ReadOnlyPaths=" universal
without converting **configured unit text** or **current host `findmnt`** into proof of a
historical cause or of the unit's private mount view. At write time no
`corpus/knowledge/root-dac-correction-r13.*` and no `tools/check-root-dac-correction.py`
existed (glob, 2026-10-20), so this attacks the r12 bytes the correction inherits plus
sibling drafts. Read-only, uid 1000; no journal message bodies were read (metadata only).

## Observed evidence (2026-10-20, read-only)

- E1 `systemctl show … limine-snapper-sync.service`: `ProtectSystem=no`, `ProtectHome=yes`,
  `ReadWritePaths=/tmp`, `PrivateMounts=no`, `ReadOnlyPaths=`/`BindReadOnlyPaths=`/
  `TemporaryFileSystem=`/`RootDirectory=`/`RootImage=`/`InaccessiblePaths=` empty,
  `DropInPaths=` empty, `NeedDaemonReload=no`; `ExecStart=limine-snapper-watcher` with no `+`.
  Unit file `SystemCallFilter=@system-service @mount`, `CapabilityBoundingSet=CAP_SYS_ADMIN`.
- E2 Local systemd.exec(5), systemd 261.2-1, § ReadWritePaths=/ReadOnlyPaths=: "Sets up a new
  file system namespace for executed processes."; § PrivateMounts=: ProtectHome=, ReadWritePaths=,
  … "also enable file system namespacing in a fashion equivalent to this option."; same §:
  "the effect of these settings may be undone by privileged processes". (S028 page; anchors
  for the source seat — I did not edit SOURCES.md.)
- E3 Journal metadata for the 9 `create subvolume failed` matches (`-o json --output-fields`,
  no MESSAGE): all `_SYSTEMD_UNIT=limine-snapper-sync.service`, `_TRANSPORT=stdout`,
  `_EXE=/usr/lib/limine/limine-snapper-sync` (ELF), `_UID=0`, `_CAP_EFFECTIVE=200000`
  (bit 21, CAP_SYS_ADMIN only); `_PID` 1506–1523, never 1386; **9 distinct `_BOOT_ID`s**, one
  match per boot, monotonic 17.9–37.8 s after boot.
- E4 systemd-journald.service(8): stdout-stream metadata reflects "the peer the stream was
  originally created for", not later children; systemd.journal-fields(7) `_PID`: stdout entries of
  forked processes "contain credentials valid for a parent process".
- E5 `journalctl --list-boots`: 11 boots retained, earliest first entry 2026-10-16 11:34:43 -03
  (boot -9, no match). The last failure is in **current boot 0** (uptime since 22:48:20).
- E6 `/var/log/pacman.log`: limine-snapper-sync 1.30.1-1 installed 2026-10-03T17:45:33-0300
  (identical to `/` ctime/mtime in r12 MD:48); systemd/snapper/limine-snapper-sync last upgraded
  2026-10-11, before the first retained match.

## Counterexamples

1. **"No private namespace / unit saw the host `/`" is false by configuration.** E1+E2: with
   `ProtectHome=yes` and `ReadWritePaths=/tmp` the unit ran in its own mount namespace even though
   `PrivateMounts=no` is displayed. Host `findmnt` (r12 MD:49) never observed that namespace, and
   with CAP_SYS_ADMIN plus `@mount` the configured shape is not even an upper bound on the built
   view (E2 "may be undone"). Wording that reads `PrivateMounts=no` or an empty list as namespace
   absence is a fresh false universal.
2. **Configured ≠ failure-time configured.** E1 is current loaded text. E6 bounds packaged unit
   text to unchanged since 2026-10-11 [inf]; `/etc`/`/run` drop-ins, `set-property --runtime`
   and pre-retention boots leave no pacman trace. "B2 was not configured during the incidents"
   is unsupported; "as currently loaded (2026-10-20), no listed unit read-only mechanism covers `/`"
   is supportable.
3. **Current `findmnt rw` is one dated sample of one namespace.** It shares boot 0 only with the
   ninth failure (E3/E5); the other eight boots' mounts were never sampled, and it is never the
   unit view. Note boot 0's failure was 4 s of wall clock after the first journal entry.
4. **The strongest B2 non-fit is the errno, not the host state.** S035: read-only paths yield
   `EROFS` (30); the logged class is 13. The correction must anchor B2's historical non-fit on
   that errno mismatch [inf, ordinary-mkdir semantics; ioctl unverified], with findmnt/properties
   as corroboration only. Conversely, adding BindReadOnlyPaths=/TemporaryFileSystem= must not be
   phrased as a candidate cause of the logged `errno:13`.
5. **Inverse overcorrection.** A namespace can also deny with EACCES-shaped effects
   (ProtectHome=yes "inaccessible"; InaccessiblePaths=). Target `/.snapshots` is outside
   /home,/root,/run/user, but "EACCES can only come from B1+B3" would be a new universal.
6. **Journal `_CAP_EFFECTIVE=200000` is tempting false provenance.** It is the stdout stream's
   original peer (E4), not a proven ioctl issuer, so it cannot close r12's "live CapEff
   unobserved" as *issuer* proof. It is weaker-than-proof failure-time evidence that the logging
   peer lacked CAP_DAC_OVERRIDE — frontier for a later round, not for this C1 correction.
7. **Temporal coincidence trap.** E6: `/` ctime equals the limine-snapper-sync install second.
   That is co-occurrence in one pacman transaction, not who set mode 555 (S040 is the policy
   origin). Similarly "failures began 2026-10-16" is a retention artifact (E5).

## Unacceptable wording (any active MD/JSON, lesson, SCORECARD, report)

| # | Unacceptable | Why | Acceptable replacement |
|---|---|---|---|
| U1 | "the unit has no private mount namespace" / "PrivateMounts=no, so host view applies" | E1+E2 | "configured namespacing options imply a unit mount namespace; its built table is unobserved" |
| U2 | "B2 ruled out / excluded / impossible for `/`" | C1–C3 | "no listed unit read-only mechanism covers `/` in the 2026-10-20 loaded config" |
| U3 | "the unit/process saw `/` read-write (findmnt)" | host namespace, one boot | "host namespace `/` was `rw` at the 2026-10-20 query, boot 0" |
| U4 | "B2 was not configured on this host" (r12 MD:64, JSON B2 interpretation) | host≠unit; current≠historical | "currently configured unit properties list no …" |
| U5 | "only strict, ReadOnlyPaths=, BindReadOnlyPaths=, TemporaryFileSystem= or Root*= can…" | swaps one closed list for another | "among ProtectSystem values only strict covers `/`; other mechanisms include, non-exhaustively, …" |
| U6 | "BindReadOnlyPaths=/TemporaryFileSystem= may explain the logged errno 13" | they yield EROFS-family | "alternative views matter for B2 (EROFS), not for the observed 13" |
| U7 | "EACCES therefore comes from DAC + capability bounding" | C5; r12 MD:67 keeps "consistent with" | keep "consistent, not proven" |
| U8 | "journal `_CAP_EFFECTIVE` proves issuer CapEff" or "CapEff is unobservable" | E4 cuts both ways | "stream-peer metadata observed; issuer unproven" |
| U9 | "configuration unchanged during incidents" (unqualified) | C2 | "packaged unit unchanged since 2026-10-11 per pacman.log [inf]; drop-ins/runtime overrides unbounded" |
| U10 | "installing limine-snapper-sync set `/` to 555" / "failures began 10-16" | C7 | S040 policy origin; "first retained match" |
| U11 | "correction verified/complete" from checker PASS | gate checks committed constants, not semantics | "narrow conformance gate passes; semantic truth needs non-author review" |

## Smallest safe correction

- In r13 MD/JSON: (a) ProtectSystem-only exclusivity; (b) non-exhaustive alternative list
  (BindReadOnlyPaths=, TemporaryFileSystem= `:ro`, RootDirectory=/RootImage= path view);
  (c) one explicit sentence: "ProtectHome=yes and ReadWritePaths= enable a unit mount namespace
  (S028 § PrivateMounts=); host findmnt and configured properties do not observe it or the
  failure-time state"; (d) B2 historical non-fit stated as errno-family mismatch [inf].
- Supersession notices in r12 MD:53,64,86 and JSON B2 `interpretation`/`limit` must point to r13
  without restating U2/U4 as still-true.
- CorrectionCheck: besides failing the old "only strict" constant, add one forbidden-pattern
  finding for U1/U2 ("ruled out", "no private namespace", "excluded" next to B2/namespace) and
  require the namespace-unobserved constant — otherwise a correction can pass while committing C1.

## Sibling drafts (pointers, not edits)

- `BindReadonly.md:45` "neither … were configured" lacks "currently loaded, 2026-10-20" and the
  namespace-unobserved caveat (U4); `:48` "Confidence: High (1.0)" overstates a scout reading.
- `NoOralReview.md:28` agrees with C1; `:29` "issuer is a child of the watcher" needs E4's
  caveat (stdout peer, not issuer) before reuse.
- `GateMutationDesign.md:29` M3 matches U2; extend to U1 ("PrivateMounts=no ⇒ host view").

Impacted axes: depth (false universal replaced by another, or by namespace absence) and
calibration (configured/current read as historical). No harm found to adjacency/coverage.
Tools installed/updated: **none** (no install needed). No checks, repairs or privileged probes run.
