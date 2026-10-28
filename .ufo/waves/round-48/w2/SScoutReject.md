VERDICT: supports

SRC-N3 — the gate's rejection sample, evaluated live this round (opener of record).
Question under test: "what does a shell script need to do to use a TMPDIR whose value
contains whitespace". Bar: fleet CORPUS.md §"SOURCES.md — where a shokunin learns"
(rows are claims, opened in the round that writes them; `community` is never tier A;
tier C is never sole support) and lane `corpus/QUALITY.md` criterion 5 — "A rejection
is kept, not silently dropped" — so every candidate lands as a row with an explicit
verdict and a recorded flip condition.

All fetches this seat, 2026-10-28 (UTC), `curl -fsSL --max-time 60`; receipts in
`.ufo/waves/round-48/w2/SScoutReject/` with sha256s re-verified after copy.
stackprinter.appspot.com was used for Stack Exchange because direct
unix.stackexchange.com / askubuntu.com fetches returned HTTP 403.

=====================================================================
Candidate 1 — mktemp(1), Linux man-pages
URL:      https://man7.org/linux/man-pages/man1/mktemp.1.html
Access:   2026-10-28 via curl (receipt mktemp.1.html, 9832 bytes)
sha256:   74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266
Pinned:   S252's recorded digest is identical
          (SOURCES.md row S252 at ae99f021: "sha256
          74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266"),
          and the pinned snapshot
          `.ufo/waves/round-47/frozen/src/mktemp.html` at ae99f021
          hashes to the same digest. Live bytes = pinned bytes, no drift.
Quote:    "-p DIR, --tmpdir[=DIR] interpret TEMPLATE relative to DIR; if DIR
          is not specified, use $TMPDIR if set, else /tmp."
          Located: fetched HTML lines 94-96 (receipt mktemp.1.html; plain
          text under the `-p DIR, --tmpdir` heading).
Tier/kind: docs, A — already registered.
DECISION: ADMIT AS DUPLICATE — this is the already-registered S252
          (docs|A|mined; used-by corpus/lessons/round-47.md). Confirmed live:
          same URL, same bytes, same located anchor. NO new row. Its scope is
          where mktemp resolves a template dir ($TMPDIR if set, else /tmp);
          it does not itself teach the whitespace mechanics (that is the
          shell's field splitting, candidate 2), but for the question's
          "where TMPDIR is honored" half it is the canonical authority.
=====================================================================
Candidate 2 — POSIX.1-2024 Shell Command Language, word expansion
URL:      https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
          (The Open Group Base Specifications Issue 8 / POSIX.1-2024,
          page header line 25; this is the current edition — supersedes the
          Issue 7 URL pattern …/9699919799/…)
Access:   2026-10-28 via curl (receipt posix_shell.html, 357953 bytes)
sha256:   0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
Pinned:   no prior pin (new open this round).
Quotes (each ≤25 words):
  a) §2.6.5 Field Splitting (fetched HTML lines 1207-1209):
     "the shell shall scan each field containing results of expansions and
     substitutions that did not occur in double-quotes for field splitting"
  b) §2.2.3 Double-Quotes (fetched HTML line 107):
     "Enclosing characters in double-quotes ("") shall preserve the literal
     value of all characters within the double-quotes"
Tier/kind: spec, A — primary standard for exactly this scope.
DECISION: ADMIT (new row; next free id S253 — draft below). This is the
          actual answer to the question: an unquoted `$TMPDIR` containing a
          space is field-split into multiple words; quoting `"$TMPDIR"`
          (or an indirection that keeps the value in one word, e.g. the
          /proc/self/fd alias the census uses) preserves it whole.
=====================================================================
Candidate 3 — community Q&A (chosen):
URL:      https://unix.stackexchange.com/questions/131766/why-does-my-shell-script-choke-on-whitespace-or-other-special-characters
          (fetched via stackprinter export — receipt q_whitespace.txt,
          58893 bytes; canonical stackprinter URL embedded at receipt
          line 15. Direct fetch 403s; also fetched the TMPDIR-specific
          Q174817 as a second screen — receipt q174817.txt.)
Access:   2026-10-28 via curl to stackprinter.appspot.com
sha256:   b8798c059aa3326300f4ecdcf8135428f1586af8c0a3cebb49da87353ec4e6a8
          (of the stackprinter export bytes; the live SE page bytes are
          unreachable from this host — 403 — a fact recorded for the row)
Quote:    Gilles' accepted answer, receipt lines 120-121:
          "Always use double quotes around variable substitutions and
          command substitutions … your script will choke on input or
          parameters … containing whitespace" (≤25 words, truncated mid-list)
          The same answer links POSIX — but to superseded Issue 6
          (onlinepubs/009695399, receipt line 132, footnote [2] at line 255).
Tier/kind: community, C. It DOES carry a primary citation (links the POSIX
          word-expansion chapter), which lifts it above pure hearsay — but
          the citation is a bare "read the standard" pointer to a superseded
          edition, and every operative claim is Gilles' own gloss of §2.6.5.
          The page also never mentions TMPDIR or mktemp: it teaches the
          generic whitespace/splitting rule, not this question's concrete
          `mktemp`/`--tmpdir` surface, which candidate 2 + S252 already
          cover at tier A.
DECISION: REJECT — tier-C community gloss whose primary content duplicates
          what the tier-A spec row (S253 draft) states normatively. Under
          "tier C is never sole support" it can never ground the entry on
          its own, and alongside S253 it adds no proposition the spec does
          not already carry. Its POSIX link is a locator, not a quote it
          grounds a claim on.
Flip condition: admissible (as tier C, supporting-only, never sole support)
          if a knowledge entry needs (a) a corroborating community
          demonstration of the failure mode — e.g. a worked unquoted-TMPDIR
          reproduction or a directly TMPDIR/mktemp-scoped post — or
          (b) the non-normative framing ("always quote" heuristic, list vs
          string context) that the spec deliberately does not phrase. A
          post that itself reproduces `mktemp -d` under a whitespace TMPDIR
          and cites the spec would flip immediately.
=====================================================================
Screened but not selected as candidate 3 (kept as lead note, not a row):
Q174817 "finding the TMPDIR environment variable" (receipt q174817.txt,
sha256 85e34aba5e747eb4f469fbbcf1f6c1978348757b363f33dda78ffec66d59f700) —
screened: recommends `${TMPDIR-/tmp}` and mktemp but never treats a
whitespace TMPDIR; weaker fit than Q131766.

Draft registry rows for the L1 (ids S253/S254 = next free after S252; schema
matches existing rows, teaches-cell REJECTED convention per S183–S185 etc.):

| S253 | POSIX.1-2024 (Issue 8) Shell Command Language, ch.2 word expansion — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | spec | A | POSIX field-splitting and double-quote semantics governing use of an environment variable (e.g. TMPDIR) whose value contains whitespace | Issue 8 page fetched 2026-10-28 (sha256 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd); §2.6.5 Field Splitting and §2.2.3 Double-Quotes, fetched HTML lines 1207-1209 and 107 | unquoted expansion results are field-split; double-quotes preserve the literal value — so a whitespace TMPDIR must stay quoted or indirected | queued | 2026-10-28 | on-release | — |
| S254 | Unix & Linux SE Q131766 "Why does my shell script choke on whitespace or other special characters" — https://unix.stackexchange.com/questions/131766/why-does-my-shell-script-choke-on-whitespace-or-other-special-characters | community | C | Community gloss of the same quoting rule; not TMPDIR/mktemp-scoped | question page via stackprinter export fetched 2026-10-28 (export sha256 b8798c059aa3326300f4ecdcf8135428f1586af8c0a3cebb49da87353ec4e6a8; direct SE fetch 403); Gilles' accepted answer, export lines 120-121 | REJECTED: tier-C gloss duplicating tier-A spec row S253 and never sole support; flip: admissible (supporting-only) if an entry needs a corroborating worked TMPDIR/mktemp whitespace failure or the non-normative "always quote" heuristic the spec does not phrase | rejected | 2026-10-28 | on-release | — |

Notes / things this seat did NOT do: did not fetch the old Issue 6 opengroup
URL the Q&A links (superseded; not needed for the verdict). Did not run the
census selftest (out of scope for SRC-N3). w1 artifacts were not read.
