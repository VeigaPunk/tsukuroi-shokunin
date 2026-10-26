VERDICT: supports

# C1-5 — hand reproduction of the `boot_inputs_newer` fail-open, without the counter

Seat `C1ExecHandRepro`, round 43 wave 1. Independent of `tools/score-bootinputs-r43.py`: the counter was
**not** run and its code was not consulted for the decision procedure below (only its docstring header
lines 5–6 were read, and only after the reproduction had already produced its result).

Result: the declared defect reproduces exactly as declared — base `0`, fix `1` in the trigger shape;
`1`/`1` with `/etc/crypttab` present; `0`/`0` with nothing newer. Additionally reproduced with an
unprivileged in-namespace uid (both triggers: missing start point, unreadable start point).

## 1. Inputs (exact revisions, extracted verbatim)

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline -1
7d0ed1c2 round-43: C1 after receipt at 717b716; w1 spec and validated dispatch
$ git show 6951ead90566b2d74f7c45b4efca29246badad64:tools/boot-chain-audit.sh > base-boot-chain-audit.sh   # rc=0, 1297 lines
$ git show 717b716a8943151ace8657e0ca23d7d9b8434f26:tools/boot-chain-audit.sh > fix-boot-chain-audit.sh    # rc=0, 1320 lines
$ sha256sum base-boot-chain-audit.sh fix-boot-chain-audit.sh
cd398e603cbd5894b74ca3c28740f2ab3379622a85fc62ac272259d45342930c  base-boot-chain-audit.sh
3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74  fix-boot-chain-audit.sh
$ git diff --quiet 717b716a8943151ace8657e0ca23d7d9b8434f26 HEAD -- tools/boot-chain-audit.sh && echo IDENTICAL
IDENTICAL
$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/boot-chain-audit.sh
3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74  …/tools/boot-chain-audit.sh
```

The "fix" input is byte-identical to the lane worktree at lane tip `7d0ed1c2`, so the 717b716 script is
what ships. Receipt: `.ufo/waves/round-43/w1/C1ExecHandRepro/provenance.txt`.

The whole delta between the two revisions is confined to the declared region (`diff -u`, same receipt):

* new `inputs_newer_than` (fix `tools/boot-chain-audit.sh:463-475`), which decides on
  `hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)` and tests `[ -n "$hit" ]`;
* `boot_inputs_newer` (fix `:477-497`) delegating with the **same 8 start points in the same order**
  (`/etc/fstab  /etc/crypttab  /etc/mkinitcpio.conf  /etc/mkinitcpio.conf.d  /etc/default/limine
  /etc/limine-snapper-sync.conf  /usr/lib/initcpio  /usr/lib/modules`);
* three selftest cases `R43-C1-missing-start-point-none-newer`, `R43-C1-missing-start-point-deep-newer`,
  `R43-C1-all-present-deep-newer` (fix `:1225-1237`, `st_check … 0`, `… 1`, `… 1`).

Base body, verbatim (`base-boot-chain-audit.sh:480-487`):

```
    if find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
        /etc/default/limine /etc/limine-snapper-sync.conf \
        /usr/lib/initcpio /usr/lib/modules \
        -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then
        printf '1\n'
    else
        printf '0\n'
    fi
```

Both files pass `bash -n`. Gate plumbing confirmed: `newer=$(boot_inputs_newer)` at base `:749`, and the
gate conjunct `[ "$newer" = 0 ]` is on base line **761** inside
`if [ "${kernels[i]}" = 1 ] && [ "${sels[i]}" = true ] && [ "$newer" = 0 ] &&`, exactly as the claim
states (fix: `:758` / `:770`). So a wrong `0` does feed BOOTED-OBSERVED.

## 2. Harness (no counter, no lane write)

Both revisions are used as **libraries**: the last line `main "$@"` is deleted
(`sed '$ d'`, and the harness prints the residual count of `^main "$@"$` lines — observed `0` for both),
then each is sourced in the production branch and `boot_inputs_newer` is called and printed. Every leg
prints `fixture_mode=false BOOTCHAIN_FIXTURE=<unset>`, so the fixture shortcut (`boot_inputs_newer`
returning the contents of `<fixture>/boot_inputs_newer`) is provably **not** what was measured — this is
the live path.

Private namespace created per leg by
`/fast/scratch/hyaku/tsukuroi-r43/C1ExecHandRepro/run-leg.sh` (copied to the receipt dir):

* privileged-in-ns leg: `unshare --user --map-root-user --mount /usr/bin/bash ns-leg.sh <scenario>`
* unprivileged-in-ns leg: `unshare --user --map-users=0:1000:1 --map-users=1:100000:65536
  --map-groups=0:1000:1 --map-groups=1:100000:65536 --mount /usr/bin/bash ns-leg.sh <scenario> 65534`,
  the `/etc/subuid` range `vgpnk:100000:65536` mapped, and the call made with
  `setpriv --reuid 65534 --regid 65534 --clear-groups` (`uid=65534` echoed by every such leg).

Inside, first action is `mount --make-rprivate /` (logged `propagation=private`), then
`mount -t tmpfs -o size=32m tmpfs /etc`, `… /usr/lib/initcpio`, `… /usr/lib/modules`. Tool resolution
inside, verified: `find=/usr/bin/find version=find (GNU findutils) 4.11.0-modified`,
`grep=/usr/bin/grep version=grep (GNU grep) 3.12-modified`. Every file _and_ every directory gets
`touch -d @$((btime-5000))` first; only the newer file is then set to `@$((btime+100))`
(`btime=1793027300`, read from `/proc/stat`).

## 3. Legs and outcomes

`transcript.txt` (receipt) is the full log. Measured lines:

```
MEASURE scenario=failopen        uid=0     base got=0   fix got=1
MEASURE scenario=crypttab-known  uid=0     base got=1   fix got=1
MEASURE scenario=nothing-newer   uid=0     base got=0   fix got=0
MEASURE scenario=failopen        setpriv:uid=65534 base got=0   fix got=1
MEASURE scenario=unreadable-dir  setpriv:uid=65534 base got=0   fix got=1
MEASURE scenario=crypttab-known  setpriv:uid=65534 base got=1   fix got=1
MEASURE scenario=nothing-newer   setpriv:uid=65534 base got=0   fix got=0
```

Scenario contents: `/etc/fstab`, `/etc/mkinitcpio.conf`, `/etc/mkinitcpio.conf.d/hosted.conf`,
`/etc/default/limine`, `/etc/limine-snapper-sync.conf`, `/usr/lib/initcpio/install-old` all older than
btime; `/etc/crypttab` absent only in `failopen`; `/usr/lib/modules/7.2.11-arch1-1/modules.dep` newer than
btime. `unreadable-dir` = crypttab present, `modules.dep` newer, `/etc/mkinitcpio.conf.d` mode `700`
owner `0` (`NOTE mkinitcpio.conf.d mode 700 owner 0`).

`failopen`, mechanism, uid 0 (verbatim from receipt):

```
--- find, exactly as both versions invoke it (start points in the script's order)
/usr/lib/modules/7.2.11-arch1-1/modules.dep
FIND_RC=1
--- same find with stderr kept
find: ‘/etc/crypttab’: No such file or directory
/usr/lib/modules/7.2.11-arch1-1/modules.dep
FIND_RC_STDERR=1
--- pipefail demonstration, base form vs fix form
BASE_PIPELINE_RC=1
```

i.e. find **listed** a newer input and exited **1**; the base pipeline therefore read 1 (false) and
`boot_inputs_newer` printed `0` while an input WAS newer. The fix reads stdout and prints `1`.

`crypttab-known`: same find, `FIND_RC=0`, `BASE_PIPELINE_RC=0` → both revisions `1`.
`nothing-newer`: find prints nothing, `FIND_RC=0`, `BASE_PIPELINE_RC=1` (grep finds no line) → both `0`.

Unprivileged uid 65534, `failopen`:

```
diag_uid=65534
find: ‘/etc/crypttab’: No such file or directory
/usr/lib/modules/7.2.11-arch1-1/modules.dep
DIAG_FIND_RC=1
DIAG_PIPELINE_RC=1
```

Unprivileged uid 65534, `unreadable-dir` (second trigger, the "directory is unreadable" half of the claim):

```
diag_uid=65534
find: ‘/etc/mkinitcpio.conf.d’: Permission denied
/usr/lib/modules/7.2.11-arch1-1/modules.dep
DIAG_FIND_RC=1
DIAG_PIPELINE_RC=1
```

Note the same leg's root-run diagnostics print `FIND_RC=0` (root can read the 0700 dir) — the trigger is
privilege-dependent, which is why the unprivileged leg is the informative one.

## 4. Scope refinement (does not falsify, but must not be over-generalised)

The fail-open is **order-dependent inside the 8-point list**, because `-print -quit` stops find as soon as
it matches. With the real binary (`ordering.txt`):

```
$ /usr/bin/find /nonexistent-abc fxtest/d -newermt @1000 -print -quit
/usr/bin/find: ‘/nonexistent-abc’: No such file or directory
fxtest/d/new
rc=1
$ /usr/bin/find fxtest/d /nonexistent-abc -newermt @1000 -print -quit
fxtest/d/new
rc=0
```

So: an erroring start point **earlier** in argument order than the matching one → pipeline false → wrong
`0`. An erroring start point **later** than the match is never reached, so no defect appears. In the real
list `/etc/crypttab` is 2nd and `/usr/lib/initcpio`/`/usr/lib/modules` are 7th/8th, so the realistic
trigger shapes (newer kernel modules or initcpio hooks with crypttab absent, or an unreadable `/etc` boot
input) do fire; a newer `/etc/fstab` alone with crypttab absent would not. The declared wording ("find
exits 1 when a start point is missing or a directory is unreadable … even though grep matched") is
literally what I measured; only "always" would be wrong.

## 5. Current host state (informative, not decisive)

Read-only probe of the 8 start points on this host (`host-state-probe.txt`): all eight exist, `/etc/crypttab`
exists (mode 600 root, not readable by uid 1000 — `find` only stats, so no error), everything else readable
by the unprivileged uid, and
`/usr/bin/find <8 points> -newermt @"$BT" -print -quit` → no output, `rc=0`. Both triggers are therefore
**latent** on the host's present state: the routing is a code-defect route, not a live misreport today.

## 6. Host guard compliance, and what was not done

* Writes: only `.ufo/waves/round-43/w1/C1ExecHandRepro.md` and the receipt dir
  `.ufo/waves/round-43/w1/C1ExecHandRepro/`; scratch under `/fast/scratch/hyaku/tsukuroi-r43/C1ExecHandRepro/`
  (`TMPDIR` exported there), removed at the end.
* No lane mutation: `/etc/crypttab`-style fixtures lived only inside the namespace; after all legs
  `findmnt -no TARGET,FSTYPE,OPTIONS /etc /usr/lib/modules /usr/lib/initcpio` prints nothing (no leftover
  tmpfs), host `/etc/crypttab` is still `600 root`, `/etc/mkinitcpio.conf.d` still `755 root`,
  `git -C lane status --porcelain -- tools corpus SCORECARD.md` is empty, and
  `tools/boot-chain-audit.sh` still hashes `3e5c8763…` (`host-sanity.txt`).
* No mutation of the host at all: no package transaction, no sudo, no service, no mount outside the
  private `unshare` namespaces, no btrfs command of any kind (not even a read-only one), no scrub, no ioctl.
  No signal sent to any process I did not start.
* No tool install or upgrade was performed or needed; `bash 5.3.20`, `util-linux 2.42.4`
  (`unshare`, `setpriv`), `find 4.11.0-modified`, `grep 3.12-modified` were already present and are
  recorded in `host-sanity.txt`.
* **Not done:** the frozen counter `tools/score-bootinputs-r43.py` was not run (deliberately — this item is
  the counter-free reproduction); the script's own `--selftest`/census selftest was not run; the round-42 C1
  counter was not run; the `R43-C1-*` selftest cases were read in the diff but not executed; the
  `BOOTED-OBSERVED` gate was not driven end-to-end (only its `:761` conjunct was read).

## 7. Caveat on shell-level evidence

My first host-level `find` probes in this seat returned `find 0.8.0` and messages of the form
`Error: <path>: … (os error 2)` — that was a **harness builtin** resolved by the agent's persistent shell
(`type -a find` → `find is a shell builtin`), not `/usr/bin/find`. All evidence above was re-taken with the
binary the script actually resolves (`/usr/bin/find`, GNU findutils 4.11.0-modified, confirmed inside the
namespace). Anyone re-running host-level spot checks must call `/usr/bin/find` explicitly.

## 8. Receipts

`.ufo/waves/round-43/w1/C1ExecHandRepro/` —

| file | sha256 | content |
|---|---|---|
| `transcript.txt` | `25092e81a8400f0abe8cc979cc2081b23f9f056e564c3f8a9380f53b289bd930` | all 7 legs, full stdout/stderr |
| `ns-leg.sh` | `830befa2f0a22854224a36c35c50d8b9a152160ecab9fbc3fb2f233c8f64b6a2` | in-namespace driver |
| `run-leg.sh` | `b96f2abfe1b62cc9ca82d9e89429c7c973aaae1b01946db825ff0c9ed625c79c` | namespace launcher |
| `provenance.txt` | `b3aceca09868a35b7fc8cbbb906a812ea2dc5ab4a6a980411ae85e80d5e718a1` | revisions, hashes, `sed '$ d'`, `bash -n`, full `diff -u` |
| `ordering.txt` | `2f8fde2547bce24ae7d3dcc075272e122a97b9a659d3ff649f1bd5301886bb1a` | `-quit` ordering tests with `/usr/bin/find` |
| `host-state-probe.txt` | `55d5764af53d0717f110aaea78fd0ff9d1abf79ec38eb9509ed9908dab282d41` | 8 start points on the live host |
| `host-sanity.txt` | `12d1c54f5364c7668e650c6fd0e256bae9a54704d6cc2d6dcbb5ed137cace7eb` | host untouched, tool provenance |
