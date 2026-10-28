VERDICT: supports

Live `cmds/scrub.c` at btrfs-progs tag v7.1 is byte-identical to pin `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` and to the round-42 snapshot. Cited lines 421, 439, and 1546 match that snapshot, sit outside S237's declared ranges, and are the S237 bullet in the frozen `### Range gaps (R51)` block.

## Re-open

- Access date: 2026-10-28. GET body window `2026-10-28T21:13:18Z`–`2026-10-28T21:13:21Z` (receipts `access-start.txt`, `access-end.txt`). A following HEAD of the same URL returned `HTTP/2 200`, `content-length: 57034`, `date: Wed, 28 Oct 2026 21:13:21 GMT`.
- URL: `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` (the URL named for this seat; the same URL is recorded at `.ufo/waves/round-42/frozen/src/FETCH.txt:2`).
- Command: `curl -sSfL --max-time 120` of that URL, `curl_rc=0`. Body `57034` bytes, `2231` lines. `sha256sum` of the body: `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`.
- Pin match: that digest is the S237 anchor digest at freeze `2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md:246`, line 1 of `.ufo/waves/round-42/frozen/src/SHA256SUMS`, and `sha256sum` of `.ufo/waves/round-42/frozen/src/scrub.c` (`57034` bytes, `2231` lines).
- `cmp -s` of the live body against that snapshot exited 0. A second hash of both files in the receipt `line-compare.txt` reports `byte_identical=True` and `pin_match=True`.

## Cited lines

Anchor cell at `2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md:246`: `tag v7.1 (peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b), cmds/scrub.c lines 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945; raw bytes sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`.

Live line equals the same snapshot line for each cite (`line-compare.txt`):

- 421, outside (after 280-330, before 446-535). Live bytes `b'\tret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);'` (5 words after the tab).
- 439, outside (same gap). Live bytes `b'\t\t.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,'` (9 words).
- 1546, outside (after 1498-1512, before 1925-1945). Live bytes `b'\tscrub_handle_sigint_child(fdmnt);'` (1 word).

GR3 rests on these three. Freeze `2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md:193-194` cites `scrub.c:1546` and `:439` for the SIGINT handler and says that handler issues `BTRFS_IOC_SCRUB_CANCEL`. The quotes are at lines 216, 218, and 220, and each quote is the live line with its leading tab(s) removed.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` exited 0. Its S237 line is `emit-gaps.txt:3`: `S237 scrub.c: 421, 439, 1546`. The emitted block equals the frozen entry's `### Range gaps (R51)` at `btrfs-scrub-grounding-r45.md:269-275` (compared line-for-line; equal).

## Gate

- Access date: 2026-10-28
- URL: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c
- sha256: 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801
- Quote, live `cmds/scrub.c:421` (5 words), the cancel GR3 quotes at `btrfs-scrub-grounding-r45.md:216`: `ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`

The live line is a leading tab followed by that text.

## Not done

`cmp` exited 0, so no differing-line diff was produced. The v7.1 tag peel was not re-resolved; this seat fetched the raw URL the item names. No tool was installed. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS237` was removed after the receipts above were copied.
