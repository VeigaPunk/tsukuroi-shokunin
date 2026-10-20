# README frontier supersession — re-attack

**Verdict: SURVIVES, for the captured host state only.**

## Findings

None in the assigned frontier-supersession scope. [obs] `corpus/README.md:38-39` retains the dated-looking “Pending `mkinitcpio` 42 upgrade” bullet, but `corpus/README.md:146-153` explicitly says that bullet is superseded **for this host**, records the 2026-10-20 upgrade, and retains an on-release watch. The apparent contradiction is explicitly closed rather than silently deleted.

[obs] The source corrections are properly narrower than the original rows: `corpus/SOURCES.md:64` (S058) scopes v42.2 init behavior to tagged source text; `:65` (S059) scopes the observed symlink to all four 42.2 images and the emulation to btrfs-overlayfs path steps on writable tmpfs, not a read-only root or real btrfs. The cited capture confirms four 42.2 symlinks and one 41.1 directory (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:51-66`); path emulation is at `:40-48`. `corpus/knowledge/boot-chain-r17.md:43-63` identifies both `/new_root` hook arguments but only describes emulating btrfs-overlayfs. Thus README’s parenthetical “namespace emulation; not boot-tested” is material, not proof that both hook behaviors succeed.

[obs] Relevant README/SOURCES bytes match between prerequisite `51dd9ee…` and baseline `842a531…`; README is unchanged from baseline to current. S058/S059 remain unchanged; later SOURCES additions begin at S060. **Residual risk:** Plymouth behavior, the read-only branch, real-btrfs behavior, and future release behavior remain unverified; read “both hooks resolve” as pathname compatibility, not successful hook execution. No stale-current-use finding remains for the host-specific supersession.

**Verification gaps:** no LSP device is mounted (`xd://lsp` returned “No such tool”); literal searches were locators only, with conclusions grounded in the exact reads above. No tests or runtime checks were performed.

Scope: executed=read-only git rev-parse/diff and literal grep; no host probes or target execution.
