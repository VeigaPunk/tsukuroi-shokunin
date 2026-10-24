# W2RevSources — SOURCES.md conformance and quote re-open at `c052bb7`

Seat: `W2RevSources` (round 36, wave 2, falsify). Reviewed commit:
`c052bb7d41ced49aa888817069afd804eccfecf1` (change commit; freeze `1e926801195e304950e3eb9d2525ef8bbc245089`).
Declaration: `SCORECARD.md` at `6d76fb20f6ecbc940e5c8fff36c74060c885e161` plus its pre-freeze
correction block landed in `c052bb7`.

**Verdict on the assigned checks: 7 of 8 pass; the "no double quotes" criterion fails (F5).**
All eight assigned conformance checks were run; seven hold outright, the eighth (no double
quotes) fails on S199's two straight-quoted prose spans — a convention gap, not a content
fabrication. Five findings are recorded below, two of medium severity, none falsifying the
S198/S199 rows' sourced content. Timestamps are pasted from `date -u` at the moment of the
command (last: `04:38:37Z`).

## 1. Assigned checks — what was run and what was seen

| # | check | command / evidence | result |
|---|---|---|---|
| 1 | S198/S199 well-formed, 11 cells | `awk -F'\|' '/^\| S19[7-9] /{print $2, NF-2}' corpus/SOURCES.md` → `S197 11`, `S198 11`, `S199 11` (NF=13: leading and trailing pipe) | PASS |
| 2 | quotes ≤ 25 words | programmatic count over straight- and curly-quoted spans of the anchor and teaches cells: S199 anchor **16** words, S199 teaches **3** words; S198 has no quoted prose span | PASS |
| 3 | no double quotes | S199 carries two **straight ASCII `"`** delimited prose spans (16-word anchor, 3-word teaches). S198: none | **FAIL — F5** |
| 4 | S024 untouched | `git show --numstat c052bb7 -- corpus/SOURCES.md` → `3 0` (three insertions, zero deletions, so no old row byte changed). S024 line sha256 parent `0214eea29db7165edea9b048a5d92cb190d51156f2e8d058c2b32a828003ec06` = head `0214eea2…ec06` | PASS |
| 5 | census validate exit 0 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → 32 lines (31 `W04` + one `ok`), **exit 0**. Parent-state control (lane copy with `c052bb7^:corpus/SOURCES.md`, same `tools/`, `SKILL.md`, `corpus/`) → also exit 0, same 31 `W04` lines; the only differing line is the `ok` line's file path. The change adds **zero** validate findings | PASS |
| 6 | rows 197 → 199 | parent `corpus/SOURCES.md` registry rows **197**, head **199**; `sources-census.sh census --root … tsukuroi` → `tsukuroi rows 199`, `FLEET rows 199`, `missing 0`, exit 0 | PASS |
| 7 | no duplicate ids | `grep -oE '^\| S[0-9]{3} ' corpus/SOURCES.md \| tr -d '\| ' \| sort \| uniq -d` → empty; no `E03` in validate | PASS |
| 8 | quote re-open (S198 man page) | see §2 | PASS |

Both new rows also pass the `E11` used-by existence check (the note exists at
`corpus/knowledge/journalctl-v262-field-filter-r36.md`), and neither appears in any
`W04`/`E04` line: `grep -E 'S19[89]'` over the head validate output → no match.

## 2. Quote re-open — the man page and its digest (independent fetch)

Fresh fetches into `/tmp/srcq36` (curl `-sSL --fail`), 2026-10-24 04:33–04:38Z:

| artifact | URL | sha256 | matches row |
|---|---|---|---|
| Arch rendered page | `https://man.archlinux.org/man/journalctl.1` | `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` | **yes**, S198 anchor |
| upstream XML, tag `v262` | `…/systemd/v262/man/journalctl.xml` | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` | **yes**, S198 anchor |
| upstream XML, tag `v262.1` | `…/systemd/v262.1/man/journalctl.xml` | `d54bbede…1edbdd` (identical) | supports the "byte-identical" claim — see F4 |
| upstream XML, branch `main` | `…/systemd/main/man/journalctl.xml` | `d54bbede…1edbdd` (identical, fetch-time) | same |
| `NEWS`, tag `v262` | `…/systemd/v262/NEWS` | `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` | **yes**, S199 anchor |
| `src/journal/journalctl.c`, tag `v262` | `…/systemd/v262/src/journal/journalctl.c` | `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` | **yes**, note's truncated `285b3d0c…d5d0ab` |

Footer/version: `<title>journalctl(1) — Arch manual pages</title>`; `journalctl.1.html:1095`
is `<td class="foot-os">systemd 262.1</td>`; the page links package `core/systemd` and carries
`262.1-1`. **Footer 262.1 confirmed.**

§COMMANDS anchor: fresh fetch line 653 is `<b>-N</b>, <b>--fields</b>`, line 654
`Print all field names currently used in all entries of the journal.`, line 658
`<b>-F</b>, <b>--field=</b>`, line 659 `Print all possible data values the specified field can
take in all entries of the journal.`, line 662 closes the `-F` block. The row's
"rendered HTML lines 653-662" reproduces **exactly** on bytes of the same sha256. The
`-N`-takes-no-argument / `-F=`-takes-one reading used in the note matches this text.

**The rejection sentence is absent from the page.** `grep -c 'cannot be combined with options
that limit the journal'` → **0** on the Arch HTML and **0** on the v262 XML;
`grep -c 'limit the journal'` → **0** on the HTML. The S198 scope cell ("the page does not
document the limiting-option restriction") and teaches cell ("NOT on this page … grep count 0,
both the Arch page and the v262 XML") are therefore true.

**The note never cites the man page for the rejection sentence.** Every S198 mention in
`corpus/knowledge/journalctl-v262-field-filter-r36.md` was read in place: line 3 (the `source:`
header lists S198 for the `-N`/`-F` semantics and gives the page's footer+sha256), line 106
(falsifier 5 states the string is *not* in the Arch 262.1 page nor the v262 XML), line 111
(QUALITY criterion 2 counts S198 as a tier-A docs source), line 124 (Sources: "It does **not**
carry the restriction"). §The rejection attributes the exact line to
`log_error_errno(SYNTHETIC_ERRNO(EINVAL), …)` at `src/journal/journalctl.c:958-960`; the fetch
confirms lines 958-960 hold the `IN_SET(arg_action, …) && field_list_has_scope_options()` guard
and the string. The note's "83 characters + trailing newline = 84 stderr bytes" is exact: the
string measures 83 chars, 84 with `\n`.

S199 re-open: `NEWS:129` starts `* journalctl now rejects -F/--field together with filters such
as`, line 130 `unit, boot, time, cursor or grep filters. Previously field listing`, and the
bullet ends at line 133 `field lists should be adjusted to query entries explicitly.` The
row's 16-word quote is a contiguous substring across 129-130; its 3-word teaches quote
(`query entries explicitly`) is at line 133. Location label "lines 129-133" is the bullet
range, which contains the quoted sentence.

## 3. Findings

### F1 (medium) — the round lesson's `## Gate` is empty at the change commit; contract rule 1 is unsatisfied for both new rows

`corpus/lessons/round-36.md:28-36` holds the `## Gate` heading, a preamble, and a table header
with **zero rows**. SOURCES-CONTRACT-v1 rule 1
(`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, "Rules" §1):
"The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
≤25-word quote with its location grounding `teaches`." Two rows were added at `c052bb7`
(S198, S199); neither has a Gate row. The file self-declares the gap ("Wave 2 fills the rows
below from re-opened bytes; no quote is recorded at wave 1"), so the owner is the wave-2
gate-filling seat / L1, not this seat. Paste-ready rows from my re-opened bytes:

| Source | URL | Opened | Located quote | Location | Decision |
|---|---|---|---|---|---|
| S198 | https://man.archlinux.org/man/journalctl.1 | 2026-10-23 | `Print all field names currently used in all entries of the journal.` / `Print all possible data values the specified field can take in all entries of the journal.` | §COMMANDS `-N, --fields` and `-F, --field=`; rendered HTML lines 653-662; footer `systemd 262.1`; sha256 `aaae4efa…bb83c2` (re-fetched 2026-10-24) | admit — semantics only; the restriction sentence is absent (grep 0 on page and on v262 XML) |
| S199 | https://raw.githubusercontent.com/systemd/systemd/v262/NEWS | 2026-10-23 | `journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.` | CHANGES WITH 262 > Feature Removals and Incompatible Changes, `NEWS:129-133`; sha256 `a494f038…857657` (re-fetched 2026-10-24) | admit — prose statement plus the "query entries explicitly" remedy; the exact rejection line is `src/journal/journalctl.c:958-960` |

(These Gate quotes use straight `"` deliberately: the Gate parsers in
`tools/check-storage-health.py:216`, `tools/check-memory-pressure.py:204` and
`tools/check-kernel-taint.py:201` read straight-quoted spans as the located quote, so the Gate
convention differs from the registry convention in F5.)

### F2 (medium) — the lesson states the superseded source set, contradicting the landed registry

`corpus/lessons/round-36.md:23-26` says C2 "rests on S024 (re-opened pinned to the systemd v262
tag this round) and a new row S198", and the Gate preamble (`:32-35`) repeats "The two sources
the declaration names for this round's sourced claim are S024 (re-opened pinned to the systemd
v262 tag) and the new row S198". At `c052bb7` this is false in both directions: S024 is byte-identical
to the parent and still `queued` with `used-by = —` (check 4 above), while S199 — the pinned
v262 NEWS row the note's `source:` line and §Sources actually rest on — is `mined` and named
by the note's `used-by`. The sentence is a faithful copy of the *original* declaration
(`SCORECARD.md` at `6d76fb2:1658-1659`), which the pre-freeze correction item 7 replaced
("S198 journalctl(1) … semantics only" + "S199 systemd NEWS pinned at tag v262 … supersedes
S024 for this note"). The lesson was not updated with it. Effect: a reader of the committed
lesson would credit the claim to a queued, unpinned, mutable URL. Fix belongs to the lesson
owner (append a correction line or rewrite the two sentences before the L1 lands the lesson).

### F3 (low-medium) — S199's supersession is not in the contract's shape and inverts the round-35 precedent for the same situation

Contract rule 2: "A correction is a new row whose `teaches` opens `supersedes S0NN —`." S199's
teaches places it mid-sentence and narrows it — `… supersedes S024 (the mutable main URL, left
queued and unchanged) for the round-36 note` — and the same wording is duplicated in the
`scope` cell, where the contract asks for "the claim or topic the tier applies to", not a
supersession. The registry's own precedent for exactly this shape is the other way round:
S196 (pacman NEWS pinned at the installed commit, S006 = mutable main URL left queued) says
"this pinned copy is a separate row, **not** a correction of S006". No validator sees the
difference (E04 is keyed on URL+scope and the URLs differ; the E04 `supersedes` exemption is
therefore not load-bearing here), so the inconsistency is documentation-only — but two
treatments of one situation in one table is a defect of the registry's own taste record.
Recommendation: adopt the S196 wording for S199, or move the marker to the cell's opening as
rule 2 requires.

### F4 (low) — S198's anchor says "byte-identical" with no stated comparand, and as written it is false against the neighbouring digest

S198 anchor: `… fetched 2026-10-23, sha256 \`aaae4efa…\`; upstream man/journalctl.xml at tag
v262 byte-identical, sha256 \`d54bbede…\``. Read next to the page's own digest, "byte-identical"
can only attach to the Arch page, and an HTML rendering cannot be byte-identical to an XML
source — the two named digests differ by construction. The claim the wave-1 seat actually
established (`…/w1/SrcJournalctlMan/SrcJournalctlMan.md:18,73`) is that the **v262.1 and main
XML blobs are byte-identical to the v262 XML at fetch time**; I reproduced that
(all three `d54bbede…`). So the digest is right and the fact is right, but the cell does not
name the comparand and is unfalsifiable as written. Fix: "byte-identical to the `v262.1` and
`main` blobs at fetch time".

### F5 (low) — S199 uses straight ASCII double quotes as prose delimiters, against this seat's stated criterion

Two spans: anchor `(quote "journalctl now rejects -F/--field together with filters such as
unit, boot, time, cursor or grep filters.")` and teaches `the "query entries explicitly"
remedy`. Basis for treating this as nonconforming: the lane's own quote parsers give
backtick spans precedence *because* "a located quote may contain double quotes inside
backticks" (`tools/check-memory-pressure.py:184-204`, `tools/check-storage-health.py:217`,
`tools/check-kernel-taint.py:205`) — i.e. a quote containing `"` is expected to be
backticked. Honest limits: (a) SOURCES-CONTRACT-v1 has no double-quote rule — it only forbids
`|` inside a cell; (b) 37 other registry rows already carry straight `"` outside backtick
spans (38 including S199; e.g. S033, S088 quote prose the same way), so this is a registry-wide convention gap
and not an S199-only regression; (c) no counter in `tools/` was found to extract quoted spans
from `corpus/SOURCES.md` cells (the three `quoted_spans()` parsers read the Gate table), so
nothing mechanically mis-parses. Severity is therefore low: fix by backticking the two spans
(matching the counters' backtick-wins rule) or by using curly quotes as S016 does.

## 4. Residual risk and verification gaps

- **Line numbers are digest-scoped.** The S198 anchor's HTML line numbers (653-662) and footer
  line (1095) reproduce only because the fresh fetch has the same sha256 `aaae4efa…`; a
  re-render at the same package version would move them. That is a property of every
  rendered-page anchor in this registry, not of this row.
- **Not re-opened here (out of this seat's scope):** the note's 54-cell `matrix-mini.json`, the
  `cap()` hazard replication, and `src/journal/journalctl-filter.c` (digest `480f7a03…72f48`,
  lines 26-43). The note's truncated digests were checked only where the fetch was already
  needed (`journalctl.c` `285b3d0c…`, which matched).
- **No lane gate other than `sources-census.sh` was run**; the round's own gates at the change
  commit belong to other seats. Nothing in this review exercises C1.
- **Tool installs:** none. No pacman, no network tooling beyond `curl` already present.
- **Evidence files:** `validate-head.out`, `validate-parent-control.out`,
  `validate-parent-vs-head.diff` in this seat directory.
- **Working-tree observation (not part of `c052bb7`).** At `04:40:14Z` the lane tree is not
  clean: `git status --porcelain` shows ` M SCORECARD.md` and ` M SKILL.md` (uncommitted L1
  edits; the SCORECARD hunk is a "Round 36 measured outcome" block stamped `04:39Z`).
  `corpus/SOURCES.md`, `corpus/lessons/round-36.md` and `corpus/README.md` are **unmodified**
  relative to `c052bb7`, so every check in §1 is against committed bytes. The uncommitted
  `SKILL.md` hunk moves the round-36 gate/probe row above the table's delimiter row:
  committed `SKILL.md:3057` header → `3058` `|---|---|…|` → `3059` child-env row is
  well-formed, while the working tree reads `3056` header → `3057` child-env row → `3058`
  delimiter, and the prose now says "round36 prepends one probe row". If that hunk lands
  as-is the round-36 probe sits between header and delimiter, which is not a Markdown table
  header/body pair. Reported as tree state, not as a defect of the reviewed commit.

