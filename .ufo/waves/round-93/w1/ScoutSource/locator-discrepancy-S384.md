# Locator discrepancy in the working-tree S384 row and in the r93 lesson's Gate table

**Observed (2026-11-08, bytes pinned twice and independently):**

| artefact | says | measured |
|---|---|---|
| `corpus/SOURCES.md` S384 anchor (working tree, uncommitted) | "raw 2089-2091 (`--version` dispatch to `version()`), **print at raw 2029**, `--version-only` raw 2022-2026" | the print `puts("Limine " LIMINE_VERSION);` is at raw **2035**; raw **2029 is a blank line** |
| `corpus/lessons/round-93.md` `## Gate` table, S384 row | `"puts(\"Limine \" LIMINE_VERSION);" (raw 2029; `--version` dispatch raw 2090)` | same off-by-6 |
| `corpus/lessons/round-93.md` `## Gate` table, S384 row | "`--version` dispatch raw 2090" | raw 2090 is `|| strcmp(argv[1], "--version") == 0) {` — the dispatch is 2089-2091 ✓ |
| S384 anchor | "`--version-only` raw 2022-2026" | 2022 is the `--version-only` strcmp ✓, but the **print** it selects is `puts(LIMINE_VERSION);` at raw **2031**, outside 2022-2026 |

**Evidence the measurement is not a local artefact** (three independent copies, one sha256):

- upstream raw `v12.9.5/host/limine.c` → sha256 `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0`
- the lane's own r93 pin `.ufo/waves/round-93/before/src/limine-v12.9.5-host_limine.c` → **same sha256**
- my refetch → **same sha256**

and within those bytes (no CRLF, 2096 lines):

```
2029 ''                                            <- blank
2030 '    if (version_only) {'
2031 '        puts(LIMINE_VERSION);'               <- --version-only print
2035 '    puts("Limine " LIMINE_VERSION);'         <- --version print
```

`grep -n 'puts("Limine " LIMINE_VERSION);'` → `2035`. `grep -n 'puts(LIMINE_VERSION);'` → `2031`.
The same line numbers hold at v12.9.4 and v12.9.6 (`host/limine.c` is byte-identical across all
three tags, sha256 `4da21c7c…`).

**Why it matters.** The row's *quote* is verbatim-correct — only the **line locator** is off by
six. `corpus/CORPUS.md` §SOURCES.md contract v1 requires an `anchor` that is an "exact section /
heading / page / **line** plus revision". A locator that points at a blank line cannot be
re-derived by a reader who opens the file at the named line, and the contract's rule 1 asks that
a quote's location ground its `teaches` cell. The locator is the row's own verification handle.

**Proposed correction (appended row, per contract rule 2 — a correction is a new row whose
`teaches` opens `supersedes S0NN —`):** the next unused id after S384 is **S385** … which is
also the id the r93 lesson already names for the S377 anchor correction. **The two corrections
must not collide on one id.** Recommended allocation, since the S377 correction is already
claimed as S385 in the lesson and this seat's S377 proposal reuses it:

- **S385** — the S377 anchor correction (as proposed in `s377-correction.md`), and
- **S386** — this locator correction for S384.

Proposed S386 row (11 cells, `|`-free, next-unused id, `supersedes` prefix):

```
| S386 | Limine v12.9.5 host/limine.c — the `limine --version` output the V3 installed-version probe parses, locator-corrected — https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c | code | A | The exact lines of the `limine --version` output the V3 installed-version probe parses | tag v12.9.5 (file sha256 `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0`), raw 2035 (`puts("Limine " LIMINE_VERSION);`), raw 2031 (`puts(LIMINE_VERSION);`), raw 2089-2091 (`--version` dispatch to `version()`), raw 2002 (`#define LIMINE_VERSION "%VERSION%"`, substituted from `@PACKAGE_VERSION@` by `GNUmakefile.in` raw 170); fetched 2026-11-08 | supersedes S384 — the version print is at raw 2035, not raw 2029 (raw 2029 is a blank line), and the `--version-only` print is at raw 2031, outside the cited 2022-2026; the output shape is unchanged | mined | 2026-11-08 | on-release | corpus/knowledge/limine-version-probe-r93.md, corpus/lessons/round-93.md |
```

If the lane prefers to correct S384 in place rather than append (contract rule 2 allows only
`status`, `recheck` and `used-by` to change in place — an `anchor` change is **not** one of
them), then the lesson must log the anchor change old→new and carry a QUALITY-127 sweep receipt
for the superseded locator string, exactly as it did for S377. **The lane must pick one route and
apply it to both corrections consistently** — the r93 lesson currently names an S385 that does
not exist while doing an in-place S377 edit and an in-place S384 edit whose locator is wrong.
