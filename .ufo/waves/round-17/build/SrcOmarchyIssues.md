# SrcOmarchyIssues — mkinitcpio 42, snapshot boots, Plymouth (accessed 2026-10-20)

Opened: `github.com/{basecamp,omacom}/omarchy/issues?q=…` (both are one tracker; payloads canonicalize to `https://github.com/omacom/omarchy/issues/<N>`) and `api.github.com/search/issues?q=<term>+repo%3Aomacom%2Fomarchy`.

[obs] HTML `?q=` was ignored by the fetcher (four queries returned the same 14 recent issues); `github.com/search` reported "0 results" for `mkinitcpio repo:basecamp/omarchy`, contradicting #6169 — unusable. API totals (all states): `sysroot` 2, `new_root` 10 (newest 2026-09-22), `"mkinitcpio 42"` 16, `btrfs-overlayfs` since 10-10: 4, `plymouth sysroot` 0.

[obs] #14246 H1: "mkinitcpio 42.2 copies /etc/vconsole.conf via the plymouth hook…" (2026-10-04, closed 2026-10-18). Correction (comment 6017695012, 2026-10-06): "…block comes from Arch's **plymouth** package, not mkinitcpio."

[obs] PR #14885 body (merged 2026-10-18, 4.0.6): "The issue blames mkinitcpio 42.2, but the block comes from the plymouth package".

[obs] Confirmed cause (#15802 "Root cause", 2026-10-18, same plymouth/mkinitcpio/limine as host): plymouth 26.134.222-3 bundles vconsole.conf; non-Latin layouts loop at LUKS. Snapshot boots worked: #15862 "The pre-update snapshot still booted successfully."; #15904 "The only working path left was the limine-snapper snapshot entries".

[obs] #6634/#8047 describe `/new_root` hook behaviour, never `/sysroot`; latest analysis 2026-10-08/09, pre-42.2.

[inf] Nothing above establishes an initramfs `/sysroot` regression; no issue links `/sysroot` to snapshot or Plymouth breakage. [unk] term search cannot prove absence; no 42.2 snapshot-boot with btrfs-overlayfs report exists. #16068 (2026-10-20) is Plymouth DRM tiling.

Scope: executed=none
