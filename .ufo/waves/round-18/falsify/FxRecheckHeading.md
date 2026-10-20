# FxRecheckHeading — R18 recheck resolution

**FAILS — actionable gate bypass.** **SURVIVES (narrowly):** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-recheck-commands.py:59-60,447-464` accepts both R17/R18 headings and makes R18 operative; selftest source `:1188-1212` covers normal safe/unsafe R18 literal and pointer cases. No tests were executed.

**FAILS:** `:302-309` puts any nonempty backtick span in `state["commands"]`; `:209-234,237-243` can yield no command for an empty argv0 or wrapper-only span. Then `:489-518` validates only that the command list is nonempty and has no detected forbidden invocation, setting `resolved=True`; `:519-536` consequently skips findings for the last recheck header and its pointer hits. Example (static inference, unexecuted): an R18 section declares `- `''`` while the last `recheck:` points to a §7 containing a forbidden command. `''` is a nonempty span but tokenizes to an empty command name, so the replacement can suppress the old pointer finding without supplying a command. Wrapper-only `sudo` has the same no-argv0 path. Existing `:1035-1041` covers a section with no command span, not an unparseable span; `:1213-1219` covers an empty header, not an empty argv0.

**Required fix:** fail closed when any declared procedure command has no parseable argv0 (including empty argv0 and a wrapper with no target); do not let that section resolve/suppress the last header or pointer findings. Keep this scoped to last-recheck replacement resolution, not a claim of full shell safety.

**Verification gap:** read-only assignment; runtime result/exit not exercised. LSP unavailable: `xd://lsp` is not a mounted device, so no status/references/definition/diagnostics were available; literal search is not semantic proof. Broader shell parsing remains out of scope.

Scope: executed=none