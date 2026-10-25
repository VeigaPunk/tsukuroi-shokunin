# Scribe5549 — round-37 claim/assimilation evidence draft

seat: scribe; item 5/8; milestone: Draft evidence only
axes: C1 operability; C2 depth; C3 calibration; frontier assimilation (errno discrimination)

## Scope and evidence provenance

This is a read-only draft from the assigned round-37 claim/assimilation/lesson surface. I opened `SCORECARD.md` lines 1857–1919, `corpus/lessons/round-36-verifier-spotcheck.md` lines 1–112, `corpus/SOURCES.md` (including the S035 registry row), `corpus/knowledge/root-dac-decision-r12.md`, `corpus/knowledge/root-dac-correction-r13.md`, and `corpus/knowledge/degraded-triage-r4.md` (errno/J4 passages). These are local repository observations, not fresh reproductions of the historical measurements they quote.

Attempted primary-source opening this round: `https://man.archlinux.org/man/mkdir.2` failed to fetch (`ECONNRESET: The socket connection was closed unexpectedly`). Thus no external-source row is proposed: the local S035 registry description is not a substitute for opening the source this round. No source URL is represented here as freshly opened.

## Observations: claims remain bounded

- **C1, operability:** the round-37 declaration specifies a VERSION-8 probe and livefive predicate, addressing S1 direct full-battery crash, S3 vacuity, S4 ambient PATH blindness, and parameter-name `env` false positive. Its listed after-state is a claim to be evaluated against frozen receipts; this draft contains no execution of V8 and cannot certify it. The round-36 closure explicitly called the predecessor claim NOT VERIFIED because of counter defects. Preserve that distinction: V8 intent is not V8 evidence.
- **C2, depth:** the declared correction is exactly three changes to the journalctl-v262 note: 15 predicate terms, `-F` truncation versus unchanged `-N` under `-n`, and action-override classification. The opened spot-check says these were still unapplied at round-36 close. Declaration describes a before/after criterion and checker, but this draft has not run that checker or established the change landed. Do not generalize the correction to journalctl behavior outside its stated systemd-v262 scope.
- **C3, calibration:** SCORECARD declares a verified-rate ledger matching claims and measured verdicts across rounds 33–36, implementing the dated proposal. This draft has not read or recomputed the ledger's rows, so neither its correctness nor the zero-mismatch result is observed here.

## Frontier assimilation: errno is a discriminator, not a cause

**Observed in local knowledge:** the opened root-DAC decision note scopes its matrix to ordinary `mkdir`/`mkdirat` create-class outcomes. Its named classes include EACCES (parent write/path search denial), EROFS (read-only filesystem), EEXIST (already-present path), and EPERM (filesystem cannot create directories); the note explicitly excludes using ordinary-mkdir controls as proof of the Btrfs subvolume ioctl or historical host cause. The note's decision procedure starts with the observed errno/API family and says the collection order is not a universal errno-priority proof. The r13 correction further labels historical cause unknown and separates conditional inference from measured ordinary-mkdir fixtures.

**Assimilation proposal (inference, not a source-backed new fact):** treat exact errno/API family as an input branch, collect operation-specific evidence, and only then attribute a mechanism. In particular, a logged `errno:13` is compatible with an EACCES class but does not alone prove DAC caused the event; an ordinary `mkdir` control does not establish the Btrfs ioctl path. Keep `EPERM`, `EEXIST`, and `EROFS` distinct rather than collapsing them into “permission denied.” Retain an unknown/unclassified outcome when evidence does not discriminate. This aligns the existing decision note's boundaries; it is not a claim that a new error-classifier was implemented or tested.

The round-36 spot-check's routed list also provides a depth lesson: corrections should be checked against explicit counterexamples and negative cases, not just the prose label. However, no new C2 fixture or errno experiment was executed for this draft.

## Unknown / limits

- External source verification is unavailable in this attempt due to the recorded fetch error; S035 was not refreshed and no source row is proposed.
- No V8 probe, C2 checker, C3 ledger, or host operation was executed. No claim about current host errno or present service state is made.
- No tools installed or updated; no pacman transaction, delegation, background job, tracked lane edit, or Git/jj mutation performed. Only this assigned report is written.

## Handoff

Behavior: evidence-only draft distinguishing observed local claim surfaces, inference, and unknowns. Gates: none run. Touched surface: `.ufo/waves/round-37/w1/Scribe5549.md` only. Out of scope: implementation, source-registry edits, external-source admission, host changes, and judgment of claim outcomes. Findings: errno discrimination is a useful existing lesson, bounded to operation/API and evidence; V8/C2/C3 outcomes remain unverified here. Artifact: `.ufo/waves/round-37/w1/Scribe5549.md`.

Report: .ufo/waves/round-37/w1/Scribe5549.md