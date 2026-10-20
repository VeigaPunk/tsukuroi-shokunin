# QualityReview — round 13 correction, stale mid-wave QUALITY evaluation

- Seat: `TsukuroiR13.QualityReview` (leaf; read-only; no delegation, no background jobs, no commits).
- Axis judged: depth. Scope: the QUALITY evaluation in `corpus/knowledge/root-dac-decision-r12.md` (`## QUALITY check`, landed bytes) against the landed implementation and history.
- Routed by: `corpus/lessons/round-12-verifier-spotcheck.md`, Routed defect 4 ("replace stale mid-wave process language in the new note's QUALITY evaluation with an accurate landing-time account").
- Checks not run (per assignment). Read-only `git log`/`git show --stat`/`git show <rev>:path` and reads only.
- Tools installed/updated: none.
- Write scope honoured: no lane-authored file edited. The working tree already holds an uncommitted round-13 block appended to the MD (`## Round-13 correction`), 2 lines in the JSON and 3 lines in `corpus/QUALITY.md`. That diff is a sibling seat's and was not reviewed or touched here.

## Landing facts (observed)

| Fact | Observation |
|---|---|
| Matrix content commit | `70fede2` (2026-10-20 00:58:24 -0300) adds `root-dac-decision-r12.md` (+121) and `.json` (+414). Heading `## QUALITY check` at `root-dac-decision-r12.md:90` in that commit. |
| Same commit | also touches `LOG.md` (+47; round-12 entry at `LOG.md:428–473`), `SKILL.md` (+43/−), `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/lessons/round-12.md`, `corpus/knowledge/snapper-eacces-mechanism.md` (+33), `PROVINCE.md`, `SHONEN.md`, `tools/tsukuroi-census.sh`. |
| Later commits | `670126f` measurement pin (`LOG.md:475–516`, SCORECARD, lesson, resumed evidence; matrix files **not** changed). `f3868cd` late source-log erratum (`LOG.md:518–531`, `SOURCES.md`; matrix files **not** changed). |
| Report | fleet commit `6800f05` exists in the fleet repository (`git -C /home/vgpnk/Projects/shokunin cat-file -t` → commit); it is absent from the lane repository. |
| Lane working tree | `corpus/knowledge/root-dac-decision-r12.md` and `.json`, `corpus/QUALITY.md` are `M` (sibling round-13 edits, uncommitted). |
| Literal predicate | `resumed/admission-criterion-red-green.json` records only `549ec0c` (count 0, exit 1) and `b76b5c3` (count 1, exit 0). No run on `root-dac-decision-r12.md` is recorded. |

## Findings (by severity)

**F1 — HIGH (QUALITY #4, stale process claim presented as landing account).** Item 4 reads "This new entry is uncommitted mid-wave and was corrected in place before landing; no old wave evidence or LOG/lesson/SCORECARD/README/SKILL file was edited." At landing the entry was committed in `70fede2`, and that same commit edited LOG, SKILL, lesson, SOURCES, QUALITY, corpus/README, snapper note and census. The sentence is true only of the seat's own authoring window; as a landing account it is false. Errata wording is otherwise correct (snapper erratum present at `snapper-eacces-mechanism.md:70–90` in `70fede2`).

**F2 — HIGH (QUALITY #10, stale instruction plus invalid negative).** Item 10 says `SKILL.md:1695` and `snapper-eacces-mechanism.md:75` list only S027/S028/S034/S035, that "README/LOG/SCORECARD have no mention", and that "the parent must update … at landing".
- At `70fede2`: `SKILL.md:1695` and `snapper…:75` list `S038–S040`. The instruction is already discharged.
- `LOG.md:437,442,448` mention the entry; `corpus/README.md:57` mentions it.
- The lane has no root `README.md` (`ls: cannot access 'README.md'`). "No mention" was recorded from a missing file, which is a non-match-by-error, not a bounded negative (QUALITY #9; MatrixR command 21 conflated the two).
- AGENTS rule 10 requires a sweep of README.md, SKILL.md and **corpus/knowledge/**. The recorded sweep covered one knowledge file.

**F3 — MEDIUM (QUALITY #11, stale).** Item 11 says "No landing commit is claimed here." Landing `70fede2` contains its matching LOG entry in the same commit (criterion 11 met). Later pins are `670126f` and `f3868cd`. The LOG entry's verification/admission text (`LOG.md:470–473`, "pending independent hyaku closure") is now historical; the closure verdict (`admitted: false`, `rejected-harmed` for C2 as delivered) has no lane LOG entry.

**F4 — MEDIUM (QUALITY #13, incomplete).** AGENTS criterion 13 requires the `-Qkk` blind-spot clause ("because -Qkk cannot see /, the census separately reports root-directory mode"). The matrix has zero `Qkk` matches; `snapper-eacces-mechanism.md:13` carries the clause. Item 13 lists fields but not the clause. The census cannot be cited (independence), so the clause must state that `/` is read directly by stat/getfacl and root health belongs to C1.

**F5 — MEDIUM (QUALITY #16, support not in the entry's own recheck).** Item 16 and `MD:50,119` say "no `/etc` or `/run` override recorded". The entry's `recheck:` line and MatrixR's command table contain no override sweep. The support is in `resumed/ClaimCriticR.md` N1 (`grep -rnE '^[a-zA-Z]+[!+-]* +/ ' /usr/lib/tmpfiles.d/ /etc/tmpfiles.d/`) and N2 (`systemd-tmpfiles --cat-config | grep …`, merged line 338, "no /etc/tmpfiles.d override"); `SourcesR.md:210` also cites `--cat-config`. `/run` is covered only by the merged `--cat-config` output, not by N1.

**F6 — MEDIUM (QUALITY #14, performed claim not evidenced).** Item 14 and the section header say the check was "Performed on this entry". The literal-heading predicate on the new entry is not recorded in the red/green evidence (AdmissionCriticR §312 asked for it). The heading itself is literal at `:90`.

**F7 — LOW-MEDIUM (QUALITY #9, conflation).** Item 9 says "target-path absence is bounded by stat (ENOENT text), findmnt (not a mountpoint) and snapper list-configs (0 configs)". Only stat's ENOENT text bears on absence; the other two are explicitly not path proof (`MD:54`, `MatrixCriticR` X5, fixed).

**F8 — LOW-MEDIUM (QUALITY #7, anchor mismatch).** Item 7 requires "exact `corpus/SOURCES.md` S### row … and section anchor". The S027 row anchor is `Capabilities list > CAP_DAC_OVERRIDE` only (`SOURCES.md:33`). The `§ Thread capability sets > Effective/Bounding` anchors used in `MD:1,113–114` are page-verified but not registry-anchored. Immutable fields must not be edited in place (lesson, Sources section).

## Superseding landing-time requirements (exact text for the lane's next correction, appended as a new block; do not edit items 4/9/10/11/13/14/16 in place — QUALITY #4 append-only)

Replace the stale statements with these landing-time accounts (all facts above are observed):

- **Item 4:** "Errata append-only: the old `snapper-eacces-mechanism.md` was not rewritten in place; its owner's falsifier erratum is at lines 70–90 (landed `70fede2`). The entry's matrix files first landed in content commit `70fede2`, with the matching LOG entry at `LOG.md:428–473`. `670126f` and `f3868cd` did not change the matrix files. The earlier phrase 'uncommitted mid-wave' describes the authoring window before `70fede2`."
- **Item 7 (add):** "S027's registry anchor is `CAP_DAC_OVERRIDE` only (`SOURCES.md:33`). The `§ Thread capability sets` anchors are page-verified section-level citations, not registry-anchored; the immutable row is not edited here. [Requirement: either a new superseding registry row, or this explicit limit stays.]"
- **Item 9:** "Target-path absence rests only on `stat` ENOENT text for `/.snapshots` (current state). `findmnt` rc=1 means only 'not a mountpoint'; `snapper list-configs` 0 rows means only 'no configured config'. Neither bears on path absence. BPF-LSM programs are not enumerated (`/sys/kernel/security/lsm` read only)."
- **Item 10:** "Supersession sweep at landing (`70fede2`): `SKILL.md:1695` and `snapper-eacces-mechanism.md:75` list S027/S028/S034/S035/S038–S040. `LOG.md:437,442,448` and `corpus/README.md:57` mention the entry. The lane has no root `README.md` (absent; not a no-match). [Requirement: record a bounded `corpus/knowledge/` sweep for superseded text, with command, scope and date (AGENTS rule 10).]"
- **Item 11:** "Landing commit `70fede2` contains its matching LOG entry (`LOG.md:428–473`); measurement pin `670126f` (`LOG.md:475–516`); late erratum `f3868cd` (`LOG.md:518–531`). Filed report: fleet commit `6800f05` (fleet repository). `LOG.md:470–473` ('pending … closure') is historical; the closure verdict (`rejected-harmed`, C2 as delivered; `corpus/lessons/round-12-verifier-spotcheck.md`) is recorded by an appended L1 LOG entry. [Requirement: that entry must be written by L1.]"
- **Item 13 (add):** "`pacman -Qkk` cannot see `/` (unowned; `snapper-eacces-mechanism.md:13`). Root-directory mode is read directly by `stat`/`getfacl`; root health is reported only by the independent census arm C1, which this entry does not cite."
- **Item 14:** "Heading literal at `root-dac-decision-r12.md:90`. The literal-predicate run on this entry is not recorded in `resumed/admission-criterion-red-green.json`. [Requirement: record `grep -c '^## QUALITY check$' corpus/knowledge/root-dac-decision-r12.md` with its exit, or remove 'Performed on this entry'.]"
- **Item 16 (add):** "Policy sources: `/usr/lib/tmpfiles.d/root.conf:10` (`z / 555 - - -`, systemd 261.2-1); no `/etc/tmpfiles.d` override by `ClaimCriticR.md` N1; merged effective config via `systemd-tmpfiles --cat-config` (`ClaimCriticR.md` N2). [Requirement: these commands are added to `recheck:` or cited by path and date.]"

## Adjacent, out of this seat's scope (routed, not evaluated)

- Round-12 lesson Gate (`corpus/lessons/round-12.md:111–116`) still says "The gate admits the corrected C2 entry". That is superseded by the closure's `rejected-harmed` verdict and needs an appended supersession, not an in-place edit.
- SC1/SC2 root-owned hypothetical versus caller-owned controls (closure defect 4): the sibling's uncommitted block addresses this; not verified here.
- `grep` hits for `chmod 755 /|ProtectSystem=full|read-only mount|root-owned 0755` in `snapper-eacces-mechanism.md`, the matrix MD/JSON, `lessons/round-1.md` and `SKILL.md` are not yet classified as superseded-or-retained text.

## Residual risk and verification gaps

- No checks run (per assignment). The literal predicate on the landed entry is unrecorded; F6 is therefore a gap, not a confirmed failure of the heading.
- `6800f05` existence verified only in the fleet repository; its bytes not inspected.
- The sibling round-13 block and QUALITY.md diff were not reviewed.
- L1 verifies once after integration.
