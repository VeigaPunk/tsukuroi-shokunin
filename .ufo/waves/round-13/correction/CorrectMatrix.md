# CorrectMatrix — round-13 correction executor

## Files changed (write set only)

- `corpus/knowledge/root-dac-correction-r13.json` (new, 20,909 bytes)
- `corpus/knowledge/root-dac-correction-r13.md` (new, 178 lines)
- `.ufo/waves/round-13/correction/CorrectMatrix.md` (this report)

No other file was written. No commit, no test/build/lint/formatter, no install.

## Behavior delivered

Superseding correction `R13-DAC-EXCLUSIVITY` for the round-12 B2 false
universal, with provenance trio (`source:` / `verified-at:` / `recheck:`) and
an explicit `## QUALITY check` #1–16 evaluated for this entry's own bytes.

- Universal narrowed to `ProtectSystem=` values: `full` does not cover `/`;
  `strict` covers the hierarchy except `/dev/`, `/proc/`, `/sys/`, with
  `ReadWritePaths=` and `StateDirectory=`/`LogsDirectory=` exceptions and the
  `PrivateTmp=` writable `/tmp/`,`/var/tmp/` case preserved.
- Alternates retained and non-exhaustive: `BindReadOnlyPaths=` (intrinsically
  read-only bind), `TemporaryFileSystem=` (`ro` only when the mount option is
  given), `RootDirectory=`/`RootImage=` (path-view change, not intrinsically
  read-only).
- B2 RO indicator scoped to the mount backing the **resolved parent**; existing
  final target separate as B4/EEXIST; no errno-ordering universal.
- Explicit replacement pointers: r12 MD:41-42, :53, :64, :86; JSON
  B2.interpretation, B2.limit, decision_procedure[2]; related unmapped sites
  SC5 target-path phrasing and SC7/`host_observation.unit` captured-pair model.
- SC1/SC2: root:root `0555` is hypothetical; executed smoke parent identity is
  **derived** caller-owned (early smoke JSON has no parent-UID field; separate
  resumed mkdir-controls has `parent_uid1000`). Root-owned outcome is a
  conditional inference for exact `0555`/base ACL/search/no bypass/no extra FS
  denial, not measured and not an ownership-equivalence proof.
- Historical cause remains **unknown**; B2/EROFS API-scoped; ordinary mkdir is
  not the Btrfs subvolume ioctl; residual FS-specific denial unknown retained.
- Private mount namespace unobserved/unknown, not operator-only; sentinel
  `SecurityBoundary.md` cited as bounded safety evidence. No `snapper` call,
  service start, `systemd-run`, `nsenter`, or privileged probe.

## Exact retained evidence

- Historical revision `70fede2a7a890cb50a72db2d4230ee541183bf7b`; git shows the
  only r12 commit touching these files. Worktree r12 edits are L1 append
  notices only (`git diff` additions: MD notice block, JSON `superseded_by`).
- Local content check (read-only): JSON parses; all 8 `historical_bytes_check`
  markers present in the r12 blobs at that revision and absent from every
  `gate_contract.corrected_field_scan` value and from all r13 MD lines; the two
  required tables are 4 columns/4 delimiters; MD has the 10 pinned headings.
- `corrected_universal.text` and the MD corrected-claim paragraph each carry
  `BindReadOnlyPaths=`, `TemporaryFileSystem=` (+ro), `RootDirectory=`,
  `RootImage=`, `ProtectSystem=no`, `ReadOnlyPaths=`, "not excluded".
- Sources: S041 (docs tier A, namespace mechanisms; row **reserved**, owned by
  SourceRegistry) carries ProtectSystem/ReadOnlyPaths/Bind/ TempFS/RootDir/
  RootImage; S028 capability-only context; S035 EROFS/EEXIST classes. Man page
  reopened online (footer 262.1) and locally (host systemd 261.2-1); docs are
  not claimed to prove host runtime config.
- Gate constants and deviations sent to `TsukuroiR13.CorrectionCheck`; the
  deviations are: `full_discriminator`→`b2_discriminator`, derived fixture
  identity, parent-scoped RO, S041 citation split, added scope/unknown fields.

## Risks / blockers

- S041 row does not exist yet; the entry cites it as reserved. If SourceRegistry
  lands a different S041 scope/anchor set, the correction's source line needs
  alignment (registry seat owns the row).
- L1 must land the r12 notices + LOG append; this entry alone is not a landing
  commit and does not claim one. QUALITY #11 states that dependency.
- Gate author must exclude `replaced_b2_claims`, `related_locations`,
  `b2_discriminator`, and `historical_bytes_check` from forbidden-marker scans;
  those fields intentionally paraphrase or carry historical phrases.
- The early smoke JSON records no parent UID; parent ownership is derived. Any
  future gate that requires a recorded owner field will fail by design until a
  new fixture records it.

## Tools installed/updated

None. All reads used `read`/`grep`/`eval` and one git/log/diff read; no package
transaction, no privileged probe.
