# Round 66 / w1 — seat S1Scribe (scribe, item C1-DRAFT)

Stamped: 2026-11-03T21:14:00Z
Lane base commit `c68bfe97` (read-only git; no mutating git/jj command was run).
Scope served: claim **C1 (depth, SOURCED — S283)**, draft prose only.

## What this seat produced (three drafts, all under `.ufo/waves/round-66/drafts/`)

| file | what it is | for the L1 to land as |
|---|---|---|
| `cb-note-draft.md` | the knowledge entry, provenance trio first, scope paragraph, and rows CB1–CB5 | `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` |
| `s283-row-draft.md` | the S283 registry row in the registry's exact column order, with per-cell derivation and the L1's post-landing checks | one row in `corpus/SOURCES.md`, directly after S282 (line 292) |
| `s283-gate-draft.md` | the round-lesson `## Gate` block for S283 (URL, access date, ≤25-word located quote, location, word count left PENDING-RECEIPT with the command to run), plus the Candidates/Admitted/Rejected/Spot-check/Census placeholders in the r65 shape | the `## Gate` section of `corpus/lessons/round-66.md` |

No tracked file was edited. No host probe was run by this seat. No census, selftest or
lane gate was run — the checks named in the drafts are written for the L1 to run once at
integration, as the seat spec requires.

## Behaviour and gates the drafts carry

**Knowledge header (the `check-knowledge-header.py` shape).** The note draft opens with
the three column-0 keys in order: `source:` (S283 row id, the release URL and the
`"Changes in the system and service manager:"` anchor), `verified-at:` (2026-11-03 and
the lane base `c68bfe97`), `recheck:` (`on-release`, which also names the four falsifier
states that re-fire it sooner). `verified-at:` carries an ISO date and `recheck:` carries
a symbolic cadence, so the gate's `date_problem` / `cadence_problem` rules are satisfied
by construction. The `recheck:` line contains no backticked command and no `§` pointer,
so the recheck-procedure gate has nothing to flag; the note also contains no line
beginning with `$ `, so the exec-log scan has nothing to flag.

**CB table shape.** Exactly five rows, `grep -c '^| CB'` → 5, each row beginning
`| CB<n> |` (CB1…CB5) and each carrying **4 pipes** (id, row, receipt) — no cell
contains a literal pipe, and no escaped pipe appears anywhere.

**Registry row shape.** The drafted S283 line splits into **NF 13** under `awk -F'|'`
(11 cells + the two empty edge fields), verified on the draft text itself. Fields:
id `S283`; source `systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262`;
kind `docs`; tier `A`; scope naming `systemd.credentials_boot_policy=` boot-credential
behaviour with the four values and the null-key scope; anchor = section + bullet +
`published_at 2026-09-22T13:19:16Z` + raw-JSON sha256 `008e1265…babce0b` + fetch date
2026-11-03; teaches = one grounded benefit; status `mined`; opened `2026-11-03`; recheck
`on-release`; used-by `corpus/knowledge/systemd262-credentials-boot-policy-r66.md`.

**Two census deltas the L1 should expect, so they are not read as defects.** (1) S283
repeats S282's URL under a **different scope**, so one more `W04 duplicate url … across
scopes` warning appears (44 → 45); W04 does not set the validate exit code, and no E04
fires because E04 requires the same URL *within the same scope*. (2) E11 fires for S283
until the note lands, because its `used-by` path does not exist yet — note and row must
land in the same commit, and the after-census receipt is taken after that commit (the
r64/r65 landing-order pattern). The row's insertion anchor is stated explicitly (S282's
unique tail cell plus the following `## Paths` heading) because the r65 lesson records a
mis-anchored insert that landed the row outside the Registry section.

**Gate quote.** The quote chosen is the S283 bullet's first sentence, 18 words by the
L1's own pre-declaration receipt (`.ufo/waves/round-66/before/s283-open-receipt.txt`,
"18 words by `wc -w`"), inside the ≤25-word cap. Its word-count cell is deliberately
**PENDING-RECEIPT** in the gate draft: this seat did not run `wc -w`, and the spec
leaves the value for the L1. The command to run is written verbatim in the draft.

## Receipts the drafts rely on (all read-only reads; each already on disk)

- `.ufo/waves/round-66/before/s283-open-receipt.txt` and
  `.ufo/waves/round-66/before/s283-open-v262-release.json` — the pinned v262 release
  body, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`,
  55194 bytes, `published_at 2026-09-22T13:19:16Z`.
- `.ufo/waves/round-66/probes/r66-bootctl.txt`, `r66-cmdline.txt`, `r66-limine-keys.txt`,
  `r66-root-policy-units.txt`, `r66-secureboot.txt`, `r66-tpm2.txt`, `r66-uki-stub.txt`
  — the host receipts behind CB2–CB4.
- `.ufo/waves/round-66/drafts/scout-s283-scope.md` — the scout's man-page receipt,
  verdict **SCOPE-AGREES** on all four values and both scope halves; it existed on disk
  when CB1 was written, so CB1 cites it rather than carrying PENDING-RECEIPT.

Byte-form facts this seat derived from the pinned capture (used in the gate draft so a
strict re-check does not false-fail): the stored body uses CRLF endings throughout
(876 CRLF, 0 bare LF); the section heading is stored as `##` plus NINE spaces and sits
at decoded body line 155; the bullet occupies decoded body lines 248–253; the one-line
quote has **0** strict one-line occurrences but **1** whitespace-normalised occurrence.

## Findings the L1 should carry into the lesson (not fixed by this seat)

1. **The `protocol: efi` datum is BLOCKED live this round.** `/boot` is a vfat ESP
   mounted `fmask=0077,dmask=0077`, so every read of `/boot/limine.conf` returns rc 2
   "Permission denied (os error 13)". The value (six `protocol: efi` lines) exists only
   as prior-round ground in `.ufo/waves/round-65/probes/r65-limine-conf.txt`. CB2 states
   it as prior-round, not as a live reading — this is the claim's "every host value
   receipted" limit and must not be quietly upgraded.
2. **Two sources disagree on UKI enablement**: `/etc/default/limine` sets
   `ENABLE_UKI=yes`, while `/etc/limine-entry-tool.conf:168` sets `ENABLE_UKI=no`.
   Recorded as a conflict, not interpreted (CB2, CB5e).
3. **The prescribed SecureBoot byte read fails on efivarfs.** `od -An -t u1 -j4 -N1`
   exits rc 1 "Illegal seek" (the file is not seekable) and prints the offset-0
   attribute byte. The value rests on the disclosed sequential `-N5` read (6 0 0 0 0 →
   data byte 0) plus bootctl's independent "Secure Boot: disabled"; CB3 says so.
4. **The option's exposure is real but unmeasured.** The stub advertises "Picks up
   credentials from boot partition", the shipped shared library carries the option
   string, and no unit file or drop-in in `/etc/systemd`, `/usr/lib/systemd` or
   `/etc/kernel` references the option — yet the boot partition is unreadable, so the
   presence of a null-key boot credential is UNKNOWN, not absent. CB4 says exactly that;
   the UKI interior read is out of scope (CB5a), as in the previous round's note.
5. **The verdict is "inert as a control, exposure pre-existing".** The token is absent
   from `/proc/cmdline`, so the documented default `relaxed` governs; `relaxed` accepts
   a null key when SecureBoot is disabled or no TPM2 is available, and this host has
   both conditions true — so v262's default preserves the previous behaviour rather than
   narrowing it. FALSIFIER-CB4-A names four re-fire states (token appearing on the
   command line; a TPM2 device appearing; SecureBoot turning enabled; the boot partition
   becoming readable).

## Touched surfaces (this seat's writes — three files, nothing else)

- `.ufo/waves/round-66/drafts/cb-note-draft.md`
- `.ufo/waves/round-66/drafts/s283-row-draft.md`
- `.ufo/waves/round-66/drafts/s283-gate-draft.md`
- `.ufo/waves/round-66/w1/S1Scribe.md` (this report)

Scratch: `/fast/scratch/hyaku/tsukuroi-r66/S1Scribe/` was created for the one throwaway
body-facts computation and removed before this report was written; no receipt file lives
only in scratch.

## Out of scope (explicitly not done here)

- No tracked file edited: no `corpus/SOURCES.md` row inserted, no note landed, no lesson
  edited, no SCORECARD/LOG change.
- No census, selftest or lane gate executed (the L1 runs them once at integration).
- No `wc -w` run by this seat; the gate word-count cell stays PENDING-RECEIPT.
- No host probe run by this seat; the host receipts are the E1HostProbes seat's.
- No git mutation of any kind (no commit, push, stash, checkout, reset, pull).
- No delegation, no sub-swarm, no background job.

## Landing checklist for the L1 (all commands are the L1's)

1. Land `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` from
   `cb-note-draft.md` and the S283 row from `s283-row-draft.md` in the same commit.
2. Verify the row: `grep -nE '^\| S28[23]' corpus/SOURCES.md` (S283 immediately after
   S282), `awk -F'|'` NF 13 on the S283 line, `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md`
   → 283.
3. Verify the note: `grep -c '^| CB'` → 5, and the knowledge-header gate at the work
   revision.
4. Run the gate word count: `printf '%s' 'The new systemd.credentials_boot_policy= kernel
   command line option controls when boot credentials encrypted with the "null" key are
   accepted.' | wc -w` and paste the value into the lesson's Gate table.
5. Take the after-census receipt AFTER that commit, and expect one extra W04 (45) plus
   zero E-codes.

## One landing-order risk to note

The drafts cite `.ufo/waves/round-66/drafts/scout-s283-scope.md` and the
`.ufo/waves/round-66/probes/r66-*.txt` receipts by path. The cited-receipts gate checks
that every `.ufo/waves/round-66/…` path named in a tracked blob exists as a blob in the
same revision's tree — so the probe receipts and the scout's draft must be landed
alongside the note and the row, or those citations become CITED-RECEIPT-MISSING. The
r65 lane landed its probes for the same reason.
