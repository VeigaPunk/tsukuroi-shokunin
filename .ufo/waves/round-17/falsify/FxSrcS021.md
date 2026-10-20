# FxSrcS021 — SOURCES S021 and the lesson's quote

**Verdict: row SURVIVES; the alleged S021 "Gate quote" FAILS to exist — the lesson's only S021 quote (line 31) reproduces the source verbatim.**

[obs] Cited URL re-opened 2026-10-20 (text/plain, 1519 B): line 4 `root_mnt="/new_root"`; line 7 `fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0`.

[obs] Pin: commit 3c011dc2… committed 2026-01-11T13:38:30+01:00; files API content_sha256 eeac1ed3…/blob 6f6d98f5… identical at that ref and master, whose last_commit_id is 3c011dc2 — no later touch. (`/-/raw/<sha>/…` 403; API used.)

[obs] `corpus/lessons/round-17.md:31` (dd15c183): "Re-opened unchanged today: S021 (hook still `root_mnt="/new_root"`)" — verbatim. Gate rows 10-17 contain no S021 item; row 11 rejects only the 42.2 "silently no-ops" verdict, so no conflict.

[obs] `teaches` ⊆ source: "hardcodes /new_root" = line 4 literal (dracut sibling uses `${NEWROOT}`); "returns success when findmnt cannot find it" = line 7 `|| return 0`, and findmnt(8) §EXIT STATUS (manpages.debian.org, 2026-10-20): "1 on any error (for example … mountpoint does not exist)". Closing clause is a scope limiter, warranted (master URL mutable).

[unk] Later failure arms also `return 0` (understates). No boot or findmnt executed; symlinked `/new_root` behaviour is S055's emulation.

Scope: executed=sed -n (SOURCES.md head), grep -rn S021 (.ufo/waves/round-17), git show dd15c183 (corpus/lessons/round-17.md, corpus/SOURCES.md) | grep -n, git show dd15c183:corpus/lessons/round-17.md | sed -n 6,19p | cat -n, wc -w (report)
