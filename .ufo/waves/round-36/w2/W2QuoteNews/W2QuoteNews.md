# W2QuoteNews — S199 pinned-NEWS quote audit (round 36, w2)

Seat: `tsukuroi-r36.W2QuoteNews`. Role: reviewer, assigned to re-open the pinned S199 bytes and judge
whether `corpus/knowledge/journalctl-v262-field-filter-r36.md` cites them accurately.
Freeze `1e926801195e304950e3eb9d2525ef8bbc245089`; change `c052bb7d41ced49aa888817069afd804eccfecf1`.
All work read-only: no VCS mutation, no pacman, no installs. Every path cited is absolute.

Timestamps below were pasted from `date -u +%H:%M:%SZ` at the moment of the step
(04:33:46Z fetch; 04:36:40Z malformed-value probes; 04:37:16Z coverage/man text; 04:38:39Z section scan;
04:38:48Z report dir).

## Verdict summary

| assigned item | verdict |
|---|---|
| 1. Re-open pinned S199 source bytes | **AGREE** — fetched, 1,271,752 bytes |
| 2. sha256 equals `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` | **AGREE** — exact match |
| 3. Quote is at lines 129-133 | **AGREE** — exact bytes; sentence spans 129-130, paragraph ends 133 |
| 4. Note cites S199 accurately | **AGREE on every S199-anchored claim**; three low-severity imprecisions in adjacent citations (F1-F3) |

No medium- or high-severity defect. The core C2 statement ("v262 rejects `-F`/`-N` combined with
journal-limiting options") is corroborated by the pinned bytes, the v262 sources, and live behavior.

## 1. Fetch

```
$ curl -sSL -o /tmp/systemd-NEWS-v262 https://raw.githubusercontent.com/systemd/systemd/v262/NEWS
$ wc -l /tmp/systemd-NEWS-v262
23386 /tmp/systemd-NEWS-v262
$ date -u +%H:%M:%SZ
04:33:46Z
```

Byte length 1,271,752 — identical to the count recorded by the pinner
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/SrcSystemdNews/SrcSystemdNews.md:104`).

## 2. sha256

```
$ sha256sum /tmp/systemd-NEWS-v262
a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657  /tmp/systemd-NEWS-v262
```

Exact match to the assignment's expected digest. AGREE.

## 3. The quote at lines 129-133

Raw bytes (`sed -n '129,133p' | cat -A`), eight-space bullet indent plus two-space continuation:

```
129|        * journalctl now rejects -F/--field together with filters such as$
130|          unit, boot, time, cursor or grep filters. Previously field listing$
131|          used sd_journal_query_unique(), which cannot represent those filters,$
132|          so the filters were silently ignored. Scripts relying on filtered$
133|          field lists should be adjusted to query entries explicitly.$
```

Normalized (continuation indent stripped, newlines to spaces), byte-for-byte:

```
* journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters. Previously field listing used sd_journal_query_unique(), which cannot represent those filters, so the filters were silently ignored. Scripts relying on filtered field lists should be adjusted to query entries explicitly.
```

- The assignment quote `journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.`
  is an exact prefix of the paragraph after `* ` — **AGREE**.
- Note the singular `--field` (the long form of `-F`). This is not a typo: the runtime string separately
  names `-F/--field=` and `-N/--fields`.
- Line 129 begins at byte offset 7492 and line 133 ends at byte offset 7868 (exclusive end 7869).
  The pinner's recorded range `[7492, 7869)` reproduces exactly.
- Section context verified: `CHANGES WITH 262:` at line 3, `Feature Removals and Incompatible Changes:`
  at line 26; the bullet is under both, as the note states. The 262 section runs to line 878
  (`CHANGES WITH 261:` at 879).

## 4. Does the note cite it accurately?

### AGREE — item by item

1. **Note line 3** asserts `NEWS:129-133`, `"CHANGES WITH 262" > "Feature Removals and Incompatible Changes:"`,
   sha256 `a494f038…a7657`, pinned at tag `v262`. All four verified above.
2. **§Safe substitution** quotes: `"Scripts relying on filtered field lists should be adjusted to query entries explicitly."`
   Appears verbatim at lines 132-133 (normalized). AGREE.
3. **§Falsifier 6** says NEWS does *not* carry the exact scope-rejection sentence and "says only that `-F` is
   rejected 'together with filters such as unit, boot, time, cursor or grep filters'".
   - exact string `cannot be combined with options that limit the journal` → count in NEWS = **0**
   - within lines 3-878 (the whole 262 section), `-N` / `--fields` → **no matches**
   - the quoted fragment is verbatim (line-wrapped between `such as` and `unit` in raw bytes; normalized quote is honest)
   AGREE, including the implicit point that S199 evidences only the `-F` half.
4. **S198 claim** ("man page at 262 does not carry the restriction"): re-fetched
   `https://man.archlinux.org/man/journalctl.1` (HTTP 200, 65,136 bytes) at 04:33Z:
   - sha256 `aaae4efa61ff9c56e6249feb2f4527db57f1a4beb0eac4ad1eeb111a4bbb83c2` — matches the note's S198 pin exactly
   - footer contains `systemd 262.1`
   - rejection-string count **0**; `man/journalctl.xml` at `v262` also **0** (repo blob sha `d54bbede…1edbdd`)
   AGREE.
5. **Source citations**: `src/journal/journalctl.c` v262 sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab`
   (note prefix `285b3d0c…d5d0ab` — matches); lines 958-960 are exactly
   `if (IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()) return log_error_errno(SYNTHETIC_ERRNO(EINVAL), "-F/--field= and -N/--fields cannot be combined with options that limit the journal.");`
   `src/journal/journalctl-filter.c` sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48`
   (note prefix `480f7a03…72f48` — matches). AGREE.
6. **Live counters**: this host runs `systemd 262 (262-1-arch)`.
   - `journalctl --no-pager -b 0 -F PRIORITY` → `rc=1`, stderr **84 bytes**, stdout 0; line is 83 chars + `\n`
   - `journalctl --no-pager -N PRIORITY,MESSAGE` → `rc=1`, **54** stderr bytes, `Extraneous arguments starting with 'PRIORITY,MESSAGE'`
   - `journalctl --no-pager -b 0 -N PRIORITY` → `rc=1`, **46** stderr bytes
   - `journalctl --no-pager -F PRIORITY PRIORITY=3` → `rc=1`, `Extraneous arguments starting with 'PRIORITY=3'`
   - `journalctl --no-pager -b all -F PRIORITY` → `rc=0`
   - safe substitution `-b 0 -o json --output-fields=PRIORITY | jq -r .PRIORITY | sort -u` → exit 0, `2 3 4 5 6 7`;
     the `-b -1` variant → exit 0, same six values
   AGREE on every measured number the note prints.
7. **Matrix artifact** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json`:
   54 cells = 6 `core` + 29 `ext` + 4 `merged` + 15 `live`, exactly the note's composition.
   All 40 cell ids cited in the note exist; every table row's REJECT/WORK verdict equals its cell `exit`
   (REJECT rows all `exit=1, stderr=84`; WORK rows all `exit=0`). Header records
   `rejection_line_bytes_with_newline = 84`, `rejection_line` exact, `journalctl_version_first_line = "systemd 262 (262-1-arch)"`.
   `peer_crosscheck = {peer_cells:10, overlap:6, overlap_all_agree:true, peer_only_rerun:4}` — matches the note's
   Unknowns note. AGREE.
8. **Prior state**: at the freeze base `6d76fb2`, `git grep` for the rejection string returns exactly one hit,
   `SCORECARD.md:1632`; none in `corpus/knowledge/` or `SKILL.md`. Working-tree `grep` now additionally hits the
   note itself (lines 14 and 91), as expected for a newly added entry. AGREE.
9. **Provenance**: the note's bytes in the working tree equal its bytes at `c052bb7d`
   (sha256 `0077b6cf7e81ef243997fe5bd8559f5e21569290f271b2f60cb0cd1b57a8a8bf` both), so I reviewed exactly the
   committed text. `SrcSystemdNews/s024-row.md:18,72` stores the same digest and the `[7492, 7869)` range;
   `SCORECARD.md:1739-1743` (pre-freeze correction item 7) states `S199` supersedes `S024` for this note. AGREE.

### DISAGREE — concrete imprecisions (all low)

**F1 (Low, factual, Sources line 126).** The note calls `field_list_has_scope_options()` "the **16-term**
limiting-option predicate". The v262 function has **15** disjuncts:
`arg_boot_filter, arg_invocation, arg_dmesg, arg_cursor, arg_after_cursor, arg_cursor_file,
arg_system_units, arg_user_units, arg_syslog_identifier, arg_exclude_identifier, arg_priorities,
arg_facilities, arg_since_set, arg_until_set, arg_pattern`.
The note's own decision table lists exactly those 15 limiter rows, so the count is internally inconsistent
with the note's table. Evidence: `sed -n '26,43p'` of the pinned `480f7a03…72f48` blob; term count 15.
No behavioral consequence; fix the word "16" to "15".

**F2 (Low, edge falsifier).** The decision-table row "`arg_boot_filter` | `-b`, `--boot=` (any value except `all`)"
overclaims. `journalctl --no-pager --boot= -F PRIORITY` exits **1** but prints
`Failed to parse boot descriptor ''` (35 stderr bytes), not the scope-rejection line — so under the note's own
definition (`REJECT = exit 1 with the scope-rejection line`) that cell is neither REJECT nor WORK.
`-b` with no argument does print the 84-byte scope line. The same parse-before-guard pattern holds for other
malformed limiter values: `--since=` → `Failed to parse timestamp: ` (28 B); `--until=` → same (28 B);
`-p ''` → `Unknown log level ` (19 B); `--facility=` (empty) exits 0. The predicate claim is untouched;
the parenthetical should read "any *parseable* value except `all`".

**F3 (Low, reproducibility/coverage wording).** The Consumers preamble says "Every `journalctl` occurrence in
`tools/` ... 43 hits across 4 files), with its verdict".
- `grep -rn journalctl tools/` today returns **53 hits across 5 files**, because of the untracked bytecode cache
  `tools/__pycache__/score-census-handoff-r32.cpython-314.pyc`; with `--exclude-dir=__pycache__` it is exactly
  **43 hits across 4 tracked files** — the note's number reproduces for sources, not for the literal command.
- The table's rows cover the invocation/fixture sites (all 12 census invocation lines are correct on their cited
  lines, as are the stub spans `tsukuroi-census.sh:1883-1900`, `score-census-handoff-r32.py:150-165` and `708-731`,
  `check-boot-chain.py:870`, `check-source-scope-correction.py:174`). The remaining hits are comment-only or
  definition/test-harness mentions (e.g. `tsukuroi-census.sh:153,171,192,209,224,240,242,258,407,968,974,977,985,989,1077,1218,1229,1359,1368,1406,1911,2046,2282,2283,2414,2585`;
  `score-census-handoff-r32.py:183,188,469,787,805`) and receive no row, so "every occurrence ... with its
  verdict" is stronger than what the table delivers. No verdict in the table is wrong.

### Informational (not defects)

**F4 [inf].** `live_namespace` (`journalctl --no-pager -F PRIORITY --namespace=x`) records `exit=0`, stdout 0 bytes,
stderr `No journal files were found.` (29 bytes). It proves only non-rejection, not a successful field listing.
The note defines `WORK = exit 0`, so the row is consistent as written; a reader who equates WORK with "lists fields"
would over-read it.

**F5 [inf].** NEWS's 262 bullet names only `-F/--field`; the note's title pairs `-F`/`-N`. The `-N` half is
correctly attributed to `journalctl.c:958-960` and the live cells, never to NEWS, so this is not a misattribution —
but S199 must not be cited for the `-N` clause on its own. The note keeps the two sources distinct.

## Residual risk

- **Upstream permanence** ([unk] in the note): I did not test systemd >262 or <262. The note's claim is
  source-scoped to the `v262` tag and its own Unknowns say so; nothing I ran widens or narrows that.
- **ExecC2Live matrix revisions**: I audited `matrix-mini.json` as it stands (54 cells; peer 10/6/4). The note
  already flags later revisions as uncovered; I confirm that flag is still apt.
- **Sampling**: I re-ran the rejection cells, every WORK-row cell cited in the table, the `-N` misuse cells and
  the substitution pipeline myself (~20 of 54). The remaining cells were validated from the file's own recorded
  `exit`/`stderr_bytes`/`stdout_sha256`, not re-executed.
- **Mutable URL drift**: the Arch `journalctl.1` page still hashes to the S198 pin today, but it is a mutable URL;
  the note's sha pin is what makes it auditable, and that pin currently holds.

## Verification gaps

- Did not run the full 54-cell matrix end-to-end, did not fetch `v261` NEWS to confirm absence, and did not test
  multi-limiter combinations beyond `--quiet -b 0 -F` (table scope).
- S198's "-N takes no argument" is established here from live behavior + the man text "field names currently used
  in all entries", not by reading the full §COMMANDS block.
- No `lsp` server answers Markdown or the corpus notes; caller/definition checks were done by direct source reads
  (journalctl.c / journalctl-filter.c) and live probes, not semantic LSP resolution. Recorded per role rules.

## Reproduction commands

```
curl -sSL -o /tmp/systemd-NEWS-v262 https://raw.githubusercontent.com/systemd/systemd/v262/NEWS
sha256sum /tmp/systemd-NEWS-v262
sed -n '129,133p' /tmp/systemd-NEWS-v262
grep -c -F 'cannot be combined with options that limit the journal' /tmp/systemd-NEWS-v262     # 0
journalctl --version | head -1
journalctl --no-pager -b 0 -F PRIORITY; echo "rc=$?"                                          # rc=1, 84 stderr bytes
journalctl --no-pager -N PRIORITY,MESSAGE; echo "rc=$?"                                       # rc=1, 54 stderr bytes
journalctl --no-pager -b 0 -N PRIORITY; echo "rc=$?"                                          # rc=1, 46 stderr bytes
journalctl --no-pager -b all -F PRIORITY; echo "rc=$?"                                        # rc=0
journalctl --no-pager --boot= -F PRIORITY; echo "rc=$?"                                       # rc=1, parse error, 35 bytes
journalctl --no-pager -b 0 -o json --output-fields=PRIORITY | jq -r .PRIORITY | sort -u       # 2 3 4 5 6 7
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -F \
  'cannot be combined with options that limit the journal' 6d76fb20f6ecbc940e5c8fff36c74060c885e161 -- .
```

## Tooling

No installs or upgrades; no pacman invocation of any form. Tools used: `curl`, `sha256sum`, GNU grep/awk/sed,
`python3` (3.14, stdlib only), `jq`, `journalctl` (read-only), `git` (read-only: `log`, `show`, `grep`, `ls-files`).
