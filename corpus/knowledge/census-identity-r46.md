source: S250 S251 (rows in `corpus/SOURCES.md`; S250 is GNU bash tag bash-5.3 `shell.c`, `general.c` and `general.h`, S251 the Linux man-pages `proc_pid_fd(5)` page; snapshots `.ufo/waves/round-46/frozen/src/`, digests in its `SHA256SUMS`, fetch log `FETCH.txt`)
verified-at: 2026-10-27 (bash tag bash-5.3, peeled commit b8c60bc9ca365f8261fa97900b6fa939f6ebc303; host bash 5.3.20-1; kernel 7.2.11-arch1-1)
recheck: on-release — re-fetch the URLs in `.ufo/waves/round-46/frozen/src/FETCH.txt` and compare `sha256sum` with its `SHA256SUMS`; `bash tools/tsukuroi-census.sh --identity`; `python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>`

# The census identity line, round 46: one command names the census bytes

Scope: the host-census gate of `PROVINCE.md` (`tools/tsukuroi-census.sh`), its own identity. Since round 10 the lane
has re-derived which census produced a verdict with three commands (`md5sum`/`sha256sum`, `wc -l`, `wc -c`) and named
the missing one-command form as debt D12 (`corpus/knowledge/closeout-r11.md:42-44`, `:261-262`). The census `VERSION`
string has stayed `census-v2` through every change since round 3, so the version names nothing: identity is by hash.

## The line

`bash tools/tsukuroi-census.sh --identity` prints one line and exits 0, before any plane probe:

```
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=<64 hex> md5=<32 hex> bytes=<n> lines=<n> planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
```

`lines` counts newline bytes, as `wc -l` does; the census file ends without a newline, so `lines` is one less than the
number of text lines an editor shows. `--identity` takes no other argument: with any other flag the census prints
`--identity takes no other argument` and the usage to stderr and exits 2.

## Which bytes it names, and when it refuses

Bash runs a script file by opening it and moving the descriptor to a high number before reading commands from it
(S250 `shell.c:1586`, `:1700`: `fd = move_to_high_fd (fd, 1, -1);`). With `check_new` set, `move_to_high_fd` walks down
from the descriptor table size, capped at `HIGH_FD_MAX` 256 (`general.h:252`), to the first descriptor that is not in
use (S250 `general.c:690-700`), so the script normally sits on descriptor 255 and on a lower one when 255 is taken or the
descriptor limit is lower. The descriptor is close-on-exec (`shell.c:1703`). Each `/proc/<pid>/fd/<n>` entry is "a
symbolic link to the actual file" (S251 `proc_pid_fd.5.html:75`), and a pipe's entry reads `type:[inode]` instead
(`:80`).

The identity therefore hashes the file through `/proc/$$/fd/<n>`: it tries 255 first, then every descriptor of 10 or
more, and takes the first regular-file entry whose link equals `readlink -f` of the invoked path (`$SELF`). It reads the
sha256 again after md5, bytes and lines, and all four print only when both sha256 reads agree. When no descriptor
qualifies, the four byte fields print `unverifiable` and `verified=no`:

- the script is read from stdin (`bash -s -- --identity < tools/tsukuroi-census.sh`): bash reads commands from
  descriptor 0 (`shell.c:784`) and `BASH_SOURCE[0]` is unset, so `$SELF` is empty (the census now reads
  `${BASH_SOURCE[0]:-}`; before round 46 the stdin form died at line 455 with `BASH_SOURCE[0]: unbound variable`);
- the script comes through a pipe or process substitution (`bash <(cat tools/tsukuroi-census.sh) --identity`): the
  descriptor's link is `pipe:[…]`, not a regular file;
- the invoked file was replaced after bash opened it (the descriptor's link then names the deleted inode, not the
  path), or the descriptor limit puts the script below descriptor 10.

A path is never hashed on trust: a regular file named `bash` in the working directory, which a path-based identity
would hash in the stdin case, is ignored.

## Re-deriving the revision from the line

The line names bytes, not a commit. To find the lane commits whose census has those bytes, without the author:

```
want=<sha256 from the identity line>
git -C <lane> log --format=%H -- tools/tsukuroi-census.sh | while read -r h; do
  [ "$(git -C <lane> show "$h:tools/tsukuroi-census.sh" | sha256sum | cut -d' ' -f1)" = "$want" ] && echo "$h"
done
```

The first hash printed is the newest commit that wrote those bytes; no output means the bytes were never committed
(a local edit).

## Limits

- Bash behaviour is pinned at the tag bash-5.3 source; the host runs 5.3.20, and whether patches 1-20 touch
  `open_shell_script` or `move_to_high_fd` is not checked here [inference: the selftest's descriptor and stdin cases
  pass on the host bash, which is consistent with the pinned lines but does not read the patches].
- The identity names the bytes of the file bash holds open at the moment it runs. Bash reads a script in pieces, so a
  file edited in place while an earlier part was being executed can differ from what ran; the second sha256 read only
  narrows that window. `main "$@"` is the file's last line, so by the time `--identity` runs bash has read the whole
  file once.
- `version` stays the literal `census-v2`; the identity of a revision is the sha256.

## QUALITY check

1. Falsifiable: every rule above names the source line that decides it, and the counter re-derives each field from
   the committed bytes (`tools/score-census-identity-r46.py`).
2. Each external claim cites S250 or S251 with a line in a digest-checked snapshot.
3. `[inference]` marks the one statement the pinned source does not decide (the effect of the host's bash patches).
4. New entry; the census header and SKILL.md gain appended text only.
7. External claims cite tier-A rows (S250 code at a pinned tag, S251 the man-pages project page).
12. No mechanism is tagged unknown for want of a tool.
14. The criteria not listed above, read for applicability: 5, 6, 9, 13 do not apply (no reject in this entry, no
   pacman advice, no negative host claim, no EACCES triage); 8 (header lines present, no `[unknown]`); 10 (the debt
   D12 mentions in `closeout-r11.md` and `plans/` are history and stay; the SKILL.md section of this round points
   here); 11 (the LOG.md round-46 entry lands with this entry).
