VERDICT: defect-found

Item C2-EX5 — row EX5 of `corpus/knowledge/pacman-exec-environment-r40.md:25` (tip f951f288483c1af0cef4afd458488b84cf7a2165; the file is clean vs HEAD, `git diff --stat HEAD -- <file>` empty) judged against the pinned source trans.c (S222, snapshot sha256 `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`).

Row verdict: **partly** — the rule, value and source cells hold at the cited lines except two rule-cell glosses the pinned source does not state ("private", "(from the local database)"), and the host cell's second sentence ("on this host `/tmp` is a tmpfs") is **false on this host** (`/tmp` is xfs on `/dev/nvme1n1p1`) and has no record in the frozen hostcap capture. The declared L1 claim ("scriptlet staged at `<root>/tmp/alpm_XXXXXX/.INSTALL` then removed") itself is supported; the defect is the host cell.

## 1. Provenance (re-open)

Upstream raw re-opened by this seat, access time **2026-10-26T07:15:30Z** (`date -u` at curl start), `curl -fsS --retry 2`:

- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c → sha256 `637c1165…` = SHA256SUMS row
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc → `2970cb35…` = row
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/meson_options.txt → `89e5b350…` = row
- https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD → `32d40dfd…` = row

All four fetched digests equal `.ufo/waves/round-40/frozen/src/SHA256SUMS`; `sha256sum -c SHA256SUMS` in that dir reads OK for all six files (hook.c, util.c not re-fetched upstream — EX5 needs neither). Receipt: `.ufo/waves/round-40/w1/C2RevEX5/upstream-fetch.txt`. Below, "trans.c" = the pinned snapshot `.ufo/waves/round-40/frozen/src/trans.c` (digest-verified).

## 2. Rule cell, clause by clause

1. **"Before a scriptlet runs" — holds.** Staging happens inside `_alpm_runscriptlet` before the scriptlet is run: tmpdir creation trans.c:360-372 precedes `retval = _alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL);` trans.c:410.
2. **"libalpm requests `<root>/tmp` with mode 01777 when that directory is missing" — holds.** trans.c:363 `snprintf(tmpdir, len, "%stmp/", handle->root);`, :364 `if(access(tmpdir, F_OK) != 0) {`, :365 `_alpm_makepath_mode(tmpdir, 01777);`. `_alpm_makepath_mode` (pinned util.c:110-148): `oldmask = umask(0000);` :118, `mkdir(str, mode)` :129/:140, `umask(oldmask);` :145 — the mode is requested of mkdir(2) with the umask cleared, so a created `<root>/tmp` gets exactly 01777. "Requests" is accurate (conservative, if anything).
3. **"makes a private directory `tmp/alpm_XXXXXX` under the root" — partly.** Name, location and creation hold: trans.c:361 `strlen("tmp/alpm_XXXXXX")`, :367 `snprintf(tmpdir, len, "%stmp/alpm_XXXXXX", handle->root);`, :368 `mkdtemp(tmpdir)`. **"private" is not stated by the pinned source**: mkdtemp's 0700 mode is libc semantics, absent from the pinned snapshot (QUALITY 66, `corpus/QUALITY.md:133` — a statement keeps what its quoted source states).
4. **"copies (from the local database) or extracts (from a package file) the scriptlet into it as `.INSTALL`" — partly.** The two branches and the `.INSTALL` name hold: trans.c:374 `/* either extract or copy the scriptlet */`, :375-377 `scriptfn = "<tmpdir>/.INSTALL"`, :378-381 `is_archive` → `_alpm_unpack_single(handle, filepath, tmpdir, ".INSTALL")`, :382-386 else `_alpm_copyfile(filepath, scriptfn)`. "Extracts (from a package file)" holds via the is_archive branch (:378-379; the archive vs scriptlet-file distinction is stated at :351-353). **"Copies (from the local database)" is not stated by the pinned source**: trans.c:383 copies from `filepath` and the pinned snapshot contains no caller. The attribution is true upstream — add.c:641 `char *scriptlet = _alpm_local_db_pkgpath(db, newpkg, "install");` feeding `_alpm_runscriptlet(…, 0)` at add.c:644, and remove.c:709/729 → :711/:731 — but add.c/remove.c are outside the pinned snapshot and uncited by the row (supplementary fetch 2026-10-26T07:18:06Z, sha256 `fd313629…`/`a052d455…`; not row evidence).
5. **"sources it from there" — holds.** trans.c:397-398 chops the root off scriptpath (`/* chop off the root so we can find the tmpdir in the chroot */`), :400-406 builds `cmdline` = `. <scriptpath>; <script> <ver> [<oldver>]`, run at :410 through `_alpm_run_chroot` — the `.` command sources `tmp/alpm_XXXXXX/.INSTALL` inside the chroot.
6. **"afterwards removes the file and the directory" — holds.** trans.c:412 `cleanup:`, :413 `if(scriptfn && unlink(scriptfn))`, :417 `if(rmdir(tmpdir))`.
7. **"logging a warning when either removal fails" — holds.** trans.c:414-415 `ALPM_LOG_WARNING … _("could not remove %s\n"), scriptfn`, :418-419 `_("could not remove tmpdir %s\n"), tmpdir`.

**Value cell `tmp/alpm_XXXXXX/.INSTALL` — holds** (trans.c:367 + :377; the frozen counter derives the same string from the snapshot, `tools/check-exec-environment-r40.py:163-167`).

**Source cell — holds.** The quote `/* create a directory in $root/tmp/ for copying/extracting the scriptlet */` is verbatim at trans.c:360 (`grep -cF` on the pinned file → 1), inside the cited range 360-377; `mkdtemp` :368, error `could not create temp directory` :369, cleanup :412-420 — all at the cited lines. Excerpt receipt: `.ufo/waves/round-40/w1/C2RevEX5/trans-c-ex5-lines.txt`.

## 3. Host cell

- **Sentence 1 — holds** (source-derived): "A root whose `/tmp` cannot hold a new directory fails every scriptlet with `could not create temp directory` (trans.c:369)". `mkdtemp` failure → trans.c:369 error log, :370-371 `free(tmpdir); return 1;`; every scriptlet run passes through :368. Consistent also when `<root>/tmp` is missing and uncreatable: `_alpm_makepath_mode`'s failure at :365 is unchecked and `mkdtemp` then fails into :369. The wording claims scriptlet failure, not transaction abort — accurate.
- **Sentence 2 — fails.** "on this host `/tmp` is a tmpfs" is **false** on this host (plazir27). Observed read-only 2026-10-26T07:18:06Z (receipt `host-tmp-fstype.txt`):
  - `findmnt /tmp` → `TARGET SOURCE FSTYPE OPTIONS` / `/tmp /dev/nvme1n1p1 xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota`
  - `stat -f -c %T /tmp` → `xfs`
  - `/proc/self/mountinfo` → `250 33 259:4 / /tmp rw,nosuid,nodev,noatime shared:213 - xfs /dev/nvme1n1p1 …`
  - `/etc/fstab:26` mounts `/tmp` as xfs (`UUID=1f8a5361-4f35-449a-bb30-63669df878d1`); the fstab comment (:25) reads "# /tmp is emptied at every boot by /etc/tmpfiles.d/tmp.conf; nofail keeps boot working if the drive is missing." — emptied-at-boot via tmpfiles.d on a disk partition, not a tmpfs mount.
  - `df -T /tmp` → `/dev/nvme1n1p1 xfs …`
- **No capture backing either**: the frozen hostcap `.ufo/waves/round-40/frozen/hostcap/` records no `/tmp` fstype — `MANIFEST.sha256` (sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`, equals SOURCES S225) lists exactly `capture-meta.txt`, `libalpm-shell-strings.txt`, `hooks-needstargets.tsv`, and `capture-meta.txt` records pacman_q/libalpm/owner only. The entry's own header (`pacman-exec-environment-r40.md:13`) says "the host column comes from a frozen read-only capture" — this sentence had none.
- **The frozen counter cannot see it**: `tools/check-exec-environment-r40.py` (sha256 `d4a2bb94…`, matches the declaration) checks host cells only for EX6 (:322) and EX4 (:324-326) — "the two host values" (docstring :5, :31-34). Its host record in the author's after-receipt `.ufo/waves/round-40/after/c2-after-bf23805.jsonl:17-21` is `{hooks_total: 69, hooks_needstargets: 14, libalpm_usr_bin_bash: 1}`; EX5 reads `"present": true, "verified": true, "reasons": []` (:61-64) and the run is PASS/exit 0 (:82-83) with the false sentence in place.

## 4. Proposed append-only correction text

Append to `corpus/knowledge/pacman-exec-environment-r40.md` (append-only; the frozen counter's EX5 checks — value/tokens/quote at `check-exec-environment-r40.py:90,163-167,280` — do not read the host cell, so this correction cannot flip the counter):

```markdown

## Wave-1 corrections (appended 2026-10-26, seat C2RevEX5)

- EX5 host cell, second sentence ("on this host `/tmp` is a tmpfs") is withdrawn as false: on this host
  `/tmp` is a separate xfs partition, `/dev/nvme1n1p1`, mounted by `/etc/fstab` (line 26,
  `UUID=1f8a5361-4f35-449a-bb30-63669df878d1  /tmp  xfs  rw,noatime,nosuid,nodev,logbsize=256k,nofail,…`)
  and emptied at every boot by `/etc/tmpfiles.d/tmp.conf` (fstab comment, line 25); observed read-only
  2026-10-26T07:18:06Z with `findmnt /tmp` → FSTYPE `xfs`, `stat -f -c %T /tmp` → `xfs`, and
  `/proc/self/mountinfo` → `- xfs /dev/nvme1n1p1`. The frozen hostcap capture (MANIFEST.sha256
  `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`) records no `/tmp` fstype, so the
  sentence also had no capture backing. The first host sentence (a root whose `/tmp` cannot hold a new
  directory fails every scriptlet with `could not create temp directory`, trans.c:369) is unaffected.
  Receipt: `.ufo/waves/round-40/w1/C2RevEX5/host-tmp-fstype.txt`.
- EX5 rule cell, two glosses read as qualified (QUALITY 66, `corpus/QUALITY.md:133`): "private" — the
  pinned trans.c states the name `tmp/alpm_XXXXXX` and `mkdtemp` (trans.c:361,367-368); the 0700 mode
  mkdtemp creates with is libc semantics, not in the pinned snapshot. "(from the local database)" — the
  copy branch (trans.c:383) copies from `filepath`; that filepath is the local database's `install` file
  per the caller `_alpm_local_db_pkgpath(db, newpkg, "install")` (upstream add.c:641, used at add.c:644;
  remove.c:709-711,729-731), files outside the pinned snapshot, re-opened 2026-10-26T07:18:06Z only for
  this note (sha256 add.c `fd313629…`, remove.c `a052d455…`).
```

Optional (L1's call, not part of the correction): if the host column should regain capture backing, a fresh capture row for `/tmp`'s fstype would mean a new hostcap capture and a new MANIFEST digest, i.e. an S225 update — the withdrawn wording above needs no capture change.

## 5. Not done / residual

- Did not run `tools/check-exec-environment-r40.py` myself; the counter state is cited from the author's after-receipt and the counter source. Its EX5 checks do not read the host cell, so a rerun cannot bear on the defect found.
- Did not re-fetch hook.c/util.c upstream (EX5 needs neither; pinned digests verified by `sha256sum -c`).
- add.c/remove.c were fetched outside the pin only to characterize the "(from the local database)" gloss as true-but-unpinned; they are not row evidence and the correction cites them as such.
- Residual: none within this item's scope. The other EX rows' host cells were not examined (out of scope for C2-EX5).

## 6. Tooling and bounds

No tools installed or upgraded (curl and coreutils only; no pacman transaction, no service restart, no host mutation — all host reads read-only). Scratch `/fast/scratch/hyaku/tsukuroi-r40/C2RevEX5` removed after receipts were copied. Written: this report and the three receipts under `.ufo/waves/round-40/w1/C2RevEX5/` only.
