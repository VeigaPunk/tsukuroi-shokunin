# FxSrcS053 — attack on SOURCES S053 + lesson Gate quote

**Verdict: SURVIVES** (source facts verbatim; one clause is labeled inference)

Attacked bytes landed: `git status --porcelain` on the three files → empty; `git diff dd15c18` → 0 lines. S053 once at `corpus/SOURCES.md:59`; lesson row `corpus/lessons/round-17.md:25`.

[obs] Re-opened the releases API 2026-10-20 (read tool): 20 releases; v42 family is exactly `v42`, `v42.1`, `v42.2` (`v42.2` first = latest). Anchor correct: v42 `description` starts `CHANGES WITH v42`.

[obs] Gate quote verbatim: whitespace-normalized `"Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one."` is a substring of the v42 description (source wraps after `just like`).

[obs] `teaches` checks out: v42.1 `released_at 2026-09-27` — `/EFI/Linux` ESP creation, `install/systemd` halt/reboot/poweroff/shutdown symlinks and `systemd-pcrextend.socket`/`@.service`; v42.2 `2026-10-01` — `install/systemd` `systemd-tpm2-setup-early.service`, `systemd-pcrnvdone.service` (NvPCR/PCR 9). `/new_root` occurs **0×** in v42.1, v42.2, and all 20 descriptions; `/sysroot` occurs only in v42.

[inf] Boundary: `"so v42's /sysroot change stands for busybox hooks"` is inferred from release-notes silence, not asserted by S053; and `"TPM units"` compresses `systemd-pcrnvdone.service` (PCR 9). [inf] `boot-chain-r17.md:175` truncates the same quote without an ellipsis (distinct from the Gate row).

[unk] The access timestamp itself is unprovable; the match retains the payload's line-wrap, consistent with reading the API.

Scope: executed=sed, grep, cat (artifact copy to /tmp), wc, head, od, python3 (JSON/quote checks), git status/diff/show (read-only)
