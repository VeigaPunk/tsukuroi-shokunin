# r92 row freshness — refetch of S377, S378, S379, S380, S381

All refetches: 2026-11-08 (UTC) 06:11Z. HTTP status and byte counts are in `pin-table.tsv`.
The r92 pins live at `.ufo/waves/round-92/before/src/` with digests in that directory's
`SHA256SUMS`; "identical" below means byte-for-byte equal by sha256.

| row | URL refetched | r92 pin sha256 | live sha256 | identical? |
|---|---|---|---|---|
| S377 | `https://docs.python.org/3/using/cmdline.html` | `558f4c7def649d2fbe69a61a785905054864918cff0fa9ea6a9e3c8e8b54f931` (rendered text `python-3-cmdline.txt`) | `2371db30c8f4dfbb8118f990ebd6aed2203c719ed0194d2c46e3325098477aba` (raw HTML) | **not comparable byte-wise** (different renderings); the *docs version string* is compared below |
| S378 | `https://raw.githubusercontent.com/containers/bubblewrap/main/bwrap.xml` | `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da` | `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da` | **identical** |
| S379 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c` | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | **identical** |
| S380 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog` | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` | **identical** |
| S381 | `https://api.github.com/repos/Limine-Bootloader/Limine/issues/700` | `7c7ac6e0f9330da89cad4bc999a0a3239a39ff57f33629b557b41109499f1049` | `7c7ac6e0f9330da89cad4bc999a0a3239a39ff57f33629b557b41109499f1049` | **identical** (the `body` field compared separately: identical) |

## S377 — the docs version string (routed defect 3)

| artefact | version string carried |
|---|---|
| live page `https://docs.python.org/3/using/cmdline.html` (fetched 2026-11-08) | **`Python 3.15.2 documentation`** — 3 occurrences; `<title>1. Command line and environment &#8212; Python 3.15.2 documentation</title>` |
| r92 pinned snapshot `.ufo/waves/round-92/before/src/python-3-cmdline.txt` | **`Python 3.15.2 documentation`** — line 1 reads `1. Command line and environment — Python 3.15.2 documentation` |
| `corpus/SOURCES.md` S377 anchor at the freeze commit `c633f49a` | `Python 3.14 docs, `-P` and `-I` entries, opened 2026-11-08` — **the anchor names 3.14; both the pinned text and the live page carry 3.15.2** |

So the r92 spot-check's routed defect 3 reproduces exactly: the ≤25-word quote is unchanged and
correct; only the anchor's version string is wrong.

**Both the pinned snapshot and the live page already carry 3.15.2** — the anchor was wrong when
the row was written, not stale since.

### Two further freshness facts about S377 that the row does not carry

1. **The URL is a rolling "latest stable" URL.** `https://docs.python.org/3/using/cmdline.html`
   follows Python's current stable release, so its content changes on every Python release and
   the anchor's version string drifts again on the next one. The version-pinned URL
   `https://docs.python.org/3.15/using/cmdline.html` (HTTP 200, 171073 bytes, sha256
   `d3c503060ebf18e5a807ba35d8527cfde49f8322373b9111e5c26d657b658cf6`) carries **the same docs
   content**: `diff` against the `/3/` copy is exactly **one** line, the Sphinx build stamp
   (`Last updated on Nov 08, 2026 (00:12 UTC)` vs `(06:12 UTC)`). The row's URL should be
   version-pinned and the recheck cadence should follow Python's release, not a fixed 180d.
2. **The round-93 lesson's parenthetical about "3.17" is wrong.** `corpus/lessons/round-93.md`
   line 28 says the live page's `3.17` mentions "are the development banner". Measured on the
   live page: `3.17` occurs **2** times, and both are inside the `-b`/`-bb` deprecation note
   (`Deprecated since version 3.15: Deprecate -b and -bb command line options and schedule them
   to become no-op in Python 3.17.` / `Starting with Python 3.17, no BytesWarning will be
   raised for these cases; use a type checker instead.`). The live page carries **no**
   development banner (`development version` → 0 occurrences; `pre-release` → 0), and
   `https://docs.python.org/3.17/using/cmdline.html` is **HTTP 404** — there is no 3.17 docs
   tree. The pinned r92 snapshot carries the same two `3.17` occurrences at its lines 182 and
   184, in the same `-b`/`-bb` note. The conclusion ("the page is 3.15.2") is right; the reason
   offered for it is not, and a reader who took "3.17 banner" for a page version would infer the
   wrong docs version.

## S378 — bubblewrap

Live `main` is byte-identical to the r92 pin. The version claim in the anchor
(`bwrap 0.13.1 source bwrap.xml`) still holds: the latest upstream release is **v0.13.1**
(published 2026-10-14T12:21:00Z) and `main`'s head is `1fb0aa26d3eb66254f7742e704add7f82f41a582`
(2026-10-14T12:26:03Z); the file at tag `v0.13.1` is byte-identical to `main`'s copy
(sha256 `2cb77df2…`). The quoted options are still present at the same places in the live file:
`--unshare-all` raw 158-160, `--clearenv` raw 232-235, `--die-with-parent` raw 587.
Caveat for the boundary: the URL is a **branch** URL (`main`), so it is mutable by construction —
a tag URL (`v0.13.1`, same bytes today) would be the re-openable locator.

## S379 / S380 — the v12.9.6 Limine files

Both refetched byte-identical. The S379 anchor's line numbers were re-checked against the
refetched v12.9.6 file: `create_menu_tree()` raw 298-407 ✓; cut raw 328-330 ✓; label-end NUL
raw 362-365 ✓; `menu_tree = create_menu_tree();` at raw 668 ✓ (the "reads after 668" pointer);
`config_get_value` at raw 727 ✓. The S380 anchor's `Miscellaneous:` block at raw 13-16 still
carries both upstream sentences ✓.

## S381 — Limine issue #700

Refetched byte-identical (JSON sha256 and `body` both equal to the r92 pin). State is
`closed`, created 2026-10-27T18:52:23Z, closed 2026-10-27T22:43:43Z. The timeline confirms the
`closed by #702` claim: one `cross-referenced` event at 2026-10-27T19:31:03Z pointing at
**#702 "docs: clarify positioning of global options"**, which is `state: closed`,
`merged_at: 2026-10-27T22:41:28Z`, merge commit `23cae02972ee54e5fb34df8e3e62382dcd5702cf`,
body `Resolves #700 by correcting the incorrect documentation`. The reporter's `### Cause` block
still reads as quoted. **One freshness note the row does not carry:** the outcome was
documentation-only. PR #702 changed `CONFIG.md` — v12.9.5 `CONFIG.md` raw 76 says
`Global options can appear anywhere in the file and are not part of an entry`, v12.9.6
`CONFIG.md` raw 76 says `Global options must come before the first menu entry` — and the code
cut is unchanged between the two tags (`common/lib/config.c` identical, `a940acae…`). So #700's
"reporter's reading" is a lead that upstream resolved by **documenting** the pre-12.9.5 rule,
not by changing the parse; the S379/S380 pins are what carry the behaviour.
