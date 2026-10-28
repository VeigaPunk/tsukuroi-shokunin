VERDICT: supports

# C2-A4 — independent audit of every `**Quote.**` line in GR1/GR2/GR3

Item: verify all quote lines of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at freeze
`ae99f021b76f8eb1c8805d32d80644464afb1ff6` against the pinned snapshots, with my own parser;
compare counts with the frozen C2 counter (`quotes_ok` must be 3).

## Result

| Row | quotes | verified ok | bad |
|-----|--------|-------------|-----|
| GR1 | 12 | 12 | 0 |
| GR2 | 29 | 29 | 0 |
| GR3 | 12 | 12 | 0 |
| **total** | **53** | **53** | **0** |

Expected was 53 (GR1 12 / GR2 29 / GR3 12) — matched exactly. Zero malformed or
`partly`-matching quote lines; no `**Quote.**` line failed to parse under my own regex
(`audit.json` `unparsed_quoteish: []`).

Every quote is a **verbatim substring** of its snapshot line — for all 53 quotes the quoted
text is also an *exact* (whitespace-unmodified) substring, so the claim holds under a
stricter rule than the required whitespace-normalised one (`audit.json` per-quote
`exact_substring: true`, `exact_vs_norm: []`).

## Method (own parser, no counter import)

- Parser: `.ufo/waves/round-48/w2/GRevQuotes/audit.py` (written this seat, 125 lines).
  Entry + snapshots + SHA256SUMS read via `git -C <lane> show ae99f021:<path>` — the frozen
  bytes under test, not the mutable worktree.
- Section split: `## GRn` header up to the next `## ` heading (own logic; did not reuse
  `row_extent`).
- S-id → directory resolution derived independently from the entry's own header
  (`source: S246 S247 S248 S249 S242 S243 S244 S237 …`) and each round's `FETCH.txt`
  (round-44 `FETCH.txt` maps `scrub.c -> S242`, `sysfs.c -> S243`, `btrfs-scrub@.* + PKGBUILD
  -> S244`; round-43 `FETCH.txt` states `scrub.c (S237)` is the round-42 snapshot). The
  double registration of `scrub.c` (S237 = round-42, S242 = round-44) is handled by
  resolving `(sid, file)` pairs, not file alone.
- Each resolved snapshot file's sha256 recomputed and compared with its own `SHA256SUMS`
  (parsed from the same revision). All 9 touched files digest-verified:

  - `.ufo/waves/round-42/frozen/src/scrub.c` — sha256 `48df2e2f…8f0801` ok (S237)
  - `.ufo/waves/round-43/frozen/src/ioctl.c` — not cited by any quote line (S240 unused in quotes)
  - `.ufo/waves/round-44/frozen/src/scrub.c` — sha256 `f347931b…5ca5b8` ok (S242)
  - `.ufo/waves/round-44/frozen/src/sysfs.c` — sha256 `ce146120…f731c43` ok (S243)
  - `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service` — sha256 `eaa7af92…240252` ok (S244)
  - `.ufo/waves/round-45/frozen/src/cmdline.c` — sha256 `1af5ad98…46ca9d` ok (S246)
  - `.ufo/waves/round-45/frozen/src/vsprintf.c` — sha256 `cabb648a…93469ca` ok (S246)
  - `.ufo/waves/round-45/frozen/src/kstrtox.c` — sha256 `0c52ae02…db8d1ee4` ok (S246)
  - `.ufo/waves/round-45/frozen/src/dev-replace.c` — sha256 `f07ef0a0…034f3a` ok (S247)
  - `.ufo/waves/round-45/frozen/src/systemd.kill.xml` — sha256 `44832283…f965f9b` ok (S248)

- Comparison rule: `norm(quote) in norm(snapshot_line)` with `norm = whitespace-collapse`;
  line number bounds-checked (1 ≤ n ≤ file lines). Full per-quote records in
  `.ufo/waves/round-48/w2/GRevQuotes/audit.json` (`all` arrays carry `src_line_text`).

## Spot check by eye (six lines read directly from `git show`)

- `round-42/src/scrub.c:421` → `	ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` — quote line 181 matches.
- `round-45/src/cmdline.c:147` → ` *	potentially suffixed with K, M, G, T, P, E.` — quote line 27 matches.
- `round-45/src/systemd.kill.xml:68` → `<para>If set to <option>control-group</option>, all remaining processes in the control group of this` — quote line 167 matches.
- `round-45/src/dev-replace.c:700` → `	/* the disk copy procedure reuses the scrub code */` — quote line 81 matches.
- `round-44/src/btrfs-scrub@.service:9` → `KillSignal=SIGINT` — quote line 163 matches.
- `round-44/src/sysfs.c:2040` → `	limit = memparse(buf, &endptr);` — quote line 47 matches.

## Comparison with the frozen counter

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r48.py --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6`
(receipt: `.ufo/waves/round-48/w2/GRevQuotes/counter.json`):

- `quotes_ok: 3` — required value, matched.
- Per-row `quotes`: GR1 `{quotes: 12, ok: 12, bad: []}`, GR2 `{quotes: 29, ok: 29, bad: []}`,
  GR3 `{quotes: 12, ok: 12, bad: []}` — identical to my independent counts.
- For context (outside this item's scope): counter's overall `verdict: FAIL` at this rev is
  expected mid-wave — `structural_ok: 1`, `verdicts_ok: 0`, `marks_ok: 0` (counted verdicts
  and admission marks are pending by design until seats write reports and the L1 integrates).

## Reservations

- None on the quote leg itself. My parser and the counter agree to the line; every digest
  pinned; snapshot files are tracked blobs at the freeze revision (`git ls-tree` shows all
  four `frozen/src` dirs at ae99f021; `git status` on those dirs is clean).
- Scope note: this audit covers the `**Quote.**` leg only (C2-A4). The `[inference]` marks,
  citation-bound checks, and verdict legs are other seats' items.

## Receipts

- `.ufo/waves/round-48/w2/GRevQuotes/audit.py` — the parser I wrote and ran.
- `.ufo/waves/round-48/w2/GRevQuotes/audit.json` — full per-quote results (doc line, sid,
  file, src line, digest status, result, source line text).
- `.ufo/waves/round-48/w2/GRevQuotes/counter.json` — frozen counter output at the freeze rev.
