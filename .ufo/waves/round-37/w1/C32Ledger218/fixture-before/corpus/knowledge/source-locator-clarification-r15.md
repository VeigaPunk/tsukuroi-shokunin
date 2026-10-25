source: S046 (docs, tier A, mined; `corpus/SOURCES.md:52`) — https://man.archlinux.org/man/systemd.exec.5; prior S044 at `corpus/SOURCES.md:50` and pair `corpus/knowledge/source-scope-correction-r14.md` / `.json`; debt routed by `corpus/lessons/round-14-verifier-spotcheck.md` § Adjudicated concerns and routing items 1–2.
verified-at: 2026-10-20 — reopened https://man.archlinux.org/man/systemd.exec.5 over HTTPS (native HTML; page footer "systemd 262.1"; response body 293394 bytes) and read SANDBOXING > ProtectSystem=, first definition. The observed 262.1 is the man-page footer revision, not an installed-package measurement; no host probe, package transaction, service change, snapper call or source-supplied command was performed.
recheck: on-release for S046 (re-read § ProtectSystem= whenever the man.archlinux.org systemd.exec(5) revision changes) and 90d for this pair; procedure: reopen the URL, read the SANDBOXING > ProtectSystem= first definition, compare its first sentence and the footer version with this file, and re-count whitespace words in the quote; no host mutation.

This pair resolves only the two status-neutral documentation debts routed after round 14. It adds no capability, changes no r14 byte, makes no general source-truth enforcement or host claim, and does not re-certify any historical proposition.

## R15-LOCATOR

**Source object:** S046, `systemd.exec(5)` (docs, tier A, mined at `corpus/SOURCES.md:52`), reopened 2026-10-20, page footer **systemd 262.1**.

**Defect routed by the verifier:** the round-14 correction cited the reader-dependent "rendered lines 1266-1267" for the S044 quote without naming a renderer. That string is withdrawn as a locator here; it was never evidence that the quote was false. The reopened page shows the S044 quote is exact, while the verifier's reader places the entry at a different offset than the r14 citation did, so a bare rendered line cannot identify it reliably. The r14 citation and that reader disagree on the entry's position, which is why the response is withdrawal rather than a corrected number.

**Located quote (identical to the JSON `R15-LOCATOR` quote and to the r14 located quote), 11 whitespace words, exact after joining the source line break after `values` with one space:**

> Takes a boolean argument or the special values "full" or "strict".

**Active locator:** the stable heading path **SANDBOXING > ProtectSystem=**, its first definition paragraph and this located quote, plus the observed footer version systemd 262.1 and the 2026-10-20 access date. No reader line number is used. The shorter argument-form phrasing `Takes a boolean argument or the special values` opens other option entries with different value sets; the option heading and this full sentence disambiguate the entry.

**Supersession scope:** only the supplemental locator is superseded, in `corpus/knowledge/source-scope-correction-r14.md` § R14-VALUE-DOMAIN (the source-object sentence), `source-scope-correction-r14.json` `corrections[0].location` and `sources[0].anchor`. The r14 quote, replacement proposition, attribution correction and preserved history stand unchanged. The r14 fragment remains readable as historical text under the r15 notice there.

## R15-POSITIVE-DOMAIN

**Source object:** S046, same row and same reopened page revision as above. Located quote, **11 whitespace words**, exact after joining rendered line breaks with one space:

> Takes a boolean argument or the special values "full" or "strict".

**Proposition supported:** the first definition paragraph of `ProtectSystem=` states the documented argument forms — a boolean argument, or the special values `full` and `strict`. That is a positive statement about the option's documented input, not a proof about all values a parser accepts. The retained technical teaching is also positive: `full` adds `/etc/` to the mounts made read-only by true, while `strict` mounts the file system hierarchy read-only except the API file system subtrees `/dev/`, `/proc/` and `/sys/`. The separate other-mechanism examples remain illustrative lane scope, not a source statement about `ProtectSystem=` values.

**Superseded negative sentence:** the r14 clause "documents no further values for this option" is withdrawn as an unsupported absence claim and superseded by this positive definition. It had no command-and-date documentation sweep, and this pair does not claim an exhaustive parser proof, an exhaustive documentation absence or any proposition about undocumented values.

**What is not superseded:** the 11-word quote, the `full`/`strict` coverage statements, the rejection of host-cause and maintainer-acceptance readings, and every S041/S044 row remain exact. Only the unqualified locator and the negative documentation clause change.

## QUALITY check

Performed on the bytes above at authoring, 2026-10-20. This is an author-side check, not independent verification and not execution of the round-15 checker.

| # | Criterion | Evaluation |
|---|---|---|
| 1 | Falsifiable | Each correction is bound to one located sentence and one proposition; host state is not claimed. |
| 2 | Measured anchor | S046 URL, stable heading, footer version, access date and quote word counts are recorded; no line number appears in a JSON location. |
| 3 | Observation / inference / unknown | The quote, footer version and access date are observations; undocumented values are unknown and not asserted. |
| 4 | Append-only | No r14 or r13 byte is edited; the r15 notices there and this pair are additive. |
| 5 | Rejection kept | Prior rejections (host cause, maintainer acceptance, #6629 transfer) remain unchanged. |
| 6 | Pacman advice | Not applicable; neither file contains a package command. |
| 7 | S### citation | S046 is present at `corpus/SOURCES.md:52` as docs, tier A, mined; S044 stays at `:50`. This seat did not write or validate those rows. |
| 8 | Unknown sweep | The definition was read in the reopened page; the frontmatter carries `source:`, `verified-at:` (ISO date) and `recheck:` with a cadence. |
| 9 | Negative claims bounded | No new negative claim is made; the one negative clause is quoted and marked superseded, so no new sweep command is required. |
| 10 | Mention sweep / tables | L1 owns the final cross-file sweep; the tables here retain their intended columns at authoring. |
| 11 | LOG entry | L1 owns `LOG.md`; this pair claims no landing commit. |
| 12 | Absent tool | None needed; the page was fetched over HTTPS and its bytes inspected. |
| 13 | EACCES triage | Not applicable; no permission finding. |
| 14 | Performed, not promised | This table evaluates the preceding bytes; pointers resolve to the named URL, row and files. |
| 15 | Root metadata | Not applicable; no mode, owner or writability claim. |
| 16 | Policy sources | Not applicable; no health grade or repair advice. |
| 17 | Exhaustive scoping | `full`/`strict` statements are option-scoped; other mechanisms stay illustrative lane scope. |
| 18 | Bot attribution | Not applicable; no comment teaching appears in this pair. |
| 19 | Claim/source scope | Each replacement names S046, its located 20- or 11-word quote and the exact proposition; predicate execution belongs to L1. |
| 20 | Comment ID and fields | Not applicable; #8047 fields are untouched. |
| 21 | Portable locators | Applies: stable heading, quote, footer version and access date; the supplemental reader lines are withdrawn, not the quote. |
| 22 | Positive vs absence | Applies: only the positive argument definition is carried; the negative sentence is superseded without an absence proof. |
