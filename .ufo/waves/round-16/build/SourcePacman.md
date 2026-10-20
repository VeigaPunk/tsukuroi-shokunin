# SourcePacman — `--print` planning distinction

**Observed** (2026-10-20). Opened `https://man.archlinux.org/man/pacman.8` (reader: ECONNRESET; `curl -sS https://man.archlinux.org/man/pacman.8.raw` exit0, 29,919 bytes). Page footer: Pacman 7.1.0, 2026-10-15. Section **TRANSACTION OPTIONS (APPLY TO -S, -R AND -U)**, option `-p, --print`, exact text:

> "Only print the targets instead of performing the actual operation (sync, remove or upgrade)."

Following sentence: "Use --print-format to specify how targets are displayed. The default format string is \"%l\"…"; `--print-format` "Implies --print".

**Distinction.** The page contrasts listing targets with performing the operation; it never says "planning". It does not state that `--print` suppresses `-y/--refresh` (SYNC OPTIONS: "Download a fresh copy of the master package databases (repo.db)…") or network access; `-w, --downloadonly` is separately defined ("Retrieve all packages from the server, but do not install/upgrade anything.").

**Limits.** Static page only; no host probe, no new registry row. Existing text matches `corpus/SOURCES.md` S048 and `corpus/lessons/round-15.md:22`. High confidence on text/locator. Unresolved: whether `-y --print` still writes sync databases — not stated here; `corpus/knowledge/update-safety-v3.md:7` ("no download, no db write") is stronger than this quote.
