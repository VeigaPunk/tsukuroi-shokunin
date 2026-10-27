VERDICT: draft

Item C2-S10 — draft of the round-46 lesson Gate block "Re-opened rows and rows touched old→new". The
deliverable is the Markdown in §3; §1-§2 are the evidence behind each cell, §4-§5 the limits and one adjacent
observation. Everything below was run read-only against `a44770491eb5ca15ce9f8b3207309d1af683ffaf` and the frozen
snapshots; no lane file, host service, unit, sysfs attribute or PATH directory was touched.

## 1. Rows touched base→implementation (the item's question)

Receipt: `.ufo/waves/round-46/w1/SrcReopenR45/col-diff.txt`.

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff \
  2042117cfb724170772f4c128cc2ddba0b61d817 a44770491eb5ca15ce9f8b3207309d1af683ffaf -- corpus/SOURCES.md
@@ -256,6 +256,8 @@                       ← one hunk
--numstat → 2	0	corpus/SOURCES.md
removed lines, grep -cE '^-[^-]' → 0
added lines,  grep -cE '^\+[^+]' → 2
rows, grep -cE '^\| S[0-9]+ ' → 249 (base) / 251 (implementation)
```

The two added lines are the new rows `S250` and `S251` at `corpus/SOURCES.md:259-260`, immediately after `S249`
at `:258`. **Zero removed lines means no cell of any old row changed in any column** — not the last (used-by)
column, not the locator/digest column, not the recheck column. Extracted used-by cells for the ten ids are
identical at base and at implementation (`col-diff.txt` §"used-by", both revisions printed). So the answer is:
only new rows were added; no old row was edited.

## 2. Re-open evidence I ran myself (2026-10-27, read-only, `curl` + `cmp` + `sha256sum` + `git ls-remote`)

- **15 live fetches, all HTTP 200**, 2026-10-27T05:23:37Z–05:23:47Z: S237 `cmds/scrub.c` (btrfs-progs v7.1);
  S242 `fs/btrfs/scrub.c`, S243 `fs/btrfs/sysfs.c`, S247 `fs/btrfs/dev-replace.c` (linux v7.2.11 `plain/`); S244
  `btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD` (packaging 7.1-1 raw); S246 `lib/cmdline.c`,
  `lib/vsprintf.c`, `lib/kstrtox.c`; S248 `man/systemd.kill.xml` (systemd v262 raw); S250 `shell.c`, `general.c`,
  `general.h` (bash-5.3 cgit plain); S251 `proc_pid_fd.5.html` (man7). URLs, codes and per-file timestamps:
  `.../SrcReopenR45/commands-live.txt`.
- **Byte identity, not only digests**: `cmp -s` live-vs-frozen → `15/15 IDENTICAL, 0 DIFFER`
  (`cmp-live-vs-frozen.txt`). This closes, for my own evidence, the `cmp` gap C2ExecLiveSources reports for its
  batch.
- **Frozen manifests verify**: `sha256sum -c SHA256SUMS` → OK 2/2 in `.ufo/waves/round-42/frozen/src`, 5/5 in
  `round-44`, 5/5 in `round-45`, 4/4 in `round-46` (`frozen-check.txt`).
- **Live digests equal the rows' own locator cells**: S237 `48df2e2f…0801`; S242 `f347931b…a5b8`; S243
  `ce146120…1c43`; S244 timer `9a0b6cc2…f8ad` / service `eaa7af92…0252` (PKGBUILD `3b803e8b…ce98` matches
  `round-44/frozen/src/SHA256SUMS`; the row names `PKGBUILD:99-101` without a digest); S246 `1af5ad98…ca9d`,
  `cabb648a…69ca`, `0c52ae02…1ee4`; S247 `f07ef0a0…4f3a`; S248 `44832283…0e72`; S250 `5f3d539f…f73d`,
  `669ef408…d165`, `bf9251e3…f2f2`; S251 `3a50ddef…f27e` (`sha256-live.txt`).
- **Tag pins re-resolved** (`tags-live.txt`): `refs/tags/v7.2.11^{}` `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`;
  btrfs-progs `refs/tags/v7.1^{}` `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`; `refs/tags/v262^{}`
  `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`; `refs/tags/bash-5.3` `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`
  (lightweight tag: the id is the commit); packaging `refs/tags/7.1-1^{}`
  `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`. All equal the rows and the `FETCH.txt` logs.
- **S249 host re-run** (seat C2ExecHostRecheck, `.ufo/waves/round-46/w1/C2ExecHostRecheck/capture-now.txt`, run
  at 2026-10-27T05:21:49Z, uid 1000, `CapEff=0000000000000000`): its nine value lines are identical to round-45
  `capture.txt`; `diff -u` prints exactly one line, `captured <timestamp>` (`hostcap-diff.txt`). The frozen
  `capture.sh` `c6d2c448…51fc` and `capture.txt` `f5958a83…1e70` still match the S249 row.
- **S250/S251 locators read at the pinned lines** in `.ufo/waves/round-46/frozen/src`: `shell.c:1586`
  `fd = open (filename, O_RDONLY);`, `shell.c:1700` `fd = move_to_high_fd (fd, 1, -1);`, `general.h:252`
  `#define HIGH_FD_MAX	256`, `proc_pid_fd.5.html:73-75` "which is a symbolic link to the actual file";
  `:79-80` "will be symbolic links whose content is the file type with the inode".
- **Peer confirmation**: `.ufo/waves/round-46/w1/C2ExecLiveSources.md` re-fetched S237, S242, S243, S244 service
  and S246/S247/S248 with matching digests (its batch timestamp 05:22:16Z); its stated limit is that its `cmp`
  batch aborted, so its identity claim is digest-only. The S244 timer and PKGBUILD were re-fetched only in my
  batch.
- **Freshness of the pins on this host** (`host-packages.txt`): `pacman -Q` → `linux 7.2.11.arch1-1`,
  `btrfs-progs 7.1-1`, `systemd 262-1`, `bash 5.3.20-1`; `uname -r` → `7.2.11-arch1-1`. The kernel, btrfs-progs,
  systemd and packaging `on-release` pins still name the installed versions; bash 5.3 upstream patches 1-20 sit
  outside tag `bash-5.3`, as `round-46/frozen/src/FETCH.txt` records.

## 3. Drafted block — exact Markdown

### Re-opened rows and rows touched old→new (opened 2026-10-27 by wave-`w1` seat SrcReopenR45; `corpus/SOURCES.md` only)

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 2042117cfb724170772f4c128cc2ddba0b61d817 a44770491eb5ca15ce9f8b3207309d1af683ffaf -- corpus/SOURCES.md` is one hunk (`@@ -256,6 +256,8 @@`), two added lines and none removed (`--numstat` `2 0`): the new rows `S250`/`S251` at `:259-260`, nothing after `S249`. No cell of any old row changed in any column, so the registry goes 249 → 251 rows with every earlier row byte-identical. The eight old rows below were re-opened in place (last column unchanged); the two new rows carry their first used-by value.

| Row | used-by old → new | Re-open evidence (2026-10-27 UTC) |
|---|---|---|
| S237 | `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` 05:23:37Z HTTP 200, sha256 `48df2e2f…0801` = row locator = `.ufo/waves/round-42/frozen/src/SHA256SUMS` (`cmp` identical); tag `refs/tags/v7.1^{}` `4ab0e80b…ba8b` unchanged |
| S242 | `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `plain/fs/btrfs/scrub.c?h=v7.2.11` 05:23:37Z 200, `f347931b…a5b8` = row locator = round-44 `SHA256SUMS` (`cmp` identical); `refs/tags/v7.2.11^{}` `a2de78ee…b6ea` unchanged |
| S243 | `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `plain/fs/btrfs/sysfs.c?h=v7.2.11` 05:23:37Z 200, `ce146120…1c43` = row locator = round-44 `SHA256SUMS` (`cmp` identical) |
| S244 | `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `gitlab…/packages/btrfs-progs/-/raw/7.1-1/` 05:23:41Z 200: timer `9a0b6cc2…f8ad`, service `eaa7af92…0252` (= row locators), `PKGBUILD` `3b803e8b…ce98`; all three `cmp` identical to round-44 `frozen/src`; `refs/tags/7.1-1^{}` `0c0a4d77…3e0` unchanged |
| S246 | `corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `lib/cmdline.c` `1af5ad98…ca9d`, `lib/vsprintf.c` `cabb648a…69ca`, `lib/kstrtox.c` `0c52ae02…1ee4` (05:23:40Z, 200) = row locators = round-45 `SHA256SUMS`, `cmp` identical; seat C2ExecLiveSources matched the same three digests (05:22:16Z) |
| S247 | `corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `fs/btrfs/dev-replace.c` 05:23:37Z 200, `f07ef0a0…4f3a` = row locator = round-45 `SHA256SUMS` (`cmp` identical); re-fetch confirmed by C2ExecLiveSources (05:22:16Z) |
| S248 | `corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | live `raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml` 05:23:40Z 200, `44832283…0e72` = row locator = round-45 `SHA256SUMS` (`cmp` identical); `refs/tags/v262^{}` `8cc40e0c…b492` unchanged |
| S249 | `corpus/knowledge/btrfs-scrub-grounding-r45.md` → unchanged | own-work re-run by seat C2ExecHostRecheck 05:21:49Z (`w1/C2ExecHostRecheck/capture-now.txt`): nine value lines equal round-45 `capture.txt` (`f5958a83…1e70`), `diff -u` prints only `captured <timestamp>`; frozen `capture.sh` `c6d2c448…51fc` still matches the row |
| S250 | (new row — no old value) → `corpus/knowledge/census-identity-r46.md` | no old value; live `shell.c` `5f3d539f…f73d`, `general.c` `669ef408…d165`, `general.h` `bf9251e3…f2f2` at `bash-5.3` (05:23:45-47Z, 200) = row locators = round-46 `SHA256SUMS`, `cmp` identical; `refs/tags/bash-5.3` `b8c60bc9…c303`; the locator's lines read as named (`shell.c:1586`, `:1700-1703`, `general.h:252`) |
| S251 | (new row — no old value) → `corpus/knowledge/census-identity-r46.md` | no old value; live page 05:23:41Z 200, `3a50ddef…f27e` = row locator = round-46 `SHA256SUMS` (`cmp` identical); raw lines 72-81 carry "which is a symbolic link to the actual file" and "the file type with the inode" |

Snapshot digests: `sha256sum -c SHA256SUMS` OK 2/2 in `.ufo/waves/round-42/frozen/src`, 5/5 in `round-44`, 5/5 in `round-45`, 4/4 in `round-46`; this round's 15 live re-fetches are `cmp`-identical to those snapshots (15 identical, 0 differ). Tag pins re-resolved the same day and unchanged: `v7.2.11^{}` `a2de78ee…b6ea`, btrfs-progs `v7.1^{}` `4ab0e80b…ba8b`, `v262^{}` `8cc40e0c…b492`, `bash-5.3` `b8c60bc9…c303`, packaging `7.1-1^{}` `0c0a4d77…3e0`. The host still runs the pinned versions (`pacman -Q`: `linux 7.2.11.arch1-1`, `btrfs-progs 7.1-1`, `systemd 262-1`, `bash 5.3.20-1`; bash patches 1-20 sit outside the tag, per `round-46/frozen/src/FETCH.txt`). Receipts: `.ufo/waves/round-46/w1/SrcReopenR45/` (`commands-live.txt`, `sha256-live.txt`, `cmp-live-vs-frozen.txt`, `frozen-check.txt`, `tags-live.txt`, `hostcap-diff.txt`, `col-diff.txt`, `host-packages.txt`).

## 4. Limits — what I did not do

- I did not run `scripts/sources-census.sh validate`; the registry-wide census line belongs to the row/format
  seats, and running it would duplicate their receipt.
- I re-derived no quote line number except the S250/S251 spot lines above; the older rows' line ranges were taken
  from their locator cells and the frozen files by digest, not re-walked line by line.
- The block is bound to `a4477049`. If the L1 amends `corpus/SOURCES.md` during integration, re-run the §1
  command and re-emit the table; the used-by strings would then have to be re-extracted.
- `S250`'s "peeled commit" wording: `bash-5.3` is a lightweight tag (`git ls-remote` prints one line, no `^{}`),
  so `b8c60bc9…` is the commit itself. The row's claim holds; the word "peeled" is loose.

## 5. Adjacent observation (outside this item; no action taken)

`pacman -Q …` on this host prints `error: openai-chatgpt: missing required signature` on stderr before the
requested records. `/etc/pacman.conf:32` carries `Include = /etc/pacman.d/openai-chatgpt.conf`, whose
`/etc/pacman.d/openai-chatgpt.conf:3` defines `[openai-chatgpt]`, and the repo's sync database is accompanied by
`/var/lib/pacman/sync/openai-chatgpt.db.sig` (2026-10-20 23:22) that pacman reports as unverifiable; I did not
inspect the keyring (`/etc/pacman.d/gnupg/` is root-only), so the cause is not established beyond the message.
`-Q` results are unaffected (verified: `pacman -Q bash` prints
`bash 5.3.20-1` after the error line). Flagged for the host-operability/update-safety plane; I did not change any
pacman configuration or database.
