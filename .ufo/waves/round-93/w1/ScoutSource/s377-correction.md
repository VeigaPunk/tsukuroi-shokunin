# S377 — proposed appended-row correction (never a silent rewrite)

## The defect (r92 spot-check routed defect 3, reproduced)

`corpus/SOURCES.md` S377's **anchor** cell at the freeze commit `c633f49a` reads
`Python 3.14 docs, `-P` and `-I` entries, opened 2026-11-08`.
The ≤25-word **quote** cell is correct and unchanged. The anchor's *version string* is wrong:

- live page (2026-11-08): `Python 3.15.2 documentation` (3 occurrences; `<title>1. Command line
  and environment &#8212; Python 3.15.2 documentation</title>`);
- r92 pinned snapshot `.ufo/waves/round-92/before/src/python-3-cmdline.txt` line 1:
  `1. Command line and environment — Python 3.15.2 documentation`.

Both already carried 3.15.2 when the row was written — the anchor was wrong at write time, not
stale since.

## Current lane state (measured, 2026-11-08)

- Working tree: `git diff corpus/SOURCES.md` shows the **S377 row changed in place**, anchor cell
  `Python 3.14 docs` → `Python 3.15.2 docs`.
- `git diff -U0 c633f49a -- corpus/SOURCES.md | grep -E '^-[^-]'` prints **exactly 1** line (the
  S377 row) — so the QUALITY-60 sweep requirement is met and the change is disclosed.
- `corpus/lessons/round-93.md` lines 26-29 log the anchor change old → new and name the sweep
  receipt `.ufo/waves/round-93/after/q127-s377-pre.txt` (present; it prints the old cell at the
  freeze revision `c633f49a:corpus/SOURCES.md:388`). The r92 spot-check's routed defect 3
  allows exactly this route ("correct the anchor by an appended row **or** a logged anchor
  change, never a silent rewrite").
- **But** `corpus/lessons/round-93.md` line 38 states the routed-3 disposition as
  *"S377's anchor is corrected by an appended row (S385) rather than a silent rewrite"*, and
  **no S385 row exists** in `corpus/SOURCES.md` (`grep -c '^| S385'` → 0; `S385` occurs in the
  whole lane only in that lesson sentence). The lesson therefore claims a correction mechanism
  it did not use, and the claim is a dangling id in prose.

## The proposed appended row (contract-compliant form)

`corpus/CORPUS.md` §SOURCES.md contract v1 rule 2: *"**Append-only.** Only `status`, `recheck`
and `used-by` change in place, and each change is logged old→new in the round lesson. A
correction is a new row whose `teaches` opens `supersedes S0NN —`."* The next unused id after
S384 is **S385**. Proposed row (11 cells, `|`-free, next-unused id, `supersedes` prefix):

```
| S385 | Python 3 documentation — command line and environment (`-P`, `-I`), version-pinned — https://docs.python.org/3.15/using/cmdline.html#cmdoption-P | docs | A | What `python3 -I` / `-P` do to `sys.path` and to `PYTHON*` variables, at the docs release that carries them | tag `3.15` docs (docs version string `Python 3.15.2 documentation`, page title `1. Command line and environment — Python 3.15.2 documentation`), `-P` entry `cmdoption-P`, `-I` entry `cmdoption-I`; fetched 2026-11-08, raw bytes sha256 `d3c503060ebf18e5a807ba35d8527cfde49f8322373b9111e5c26d657b658cf6`; the `/3/` alias (sha256 `2371db30c8f4dfbb8118f990ebd6aed2203c719ed0194d2c46e3325098477aba`) differs from it only in the Sphinx build stamp | supersedes S377 — the anchor named `Python 3.14 docs`; the pinned snapshot (`.ufo/waves/round-92/before/src/python-3-cmdline.txt`) and the live page both carry `Python 3.15.2`, and the version-pinned URL keeps the locator from drifting with the next Python release; the `-I`/`-P` quote is unchanged | mined | 2026-11-08 | on-release | corpus/knowledge/limine-r92-oracle-isolation.md, corpus/lessons/round-92.md, corpus/lessons/round-93.md |
```

**Why this shape:** the anchor moves to a version-pinned URL (the `/3/` alias is a rolling
"latest stable" URL, so the version string drifts again on the next Python release), the row opens
`supersedes S377 —` as rule 2 requires, and S377 stays untouched as the historical record.

**Two ways to land it — pick one, do not do both:**

1. **Appended row (the proposal above, this seat's recommendation).** Land S385 as above. Then
   the lesson's line-38 sentence becomes true and no dangling id remains. Under rule 2 the
   in-place S377 edit is the one thing to undo: revert S377's anchor cell to `Python 3.14 docs`
   (its historical value) and let S385 carry the correction. **The revert itself is an in-place
   change and must be logged old→new in the lesson and covered by the QUALITY-60 sweep**, which
   then prints 2 changed lines (the S377 removal and the S385 removal-side).
2. **Logged anchor change (what the working tree already does).** Keep the in-place S377 anchor
   edit, keep the `q127-s377-pre.txt` sweep receipt, and correct the lesson's line-38 sentence to
   name the *logged anchor change* instead of a non-existent S385. This route is explicitly
   permitted by the r92 spot-check's routed defect 3 wording, and the sweep requirement is
   already met (1 changed line). What it does **not** do is make the docs version
   release-independent: the `/3/` URL still moves under the row.

**Either way, one correction to the lesson's prose is required:** line 28's parenthetical
"*(the 3.17 mentions are the development banner)*" is false. Measured on the live page: `3.17`
occurs twice, both inside the `-b`/`-bb` deprecation note
(`schedule them to become no-op in Python 3.17` / `Starting with Python 3.17, no BytesWarning
will be raised for these cases; use a type checker instead`); the page carries no development
banner (`development version` → 0, `pre-release` → 0) and
`https://docs.python.org/3.17/using/cmdline.html` is HTTP 404. The pinned r92 snapshot carries
the same two `3.17` occurrences at its lines 182 and 184, in the same note. The conclusion
("the page is 3.15.2") is right; the stated reason is not, and a reader who took "3.17 banner"
for a page version would infer the wrong docs version.
