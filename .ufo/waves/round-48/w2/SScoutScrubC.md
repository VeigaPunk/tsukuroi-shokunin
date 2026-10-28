VERDICT: supports

# SRC-SScoutScrubC — live re-open of S237 and S242 (round 48, wave w2)

Access date (UTC): 2026-10-28. Scratch: /fast/scratch/hyaku/tsukuroi-r48/SScoutScrubC (removed on finish). Receipts: this dir holds the fetched bytes as `s237-scrub.c` and `s242-scrub.c`.

## (1) Fetches, digests, byte-identity

### S237 — btrfs-progs v7.1 cmds/scrub.c (SOURCES.md:246)
- Row URL: https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (HTML view); raw fetch URL per the round-42 FETCH.txt: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c
- Fetch: `curl -fsSL --max-time 60 -o s237-scrub.c <raw URL>` — succeeded, no redirect of note (raw host serves directly).
- sha256 of fetched bytes: `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — equals the row pin and `.ufo/waves/round-42/frozen/src/SHA256SUMS`.
- `cmp s237-scrub.c .ufo/waves/round-42/frozen/src/scrub.c` → identical (exit 0). Fetched file is 2231 lines.
- Tag check: `git ls-remote https://github.com/kdave/btrfs-progs 'refs/tags/v7.1*'` → `0a919c7d6e389c07920675b7fad3f793b92aa78b refs/tags/v7.1`, peeled `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` — the peeled commit matches the row exactly. The pin is an annotated tag, not a branch tip; nothing moved.

### S242 — Linux v7.2.11 fs/btrfs/scrub.c (SOURCES.md:251)
- Row URL (HTML view): https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11; raw fetch URL per the round-44 FETCH.txt: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11
- Fetch: `curl -fsSL --max-time 60 -o s242-scrub.c <plain URL>` — succeeded.
- sha256 of fetched bytes: `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` — equals the row pin and `.ufo/waves/round-44/frozen/src/SHA256SUMS`.
- `cmp s242-scrub.c .ufo/waves/round-44/frozen/src/scrub.c` → identical (exit 0). Fetched file is 3337 lines.
- Tag check: `git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'refs/tags/v7.2.11*'` → `8316c24ec1b77dba19ba072ca4fe251b36dc65d3 refs/tags/v7.2.11`, peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` — matches the row. Tag, not a moving branch; nothing moved.

## (2) Anchors located in the LIVE bytes

Item-specified anchors (S242 live file, same line numbers as the snapshot since bytes are identical):

- scrub.c:3094-3095 —
  > `if (btrfs_fs_closing(fs_info))` / `return -EAGAIN;`
- scrub.c:3147-3153 (`-EINPROGRESS` refusal block) —
  > `if (dev->scrub_ctx ||` … `btrfs_dev_replace_is_ongoing(&fs_info->dev_replace))) {` … `ret = -EINPROGRESS; goto out;`

Row-listed S242 ranges (1365-1385, 3140-3162, 3215-3226, 3321-3337): all inside the 3337-line live file; the 3140-3162 range contains the refusal block above.

S237 anchors (byte-identical file, so row line numbers hold; spot-checked):
- cmds/scrub.c:67-70 —
  > `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` / `#define SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"` / `#define SCRUB_FILE_VERSION "1"`
- cmds/scrub.c:826-830 —
  > `#define _SCRUB_KVWRITE(fd, buf, name, use)` …
- cmds/scrub.c:1925-1930 —
  > `ret = connect(fdres, (struct sockaddr *)&addr, sizeof(addr));` … `fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid);`

## (3) Cadence and pins

Both rows pin immutable annotated tags (verified peeled commits unchanged), `on-release` recheck remains correct — the bytes can only change if a tag is re-pointed, which did not happen; the pins, line anchors and sha256 values in both rows still read exactly right as of 2026-10-28.

## (4) Proposed cell updates

S237: `no change`.
S242: `no change`.
