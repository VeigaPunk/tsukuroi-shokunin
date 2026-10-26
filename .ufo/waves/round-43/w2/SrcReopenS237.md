VERDICT: supports

# Seat SrcReopenS237 — item C2-F5 (re-open S237 live)

Date: 2026-10-26. Fleet root `/home/vgpnk/Projects/shokunin`; lane
`tsukuroi-shokunin`; scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcReopenS237/` (removed on exit).

## 1. S237 Gate quote located (lessons/round-43.md)

- `corpus/lessons/round-43.md:31` (row S237): quote `"ret = rename(datafile_old, datafile_new);"`, location
  `.ufo/waves/round-42/frozen/src/scrub.c:534`, URL `https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c`.
- Present exactly, with that text, at line 534 in the frozen snapshot and in the live file (below).

## 2. Live re-open: source identical to frozen, tag resolves

- Raw fetch `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` (2026-10-26):
  `curl -fsSL … -o live-scrub.c`; `sha256sum live-scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — the full frozen hash
  (48df2e2f…0801), byte-identical (`cmp` → identical; 2231 lines).
- Frozen snapshot `git -C … show` is not needed; `sha256sum` of
  `.ufo/waves/round-42/frozen/src/scrub.c` → same `48df2e2f…0801`.
- `git ls-remote https://github.com/kdave/btrfs-progs refs/tags/v7.1 refs/tags/v7.1^{}` →
  `0a919c7d6e389c07920675b7fad3f793b92aa78b  refs/tags/v7.1` and
  `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b  refs/tags/v7.1^{}` — peeled commit
  `4ab0e80b…` matches the SOURCES.md row's peeled-commit claim.
- Quote at `.ufo/waves/round-42/frozen/src/scrub.c:534` and live `live-scrub.c:534`:
  `	ret = rename(datafile_old, datafile_new);`.

## 3. Logged used-by change old→new (corpus/SOURCES.md)

`git diff 6951ead90566b2d74f7c45b4efca29246badad64 8acf0b022586a0f3164c77659fb96ba5f90949b6 -- corpus/SOURCES.md`:
1 file changed, 3 insertions(+), 1 deletion(-): the S237 row rewritten (only its last field) plus two new rows S240, S241.

Row lines (both revisions at line 246):

- Base `6951ead`: last field (used-by) = `corpus/knowledge/btrfs-scrub-record-r42.md`
- Tip `8acf0b`: last field (used-by) = `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`
- `diff` of the two S237 rows: change confined to the final field; all other columns identical
  (id, URL, type `code`, status `A`, description, snapshot detail incl. peeled commit and sha256,
  purpose, `mined`, date `2026-10-26`, `on-release`). Status `mined` unchanged.

This matches the lessons table `corpus/lessons/round-43.md:33-34`: "S237 `used-by` … r42.md → r42.md, r43.md (status `mined` unchanged)".

## Verdict

Supports C2-F5: the live S237 source is byte-identical to the frozen snapshot (sha256
48df2e2f…0801), tag v7.1 peels to 4ab0e80b… as logged, the Gate quote is at scrub.c:534 in both, and the
SOURCES.md S237 row changed only in `used-by`, logged old→new (r42 → r42, r43), status mined unchanged.

## Not done

No mutation of the lane, fleet root, or host; no counters run (none required for this seat). Scratch removed.
