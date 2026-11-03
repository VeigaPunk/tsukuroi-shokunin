## Round-65 additions (C1 sourced plane; C2 census arm)

Append-only round documentation (2026-11-03). The round-65 work: C1 the systemd v262
NvPCR/UKI applicability plane (`corpus/knowledge/systemd262-uki-pcr-r65.md`, SY1-SY5, SOURCED via
S282 — the v262 release body's "Changes in the TPM Subsystem" bullet, fetched live before the
declaration text); C2 the census initramfs arm (`probe_initramfs_arm` + the verdict-neutral
`INITRAMFS` line in `tools/tsukuroi-census.sh` — the owned initramfs/boot-recovery surface gains
its executable census read; overrides `TSUKUROI_MKINITCPIO_{CONF,CONFD,PRESETS,HOOKS}`; no
privilege, no mutation, never a rollup term, never an exit-code input; selftest cases
168 -> <N_AFTER>). No new tool: the registry stays 100 rows (the arm lives inside the registered
`tsukuroi-census` gate). Routed repairs landed, not claimed: the R64-SPOTCHECK-C1-PROOF
re-expression (SCORECARD erratum; the re-expressed identity command re-runs green at `431f0c9` —
SOURCES +3/-0, SKILL +120/-1 EOF artifact, SCORECARD 0/0, receipt
`.ufo/waves/round-65/after/reidentity-at-431f0c9.txt`) and one considerthese adoption
(<CONSIDERTHESE-SUMMARY>). Assimilation from `merge/tsukuroi/`: none — L0 `tsukuroi | round-64`
(+ 82-id addendum) open, mass id drift routed.
