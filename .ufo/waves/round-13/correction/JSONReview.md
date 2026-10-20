# JSONReview — B2 "not configured" duplicates in root-dac-decision-r12.json

Seat: TsukuroiR13.JSONReview (leaf, read-only). Write set: this file only.
Tools installed or updated: none. No tests, builds or privileged probes run.

## Snapshot (volatile)

Target: `corpus/knowledge/root-dac-decision-r12.json`, sha256
`2f2cba66b4d6aac2b998de1fae3826965f9f5649d5ca8db5530292b056c66571`.
The file is **uncommitted-modified** (`git status`: ` M`), as is
`root-dac-decision-r12.md` (+27 lines). Another round-13 seat added two top-level
keys (`superseded_by`, `correction_notice`; +2 lines). Lines below are from that
snapshot. L1 must re-hash before overlaying.

## Findings by severity

### HIGH-1 — The sole explicit "B2 not configured" assertion is still active text

- `$.branches[1].interpretation`, JSON line 77, final sentence:
  "On this host the unit has ProtectSystem=no and empty ReadOnlyPaths=, so B2 is not configured for /."
- This is the only occurrence of "not configured" in the JSON (grep over the file).
- Overlay status: the top-level `correction_notice` (line 3) names
  "B2 interpretation/limit", so it is a supersession pointer, not an in-place edit.
  The sentence itself is unchanged.
- The notice cannot be applied to a field-level claim by reader: it lists no
  line or pointer for the sentence.

### HIGH-2 — Dangling supersession pointer

- `$.superseded_by` (line 2) = `corpus/knowledge/root-dac-correction-r13.json`.
- That file does not exist (`ls corpus/knowledge | grep -i r13|correction`: empty).
- The MD round-13 section (`root-dac-decision-r12.md` ~lines 123–148) names
  `root-dac-correction-r13.md` / `.json` as "the current procedure" — also absent.
- `corpus/QUALITY.md` item 17 cites `corpus/lessons/round-13.md`; that file now
  exists (checked).
- Until the correction JSON lands, the active procedure in this file is the
  uncorrected one.

### HIGH-3 — "B2 not configured" rests on 2 of the 7 properties the discriminator queries

- Discriminator command, JSON line 81 (`branches[1].discriminator.commands[1]`):
  `systemctl show -p ProtectSystem -p ReadOnlyPaths -p ReadWritePaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage <unit>`
- `$.host_observation.unit` (lines 348–366) records only `protect_system`,
  `read_only_paths`, `read_write_paths` (plus `protect_system_full_covers_root`).
  No key for BindReadOnlyPaths, TemporaryFileSystem, RootDirectory or RootImage.
- `$.branches[1].limit` (line 87) says those four "were not part of the captured
  property set in this round". Within the JSON that is accurate.
- Contrary evidence exists in round-12 wave artifacts (read-only, not in JSON):
  - `.ufo/waves/round-12/MatrixCritic.md` line 23 (P7): `RootDirectory=`/`RootImage=` (empty).
  - `.ufo/waves/round-12/resumed/MatrixCriticR.md` line 16 (R2) queried
    `BindReadOnlyPaths`, `TemporaryFileSystem`, `RootDirectory`, `RootImage`;
    line 79 summarises them as "all empty or `yes` here".
  - Raw R2 cells are truncated in the transcription I could read; the summary
    values are **not independently verified** by this seat.
- Overlay implication: either add those four keys to `host_observation.unit` with
  the raw values (after L1 re-check of the raw probe output), or keep the
  "not captured in the JSON" wording and do not state that B2 is not configured.

### MEDIUM-1 — Exhaustive-sounding mechanism lists (same fault as round-12 X3)

- `$.branches[1].limit` line 87: "…so only strict or a ReadOnlyPaths= entry can make
  / read-only through the unit." Same sentence acknowledges BindReadOnlyPaths=,
  TemporaryFileSystem=, RootDirectory=, RootImage= as view changers — self-contradictory.
  This is the false universal that the round-12 closure rejected (C2).
- `$.branches[1].interpretation` line 77: "A read-only superblock, a covering
  ReadOnlyPaths= entry, or ProtectSystem=strict fails create-class writes with
  EROFS" — omits BindReadOnlyPaths= and TemporaryFileSystem=…:ro as EROFS sources.
- `$.decision_procedure[2]` line 174: trigger list "a read-only superblock,
  ProtectSystem=strict, or a ReadOnlyPaths= entry covering the target -> B2-family
  indicator" — same omission; reads only `ProtectSystem/ReadOnlyPaths/ReadWritePaths`.
  The MD notice (~line 130) names this step as superseded.
- `$.scenarios[4]` (SC5), `inputs.mount` line 242: "unit ProtectSystem=strict /
  ReadOnlyPaths= covering the target" — same truncated list.

### MEDIUM-2 — Same unit state recorded in three JSON places (update together)

- Structured: `$.host_observation.unit` lines 354 (`protect_system: "no"`),
  356 (`read_only_paths: ""`), 357 (`read_write_paths: "/tmp"`),
  365 (`protect_system_full_covers_root: false`).
- Free-text restatement: `$.scenarios[6].inputs.unit` line 273
  ("ProtectSystem=no, ReadOnlyPaths empty, ReadWritePaths=/tmp, ProtectHome=yes").
- Derived: `$.branches[1].interpretation` line 77 (the "not configured" conclusion).
- Any overlay that changes the B2 scope must change all three or the JSON
  disagrees with itself. The structured block is the only one that would carry
  the missing four properties.

### LOW-1 — Consistent with the corrected scope; no overlay needed

- `$.host_causal_attribution.why_not_proven` (~line 404): "the unit-private mount
  namespace was not observed". This is correct scoping and does not assert B2
  absence.
- `$.host_causal_attribution.leading_hypothesis` (~line 403): names only B1+B3.
  It does not claim B2 is excluded. No change required.
- `$.branches[1].discriminator.expected_signal` (line 84): lists
  BindReadOnlyPaths, TemporaryFileSystem, RootDirectory/RootImage. It is the
  correct statement and the one the other passages should match.

## Effective-overlay location list (current JSON snapshot)

| # | JSON pointer | Line | Current text (abridged) | Action for overlay |
|---|---|---|---|---|
| 1 | `$.superseded_by` | 2 | `root-dac-correction-r13.json` | Target must exist before overlay is "effective" |
| 2 | `$.correction_notice` | 3 | Round-13 supersession, names B2 interp/limit + step 2 | Keep; add exact pointers (see 3–6) |
| 3 | `$.branches[1].interpretation` | 77 | "...so B2 is not configured for /." | Replace the conclusion; remove the unconditional form |
| 4 | `$.branches[1].limit` | 87 | "...only strict or a ReadOnlyPaths= entry can make / read-only" | Remove exclusivity; keep the alternate-mechanism list |
| 5 | `$.decision_procedure[2]` | 174 | closed trigger list | Add BindReadOnlyPaths=, TemporaryFileSystem=:ro; RootDirectory/RootImage as path-view only |
| 6 | `$.scenarios[4].inputs.mount` | 242 (SC5) | truncated list | Align with step 2 |
| 7 | `$.host_observation.unit` | 348–366 | 3 of 7 queried props | Add BindReadOnlyPaths, TemporaryFileSystem, RootDirectory, RootImage (raw values to be verified) or label "not captured" |
| 8 | `$.scenarios[6].inputs.unit` | 273 | free-text restatement | Keep in sync with #7 |
| 9 | `$.branches[1].discriminator.expected_signal` | 84 | already complete | No change |
| 10 | `$.host_causal_attribution.why_not_proven` | ~404 | unit-private namespace unobserved | No change |

Markdown counterparts of the same B2 "not configured" claim (outside the JSON write
scope, listed for L1; line numbers as read at this snapshot, MD also modified):
- `corpus/knowledge/root-dac-decision-r12.md` line 53 (current-host [obs]):
  "B2 is not configured for `/`."
- line 64 (worked example step 3): "B2 is not configured on this host, but a host
  `findmnt` cannot exclude ...".
- line 86 (R13): "Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce ...".
- lines ~123–148 (round-13 notice): already states that `ProtectSystem=no` and
  empty `ReadOnlyPaths=` "exclude only those configured mechanisms, **not B2**".
  This is the wording the JSON overlay should match.
- `corpus/QUALITY.md` item 17 (line 23) already gives the scoping rule.

## Residual risk / verification gaps

- The round-12 R2 raw values for BindReadOnlyPaths/TemporaryFileSystem were not
  visible in full to this seat. Do not cite them as fact until L1 reads the raw probe.
- SC1/SC2 fixture attribution is covered by the notice but is not B2; not reviewed here.
- The JSON and MD are being edited concurrently by other round-13 seats; this
  review is a point-in-time read (sha above).
- No runtime check of `systemctl show` or `findmnt` was performed; the analysis
  uses only the static text and the round-12 transcriptions named above.
