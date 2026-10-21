## Attack
Axis: persistent repository-state residue. I tested whether the C1 adjacency gate's `--selftest` leaves a worktree/index/ref/ignored-file change or an unremoved fixture behind in a fresh clone of the attacked revision. Any such residue would falsify the selftest-safety claim.

## Method
- Cloned the lane without hardlinks or checkout, then detached at the attacked revision:
  ```sh
  git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/r19-fxexec-selftestadj-4c8e2b1f
  git -C /tmp/r19-fxexec-selftestadj-4c8e2b1f checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
  ```
- Before testing in `/tmp/r19-fxexec-selftestadj-4c8e2b1f`, `git status --porcelain --ignored` emitted no lines and exited 0; `git rev-parse HEAD` returned `8e5916360f2dfe7bc4eb4ba144081af555900116`.
- Captured an lstat/content-hash manifest of the whole clone (including `.git`) before and immediately after the canonical selftest, then compared them:
  ```sh
  python3 /tmp/r19-fxexec-selftestadj-ctl/manifest.py /tmp/r19-fxexec-selftestadj-4c8e2b1f /tmp/r19-fxexec-selftestadj-ctl/M0.json && python3 tools/check-adjacency-anchors.py --selftest > /tmp/r19-fxexec-selftestadj-ctl/runA.stdout 2> /tmp/r19-fxexec-selftestadj-ctl/runA.stderr; echo "exit=$?"
  python3 /tmp/r19-fxexec-selftestadj-ctl/manifest.py /tmp/r19-fxexec-selftestadj-4c8e2b1f /tmp/r19-fxexec-selftestadj-ctl/M1.json && cmp /tmp/r19-fxexec-selftestadj-ctl/M0.json /tmp/r19-fxexec-selftestadj-ctl/M1.json; echo "cmp_exit=$?"
  ```
- Repeated the test under `strace` in a second clone checked out at the same revision and made read-only with `chmod -R a-w /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f`. Captured a pre/post manifest and compared them. The complete traced invocation was:
  ```sh
  strace -f -s 512 -e trace=openat,openat2,open,creat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,link,linkat,symlink,symlinkat,chmod,fchmodat,utimensat,truncate,ftruncate,chown,fchownat,mknodat,execve -o /tmp/r19-fxexec-selftestadj-ctl/strace-C-ro.log python3 tools/check-adjacency-anchors.py --selftest > /tmp/r19-fxexec-selftestadj-ctl/runC.stdout 2> /tmp/r19-fxexec-selftestadj-ctl/runC.stderr; echo "exit=$?"
  ```
- The second clone setup and read-only change were:
  ```sh
  git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f && git -C /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
  chmod -R a-w /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f && python3 /tmp/r19-fxexec-selftestadj-ctl/manifest.py /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f /tmp/r19-fxexec-selftestadj-ctl/M0-ro.json; echo "exit=$?"
  python3 /tmp/r19-fxexec-selftestadj-ctl/manifest.py /tmp/r19-fxexec-selftestadj-ro-4c8e2b1f /tmp/r19-fxexec-selftestadj-ctl/M1-ro.json && cmp /tmp/r19-fxexec-selftestadj-ctl/M0-ro.json /tmp/r19-fxexec-selftestadj-ctl/M1-ro.json; printf 'manifest_cmp_exit=%s\n' "$?"
  ```
- Exact traced invocation in the first clone (`runB`):
  ```sh
  strace -f -s 512 -e trace=openat,openat2,open,creat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,link,linkat,symlink,symlinkat,chmod,fchmodat,utimensat,truncate,ftruncate,chown,fchownat,mknodat,execve -o /tmp/r19-fxexec-selftestadj-ctl/strace-B.log python3 tools/check-adjacency-anchors.py --selftest > /tmp/r19-fxexec-selftestadj-ctl/runB.stdout 2> /tmp/r19-fxexec-selftestadj-ctl/runB.stderr; echo "exit=$?"
  ```

## Verdict
CONFIRM — C1 selftest-safety attack. The canonical selftest passed and the immediate before/after full-clone manifests matched exactly. The read-only-clone run also passed with identical pre/post manifests. This confirms only the assigned no-residue attack, not the substantive adjacency claim.

## Evidence
- `runA.stdout`: exact output `PASS (12 cases, 12 passed, 0 failed)`; shell exit output `exit=0`; `runA.stderr` was empty.
- First clone manifest command reported `entries=4115` both before and after; `cmp` returned `cmp_exit=0`.
- `runB.stdout`: exact output `PASS (12 cases, 12 passed, 0 failed)`; shell exit output `exit=0`; `runB.stderr` was empty. Grepping `strace-B.log` for write-mode opens or mutating path syscalls against `/tmp/r19-fxexec-selftestadj-4c8e2b1f` returned “No matches found”. Grepping that trace for the live lane path also returned “No matches found”.
- `runC.stdout`: exact output `PASS (12 cases, 12 passed, 0 failed)`; shell exit output `exit=0`; `runC.stderr` was empty. The read-only clone manifests each reported 4115 entries and compared with `cmp_exit=0`. Greps of `strace-C-ro.log` for write-mode opens/mutating syscalls against the read-only clone and for the live lane path both returned “No matches found”.
- In the traced test, fixture writes were confined to `/tmp/check-adjacency-anchors-m6o_ap6j/fixture-repo`; the trace records `rmdir("/tmp/check-adjacency-anchors-m6o_ap6j") = 0`. A subsequent `/tmp/check-adjacency-anchors-*` glob found no files.
- Source at `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-adjacency-anchors.py:13` disables bytecode writes. At `:716-742`, selftest switches `ROOT` to a `TemporaryDirectory` fixture; at `:851-852`, it restores `ROOT`; at `:858-859`, it prints the PASS summary and returns success.
- Post-test `git status --porcelain --ignored` emitted no lines and exited 0; `git rev-parse HEAD` still returned `8e5916360f2dfe7bc4eb4ba144081af555900116`; `git for-each-ref` retained the same three refs at `2fd1e6768f187be8c5e837af6286c3736953fcff` as in the pre-test listing.

## Residual
A later whole-clone manifest (`M2`), taken after the second run and the follow-up `git status`/`rev-parse`/`for-each-ref` inspections, differed from `M0` only in `.git` directory `mtime_ns` and `ctime_ns`; the `diff -u` showed no changed child entries. Because M2 was taken after those inspection commands rather than immediately after runB, I cannot attribute that directory-metadata change to one command. Porcelain status, HEAD, refs, and the runB trace showed no persistent file/ref change. The fixture was temporary; no boot or host action was performed.

Scope: executed=git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/r19-fxexec-selftestadj-4c8e2b1f; git -C /tmp/r19-fxexec-selftestadj-4c8e2b1f checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 tools/check-adjacency-anchors.py --selftest; strace -f -s 512 -e trace=openat,openat2,open,creat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,link,linkat,symlink,symlinkat,chmod,fchmodat,utimensat,truncate,ftruncate,chown,fchownat,mknodat,execve -o /tmp/r19-fxexec-selftestadj-ctl/strace-B.log python3 tools/check-adjacency-anchors.py --selftest; git status --porcelain --ignored; git rev-parse HEAD; git for-each-ref; cmp /tmp/r19-fxexec-selftestadj-ctl/M0.json /tmp/r19-fxexec-selftestadj-ctl/M1.json; cmp /tmp/r19-fxexec-selftestadj-ctl/M0-ro.json /tmp/r19-fxexec-selftestadj-ctl/M1-ro.json; strace -f -s 512 -e trace=openat,openat2,open,creat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,link,linkat,symlink,symlinkat,chmod,fchmodat,utimensat,truncate,ftruncate,chown,fchownat,mknodat,execve -o /tmp/r19-fxexec-selftestadj-ctl/strace-C-ro.log python3 tools/check-adjacency-anchors.py --selftest