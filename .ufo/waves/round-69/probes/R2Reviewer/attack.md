2026-11-03T23:34:08Z
# R2Reviewer — operability / C2 adversarial review

Reviewed draft sha256 4a6daf43ee9cc701c40625f1e2844fe73b7853973795c0a51b17dd4843b7c36d, copied into the one shared sandbox clone. Recommendation only, not integration/admission.

## HIGH — Numeric taint input can abort the entire census or fabricate a decode
`tools/tsukuroi-census.sh:2313-2328` accepts any digit string, compares with Bash integer `test`, then interprets it in Bash arithmetic without bounded decimal normalization. `08` passes the digit guard but aborts at line 2326 as invalid octal; neither KERNEL nor the canonical rollup prints. `00` emits an empty taint_bits value instead of none. A huge decimal fails the range comparison and then overflows into a bogus all-bits decode instead of UNKNOWN. This violates verdict-neutral emission and the closed-table contract. Normalize bounded decimal input before arithmetic, or reject unsupported numeric representations with UNKNOWN without terminating the caller.

```text
$ printf '08\n' > /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-08; TSUKUROI_KERNEL_TAINTED=/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-08 bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh
[excerpt]
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0
INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0
/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh: line 2326: 08: value too great for base (error token is "08")
rc=1

$ printf '00\n' > /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-00; TSUKUROI_KERNEL_TAINTED=/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-00 bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh
[excerpt]
INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=00 taint_bits= pending=NO unreadable=0 detail=qo:multi-owner
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
rc=1

$ printf '99999999999999999999999999999999999999\n' > /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-99999999999999999999999999999999999999; TSUKUROI_KERNEL_TAINTED=/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/taint-99999999999999999999999999999999999999 bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh
[excerpt]
INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=99999999999999999999999999999999999999 taint_bits=P,F,S,R,M,B,U,D,A,W,C,I,O,E,L,K,X,T,N,J pending=NO unreadable=0 detail=qo:multi-owner
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh: line 2321: [: 99999999999999999999999999999999999999: integer expected
rc=1

```

## MED — Fixture-only behavior remains an uncovered test channel (coverage risk, not observed gating)
Channel: `TSUKUROI_FIXTURE`, plus kernel override path identities. Child census executions inherit the marker in `base_env`; `check` runs the ordinary script against these marked paths. A variant branching on marker presence could implement correct fixture behavior and incorrect default behavior without these fixture cases detecting it. Code inspection of `probe_kernel_arm` found no marker/path-provenance branch in this draft. No mutant was made (reviewer is read-only). The successful live run provides separate evidence, not proof against all fixture-only variants.

## LOW / verification gaps
The requested R2_FIELDS denominator is seven, but the canonical line declares eight required key=value fields. Observed all eight once in exact order; compatibility summary below counts the first seven as 7/7 and explicitly verifies unreadable separately. Optional detail appears once.
Language-server device unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; references/definitions/diagnostics unavailable. Text inspection is a literal fallback, not semantic proof.
Numeric edge finding concerns supplied/abnormal numeric input; the normal procfs value on this host is decoded correctly. No privilege, installs, package transactions, tracked-lane writes, or runtime rerouting performed.

## Canonical selftest and live run
```text
$ TMPDIR=/fast/scratch/hyaku/tsukuroi-r69/R2Reviewer bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh --selftest
[excerpt; tool exit code 0]
TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0 failed)
rc=0
$ bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh
[excerpt from neutrality live run]
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
rc=1
```
Exactly one KERNEL line after INITRAMFS and before the rollup. Required key order: release,pkg,pkgver,modules_tree,tainted,taint_bits,pending,unreadable. All once. No rollup term added.

## Neutrality comparison
Normal live neutrality: YES (not unconditional; numeric abort above disproves universal neutrality).
Every differing line classified: header timestamp; drivers memory/cgroup/PSI/swap counters; journal error/coredump counts; HANDOFF coredump count; the new KERNEL line. No other difference. Rollup identical, both exit 1. Full diff and inventory:
```text
$ bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/neutral.sh /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer
patched_live_rc=1
base_live_rc=1
--- diff (base -> patched), normalized header timestamp ---
4,5c4,5
< PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=100 (oom=0 io=95 gpu=0 other=5) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=5 C3_sigkill=25; C4_sweep=220 C4_present=4[user.slice,user.slice/user-1000.slice,user.slice/user-1000.slice/user@1000.service/app.slice] C4_local=0; C5_swap_fail=22847614 C5_swap_peak_pct=99% C5_pswp=37686445/73992508 C5_sock_throttled=271730; C6_psi_some_avg300=0.49 C6_psi_full_avg300=0.49 C6_psi_full_total_us=653533498 C6_avail_kb=23455836 C6_shmem_kb=4668; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
< PLANE journal: DEGRADED (boots=3 current=yes target=graphical.target:active err=5390 (coredump=58 kernel=100 other=5232); failedhist=5231[ai-usage.service,app.slice,comfyui.service,init.scope,-.slice,user@1000.service]; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
---
> PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=100 (oom=0 io=95 gpu=0 other=5) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=5 C3_sigkill=25; C4_sweep=226 C4_present=4[user.slice,user.slice/user-1000.slice,user.slice/user-1000.slice/user@1000.service/app.slice] C4_local=0; C5_swap_fail=22847621 C5_swap_peak_pct=99% C5_pswp=37713625/74054998 C5_sock_throttled=279604; C6_psi_some_avg300=1.69 C6_psi_full_avg300=1.69 C6_psi_full_total_us=663294200 C6_avail_kb=24194016 C6_shmem_kb=1644; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
> PLANE journal: DEGRADED (boots=3 current=yes target=graphical.target:active err=5421 (coredump=89 kernel=100 other=5232); failedhist=5231[ai-usage.service,app.slice,comfyui.service,init.scope,-.slice,user@1000.service]; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
9c9
< HANDOFF ADJ-04 mori class=coredumps value=58 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
---
> HANDOFF ADJ-04 mori class=coredumps value=89 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
13a14
> KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner
--- raw diff ---
1c1
< tsukuroi-census census-v2 — host=plazir27 — 2026-11-03T23:20:14Z — read-only
---
> tsukuroi-census census-v2 — host=plazir27 — 2026-11-03T23:31:37Z — read-only
4,5c4,5
< PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=100 (oom=0 io=95 gpu=0 other=5) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=5 C3_sigkill=25; C4_sweep=220 C4_present=4[user.slice,user.slice/user-1000.slice,user.slice/user-1000.slice/user@1000.service/app.slice] C4_local=0; C5_swap_fail=22847614 C5_swap_peak_pct=99% C5_pswp=37686445/73992508 C5_sock_throttled=271730; C6_psi_some_avg300=0.49 C6_psi_full_avg300=0.49 C6_psi_full_total_us=653533498 C6_avail_kb=23455836 C6_shmem_kb=4668; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
< PLANE journal: DEGRADED (boots=3 current=yes target=graphical.target:active err=5390 (coredump=58 kernel=100 other=5232); failedhist=5231[ai-usage.service,app.slice,comfyui.service,init.scope,-.slice,user@1000.service]; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
---
> PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=100 (oom=0 io=95 gpu=0 other=5) [unknown: accepted noise floor]; nvidia=present smi=615.78.08 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=0 C2_sysd_oom=5 C3_sigkill=25; C4_sweep=226 C4_present=4[user.slice,user.slice/user-1000.slice,user.slice/user-1000.slice/user@1000.service/app.slice] C4_local=0; C5_swap_fail=22847621 C5_swap_peak_pct=99% C5_pswp=37713625/74054998 C5_sock_throttled=279604; C6_psi_some_avg300=1.69 C6_psi_full_avg300=1.69 C6_psi_full_total_us=663294200 C6_avail_kb=24194016 C6_shmem_kb=1644; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
> PLANE journal: DEGRADED (boots=3 current=yes target=graphical.target:active err=5421 (coredump=89 kernel=100 other=5232); failedhist=5231[ai-usage.service,app.slice,comfyui.service,init.scope,-.slice,user@1000.service]; timers_enabled=2 timers_scanned=2 armed=2 timer_drift=0 timer_unknown=0)
9c9
< HANDOFF ADJ-04 mori class=coredumps value=58 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
---
> HANDOFF ADJ-04 mori class=coredumps value=89 kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER
13a14
> KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner
--- line-type counts base/patched ---
[base]
  tsukuroi-census  1
  PLANE            6
  HANDOFF          2
  DRIFT            1
  STORAGE          1
  SCRUB            1
  INITRAMFS        1
  KERNEL           0
  TSUKUROI_CENSUS: 1
[patched]
  tsukuroi-census  1
  PLANE            6
  HANDOFF          2
  DRIFT            1
  STORAGE          1
  SCRUB            1
  INITRAMFS        1
  KERNEL           1
  TSUKUROI_CENSUS: 1

rc=0

```
Base extraction/run commands: `$ git -C /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone show acce353bacad74043636018d829e9e9b8e0fdf1c:tools/tsukuroi-census.sh > /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/base.sh` (rc=0); base/HEAD tools identical (`git diff --quiet ... -- tools/tsukuroi-census.sh`, rc=0); `$ bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh` before overlay (rc=1). Base selftest observed PASS (177 cases, 177 passed, 0 failed), rc=0.

## Fixture results and reproducible harness
All requested fixtures exercised. Absent/empty release and garbage/negative taint produce honest UNKNOWN. File-as-modules produces UNKNOWN and unreadable=1. Failed pacman produces UNKNOWN. Unexpected owner is echoed as evilmc, not guessed linux. Every fixture census exits 2 because the deliberately narrow pacman stub blocks unrelated package probes; this is not a KERNEL verdict.
Initial harness omitted STUB_QO/STUB_QORC from env, so initial ownership observations were invalidated and discarded. The corrected run below is authoritative.

```bash
# harness.sh
#!/usr/bin/env bash
# R2Reviewer — C2 KERNEL-arm attack harness. Usage: attack.sh <census.sh> <outdir>
# Convention per case: fixture dir $OUT/fx/<name> with:
#   ko=  osrelease file content | ABSENT | EMPTY | UNREADABLE
#   kt=  tainted file content   | ABSENT | EMPTY | UNREADABLE
#   km=  DIR        -> override TSUKUROI_KERNEL_MODULES to an existing fixture dir
#      DEFAULT     -> leave override unset (arm derives /usr/lib/modules/<release>)
#   qo=  pacman -Qo stdout lines; qorc=N stub exit code (default 0)
set -u
CEN=$(readlink -f "$1"); OUT=$(readlink -f "$2"); mkdir -p "$OUT"; BIN="$OUT/bin"; mkdir -p "$BIN"
cat > "$BIN/pacman" <<'EOF'
#!/usr/bin/env bash
# R2Reviewer stub: -Qo answers from $STUB_QO, exit $STUB_QORC; other pacman uses exit 64.
case "${1:-}" in
  -Qo) [ -n "${STUB_QO:-}" ] && [ -f "$STUB_QO" ] && cat "$STUB_QO"; exit "${STUB_QORC:-0}" ;;
  *) exit 64 ;;
esac
EOF
chmod 700 "$BIN/pacman"

krun() { # krun NAME ko=... kt=... km=... [qo=...] [qorc=N] [touchmodtree=1]
  local cname=$1; shift
  local fx="$OUT/fx/$cname"; rm -rf "$fx"; mkdir -p "$fx" "$fx/modtree.dir" "$fx/absent"
  local a k v envs=() ko="$fx/osrelease" kt="$fx/tainted" km=""
  for a in "$@"; do
    k=${a%%=*}; v=${a#*=}
    case "$k" in
      ko) case "$v" in
            ABSENT) ko="$fx/absent/osrelease" ;;
            EMPTY)  : > "$fx/osrelease"; ko="$fx/osrelease" ;;
            UNREADABLE) printf '7.2.11-arch1-1\n' > "$fx/osrelease"; chmod 000 "$fx/osrelease"; ko="$fx/osrelease" ;;
            *) printf '%b' "$v" > "$fx/osrelease"; ko="$fx/osrelease" ;;
          esac ;;
      kt) case "$v" in
            ABSENT) kt="$fx/absent/tainted" ;;
            EMPTY)  : > "$fx/tainted"; kt="$fx/tainted" ;;
            UNREADABLE) printf '12288\n' > "$fx/tainted"; chmod 000 "$fx/tainted"; kt="$fx/tainted" ;;
            *) printf '%b' "$v" > "$fx/tainted"; kt="$fx/tainted" ;;
          esac ;;
      km) [ "$v" = DEFAULT ] || km="$fx/modtree.dir" ;;
      qo) printf '%b' "$v" > "$fx/qo" ;;
      qorc) echo "$v" > "$fx/qo.rc" ;;
      modtreefile) printf 'x' > "$fx/modtree.file"; km="$fx/modtree.file" ;;
    esac
  done
  envs=(TSUKUROI_PACMAN="$BIN/pacman" TSUKUROI_FIXTURE="$fx"
        STUB_QO="$fx/qo" STUB_QORC="$(cat "$fx/qo.rc" 2>/dev/null || printf 0)"
        TSUKUROI_KERNEL_OSRELEASE="$ko" TSUKUROI_KERNEL_TAINTED="$kt")
  [ -n "$km" ] && envs+=("TSUKUROI_KERNEL_MODULES=$km")
  local out rc
  out=$(env "${envs[@]}" bash "$CEN" 2>"$OUT/$cname.stderr"); rc=$?
  printf '=== %s: rc=%d\n' "$cname" "$rc"
  if printf '%s\n' "$out" | grep -q '^KERNEL '; then
    printf '%s\n' "$out" | grep '^KERNEL '
  else
    printf '  (NO KERNEL LINE) tail: %s\n' "$(printf '%s' "$out" | tail -n2 | tr '\n' '|')"
  fi
  printf '%s\n' "$out" > "$OUT/$cname.out"
}

# driver.sh
#!/usr/bin/env bash
# R2Reviewer — attack driver: sources harness.sh, runs all cases.
H=$(dirname "$(readlink -f "$0")")
. "$H/harness.sh" "$1" "$2"
O=$2
krun c01-healthy      'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/fx-owned is owned by linux 7.2.11.arch1-1\n'
krun c02-ko-absent    'ko=ABSENT' 'kt=12288\n' 'km=DIR'
krun c03-ko-empty     'ko=EMPTY' 'kt=12288\n' 'km=DIR'
krun c04-ko-unread    'ko=UNREADABLE' 'kt=12288\n' 'km=DIR'
krun c05-ko-spaces    'ko=   padded 7.2.11-arch1-1 more\n' 'kt=12288\n' 'km=DIR'
krun c06-kt-garbage   'ko=7.9.9-fake\n' 'kt=abc\n' 'km=DEFAULT'
krun c07-kt-negative  'ko=7.9.9-fake\n' 'kt=-5\n' 'km=DEFAULT'
krun c08-kt-empty     'ko=7.9.9-fake\n' 'kt=EMPTY' 'km=DEFAULT'
krun c09-kt-zero      'ko=7.9.9-fake\n' 'kt=0\n' 'km=DEFAULT'
krun c10-kt-12288     'ko=7.9.9-fake\n' 'kt=12288\n' 'km=DEFAULT'
krun c11-kt-bit20     'ko=7.9.9-fake\n' 'kt=1048576\n' 'km=DEFAULT'
krun c12-kt-allbits   'ko=7.9.9-fake\n' 'kt=1048560\n' 'km=DEFAULT'
krun c13-km-file      'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'modtreefile=1'
krun c14-qo-fail      'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qorc=1'
krun c15-qo-empty     'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=\n' 'qorc=0'
krun c16-qo-notail    'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/x is owned by linux\n'
krun c17-qo-foreign   'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/x is owned by evilmc 9.9.9\n'
krun c18-qo-two       'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/x is owned by linux 7.2.11.arch1-1\n/x is owned by linux-headers 7.2.11.arch1-1\n'
krun c19-pending-yes  'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/x is owned by linux 7.2.12.arch1-1\n'
krun c20-pkgver-nodot 'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DIR' 'qo=/x is owned by linux 5\n'
krun c21-derive-real  'ko=7.2.11-arch1-1\n' 'kt=12288\n' 'km=DEFAULT' 'qo=/usr/lib/modules/7.2.11-arch1-1/ is owned by linux 7.2.11.arch1-1\n'
krun c22-derive-404   'ko=7.9.9-fake\n' 'kt=12288\n' 'km=DEFAULT'
krun c23-crlf-release 'ko=7.2.11-arch1-1\r\n' 'kt=12288\n' 'km=DIR'
krun c24-derive-noko  'ko=ABSENT' 'kt=12288\n' 'km=DEFAULT' 'qo=/usr/lib/modules/ is owned by linux 7.2.11.arch1-1\n'
printf 'ALL CASES DONE\n'
```
```text
$ bash /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/driver.sh /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/clone/tools/tsukuroi-census.sh /fast/scratch/hyaku/tsukuroi-r69/R2Reviewer/att/out
=== c01-healthy: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0
=== c02-ko-absent: rc=2
KERNEL kernel-plane release=UNKNOWN pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=osrelease:absent,qo:unowned
=== c03-ko-empty: rc=2
KERNEL kernel-plane release=UNKNOWN pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=osrelease:unparsable,qo:unowned
=== c04-ko-unread: rc=2
KERNEL kernel-plane release=UNKNOWN pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=1 detail=osrelease:unreadable,qo:unowned
=== c05-ko-spaces: rc=2
KERNEL kernel-plane release=padded pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=qo:unowned
=== c06-kt-garbage: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=UNKNOWN taint_bits=UNKNOWN pending=UNKNOWN unreadable=0 detail=modules:absent,tainted:unparsable
=== c07-kt-negative: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=UNKNOWN taint_bits=UNKNOWN pending=UNKNOWN unreadable=0 detail=modules:absent,tainted:unparsable
=== c08-kt-empty: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=UNKNOWN taint_bits=UNKNOWN pending=UNKNOWN unreadable=0 detail=modules:absent,tainted:unparsable
=== c09-kt-zero: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=0 taint_bits=none pending=UNKNOWN unreadable=0 detail=modules:absent
=== c10-kt-12288: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=modules:absent
=== c11-kt-bit20: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=1048576 taint_bits=UNKNOWN pending=UNKNOWN unreadable=0 detail=modules:absent,tainted:bits-outside-closed-table
=== c12-kt-allbits: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=1048560 taint_bits=M,B,U,D,A,W,C,I,O,E,L,K,X,T,N,J pending=UNKNOWN unreadable=0 detail=modules:absent
=== c13-km-file: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=UNKNOWN pkgver=UNKNOWN modules_tree=UNKNOWN tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=1 detail=modules:not-directory
=== c14-qo-fail: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=qo:failed
=== c15-qo-empty: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=qo:unowned
=== c16-qo-notail: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=qo:shape
=== c17-qo-foreign: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=evilmc pkgver=9.9.9 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=YES unreadable=0
=== c18-qo-two: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner
=== c19-pending-yes: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.12.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=YES unreadable=0
=== c20-pkgver-nodot: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=5 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0
=== c21-derive-real: rc=2
KERNEL kernel-plane release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=NO unreadable=0
=== c22-derive-404: rc=2
KERNEL kernel-plane release=7.9.9-fake pkg=UNKNOWN pkgver=UNKNOWN modules_tree=ABSENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=modules:absent
=== c23-crlf-release: rc=2
KERNEL kernel-plane release=UNKNOWN pkg=UNKNOWN pkgver=UNKNOWN modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=osrelease:unparsable,qo:unowned
=== c24-derive-noko: rc=2
KERNEL kernel-plane release=UNKNOWN pkg=UNKNOWN pkgver=UNKNOWN modules_tree=UNKNOWN tainted=12288 taint_bits=O,E pending=UNKNOWN unreadable=0 detail=osrelease:absent,modules:release-unknown
ALL CASES DONE

rc=0

```

R2_SELFTEST=192 R2_RC=0 R2_FIELDS=7/7 R2_NEUTRAL=yes R2_HIGH=1 R2_HIDDEN_CHANNEL=TSUKUROI_FIXTURE
