VERDICT: defect-found

Scope: `tools/lint-grounding-r51.py` at 2732ee6c06108c031c4d8043239b994e0504eb2f (`git show`, lane bytes), audited against its docstring (lint.py:1-29). The pinned lint PASSES (lint_ok 3). Its gap leg is self-consistent but under-covers: it omits 14 lines the rows cite outside declared ranges, and the quote leg and the tokenizer each admit defects a fixture reproduces. Receipts: `.ufo/waves/round-51/w1/R51RevLint/` (`fixtures-lint-r51.py` regenerates every fixture from `git show`; `fixtures-lint-r51.out` is its output; `lint-revision.json`; `emit-gaps.txt`). No tool was installed; scratch removed.

## 1. Counts at the pinned revision

- `python3 tools/lint-grounding-r51.py --revision 2732ee6c…` → `quotes 63, quote_bad 0, cites 28, cite_bad 0, gaps_computed 62, gap_missing [], gap_extra [], lint_ok 3, verdict PASS`. Per row: quotes 12/39/12, cites 2/20/6 (GR1/GR2/GR3).
- `--emit-gaps` → 5 bullets, 62 lines, byte-identical to entry lines 271-275.
- Quote count cross-check: `**Quote.**` occurrences in the file = 63 (all match QUOTE_RE; the one non-matching "Quote" word is prose at entry line 256, not a quote).

## 2. Holes (each reproduced; fixture = the pinned entry with the one stated edit)

### H1 (high) Gap block omits 14 truly-cited out-of-range lines; a truthful block is rejected
Tokenizer: `CONT_RE` (lint.py:78) only continues a citation when `:a` follows the previous `file:line` immediately (`,`/`and`/`;`/space). Colon-only parenthetical references after a sentence cite are not tokenised:
- entry L79 `(:3075-3078)`, L80 `(:3080-3082)`, L81 `(:3087-3090)`, L82 `(:3093-3095)` — all S240 ioctl.c (the sentence names `ioctl.c:3072-3073` at L79). Lines 3076-3078, 3081-3082, 3087, 3089-3090, 3094-3095 lie outside S240's declared 3066-3075, 3118-3140, 5578-5584 (SOURCES.md S240 anchor) and are missing.
- entry L66 `(:3114-3116, returned at :3250-3253)` — words between cite and continuation break `CONT_RE`. S242 scrub.c 3250-3253 (`out_free_ctx:` … `return ret;`) lie outside 1365-1385, 3140-3162, 3215-3226, 3321-3337 and are missing.
Fixture F1: replace the block with the truthful set (S237 421, 439, 1546; S240 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190; S242 3081, 3094-3139, 3250-3253; S243 1288, 2015; S247 1197). Lint prints `FAIL`, `gap_extra ["S240 ioctl.c: 3076-3078, 3081-3082, 3087, 3089-3090, 3094-3095", "S242 scrub.c: 3250-3253"]`, `gaps_computed 62`. Correct entry rejected; pinned entry (missing 14 lines) passes. Count: 62 computed + 10 S240 + 4 S242 = 76 true lines.
Consequence for L1: the frozen tool (sha256 35df03c5…) and any truthful block are incompatible at this revision. Either the tool changes (new frozen hash, new claim) or the block stays under-declared. This is the decision to make before w2.

### H2 (high) Quote leg bypassed by a bullet prefix or trailing text; false quote text passes
QUOTE_RE (lint.py:76) is anchored `^\*\*Quote\.\*\* ` and `"\s*$`. Any other form falls to the prose leg (lint.py:237), which checks only the `file:line`, not the quoted words.
- F2a: entry L27 → `- **Quote.** \`S246\` cmdline.c:147: "* potentially suffixed with K, M, G, T, P, Z."` → PASS, quote_bad 0.
- F2b: L27 → `**Quote.** … "* potentially suffixed with K, M, G, T, P, Z." (checked)` → PASS.
- Control F2c (same false text in conformant form) → FAIL, `quote S246 cmdline.c:147: not the whole line; line is '* potentially suffixed with K, M, G, T, P, E.'`.
Fix: reject any line containing `**Quote.**` that is not an exact QUOTE_RE match.

### H3 (medium) Empty quote matches any blank source line; whitespace collapse accepts tab-for-space
- F3a: insert `**Quote.** \`S246\` cmdline.c:152: ""` (cmdline.c:152 is blank in the snapshot) → PASS. Control F3b (`cmdline.c:153: ""`, non-blank) → FAIL. An empty quote evidences nothing. Reject empty quotes.
- `norm` (lint.py:99-100) is `' '.join(s.split())`: any run of whitespace equals one space. The pinned GR1 quote L27 `"* potentially …"` matches snapshot line 147 `' *\tpotentially suffixed with K, M, G, T, P, E.'` (a TAB at S246 cmdline.c:147, verified by reading the snapshot bytes). The docstring says "a changed character is a defect"; a tab-to-space change is accepted. Low impact; decide explicitly.
- Not tested (code-read only): entity handling. `S248` snapshot has no `&` in any line (checked), so no row can exercise it; the comparison is on raw bytes, so a decoded `<` against a source `&lt;` would fail.

### H4 (medium) En-dash range silently truncated to its first line
CITE_RE (lint.py:77) takes `-` only. F5a: entry L176 `S240 ioctl.c:3190)` → `ioctl.c:3190–3196)` (en dash) → PASS, gap block unchanged; lines 3191-3196 (outside declared) go unchecked. F5b hyphen control → FAIL, `gap_missing ["S240 ioctl.c: 3191-3196"]`. Same truncation for spaced ranges (`3250 - 3253`). Fix: accept `[-–—]` with optional spaces, or reject any unrecognised range separator in a `file:` context.

### H5 (medium) Citations to a basename outside the row's PROSE map are skipped silently
lint.py:238-240: `sid = PROSE[row].get(base); if sid is None: continue`. Extensions outside `(c|h|xml|service|txt|sh)` (lint.py:77) are never tokenised either.
- F6a: insert into GR1 `Probe: see ioctl.c:99999 and btrfs-scrub@.timer:9.` → PASS (no cite counted).
- Control F6b: `Probe: see cmdline.c:99999.` (mapped basename) → FAIL, `cite cmdline.c:99999-99999: does not resolve in S246`.
Fix: treat any `token.ext:digit` as a cite and fail when its basename is not mapped for the row.

### H6 (medium) Spaced colon, backtick-separated and word-separated continuations are not tokenised
- F7a: GR3 insert `Probe: \`scrub.c: 2000\`.` → PASS. Control F7b `scrub.c:2000` → FAIL `gap_missing ["S237 scrub.c: 2000"]`.
- F8a: `Probe: (\`scrub.c:1546\`, \`:2000\`).` → PASS. Control F8b `(scrub.c:1546, :2000)` → FAIL. Live instance: GR3 L193-194 `scrub.c:1546`, `` `:439` `` (439 is covered only by the quote at L220 — no gap effect today).
- F9a: `Probe: scrub.c:1512, returned at :2000.` → PASS. Same shape as the live H1 miss at L66.
- Other live misses with no gap effect today (in-range or inside a cited span): L62 `:1265-1268` (line start), L65 `:3094-3095`, L66 `:3109-3111`, `:3114-3116`, L67-70 `:3120-3123`, `:3127-3133`, `:3138-3142`, `:3147-3153` (inside the L65 cite `scrub.c:3094-3153`, so they vanish if that cite is edited), L80 `:3084-3085` and L83 `:3109-3110`, `:3115` (quoted), L173 `:3133` (in S240 3118-3140), L194 `:439`.

### H7 (medium) Duplicate gap-block keys overwrite silently
lint.py:279 `out[(sid, base)] = expand(...)` keeps only the last line per key. F10a: insert `- S237 scrub.c: 2000` before the S237 line → PASS, bogus `2000` discarded. F10b control (line after) → FAIL, `gap_extra ["S237 scrub.c: 2000"]`. Fix: reject a duplicate key.

### H8 (medium) The declared-range source is unpinned, so widening it removes gaps
`declared_ranges` reads `corpus/SOURCES.md` at the revision (lint.py:206, 299). `.ufo/waves/round-51/frozen/FROZEN-hashes.txt` lists tools and the battery only (six lines; `grep SOURCES` finds none). F11a: widen the S237 anchor cell by `, 421, 439, 1546` (one-line edit, `1498-1512, 1925-1945;`) and regenerate the block without the S237 line → PASS. Control F11b (pinned registry, same block) → FAIL, `gap_missing ["S237 scrub.c: 421, 439, 1546"]`. The entry bytes and tool hash are unchanged in F11a, so the row hashes do not see it. Fix: pin the SOURCES.md anchor cells of SNAPSHOTS rows, or derive the declared set from a frozen file.

### H9 (low, latent) Basename-to-S-row map is per row, not per context
PROSE (lint.py:67-74) maps `scrub.c` to S242 in GR2 and to S237 in GR3, and the cite leg checks only that the line exists in the mapped file. No wrong binding exists at this revision (checked below), but a GR3 kernel citation `scrub.c:N` with N ≤ 2232 would bind silently to btrfs-progs S237. [inference: not fixture-run.]

## 3. Positive checks (what holds)

- Declared-range parser `declared_ranges`/`parse_ranges` (lint.py:112-142) reads every S-row anchor as written: S237 `67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945`; S240 `3066-3075, 3118-3140, 5578-5584`; S242 `1365-1385, 3140-3162, 3215-3226, 3321-3337`; S243 `72-74, 2021-2049, 2113`; S247 `700-703, 1143-1144, 1235, 1256-1268, 1276-1300`; S244 `1-10`; S246 cmdline `142-201`, vsprintf `79-115`, kstrtox `26-40`; S248 `62-116`; S249 none (OWN_WORK, skipped at lint.py:251). No duplicate S-row id in SOURCES.md. `parse_ranges` drops a non-matching part silently (lint.py:117-118); that only shrinks the declared set, so it fails closed [code-read].
- Quote binds to the cited number: lint.py:232-233 compares against `src[n-1]`. F4 (quote text of cmdline.c:147 cited as :159) → FAIL, `not the whole line; line is '/* Consume valid suffix even in case of overflow. */'`. A leader-dropped quote (F2d, `potentially suffixed…`) → FAIL.
- Pinned quote L27 is correct except the tab-for-space accepted in H3.
- PROSE binding in the pinned rows: GR2 `scrub.c` cites (L62, L65, L67-70, L87-88) are S242 kernel lines, and GR3 `scrub.c:1512` (L193, "btrfs-progs") and `:1546` are S237 — consistent with the labels. GR2 `ioctl.c:3132` (L173) is S240 3132 `if (!capable(CAP_SYS_ADMIN))` and 3133 `return -EPERM;` in `btrfs_ioctl_scrub_progress` (read from `.ufo/waves/round-43/frozen/src/ioctl.c` at the revision, lines 3124-3133): the prose matches the code.
- Gap set equality (lint.py:317-324) is correct both directions for the sets it computes (F10b, F11b, F5b, F1 each fail in the expected direction).

## 4. Proposed amendment inputs (for L1; the frozen tool is not changed by this seat)

- Fix the tokenizer (H1, H4, H5, H6): attach each colon-led `:a(-b)` to the nearest preceding `file.ext` in the same sentence or parenthetical; accept `-`/`–`/`—` with optional spaces; treat every `token.ext:digit` as a cite; fail on any unmapped basename.
- Fix the quote leg (H2, H3): every line containing `**Quote.**` must match the exact form; reject empty quotes.
- Reject duplicate gap-block keys (H7); pin the SOURCES.md anchors (H8).
- Truthful block for the entry, under the fixed tokenizer (exact text, 5 bullets, 76 lines):
```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3076-3078, 3080-3082, 3084-3085, 3087-3090, 3093-3095, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139, 3250-3253
- S243 sysfs.c: 1288, 2015
- S247 dev-replace.c: 1197
```
Under the frozen tool this block FAILS (F1). Under the frozen tool, the pinned block PASSES only because the tool misses the 14 lines. The L1 must choose between a tool change (new frozen hash and claim) or a block that the frozen tool accepts while under-declaring.

## 5. Not done

- No change to any lane file, index or fleet file. Read-only `git show` and fixture copies in scratch only (removed).
- The counter `tools/check-scrub-admission-r51.py` and the other C2/C3 tools were not audited (not in this item).
- Prose claims in `## Limits` (entry L240-276) carry unlinted `file:line` cites (e.g. `dev-replace.c:1111, :1126-1144`, `scrub.c:421`); they are outside GR1-GR3, so the lint does not check them.
- Semantic correctness of each row claim beyond the cited line text was not judged.
- Tooling: none installed, none upgraded.
