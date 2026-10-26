VERDICT: draft

# Seat C2ScribeSkill — item C2-23 (round 40, hyaku run 8)

Item: draft (do not apply) an append-only `SKILL.md` section `## Hook and scriptlet execution
environment — round 40` — a decision table an operator acts on (symptom → EX row → what to check →
command), each row citing its EX id and source line. Draft only: no lane file was edited, no
`git`/`jj` command was run in the lane, no hook or scriptlet was executed, no host state was
changed. The proposed text is below, verbatim, ready to append after `SKILL.md:3324` (the file
currently ends with the round-39 corrections section, `SKILL.md:3316-3324`).

## Proposed SKILL.md text (append-only; do not apply)

```markdown
## Hook and scriptlet execution environment — round 40

Appended 2026-10-26 (round-40 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The
round-38 table above orders the hooks **inside** one phase (HO1–HO7) and the round-39 one fixes what
happens **between** phases (TO1–TO8); this section answers the narrower question for the update-safety
plane: what a hook `Exec` command or an install scriptlet **finds when it starts** — working directory,
streams, environment, interpreter, staged scriptlet file, stdin, `Depends`, and the paths a `Path`
trigger matches. Rules EX1–EX8 and their quotes: `corpus/knowledge/pacman-exec-environment-r40.md`
(source: S219–S225 — pacman `54d9411` `meson_options.txt`, `util.c`, `trans.c`, `hook.c`,
`alpm-hooks.5.asciidoc`, the Arch `PKGBUILD` at `7.1.0.r9.g54d9411-3`, and an own-work host capture;
snapshots `.ufo/waves/round-40/frozen/src/`, digests in `SHA256SUMS`; capture
`.ufo/waves/round-40/frozen/hostcap/`, MANIFEST sha256
`57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`). Every row cites the EX id and the
pinned source line it rests on. Detection and report only: nothing here authorizes a package, hook or
transaction action, and no hook or scriptlet was executed for it.

Measured on this host, 2026-10-26, read-only: `pacman 7.1.0.r9.g54d9411-3`; `pacman-conf RootDir` → `/`;
`pacman-conf HookDir` → `/etc/pacman.d/hooks/`; 67 hook files in `/usr/share/libalpm/hooks` plus 3 in
`/etc/pacman.d/hooks`, 69 effective after one same-name override, 14 of them carrying `NeedsTargets`;
`strings /usr/lib/libalpm.so.16.0.1` lists `/usr/bin/bash` and not `/bin/sh`; `pacman.log` holds 295
`running '…'` lines, 0 `could not satisfy dependencies` and 0 `could not create temp directory`; `/tmp`
is a separate xfs filesystem (`/dev/nvme1n1p1`,
`rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota`), mode `1777 root:root`, 125G free,
67M free inodes (1% used), 0 leftover `alpm_*` directories; `pacman-conf NoUpgrade` prints nothing (no
`NoUpgrade` line in `/etc/pacman.conf`); `/bin/sh` is a symlink to `bash` 5.3.20. These are probes, not
a transaction: none of them observes a hook or scriptlet running.

### Symptom → EX row → check → command

| Symptom (verbatim string or observation) | Rule (EX id, pinned line) | What it means | What to check | Command (read-only, paste-ready) | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|---|
| `Exec = /usr/bin/ldconfig -r .` (`11-glibc-ldconfig.hook:36`), or a hook/scriptlet writes a file the operator finds at `/`, or misses one it expected beside itself | EX1 (`util.c:628`, `:683`) | Every `_alpm_run_chroot` child — hook `Exec`, install scriptlet and `ldconfig` — starts in `/` of the installation root; `.` and bare names resolve there, not in the shell that ran pacman. Here the parent's `chdir` lands on `/` and no `chroot()` call happens | Is any path in the `Exec` or the scriptlet relative? `RootDir` (here `/`), so the host's `-r .` means `-r /` | `pacman-conf RootDir; grep -n 'ldconfig -r \.' /usr/share/libalpm/hooks/*.hook` | Make the path absolute in the hook or scriptlet; do not add a `cd` and expect it to survive — the child sets `/` itself |
| A `[ALPM-SCRIPTLET]` line cannot be split into stdout and stderr; an error line has no tag of its own | EX2 (`util.c:665-666`; tag at `util.c:527`) | One socket carries both streams merged; the only attribution is the `running '<name>'...` line above the text | The nearest preceding `running` line; whether the child printed anything at all | `awk '/\[ALPM\] running /{h=$0} /\[ALPM-SCRIPTLET\]/{print h; print}' /var/log/pacman.log \| tail -6` | Attribute the text by the hook header; read the merged order as arrival order, not program order |
| A hook whose `Exec` reads stdin (`while read -r f`, `cat`) loops zero times, or a `NeedsTargets` hook gets a list shorter than its trigger matches | EX6 (`hook.c:519-526`; feed `:469-490`, newline `:476`; `alpm-hooks.5.asciidoc:91-93`) with EX2 (`util.c:667`, `:722-726`) | Without `NeedsTargets` the parent closes the child's stdin at once, so the child reads end-of-file; with it the matched targets arrive sorted (`strcmp`), de-duplicated, one per line | `NeedsTargets` present? does the `Exec` read stdin? host: 14 effective hooks carry it, e.g. `texinfo-install.hook:10-11` | `h=/usr/share/libalpm/hooks/texinfo-install.hook; grep -n '^NeedsTargets' "$h"; grep -n '^Exec' "$h"` | Add `NeedsTargets` for a stdin-reading `Exec`; otherwise remove the read — it always sees EOF |
| `running '<hook>'...` in the log, the hook's effect absent, and no `unable to run hook …` line anywhere | EX7 (`hook.c:507-517`; `running` at `:653`, call at `:660`; abort `:660-668`) | The `running` line is written before `Depends` are checked; a missing `Depends` skips the command **after** the line is written and the error goes to stderr only; only a Pre `AbortOnFail` hook turns that skip into a transaction abort (0 such hooks here) | `Depends` against the local db; `When`; `AbortOnFail`; the stderr-side error count (0 in the live log) | `h=/usr/share/libalpm/hooks/10-glibc-locale-gen.hook; grep -n -e '^Depends' -e '^When' -e '^AbortOnFail' "$h"; for p in $(sed -n 's/^Depends = //p' "$h"); do pacman -Q "$p"; done; grep -n "running '$(basename "$h")'" /var/log/pacman.log \| tail -3; grep -c 'could not satisfy dependencies' /var/log/pacman.log` | Install the dependency or drop the `Depends` line; never read a `running` line as proof of execution |
| An install scriptlet dies with `syntax error near unexpected token`, `[[: not found` or `Syntax error: "(" unexpected` | EX4 (`trans.c:357`, `:410`; `PKGBUILD:115`; upstream default `meson_options.txt:17`) | Arch's libalpm runs a scriptlet as `/usr/bin/bash -c '. <scriptlet>; <function> <new> [<old>]'`; upstream's build default is `/bin/sh`. A hook `Exec` is not a scriptlet: libalpm execs `cmd[0]` directly (`hook.c:526`, `:528`), so a hook's shell is the one its `Exec` names | The installed libalpm's compiled-in shell string; whether the failing text lives in a local-db `install` file or in a hook `Exec` | `pacman -Q pacman; strings /usr/lib/libalpm.so.16.0.1 \| grep -Fx -e /usr/bin/bash -e /bin/sh; grep -nE -e '\[\[' -e '<<<' -e '\bfunction [a-zA-Z_]' /var/lib/pacman/local/systemd-262-1/install` | Keep bash-only syntax only where bash is the runner; a hook that needs it must name `bash -c`. `/bin/sh` is bash here, so this failure is a source-level conditional on this host |
| `error: could not create temp directory` in the middle of a transaction, and every scriptlet of that transaction fails | EX5 (`trans.c:361-369`; cleanup `:412-420`) | `mkdtemp("<root>/tmp/alpm_XXXXXX")` failed: `<root>/tmp` is absent and not creatable at 01777, or not writable, out of space or inodes, or read-only. The `tmp/alpm_XXXXXX/.INSTALL` file is never staged, so no scriptlet body runs | `RootDir` to map `<root>/tmp` (here `/`); mount, mode, free space and inodes of that directory; leftover `alpm_*` directories from a failed cleanup | `pacman-conf RootDir; findmnt -T /tmp; stat -c '%a %U:%G %n' /tmp; df -h /tmp; df -i /tmp; find /tmp -maxdepth 1 -name 'alpm_*' -ls` | Restore a writable 1777 `<root>/tmp` with space and inodes, then re-run the transaction; `could not remove tmpdir` in the log means cleanup left a directory behind |
| A `Path` hook's command ran while the file pacman left is `<file>.pacnew` beside an unchanged `<file>` | EX8 (`hook.c:258-279`; `NoExtract` skip `:271`; upgrade and removal sides `:281-306`) | Matching is against the package's file-list name, independent of the extraction outcome: `NoExtract` excludes a path, `NoUpgrade` does not, so a protected file still matches under its listed name | The hook's `Target`; `NoUpgrade` entries (none on this host, so this row is source-level here); the file pair and its mtimes | `pacman-conf NoUpgrade; h=/usr/share/libalpm/hooks/texinfo-install.hook; grep -n '^Target' "$h"; ls -l /etc/pacman.conf /etc/pacman.conf.pacnew 2>&1` | Make the command act on the `.pacnew` or on both files; never assume the old file was replaced |
| A file created by a hook or scriptlet is `0644`/`0755` although the operator's umask is stricter; a variable exported in the operator's shell reaches the command while a `BASH_ENV`/rc-file setting does not | EX3 (`util.c:692-695`, `execv` `:698`) | The child sets `SHLVL=1` when unset, removes `BASH_ENV` and sets umask 0022; every other variable of pacman's environment passes through unchanged | Mode of the created file; the operator's umask (the child's is fixed at 0022); where the variable was set | `stat -c '%a %U:%G %n' /var/log/pacman.log; umask` (substitute the created file) | `chmod` explicitly in the scriptlet; export variables before starting pacman |

### Limits of this table

- **No hook or scriptlet was run** for any row. Pacman transactions are paused on this host; every host
  value above is a read-only probe on 2026-10-26 or the frozen capture S225 (captured
  2026-10-26T06:54:46Z).
- **Correction to the entry's EX5 host cell** (`corpus/knowledge/pacman-exec-environment-r40.md:25`,
  "on this host `/tmp` is a tmpfs"): measured 2026-10-26, `/tmp` is xfs on `/dev/nvme1n1p1`
  (`findmnt -T /tmp`; `/etc/fstab:26`; `systemctl cat tmp.mount` is an fstab-generated xfs mount, not
  the systemd tmpfs). The rule (EX5) is unaffected; use the measured value. With 125G free and 67M free
  inodes, a `could not create temp directory` here would come from permissions or a removed
  `<root>/tmp`, not from exhaustion.
- **EX4 is a source-level conditional on this host**: `/bin/sh` is a symlink to `bash` 5.3.20, so
  bash-only scriptlet syntax does not fail here even under `/bin/sh`. That the shell choice matters is
  visible in the stored scriptlets: 8 of 51 `install` files under `/var/lib/pacman/local/` carry
  `[[`/`function` (`systemd-262-1/install:4`, `:76`).
- **EX8 has no host instance**: `pacman-conf NoUpgrade` prints nothing and `/etc/pacman.conf` has no
  `NoUpgrade` line, so the `.pacnew` row is source-level here. A `.pacnew` written from a package's
  `backup` list was not traced in this entry.
- **A `running` line without effect has more than one cause.** Check EX6 before EX7 when the `Exec`
  reads stdin: a silent command, an EOF read and an unmet `Depends` all leave the same log shape. The
  stderr-side `unable to run hook …` error is the only discriminator for the `Depends` case.
- **`[ALPM-SCRIPTLET]` proves one thing only**: a chroot child printed that line — not which child, not
  success (TO8).
- **A missing log line is weak evidence**: libalpm's parent-side validation and exec errors stay on
  stderr.
- **The counter scores the entry, not this section.** `exec-environment-r40` (gate registry,
  `SKILL.md:3119`) verifies the EX1–EX8 quotes against the pinned snapshots and two host values from the
  frozen capture (the 14/69 `NeedsTargets` count and the `/usr/bin/bash` string); it does not read this
  table, and it does not check the `/tmp` value above.

Counting: `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` — 0 when
EX1–EX8 each carry the source-derived value, the frozen proposition tokens and no negation word, a
4–25 word quote at the cited lines on a new mined upstream row, no duplicate row or heading, both
capture-derived host values, and 0 base hits of the novelty tokens; 1 when any of these fails; 2 on
revision, git or frozen-input failure. Frozen sha256
`d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`.
```

## Evidence for the draft

Frozen source pins (snapshots `.ufo/waves/round-40/frozen/src/`, `SHA256SUMS`):

- `util.c:628` `if(chdir(handle->root) != 0)`, `:665-667` `dup2(child2parent_pipefd[HEAD], 1|2)` and
  `dup2(parent2child_pipefd[TAIL], 0)`, `:683` `chdir("/")`, `:692` `setenv("SHLVL", "1", 0)`, `:694`
  `unsetenv("BASH_ENV")`, `:695` `umask(0022)`, `:698` `execv(cmd, argv)`, `:716-726` stdin end closed
  when no `stdin_cb`; `:527` `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line)`.
- `trans.c:357` `strcpy(arg0, SCRIPTLET_SHELL)`, `:361-369` `<root>/tmp/alpm_XXXXXX` + `mkdtemp` +
  `could not create temp directory`, `:410` `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)`,
  `:412-420` cleanup (`unlink`, `rmdir`, warnings).
- `hook.c:143` AbortOnFail rejected on a Post hook, `:258-279` Path match with the `NoExtract` skip at
  `:271`, `:469-490` target feed with `buf[len++] = '\n'` at `:476`, `:507-517` `Depends` check and
  `could not satisfy dependencies`, `:519-526` sort/dedup and `_alpm_run_chroot` for both stdin modes,
  `:653` `running '%s'...` before `:660` `_alpm_hook_run_hook`, `:660-668` abort gate for Pre only.
- `meson_options.txt:17` `option('scriptlet-shell', … value : '/bin/sh'`; `PKGBUILD:115`
  `-Dscriptlet-shell=/usr/bin/bash`.
- `alpm-hooks.5.asciidoc:61-67` `Target`, `:83-85` `Depends`, `:91-93` `NeedsTargets`.

Host probes (commands and verbatim outputs in `.ufo/waves/round-40/w1/C2ScribeSkill/host-probes.txt`):
`pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`; `strings /usr/lib/libalpm.so.16.0.1 | grep -Fx -e
/usr/bin/bash -e /bin/sh` → `/usr/bin/bash` only; 67 `/usr` hook files + 3 `/etc` hook files → 14
effective `NeedsTargets`; `grep -c 'could not satisfy dependencies' /var/log/pacman.log` → `0`;
`grep -c 'could not create temp directory' /var/log/pacman.log` → `0`; `findmnt -T /tmp` → xfs on
`/dev/nvme1n1p1`; `stat -c '%a %U:%G %n' /tmp` → `1777 root:root /tmp`; `pacman-conf NoUpgrade` → no
output; `11-glibc-ldconfig.hook:36` → `Exec = /usr/bin/ldconfig -r .`; `texinfo-install.hook:10-11` →
`while read -r f` + `NeedsTargets`; `10-glibc-locale-gen.hook:8-9` → `Depends = bash`, `Depends = glibc`
(both installed); 8 of 51 local `install` files carry `[[`/`function`. All commands in the table were
executed once in this seat with the same shape (read-only) before being written down.

Instrument scope: `tools/check-exec-environment-r40.py` checks only two host cells — EX6's
`"<N> of <M> effective hook files"` and EX4's `/usr/bin/bash` + `libalpm.so.16.0.1`
(`tools/check-exec-environment-r40.py:322-327`); `host_values()` reads the frozen `hooks-needstargets.tsv`
and `libalpm-shell-strings.txt` (`:184-187`). The EX5 host sentence is not read by the counter.

## Findings

### F1 — the entry's EX5 host cell is false as measured (`/tmp` is xfs, not tmpfs)

Verbatim conflict:

- Claim, `corpus/knowledge/pacman-exec-environment-r40.md:25` (EX5, host cell): `…on this host \`/tmp\` is a tmpfs |`
- Measured, 2026-10-26: `findmnt -T /tmp` → `/tmp   /dev/nvme1n1p1 xfs    rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota`;
  `/etc/fstab:26` mounts `/tmp` as `xfs`; `systemctl cat tmp.mount` → `Automatically generated by
  systemd-fstab-generator`, `What=/dev/disk/by-uuid/1f8a5361-…`, `Where=/tmp` (the `tmp.mount` name
  does not imply a tmpfs).

Effect: the EX5 *rule* (staging under `<root>/tmp`, `could not create temp directory`) is unaffected;
the host cell's mechanism is wrong, and one plausible operator reading — "scriptlets fail here when
the tmpfs fills" — is the opposite of this host's layout (125G free, 67M free inodes, 0 `alpm_*`
leftovers). The counter cannot catch it: neither `counts_ok` leg reads EX5. Suggested handling for the
L1 (not done by this seat): an append-only correction row in the section above, or an entry correction
commit; the draft already carries the measured value in its EX5 row and its first limit bullet.

### F2 — the entry's EX8 host cell has no host instance

`pacman-conf NoUpgrade` prints nothing and `/etc/pacman.conf` contains no `NoUpgrade` line, so on this
host no `.pacnew` outcome arises through `NoUpgrade`; the EX8 host cell is a conditional, not an
observation. The draft labels the row source-level rather than claiming an instance. (A `.pacnew`
written from a package's `backup` list is out of the entry's cited scope and was not traced.)

### F3 — the draft's commands avoid the Markdown pipe trap

`grep` alternation written as `\|` inside a Markdown table cell collides with the cell delimiter; the
draft uses repeated `-e` patterns for those, and `\|` only for real shell pipes. Each final one-liner
was run once (read-only) and produced the outputs recorded in the receipt.

## Behavior, gates, touched surfaces

- Behavior: none; this seat produced a draft only.
- Gates rerun by this seat: none (the counter was read, not run — the item is a draft; running it would
  score the entry, not the section, and is the L1's verification step).
- Touched surfaces: only this report and
  `.ufo/waves/round-40/w1/C2ScribeSkill/host-probes.txt`. No lane file, index, jj state, hook, package,
  service, mount, sysfs file or `/etc` file was modified; no `sudo`; no tool installed or upgraded; no
  process signalled.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r40/C2ScribeSkill` was created empty and removed at the end
  (nothing was built there).

## Out of scope / not done

- Did not apply the section to `SKILL.md`, did not edit the entry, `SOURCES.md`, counters, registry, or
  any other lane file.
- Did not run `tools/check-exec-environment-r40.py`, the census, or any transaction; did not run a hook
  or scriptlet; did not read `/boot`.
- Did not verify a `.pacnew` produced from a package `backup` list, and did not test the failure paths
  (`could not create temp directory`, unmet `Depends`) by execution — pacman transactions are paused.

## Artifact paths

- Report: `.ufo/waves/round-40/w1/C2ScribeSkill.md`
- Receipt: `.ufo/waves/round-40/w1/C2ScribeSkill/host-probes.txt`
- Proposal target: `SKILL.md` end (after line 3324), as an append-only section.
