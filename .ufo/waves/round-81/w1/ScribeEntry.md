# ScribeEntry — prose audit of the C1 entry (round 81, w1)

Scope: `corpus/knowledge/mount-unit-fstab-plane-r81.md` ("What this host does with it", Limits, provenance trio,
recheck) against `.ufo/waves/round-81/before/host/generator.txt`. Read-only. No production file edited. No git/jj
mutation. No task dispatch. Tables and receipts: `w1/ScribeEntry/audit.md` and `w1/ScribeEntry/receipts.txt`.

## Verdict

The entry is not ready to be cited. The counter's own result is real (selftest 6/6; fixture run `"count": 8,
"target": 8, "finding": "met"`), but the prose around it contains a wrong count, a self-contradicted claim, a
wrong-unit measured leg, and unmarked inferences. The recheck cannot pass at any landed revision today, because
the entry, its JSON and the S331/S332 registry rows are uncommitted.

Of 13 factual sentences in "What this host does with it": 3 SUPPORTED (2, 4, 10), 2 supported-but-incomplete or
partly so (3, 9 with the fstab side live-only), 1 PARTIAL (6, omission), 1 PARTIAL (7, split yes, "on this boot" no),
1 claim right but citation wrong (8), 1 PARTIAL-overclaim (5), 2 CONTRADICTED (1, 11), 2 UNSUPPORTED (12, 13).
Full table: audit.md §1.

## Findings (scoped)

1. **Counts wrong (H).** The entry says six local file systems, four required. fstab has seven local rows: five
   required (`/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`, `/boot`) and two nofail (`/tmp`, `/fast`). The
   generator agrees with five (`local-fs.target.requires`, generator.txt 140–145). The S332 registry row repeats
   the error ("four required mounts"). [R8, R10]
2. **Self-contradicted Options claim (H).** "The generated Options= line … drops the x-systemd.* tokens" is false for
   `/tmp`: tmp.mount Options (generator.txt 77) still carries `x-systemd.before=local-fs.target`. Only the
   device-timeout token is dropped. [R10]
3. **Wrong timing (H).** "Measured on this boot" and Limits' "one boot's generator output" are contradicted. The
   generator files are stamped 2026-11-04 17:34:49; the system booted 2026-11-02 12:07:17. The output is a later
   regeneration whose cause is unknown. [R7]
4. **Wrong citation (M).** "tmp.mount … fast.mount is not (S332 :35–47 vs :95–107)": 95–107 is `var-log.mount`. The
   tmp block (64–77, Before= at 70) is never cited. [R10]
5. **Measured leg of MT5 is the wrong unit (M).** S332 99–100 is `var-log.mount`'s default Before=local-fs.target,
   not the x-systemd.before effect. The counter's R7 test is substring-only and passes it anyway. [R13]
6. **Unmarked inference (M).** "Still delays local-fs.target by up to the device timeout" and "up to ten seconds
   for /tmp, nothing for /fast" are stated as fact. No test supports them. "Nofail bounds waiting" also conflicts
   with S331's "boot continues without waiting". [audit row 12–13]
7. **Overclaim (M).** "Matches the documentation row for row": the host exercises only MT1 (partly), MT2, MT5, MT6.
   MT3, MT4, MT7, MT8 have no instance (no noauto, automount, requires/wants or wanted-by in fstab or the generator
   output). [R8, R10]
8. **Anchor convention undisclosed (M).** MT anchors use tag-stripped token numbering, but the entry and S331 call
   them "v262 upstream lines". Raw-file numbering puts MT1 at 135–138 and MT4 at 491–492, outside their cited
   windows. The r79 sibling discloses this convention (`systemd-dependency-propagation-r79.md:25-29`); r81 does not.
   [R12]
9. **fstab side unpersisted (M).** `/etc/fstab` is in no receipt. Every fstab-side sentence (rows 1–4, 9) rests on a
   live read that the entry does not cite. [R8]
10. **Not committed; recheck not runnable (M, operability).** The entry `.md`/`.json` are untracked; S331/S332 are
    only in the worktree SOURCES.md (HEAD has 0). The counter at HEAD `e8e5d5b3` and at the declaration commit
    `8023711` prints `note-absent` and exits 1. `<REV>` is not defined in the entry. [R3, R4, R5]
11. **Recheck cannot detect its trigger (M, freshness).** The counter reads only the pinned snapshot and its
    SHA256SUMS; it never re-fetches upstream. A new systemd release would not change its output. [R6; counter
    `verify()`]
12. **Limits incomplete (L).** Not named as declined: `x-systemd.wants-mounts-for=`/`requires-mounts-for=`,
    `x-systemd.device-bound=`, `x-systemd.idle-timeout=`, `x-systemd.rw-only`, `_netdev`, `ReadWriteOnly=`,
    `TimeoutSec=`, the unit-file keys, the swap row (fstab 22) and the tmpfs `/dev/shm` row (fstab 30, no unit
    generated). [audit §2]
13. **Omission in the wants sentence (L).** `systemd-remount-fs.service` is in `local-fs.target.wants` (138) and
    not mentioned.

Confirmed correct: the upstream snapshot digest (`afbf3be6…2394`) matches a fresh fetch today; the host runs
systemd 262.1-1-arch; the `source:`/`verified-at:`/`recheck:` header keys are at column 0 with an ISO date and an
on-release cadence; the device.d drop-ins (generator 121–134) support the device-timeout sentence; the requires
list (140–145) and fast/tmp Options differ by exactly `x-systemd.before=local-fs.target`; every quote is located
inside its cited window under tag-stripped numbering.

## Counter and recheck runs (exact outputs in receipts.txt)

- `count-mount-rows-r81.py --selftest` → `SELFTEST total=6 passed=6 failed=0`, rc 0 (R1).
- Fixture of the working-tree bytes → `{"claim": "C1", "revision": "fixture", "count": 8, "target": 8, "finding": "met", "problems": []}`, rc 0. The recheck's expected substring matches this format (R2).
- `--revision e8e5d5b3…` and `--revision 8023711…` → `note-absent`, rc 1 (R3). `--revision HEAD` → E-REVISION-INVALID, rc 2 (the counter requires hex).

## Scope limits and unknowns

- Cause of the 2026-11-04 17:34:49 generator regeneration: UNKNOWN. No unit operation or reload was run by me.
- Whether that output equals the 2026-11-02 boot's generation: [INFERENCE] (fstab mtime 2026-10-20 09:48:47 suggests
  yes). Not measured.
- Knowledge-header and registry-coverage gates: not run (entry is untracked, they read committed revisions).
- No boot, device-removal or unit test (none in scope). I did not verify the entry against the installed Arch build
  sources (QUALITY 103).
- Git: read-only only (`log`, `status`, `show`, `ls-files`, `rev-parse`, `remote -v`, `branch -a`). No mutation.

## Tooling record

No tool was installed, upgraded or removed. Available tools used: `python3`, `curl`, `git`, `systemctl --version`.
One read-only query: `pacman -Q systemd` (a query, not a transaction; pacman is paused host-wide). Nothing was
written to `~/.local/bin` or any PATH directory.

## Artifacts

- `.ufo/waves/round-81/w1/ScribeEntry/audit.md` — sentence→line-range table, Limits check, provenance trio, defects D1–D15.
- `.ufo/waves/round-81/w1/ScribeEntry/receipts.txt` — R1–R14 verbatim outputs.
- This report: `.ufo/waves/round-81/w1/ScribeEntry.md`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r81/ScribeEntry` removed before yield (see final command receipt).
