# Omarchy source check: `/` mode `0555`

**Capture:** 2026-10-19. **Axes:** operability (permission-origin provenance) and depth (separating the root-directory mode from Snapper setup). **Scope:** read-only upstream Omarchy source and issue #6629; no host mutation or shipped-artifact RE.

## Finding

**[unknown] The origin of this host's `/` mode `0555` remains unidentified.** The Omarchy material checked here documents Snapper configuration and a missing `inotify-tools` dependency; it does not document `/` being set to `0555`, explain that mode, or say whether it is intended. Issue #6629 is related context, not provenance for the root-directory mode. Do not attribute the mode to Omarchy or to #6629 on this evidence.

The distinction matters: “root configuration” and `snapper -c root create-config /` refer to Snapper's configuration name and target path, not an assertion about the mode of `/`.

## Evidence chain

- The local evidence note records `/` as `555 root:root` with no ACL write bit (`corpus/knowledge/snapper-eacces-mechanism.md:9`). It records `pacman -Qo /` as unowned and a filesystem package mtree sweep with zero root-directory entries (`:13`); therefore there is no package metadata baseline in that note for the mode. These are prior recorded observations, **not probes run by this seat**.
- The local source registry already labels “Omarchy installer source that may explain `/` mode 0555” as an unopened lead and says the origin is unknown and no URL had been identified (`corpus/SOURCES.md:64`).
- Omarchy issue [#6629](https://github.com/omacom/omarchy/issues/6629) reports Omarchy 3.8.4's inactive Limine Snapper watcher due to missing `inotifywait`, no Snapper `root` config, and no dedicated `/.snapshots` subvolume. The reporter's workaround invokes `snapper -c root create-config /`. The maintainer's 2026-10-17 comment says 4.x adds `inotify-tools`, ensures the root config is created, and makes the no-config snapshot command explicit; it calls a dedicated top-level `@snapshots` subvolume a design change. Neither the issue nor its response mentions `/` mode `0555` or attributes an `EACCES` to that mode.
- At the pinned Omarchy v3.8.4 revision [`8fcc9d6`](https://github.com/omacom/omarchy/blob/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/install/login/limine-snapper.sh), the relevant Limine branch checks for a Snapper `root` config, runs `snapper -c root create-config /` when missing, and copies the default Snapper config to `/etc/snapper/configs/root` (lines 54–58). The script contents inspected do not directly chmod or chown `/`. Its dispatcher calls this script (`install/login/all.sh`, final line).
- At the pinned `quattro` commit [`81fd2d2`](https://github.com/omacom/omarchy/commit/81fd2d23ca6e3462183a4dc8360de3113fa8d80c), [`install/config/snapper.sh`](https://github.com/omacom/omarchy/blob/81fd2d23ca6e3462183a4dc8360de3113fa8d80c/install/config/snapper.sh) creates the Snapper config for `/` if its config file is absent, installs the template, writes the Snapper config-name file, and applies `chmod 0644` to that config-name file. It contains no direct mode change to `/`. [`install/config/all.sh`](https://github.com/omacom/omarchy/blob/81fd2d23ca6e3462183a4dc8360de3113fa8d80c/install/config/all.sh) dispatches `config/snapper.sh`. This confirms the present Snapper setup path, not the historical origin of the host's root mode.

## Competing interpretations and divergence

1. `/` may have inherited `0555` from an installer, image, or filesystem-layout step. No such source or captured install-time state was found in this bounded check.
2. The mode may have been changed after installation by a local administrator, another program, or policy. No change history was checked here.
3. The Omarchy Snapper script's `create-config /` call is a possible indirect lead, because the inspected script calls Snapper on `/`; however, the Omarchy wrapper itself does not change `/`'s mode, and Snapper's implementation and any before/after mode record were not inspected. This possibility is not evidence of causation.

Thus the known issue's last-known-good/different behavior concerns missing Snapper initialization and a watcher dependency; the observed `0555` root-directory state is a separate, unresolved provenance question. The checked Omarchy source supports the config setup behavior only. It does not establish that the mode is ordinary, intentional, or a bug.

**Risk:** #6629 does not justify changing `/` permissions. No permission repair, recommendation to run `chmod`, or causal PASS is supported by this source set. Resolving provenance would require trustworthy install-time or mode-change evidence beyond the sources inspected here.

## Search and execution record

- Read local `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` lead lines, and `corpus/knowledge/snapper-eacces-mechanism.md` evidence/source sections.
- Read the GitHub issue and the exact source URLs/revisions linked above; queried the Omarchy tag list to locate `v3.8.4` after the current `quattro` branch returned 404 for the historical script path. Read the `quattro` commit metadata to pin the current source revision.
- GitHub code search for `repo:omacom/omarchy "0555"` and `"chmod 755 /"` returned an authentication gate (“sign in to search code”). Therefore this is **not** a repository-wide source no-hit. A broad negative about all Omarchy code is not claimed. Synthesized `web_search` answers were not used as evidence.
- No LSP was available for these remote GitHub files; no local implementation/definition search was needed. Local text search was used only to locate repository evidence/lead references, not as semantic proof about upstream code.
- No host commands were run (unrun). No packages/tools were installed or updated. No tests, build, or formatter was run.
