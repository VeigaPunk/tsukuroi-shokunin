# RevSrcS144 — falsify wave 2, attempt 2

Verdict: holds. Every checkable cell of the S144 registry row and its single Gate quote agrees with a fresh independent fetch of the source; two minor [obs] residuals noted.

## Setup

`curl -fsS https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/signing.c -o /fast/scratch/hyaku/tsuku27a2/RevSrcS144/signing.c` exited 0; the file is 3137 bytes and 125 lines, sha256 `96c807347e4e60bbb39d91b7ad611279b75aab2d23b967459eaaa7c56a796735`.

Note on revision: the lane worktree HEAD is `2e519d615135ba3b3d60dcd19a5642dc0d4391f9` (round-27 attempt-2 start), one commit after the attack revision `099c7b3f42d073203d9448807860f04c175eccd7`. `git diff --stat 099c7b3f..HEAD` on `corpus/SOURCES.md`, `corpus/lessons/round-27.md`, `.ufo/waves/round-27/sources/S144.c`, `corpus/knowledge/kernel-taint-r27.md` and `corpus/knowledge/kernel-taint-r27.json` is empty, so every audited byte is the attack revision's byte.

## Findings (agree or disagree per item)

1. Anchor-cell sha256 versus fresh fetch: AGREE. `corpus/SOURCES.md:150` anchor cell states `raw bytes sha256 96c807347e4e60bbb39d91b7ad611279b75aab2d23b967459eaaa7c56a796735`; `sha256sum /fast/scratch/hyaku/tsuku27a2/RevSrcS144/signing.c` prints the identical digest.
2. Anchor-cell sha256 versus committed snapshot: AGREE. `sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/sources/S144.c` prints `96c807347e4e60bbb39d91b7ad611279b75aab2d23b967459eaaa7c56a796735`, and `cmp` against the fresh fetch reports IDENTICAL. The anchor's `snapshot .ufo/waves/round-27/sources/S144.c (125 lines)` also matches: both files are 125 lines.
3. Gate quote for S144 (the only one in `corpus/lessons/round-27.md`; grep counts exactly one `S144` mention in that file): AGREE on all three axes.
   - Exact text: `corpus/lessons/round-27.md:22` quotes `` `reason = "module with unavailable key";` ``; `/fast/scratch/hyaku/tsuku27a2/RevSrcS144/signing.c:107` reads `\t\treason = "module with unavailable key";`. Quote cell equals the source line modulo leading indentation, consistent with the Gate preamble's whitespace-normalised-substring rule (round-27.md:7-9).
   - Word count: 6 words (`reason`, `=`, `"module`, `with`, `unavailable`, `key";`), within the at-most-25-words cap.
   - Stated line: location cell says `kernel/module/signing.c line 107`; grep shows the string's only occurrence at line 107, so the line is correct both as stated and under the Gate's "first line of the match" convention. URL cell (`raw.githubusercontent.com/torvalds/linux/v7.2/kernel/module/signing.c`) is the exact URL I fetched.
4. Scope cell (QUALITY 66): AGREE. `SOURCES.md:150` scope is "Module signature verification outcomes and the permissive versus enforcing decision, for the host kernel 7.2.11". The file delivers exactly that: `mod_verify_sig` performs the signature verification (lines 41-62), `module_sig_check` maps outcomes to accept/reject/lockdown (lines 65-125), and `sig_enforce` plus `is_module_sig_enforced` implement the permissive-versus-enforcing decision (lines 20-31). Pinning to tag v7.2 for a 7.2.11 host is the documented convention used by the whole block (S140-S145).
5. Teaches cell (QUALITY 66): AGREE with reservation. Each clause is supported by the source:
   - "verified against the kernel's built-in and secondary trusted keyrings" — line 56-60 calls `verify_pkcs7_signature(..., VERIFY_USE_SECONDARY_KEYRING, VERIFYING_MODULE_SIGNATURE, NULL, NULL)`; `VERIFY_USE_SECONDARY_KEYRING` is the request to fall back to the secondary trusted keyring beyond the built-in. [inf] The built-in keyring is the default base for that helper; the line itself names only the secondary flag.
   - "an unsigned module, unsupported crypto or an unavailable key is rejected when sig_enforce is set" — lines 103-114: `-ENODATA`/`-ENOPKG`/`-ENOKEY` set the three reasons, then `is_module_sig_enforced()` returns `-EKEYREJECTED`.
   - "otherwise passes to the lockdown check" — line 124 `return security_locked_down(LOCKDOWN_MODULE_SIGNATURE);`.
   - "other verification errors are fatal even when signatures are not required" — lines 110-113 `default:` returns the raw error; the comment says "All other errors are fatal ... even if signatures aren't required."
   - No forbidden 'only'/'otherwise'/'exactly' qualifier overstates a branch.
   - Reservation [obs]: under a strict "keep every branch" reading, the teaches cell omits two branches — the success path (`sig_ok` set, return 0, lines 78-82) and the mangled-module path (MODULE_INIT_IGNORE_MODVERSIONS/VERMAGIC flags make `mangled_module` true so the signature is refused, lines 71-82). Nothing taught is wrong; the cell is a partial enumeration. I do not count this as a defect because the registry's teaches column is a summary cell (peers S140/S141 teach subsets too), but the L1 may choose to append the two branches.

## Additional observations

6. [obs] The wave-1 scribe spec required "two to four Gate rows" per source (`.ufo/waves/round-27/w2a2-dispatch.json`, SrcModuleSigning entry, and `w1-spec.json:28-30`); S144 landed one. The single row meets every Gate validity rule; the count shortfall is a process deviation, not a content defect, and KT3's needs are still met.
7. [obs] Anchor cell names only line 107. Per the Gate convention (the cited line is the quote's first line) this is internally consistent, though an anchor naming the `module_sig_check` range would be more descriptive.
8. [obs] `used-by` pointer is accurate: `corpus/knowledge/kernel-taint-r27.json:96-111` lists S144 among KT3's sources and embeds the same quote text and `kernel/module/signing.c line 107` location; `kernel-taint-r27.md:3` lists S144 in the source front-matter.

## Residual risk and verification gaps

- [unk] I verified the quote text against the fresh fetch and the snapshot (byte-identical), but I did not re-run the L1's `build_c1.py` substring checker; not needed since bytes and substring are directly confirmed.
- [unk] Teaches clause "built-in and secondary trusted keyrings" rests on the semantics of `VERIFY_USE_SECONDARY_KEYRING`; the signing.c file itself does not enumerate keyring names. The clause is consistent with `Documentation/admin-guide/module-signing.rst` (S145, not in my scope to re-verify).
- No other residual risk found in scope: hash, snapshot, quote, line, scope and teaches cells all agree.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (S144 row, header, registry), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-27.md (Gate rows 1-30), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kernel-taint-r27.{json,md} (S144 references), .ufo/waves/round-27/sources/S144.c (hash only), /fast/scratch/hyaku/tsuku27a2/RevSrcS144/signing.c (full); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevSrcS144.md, /fast/scratch/hyaku/tsuku27a2/RevSrcS144/signing.c; executed=curl fetch, sha256sum, cmp, wc, grep -c, git rev-parse/log/diff/merge-base/cat-file (all read-only)
Model: not exposed
Installs: none
