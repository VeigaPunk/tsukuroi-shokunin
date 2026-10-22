# SrcOmarchyUpdate — C2 operator procedure source: how Omarchy updates packages

Verdict: the Omarchy way to update a machine is a scripted pipeline that ends in one full-system pacman transaction, so lifting the host-wide pacman pause "the Omarchy way" would mean running the `omarchy update` wrapper (not a bare pacman call), and the code for that wrapper differs between upstream `master` today (`pacman -Syu --noconfirm --overwrite '/usr/share/omarchy/*'`) and the version actually installed on this host (tag `v3.8.4`: `sudo pacman -Syyu --noconfirm`); I did not run any of it, and the row set below is the source evidence the C2 pause-lift gate can cite.

Scope of this seat: read the official Omarchy update script and its helpers in `github.com/basecamp/omarchy` (`bin/omarchy-update*`), record how packages are updated (which pacman command, snapshot before update, mirror handling), draft SOURCES rows, and describe what an operator would run to lift the pause the Omarchy way **without recommending running it**. Host actions were read-only.

---

## 1. Two versions of the update code are in play, and they issue different pacman commands

1.1 [obs] The host runs a git checkout of Omarchy at `~/.local/share/omarchy`, on branch `master`, exactly at tag `v3.8.4`, clean working tree, remote `https://github.com/basecamp/omarchy.git`.
- Evidence: command `git -C ~/.local/share/omarchy describe --tags --exact-match` → exit 0, output `v3.8.4`; `git -C ~/.local/share/omarchy rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'` → exit 0, output `master`; `git -C ~/.local/share/omarchy status --porcelain` → exit 0, empty output; `git -C ~/.local/share/omarchy remote -v` → exit 0, output `origin https://github.com/basecamp/omarchy.git (fetch)`.

1.2 [obs] The host-installed `v3.8.4` package-update step is a single full-system transaction with a forced database refresh:
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-system-pkgs:8-9` — `echo -e "\e[32m\nUpdate system packages\e[0m"` then `sudo pacman -Syyu --noconfirm`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update-system-pkgs` opened 2026-10-22 — quote: `sudo pacman -Syyu --noconfirm`.

1.3 [obs] Upstream `master` today splits the same step and adds a conflict handler; the transaction itself is now `pacman -Syu --noconfirm --overwrite '/usr/share/omarchy/*'`, and the interactive retry drops `--noconfirm`:
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-system-pkgs` opened 2026-10-22 — quote: `omarchy-update-pacman -Syu --noconfirm`; and quote: `exec omarchy-update-pacman -Syu --overwrite '/usr/share/omarchy/*'`.

1.4 [obs] Upstream `master` routes the transaction through a wrapper that adds sudo and a systemd scope:
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-pacman` opened 2026-10-22 — quote: `exec sudo env "${env_args[@]}" "${scope[@]}" pacman "$@"`; the file also states the reason in its comment block: `Registering the transaction as a PID 1 scope keeps it` … `out of the user manager's cgroups entirely`.
- [inf] The `-Syyu` → `-Syu` change between `v3.8.4` and `master` is material for premise P4: the installed code refreshes the sync databases forcibly (double `-y`) before upgrading, whereas upstream `master` relies on the databases already being fresh from the preceding keyring step and the snapshot.

1.5 [obs] Upstream `master` no longer ships two scripts that `v3.8.4` has: fetching `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-perform` and `.../master/bin/omarchy-update-branch` both returned HTTP 404 on 2026-10-22, while the host checkout contains both files.
- Evidence: fetch outcomes above; `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-perform:11-22` and `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-branch:15-36` exist locally.

## 2. What the update pipeline does, in order

2.1 [obs] Upstream `master` orchestrator (`bin/omarchy-update`), order of steps: sudo authorization → cache prune → snapshot → stay-awake → dev checkout update → keyring → system packages → migrations → orphan packages → log analysis → service restarts → `post-update` hook → mise → AUR → boot verification → reboot prompt.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update` opened 2026-10-22; the script body calls `omarchy-update-pkg-prune`, `omarchy-snapshot create`, `omarchy-update-keyring`, `omarchy-update-system-pkgs`, `omarchy-migrate`, `omarchy-update-orphan-pkgs -y`, `omarchy-update-analyze-logs`, `omarchy-update-restart --services-only`, `omarchy-hook post-update`, `omarchy-update-mise`, `omarchy-update-aur-pkgs`, `omarchy-update-boot`.

2.2 [obs] The installed `v3.8.4` orchestrator is much shorter: confirm prompt → snapshot → pull the Omarchy git checkout → run the pipeline.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update:19-23`:
  `if [[ $1 == "-y" ]] || omarchy-update-confirm; then` / `omarchy-snapshot create || (($? == 127))` / `omarchy-update-git` / `omarchy-update-perform`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update` opened 2026-10-22 — quote: `omarchy-snapshot create || (($? == 127))`.

2.3 [obs] The installed `v3.8.4` pipeline order is: keyring → available-icon reset → system packages → migrations → AUR → orphan packages → `post-update` hook → log analysis → restart/reboot prompt.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-perform:11-22`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update-perform` opened 2026-10-22 — quote: `Perform all update steps`.

2.4 [obs] The AUR phase runs third-party PKGBUILD code as the user with `yay -Sua --noconfirm --cleanafter --ignore gcc14,gcc14-libs`; the orphan phase removes unowned packages with `sudo pacman -Rs --noconfirm`.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-aur-pkgs:5-13` and `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-orphan-pkgs:6-11`.
- [inf] Those two phases are package transactions in their own right; an "omarchy way" lift of the pause therefore touches more than the single `pacman -Syyu` transaction.

2.5 [obs] The `v3.8.4` pipeline's first step pulls the Omarchy checkout itself (`git -C $OMARCHY_PATH pull --autostash`), i.e. it mutates the source tree under `~/.local/share/omarchy` before any package step.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-git:9-15`.

## 3. Snapshot before update

3.1 [obs] Both versions take a Snapper snapshot before the package transaction and treat "snapper absent" as a non-fatal skip (exit 127).
- Evidence: upstream `master` `bin/omarchy-update` opened 2026-10-22 — quote: `omarchy-snapshot create || (($? == 127))`; the surrounding comment reads `127 means Snapper deliberately absent.` → the exact source line is `# 127 means Snapper deliberately absent. Any other failure already said`.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-snapshot:17-18` — `if ! command -v snapper &>/dev/null; then` / `exit 127 # omarchy-update can use this to just ignore if snapper is not available`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot` opened 2026-10-22 — quote: `sudo snapper -c "$config" create -c number -d "$DESC"`.

3.2 [obs] Upstream `master` additionally refuses to let an unconfigured Snapper masquerade as a successful snapshot.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot` opened 2026-10-22 — quote: `Snapper installed but unconfigured snapshots nothing.`; the script then prints `Configure Snapper with: sudo bash -euo pipefail \"$OMARCHY_PATH/install/config/snapper.sh\"` and exits 1.

3.3 [obs] On this host Snapper is installed and configured with two configs, so the Omarchy snapshot step would in fact create snapshots (both `/` and `/home`):
- Evidence: command `sudo -n snapper --csvout list-configs` → exit 0, output `config,subvolume` / `home,/home` / `root,/`; command `sudo -n snapper list` → exit 0, output shows snapshots `1 │ single │ … │ Tue 20 Oct 2026 09:03:02 AM -03 │ root │ number │ pre-nvme-baseline-2026-10-20` and `2 │ single │ … │ pre-aur-elephant-2.22.1`.
- [unk] I did not verify whether a snapshot taken now would capture the post-mkinitcpio-42 state usefully; that is a boot-chain question outside this seat.

3.4 [obs] Upstream `master` also snapshots before a branch switch (in `v3.8.4`; the `master` script of that name now 404s).
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-branch:15-16` — `# Snapshot before switching branch` / `omarchy-snapshot create || (( $? == 127 ))`.

## 4. Mirror handling

4.1 [obs] Omarchy ships its own mirror list and pacman configuration templates per channel, and copies them into place whole.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/default/pacman/mirrorlist-stable` opened 2026-10-22 — quote: `Server = https://stable-mirror.omarchy.org/$repo/os/$arch`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/default/pacman/pacman-stable.conf` opened 2026-10-22 — quote: `Server = https://pkgs.omarchy.org/stable/$arch` and quote: `Include = /etc/pacman.d/mirrorlist` (that `Include` line appears for `[core]`, `[extra]` and `[multilib]`).

4.2 [obs] The mirror/template selection logic lives in `install/helpers/pacman.sh`; `x86` uses `default/pacman`, and the default channel is `stable` (except Apple Silicon, which is `edge`).
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/install/helpers/pacman.sh` opened 2026-10-22 — quote: `echo "$OMARCHY_PATH/default/pacman" ;;` (the `x86` branch of `omarchy_pacman_templates`) and quote: `aarch64-apple) echo edge ;;`.

4.3 [obs] The channel is detected by grepping the live configuration, not by reading a state file.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-version-channel` opened 2026-10-22 — quote: `Print the active Omarchy mirror and package channel`; the script matches `https://(arm-)?stable-mirror\.omarchy\.org/` in `/etc/pacman.d/mirrorlist` and `https://pkgs.omarchy.org/stable/` in `/etc/pacman.conf`.

4.4 [obs] Resetting the mirror/channel is a separate command, not part of `omarchy update`: `omarchy-refresh-pacman` backs up `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist`, copies the channel templates over them, and then forces a database reset plus a downgrade-capable upgrade.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-refresh-pacman` opened 2026-10-22 — quote: `omarchy-update-pacman -Syyuu --noconfirm` and quote: `Reset all package DBs and then update`; upstream adds `sudo cp -f /etc/pacman.conf /etc/pacman.conf.bak` and `sudo cp -f /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-pacman` opened 2026-10-22 — quote: `sudo pacman -Syyuu --noconfirm`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-refresh-pacman` opened 2026-10-22 — the upstream file also carries this rationale for skipping the `-dev` pair on stable/rc: `A stable or rc repository can still list an old -dev build`.

4.5 [obs] The host is already on the Omarchy stable mirror and the stable Omarchy package repository, i.e. exactly the upstream `stable` template content.
- Evidence: `/etc/pacman.d/mirrorlist:1` — `Server = https://stable-mirror.omarchy.org/$repo/os/$arch`; `/etc/pacman.conf:28-32` — `[omarchy]`, `Server = https://pkgs.omarchy.org/stable/$arch`, `Include = /etc/pacman.d/openai-chatgpt.conf`.
- Evidence: command `bash ~/.local/share/omarchy/bin/omarchy-version-channel` → exit 0, output `stable`.
- [inf] Therefore "mirror handling" is not a change the operator would need to make to lift the pause on this host; the mirror state already matches upstream's stable template, and `omarchy refresh pacman` would only re-copy the same content (plus a forced `-Syyuu` transaction).

4.6 [obs] The channel templates are selected by platform directory in upstream, and the ARM platforms have their own template directories.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/install/helpers/pacman.sh` opened 2026-10-22 — quote: `aarch64 | aarch64-apple) echo "$OMARCHY_PATH/default/pacman/$1" ;;`.

## 5. Cache handling and rollback (bears on premise P5)

5.1 [obs] Upstream `master` prunes the pacman cache before the snapshot and states why, and it keeps two versions per package.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-pkg-prune` opened 2026-10-22 — quote: `The cache is the only offline downgrade path, so keep two.` and quote: `sudo paccache -rk2`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update` opened 2026-10-22 — the comment above the prune call reads `# Before the snapshot: the cache is on the snapshotted subvolume, so pruning` / `# after it frees nothing until that snapshot ages out.`

5.2 [obs] On this host the pacman cache is on its own btrfs subvolume (`/var/cache/pacman/pkg` ← `@pkg`), which is separate from the root snapshot subvolume `@`.
- Evidence: command `findmnt -t btrfs -no TARGET,SOURCE` → exit 0, output ` /  /dev/mapper/root[/@]`, `├─/home  /dev/mapper/root[/@home]`, `├─/var/cache/pacman/pkg  /dev/mapper/root[/@pkg]`, `├─/var/log  /dev/mapper/root[/@log]`; command `sudo -n btrfs subvolume list /` → exit 0, output lists `ID 259 … path @pkg`.
- [inf] The upstream rationale quoted in 5.1 (prune before snapshot because the cache lives on the snapshotted subvolume) does not transfer to this host's layout, where pruning after a snapshot would still free space. It does not change the ordering as coded, but the comment's premise is false here.
- [unk] I did not compare the host's cache state (`paccache -rk1`, `paccache -ruk0`, `pacman -Scc` per the round-24 capture) against what upstream's `paccache -rk2` would retain; the premise P5 evidence is another seat's.

## 6. Boot verification (bears on premise P3)

6.1 [obs] Upstream `master` refuses to finish or offer a reboot until the platform's boot chain verifies after the package steps.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-boot` opened 2026-10-22 — quote: `Proves that the boot files the package steps left boot the updated system;`; the orchestrator then prints `The update is not finished: its boot files did not pass verification` and exits 1 when verification fails.

6.2 [obs] The installed `v3.8.4` has no equivalent boot verification step; it only offers a reboot when the running kernel differs from an installed kernel, or when a reboot-required marker file exists.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-restart:21-25`.

6.3 [inf] The installed version therefore has no automated guard against the `/new_root` versus `/sysroot` boot-chain mismatch that premise P3 concerns; on this host the reboot decision is left to the operator.

## 7. Keyring step contains a partial sync (relevant to the lane's update-safety rules)

7.1 [obs] The keyring step, in both the installed version and upstream `master`, refreshes the databases only and installs a single keyring package before the full upgrade.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy-update-keyring:12-13` — `sudo pacman -Sy` / `omarchy-pkg-add omarchy-keyring`; `:21` — `sudo pacman -Sy --noconfirm archlinux-keyring >/dev/null 2> >(grep -vE …)`.
- Evidence: URL `https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-keyring` opened 2026-10-22 — quote: `Ensure we have the latest archlinux-keyring, maintainer keys might have changed.` and quote: `sudo pacman -Sy --needed --noconfirm "${keyrings[@]}"`.
- [obs] Upstream's own comment on the `pacman -Sy` in that file reads: `This is generally not a good idea, but this is a special case because we're going to be updating`.
- [inf] The Omarchy flow therefore performs, by design, a partial sync (a `pacman -Sy` with a single package) before the full upgrade — the exact shape that the lane's tooling directive and this lane's update-safety gate forbid. Any decision to run the Omarchy pipeline on this host has to account for that, independently of the full-upgrade gate.

## 8. What an operator would run to lift the pause, the Omarchy way (description only — not a recommendation)

8.1 [obs] The user-facing entry point is the `omarchy` CLI route `omarchy update`, which dispatches to `omarchy-update` and is marked `requires_sudo: true`.
- Evidence: command `omarchy commands --json` → exit 0; the row read `{"route": "omarchy update", "binary": "omarchy-update", "group": "update", "name": "", "summary": "Update Omarchy and system packages", "requires_sudo": true, "args": "[-y]"}`.
- Evidence: `/home/vgpnk/.local/share/omarchy/bin/omarchy:489` — `omarchy update              Update Omarchy and system packages`.

8.2 [inf] So, describing the procedure without endorsing it: an operator on this host would run `omarchy update` (or `omarchy update -y`), and the installed `v3.8.4` code would then (a) prompt for confirmation, (b) create Snapper snapshots for `/` and `/home`, (c) `git pull` the Omarchy checkout at `~/.local/share/omarchy`, (d) refresh the keyring with `pacman -Sy` plus `omarchy-keyring`/`archlinux-keyring`, (e) run `sudo pacman -Syyu --noconfirm`, (f) run Omarchy migrations, (g) build and install AUR updates with `yay -Sua`, (h) remove orphaned packages with `pacman -Rs`, (i) run the `post-update` hook, (j) analyze `/tmp/omarchy-update.log`, and (k) offer a reboot if the kernel changed. Mirror state would not change, because the host already matches the upstream stable template; `omarchy refresh pacman` is the separate route that rewrites `/etc/pacman.conf` and `/etc/pacman.d/mirrorlist` and then runs `pacman -Syyuu`.

8.3 [obs] The lane's pause is host-wide on pacman transactions, and this seat performed none: no `pacman -S/-Sy/-Syu/-U/-R/-Scc`, no `paccache`, no `yay`, no `omarchy update`, no `omarchy refresh pacman`, no service restart, no configuration write, no boot action.

8.4 [inf] If the pause were lifted by an operator later, the Omarchy procedure would land the whole `pacman -Syyu` set (including `mkinitcpio` and the boot-chain packages) in a single transaction, with the snapshot taken first and — on this host's `v3.8.4` code — no boot-file verification step afterwards. That is an observation about the procedure's shape, not a recommendation to run it; whether it is safe here is a decision for the update-safety gate (P1–P5), not for this seat.

## 9. Draft SOURCES rows (for the L1 to number and merge into `corpus/SOURCES.md`)

All rows: `kind` = code, `tier` = A, `opened` = 2026-10-22, `status` = mined, `recheck` = on-release, `used-by` = `corpus/knowledge/pause-lift-gate-r24.json` (planned C2 gate entry; the file does not exist at the time of writing). The `id` column is left as `S0NN` placeholders because the L1 assigns the numbers. Every URL below was opened by this seat on 2026-10-22; each quote is copied exactly from the opened file and is at most 25 words.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | Upstream Omarchy update orchestrator — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update | code | A | The upstream `master` update pipeline's step order and where it delegates the package transaction; not the code installed on this host and not a host state report | master branch opened 2026-10-22; quote: `omarchy-snapshot create \|\| (($? == 127))` | The upstream update is a pipeline (prune → snapshot → keyring → system packages → migrate → AUR → boot verify → reboot), and a missing Snapper is a tolerated skip rather than a failure | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy system-package step — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-system-pkgs | code | A | The pacman invocation the upstream pipeline uses for system packages, including the conflict retry; not host package state | master branch opened 2026-10-22; quote: `omarchy-update-pacman -Syu --noconfirm`; quote: `exec omarchy-update-pacman -Syu --overwrite '/usr/share/omarchy/*'` | Upstream upgrades with `-Syu` plus `--noconfirm` and overwrites only Omarchy's own tree, and drops `--noconfirm` when a human must answer a conflict | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy pacman wrapper — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-pacman | code | A | How the upstream pipeline invokes pacman (sudo, environment, systemd scope); not a claim about any particular transaction | master branch opened 2026-10-22; quote: `exec sudo env "${env_args[@]}" "${scope[@]}" pacman "$@"` | The upstream update runs pacman under sudo inside a systemd scope so a systemd reexec during the transaction cannot kill it | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy snapshot helper — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot | code | A | How Omarchy takes a pre-update system snapshot with Snapper, including the unconfigured-Snapper case; not evidence that any particular snapshot was taken here | master branch opened 2026-10-22; quote: `Snapper installed but unconfigured snapshots nothing.`; quote: `sudo snapper -c "$config" create -c number -d "$DESC"` | Omarchy snapshots each configured Snapper config before updating, and refuses to let an unconfigured Snapper read as a successful snapshot | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy cache prune helper — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-pkg-prune | code | A | The upstream cache-pruning policy and its stated rollback rationale; not a measurement of this host's cache | master branch opened 2026-10-22; quote: `The cache is the only offline downgrade path, so keep two.`; quote: `sudo paccache -rk2` | Omarchy keeps two cached versions per package as the offline downgrade path, pruning before the snapshot | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy mirror and channel reset — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-refresh-pacman | code | A | How Omarchy installs its own mirror list and pacman configuration, and what transaction follows a channel reset; not a statement that this host needs a reset | master branch opened 2026-10-22; quote: `omarchy-update-pacman -Syyuu --noconfirm`; quote: `Reset all package DBs and then update` | A channel reset rewrites /etc/pacman.conf and the mirrorlist from templates (with .bak copies) and then forces a database reset plus a downgrade-capable upgrade | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy stable mirror list — https://raw.githubusercontent.com/basecamp/omarchy/master/default/pacman/mirrorlist-stable | code | A | The exact stable mirror template shipped by Omarchy; not a claim about the mirror's current health or freshness | master branch opened 2026-10-22; quote: `Server = https://stable-mirror.omarchy.org/$repo/os/$arch` | Omarchy's stable channel points every repository at its own mirror host, with Arch mirrors included by the same line | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy stable pacman configuration — https://raw.githubusercontent.com/basecamp/omarchy/master/default/pacman/pacman-stable.conf | code | A | The stable pacman.conf template's repositories and signature policy; not the live /etc/pacman.conf | master branch opened 2026-10-22; quote: `Server = https://pkgs.omarchy.org/stable/$arch`; quote: `Include = /etc/pacman.d/mirrorlist` | The stable template adds the Omarchy package repository, keeps Arch repositories on the included mirrorlist, and requires package signatures | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy pacman template selection — https://raw.githubusercontent.com/basecamp/omarchy/master/install/helpers/pacman.sh | code | A | Which template directory and default channel a platform takes; not a host channel determination | master branch opened 2026-10-22; quote: `echo "$OMARCHY_PATH/default/pacman" ;;`; quote: `aarch64-apple) echo edge ;;` | Templates are chosen per platform, x86 reading default/pacman, and the default channel is stable except on Apple Silicon | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy channel detection — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-version-channel | code | A | How the active mirror and package channel are read out of the live configuration; not a mirror-freshness measurement | master branch opened 2026-10-22; quote: `Print the active Omarchy mirror and package channel` | The active channel is inferred by grepping the live mirrorlist and pacman.conf, so a stale database still reports the configured channel | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy keyring step — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-keyring | code | A | The keyring refresh the update performs before the full upgrade, including its partial sync; not a keyring-health claim about this host | master branch opened 2026-10-22; quote: `Ensure we have the latest archlinux-keyring, maintainer keys might have changed.`; quote: `sudo pacman -Sy --needed --noconfirm "${keyrings[@]}"` | The upstream update refreshes signing keys with a partial sync before the full upgrade, and the file itself calls that generally a bad idea | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Upstream Omarchy boot verification — https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-update-boot | code | A | The upstream post-transaction boot-chain verification gate; not a verification that this host's boot chain would pass | master branch opened 2026-10-22; quote: `Proves that the boot files the package steps left boot the updated system;` | Upstream refuses to finish the update or offer a reboot until the platform's boot files verify | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Omarchy v3.8.4 update orchestrator (version installed on this host) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update | code | A | The update entry point of the exact release tag installed on this host; not the current upstream behaviour | tag v3.8.4 opened 2026-10-22; quote: `omarchy-snapshot create \|\| (($? == 127))` | The installed release takes a Snapper snapshot, pulls the Omarchy checkout, then runs the update pipeline, and skips the snapshot only when Snapper is absent | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Omarchy v3.8.4 system-package step (version installed on this host) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update-system-pkgs | code | A | The pacman command the installed release runs for system packages; not a host package-state measurement | tag v3.8.4 opened 2026-10-22; quote: `sudo pacman -Syyu --noconfirm` | The installed release performs one full-system upgrade with a forced double database refresh and no prompts, with no boot verification afterwards | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Omarchy v3.8.4 update pipeline (version installed on this host) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-update-perform | code | A | The ordered steps of the installed release's pipeline, including its AUR and orphan-package phases | tag v3.8.4 opened 2026-10-22; quote: `Perform all update steps` | The installed release's pipeline includes keyring refresh, full system upgrade, migrations, AUR update and orphan removal, i.e. more than one package transaction | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Omarchy v3.8.4 mirror and channel reset (version installed on this host) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-pacman | code | A | The installed release's mirror/template reset behaviour; not evidence that a reset was or should be run here | tag v3.8.4 opened 2026-10-22; quote: `sudo pacman -Syyuu --noconfirm` | The installed release's channel reset rewrites the pacman configuration and mirrorlist from its own templates and then forces a database reset with a downgrade-capable upgrade | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |

Note for the L1: the `master`-branch rows above are mutable (no commit pin is claimed, as with existing row S006); the `v3.8.4` rows are pinned to a tag and are the rows that describe the code actually installed on this host.

## 10. Out of scope and limits

- [obs] Not performed: any pacman, paccache, yay or `omarchy` transaction; any sync of a package database; any write to `/etc/pacman.conf`, `/etc/pacman.d/mirrorlist` or any other configuration; any service restart; any boot, snapshot or subvolume action; any edit to production lane files (`corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`); any git or jj write in the lane.
- [obs] Read-only host commands used: `git -C ~/.local/share/omarchy log/status/describe/rev-parse/remote -v`, `cat -n` of files under `~/.local/share/omarchy/bin` and `default/pacman`, `omarchy commands --json`, `bash ~/.local/share/omarchy/bin/omarchy-version-channel`, `sudo -n snapper --csvout list-configs`, `sudo -n snapper list`, `sudo -n btrfs subvolume list /`, `findmnt -t btrfs`.
- [unk] Whether a fresh Omarchy snapshot taken now would be a usable rollback point for the current boot-chain state (P3) was not determined here.
- [unk] The upstream `master` tree is mutable and was read once on 2026-10-22; no commit SHA is claimed for the `master` rows.
- [unk] Whether upstream's `master` update would pass this host's boot chain was not tested; only the presence of the verification gate is reported.

Scope: read=upstream omarchy bin/omarchy-update* helpers, default/pacman templates and install/helpers/pacman.sh (master and tag v3.8.4), the host's installed omarchy checkout at ~/.local/share/omarchy, /etc/pacman.conf, /etc/pacman.d/mirrorlist, snapper config and snapshot lists, and the btrfs subvolume layout; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/SrcOmarchyUpdate.md; executed=read-only host queries only (git log/status/describe/rev-parse/remote -v, omarchy commands --json, omarchy-version-channel, sudo -n snapper --csvout list-configs, sudo -n snapper list, sudo -n btrfs subvolume list /, findmnt -t btrfs, cat of omarchy sources) and HTTP GETs of the URLs listed above
Installs: none
