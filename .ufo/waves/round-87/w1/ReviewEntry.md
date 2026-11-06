# ReviewEntry — C2 entry review: limine-pin-plane-r87 (LP1-LP8)

Seat: ReviewEntry-4, wave round-87 w1, 2026-11-06. Advisory review; a seat is the lane — nothing here
is an admission. Lane revision measured: `cefb4188b484329c4908a19a277f8fb120fb4f56`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → same; `log --oneline -1`
→ "cefb4188 round-87: entry — limine-pin-plane-r87 LP1-LP8, SOURCES S350-S354, live gate receipt").
Scope: `corpus/knowledge/limine-pin-plane-r87.md` + `.json` rows LP1-LP8 against the pinned snapshots
`.ufo/waves/round-87/before/src/` (sha256-verified, rc=0), plus SOURCES S350-S354, Operator actions,
Limits, and the header's host/live-receipt claims. Read-only: no lane file edited; no `sudo`; no
scratch dir was needed (pure reads with absolute paths; nothing to clean). No tool installs or
upgrades were performed. No `lsp` device is mounted in this session, so caller/definition checks
used `grep`/`read` as the documented fallback (no semantic-server proof claimed).
Receipts: `.ufo/waves/round-87/w1/ReviewEntry/` (sed-proofs.md, quote-verification.txt,
sources-check.txt).

## Verdicts per row

| Row | Verdict | One-line reason |
|---|---|---|
| LP1 | support | case-insensitive, line-start (`SEPARATOR '\n'`, config.c:25), `:`-terminated key match; blanks/CR strip loop 527-552 precedes matching; `#` lines cannot hold a key. Quote verbatim (19 words). |
| LP2 | **partial** | key enumeration complete and fully anchored (exhaustive CONFIG.md scan); the sentence "A `#...` inside `cmdline` or `comment` is not a pin" rests on lines no citation covers (cmdline 272-274, comment 267-268; URI grammar S351 28-32). |
| LP3 | support | backward scan from end of URI = last `#` (uri.c:78-104); exactly 128 hex, either case; else URI_ERROR. Quote verbatim with `…` (20 words). |
| LP4 | support | blake2b hash of the file as stored (CONFIG.md 446-447, 458-460); `$` resource hashed compressed, before decode (uri.c 344, 403-470; decode at 485-486). Quote verbatim substring (19 words). |
| LP5 | **partial** | panic-default, `no` case-insensitive, first occurrence, warning+prompt all verified; but cited uri.c:311 accepts lowercase `y` too, so "`Y` boots … any other key returns" says more than the cited lines. |
| LP6 | support | SB+enrolled config → panic + editor off (menu.c 1714-1717); no enrolled hash → SB inactive (CONFIG.md 453-454); wallpaper/font skipped either way (152-156, 450-451; uri.c 18-26, 302, 696-702). Quote verbatim (14 words). |
| LP7 | support (anchor gap) | objcopy in-place rewrite verbatim from HTML 189-191; `--dump-section` at 634; host_value grounded in round-86 M3 + host receipt mtimes. Quote tail sits on line 191, outside the cited 189-190. |
| LP8 | support | live receipt findings are exactly the two quoted strings; pins 50/56/64 `OK`/`none`; line 72 fallback has no `#`; line 8 `no` → prompt; rc 1. |

Counts: 6 support, 2 partial, 0 refute. All 8 quotes verbatim (whitespace-normalized) and ≤25 words
(quote-verification.txt). .md and .json rows are consistent with each other (statements, sources,
quotes, host values identical).

## Findings (by severity)

### F1 — LP2: unsourced sub-claim (partial)
Statement cell, last sentence: "A `#...` inside `cmdline` or `comment` is not a pin."
The cited anchors (S350 111-113, 134, 210, 295-308, 330-350) never mention `cmdline` or `comment`
(CONFIG.md:267-268, 272-274 — uncited) and never cite the URI grammar that confines `#hash` splitting
to URI values (S351 28-32 — uncited for this row). The claim is TRUE under the pinned grammar (only
URI values reach `uri_resolve`; cmdline/comment are plain strings), but it says more than the cited
lines. Proposed rewording of the Source cell (md table + .json `source`):
`S350 111-113, 134, 210, 267-268, 272-274, 295-308, 330-350; S351 28-32`
and extend the S350 anchor in corpus/SOURCES.md with `267-268, 272-274` (S351's anchor already
covers 28-32 via 28-104). No statement change needed once cited.

### F2 — LP5: `y` also continues (partial, minor)
uri.c:311 (inside the cited 301-312): `if (ch != 'Y' && ch != 'y') {` — lowercase `y` boots too.
The statement "`Y` boots the file anyway, and any other key returns to the menu" is the pinned
docs' simplification (CONFIG.md 153-154, not cited here) but contradicts the cited code line for
`y`. Proposed rewording (md + .json `statement`):
"… it prints a warning and waits: `Y` (or `y`) boots the file anyway, and any other key returns to the menu."
Also, "The value is read from the first occurrence in the file" rests on `config_get_value(NULL, 0, …)`
(menu.c:1711, cited) plus the index semantics at config.c:801-802 (`if (index--) continue;`, uncited).
Proposed Source cell: `S353 1711-1712; S351 301-312; S352 798-802`.

### F3 — LP7 / S354: anchor misses the quote's last line (support, defect in citation)
The quote "…destructively renames the result with the name of infile." spans HTML lines 189-191;
row and SOURCES S354 cite 189-190 only (line 191 = `the name of <var>infile</var>.`). Proposed:
row Source cell and SOURCES S354 anchor → "raw HTML lines 188-191 (that paragraph) and 634".

### F4 — Limits bullet 3: trunk BLAKE3 claim has no pinned source
"The trunk CONFIG.md (after v12.9.4) also accepts BLAKE3 hashes, distinguished by length
(64/128/256 hex)." No trunk snapshot was pinned this round; pinned v12.9.4 CONFIG.md contains no
blake3/64/256-hex mention (grep empty), so the second sentence ("v12.9.4 accepts only 128 hex
characters") IS sourced (uri.c 89-101) but the trunk claim is not. Proposed: either pin a trunk
CONFIG.md snapshot as a new source row (with SHA256SUMS/freeze-manifest entry), or append
"[trunk not pinned this round]" to the bullet.

### F5 — cosmetic (no action required)
- LP1 anchor ends 551; the stripping loop's closing brace is config.c:552 → cite 527-552 for exactness.
- LP2 quote drops the leading `* ` bullet of CONFIG.md:295 (consistent with corpus quote style).
- LP4 row cites S351 403-470; the non-gzip hash-as-read branch (uri.c 478-484) and the
  `gzip_open` decode point (485-486) sit just outside; SOURCES S351 anchor 403-487 covers them.
  Optional: extend the row cite to 403-489.
- LP4 statement says "as stored on the partition"; CONFIG.md:458 says "as stored on disk" — fair
  host-context paraphrase for `boot():`, noted only.

## Operator actions and Limits — claims-without-source check

- Action 1 (`--live`, rc 1, per-pin entry+consequence): verified against live-receipt.txt
  (rc=1, JSON has `entry`, `status`, `consequence` per pin). ✓
- Action 2 (Y boots main entry; snapshot entries boot without prompt): follows from LP5 grammar +
  host line 8 `no` + live receipt (`consequence: prompt` on 30/38, `none` on 50/56/64). ✓
- Action 3 (repair options; hook named only as S075, command not opened): honest; S075 is the
  limine-entry-tool README @1.40.0 ("single limine.conf output") — supports "the hook that wrote
  the pins" at README granularity; the entry itself flags the unopened hook body in Limits. ✓
- Action 4 (`find /boot … b2sum` + `cmp`, "(QUALITY 124)"): corpus/QUALITY.md:285 criterion 124
  exists ("No in-place writer touches `/boot`, and every `sudo` step leaves a `/boot` digest
  receipt (R87-BOOT-NO-INPLACE-WRITER)"); the live receipt executed exactly this recipe
  (identical before/after digest, `cmp: identical`). ✓
- Limits bullet 1 (unmodelled: macros, SB unhashed-path rule, missing-file per protocol,
  URI-shaped cmdline): matches the SCORECARD-frozen "Not certified" list. ✓
- Limits bullet 2 (enrolled config hash invisible; `--live` reads SB as enforced when the efivar
  says on — stricter reading): verified in the gate — tools/check-limine-pins.py:154-156
  `live_secure_boot()` docstring says exactly this; live receipt `"secure_boot_source": "efivar"`,
  `"secure_boot_enforced": false`. Host efivar bytes (host receipt `od`): attributes `6 0 0 0`,
  data byte 0 → off. ✓
- Limits bullet 4 (hook command not opened): honest. ✓
- Header facts: host capture timestamp 2026-11-06T19:04:43-03:00 read-only ✓; live run
  19:13:00-03:00 with identical `/boot` b2sum lists ✓; limine 12.9.4-1 ✓; snapshots
  `SHA256SUMS` ✓ (sha256sum -c rc=0); LP1/LP3 host_value cells match the host receipt
  (lower-case keys, 2- and 5-space indents; five 128-lower-hex pins) ✓; LP6 host_value
  (SecureBoot efivar byte 0) ✓; LP7 host_value (r86 ScoutHost 18:11:22, 5 PE header bytes per UKI)
  grounded in corpus/lessons/round-86.md:67 (M3) + host receipt mtimes ✓.
- Entry header "Gate in `corpus/lessons/round-87.md`": file exists; routed item 1 names QUALITY 124
  and the receipts cited. ✓
- Header claim "the lane's boot gates … none of them hashes the file a pin names": verified —
  check-boot-chain.py compares the conf line's `#hash` prefix against a stored registry
  `b2sum_prefix` (lines 321-333) and capture sha256s; check-boot-writers.py sha256s committed
  capture files (lines 234-258); neither hashes a `/boot` UKI. ✓

## SOURCES S350-S354

sha256 of all five pinned files matches SOURCES.md and the freeze manifest (rc=0; details in
sources-check.txt). Anchors cover every row citation except the S354 line-191 gap (F3). used-by
matches citing files (S350-S353 → entry + gate; S354 → entry only; gate cites S350-S353 in its
docstring). URLs in URLS.txt match the SOURCES.md URLs. ✓ except F3.

## Proposed patches (text only — L1 decides what lands)

1. `corpus/knowledge/limine-pin-plane-r87.md` LP2 Source cell and `.json` LP2 `source`:
   `S350 111-113, 134, 210, 295-308, 330-350` → `S350 111-113, 134, 210, 267-268, 272-274, 295-308, 330-350; S351 28-32`;
   `corpus/SOURCES.md` S350 anchor: add `267-268, 272-274`.
2. LP5 statement (md + json): "`Y` boots the file anyway" → "`Y` (or `y`) boots the file anyway";
   Source cell → `S353 1711-1712; S351 301-312; S352 798-802`.
3. LP7 Source cell and SOURCES S354 anchor: `raw HTML lines 189-190` → `raw HTML lines 188-191`.
4. Limits bullet 3: pin a trunk CONFIG.md snapshot (new S-row + SHA256SUMS + freeze entry) or mark
   the trunk sentence "[trunk not pinned this round]".
5. Optional cosmetics: LP1 cite 527-552; LP4 cite S351 403-489.

## Residual risk and verification gaps

- C1 (battery/gate behavior) was out of scope; I did not run `tools/limine-pin-battery-r87.py` or
  the gate — the live receipt is the L1's committed run and was used as evidence, not re-executed.
- Verbatim checks used the entry's own normalization convention (whitespace-normalized joins,
  `…` for skipped lines, tag-strip for HTML); no upstream re-fetch — pin integrity rests on
  SHA256SUMS + freeze manifest + SOURCES agreement (all consistent).
- "The hook that wrote the pins" is a README-granularity inference (S075) plus the host package
  list; the hook body was not opened (the entry says so).
- No `lsp` server was available; semantic checks are text-based reads of the pinned files.
