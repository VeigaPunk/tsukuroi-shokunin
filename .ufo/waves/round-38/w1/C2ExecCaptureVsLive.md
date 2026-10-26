VERDICT: supports

# C2-13 — frozen hook capture integrity vs live host, and frozen counter run

Seat: C2ExecCaptureVsLive (leaf, L2 of lane round 38). Read-only on lane content; no package,
service, sysfs or /etc change; no sudo; single scratch root under
`/fast/scratch/hyaku/tsukuroi-r38/C2ExecCaptureVsLive` (created, used, removed — see "Scratch").
Receipts: `.ufo/waves/round-38/w1/C2ExecCaptureVsLive/` (11 files listed at the end).

Capture under test: `.ufo/waves/round-38/frozen/hooks-capture/`
(mtime of `MANIFEST.sha256` = 2026-10-26 01:11:58 -0300; `capture-meta.txt` claims
`# captured 2026-10-26T04:11:58Z host=plazir27 read-only`).

## 1. Manifest self-integrity — PASS

```
$ cd .ufo/waves/round-38/frozen/hooks-capture && sha256sum -c MANIFEST.sha256
… 70 lines, every one ": OK" …            (receipt sha256sum-c.txt, exit 0)
$ sha256sum MANIFEST.sha256
da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd  MANIFEST.sha256
```

* Observed digest equals the expected `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`
  (`receipts/manifest-digest.txt`), equals the constant `MANIFEST_SHA256` at
  `tools/check-hook-order-r38.py:52`, and equals the digest of the copy committed at the
  implementation revision: `git show 1fe28e7:…/MANIFEST.sha256 | sha256sum` →
  `da07f434…ddd701dd` (byte-identical to the worktree copy, `cmp -s` = IDENTICAL).
* `MANIFEST.sha256` has 70 entries (`wc -l` = 70); 0 entries name anything but a `.hook` file.
* Worktree capture is clean at HEAD `5edb6c2e…`: `git status --porcelain -- .ufo/waves/round-38/frozen/hooks-capture`
  printed nothing; 72 files tracked under that path at `1fe28e7` = 70 hooks + `MANIFEST.sha256` + `capture-meta.txt`.
* Counter file digest matches the declared one: `sha256sum tools/check-hook-order-r38.py` →
  `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`.

## 2. Capture vs the host's current .hook set — PASS (names and bytes)

Host now (`find … -maxdepth 1 -type f -name '*.hook'`): `/etc/pacman.d/hooks` = 3 files,
`/usr/share/libalpm/hooks` = 67 files, total 70. `find … ! -type f` in both dirs printed nothing,
so every entry is a regular file (no symlinks or subdirs hiding a hook from `-type f`).

Set comparison against the manifest's 70 relative names (`receipts/live-names.txt` vs
`receipts/manifest-names.txt`):

```
== only-in-live(not captured):      (empty)
== only-in-capture(not live):       (empty)
== identical name sets? YES         counts live=70 manifest=70
```

Byte comparison of every one of the 70 captured files against its live counterpart
(`cmp -s live capture`, loop over all names): `content-diff-any=0` — the capture is not merely
name-complete, it is byte-current.

No extras: `find …/hooks-capture -type f` outside the two data dirs yields exactly
`MANIFEST.sha256` and `capture-meta.txt` (`receipts/capture-files.txt`).

Freshness corroboration: newest live hook mtime is `2026-10-12T12:15:42`
(`/usr/share/libalpm/hooks/{10-openssh-mark-sshd-for-restart,70-openssh-restart-sshd}.hook`),
i.e. 13 days older than the 2026-10-26 capture, so no live hook was written after the capture;
the byte comparison above is the stronger statement and holds regardless of mtime.

One name exists in both dirs — `90-mkinitcpio-install.hook` (`receipts/duplicate-names.txt`),
with different content (`etc` sha256 `a0689d022b3b505d…`, `usr` sha256 `9fc607e81d2f09aa…`).
70 files − 1 shadowed name = 69 effective hooks, which is exactly the counter's
`rows_expected: 69` (counters/check-hook-order-r38.py:117 keeps the first seen name when walking
`reversed(DIRS)` = etc before usr, matching libalpm's "first directory wins" `find_hook` rule stated
in its own docstring, `tools/check-hook-order-r38.py:20-21`).

## 3. Live readability without root — PASS

```
$ stat -c '%A %U:%G %s %n' /etc/pacman.d/hooks/*.hook
-rw-r--r-- root:root 653 /etc/pacman.d/hooks/90-mkinitcpio-install.hook
-rw-r--r-- root:root 302 /etc/pacman.d/hooks/99-limine.hook
-rw-r--r-- root:root 263 /etc/pacman.d/hooks/walker-restart.hook
$ stat -c '%A %U:%G' /usr/share/libalpm/hooks/*.hook | sort | uniq -c
     67 -rw-r--r-- root:root
$ stat -c '%A %U:%G %n' /etc/pacman.d/hooks /usr/share/libalpm/hooks
drwxr-xr-x root:root /etc/pacman.d/hooks
drwxr-xr-x root:root /usr/share/libalpm/hooks
```

All 70 live hooks are `0644 root:root`, both dirs `0755 root:root` — world-readable, so the
capture needs no root. Demonstrated, not just inferred: the whole `sha256sum -c` run, the 70-file
`cmp` loop and `pacman-conf`/`pacman -Q` above were executed as uid `vgpnk` with no elevation
(`id -un` → `vgpnk`). The captured copies are `-rw-r--r-- vgpnk:vgpnk` (dirs `0755 vgpnk:vgpnk`,
`receipts/perms.txt`), so a fresh reader can re-verify them too.

## 4. Frozen counter, one run — PASS, exit 0

```
$ python3 tools/check-hook-order-r38.py --revision 1fe28e725be47364fc6033bf81ecabc66ee5fe62
{
 "counter": "check-hook-order-r38",
 "revision": "1fe28e725be47364fc6033bf81ecabc66ee5fe62",
 "branch_tip": "5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf",
 "predicate": "rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1",
 "entry_present": true,
 "rows_expected": 69,
 "rows_matched": 69,
 "mismatches": 0,
 "extra_rows": 0,
 "source_ok": 1,
 "source_ids": ["S208","S209","S210","S211","S212"],
 "source_problems": [],
 "result": "PASS",
 "exit": 0,
 "missing_rows_first5": [],
 "extra_rows_first5": []
}
EXIT=0
```

Every conjunct of the declared C2 predicate is satisfied on the frozen revision: 69 == 69,
0 mismatches, 0 extras, `source_ok` 1, result PASS. Full record: `receipts/counter-run1.json`.
I ran the counter once as assigned; the three extra runs in §5 are the tamper probes, on a
scratch clone, not repeats of the scoring run.

## 5. The manifest pin is load-bearing (tamper probes, scratch clone)

Cheap control on the "capture_tampered" arm, so the PASS is not obtained by a check that cannot
fail. `D` = `git clone -q --shared <lane>` under scratch, `remote remove origin`,
`git -C $D rev-parse --show-toplevel` == `$D` verified before any use; the frozen lane counter was
pointed at the clone with `--repo $D`. Receipt: `receipts/tamper-probes.txt`.

| probe | mutation in the clone | observed |
|---|---|---|
| 0 | none | `PASS`, exit 0, rows 69/69 |
| 1 | append 1 byte to `etc-pacman.d-hooks/99-limine.hook` | `{"error":"capture_tampered: etc-pacman.d-hooks/99-limine.hook","exit":2}`, exit 2 |
| 2 | add `usr-share-libalpm-hooks/zz-extra.hook` (copy of dbus-reload.hook) | `{"error":"capture_tampered: usr-share-libalpm-hooks/zz-extra.hook","exit":2}`, exit 2 |
| 3 | `git -C $D checkout -- …/hooks-capture` (restore) | `PASS`, exit 0, rows 69/69 |

So a single-byte drift and an extra file both abort scoring at exit 2 before any row is compared,
and a clean tree scores PASS again — the exit-2 arm is reachable and the PASS is a real end state.

## 6. Findings (non-blocking, do not falsify the claim)

F1 — `capture-meta.txt` is outside the integrity chain. It is not an entry of `MANIFEST.sha256`
(`grep -c capture-meta MANIFEST.sha256` = 0) and not referenced by the counter
(`grep -c capture-meta tools/check-hook-order-r38.py` = 0), although it is committed alongside the
capture. Its content can be rewritten without the counter noticing; treat its host/time/pacman-version
lines as unattested provenance, not pinned evidence.

F2 — `capture-meta.txt` records a command whose output is missing and not reproducible as recorded.
The file is 199 bytes / 6 lines and ends at the command line
`$ pacman-conf --verbose 2>/dev/null | grep -i hookdir` with no following output line
(`cat -A …/capture-meta.txt | tail -4`). On this host the same command now prints
`HookDir = /etc/pacman.d/hooks/` (`pacman-conf --verbose` line 5). At capture time either the
command emitted nothing or its output was dropped; either way the HookDir *list* is not actually
evidenced in the capture. The effective order the counter models is instead hardcoded
(`DIRS = (('usr','usr-share-libalpm-hooks'), ('etc','etc-pacman.d-hooks'))`,
`tools/check-hook-order-r38.py:53`), and the host side is consistent with it:
`grep -n -i hookdir /etc/pacman.conf` → no `HookDir` key (no third hook dir configured),
`pacman-conf HookDir` → `/etc/pacman.d/hooks/`, `pacman -Q pacman` →
`pacman 7.1.0.r9.g54d9411-3` (matching the pinned `54d9411` commit in the claim). The capture
therefore does cover every host hook directory that exists — the defect is in the metadata file's
evidence value, not in the captured set.

Nothing else found: capture set, bytes, modes, and the counter's PASS all support C2's capture
integrity and depth claim as frozen.

## 7. Not done / limits

* I did not judge any HO1–HO7 rule row against libalpm source; that is the HO-row seats' item
  (C2RevHookC, C2RevOtherSrc, C2CritHO5, C2CritHO6, C2RevenConf), so this report emits no
  `HO<n>:` lines.
* I did not run `tools/score-storage-arm-r38-*.py` or touch C1 (other seat).
* I did not run the counter against any revision other than `1fe28e7` (and the restored clone),
  did not modify the lane, and installed no tools — the host already had python3/git/coreutils,
  so the tooling authorization was not exercised and there is nothing to record under
  /home/vgpnk/.omp/agent/RULES.md.
* Live dirs were sampled once at seat time (2026-10-26T01:4x -0300 / ~04:4xZ); the byte equality
  above is a point-in-time statement, not a standing invariant.

## 8. Scratch

`/fast/scratch/hyaku/tsukuroi-r38/C2ExecCaptureVsLive` — created with `mkdir -p`, `TMPDIR` exported
there, clone `fx.NVHwuM` removed, final `rm -rf` verified: `test ! -d "$S"` → `scratch-removed=yes`,
and no `C2ExecCaptureVsLive` entry remains under `/fast/scratch/hyaku/tsukuroi-r38/`. No /tmp path
is used as evidence.

## 9. Receipts kept

`.ufo/waves/round-38/w1/C2ExecCaptureVsLive/`: `sha256sum-c.txt`, `manifest-digest.txt`,
`live-names.txt`, `manifest-names.txt`, `capture-files.txt`, `duplicate-names.txt`, `perms.txt`,
`env.txt`, `counter-run1.json`, `tamper-probes.txt`.
