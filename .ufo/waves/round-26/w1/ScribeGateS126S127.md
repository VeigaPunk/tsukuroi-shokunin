# ScribeGateS126S127 — round 26, wave 1

Verdict: done — both sources were re-opened by ordinary means on 2026-10-22, every anchor digest reproduced, and the Gate-record rows for S126 and S127 are landed in `corpus/lessons/round-26.md` at commit `ef72f10`; the landed rows parse cleanly and the C1 storage checker passes 6 of 6 with exit 0 at `7dfea92`.

## 1. What this seat was asked to do

Routed defect 2 (round-25 verifier spot-check line 104): registry rows S126 and S127 in
`corpus/SOURCES.md` had no lesson `## Gate` record — no URL or repo path with revision, no
access date, and no ≤25-word quote with its location. This seat re-opened each source today
by ordinary means, verified the anchor digests, and supplied the Gate records for the round-26
lesson.

[obs] The defect was real at the base revision. `grep -c "S126" corpus/lessons/round-25.md`
returned 1 (the errata prose at line 72, not a Gate row) and `grep -c "S127"` returned 0, so
neither row had a Gate table row in the round-25 lesson (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md:11-30`).

## 2. S126 — systemd v262 `man/oomd.conf.xml`, re-opened and re-verified

[obs] The fetch is reproducible. `curl -sSfL -o oomd.conf.xml
https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml` returned HTTP 200 and
12 557 bytes; `sha256sum` gave
`36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`, byte-identical on two
further fetches (`curl … | sha256sum` and a second download compared with `cmp` → IDENTICAL).

[obs] That digest equals the S126 anchor exactly. The anchor cell of row S126 in
`corpus/SOURCES.md:132` reads "tag v262, lines 150-202; raw bytes sha256
36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617" — reproduced.

[obs] The S120 transposition claim is confirmed and localised. S120's anchor
(`corpus/SOURCES.md:126`) reads `…45632d4a61ae…` and S126's reads `…45632a4d61ae…`; a
character-level comparison of the two 64-hex strings shows they differ at exactly two
positions, index 16 (`d` vs `a`) and index 18 (`a` vs `d`), with the `4` unchanged. The
fetched bytes hash to S126's value, so S120's anchor is the transposition and S126's is
correct.

[obs] The S126 anchor's cited line range holds in the fetched bytes. The `[OOM] Section
Options` block begins at line 157 (`<refsect1>`), with `SwapUsedLimit=` at line 164,
`DefaultMemoryPressureLimit=` at line 178 and `DefaultMemoryPressureDurationSec=` at line 196;
the three default sentences sit at lines 172, 190 and 202, all inside the anchor's
"lines 150-202". These are the same three lines the round-25 lesson recorded for S120
(`corpus/lessons/round-25.md:23-25`), so S120's quotes stand unchanged under S126.

Quotes verified as byte-exact substrings of the fetched bytes (word count by whitespace split):

| Quote | Words | Line, tag v262 |
|---|---|---|
| `Defaults to 90%.` | 3 | 172 |
| `Defaults to 60%.` | 3 | 190 |
| `Defaults to 30 seconds when unset or 0.` | 8 | 202 |

## 3. S127 — sibling lane mori, `system-pressure-r24.md` at commit 4f05dd5a, re-opened

[obs] Read read-only through the sibling repo, no worktree write: `git -C
/home/vgpnk/Projects/shokunin/mori-shokunin show 4f05dd5a:corpus/knowledge/system-pressure-r24.md`.

[obs] Both anchor digests reproduce. `git rev-parse
4f05dd5a:corpus/knowledge/system-pressure-r24.md` returned
`d4ccce4262d8224e362da65eb5ba4b851ad0fea2`, matching the git blob id named in the S127 source
cell (`corpus/SOURCES.md:133`), and `git show 4f05dd5a:corpus/knowledge/system-pressure-r24.md
| sha256sum` returned
`5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5`, matching the anchor cell's
"blob sha256 5d3a322a…c019ce5". The commit resolves to
`4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e` ("round-24: measured outcome, capability rows, LOG,
QUALITY 72-75 wording, lesson corrections", 2026-10-22).

[obs] The anchor's cited sections and line ranges hold in that blob: `## Scope` at line 43, the
F2 block at lines 69-78, the F9 block at lines 133-144 with the root-identity sentence on line
144, and the F10 block at lines 146-150.

Quotes verified against the blob (word count by whitespace split; "exact" = byte-exact inside
the stated lines, "normalised" = exact after whitespace normalisation only):

| Quote | Words | Location | Match |
|---|---|---|---|
| `records what those files are, exactly which shapes the kernel emits, which error codes the kernel returns,` | 17 | line 46, section Scope | exact |
| `Each documented file (cpu, memory, io) holds two lines of the form` | 12 | line 69, section F2 | exact |
| `A system-scope read says nothing about any **non-root** cgroup's pressure, and vice versa` | 13 | line 144, section F9 | exact |
| `no registry row; on this host the two were byte-identical in one read pass` | 14 | line 144, section F9 | exact |
| `**F10 — the kernel accumulates the total monotonically.**` | 8 | line 146, section F10 | exact |
| `That covers F12, the cgroup-code half of F9, U1's branch location and the mechanism half of U7.` | 17 | lines 37-38, wave-2 corrections | normalised (the line wraps mid-sentence) |

[obs] The withdrawal sentence is mori's own statement that it withdraws the cgroup-code half of
F9, which is what the S127 teaches cell relies on when it hands the root-identity fact to this
lane's S117.

## 4. The landed Gate records

[obs] The L1 landed the two Gate-record rows in `corpus/lessons/round-26.md` at commit
`ef72f10` ("round-26: C1 storage-integrity entry SH1-SH6, sources S128-S139 with snapshots,
Gate, SKILL section and registry, PROVINCE frontier, README row; routed defects 1,2,6,7,8 …").
The lesson text states that "The S126 and S127 records below are the Gate records round 25 owed
(routed defect 2)".

[obs] The landed rows carry, for each source, the id, the URL or repo path with revision, the
access date 2026-10-22, a quote of at most 25 words and its line location:

- S126 — `https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml`, 2026-10-22,
  `"Defaults to 60%."` at oomd.conf.xml line 190, tag v262, with the re-fetched bytes sha256
  `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617` recorded as equal to the
  S126 anchor; and `"Defaults to 30 seconds when unset or 0."` at line 202, tag v262.
- S127 — `mori-shokunin/corpus/knowledge/system-pressure-r24.md at commit 4f05dd5a (blob
  d4ccce4262d8224e362da65eb5ba4b851ad0fea2)`, 2026-10-22,
  `"records what those files are, exactly which shapes the kernel emits, which error codes the
  kernel returns,"` at line 46, section Scope, with the re-read bytes sha256
  `5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5` recorded as equal to the
  S127 anchor.

[obs] Both landed rows parse under the committed checker's own parser. Running the Gate parser
of `tools/check-storage-health.py` against `git show HEAD:corpus/lessons/round-26.md` returned
zero Gate findings and mapped S126 to the two quotes above (3 and 8 words) and S127 to the
17-word Scope quote.

[obs] The C1 gate is green with these rows in place: `python3 tools/check-storage-health.py
--revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467` printed `status PASS`, `verified_rows 6`,
`declared_rows 6`, no findings, exit 0. (The same command with the literal string `HEAD` exits
2 with `E-REVISION-INVALID`, so a full 40-hex revision is required — [obs], not a defect.)

## 5. Things this seat did not do, and open items

- [unk] The round-25 spot-check expected the S127 Gate record to cite the mori source with its
  revision; the landed row does cite the commit and the git blob id, so the row is traceable,
  but no mori file snapshot is committed under `.ufo/waves/round-26/sources/` for S126 or S127.
  Those two rows are historical round-25 rows whose snapshots live in the round-25 wave, and the
  round-26 snapshot rule applies to the round-26 sources S128-S139. Flip: if the L1 wants the
  two rows to be re-verifiable from the round-26 wave alone, the two fetched copies kept at
  `.ufo/waves/round-26/w1/ScribeGateS126S127/S126.oomd.conf.xml` and
  `.ufo/waves/round-26/w1/ScribeGateS126S127/S127.system-pressure-r24.md` have exactly the
  anchor digests and can be committed as-is.
- [obs] The S127 landed Gate row quotes the Scope sentence only. The F2, F9 and F10 quotes in
  section 3 are verified and available if the L1 wants the teaches cell's "F2, F9 and F10"
  citation to be quoted rather than only asserted.
- [obs] No lane file was edited by this seat. No git or jj write command was run against
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. No service, package, mount, scrub or
  counter action was performed; the only commands were `curl`, `sha256sum`, `wc`, `stat`,
  `git show`/`rev-parse`/`log`/`diff` (read-only) and local parsing.

## 6. Exact commands executed

- `curl -sSfL -o oomd.conf.xml https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml` → HTTP 200, 12 557 bytes.
- `sha256sum oomd.conf.xml` → `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`; repeated twice more (pipe and `cmp`), identical each time.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 4f05dd5a:corpus/knowledge/system-pressure-r24.md` → 229 lines; `| sha256sum` → `5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5`.
- `git -C …/mori-shokunin rev-parse 4f05dd5a:corpus/knowledge/system-pressure-r24.md` → `d4ccce4262d8224e362da65eb5ba4b851ad0fea2`; `rev-parse 4f05dd5a^{commit}` → `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`.
- `git -C …/mori-shokunin diff --stat 4f05dd5a HEAD -- corpus/knowledge/system-pressure-r24.md` → 16 insertions, 10 deletions (the sibling file moved on after the pinned commit; the pinned blob is what S127 names).
- `python3 tools/check-storage-health.py --revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467` → `status PASS`, `verified_rows 6`, `declared_rows 6`, findings `[]`, exit 0.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, exit 0, 25 W04 duplicate-URL warnings (S126 among them; that warning already existed at round 25 and is disclosed in the round-25 spot-check).

Scope: read=corpus/SOURCES.md (rows S120, S126, S127 and registry header), corpus/lessons/round-25.md (Gate table and errata), corpus/lessons/round-25-verifier-spotcheck.md (routed defect 2), corpus/lessons/round-26.md at HEAD, corpus/knowledge/memory-pressure-r25.json, tools/check-storage-health.py, tools/check-memory-pressure.py, /home/vgpnk/.omp/agent/RULES.md; wrote=.ufo/waves/round-26/w1/ScribeGateS126S127.md, .ufo/waves/round-26/w1/ScribeGateS126S127/S126.oomd.conf.xml, .ufo/waves/round-26/w1/ScribeGateS126S127/S127.system-pressure-r24.md; executed=curl fetch of the systemd v262 oomd.conf.xml (three times), sha256sum, wc -l, stat, cmp, git show/rev-parse/log/diff (read-only), check-storage-health.py at the full revision, sources-census.sh validate

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
