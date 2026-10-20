# MistakeScribe — round-13 correction draft

Seat: `TsukuroiR13.MistakeScribe` (leaf). Scope: draft at most five mistake rows
(class / evidence / captured-by / fix) for the routed false universal, bot
attribution, fixture identity and late source-seat write.

Method and limits:
- Only file reads were performed (AGENTS.md, QUALITY.md, lessons round-12 and
  round-12-verifier-spotcheck, RULES.md, round-13 correction spec/dispatch
  headers, `corpus/knowledge/root-dac-decision-r12.md` lines 1–121, and grep
  hits in `corpus/SOURCES.md`). No commands were executed for verification; no
  tests, builds, lint or formatters ran; no execution claim is made here.
- `[obs]` = read directly in this session at the pointer given.
- `[cited]` = taken from `corpus/lessons/round-12-verifier-spotcheck.md`; the
  underlying file was not reopened by this seat (noted per row).
- Tools installed or updated by this seat: none.
- No commits, no edits outside this report, no LOG append (L1 owns LOG).

## Mistake rows

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | Routed false universal: an exclusive condition ("only `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit") that the entry's own discriminators contradict. | [obs] `corpus/knowledge/root-dac-decision-r12.md:53` ("only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit") and `:86` (R13, "Only `strict` or a `ReadOnlyPaths=` entry ... could produce a B2-family `EROFS`"). Same file `:53` lists `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, `RootImage=` as B2 path-view queries. [cited] JSON B2 `limit` carries the same sentence (not reopened here); spotcheck lines 143–161. | Outside closure source reopen of systemd.exec (spotcheck §C2, "disagree as delivered"). Author self-check `root-dac-decision-r12.md:94–109` marks criteria #1–#16 evaluated; none tests quantifier scope of exclusive wording, so the self-check passed it. | Do not edit the filed matrix in place. Land a superseding entry with a supersession notice that: (a) restates the source as "among `ProtectSystem` values only `strict` covers the hierarchy; `full` does not cover `/`" (S028); (b) keeps the four alternate path-view mechanisms as named B2 discriminators; (c) corrects MD `:53`, `:86` and JSON B2 `limit` together. Proposed for L1 review, not executed: a QUALITY criterion requiring universal/exclusive wording to be checked against every listed alternative. |
| M2 | Authority misattribution: automated triage comments presented as maintainer-side. | [obs] `corpus/SOURCES.md:42` (S036, "its maintainer-side rebuttal comment") and `:43` (S037, "a maintainer-side comment"), both naming `@omarchybot`. [obs] `corpus/lessons/round-12.md:88` labels S036 "maintainer-bot comment 2026-10-09", which keeps the ambiguity inside the lesson. [cited] spotcheck lines 183–186: the bot explicitly defers to a maintainer; the comments are automated triage. | Outside source critic reopening the GitHub API comment endpoints (spotcheck §Outside discernment; S036/S037 rejection agreed, attribution flagged). Author gate did not catch it because the rejection status does not depend on author identity. | Do not edit S036/S037 immutable fields in place. Append a superseding registry note stating author = `@omarchybot` (automated triage), not maintainer acceptance; keep `rejected` status and recheck unchanged. Reword the "maintainer" label in `round-12.md:88` by appended erratum, not rewrite. Apply the same attribution rule to any future bot-authored source row. |
| M3 | Fixture identity: a control described with the wrong owner (uid-1000 success claimed against a root-owned `0755` parent), with a residual of the same class in SC1/SC2. | [obs] `root-dac-decision-r12.md:57` ("The `0755` fixture parent was created by uid 1000, not root-owned"); `:58` (SC3 correction: root-owned `0755` gives uid 1000 only `r-x`, so `EACCES`, not success); `:84` (R11, ownership decides the class). [obs] `corpus/lessons/round-12.md:44` row "stale fixture identity / credential proxy". [cited] spotcheck lines 248–251: SC1/SC2 specify root-owned hypothetical inputs but cite caller-owned smoke controls as their basis (not reopened here). | Partly captured by resumed `C2ReviewR` F3–F4 (`round-12.md:44`) and the in-place SC3 correction. The SC1/SC2 residual was caught only by the outside spotcheck. | Each scenario states fixture owner and mode as separate fields, and labels the outcome as executed (cite the smoke artifact) or inferred (`[inf]`). Relabel SC1/SC2 as hypothetical inputs with an inferred same-mode outcome, and drop the caller-owned control as their basis. Record in a new entry with a supersession notice; no reliance on mode alone. |
| M4 | Late source-seat write after the report, a conformance and ordering defect (status-neutral). | [cited] spotcheck lines 45–50: `f3868cd` committed after the report and added the S027 source-reopen paragraph and LOG erratum; report bytes preserved. [obs] `corpus/SOURCES.md:68` and `:70` are seat-authored provenance paragraphs (clock correction of S038–S040 dates; "Matrix citation confirmed (2026-10-20, Sources seat)"), showing seat writes to the registry during the resumed attempt. Distinct from `round-12.md:45` (fleet-root relative write, a different failure). | Operator identified the write; outside closure confirmed it. The lane's report gate did not detect a write landing after the report. | Stop and join source seats before final measurement, commit and report. The report commit must be the last commit touching seat-writable paths. Preserve `f3868cd` and its LOG erratum as history; never rewrite the filed report. For L1 decision: an ordering assertion at integration (last commit touching seat-writable paths precedes the report commit). |
| M5 | Routed blocking defect deferred to a later round while the entry stayed admitted-false. | [cited] spotcheck line 14 (`admitted: false`) and lines 237–242 ("tsukuroi / next steered round — blocking correctness" for the false universal). [obs] `root-dac-decision-r12.md:98` (criterion #5 "Rejections retained") coexists with M1's live exclusive sentence. [obs] `corpus/lessons/round-12.md:111–112` and `:167–169`: author-side admit of the corrected C2 entry "on the lane's own evidence", recorded before fresh non-author verification. | Outside closure disposition (`admitted: false`). The author gate admitted C2 before the universal was checked against alternatives. | When the fix is a superseding entry and the defect is blocking, route it to the same round and keep author admission provisional with an explicit blocker field. Do not record an admit on a row whose quantifiers were unchecked. Round-13 C1 is the routed correction; this row records the disposition gap, not a new claim. |

## Not covered

- Did not reopen: JSON B2 `limit`, SC1/SC2 text, S036/S037 API endpoints, the
  systemd.exec page, or the spotcheck's sample of `CloseTsukuroiR12`. Rows M1,
  M2, M3 and M4 partly rest on `[cited]` lines; their `[obs]` pointers were
  read here.
- `spec.json` and `dispatch.json` were read only as headers (ranges elided);
  nothing in those ranges was needed for these rows.
- No claim that the corrections described above are complete or landed.
