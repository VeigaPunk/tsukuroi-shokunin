VERDICT: supports

EX6 ("NeedsTargets targets arrive sorted with `strcmp`, duplicates from several triggers removed, one target per line") reproduced from the pinned sources in a C harness: every non-empty match set produced a strictly `strcmp`-ascending, duplicate-free, newline-terminated byte stream, and the partial-write branch that splits a target across two buffer fills does not lose the newline — the final stream still ends in `\n`, with the terminator of a split tail delivered as its own separate write.

## 1. Method and provenance

Extraction (verbatim, no edits): `.ufo/waves/round-40/frozen/src/hook.c:469-490` (`_alpm_hook_feed_targets`) and `:492-505` (`_alpm_strlist_dedup`), copied 1:1 into the harness and re-checked by diff before every build:

```
$ L=$(grep -n '^static ssize_t _alpm_hook_feed_targets' harness.c | cut -d: -f1); echo $L
125
$ sed -n "${L},$((L+36))p" harness.c | diff - <(sed -n '469,505p' \
    .ufo/waves/round-40/frozen/src/hook.c) && echo VERBATIM-OK
VERBATIM-OK
```

Pinned-source integrity first (Bash, cwd `.ufo/waves/round-40/frozen/src`): `sha256sum -c SHA256SUMS` → all 6 `OK`, `hook.c` = `99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a`, matching `FETCH.txt`'s pacman `54d9411` pin.

Stand-ins (assignment): `alpm_list_t` = `{next, prev, data}` with the real `head->prev == tail` invariant; `alpm_list_remove_item` copied verbatim from upstream `lib/libalpm/alpm_list.c@54d9411` (fetched 2026-10-26, sha256 `3bb690c42eaef06e6bd2d512aadb47a61e14ab231a802d0abadb89285ece0ba3`; note it unlinking *without* freeing is exactly why the verbatim dedup's trailing `free(next)` is legal); `alpm_list_msort` replaced by `qsort` over the node data pointers with a `strcmp` wrapper, per assignment, then written back into the existing nodes.

Driver fidelity: the callback is invoked only when the buffer is empty and its whole return value is written, which is what `_alpm_chroot_write_to_child` does (`util.c:490-517`, `out_cb(buf, buf_limit, cb_ctx)` at `:498`); a partial `send()` there only `memmove`s the leftover, so the recorded chunk sequence is exactly the byte stream on the child's stdin pipe.

Buffer sizes: 16 and 4096 as instructed, plus the production size. The real stdin buffer is `char ibuf[LINE_MAX]` (`util.c:706`) passed as `sizeof(ibuf)` (`util.c:741`); on this host (`gcc -E -dM`, `getconf LINE_MAX`) `LINE_MAX = 2048`, `PIPE_BUF = 4096`.

Build: `gcc -std=c11 -Wall -Wextra -O1 -o harness harness.c`, rc=0, no warnings (gcc 16.2.1). Sanitizer build (`-fsanitize=address,undefined`, `ASAN_OPTIONS=detect_leaks=0`) over the same tests: rc=0, zero ASAN/UBSAN reports — the dedup `free()` path and both feed branches are clean.

Receipts: `.ufo/waves/round-40/w1/C2ExecFeedTargets/{harness.c (sha256 4165edca…), run.txt (f95ab21a…), extracted.txt (2688b01a…), upstream-alpm_list_remove_item.c.txt, BUILD.txt}`.

## 2. Bytes produced

Input fixture (8 matches = unsorted, with duplicates from three triggers): `usr/lib/firmware/b, etc/pacman.conf, usr/lib/firmware/b, usr/bin/pacman, etc/pacman.conf, usr/share/doc/x, etc/pacman.conf, usr/bin/pacman-db-upgrade`.

Sort+dedup alone (T0, no feed): `["etc/pacman.conf", "usr/bin/pacman", "usr/bin/pacman-db-upgrade", "usr/lib/firmware/b", "usr/share/doc/x"]`, `head->prev==tail=yes`.

T1, 4096-byte buffer, one callback returns everything (`*pos` becomes NULL, next call n=0 closes the pipe):

```
STREAM(92 bytes)="etc/pacman.conf\nusr/bin/pacman\nusr/bin/pacman-db-upgrade\nusr/lib/firmware/b\nusr/share/doc/x\n"
checks: bytes=92 lines=5 sorted=yes dedup=yes last_byte_newline=yes trailing_garbage=0
```

T2, same list through a 16-byte buffer — six callbacks, identical bytes:

```
call 0: n=16 "etc/pacman.conf\n"        ends_with_newline=yes
call 1: n=16 "usr/bin/pacman\nu"        ends_with_newline=NO   <- partial branch (:483-487)
call 2: n=16 "sr/bin/pacman-db"         ends_with_newline=NO
call 3: n=16 "-upgrade\nusr/lib"        ends_with_newline=NO
call 4: n=16 "/firmware/b\nusr/"        ends_with_newline=NO
call 5: n=12 "share/doc/x\n"            ends_with_newline=yes
call 6: n=0  loop ends, pipe closed
STREAM(92 bytes)="etc/pacman.conf\nusr/bin/pacman\nusr/bin/pacman-db-upgrade\nusr/lib/firmware/b\nusr/share/doc/x\n"
checks: bytes=92 lines=5 sorted=yes dedup=yes last_byte_newline=yes trailing_garbage=0
T6 stream equality across buffers: IDENTICAL (4096 n=92 calls=1, 16 n=92 calls=6)
```

T8 with the production buffer (`LINE_MAX=2048`), 80 matches collapsing to 60 unique (3060 target bytes): the partial branch fires at the first boundary — `call 0: n=2048` ends 8 bytes into a target, at `"…pkg04/module25.py\nusr/lib/"`, without a newline; `call 1: n=1012` resumes `"python3.13/site-packages/pkg04/module32.py\n…"`. Stream: `bytes=3060 lines=60 sorted=yes dedup=yes last_byte_newline=yes trailing_garbage=0`. In total `run.txt` records 15 non-newline-terminated write chunks, all of which reassemble into terminated lines.

T9 (ordering semantics): input `etc/Z, etc/a, usr/bin/foo, usr/bin/foo-bar, etc/a, usr/bin/Foo` → `"etc/Z\netc/a\nusr/bin/Foo\nusr/bin/foo\nusr/bin/foo-bar\n"` (52 bytes, 5 lines): bytewise `strcmp`, not locale collation (uppercase before lowercase); a prefix (`usr/bin/foo`) and its extension (`usr/bin/foo-bar`) stay distinct, only exact duplicates collapse.

## 3. The partial-write branch, and the last target

`hook.c:483-487` (the item's `:479-483` is four lines low — verified with `grep -n 'if\(\*pos && remaining\)'`: 483 `if(*pos && remaining) {`, 484 `memcpy`, 485 `(*pos)->data = … + remaining`, 486 `written += remaining`, 487 `}`):

- A target straddling a buffer boundary is emitted in pieces and the piece that ends the fill carries **no** newline (T2 call1 `"usr/bin/pacman\nu"`, T3 call4 `"ngtargetname.txt"`, T4 call0 `"0123456789abcdef"`, T8 call0).
- The newline is not lost: the node's `data` pointer was advanced by `remaining` (`:485`), so the next callback writes the tail and then `'\n'`.
- Consequence for the *last* target: when the tail consumes the remaining buffer exactly, the final newline arrives as a **separate one-byte write** and is still the last byte of the stream. T3 (`etc/pacman.conf`, `usr/bin/pacman`, `usr/share/doc/pacman/hooks/verylongtargetname.txt`; 16-byte buffer): calls `n=16,16,16,16,16` then `call 5: n=1 chunk="\n"`, stream 81 bytes = `"etc/pacman.conf\nusr/bin/pacman\nusr/share/doc/pacman/hooks/verylongtargetname.txt\n"`, `lines=3 last_byte_newline=yes`. T4: single 16-char target in a 16-byte buffer → `call 0 n=16 "0123456789abcdef"` (no newline), `call 1 n=1 "\n"`, total 17 bytes, terminated. T7: 20-char target → `call 0 n=16`, `call 1 n=5 "ghij\n"`, 21 bytes, terminated.
- So the answer to the explicit question is: **the chunk** written by a partial write is not newline-terminated, but **the stdin byte stream always is**, provided the callback is called again after the buffer drains — which `_alpm_chroot_write_to_child` does whenever `*buf_size` reaches 0 (`util.c:496-498`; a partial `send()` at `:504` only `memmove`s the leftover at `:509` and never re-calls the callback, so the byte stream is unchanged). Only a 0-byte stream (no matches, T5: `n=0` immediately, 0 bytes) has no terminator, and that path never runs a hook with `NeedsTargets`: a hook is added to `hooks_triggered` only when `_alpm_hook_triggered` reports a non-empty match set (`hook.c:667-669`; its return value requires one of install/upgrade/remove to be non-empty, `hook.c:338-341`).

## 4. Side observation (not a defect)

The partial branch writes through the list node: `(*pos)->data = (char *) (*pos)->data + remaining` (`hook.c:485`). The list is therefore single-use. T7: after a 16-byte partial write the node's data is `"ghij"` instead of `"0123456789abcdefghij"` (advanced 16 bytes), and re-feeding the same head yields `"ghij\n"` (5 bytes) instead of 21. This is harmless in libalpm because the pointers are borrowed package file-list names (`filelist.files[f].name`, `hook.c:275`, `:290`, `:304`), the match list is freed node-only (`alpm_list_free(hook->matches)`, `hook.c:81` — the verbatim dedup frees the removed node itself at `:499`), and hook structs are parsed and freed inside each `_alpm_hook_run` (`hook.c:579-620` re-parse, `:679` free). No invalid free, no cross-run corruption observed; the ASAN/UBSAN run is clean. [INFERENCE] on the "no cross-run corruption" part rests on the borrow/free-path reads cited here, not on a live pacman run (none is permitted).

## 5. Two corrections for the C2 text (C2-26 is empirical, so no draft cell is proposed)

1. **Line numbers.** Split branch is `hook.c:483-487`, not `:479-483`. The feed function is `:469-490`, the newline is added at `:476`, dedup is `:492-505`, and the ordering of operations (msort, then dedup, then `_alpm_run_chroot` with `(_alpm_cb_io) _alpm_hook_feed_targets`) is `hook.c:521-526`.
2. **Doc attribution.** EX6's doc column cites `alpm-hooks.5.asciidoc:91-93`, but those lines say only: "Causes the list of matched trigger targets to be passed to the running hook on 'stdin'." The man page documents the *channel*, not the format: `grep -n "NeedsTargets\|sorted\|one per line\|stdin"` over the pinned page yields only lines 24, 91, 93, with no `sorted` and no "one per line". Sortedness, de-duplication and newline framing are source-derived (`hook.c:469-505`, `:521-526`) and now empirically confirmed; the citation should be split accordingly rather than implying the man page specifies the format.

## 6. What I did not do

- No live pacman/hook invocation (not permitted); behaviour is from the pinned source compiled locally.
- `alpm_list_msort` itself was not exercised (replaced by `qsort`+`strcmp` per assignment); the sort order result is therefore only as good as `strcmp`-equivalence, which is the comparator libalpm passes.
- No test of target names containing `\n` bytes (would make "one target per line" ambiguous); not tested because package file lists cannot carry such names — [INFERENCE], not verified here.
- No tool installs or upgrades; nothing outside the seat report, receipts dir and `/fast/scratch/hyaku/tsukuroi-r40/C2ExecFeedTargets/` was written, and that scratch dir was removed at the end.
