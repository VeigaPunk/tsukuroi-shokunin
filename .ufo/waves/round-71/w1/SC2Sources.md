# SC2Sources — C1 registry rows S297–S300 and Gate record

Seat SC2Sources, tsukuroi lane round 71 (hyaku run 15), wave w1. Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e` (the
declaration commit; `git rev-parse HEAD` re-read 2026-11-04). Read-only on the lane: the four rows are a
draft for the L1 to append, and nothing was staged, committed or pushed.

## Behavior

Registered the four sources the round-71 declaration planned for C1's depth claim, at the tag the
snapshots were committed under.

- **S297** `kernel/params.c` (code, A) — the parameters attribute exists only for a nonzero `perm`
  (`BUG_ON(!kp->perm)` at 634), its mode is `kp->perm` (675), a store handler is attached only when a
  write bit is set (669-673), and show/store return `-EPERM` when `ops->get`/`ops->set` is NULL
  (569-570, 586-587).
- **S298** `include/linux/moduleparam.h` (code, A) — `kernel_param_ops` set/get return conventions
  (60-69), `struct kernel_param` with `const u16 perm` (82-94), and the documented `@perm` values 0,
  0444, 0644 (118-127).
- **S299** `kernel/module/main.c` (code, A) — `unknown_module_param_cb` warns that an unknown parameter
  is ignored and returns 0 unconditionally (3378-3395); `blacklisted()` returns `-EPERM` at the load
  gate (3406-3408); `module_blacklist` is a comma list declared `core_param(..., 0400)` (2934-2953).
- **S300** `Documentation/admin-guide/kernel-parameters.rst` (docs, A) — the two specification routes
  with both syntaxes (20-24), built-ins restricted to the kernel command line and modprobe reading it
  (26-30), and the `/sys/module/<name>/parameters/` exposure with its runtime-write note (32-37).

Each `source` cell carries that snapshot's exact `SOURCES.json` URL and each `anchor` cell names the tag
`v7.2.11`, the snapshot basename, the line ranges and the raw-bytes sha256 — the two bindings
`tools/count-mp-rows-r71.py` tests (`url in source`, `snapshot basename in anchor`). Verified with the
counter's own `SROW_RE` and `line.split('|')` cell indices: 4/4 `url-bound=ok basename-bound=ok`.

## Gates

- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-71/before/src` → 4 OK, rc 0, and each digest equals
  the `SOURCES.json` map digest (recomputed in-session).
- Row shape: NF **13** (11 cells) and **12** pipe delimiters on all four rows → no pipe inside a cell.
- Fields: kind code/code/code/docs, tier A, status `mined`, opened `2026-11-04`, recheck `on-release`,
  used-by `corpus/knowledge/module-parameter-plane-r71.md`.
- `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` (validator sha256
  `3fb72615…a64e30`): run A without the note → rc **1**, exactly 4 `E11` naming the declared note path;
  run B with a 0-byte placeholder at that path → rc **0**, 0 E, 46 W (all pre-existing `W04`, none for
  S297-S300). Full transcripts in `census.txt`.
- Gate quotes: one per row, 12 / 10 / 7 / 18 words, no pipe, each located verbatim (whitespace-
  normalized) inside its declared 1-based span; eleven supporting locators re-located the same way.

## Touched surfaces

- `.ufo/waves/round-71/w1/SC2Sources/{rows.md,gate.md,census.txt}` — written by this seat.
- `.ufo/waves/round-71/w1/SC2Sources.md` — this report.
- Scratch `/fast/scratch/hyaku/tsukuroi-r71/SC2Sources` (lane corpus/tools/SKILL.md copies + the mirror
  registry) — created, then deleted before yield.
- Nothing else: no lane edit, no `.ufo/state`, no `MANIFEST.json`, no sibling lane, no fleet-root
  tracked file, no git mutation, no pacman transaction, no host write.

## Findings

1. **The C1 note is not on disk.** `corpus/knowledge/module-parameter-plane-r71.md` was absent at
   2026-11-04 00:55Z (`ls` → No such file or directory). The four rows' `used-by` therefore raises
   `E11` until that note lands; the L1 who appends these rows before the note exists will see four
   E11 lines, not a clean registry.
2. **Unknown-parameter handling is two different arms, and C1's wording rides one of them.**
   `main.c:3393` warns `unknown parameter ... ignored` and `unknown_module_param_cb` returns 0, so a
   mistyped *module-load* parameter does not fail the load. On the kernel-command-line path the same
   miss hits `params.c:196` (`pr_err` "Unknown parameter") and `parse_args` returns an `ERR_PTR` at
   `params.c:208`. The MP row that states "an unknown parameter is warned and ignored, so a typo does
   not fail the load" is grounded by S299 only if it stays scoped to the module-load arm; S297 alone
   would not carry it.
3. **`perm` is the whole writability story.** `params.c:669-675` says it outright: the store handler is
   attached only when a write bit is present "so runtime DAC changes cannot make param writable", and
   `mattr.attr.mode = kp->perm`. That is the mechanism behind the host's read-only `nvidia_drm` and
   `nvidia` parameters and the root-writable `nvidia_uvm` ones; the rows record the mechanism, not the
   host reading (which belongs to the host capture).
4. **No URL collision.** None of the four URLs duplicates an existing row's URL, so the rows add no
   `W04` and no `E04`; the registry's 46 `W04` warnings are unchanged by this seat.
5. **Uncommitted lane changes observed, not mine.** `git status --porcelain` at 22:00Z showed
   `M tools/count-xs-rows-r70.py` (the round's D3 shebang repair) and at 22:01Z also
   `M tools/tsukuroi-census.sh` (the C2 arm, being edited concurrently). This seat touched neither; it is
   noted only because this seat's census mirror copied `tools/` from the lane while those edits were in
   flight. Live-seat concurrency on those two files is expected, and the lane tree is the L1's to
   commit.

## Limits

- The four rows are a draft. Ids S297-S300 are the declaration's planned ids and `S296` is the last id
  in the lane at `0fcfca3`, so an append after `S296` keeps E03 (duplicate id) quiet.
- Run B's rc 0 depends on a 0-byte placeholder in the scratch mirror; it is not evidence that the note
  exists. Only the note seat's file makes `used-by` true in the lane.
- Quotes come from the committed snapshots. No network fetch was made this round, and no claim is made
  that the URLs still serve these bytes today.
- No tool was installed or upgraded.
