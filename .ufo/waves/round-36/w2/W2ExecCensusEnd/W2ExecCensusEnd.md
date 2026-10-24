# Round 36 census / registry close-out

## Scope and result

Initial read-only `git rev-parse HEAD` returned `c052bb7d41ced49aa888817069afd804eccfecf1`. The first census run and checker invocation were launched together; the checker then reported branch tip `c052bb7d41ced49aa888817069afd804eccfecf1`. The census command validates the current worktree (it has no revision argument); I repeated it to persist the complete transcript in `census-end.txt`. A later checker capture reports branch tip `8d5fa7fe27c336d602a463519e839e932d26301d`; the cause of this change during the wave is **[unk]**. No production files were edited. The assigned artifacts are `census-end.txt`, `registry-coverage.txt`, and this report.

## Sources census

Command:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed exit: **0**. Full captured output (also retained in `census-end.txt`):

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init across scopes
tsukuroi	W04	S082 duplicate url git-scm.com/docs/git-rev-parse/2.56.0 across scopes
tsukuroi	W04	S087 duplicate url archlinux.org/news across scopes
tsukuroi	W04	S089 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S090 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S092 duplicate url wiki.archlinux.org/title/System_maintenance?oldid=885170 across scopes
tsukuroi	W04	S095 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 across scopes
tsukuroi	W04	S098 duplicate url gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs across scopes
tsukuroi	W04	S105 duplicate url archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks across scopes
tsukuroi	W04	S106 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S107 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S108 duplicate url wiki.archlinux.org/title/Downgrading_packages?oldid=887421 across scopes
tsukuroi	W04	S109 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions across scopes
tsukuroi	W04	S111 duplicate url gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook across scopes
tsukuroi	W04	S126 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml across scopes
tsukuroi	W04	S136 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml across scopes
tsukuroi	W04	S137 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S138 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst across scopes
tsukuroi	W04	S149 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S155 duplicate url raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst across scopes
tsukuroi	W04	S158 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c across scopes
tsukuroi	W04	S182 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S184 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S185 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

The 31 `W04` duplicate-URL diagnostics are warnings; the census ends `tsukuroi ok` and exits 0.

## Round-36 registry and coverage gate

`SKILL.md:3050-3060` contains the unique highest heading `## Gate and probe registry — round36 superseding current rows`. The table currently has only these two rows: `child-env-allowlist-r36` (`probe`) and `host-census` (`gate`). There is no `library` row in this operative round-36 table. The paragraph at lines 3052-3055 says round35 rows are retained, but the operative table shown at 3057-3060 contains only two entries.

Checker command:

```text
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py --revision c052bb7d41ced49aa888817069afd804eccfecf1
```

Observed checker exit: **1 (FAIL)**. The checker stdout (one JSON line) and `COMMAND_EXIT=1` marker are retained in `registry-coverage.txt`. Its JSON reports `findings=51`, `missing=51`, `registered=2`, `rows_total=2`, `tools_total=53`; findings identify unregistered regular `tools/` files (`REGISTRY-ROW-MISSING`). The saved invocation reports branch `master` tip `8d5fa7fe27c336d602a463519e839e932d26301d`. The earlier invocation's tool output reported the same requested revision/counts but branch tip `c052bb7d41ced49aa888817069afd804eccfecf1`; the reason for that branch-tip discrepancy is **[unk]**. Both invocations returned the coverage failure.

## Frozen probe SHA-256

The registry probe row says the frozen SHA-256 is recorded in the round-36 LOG freeze entry and receipt headers; the row references the value rather than embedding the 64-hex digest. `LOG.md:1377` records `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`. Read-only verification of the frozen counter object:

```text
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 1e926801195e304950e3eb9d2525ef8bbc245089:tools/probe-child-env-allowlist-r36.py | sha256sum
a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a  -
```

Thus the LOG's digest matches the probe bytes at freeze commit `1e926801195e304950e3eb9d2525ef8bbc245089`.

## Blocker / risk

The source census requirement is met. The requested registry coverage gate is **not clean**: the active table is two rows while the checker reports 51 of 53 tools missing (and no library-kind row). Production edits are outside this seat's scope, so this is reported for the L1 rather than changed here. No build, lint, formatter, or unrelated test was run; no tools were installed.
