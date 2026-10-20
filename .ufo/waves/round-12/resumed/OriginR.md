# Omarchy source check: `/` mode `0555`

**Captured:** 2026-10-20. **Axes:** operability (origin/provenance) and depth (separating Snapper setup from the root-directory mode). **Scope:** read-only Omarchy GitHub source and issue #6629. No host mutation or shipped-artifact RE.

## Finding

**[unknown] The origin of this host's `/` mode `0555` is not established by the inspected Omarchy sources or issue #6629.** Those sources document creating a Snapper `root` configuration for `/`; they do not document, explain, or endorse mode `0555`, nor tie it to the reported `EACCES`.

Here `root` names the Snapper configuration, and `/` is the target passed to `snapper create-config`. Neither fact is a statement about `/`'s inode mode. The current 4.x configuration script applies `0644` to Snapper configuration files, not to `/`.

## Evidence chain

1. **Inherited and local context (not a fresh host observation).** The inherited `.ufo/waves/round-12/Origin.md` records a 2026-10-19 host observation of `/` as `555 root:root`, no ACL write bit, and no owning package / mtree metadata baseline. I re-read that note and `corpus/knowledge/snapper-eacces-mechanism.md`; I did not repeat its host commands. These facts are historical context, not source evidence and not re-verified by this seat. The present `corpus/SOURCES.md` still describes the Omarchy installer as an unopened lead with unknown origin (Leads, “Omarchy installer source that may explain `/` mode 0555”).

2. **Issue #6629 is Snapper initialization context, not root-mode provenance.** The issue body identifies the reported system as Omarchy 3.8.4, describes an absent Snapper `root` config / `/.snapshots` and missing `inotifywait`, and gives `snapper -c root create-config /` as a workaround. It does not mention mode `0555` or claim that the command changes `/`'s mode. The sole maintainer comment ([issuecomment-6234472369](https://github.com/omacom/omarchy/issues/6629#issuecomment-6234472369), 2026-10-17) says the corresponding 4.x paths add `inotify-tools` and create the Snapper config when absent; it says nothing about `/`'s permissions. The local registry indexes this as **S037, Community tier C**, issue body § “What's wrong” / § “Workaround” and the 2026-10-17 comment; it is useful for the version-scoped issue history, not as causal evidence for the host's mode.

3. **Historical 3.8.x source.** I re-fetched the complete file at the inherited pinned revision [`8fcc9d6`](https://github.com/omacom/omarchy/blob/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/install/login/limine-snapper.sh). Its Limine branch checks for a Snapper `root` config, runs `snapper -c root create-config /` if missing, then copies the default config to `/etc/snapper/configs/root`. Its dispatcher, [`install/login/all.sh`](https://github.com/omacom/omarchy/blob/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/install/login/all.sh), invokes that script. In the complete fetched Snapper script I found no direct `chmod`/`chown` of `/` or explicit root-mode setting. This does **not** rule out an indirect effect inside Snapper itself; that implementation and a before/after mode record are outside this check.

4. **Present 4.x source, pinned to the fetched branch tip.** The GitHub recursive tree API returned `quattro` at commit [`4039002`](https://github.com/omacom/omarchy/tree/4039002da9c31560534272c0be75208a9eebc678). At that exact commit, [`install/config/snapper.sh`](https://github.com/omacom/omarchy/blob/4039002da9c31560534272c0be75208a9eebc678/install/config/snapper.sh) creates the Snapper config for `/` if absent, installs a template with `install -m 0644` to `SNAPPER_CONFIG_PATH` (default `/etc/snapper/configs/root`), and runs `chmod 0644` on `SNAPPER_CONF_PATH` (default `/etc/conf.d/snapper`). It contains no direct root-directory mode change. [`install/config/all.sh`](https://github.com/omacom/omarchy/blob/4039002da9c31560534272c0be75208a9eebc678/install/config/all.sh) dispatches this script. The fetched current script has the same relevant behavior as the previously cited `81fd2d2` version; however, `quattro` now resolves to `4039002`, so the older commit should not be presented as the current branch tip.

## Reuse, correction, limits

- **Reusable:** The inherited result that #6629 concerns missing Snapper setup rather than an evidenced `/` mode change remains supported. The old 3.8.x and present 4.x script behavior re-fetched consistently.
- **Corrected for present source state:** The inherited note's `81fd2d2` pin is a previously checked `quattro` snapshot, not the branch tip returned in this recheck. Use `4039002da9c31560534272c0be75208a9eebc678` for the present source snapshot; the relevant script behavior is unchanged in the fetched files.
- **Not established:** Neither the installer/image/filesystem-layout origin nor a later local administrator, program, or policy change is evidenced here. An indirect effect from the `snapper create-config /` call remains a possibility, not a finding; there is no captured install-time or before/after mode evidence.
- **Search boundary:** GitHub code search for `repo:omacom/omarchy 0555` returned the sign-in gate (“Sign in to search code”). I also fetched current and historical recursive tree listings, but did not read/search every source file. Therefore this is **not** a repository-wide no-hit and cannot prove no other Omarchy path sets a root mode. No guessed paths were opened; the source files inspected were the known issue-linked Snapper paths and their dispatchers.

## Risk and execution record

Do not attribute `/` mode `0555` to Omarchy, #6629, or Snapper on these sources; do not treat the `create-config /` call as proof of causation or as permission to change `/`. The competing explanations remain unresolved. The historical host measurements in the inherited note do not establish present host state.

Read-only static fetches succeeded for issue #6629, its comments, the pinned 3.8.x files, the exact `quattro` tip tree, and the two 4.x config files. The GitHub code-search page returned an authentication gate, not search results. No LSP route was exposed to this seat, and these remote GitHub files were not in a local LSP-served workspace; LSP references/implementation lookups were therefore unavailable, not attempted against an empty index. No host commands were run, so no command exit codes exist; no packages/tools were installed or updated. No tests, builds, linters, formatters, or smoke runs were performed.

**Confidence:** High for the contents and behavior of these exact fetched source snapshots and issue text; high that they do not directly state or set `/` mode `0555`; no confidence to identify the historical origin from this bounded source set. Overall provenance remains **unknown**.
