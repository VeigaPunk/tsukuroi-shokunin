# Scribe S155 — btrfs-progs v7.1 Documentation/mkfs.btrfs.rst (D04 metadata DUP)

Verdict: done — the source was opened this round at tag v7.1 (HTTP 200), saved byte-identical with sha256 `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`, and the seat delivers an 11-cell registry row, one Gate row, and four D04 candidate counter rows that pass the live counter's own R2/R3/R6/R7 checks.

## Findings

1. Source fetched with `curl -sL` from `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst`; raw.githubusercontent.com answered HTTP 200, no fallback needed. Saved bytes: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs/S155-mkfs.btrfs.rst`, 29867 bytes, 723 lines, `sha256 ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769` (`sha256sum`, exit 0). [obs]

2. Tag provenance, read from the cgit tag view `https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/tag/?h=v7.1` (HTTP 200): `tag name v7.1 (0a919c7d6e389c07920675b7fad3f793b92aa78b)`, `tag date 2026-07-15 00:41:55 +0200`, `tagged object commit 4ab0e80be9...` — the peeled commit `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` is the same pin S129 already records, so the snapshot is the tree of that tag. Page copy: `/tmp/s155-tag.html` (ephemeral). [obs]

3. What the snapshot establishes, by line (1-based, verified by `sed -n`):
   - line 21: the default block-group profiles for data and metadata depend on the device count;
   - lines 54-77: the `-m|--metadata` option; line 59 `Default on a single device filesystem is *DUP* and is recommended for metadata`; lines 65-69 the pre-5.15 rotational-device detection that used to select *single*, `changed in version 5.15 to be always *dup*`;
   - lines 508-534: the PROFILES table; header line 514 (Profiles | Redundancy Copies/Parity/Striping | Space utilization | Min/max devices), line 520 `| DUP      |  2 / 1 device |            |            |  50%              | 1/any (see note 1) |`;
   - lines 542-543: Note 1 — DUP may exist on more than one device if it starts on one device and another is added; since 4.5.1 mkfs.btrfs creates DUP on multiple devices;
   - lines 630-666: section DUP PROFILES ON A SINGLE DEVICE, ending at line 666 `should be replaced! **DUP is not backup**.` [obs]

4. The ch-profiles question: there is **no** `ch-profiles.rst` (or any file with `profile` in its name) in `Documentation/` at tag v7.1. The cgit tree view `https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/tree/Documentation?h=v7.1` (HTTP 200) lists 99 entries; `grep -i rofile` on the extracted 99-line list exits 1 (no match). The list is saved as `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs/S155-doc-listing.txt`. The DUP space ratio is therefore stated by the PROFILES table inside mkfs.btrfs.rst itself, and that line is line 520 quoted in finding 3 (redundancy `2 / 1 device`, space utilization `50%`). [obs]

5. Seat deliverables (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs/`):
   - `S155-row.md` (sha256 `55b5d1e32bf48545500c139585fb6454c4b816e16d8867838b5fd4debc2fd832`): one registry line, 11 cells by the counter's own `split_cells` (id, source, kind `docs`, tier `A`, scope, anchor, teaches, status `mined`, opened `2026-10-22`, recheck `on-release`, used-by `corpus/knowledge/btrfs-space-r30.json, corpus/knowledge/btrfs-space-r30.md, SKILL.md, corpus/lessons/round-30.md`). The anchor cell contains the literal `sha256 ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`, so R4's hash test passes once the row is integrated. No cell contains an unescaped pipe.
   - `S155-gate.md` (sha256 `adea5efb5910d7c6e5cdfcbf51c63493dbe20cdcad9ef7ab9822210377c90841`): header row plus one Gate row; quote `Default on a single device filesystem is *DUP* and is recommended for metadata` (13 words, verdict cell also names the line-520 ratio).
   - `S155-rows.json` (sha256 `1c36aed2b2dbc062dbbb03af9b8f89a32f9fd8bf95fc49d42e95efd03e6439c0`): four candidate D04 rows, all `"source": "S155"` and `"snapshot": ".ufo/waves/round-30/w1/ScribeSrcMkfs/S155-mkfs.btrfs.rst"`, in this order:
     1. line 520 (primary): 38-word statement; quote is the full DUP table row (53 chars after normalisation), so the row itself states both `2 / 1 device` and `50%`;
     2. line 59: 33-word statement, default DUP on a single-device filesystem;
     3. line 69: 29-word statement, always DUP since 5.15 regardless of the rotational flag;
     4. line 543: 32-word statement, DUP not restricted to one device (note 1, mkfs.btrfs since 4.5.1).

6. Quote verification, run exactly as `sed -n '<N>p' <file> | grep -cF '<quote>'` in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs/` with `F=S155-mkfs.btrfs.rst`; each printed `1`:
```
sed -n '520p' $F | grep -cF '| DUP      |  2 / 1 device |            |            |  50%              | 1/any (see note 1) |'
1
sed -n '59p' $F | grep -cF 'Default on a single device filesystem is *DUP* and is recommended for metadata'
1
sed -n '69p' $F | grep -cF 'changed in version 5.15 to be always *dup*.'
1
sed -n '543p' $F | grep -cF 'another one is added. Since version 4.5.1, :command:`mkfs.btrfs` will let you create DUP'
1
```
   The same strings were produced programmatically from the saved lines (so no whitespace drift), and the quotes are stored in the JSON in exactly those bytes.

7. Counter-rule simulation against the live checker (imported `tools/check-btrfs-space-r30.py` as a module and reusing its `SOURCE_KEYS`, `strip_markup`, `norm` and D04 token tuple): for all four rows `set(keys)==SOURCE_KEYS` is true, statement word counts are 38/33/29/32 (R3, and the task's 15-40 range), normalised quote lengths are 53/78/43/88 chars (R6 minimum 20), the quote is found in the three-line window starting at the cited line, and for R6's position test `window.find(q)` returned `0` with `len(first)` 53/78/43/88, i.e. `pos < len(first)` for every row. R7 holds because each quote contains `dup` (case-insensitive) — line 59 as `*DUP*`, line 69 as `*dup*`. [obs]

8. [inf] The primary statement's clause "metadata uses the DUP profile by default" is grounded at line 59 of the same snapshot, while its quote anchors line 520 (the ratio). The two are the same file and the pair was verified as a unit; if the L1 prefers every clause inside the quoted line, candidate 2 (line 59) is the substitute — the counter accepts either.

9. S155 is absent at the round-30 base `fbfec6bdf8833e7513732a06000801a8ee9b690b`: `git show fbfec6bd:corpus/SOURCES.md | grep -c '^| S155 |'` printed `0` (read-only `git show`, no writes). It is also absent from the current registry (`grep -c '^| S155 |' corpus/SOURCES.md` → `0`), so no id collision. [obs]

10. The snapshot is upstream RST, not host state: it describes defaults and semantics only. [unk] It does not say what this host's metadata profile actually is; that is D08's read-only sysfs capture, outside this seat.

## Limits
- No counter row was installed into `corpus/knowledge/btrfs-space-r30.json` and no registry row into `corpus/SOURCES.md`; integration is the L1's.
- Candidate 1's quote is an RST table line containing pipes; it is safe in JSON, but a Markdown cell copy of that quote needs `\|` escaping (the Gate row avoids it by quoting line 59).
- The GitHub refs API was rate-limited (HTTP 403), so the tag pin comes from the kernel.org cgit tag page instead.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md, corpus/lessons/round-29.md, tools/check-btrfs-space-r30.py, .ufo/waves/round-30/measure/c1-before-8fb2cef081787ccb52b38e9f74d95d2a480de18f.jsonl, the sibling drafts .ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-{row,gate,rows}, the fetched mkfs.btrfs.rst and cgit tag/tree pages; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs/{S155-mkfs.btrfs.rst,S155-row.md,S155-gate.md,S155-rows.json,S155-doc-listing.txt}, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcMkfs.md, /tmp/s155-tree.html, /tmp/s155-tag.html; executed=curl -sL (raw.githubusercontent.com HTTP 200; cgit tree and tag HTTP 200; api.github.com HTTP 403 rate limit), sha256sum, wc, sed, grep -cF, python3 (quote generation and counter-rule simulation), env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show (read-only)
Model: opencode-go/deepseek-v4.1-flash (as exposed in the session project context)
Installs: none
