VERDICT: supports

# C2-6 — live re-fetch of the pinned sources, and the Arch packaging patch surface

Seat `C2ExecLiveSources` (round 42, wave w1). Access date for every URL below: **2026-10-26**.
Receipts: `.ufo/waves/round-42/w1/C2ExecLiveSources/`. Scratch used and removed:
`/fast/scratch/hyaku/tsukuroi-r42/C2ExecLiveSources`.

Item verdict, in the three parts the item asks for: (a) both `FETCH.txt` URLs re-fetch to sha256 values
identical to `SHA256SUMS` — **supports**; (b) the tag is the same object at both remotes and is what Arch's
`source=()` names — **supports**; (c) the Arch `btrfs-progs` 7.1-1 packaging applies **no patch at all**, so nothing
can shift the entry's `cmds/scrub.c` line pins — **supports**.

## 1. Re-fetch: both URLs are byte-identical to the frozen digests

`FETCH.txt` names two URLs; I fetched each with `curl -sSfL` on 2026-10-26 and hashed:

| file | re-fetched sha256 | `frozen/src/SHA256SUMS` | match |
|---|---|---|---|
| `cmds/scrub.c` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | `48df2e2f…8f0801` | yes |
| `CHANGES` | `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22` | `bd881ab8…2a0d22` | yes |

Sizes 57034 / 93779 bytes. `cmp` of each re-fetch against the lane's frozen copies exits 0
(`refetch-sha256.txt`: "scrub.c BYTE-IDENTICAL", "CHANGES BYTE-IDENTICAL"), so the receipt chain
`FETCH.txt` → `SHA256SUMS` → frozen file is intact and the snapshots were not altered after the freeze.

URLs (accessed 2026-10-26):
- `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`
- `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/CHANGES`

## 2. Tag identity: `v7.1` is the same commit at GitHub and at git.kernel.org

`git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'` (2026-10-26):

```
0a919c7d6e389c07920675b7fad3f793b92aa78b	refs/tags/v7.1
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b	refs/tags/v7.1^{}
```

`git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git 'refs/tags/v7.1*'` returns the
**same two object names** (annotated tag `0a919c7d…`, peeled commit `4ab0e80b…`) — receipt `tag-resolution.txt`.
This matters because the Arch PKGBUILD builds from git.kernel.org, not GitHub: the GitHub snapshot the entry pins and
the tree Arch compiles are the same commit, so the pinned lines describe the shipped binary's source.

Corroborating: `refetch-CHANGES:1` is `btrfs-progs-7.1 (2026-07-14)`, and the SC5 quote resolves exactly —
`sed -n '468p'` → `* scrub limit: new command to show or set the per-device scrub limits`, matching the entry's
`S238` CHANGES:468 quote verbatim.

Upstream v7 tag set on 2026-10-26: `v7.0` (`9c598743…` peeled), `v7.1` (`4ab0e80b…`), `v7.3` (`afdc3a65…`);
there is no `v7.2` tag.

## 3. Arch packaging at tag 7.1-1: `source=()` carries no patch, and no `.patch` file exists

Packaging repo: `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs`, tag **`7.1-1`** =
commit `0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0`, created `2026-07-15T09:15:06+02:00` (GitLab API, 2026-10-26).
`7.1-1` is the second-newest tag; the newest is `7.3-1` (`a4c3fd32b94e`).

`PKGBUILD` at `?ref=7.1-1`, `source=()` (lines 45-51) — exactly five entries, **none a patch**:

```
source=(
  git+https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git?signed#tag=v${pkgver}
  initcpio-install-btrfs
  initcpio-hook-btrfs
  btrfs-scrub@.service
  btrfs-scrub@.timer
)
```

(`pkgver=7.1`, `pkgrel=1`, `validpgpkeys=('F2B41200C54EFB30380C1756C565D5F9D76D583B') # David Sterba <kdave@kernel.org>`.)
`.SRCINFO` at the same ref lists the identical five `source` lines — receipt `SRCINFO.tag-7.1-1`.

`prepare()` (PKGBUILD:59-70) is the only place patches could apply, and it is a no-op here:

```
for src in "${source[@]}"; do
  src="${src%%::*}"
  src="${src##*/}"
  [[ $src = *.patch ]] || continue
  echo "Applying patch ${src}..."
  patch -Np1 < "../${src}"
done
```

Every one of the five entries fails the `*.patch` test, so `patch` is never invoked.

Two independent confirmations of the same fact:
- Tag tree at `7.1-1` (GitLab `repository/tree?ref=7.1-1`): 12 entries, **zero** `.patch` —
  `packaging-tree-7.1-1.json`.
- Recursive tree of the packaging repo's default branch: 15 entries, **zero** `.patch` —
  `packaging-tree-default-branch.json`. There is no patch file anywhere in this packaging repo.

Integrity of the tag I read: the four non-git sources' `b2sum`s match `PKGBUILD` `b2sums=` slots 2-5 exactly
(`75659665…` install, `0d3c25d0…` hook, `4408d0f8…` service, `9601b319…` timer; receipt
`packaging-source-b2sums.txt`), so the tree I inspected is the real `7.1-1` tree rather than a stale render.
The `git+` slot's `52e892f3…` b2sum is not checkable without a signed clone (see §6).

**Consequence for the entry:** no Arch patch touches `cmds/scrub.c`, so the packaging cannot shift any `S237` line
pin. The entry's line pins describe the source of the binary this host runs.

## 4. Host package state agrees with that reading

`pacman -Qi btrfs-progs` (2026-10-26): `Version : 7.1-1`, `Architecture : x86_64`,
`Build Date : Wed 15 Jul 2026 04:12:52 AM -03` (= 07:12:52 UTC), `Install Date : Sat 03 Oct 2026 05:42:01 PM -03`,
`Packager : Tobias Powalowski <tpowa@archlinux.org>` — receipt `host-package.txt`. `btrfs --version` →
`btrfs-progs v7.1` / `-EXPERIMENTAL -INJECT -STATIC +LZO +ZSTD +UDEV +FSVERITY +ZONED CRYPTO=libgcrypt`.

Two small notes, neither a defect:
- The build stamp (07:12:52 UTC) precedes the packaging-tag commit (09:15:06 +02:00 = 07:15:06 UTC) by 2m14s.
  That is build-then-tag ordering, the normal Arch packaging-repo pattern, not evidence of a differing source.
- `/var/cache/pacman/pkg/btrfs-progs*` is absent, so I could not diff the shipped archive against a local rebuild;
  "no patch" therefore rests on `PKGBUILD` + tree, which is the authoritative statement of how the package is built.
- Weak corroboration that the shipped binary's status-record strings are upstream's: `strings -a /usr/bin/btrfs`
  yields the same literals the v7.1 source emits — `scrub status:1` (= `SCRUB_FILE_VERSION_PREFIX ":"`, scrub.c:69,
  :856), `no stats available` (:321), `devinfo/%llu/scrub_speed_max` (:1215). String presence cannot exclude a
  formatting-level patch, so this supports §3 rather than replacing it.

## 5. The entry's line pins hold against the pristine re-fetch

Sampled 25 `S237` pins from `corpus/knowledge/btrfs-scrub-record-r42.md` and printed those exact lines from the
re-fetched `scrub.c` (`line-pins-verify.txt`). All 25 match the entry's quoted text exactly, e.g.
:67 `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`, :487 `ret = flock(fd, LOCK_EX|LOCK_NB);`,
:534 `ret = rename(datafile_old, datafile_new);`, :856 `ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"`,
:321 `pr_default("\tno stats available\n");`, :1215 `snprintf(path, sizeof(path), "devinfo/%llu/scrub_speed_max", devid);`.

**Upgrade-durability of the pins, quantified.** Current Arch tag is `7.3-1`; host is still `7.1-1`. `cmds/scrub.c`
v7.1 vs v7.3 (`refetch-scrub-73.c`, sha256 `b58942cc…d528`) differs by 4 hunks / 52 diff lines
(`diff-scrub-v7.1-vs-v7.3.diff`): an error-string wording fix at :568, an `i.e.` typo at :1372, and a move of the
scrub-limit reset out of the per-device loop at :1594/:1645. Mapping the 25 sampled pins by exact text into v7.3:
24 of 25 land on the **same** line number; only the `fdres < 0 && fdres != -ENOENT` guard moves :1931 → :1933.
So a host upgrade to 7.3 would break at most one of these pins, not the witness as a whole.

## 6. What I did not do

- Did not verify the `git+` source's b2sum `52e892f3…` (needs a full signed clone of btrfs-progs; the signed-tag
  object identity in §2 is the weaker check I did run).
- Did not run `tools/check-scrub-record-r42.py` or any other counter: this item is source/packaging evidence, not
  the SC-row witness, and the counter's verdict conjunct binds only wave-2 seats.
- Did not reproduce the Arch build (`makepkg`), and the built archive is not cached locally (§4).
- Did not check `diff -u` of the CHANGES file beyond the SC5 pin at :468 (§2).
- No host mutation of any kind; every command above is a read-only fetch, hash, `ls-remote`, `pacman -Qi`,
  `strings`, or file read. No pacman/uv installs were needed.

## 7. Draft for integration — the entry's Limits bullet about packaging patches

The entry currently says (`btrfs-scrub-record-r42.md`, "Limits", first bullet): "…the host runs the Arch build
7.1-1, whose packaging patches were not compared with `cmds/scrub.c` in this entry (wave item; see the round-42
lesson)." This item closes exactly that gap. Proposed replacement (draft, for the L1 to place; keep the file's
wrapping):

```
- Upstream behaviour is pinned at btrfs-progs v7.1 source lines. The host runs the Arch build 7.1-1, whose
  `source=()` holds no patch — five entries (signed `git+…/btrfs-progs.git#tag=v7.1` plus initcpio and unit files),
  none matching `*.patch`, and no `.patch` file exists anywhere in the packaging repo at tag 7.1-1, so `prepare()`'s
  patch loop never runs and `cmds/scrub.c` in the installed binary is pristine v7.1. Checked 2026-10-26: both
  `FETCH.txt` URLs re-fetch to the `SHA256SUMS` digests, and `git ls-remote` reports the same `v7.1` tag object at
  GitHub and git.kernel.org (0a919c7d…, peeled 4ab0e80b…).
```

If the L1 prefers to keep the Limits section free of process, an equally valid alternative is a one-line addition
under SC1 or in a "Sources" note: "The Arch 7.1-1 packaging applies no patch (source=() has five entries, none a
`.patch`), so the installed `scrub.c` is pristine v7.1 — checked 2026-10-26."
