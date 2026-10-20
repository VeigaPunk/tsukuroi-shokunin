# FxSrcS022 — SOURCES S022 and the lesson's quote

**Verdict: row SURVIVES; the alleged "Gate quote" FAILS — round-17.md carries no S022 Gate item.**

[obs] `SOURCES.md:28` pins commit df088501c9bf…. GitLab API: title "Move plymouth from AUR with 580 votes", committed 2023-03-21T01:25:10Z; `commits?path=plymouth.initcpio_hook` returns only it, so the pin is the sole and last commit touching the file.

[obs] `…/plymouth/-/raw/main/plymouth.initcpio_hook` § run_latehook, accessed 2026-10-20: "plymouth update-root-fs --new-root-dir=/new_root" (12 words). Files API: content_sha256 de852646…8b6f, last_commit_id df088501…; that sha equals the PKGBUILD `sha256sums` entry whose `package()` installs it as `usr/lib/initcpio/hooks/plymouth`. "Packaged … busybox latehook" holds; bytes unchanged since 2023.

[obs] `teaches` — "The packaged latehook passes /new_root to plymouth update-root-fs; the code alone does not establish the impact of that path mismatch" — stays inside the source; its second clause is an explicit non-claim.

[obs] `corpus/lessons/round-17.md` never writes "plymouth" or "latehook" (`grep -ic plymouth` → 0); Gate lines 9–16 contain no S022 row; new rows (23–29) are S051–S057. Sole S022 text, line 31: "S022 (hook still `--new-root-dir=/new_root`)" — a re-open note, token verbatim.

[unk] plymouth option semantics (declined by the row); PKGBUILD at main HEAD; any wave-1 report carrying the assumed quote.

Scope: executed=grep S022 row (SOURCES.md), grep plymouth and S022 (round-17.md), grep latehook/no-op (round-17.md), ls -d falsify dir
