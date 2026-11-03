# CRIT-CLAIMS — round-65 claim audit (K1CritClaims, critic, w1; 2026-11-03)

Freeze `37c74e27` (HEAD at audit start; worktree carries 12 concurrent-seat paths, none of mine
touched). Base `1bd8e196`. Every control below was re-run by this seat, not copied from receipts.
Axes: calibration (do the frozen counters bite?) and falsify (can a judge re-derive and kill?).

## Controls (do-nothing, at base `1bd8e196`)

| counter | command (as frozen) | observed | target | control reaches? |
|---|---|---|---|---|
| C1 note | `git cat-file -e 1bd8e196:corpus/knowledge/systemd262-uki-pcr-r65.md` | rc=128, "does not exist in '1bd8e196'" | rc 0 | no |
| C1 row | `git show 1bd8e196:corpus/SOURCES.md \| grep -cE '^\| S282'` | 0 (rc 1) | ≥ 1, directly after S281 | no |
| C1 total | S-rows at base | 281 | ≥ 282 | no |
| C2 label | `git show 1bd8e196:tools/tsukuroi-census.sh \| grep -c INITRAMFS` | 0 (rc 1) | ≥ 1 | no |
| C2 selftest | base census.sh copied to scratch (worktree file dirty vs base: `git diff --quiet 1bd8e196 --` rc 1, so the scratch-copy route was mandatory) then `bash census-base.sh --selftest` | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)`, rc=0 (32.1 s) | ≥ 174 PASS rc 0 | no |

Control score: **C1 0/3, C2 0/2** — neither do-nothing world reaches either target. The frozen
before-receipt values (rc128 / 0 / 0 / 168) reproduce exactly.

## C1 — predicate-sound, two repairs BEFORE data

Sizing: concrete values (note present; `^| SY` ≥ 5; SOURCES ≥ 282; S282 directly after S281;
NF 13; quote ≤ 25 words; knowledge-header PASS; census validate at round end). Each counter is
one command over committed bytes; the control scores 0; the kill rule ("live-fetch or
host-probe contradiction → note states what measured; honest stop") was frozen at 16:35-03
before any after-measurement exists at HEAD. Floor values cannot be widened post-hoc (they can
only be over-satisfied: draft has exactly SY1-SY5; SOURCES row drafted at 282).

The one universal-flavored clause, "every live value receipted", is bounded and currently
checkable: all receipts cited by the note draft exist in `.ufo/waves/round-65/probes/`
(r65-bootctl.txt, r65-ukify.txt, r65-nvpcr.txt, r65-limine-conf.txt, r65-boot-inventory.txt,
r65-tpm2-units.txt, r65-hooks.txt, r65-versions.txt) — **untracked; they must land with the note**
or the clause is untestable at round end. Not a predicate defect; a landing-order requirement.

Most likely MISS #1 (covered): a round-end gate E-code — sources-census `E12 S282 row outside
Registry section` if the row is appended at EOF instead of inserted at line 292 (S281 ends the
Registry table), or knowledge-header FAIL. The predicate already names "census validate at round
end" + "knowledge-header PASS"; the draft's header carries exactly the gate's three keys
(`source:`, `verified-at:`, `recheck:` with on-release).

Most likely MISS #2 (NOT covered — repair before data): the gate quote's byte form. The 23-word
quote (`wc -w` = 23, verified this seat) occurs **0 times as a strict single line** in the captured
body (`grep -cF` = 0) because the source itself wraps it across body lines 444-446; the section
heading is `##` + **nine spaces** + `Changes in the TPM Subsystem:`. A non-author closure judge
re-deriving with strict verbatim grep false-fails and re-opens. **Smallest safe correction:** the
S282 anchor cell (or the integration receipt) records: quote 23 words, strict single-line count 0
(source's own CRLF wrapping, lines 444-446), whitespace-normalized count 1, heading byte form
9 spaces — citable by title, not by the `## ` prefix.

Sourcing chain (v262 vs 262.1): the anchor is right. Host runs systemd 262.1-1 (`pacman -Q`;
bootctl stub reports `systemd-stub 262.1-1-arch`), and the v262.1 release body is a 76-character
changelog link with 0 NvPCR mentions (fetched independently by this seat: tag v262.1, name
"systemd-stable v262.1", published 2026-10-16T21:57:14Z). The NvPCR/UKI requirement text exists
only in the v262 body; no supersession found. The open receipt discloses the version note
explicitly, and `sha256(s282-v262-release.json)` = `008e1265…babce0b` verified locally = the frozen
before-value. Scope cell is honest: the row pins the requirement; host applicability lives in the
note (SY4: failure mode unreachable today — no TPM2 — exposure latent; falsifier named). A
non-author closure judge re-derives cleanly with two GETs plus the recorded ETag/Last-Modified.

## C2 — predicate-sound, one pin recommended before data

Precedent: DRIFT/STORAGE/SCRUB header contracts all say "verdict-neutral: no PLANE text, rollup
term or exit code changes" (base lines 335-347, 352-372, 386-408) and are enforced by selftest
cases plus the score-* gate family.

By construction (audited at the E2 worktree revision, 279+/34- vs base): all 22 `INITRAMFS`
references are header/help (415, 647), line build (2175-2176), print (4049), and selftest —
`INITRAMFS_LINE` is never consumed; the rollup is built solely from the plane verdicts
(`roll=$(worse "$roll" "$PKG_V")…`). "Never rollup, never exit-input" holds by construction.

By behavior: selftest case `R65-C2` (13 tagged assertions) runs the identical census invocation
with only EXTRA_ENV toggled and asserts (a) exactly one INITRAMFS line per run, (b) every other
line identical, (c) exit code identical — with `bad()` naming "so it is rollup input (R65-C2)".
This seat ran the patched selftest hermetically (TMPDIR pointed into own scratch; no lane-side
writes): **PASS (177 cases, 177 passed, 0 failed), rc=0** (33.1 s) — 168 + 9 ≥ 174 floor, and the
kill rule ("not hermetic under the existing fixture pattern → honest stop") is not triggered.

Does the frozen predicate test neutrality? Transitively yes (selftest PASS rc 0 executes the
R65-C2 case; the live clause re-checks one line + unchanged rc/verdict lines), but it does not
NAME the case: a future revision could drop the case and still satisfy the ≥ 174 letter.
**Smallest safe correction (before data):** the C2 measurement receipt pins
`grep -c 'R65-C2' tools/tsukuroi-census.sh` = 13 at the landed revision — one command over
committed bytes; closes the only widening room found.

Most likely MISS: "base rc + existing verdict lines unchanged" read as byte-equality against the
19:39Z prearm live receipt (rc=1, 6 PLANE + 2 HANDOFF + DRIFT/STORAGE/SCRUB; currently untracked).
The packages plane already drifts run-to-run, so a literal byte-diff false-flags MISS for host
reasons. The predicate partially covers this via the R65-C2 structural A/B; recommended
measurement-receipt wording: live clause = same plane-line count + exactly one added INITRAMFS
line + same rc, with the same-session A/B from the selftest cited as the equality proof.

## Commands run (all by this seat, with rc)

```
git rev-parse HEAD                                                        rc0  37c74e27
git show 37c74e27 --stat; grep declaration blocks in frozen LOG/SCORECARD  rc0
git cat-file -e 1bd8e196:corpus/knowledge/systemd262-uki-pcr-r65.md       rc128 (absent)
git show 1bd8e196:corpus/SOURCES.md | grep -cE '^\| S282'                 rc1  count 0
git show 1bd8e196:tools/tsukuroi-census.sh | grep -c INITRAMFS            rc1  count 0
git diff --quiet 1bd8e196 -- tools/tsukuroi-census.sh                     rc1  (dirty → scratch route)
bash census-base.sh --selftest      (base copy, scratch cwd)              rc0  168 PASS
sha256sum before/s282-v262-release.json                                   rc0  008e1265… (match)
gate quote wc -w / strict grep -cF / fragment grep -n                     rc0 / rc1 (0) / rc0 (line 444)
grep -F '## Changes in the TPM Subsystem'                                 rc1  (9-space heading form)
SOURCES S-rows HEAD and base; S281 pipe count                             rc0  281/281; 12 pipes = NF 13
curl api.github.com …/releases/tags/v262.1 (body_len 76, 0 NvPCR)         rc0
pacman -Q systemd; pacman -Q linux; bootctl status                        rc0  262.1-1; 7.2.11.arch1-1
bash tools/tsukuroi-census.sh --selftest  (worktree, TMPDIR=own scratch)  rc0  177 PASS
grep -c R65-C2 tools/tsukuroi-census.sh; grep -c INITRAMFS (22); sed print site rc0
python3 tools/check-knowledge-header.py <draft>                           rc2  E-CLI (tool binds corpus/knowledge at a revision — draft gate testable only post-landing)
```

No mutating git command, no pacman transaction, no host mutation, no delegation, no installs.
Bounds kept: writes only to this draft, `w1/seats/K1CritClaims.md`, `w1/K1CritClaims.md`, the
controls receipt, and `/fast/scratch/hyaku/tsukuroi-r65/K1CritClaims/` (removed at yield).
