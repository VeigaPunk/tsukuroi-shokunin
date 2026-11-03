author: tsukuroi L1 (round 66, attempt 1; wave w1 seats listed in the report)

Round: tsukuroi 66. Lane base `c68bfe97`; declaration and wave spec frozen at `aa75398e`
(SCORECARD "Round 66 — declaration"). Claims: **C1 depth** (sourced, S283) and **C2 adjacency**
(live sibling-anchor table). Work commit and measured outcome: see SCORECARD "Round 66 — measured
outcome" and LOG.md round 66.

## Gate

### S283 — the one row opened this round (CORPUS.md rule 1)

| field | value |
|---|---|
| source | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 |
| access date | 2026-11-03 (L1 open 20:49Z, before the declaration; scout 21:05Z; reviewer R1 21:01Z; receipts `.ufo/waves/round-66/before/s283-open-receipt.txt`, `.ufo/waves/round-66/drafts/scout-s283-scope.md`) |
| quote (18 words, `printf '%s' '…' \| wc -w` → 18) | "The new systemd.credentials_boot_policy= kernel command line option controls when boot credentials encrypted with the "null" key are accepted." |
| location | section "Changes in the system and service manager:", the `systemd.credentials_boot_policy=` bullet, release body lines 248-253 of the pinned capture (sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, 55194 bytes, `published_at` 2026-09-22T13:19:16Z) |
| match note | the body wraps lines and carries CRLF, so the quote is located by whitespace-normalised match (`' '.join(b.split())`), not by a strict one-line grep. Recorded so a strict re-check does not false-fail. |
| tier / scope | A, scoped to "the systemd v262 boot-credential policy on the pinned release body" |
| status change | `queued` → `mined` (new row, opened this round). No other row's `status`, `recheck` or `used-by` changed. |

Man-page cross-check (not a separate row): the scout located the same option in the v262 man
pages at `man/kernel-command-line.xml:70` and `man/systemd.xml:969` (sha256 `eedf5d2a…` and
`458fc5ef…`, receipts in the scout draft). It is cited inside S283's scope, not registered, because
it is the same release tag and admits no claim the release body does not already carry.
Flip: a claim that rests on the man-page wording alone would need its own row.

### Candidates

| candidate | source | decision | reason |
|---|---|---|---|
| S283 — the release body, the policy bullet | tier A, opened live 2026-11-03 | **admit** | the bullet is the primary statement of the option's values and null-key scope; the knowledge entry `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` cites it as `source:` |
| the v262 man pages (`kernel-command-line.xml`, `systemd.xml`) | tier A, same tag | **not registered** (cited in S283's scope) | same release; no separate claim admitted |
| S069 — own-work, the round-19 pointer census | own-work | **cited, unchanged** | the C2 recheck note's `source:` (its outbound pointers are the census's subject) |
| (none rejected this round) | — | — | no source was opened and refused this round |

### Census before → after

- before (round start, `.ufo/waves/round-66/before/census-before-receipt.txt`): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 0 E-code, 44 W04, 282 rows.
- after: see the measured outcome in SCORECARD (run at the work revision).
- expected, stated before the run: S283 repeats S282's release URL under a different scope, so one more `W04 duplicate url across scopes` (44 → 45); no E04 (E04 is same URL within the same scope); no E11 once the note lands in the same commit as the row.

### Spot-check (LEARNING "Discernment is checked from outside")

Pending. The non-author closure judge re-opens a sample of this round's gate decisions. This lane
claims no spot-check result. The seat attacks in `.ufo/waves/round-66/w1/` and their drafts are
evidence for the closure judge, not a discernment verdict. Discernment is recorded as `unchanged`
in the report until a non-author check has run.

### Assimilation

`Assimilation: none` (no `merge/tsukuroi/` theme taken). The L0 `tsukuroi | round-64` question and
its round-64 addendum are still open with no operator answer in `.ufo/l0-questions.md`, so the
§10 mass-id-drift routing still closes adoption. Every §10 check was run anyway and recorded in
`.ufo/waves/round-66/drafts/` only where a seat ran it; nothing from `merge/tsukuroi/` was appended.

### considerthese

One still-unimplemented proposal mined: "Seat-harm incident log" (`considerthese/2026-10-26.md:19`).
Landed as the standing per-round tally in `## Seat-harm tally` below, grounded in rows opened this
round. Not a claim and not a QUALITY criterion.

## Mistakes

Classes come from `mistakes.md` §5 (`corpus/lessons` convention). `captured-by` is the criterion
or rule that should have caught the mistake, or `none`.

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| R66-M1 | landing | the round-65 closure's defect 2: a filed `SCORECARD.md` line (round-63 measured-outcome sentence, `SCORECARD.md:4650`) was edited in place, not appended as an erratum. Sweep RED on the known-bad pair `1bd8e196..7ab7c876`: CR-stripped removed-line count **1** (`.ufo/waves/round-66/drafts/mistake-sweep.md` RED-2) | none — no criterion named the append-only sweep | QUALITY 99 (the round's criterion), with the sweep shown able to fail (RED = 1 on the bad pair) and able to pass (PASS = 0 on the round-66 declaration landing `c68bfe97..aa75398e`, 29 additions) |
| R66-M2 | attribution | the round-66 declaration (frozen text, `aa75398e`) cited the C2 ceiling "no formal overlap table" as AXES.md wording. No AXES.md revision contains it (critic K1, Attack 1: `grep -n overlap AXES.md` → no match at fleet HEAD or any historical blob). It is the lane's own round-11 ceiling (`SCORECARD.md:52`), superseded from round 25 (`SCORECARD.md:836` et seq.); the operative adjacency ceiling is recipient acknowledgement / independent replay | none — the declaration's provenance was not re-read against the source before freeze | append-only erratum in SCORECARD ("Round 66 — erratum: declaration provenance") naming the superseded text; the claim predicate is unchanged; the correction is a provenance fix, not a rewrite |
| R66-M3 | survivor | the frozen C2 counter `grep -cE '^\| AR…'` counts a row whose 40-hex HEAD is a fabricated string (mutant C2-c: fabricated `fee7b068…` → count 10, rc 0). Reviewer R2 Attack 4 reproduced this with three fabricated rows. Mutation-tester M1 class S-A | none — the kill rule names the defect in prose; no counting command observes it | the existence check `git -C <sibling> cat-file -e <HEAD>^{commit}` run on all 10 rows at the work revision (10/10); the one-line resolve-then-count pipeline (`.ufo/waves/round-66/drafts/mutation-battery.md` §6) kills C2-c in scratch (count 9, rc 1) and is **proposed for the next round as a frozen-counter amendment**, not applied to this round's frozen predicate |
| R66-M4 | survivor | the frozen C1 counter `grep -c '^| CB'` counts a table header row that begins with `| CB`: a note with a header plus 4 CB rows reads 5 (mutant C1-e; control C1-e2 without header reads 4). Mutation-tester M1 class S-E | none — prefix match, not row identity | the round's note has no header row (exactly CB1–CB5, `grep -c` → 5, each with NF 5); the next-round amendment is `^\| CB[0-9]+ \|`, shown able to fail by the same battery |
| R66-M5 | stale-premise | the frozen E1 probe item prescribed `od -An -t u1 -j4 -N1` on `/sys/firmware/efi/efivars/SecureBoot-*`. efivarfs is not seekable: the command fails `Illegal seek` (`probes/r66-secureboot.txt`). E1 disclosed a sequential `od -N5` read as the substitute, and the note records the SecureBoot value as measured by that read plus bootctl's `Secure Boot: disabled` | none — the item assumed a seekable file without a dry run | the next probe item prescribes the sequential read; this round's note states the substitution |

R66-M1 is the one mined from the previous round's landing. R66-M2 to R66-M5 were found this round by
the wave's seats and the closure-side reviewers; each has a receipt in `.ufo/waves/round-66/`. The
`ENABLE_UKI` disagreement between `/etc/default/limine` and `/etc/limine-entry-tool.conf` is a finding
about the host, recorded in the note's CB2 row; it is not a lane mistake and is not mined here.

## Seat-harm tally

The standing per-round tally proposed in `considerthese/2026-10-26.md:19`. Rows opened this round:
`corpus/lessons/round-37.md:102`, `round-39.md:74`, `round-40.md:81`, `round-41.md:80` and
`round-41.md:74`. Counts agree with the round-45 ledger (`round-45.md:140-144`) for rounds 37 to 41.

| round | incidents | ids | source |
|---|---|---|---|
| 37 | 1 | R37-MISROOT-NOTE-DRAFT | `round-37.md:102` |
| 38 | 0 | — | `round-45.md:141` |
| 39 | 1 | R39-SEAT-PKILL | `round-39.md:74` |
| 40 | 1 | R40-TMP-MISROOT | `round-40.md:81` |
| 41 | 2 | R41-TMP-MISROOT-REPEAT, R41-CAPTURE-FIFO | `round-41.md:80`, `round-41.md:74` |
| 65 | 0 | — | `grep -c 'R65-.*SEAT\|misroot' corpus/lessons/round-65.md` → 0 |
| 66 | 0 | — | no seat reported seat-to-seat host damage in `.ufo/waves/round-66/w1-results.json`; no process was signalled by this L1 |

## Sweep

- Lane census after the work commit: see SCORECARD "Round 66 — measured outcome" (run at the work revision).
- The mistakes above came from the wave's own attacks and the closure-side reviewers, not from
  an unpaired sweep. The sweep receipts are cited per row.

## Sources used this round

- `corpus/SOURCES.md` S283 (new, `mined`), S282 (unchanged), S069 (unchanged, cited by the C2 note).
- `corpus/knowledge/adjacency-anchors-r19.json` (register, authoritative), `adjacency-anchors-r19.md:204`
  (superseded prose), `PROVINCE.md` ADJ-02/04/06/07 (cited by id only).
