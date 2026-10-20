# MatrixReview — round 13 correction (C1, depth)

Scope: original MD current-host paragraph, R13 rejection and worked-example step 3 in
`corpus/knowledge/root-dac-decision-r12.md`; JSON B2 branch and its procedure/SC records in
`corpus/knowledge/root-dac-decision-r12.json`. Read-only. No files edited. No checks, tests or
builds run (per assignment). Observation state read 2026-10-20; sibling seats were editing these
files during my read, so line numbers may drift. L1 re-verifies after integration.

Tooling: no installs or updates. One web read (Arch `systemd.exec.5` text) and one web search
used only to locate the same man page; quotes below come from the Arch fetch.

## 1. Axes

- depth (judged): exact scope of every "only / not configured" claim about unit-side `/` read-only.
- adjacency (secondary): sibling-seat text that cross-references this correction.

## 2. Findings — false or unbounded statements still present (active bytes)

| ID | Where (current) | Statement | Problem |
|---|---|---|---|
| F1 | MD:53 (current-host) | "only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit (S028)" | False universal. S028 also documents `BindReadOnlyPaths=` (read-only bind mounts) and `TemporaryFileSystem=` with `ro`. Cited to S028 without a `ReadOnlyPaths=` anchor. |
| F2 | MD:86 (R13) | "Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS` for `/` through the unit." | Same exclusivity. The `full` rejection half is correct and should stay. |
| F3 | JSON:87 (B2 `limit`) | "so only strict or a ReadOnlyPaths= entry can make / read-only through the unit." | Same exclusivity, in the record the closure named. The same limit also says the four alternates "can also change the unit's view", which contradicts the sentence. |
| F4 | JSON:77 (B2 `interpretation`) and MD:53, MD:64 | "On this host ... so B2 is not configured for /" / "B2 is not configured on this host" | Unbounded negative. The capture (MD:51, JSON host_observation) reads only `ProtectSystem`, `ReadOnlyPaths`, `ReadWritePaths`, `ProtectHome`, `NoNewPrivileges`, and related identity fields. `BindReadOnlyPaths`, `TemporaryFileSystem`, `RootDirectory`, `RootImage`, `InaccessiblePaths` and `RootImageOptions` are not measured. QUALITY #9 and #17 require the negative to be scoped to the properties actually checked. |
| F5 | MD:123-148 (supersession block) and JSON:2-3 (`superseded_by`, `correction_notice`) | Points to `root-dac-correction-r13.md` / `.json` as "the current procedure". | At my check, no such file existed under `corpus/knowledge/`. The active r12 files therefore name a successor that is not there. This must land with the successor, or the pointer is dangling. |
| F6 | MD:123-148 | "These alternatives were not captured in round 12." | Contradicted by repo evidence. `.ufo/waves/round-12/resumed/MatrixCriticR.md:16` (R2, `systemctl show ... -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage -p InaccessiblePaths`) records all of them empty, `ProtectSystem=no`, `ReadOnlyPaths=` empty. The row carries no date of its own. The correct wording: "not captured in the matrix's host_observation; a round-12 resumed critic probe recorded them empty (unregistered, undated in the row)". |
| F7 | MD:41-42 | "B2 explicitly excludes `ProtectSystem=full` ... while only `strict` mounts the entire hierarchy read-only" | Scope qualifier "among `ProtectSystem=` values" is missing here, though the supersession block has it. Minimal fix only. |

## 3. Source-anchor gap (QUALITY #7)

- MD:1 source line and MD:114 (S028 row) quote only `CapabilityBoundingSet=`, `ProtectSystem=`, `ReadWritePaths=`, `ProtectHome=`. No `ReadOnlyPaths=`, `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`/`RootImage=` or `RootImageOptions=` anchor.
- JSON B2 `evidence` (JSON:45-75) and `source_ids` (JSON:88: `["S028","S035"]`) have the same gap.
- `corpus/SOURCES.md:34` (S028 row) anchors only `CapabilityBoundingSet=`.
- Quotes verified this session, fetched from `https://man.archlinux.org/man/systemd.exec.5.en.txt` (systemd.exec(5), Arch), to be registered as anchors (Sources-owned; the SourceRegistry seat's S041 row is the intended vehicle):
  - `§ ProtectSystem=`: "If set to "strict" the entire file system hierarchy is mounted read-only, except for the API file system subtrees /dev/, /proc/ and /sys/"; "ReadWritePaths= may be used to exclude specific directories from being made read-only."
  - `§ ReadWritePaths=, ReadOnlyPaths=, InaccessiblePaths=, ExecPaths=, NoExecPaths=`: "Paths listed in ReadOnlyPaths= are accessible for reading only, writing will be refused even if the usual file access controls would permit this." "Nest ReadWritePaths= inside of ReadOnlyPaths= ..."
  - `§ BindPaths=, BindReadOnlyPaths=`: "BindReadOnlyPaths= creates read-only bind mounts."
  - `§ TemporaryFileSystem=`: "Each mount point may optionally be suffixed with a colon (":") and mount options such as "size=10%" or "ro"."
  - `§ ProtectHome=`: "read-only" is "mostly equivalent to ReadOnlyPaths=" (covers /home, /root, /run/user only, not /).
  - `§ RootDirectory=`: "Sets the root directory for executed processes, with the pivot_root(2) or chroot(2) system call."
  - `§ RootImageOptions=`: "Takes a comma-separated list of mount options that will be used on disk images specified by RootImage=."
  - `§ ReadWritePaths=, ReadOnlyPaths=, ...`: "Paths listed in InaccessiblePaths= will be made inaccessible for processes inside the namespace along with everything below them."

## 4. Minimal correction obligations (what the active text must say)

O1 (F1, MD:53). Replace the exclusive sentence with a scoped one. Candidate:
"[obs] Measured 2026-10-20: `ProtectSystem=no`, `ReadOnlyPaths=` empty. These exclude only those two mechanisms. Among `ProtectSystem=` values, `full` does not cover `/`; `strict` covers the hierarchy except the API subtrees (S028). Other unit-side read-only mechanisms that can cover a target are `ReadOnlyPaths=`, `BindReadOnlyPaths=` and `TemporaryFileSystem=` with `ro` (S028). `RootDirectory=`/`RootImage=` change the path view and are not intrinsically read-only. BindReadOnlyPaths, TemporaryFileSystem, RootDirectory, RootImage and RootImageOptions were not captured on this host."

O2 (F2, MD:86). Keep the `full` rejection. Replace the second sentence with: "Among ProtectSystem= values only strict covers `/`; ReadOnlyPaths=, BindReadOnlyPaths= and TemporaryFileSystem=:ro can also make a covered target read-only (S028), subject to nested ReadWritePaths= where S028 documents it."

O3 (F3, JSON:87). Remove "so only strict or a ReadOnlyPaths= entry can make / read-only through the unit." Substitute the same scoped content as O1, with the JSON key naming the unobserved properties.

O4 (F4, JSON:77; MD:53, MD:64). Change "B2 is not configured for /" to "no ProtectSystem= or ReadOnlyPaths= mechanism is configured for / in the measured set; the other B2 properties are unmeasured." This is the bounded form QUALITY #9 requires.

O5 (F5, F6). Either land `root-dac-correction-r13.{md,json}` with the same commit as these edits, or remove the successor pointer until it exists. Reword "not captured in round 12" as in F6.

O6 (F7). Insert "among `ProtectSystem=` values" at MD:41-42.

O7 (Sec. 3). Register the S028 anchors (or a new superseding S028-scope row) and cite them in MD source line, MD Sources and JSON B2 `evidence`/`source_ids`. Sources-owned; do not edit immutable S028 fields in place.

## 5. Likely omissions (beyond the named false sentences)

- OM1, ReadWritePaths re-allow. Every "covering" claim (JSON:77, :84, :87, :174; MD:41-44, :53, :64, :86) omits that a nested `ReadWritePaths=` can re-enable writes under `ProtectSystem=strict` or `ReadOnlyPaths=` (S028). Add one clause in the corrected B2 interpretation.
- OM2, procedure step 2 (JSON:174; MD:64 worked step 3) lists only `ProtectSystem`, `ReadOnlyPaths`, `ReadWritePaths`. It omits `BindReadOnlyPaths`, `TemporaryFileSystem=...:ro`, `RootDirectory`, `RootImage`, `RootImageOptions` (mount options, may carry `ro`). The supersession block says step 2 is superseded, but JSON:174 is byte-identical to round 12.
- OM3, capture omission. The systemctl capture (MD:51; JSON host_observation.unit) omits `BindReadOnlyPaths`, `TemporaryFileSystem`, `RootDirectory`, `RootImage`, `RootImageOptions`, `InaccessiblePaths`. A read-only `systemctl show` of those properties is the direct fix for F4; the probe is not privileged. It was not run here (assignment: no checks).
- OM4, InaccessiblePaths. Not in B1, B2 or B3, although it is a unit-side namespace mechanism that can make a path inaccessible (S028, text above). Its errno is not established by any registered source, so it must be listed as an unknown residual, not omitted. [inf] Error class is unverified.
- OM5, ProtectHome. `ProtectHome=read-only` makes /home, /root, /run/user read-only (S028). It does not cover `/`, but it is another unit-side read-only mechanism the exhaustive-looking B2 list omits. Optional LOW.
- OM6, SC5 inputs (JSON scenario SC5, around :240). The input list "unit ProtectSystem=strict / ReadOnlyPaths= covering the target" is sufficient-condition text, not exclusive, but it is incomplete against the corrected B2 set. Add the other mechanisms or label the list "examples".
- OM7, B2 correction must not change the sentence used as the rejection. The `full` rejection (MD:86 first clause; MD:41) is source-correct and should stay byte-stable.

## 6. Narrow-check design obligations (for CorrectionCheck seat; not run)

- Scope the "active" set explicitly. The r12 files keep the false sentences as history by design (correction_notice, supersession block). A check that scans them without a rule either fails the corrected corpus or needs an ad hoc exemption. Recommended rule: r12 files are excluded only where the `superseded_by` key (JSON) or the "Round-13 correction" heading (MD) is present, and the exemption is a named constant, not a text match.
- Forms to match: MD uses backticks ("only `strict`"), JSON uses plain text ("only strict"). Cover both. Candidate tokens: `only\s+`?strict`?\s+or`, `only\s+strict\s+or\s+a\s+ReadOnlyPaths=`, `can make\s+/\s+read-only through the unit`, `Only\s+`?strict`?\s+or`, `B2 is not configured (for|on this host)`.
- Avoid self-trigger: the supersession block text must not contain any matched token (current wording does not, but verify with the final text).
- Old bytes: `git show f3868cdef07027f7ec8ecd095457d95108f75676:corpus/knowledge/root-dac-decision-r12.{md,json}` must fail (F1, F2, F3, F4 present). Active r13 successor must pass and must still contain the positive checks: `full` does not cover `/`, `strict` scoped "among ProtectSystem", named alternates BindReadOnlyPaths, TemporaryFileSystem `ro`, RootDirectory/RootImage path-view-only, and the unknown private namespace.
- A structural/literal-only check is not sufficient for depth. Pair it with the source-anchor presence check (Sec. 3).

## 7. Verification gaps

- No checks were run. All statements are from file reads and one web fetch; not from executing the matrix or its scenarios.
- Current line numbers are from a live, concurrently edited file. JSON line numbers shifted by +2 after `superseded_by`/`correction_notice` were added.
- Whether `ReadOnlyPaths=/` (a `/` entry) is valid usage is not checked against a unit; treated as [inf].
- `InaccessiblePaths=` errno (EACCES vs ENOENT) is not established; treated as an unknown.
- Round-12 R2 values (MatrixCriticR.md:16) are an unregistered probe with no date in the row; cite as labelled prior evidence only.
