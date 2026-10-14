#!/usr/bin/env bash
# tsukuroi-census.sh — four-plane host health census (tsukuroi-shokunin, round 3, TSUKUROI-R3-2).
# v1 (round 2, TSUKUROI-R2-1) was the three-plane gate: 743 lines, md5
# 7a3d3b94ecd73fbe1a9a98e9dc88b92f (SKILL.md:235-247, LOG.md:41-49). v2 adds the
# journal/boot plane on top of that settled revision — same vocabulary, same exit map.
#
# Answers exactly one question, read-only: "what is the state of the four owned host
# planes right now, and can it be assessed at all from an unprivileged shell".
# It never installs, upgrades, removes, restarts, or writes anything (PROVINCE.md:16-17);
# its whole product is verdict + evidence + suggested operator action.
#
# Plan anchor v1: plans/round-2.plan.md:3-9 — operability axis, "an executable health census
# (tools/tsukuroi-census.sh — packages/systemd/drivers planes) emits
# TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED with a firmware-style exit map, a hermetic
# --selftest on a fixture tree, and honest verdicts on the live host".
# Anti-claim v1: plans/round-2.plan.md:8 — any plane unreadable live -> BLOCKED arm fires,
# never a fake pass.
# Plan anchor v2: plans/round-3.plan.md:3-11 — "the journal/boot plane joins the census
# (new census arms ...: boot errors, failed services history, timer drift)". The `journal`
# plane below carries those three arms, each with its own selftest cases.
# Anti-claim v2: plans/round-3.plan.md:8 — journal unreadable without elevated perms ->
# the journal arm fails closed BLOCKED; the remaining planes still report.
# Round-7 addition (lane S7-2): the drivers plane carries the memory-pressure arm —
# the round-6 OOM-event plane's detection classes (corpus/knowledge/oom-event-plane.md
# §8 C1-C6) become live evidence on the drivers line and fold into its verdict. The four
# plane ids and the rollup line keep their shape (the arm rides `drivers`), so every
# pre-round-7 consumer of the census format reads the fields it read before.
#
# Verdict vocabulary (SKILL.md:22-31): HEALTHY | DEGRADED | BLOCKED, never a scalar.
#   HEALTHY   every probe of the plane returned the pass value
#   DEGRADED  the plane answers, but carries a named defect or an unresolved unknown
#   BLOCKED   the probe itself cannot run (privilege gate / missing binary / db locked),
#             or the plane's core function is offline; never "the package is corrupt"
#
# Exit map (firmware-style, plan:5): 0 HEALTHY | 1 DEGRADED | 2 BLOCKED.
# Usage errors also exit 2. Rollup: worst plane wins (BLOCKED > DEGRADED > HEALTHY).
#
# Plane decision table as implemented (probe -> pass / degrade / block):
#
#   packages (PACMAN plane)
#     probe   pacman -Qkk over a bounded sample of `pacman -Qq` (SAMPLE_N=8, default),
#             pacman -Qm | name+version list compared against the accepted foreign baseline,
#             pacman-conf IgnorePkg IgnoreGroup, /etc/pacman.conf HoldPkg
#     pass    sample drift == 0 (rc may still be 1: backup-file diffs alone do not set rc —
#             SKILL.md:47-52, "a full sweep rc=1 is not corruption evidence"), every foreign
#             package known at its baseline version (new == 0, drift == 0, gone == 0),
#             IgnorePkg/IgnoreGroup empty
#     degrade sample drift > 0 (drift is pacman's own "N altered files" counts, which already
#             exclude `backup file:` diffs), any foreign package new / version-drifted /
#             gone vs the accepted baseline, the foreign baseline absent or unreadable
#             (never HEALTHY off a missing baseline), or IgnorePkg/IgnoreGroup non-empty
#             (holds declared, SKILL.md:45), or pins unknown
#     block   pacman binary missing, pacman -Qq fails (local db unreadable), db.lck present
#             (interrupted transaction — SKILL.md:41,45), sample probe emits `error:` or rc
#             outside {0,1}
#     note    the sample is bounded on purpose: the full sweep costs ~17 s warm (SKILL.md:107)
#             and belongs to the operator checklist, not to a gate latency budget. The sample
#             rc never decides anything on its own; the drift count does.
#             round 7 (lane S7-1): the foreign arm became a watch — `pacman -Qm` is compared
#             against the accepted baseline (default: the embedded r6 census snapshot, 16
#             rows, live `foreign=16` at round 6, rows from
#             corpus/knowledge/aur-risk-plane.md §1; TSUKUROI_FOREIGN_BASELINE may point at
#             an external name<TAB>version file instead — the register's proposed baseline
#             shape). The note reads known=new=drift=gone= plus the source, and each
#             non-empty class is named. Fail-closed both ways: a baseline row hides neither
#             a new package nor a version change, and a missing/unreadable baseline or an
#             unreadable -Qm probe never reads as a pass. This realizes the round-6
#             baseline contract (plans/round-6-record-draft.md §4) in the gate.
#
#   systemd (user scope only — PROVINCE.md:8-9 owns `systemctl --user`; the system-scope
#   row lives in SKILL.md:42 and is out of this gate's scope)
#     probe   systemctl --user is-system-running; list-units --state=failed;
#             list-unit-files --type=timer --state=enabled; show <timer> -p Result for each
#             enabled timer (bounded by TIMER_SCAN_MAX)
#     pass    state == running, failed == 0, every scanned timer Result == success
#     degrade failed > 0, any timer Result != success, any Result unreadable (unresolved
#             unknown), or state in {degraded,starting,stopping}
#     block   systemctl missing, the --user bus is unreachable (output is not a state word),
#             a list probe fails, or state in {offline,maintenance} (core function offline)
#     note    deliberate refinement vs SKILL.md:42, which lists `degraded` under BLOCKED:
#             SKILL.md:31 glosses BLOCKED as "cannot be assessed read-only"; a degraded scope
#             is fully assessed by the failed-units probe, so this gate reports it as
#             DEGRADED with the failed set named. Recorded here, not silently applied.
#
#   drivers (nvidia / kernel ring plane)
#     probe   kernel error ring — `dmesg --level=err,crit,alert,emerg` preferred, else
#             `journalctl -k -b -p err -o json` (entry-level counts; SKILL.md:220 errata:
#             line counts are traps, use entries). Then nvidia presence: PCI vendor 0x10de
#             inventory (/sys/bus/pci/devices), `nvidia-smi --query-gpu=name,driver_version`,
#             `lsmod` nvidia rows, /dev/nvidia* nodes
#     pass    kerr == 0 with a non-empty ring, and nvidia either present-and-answering
#             (smi ok + module loaded + nodes exist) or absent from PCI inventory
#     degrade kerr > 0, classes counted at entry level (oom / io / gpu / other); the plane's
#             noise floor is [unknown], so any kernel error entry is a named unresolved item
#     block   both rings unusable, ring empty (cannot tell "clean" from "no data"),
#             nvidia hardware in PCI but core function offline (smi not answering, module not
#             loaded, or no /dev/nvidia* node), or PCI inventory unreadable with no other
#             positive evidence
#     note    dmesg is restricted on the measured host (`dmesg_restrict=1`, SKILL.md:158-160);
#             the ring source actually used is printed as `ring=` in the plane line.
#
#   drivers.mem (memory-pressure arm — rides the drivers plane's line and verdict;
#   round 7, lane S7-2, detection-only). Vocabulary: the round-6 OOM-event plane's
#   detection contract (corpus/knowledge/oom-event-plane.md §8, classes C1-C6):
#             C1 kernel OOM dump entries (`journalctl -k -b -p err -o json` + the OOM
#             regex — the same source and semantics as the ring's `oom=` class),
#             C2 systemd OOM attribution (`kernel OOM killer killed some processes`,
#             emitted at PRIORITY=5, i.e. the only attribution for a session-wide
#             SIGKILL class that leaves no kernel record),
#             C3 SIGKILL/teardown class (`status=9/KILL|Failed with result
#             '(signal|oom-kill)'`),
#             C4 cgroup `memory.events[.local]` oom_kill PRESENCE FLAGS (§4.2: two
#             documented kill waves left the surviving counter at 1 — a flag per
#             cgroup, never an event count),
#             C5 swap-pressure anchors (swap.events `fail`, swap.peak vs meminfo
#             SwapTotal, `memory.stat` pswpin/pswpout, `sock_throttled`),
#             C6 live shape (PSI `avg300`/`total`, MemAvailable, Shmem), plus the
#             guards shape (§4.5: memory.max/high, memory.oom.group).
#     pass    every signal readable and every class zero
#     degrade any class > 0 (C1/C2/C3 entries, any oom_kill flag, swap fail > 0), or
#             any required signal unreadable — named in `unknown=[...]`, never silent
#     block   cgroup sweep empty AND all three journal probes unusable: no class can
#             be read at all (fail closed, same stance as the ring arms)
#     note    probe cost ≈0.3 s live (190 cgroup files + 3 bounded `--grep` reads;
#             whole-gate live run 1.11 s, inside the recorded 0.69–1.75 s band).
#             `journalctl --grep` exits 1 on no-match (measured 2026-10-14) — rc 1 is
#             "0 entries", any other non-zero rc is "unreadable". Page-cache-inclusive
#             `memory.peak` is not a pressure reading (§4.4), so the arm reports the
#             swap plane instead, and `memory.events` counters are never read as meters.
#             First live run (2026-10-14T18:33:02Z, drivers line verbatim): mem=[DEGRADED]
#             C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2
#             [user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849
#             C5_swap_peak_pct=99% C5_pswp=72117839/93795670 C5_sock_throttled=67558;
#             C6_psi_full_avg300=0.00 C6_psi_full_total_us=68342659 C6_avail_kb=19214152
#             C6_shmem_kb=6907048; guards=max/max oom.group=0 — the round-6 OOM plane's
#             state re-measured (2 kill waves, swap plane at 99%), not quoted: live
#             counters drift, re-run before citing. The arm carries no cross-run delta
#             (the census keeps no state); "new vs baseline" is the class-presence
#             reading plus the note's per-round recheck ledger.
#
#   journal (this-boot triage — SKILL.md:43 row; all probes read-only)
#     probe   arm 1 boot record: `journalctl --list-boots --no-pager` (index-0 line must exist)
#             arm 2 boot target: `systemctl is-active $BOOT_TARGET` (default graphical.target)
#             arm 3 boot errors: `journalctl -b -p err -o json --no-pager` — ENTRY count, and
#             disjoint classes on the JSON lines (coredump | kernel | other). Line counts are
#             traps (60 941 lines vs 238 entries, systemd-user-plane.md:104-116); only `-o json`
#             lines (= entries) are ever counted.
#             arm 4 failed services history: journal-derived from the same err stream, so units
#             that failed earlier this boot and were reset since are still named — the systemd
#             plane reports only the current failed set.
#             arm 5 timer drift: for each enabled user timer, `show <t> -p ActiveState` (bounded
#             TIMER_SCAN_MAX); an enabled timer that is not `active` will not fire as configured.
#             Deliberate: avoids brittle relative-time parsing of `list-timers`, and reuses the
#             systemd plane's timer-loop shape.
#     pass    index-0 boot line present, target == active, err entries == 0 with a non-empty
#             journal this boot, failedhist == 0, every enabled timer armed
#     degrade err entries > 0 (noise floor [unknown]; classes named — same stance as drivers),
#             failedhist > 0, timer drift > 0, or timer ActiveState unreadable (unresolved
#             unknown — mirrors the systemd plane's unreadable-Result semantics)
#     block   journalctl missing or --list-boots unreadable (fails closed — anti-claim v2,
#             plans/round-3.plan.md:8), no index-0 boot line, boot target not `active`
#             (SKILL.md:43 "no boot reaches graphical.target"), err stream unreadable, or the
#             journal is empty this boot (clean vs no-data cannot be told apart)
#     note    kernel entries also appear in the drivers plane's ring; the journal plane's
#             distinct value is the non-kernel classes (coredumps, service messages), the boot
#             record/target, and the armed-state of user timers. `coredumpctl` is deliberately
#             NOT probed: table parsing is a measured trap (systemd-user-plane.md:169) and
#             `--json` would add a jq dependency; the `systemd-coredump` entry class IS the
#             storm signal. First full-gate live run of v2 (2026-10-14T14:51:17Z): boots=13
#             current=yes target=graphical.target:active err=251 (coredump=211 kernel=38
#             other=2) failedhist=0 timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 —
#             snapshot only (counts drift with the live coredump storm: 249 at 14:48, 251 at
#             14:51); re-run, never quote as now.
#
# Read-only guarantee: no probe writes; the gate creates no files at all in live mode
# (selftest writes only under a mktemp dir named /tmp/tsukuroi-r3-2-selftest.XXXXXX).
# Secrets are never read: only public package/system unit/driver/journal state is queried.
#
# Hermetic selftest: `--selftest` builds a /tmp fixture tree with a dispatcher stub for
# every probe command and re-invokes this script against it via env overrides. Each case
# asserts exit code + final verdict + one or more evidence substrings, and asserts the
# fixture tree is byte-unchanged after the run (zero mutation). Every probe command and
# every host path read in live mode has an override below, so the selftest touches no
# host state:
#   TSUKUROI_PACMAN TSUKUROI_PACMAN_CONF TSUKUROI_PACMAN_CONF_FILE TSUKUROI_PACMAN_DB
#   TSUKUROI_FOREIGN_BASELINE (external baseline path; empty/unset = embedded r6 snapshot)
#   TSUKUROI_SYSTEMCTL TSUKUROI_DMESG TSUKUROI_JOURNALCTL TSUKUROI_NVIDIA_SMI TSUKUROI_LSMOD
#   TSUKUROI_PCI_SYSFS TSUKUROI_DEV_DIR TSUKUROI_HOSTNAME_FILE TSUKUROI_DMESG_RESTRICT_FILE
#   TSUKUROI_BOOT_TARGET TSUKUROI_SAMPLE_N TSUKUROI_TIMER_SCAN_MAX TSUKUROI_FIXTURE (selftest only)
#   TSUKUROI_CGROUP_ROOT TSUKUROI_MEM_SLICE TSUKUROI_PRESSURE_FILE TSUKUROI_MEMINFO_FILE
#   (the memory-pressure arm's paths; the arm itself has no other host read)
#
# Sources: PROVINCE.md:5-12,16-18 · SKILL.md:20-31 (vocabulary), :33-45 (decision table incl.
# the journal/boot row), :47-83 (Qkk benign classes), :85-135 (update-safety checklist),
# :137-172 (boundary rule) · AGENTS.md:3-5 · corpus/QUALITY.md:1-5 ·
# corpus/knowledge/package-state-plane.md, systemd-user-plane.md (§5-6 err classes + coredump
# census, §8 method traps), driver-firmware-plane.md · plans/round-2.plan.md:3-9 ·
# plans/round-3.plan.md:3-11 · plans/round-6-record-draft.md §4 (baseline contract) ·
# corpus/knowledge/aur-risk-plane.md §1 (the 16 baseline rows and their classes).
set -euo pipefail
umask 077

VERSION='census-v2'
SELF=${BASH_SOURCE[0]}

# ---- probe surface (every command and every host path is override-able) ------
PACMAN=${TSUKUROI_PACMAN:-pacman}
PACMAN_CONF=${TSUKUROI_PACMAN_CONF:-pacman-conf}
PACMAN_CONF_FILE=${TSUKUROI_PACMAN_CONF_FILE:-/etc/pacman.conf}
PACMAN_DB=${TSUKUROI_PACMAN_DB:-/var/lib/pacman}
SYSTEMCTL=${TSUKUROI_SYSTEMCTL:-systemctl}
DMESG=${TSUKUROI_DMESG:-dmesg}
JOURNALCTL=${TSUKUROI_JOURNALCTL:-journalctl}
NVIDIA_SMI=${TSUKUROI_NVIDIA_SMI:-nvidia-smi}
LSMOD=${TSUKUROI_LSMOD:-lsmod}
PCI_SYSFS=${TSUKUROI_PCI_SYSFS:-/sys/bus/pci/devices}
DEV_DIR=${TSUKUROI_DEV_DIR:-/dev}
HOSTNAME_FILE=${TSUKUROI_HOSTNAME_FILE:-/proc/sys/kernel/hostname}
DMESG_RESTRICT_FILE=${TSUKUROI_DMESG_RESTRICT_FILE:-/proc/sys/kernel/dmesg_restrict}
BOOT_TARGET=${TSUKUROI_BOOT_TARGET:-graphical.target}
SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
TIMER_SCAN_MAX=${TSUKUROI_TIMER_SCAN_MAX:-12}
CGROUP_ROOT=${TSUKUROI_CGROUP_ROOT:-/sys/fs/cgroup}
MEM_SLICE=${TSUKUROI_MEM_SLICE:-user.slice/user-1000.slice}
PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}
MEMINFO_FILE=${TSUKUROI_MEMINFO_FILE:-/proc/meminfo}
FOREIGN_BASELINE=${TSUKUROI_FOREIGN_BASELINE:-}

# Accepted foreign baseline — the round-6 census snapshot (live `foreign=16` at round 6,
# 2026-10-14; re-measured live before landing this arm and byte-identical, so the snapshot
# still equals the host's set). Source of the rows: corpus/knowledge/aur-risk-plane.md §1
# (14 offline-exile + 2 AUR-local, `name version` per row). The register owns the rows;
# this gate owns the comparison. TSUKUROI_FOREIGN_BASELINE may point at an external
# name-version file (the register's proposed corpus/knowledge/foreign-aur-baseline.tsv
# shape); unset or empty = this snapshot. Rows are never re-guessed here: a class claim
# needs the register's measured trail, and the selftest hit-case pins this constant's
# 16-row content so an edit to it cannot pass silently.
R6_FOREIGN_BASELINE='android-apktool-bin 3.0.3-1
elephant 2.21.0-1
elephant-bluetooth 2.21.0-1
elephant-calc 2.21.0-1
elephant-clipboard 2.21.0-1
elephant-desktopapplications 2.21.0-1
elephant-files 2.21.0-1
elephant-menus 2.21.0-1
elephant-providerlist 2.21.0-1
elephant-runner 2.21.0-1
elephant-symbols 2.21.0-1
elephant-todo 2.21.0-1
elephant-unicode 2.21.0-1
elephant-websearch 2.21.0-1
obsidian-cli-inspector 1.0.3-1
omarchy-walker 1.0.0-2'

CLASS_OOM='Out of memory|oom-kill|oom_reaper'
CLASS_IO='I/O error|Buffer I/O error|critical medium error|critical target error'
CLASS_GPU='NVRM|nvidia|NVIDIA|GSP|drm'
CLASS_FAILED='Failed to |entered failed state|Failed with result'
CLASS_OOM_SYS='kernel OOM killer killed some processes'
CLASS_SIGKILL="status=9/KILL|Failed with result '(signal|oom-kill)'"

# ---- shared state ------------------------------------------------------------
PKG_V=BLOCKED PKG_NOTE='probe not run'
SYS_V=BLOCKED SYS_NOTE='probe not run'
DRV_V=BLOCKED DRV_NOTE='probe not run'
MEM_V=BLOCKED MEM_NOTE='arm not run'
JRN_V=BLOCKED JRN_NOTE='probe not run'

usage() {
  cat <<'EOF'
usage: tsukuroi-census.sh [--selftest] [--sample N] [--help]

  (no flags)   run the live read-only census over packages / systemd-user / drivers
               (incl. the memory-pressure arm) / journal-boot
  --selftest   hermetic fixture-tree test of every verdict arm (writes only under
               /tmp/tsukuroi-r3-2-selftest.*); exit 0 pass, 1 fail
  --sample N   packages plane: size of the pacman -Qkk sample (default 8)

Verdict line: TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=.. drivers=.. journal=..)
Exit map:     0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors also 2)
EOF
}

# ---- helpers -----------------------------------------------------------------
CAP_OUT='' CAP_RC=0
cap() { # run read-only probe; capture stdout+stderr and rc without tripping set -e
  set +e
  CAP_OUT=$("$@" 2>&1)
  CAP_RC=$?
  set -e
}

have() { command -v "$1" >/dev/null 2>&1; }

rank() {
  case "$1" in
    HEALTHY)  printf 0 ;;
    DEGRADED) printf 1 ;;
    BLOCKED)  printf 2 ;;
    *)        printf 9 ;;
  esac
}

worse() { # worse A B -> the more severe of the two
  if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
}

nlines() { # count of lines in a string (0 for empty)
  if [ -z "$1" ]; then printf 0; else printf '%s\n' "$1" | grep -c . || true; fi
}

count_glob() { # count_glob DIR PATTERN -> number of matching entries (0 if none)
  local dir=$1 pat=$2 n=0 p
  [ -d "$dir" ] || { printf 0; return; }
  for p in "$dir"/$pat; do
    [ -e "$p" ] && n=$((n + 1))
  done
  printf '%s' "$n"
}

count_pci_nvidia() { # count_pci_nvidia DIR -> nvidia (0x10de) vendor files, or -1 if DIR unreadable
  local dir=$1 n=0 v
  [ -d "$dir" ] || { printf -- '-1'; return; }
  for v in "$dir"/*/vendor; do
    [ -f "$v" ] || continue
    if [ "$(head -c 7 -- "$v" 2>/dev/null || true)" = '0x10de' ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

class_counts() { # class_counts json|text HAYSTACK -> "oom=N io=N gpu=N other=N"
  local mode=$1 text=$2 pre='' o i g u total
  [ "$mode" = json ] && pre='"MESSAGE":"[^"]*'
  o=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_OOM})" || true)
  i=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_IO})" || true)
  g=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_GPU})" || true)
  u=$(printf '%s\n' "$text" | grep -cE "${pre}(${CLASS_OOM}|${CLASS_IO}|${CLASS_GPU})" || true)
  total=$(nlines "$text")
  printf 'oom=%s io=%s gpu=%s other=%s' "$o" "$i" "$g" "$((total - u))"
}

mem_read() { # mem_read FILE -> first line (trimmed); empty when unreadable
  [ -r "$1" ] || return 0
  head -n1 -- "$1" 2>/dev/null | tr -d '\r' || true
}

mem_field() { # mem_field FILE KEY -> second field of the first KEY row, or empty
  # (the trailing colon of /proc/meminfo keys is tolerated; cgroup keys have none)
  [ -r "$1" ] || return 0
  awk -v k="$2" '{ key = $1; sub(/:$/, "", key) } key == k { print $2; exit }' "$1" 2>/dev/null || true
}

# ---- plane: packages ---------------------------------------------------------
probe_packages() {
  PKG_V=HEALTHY
  local notes='' names=() s_rc='' drift=0 backup=0 nonroot=0 s_out='' sample_n=0

  if ! have "$PACMAN"; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman=missing (probe cannot run)"
    return
  fi
  if [ -e "$PACMAN_DB/db.lck" ]; then
    PKG_V=BLOCKED
    PKG_NOTE='db.lck=present — interrupted transaction (SKILL.md:41,45)'
    return
  fi

  cap "$PACMAN" -Qq
  local qq_rc=$CAP_RC
  if [ "$qq_rc" -ne 0 ]; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qq rc=$qq_rc [local db unreadable]"
    return
  fi
  mapfile -t names < <(printf '%s\n' "$CAP_OUT" | grep -v '^[[:space:]]*$' | head -n "$SAMPLE_N")
  sample_n=${#names[@]}
  if [ "$sample_n" -eq 0 ]; then
    PKG_V=BLOCKED
    PKG_NOTE='pacman -Qq listed no packages [local db empty; state not assessable]'
    return
  fi

  cap "$PACMAN" -Qkk "${names[@]}"
  s_rc=$CAP_RC
  s_out=$(printf '%s\n' "$CAP_OUT" | tr '\r' '\n')
  if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample rc=$s_rc [probe cannot run]"
    return
  fi
  if printf '%s\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\n' "$s_out" | grep -m1 '^error:')"
    return
  fi

  drift=$(printf '%s\n' "$s_out" \
    | sed -nE 's/^[^:]+: [0-9]+ total files, ([0-9]+) altered files?.*/\1/p' \
    | awk '{s += $1} END {print s + 0}')
  backup=$(printf '%s\n' "$s_out" | grep -c '^backup file: ' || true)
  nonroot=$(printf '%s\n' "$s_out" \
    | grep -cE '\(failed to calculate SHA256 checksum\)|\(Permission denied\)' || true)
  local drift_pkgs
  drift_pkgs=$(printf '%s\n' "$s_out" \
    | sed -nE 's/^([^:]+): [0-9]+ total files, [1-9][0-9]* altered files?.*/\1/p' \
    | paste -sd, - || true)

  local foreign_n='?' foreign_rc=0
  cap "$PACMAN" -Qm
  foreign_rc=$CAP_RC
  if [ "$foreign_rc" -eq 0 ]; then foreign_n=$(nlines "$CAP_OUT"); fi

  # foreign watch arm (round 7, lane S7-1): compare `pacman -Qm` (name version per row)
  # against the accepted baseline so the plane reports known-vs-new instead of a bare
  # count. Fail-closed both ways: a baseline row hides neither a new package nor a
  # version change, and an absent/unreadable baseline or an unreadable -Qm probe never
  # reads as a pass (r6 baseline contract, plans/round-6-record-draft.md §4).
  local base_txt='' base_state='' foreign_known=0 foreign_new_n=0 foreign_drift_n=0 foreign_gone_n=0
  local foreign_new='' foreign_drift='' foreign_gone=''
  if [ -n "$FOREIGN_BASELINE" ]; then
    if [ -f "$FOREIGN_BASELINE" ] && [ -r "$FOREIGN_BASELINE" ]; then
      base_txt=$(cat -- "$FOREIGN_BASELINE" 2>/dev/null || true)
      base_state="file($(nlines "$base_txt"))"
    elif [ -e "$FOREIGN_BASELINE" ]; then
      base_state='unreadable'
    else
      base_state='absent'
    fi
  else
    base_txt=$R6_FOREIGN_BASELINE
    base_state="r6($(nlines "$base_txt"))"
  fi

  if [ "$foreign_rc" -eq 0 ] && [ "$base_state" != absent ] && [ "$base_state" != unreadable ]; then
    local nm ver bn live_names=''
    while read -r nm ver _; do
      [ -n "$nm" ] || continue
      live_names="$live_names $nm"
      bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n {print $2; exit}')
      if [ -z "$bn" ]; then
        foreign_new_n=$((foreign_new_n + 1)); foreign_new="$foreign_new $nm"
      elif [ "$ver" = "$bn" ]; then
        foreign_known=$((foreign_known + 1))
      else
        foreign_drift_n=$((foreign_drift_n + 1)); foreign_drift="$foreign_drift $nm($bn->${ver:-?})"
      fi
    done <<< "$CAP_OUT"
    local rn rv
    while read -r rn rv _; do
      [ -n "$rn" ] || continue
      case " $live_names " in
        *" $rn "*) : ;;
        *) foreign_gone_n=$((foreign_gone_n + 1)); foreign_gone="$foreign_gone $rn" ;;
      esac
    done <<< "$base_txt"
  fi

  local fr_note
  if [ "$foreign_rc" -ne 0 ]; then
    fr_note="foreign=? [pacman -Qm unreadable]"
  elif [ "$base_state" = absent ] || [ "$base_state" = unreadable ]; then
    fr_note="foreign=$foreign_n(base=$base_state [known/new/drift/gone unknown])"
  else
    fr_note="foreign=$foreign_n(known=$foreign_known new=$foreign_new_n drift=$foreign_drift_n gone=$foreign_gone_n) base=$base_state"
    [ -n "$foreign_new" ] && fr_note="$fr_note new=[${foreign_new# }]"
    [ -n "$foreign_drift" ] && fr_note="$fr_note drift=[${foreign_drift# }]"
    [ -n "$foreign_gone" ] && fr_note="$fr_note gone=[${foreign_gone# }]"
  fi

  local pins_n='?' pins_rc=0 pins_names='' holds='none'
  cap "$PACMAN_CONF" IgnorePkg IgnoreGroup
  pins_rc=$CAP_RC
  if [ "$pins_rc" -eq 0 ]; then
    pins_n=$(nlines "$CAP_OUT")
    pins_names=$(printf '%s\n' "$CAP_OUT" | grep . | paste -sd, - || true)
  fi
  if [ -r "$PACMAN_CONF_FILE" ]; then
    holds=$(grep -hE '^[[:space:]]*HoldPkg' "$PACMAN_CONF_FILE" 2>/dev/null \
      | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' || true)
    holds=${holds:-none}
  fi

  PKG_NOTE="pacman -Qkk rc=$s_rc sample=$sample_n($(printf '%s,' "${names[@]}" | sed -E 's/,$//')) drift=$drift${drift_pkgs:+[$drift_pkgs]} backup_diffs=$backup nonroot_artifacts=$nonroot"
  PKG_NOTE="$PKG_NOTE; $fr_note; pins=${pins_names:-none}; holds=$holds; db.lck=absent"

  if [ "$drift" -gt 0 ]; then PKG_V=DEGRADED; fi
  if [ "$foreign_rc" -ne 0 ] || [ "$base_state" = absent ] || [ "$base_state" = unreadable ] \
    || [ "$foreign_new_n" -gt 0 ] || [ "$foreign_drift_n" -gt 0 ] || [ "$foreign_gone_n" -gt 0 ]; then
    PKG_V=DEGRADED
  fi
  if [ "$pins_n" != '0' ]; then PKG_V=DEGRADED; fi
  return
}

# ---- plane: systemd (user scope) ---------------------------------------------
probe_systemd() {
  SYS_V=HEALTHY
  if ! have "$SYSTEMCTL"; then
    SYS_V=BLOCKED
    SYS_NOTE='systemctl=missing (probe cannot run)'
    return
  fi

  cap "$SYSTEMCTL" --user is-system-running --no-pager
  local s_rc=$CAP_RC state
  state=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')
  case "$state" in
    running | degraded | starting | stopping | maintenance | offline | unknown) : ;;
    *)
      SYS_V=BLOCKED
      SYS_NOTE="systemctl --user unusable rc=$s_rc [$(printf '%s' "$state" | cut -c1-90)]"
      return
      ;;
  esac
  if [ "$state" = offline ] || [ "$state" = maintenance ]; then
    SYS_V=BLOCKED
    SYS_NOTE="scope=user state=$state [core function offline]"
    return
  fi

  cap "$SYSTEMCTL" --user list-units --state=failed --no-legend --plain --no-pager
  local f_rc=$CAP_RC failed=0
  if [ "$f_rc" -ne 0 ]; then
    SYS_V=BLOCKED
    SYS_NOTE="list-units --state=failed rc=$f_rc [probe cannot run]"
    return
  fi
  failed=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $2 == "loaded" && $3 == "failed"' | wc -l)

  cap "$SYSTEMCTL" --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
  local t_rc=$CAP_RC timers_enabled=0 timers=() t_scan=0
  if [ "$t_rc" -ne 0 ]; then
    SYS_V=BLOCKED
    SYS_NOTE="list-unit-files --type=timer --state=enabled rc=$t_rc [probe cannot run]"
    return
  fi
  timers_enabled=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | wc -l)
  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")

  local t_fail=0 t_unknown=0 bad='' r
  for t in "${timers[@]}"; do
    t_scan=$((t_scan + 1))
    cap "$SYSTEMCTL" --user show "$t" -p Result --value --no-pager
    r=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r')
    if [ "$CAP_RC" -ne 0 ] || [ -z "$r" ]; then
      t_unknown=$((t_unknown + 1))
    elif [ "$r" != success ]; then
      t_fail=$((t_fail + 1))
      bad="${bad}${t}=${r} "
    fi
  done

  SYS_NOTE="scope=user state=$state failed=$failed timers_enabled=$timers_enabled timers_scanned=$t_scan timer_fail=$t_fail timer_unknown=$t_unknown"
  [ -n "$bad" ] && SYS_NOTE="$SYS_NOTE ($bad)"

  if [ "$failed" -gt 0 ] || [ "$t_fail" -gt 0 ] || [ "$t_unknown" -gt 0 ]; then SYS_V=DEGRADED; fi
  case "$state" in degraded | starting | stopping) SYS_V=DEGRADED ;; esac
  return
}

# ---- plane: drivers ----------------------------------------------------------
probe_drivers() {
  DRV_V=HEALTHY
  local ring='' ring_rc=0 kerr=0 cls='oom=0 io=0 gpu=0 other=0' restrict='?'

  restrict=$(head -n1 "$DMESG_RESTRICT_FILE" 2>/dev/null | tr -d '\r' || true)
  restrict=${restrict:-?}

  if have "$DMESG"; then
    cap "$DMESG" --level=err,crit,alert,emerg
    if [ "$CAP_RC" -eq 0 ]; then
      ring=dmesg
      kerr=$(nlines "$CAP_OUT")
      cls=$(class_counts text "$CAP_OUT")
    else
      ring_rc=$CAP_RC
    fi
  else
    ring_rc=127
  fi

  if [ -z "$ring" ]; then
    if ! have "$JOURNALCTL"; then
      DRV_V=BLOCKED
      DRV_NOTE="kernel ring unusable: dmesg rc=$ring_rc, journalctl=missing"
      return
    fi
    cap "$JOURNALCTL" -k -b -p err -o json --no-pager
    if [ "$CAP_RC" -ne 0 ]; then
      DRV_V=BLOCKED
      DRV_NOTE="kernel ring unusable: dmesg rc=$ring_rc, journalctl -k rc=$CAP_RC"
      return
    fi
    ring='journalctl-k'
    kerr=$(nlines "$CAP_OUT")
    cls=$(class_counts json "$CAP_OUT")
  fi

  # kerr == 0 is only a pass if the ring really has data; an empty ring cannot be told
  # apart from a clean one, and must never be quoted as a fake HEALTHY.
  if [ "$kerr" -eq 0 ]; then
    if [ "$ring" = 'journalctl-k' ]; then
      cap "$JOURNALCTL" -k -b -o json --no-pager
      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
        DRV_V=BLOCKED
        DRV_NOTE='kernel ring empty/unreadable (journalctl -k -b lists no kernel entries)'
        return
      fi
    else
      cap "$DMESG"
      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
        DRV_V=BLOCKED
        DRV_NOTE='kernel ring empty/unreadable (dmesg lists no records)'
        return
      fi
    fi
  fi

  local pci_n smi='absent' smi_rc=127 driver='' mods=-1 nodes=0 nv='' modnote=''
  pci_n=$(count_pci_nvidia "$PCI_SYSFS")
  if have "$NVIDIA_SMI"; then
    cap "$NVIDIA_SMI" --query-gpu=name,driver_version --format=csv,noheader
    smi_rc=$CAP_RC
    if [ "$smi_rc" -eq 0 ] && [ -n "$(printf '%s' "$CAP_OUT" | tr -d '[:space:]')" ]; then
      smi=ok
      driver=$(printf '%s\n' "$CAP_OUT" | head -n1 | awk -F', *' '{print $NF}')
    else
      smi="rc=$smi_rc"
    fi
  fi
  if have "$LSMOD"; then
    cap "$LSMOD"
    mods=$(printf '%s\n' "$CAP_OUT" | grep -cE '^nvidia' || true)
  fi
  nodes=$(count_glob "$DEV_DIR" 'nvidia*')

  if [ "$pci_n" -gt 0 ]; then
    if [ "$smi" != ok ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but nvidia-smi not answering ($smi) — core function offline (SKILL.md:44)"
    elif [ "$mods" -le 0 ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but no nvidia module loaded — core function offline"
    elif [ "$nodes" -eq 0 ]; then
      DRV_V=BLOCKED
      modnote="pci_10de=$pci_n but no /dev/nvidia* node — core function offline (SKILL.md:44)"
    else
      nv=present
    fi
  elif [ "$pci_n" -eq 0 ]; then
    nv='absent(pci_10de=0)'
  else
    if [ "$smi" = ok ] && [ "$mods" -gt 0 ]; then
      nv='present(pci inventory unreadable)'
    else
      DRV_V=BLOCKED
      modnote='PCI inventory unreadable and no positive nvidia evidence — cannot assess read-only'
    fi
  fi

  if [ "$DRV_V" != BLOCKED ]; then
    if [ "$kerr" -gt 0 ]; then
      DRV_V=DEGRADED
      DRV_NOTE="ring=$ring dmesg_restrict=$restrict kerr=$kerr ($cls) [unknown: accepted noise floor]; nvidia=$nv smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
    else
      DRV_NOTE="ring=$ring dmesg_restrict=$restrict kerr=0 ($cls); nvidia=$nv smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
    fi
  else
    DRV_NOTE="$modnote; ring=$ring kerr=$kerr ($cls); smi=${driver:-$smi} modules=$mods nodes=$nodes pci_10de=$pci_n"
  fi
  return
}

# ---- arm: memory pressure (rides the drivers plane's line and verdict) -------
# Round-7 addition, lane S7-2. Detection-only, read-only, non-root. Vocabulary:
# corpus/knowledge/oom-event-plane.md §8 (classes C1-C6) plus the note's reading
# rules — `memory.events oom_kill` is a PRESENCE FLAG, never an event count (§4.2),
# the journal messages are the event list, and the page-cache-inclusive
# `memory.peak` is not a pressure reading (§4.4). Fails closed: an unreadable
# signal is a named unknown and degrades the arm; only a total inability to read
# any class (cgroup sweep empty AND all journal probes unusable) reads BLOCKED —
# never a fake pass. Nothing is written; no cgroup, unit or service is touched;
# the operator remediates.
probe_mem_arm() {
  MEM_V=HEALTHY
  local unk='' deg=0 j_ok=0 cg_ok=0
  local k_oom='?' s_oom='?' sg_oom='?'
  local sweep=0 present=0 localp=0 names=''
  local sock='-' swap_fail='-' swap_peak='-' swap_total='-' swap_pct='-'
  local ps_in='-' ps_out='-' psi_s='-' psi_f='-' psi_t='-'
  local avail='-' shmem='-' g_max='-' g_high='-' g_grp='-'
  local slice="$CGROUP_ROOT/$MEM_SLICE" f rel v

  # C1-C3 — the journal side: entry counts only (`-o json` lines). `journalctl
  # --grep` exits 1 on no-match (measured 2026-10-14), so rc 1 = "0 entries" and
  # any other non-zero rc = unreadable.
  if have "$JOURNALCTL"; then
    cap "$JOURNALCTL" -k -b -p err -o json --no-pager --grep "$CLASS_OOM"
    case "$CAP_RC" in
      0) k_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) k_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C1 " ;;
    esac
    cap "$JOURNALCTL" -b -o json --no-pager --grep "$CLASS_OOM_SYS"
    case "$CAP_RC" in
      0) s_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) s_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C2 " ;;
    esac
    cap "$JOURNALCTL" -b -o json --no-pager --grep "$CLASS_SIGKILL"
    case "$CAP_RC" in
      0) sg_oom=$(nlines "$CAP_OUT"); j_ok=$((j_ok + 1)) ;;
      1) sg_oom=0; j_ok=$((j_ok + 1)) ;;
      *) unk="${unk}C3 " ;;
    esac
  else
    unk="${unk}C1 C2 C3 "
  fi

  # C4 — cgroup presence flags, bounded sweep over memory.events[.local]
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    sweep=$((sweep + 1))
    v=$(awk '$1 == "oom_kill" { print $2; exit }' "$f" 2>/dev/null || true)
    if [ -n "$v" ] && [ "$v" != 0 ]; then
      rel=${f#"$CGROUP_ROOT"/}
      rel=${rel%/memory.events}
      case "$f" in
        *.local) localp=$((localp + 1)) ;;
        *)
          present=$((present + 1))
          [ "$present" -le 3 ] && names="${names}${names:+,}${rel}"
          ;;
      esac
    fi
  done < <(find "$CGROUP_ROOT" -xdev \( -name memory.events -o -name memory.events.local \) \
             -print 2>/dev/null | LC_ALL=C sort | head -n 4000)
  [ "$sweep" -gt 0 ] && cg_ok=1

  # C5 — swap-pressure anchors (+ the socket-throttle class and the guards shape)
  if [ -d "$slice" ]; then
    swap_fail=$(mem_field "$slice/memory.swap.events" fail)
    swap_peak=$(mem_read "$slice/memory.swap.peak")
    ps_in=$(mem_field "$slice/memory.stat" pswpin)
    ps_out=$(mem_field "$slice/memory.stat" pswpout)
    sock=$(mem_field "$slice/memory.events" sock_throttled)
    g_max=$(mem_read "$slice/memory.max")
    g_high=$(mem_read "$slice/memory.high")
    g_grp=$(mem_read "$slice/memory.oom.group")
    [ -r "$slice/memory.swap.events" ] || unk="${unk}C5-swap "
    [ -r "$slice/memory.stat" ] || unk="${unk}C5-stat "
  else
    unk="${unk}C5-slice "
  fi
  swap_total=$(mem_field "$MEMINFO_FILE" SwapTotal)
  case "$swap_peak" in '' | *[!0-9]*) swap_peak='-' ;; esac
  case "$swap_total" in '' | *[!0-9]*) swap_total='-' ;; esac
  if [ "$swap_peak" != '-' ] && [ "$swap_total" != '-' ] && [ "$swap_total" -gt 0 ]; then
    swap_pct=$(awk -v p="$swap_peak" -v t="$swap_total" \
      'BEGIN { printf "%d%%", (p / 1024 / t) * 100 }')
  fi
  case "$swap_fail" in '' | *[!0-9]*) swap_fail='-' ;; esac
  case "$sock" in '' | *[!0-9]*) sock='-' ;; esac
  case "$ps_in" in '' | *[!0-9]*) ps_in='-' ;; esac
  case "$ps_out" in '' | *[!0-9]*) ps_out='-' ;; esac
  g_max=${g_max:-'-'} g_high=${g_high:-'-'} g_grp=${g_grp:-'-'}

  # C6 — live shape: PSI (avg300 + total) and the meminfo picture
  [ -r "$MEMINFO_FILE" ] || unk="${unk}C6-meminfo "
  avail=$(mem_field "$MEMINFO_FILE" MemAvailable); avail=${avail:-'-'}
  shmem=$(mem_field "$MEMINFO_FILE" Shmem); shmem=${shmem:-'-'}
  if [ -r "$PRESSURE_FILE" ]; then
    read -r psi_s psi_f psi_t < <(awk '
      $1 == "some" || $1 == "full" {
        for (i = 2; i <= NF; i++) { split($i, a, "="); v[a[1]] = a[2] }
        if ($1 == "some") s = v["avg300"]; else { f = v["avg300"]; t = v["total"] }
      }
      END { printf "%s %s %s\n", (s == "" ? "-" : s), (f == "" ? "-" : f), (t == "" ? "-" : t) }' \
      "$PRESSURE_FILE" 2>/dev/null || true)
    psi_s=${psi_s:-'-'} psi_f=${psi_f:-'-'} psi_t=${psi_t:-'-'}
  else
    unk="${unk}C6-psi "
  fi

  # verdict: any class > 0 degrades; any unreadable signal degrades; BLOCKED only
  # when no class can be read at all (fail closed — never a fake pass)
  [ "$k_oom" != '?' ] && [ "$k_oom" -gt 0 ] && deg=1
  [ "$s_oom" != '?' ] && [ "$s_oom" -gt 0 ] && deg=1
  [ "$sg_oom" != '?' ] && [ "$sg_oom" -gt 0 ] && deg=1
  [ "$present" -gt 0 ] && deg=1
  [ "$localp" -gt 0 ] && deg=1
  [ "$swap_fail" != '-' ] && [ "$swap_fail" -gt 0 ] && deg=1

  if [ "$j_ok" -eq 0 ] && [ "$cg_ok" -eq 0 ]; then
    MEM_V=BLOCKED
  elif [ "$deg" -gt 0 ] || [ -n "$unk" ]; then
    MEM_V=DEGRADED
  fi

  MEM_NOTE="[${MEM_V}] C1_kernel_oom=$k_oom C2_sysd_oom=$s_oom C3_sigkill=$sg_oom; C4_sweep=$sweep C4_present=$present${names:+[$names]} C4_local=$localp; C5_swap_fail=$swap_fail C5_swap_peak_pct=$swap_pct C5_pswp=$ps_in/$ps_out C5_sock_throttled=$sock; C6_psi_some_avg300=$psi_s C6_psi_full_avg300=$psi_f C6_psi_full_total_us=$psi_t C6_avail_kb=$avail C6_shmem_kb=$shmem; guards=$g_max/$g_high oom.group=$g_grp${unk:+; unknown=[${unk% }]}; r6 vocab: oom-event-plane.md §8"
  return
}

# ---- plane: journal / boot (this-boot triage) --------------------------------
probe_journal() {
  JRN_V=HEALTHY
  local boots=0 cur=no lb_rc=0

  if ! have "$JOURNALCTL"; then
    JRN_V=BLOCKED
    JRN_NOTE='journalctl=missing (probe cannot run)'
    return
  fi

  # arm 1 — boot record: an index-0 (current boot) line must exist (SKILL.md:43)
  cap "$JOURNALCTL" --list-boots --no-pager
  lb_rc=$CAP_RC
  if [ "$lb_rc" -ne 0 ]; then
    JRN_V=BLOCKED
    JRN_NOTE="journalctl --list-boots rc=$lb_rc [boot record unreadable; fails closed]"
    return
  fi
  read -r boots cur < <(printf '%s\n' "$CAP_OUT" \
    | awk 'NF && $1 ~ /^-?[0-9]+$/ { n++; if ($1 == 0) c=1 } END { printf "%d %s\n", n+0, (c ? "yes" : "no") }')
  if [ "$cur" != yes ]; then
    JRN_V=BLOCKED
    JRN_NOTE="boot record missing: boots=$boots, no index-0 (current) line"
    return
  fi

  # arm 2 — boot target reached (SKILL.md:43 "no boot reaches graphical.target")
  local target=$BOOT_TARGET t_word='' t_rc=127
  if have "$SYSTEMCTL"; then
    cap "$SYSTEMCTL" is-active "$target" --no-pager
    t_rc=$CAP_RC
    t_word=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')
  fi
  case "$t_word" in
    active) : ;;
    reloading | activating | inactive | deactivating | failed | maintenance | unknown | refreshing)
      JRN_V=BLOCKED
      JRN_NOTE="boot target $target=$t_word [boot did not reach $target] (is-active rc=$t_rc)"
      return
      ;;
    *)
      JRN_V=BLOCKED
      JRN_NOTE="boot target probe unusable rc=$t_rc [$(printf '%s' "$t_word" | cut -c1-80)]"
      return
      ;;
  esac

  # arm 3 — boot error entries, counted at ENTRY level (`-o json` lines); line counts are
  # traps (SKILL.md:217-220). Classes are disjoint: coredump > kernel > other.
  cap "$JOURNALCTL" -b -p err -o json --no-pager
  local e_rc=$CAP_RC err_n=0 cls='coredump=0 kernel=0 other=0'
  if [ "$e_rc" -ne 0 ]; then
    JRN_V=BLOCKED
    JRN_NOTE="err stream unreadable: journalctl -b -p err rc=$e_rc [fails closed; no fake pass]"
    return
  fi
  err_n=$(nlines "$CAP_OUT")
  if [ "$err_n" -eq 0 ]; then
    # an empty err stream is only a pass if the journal really holds entries this boot
    cap "$JOURNALCTL" -b -n 1 -o json --no-pager
    if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then
      JRN_V=BLOCKED
      JRN_NOTE='journal empty/unreadable this boot (no entries; clean vs no-data cannot be told apart)'
      return
    fi
  else
    cls=$(printf '%s\n' "$CAP_OUT" | awk '
      /"SYSLOG_IDENTIFIER":"systemd-coredump"/ { c++; next }
      /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
      { o++ }
      END { printf "coredump=%d kernel=%d other=%d", c+0, k+0, o+0 }')
  fi

  # arm 4 — failed services HISTORY this boot (journal-derived: units that failed earlier
  # and were reset since are still named; the systemd plane owns the current failed set)
  local fh_n=0 fh_names=''
  fh_n=$(printf '%s\n' "$CAP_OUT" | grep -cE "\"MESSAGE\":\"[^\"]*(${CLASS_FAILED})" || true)
  if [ "$fh_n" -gt 0 ]; then
    fh_names=$(printf '%s\n' "$CAP_OUT" \
      | grep -E "\"MESSAGE\":\"[^\"]*(${CLASS_FAILED})" \
      | grep -oE '[A-Za-z0-9_.@-]+\.(service|socket|timer|mount|target|device|path|scope|slice)' \
      | sort -u | head -n 6 | paste -sd, - || true)
  fi

  # arm 5 — timer drift: every enabled user timer must be armed (ActiveState=active).
  # An unreadable probe is an unresolved unknown -> DEGRADED (mirrors the systemd plane's
  # unreadable-Result semantics), never a silent pass.
  local te=0 ts=0 armed=0 drift=0 t_unknown=0 bad='' r t timers=()
  cap "$SYSTEMCTL" --user list-unit-files --type=timer --state=enabled --no-legend --no-pager
  if [ "$CAP_RC" -ne 0 ]; then
    JRN_V=DEGRADED
    JRN_NOTE="boots=$boots current=$cur target=$target:$t_word err=$err_n ($cls); failedhist=$fh_n${fh_names:+[$fh_names]}; timer plane unreadable [drift unknown]"
    return
  fi
  te=$(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | wc -l)
  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")
  ts=${#timers[@]}
  for t in "${timers[@]}"; do
    cap "$SYSTEMCTL" --user show "$t" -p ActiveState --value --no-pager
    r=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')
    if [ "$CAP_RC" -ne 0 ] || [ -z "$r" ]; then
      t_unknown=$((t_unknown + 1))
    elif [ "$r" = active ]; then
      armed=$((armed + 1))
    else
      drift=$((drift + 1))
      bad="${bad}${t}=${r} "
    fi
  done

  JRN_NOTE="boots=$boots current=$cur target=$target:$t_word err=$err_n ($cls); failedhist=$fh_n${fh_names:+[$fh_names]}; timers_enabled=$te timers_scanned=$ts armed=$armed timer_drift=$drift timer_unknown=$t_unknown"
  [ -n "$bad" ] && JRN_NOTE="$JRN_NOTE (${bad% })"

  if [ "$err_n" -gt 0 ] || [ "$fh_n" -gt 0 ] || [ "$drift" -gt 0 ] || [ "$t_unknown" -gt 0 ]; then JRN_V=DEGRADED; fi
  return
}

# ---- hermetic selftest -------------------------------------------------------
run_selftest() {
  local bin fx
  work=$(mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX)
  trap 'rm -rf -- "${work:-}"' EXIT INT TERM
  bin="$work/bin"
  mkdir -p "$bin" "$work/fx"

  cat > "$bin/.dispatch" <<'STUB'
#!/usr/bin/env bash
# tsukuroi-census selftest fixture dispatcher; answers from $TSUKUROI_FIXTURE only.
set -uo pipefail
name=${0##*/}
fix=${TSUKUROI_FIXTURE:-}
[ -n "$fix" ] || { printf 'fixture dispatcher: TSUKUROI_FIXTURE unset\n' >&2; exit 97; }
rc_of() { local f="$fix/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
out_of() { local f="$fix/$1"; if [ -f "$f" ]; then cat "$f"; fi; }
args="$*"
case "$name" in
  pacman)
    case "${1:-}" in
      -Qq) out_of pq; exit "$(rc_of pq)" ;;
      -Qm) out_of pm; exit "$(rc_of pm)" ;;
      -Qkk) out_of qkk.out; exit "$(rc_of qkk)" ;;
      *) printf 'fixture pacman: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  pacman-conf) out_of pconf; exit "$(rc_of pconf)" ;;
  systemctl)
    case "$args" in
      *is-system-running*) out_of sysrunning; exit "$(rc_of sysrunning)" ;;
      *is-active*) out_of boottarget; exit "$(rc_of boottarget)" ;;
      *list-units*failed*) out_of failedunits; exit "$(rc_of failedunits)" ;;
      *list-unit-files*) out_of timerlist; exit "$(rc_of timerlist)" ;;
      *show*ActiveState*) out_of timeractivestate; exit "$(rc_of timeractivestate)" ;;
      *show*Result*) out_of timerresult; exit "$(rc_of timerresult)" ;;
      *) printf 'fixture systemctl: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  dmesg)
    case "${1:-}" in
      --level*) out_of dmesg.out; exit "$(rc_of dmesg)" ;;
      *) out_of dmesg-all.out; exit "$(rc_of dmesg-all)" ;;
    esac
    ;;
  journalctl)
    case "$args" in
      *--grep*"OOM killer"*) out_of oom-attrib.json; exit "$(rc_of oom-attrib)" ;;
      *--grep*oom_reaper*) out_of oom-kernel.json; exit "$(rc_of oom-kernel)" ;;
      *--grep*"status=9"*) out_of oom-sigkill.json; exit "$(rc_of oom-sigkill)" ;;
      *"--list-boots"*) out_of listboots; exit "$(rc_of listboots)" ;;
      *"-p err"*) out_of journal-err.json; exit "$(rc_of journal-err)" ;;
      *"-n 1"*) out_of journal-last; exit "$(rc_of journal-last)" ;;
      *) out_of journal-all.json; exit "$(rc_of journal-all)" ;;
    esac
    ;;
  nvidia-smi) out_of smi.out; exit "$(rc_of smi)" ;;
  lsmod) out_of lsmod; exit "$(rc_of lsmod)" ;;
esac
printf 'fixture dispatcher: unknown command %s\n' "$name" >&2
exit 96
STUB
  chmod 700 "$bin/.dispatch"
  local c
  for c in pacman pacman-conf systemctl dmesg journalctl nvidia-smi lsmod; do
    ln -s .dispatch "$bin/$c"
  done

  PASS=0 FAIL=0
  ok() { PASS=$((PASS + 1)); printf 'PASS %s\n' "$*"; }
  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }

  fx_default() { # clean fixture: everything passes, dmesg restricted like the measured host
    local d=$1
    mkdir -p "$d/pacmandb" "$d/pci" "$d/dev"
    printf 'alpha\nbeta\ngamma\ndelta\n' > "$d/pq"
    printf 'alpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n' > "$d/qkk.out"
    printf 0 > "$d/qkk.rc"
    : > "$d/pm"
    : > "$d/fbase"
    : > "$d/pconf"
    printf 'HoldPkg = pacman glibc\n' > "$d/pacman.conf"
    printf 'running\n' > "$d/sysrunning"
    printf 0 > "$d/sysrunning.rc"
    : > "$d/failedunits"
    printf 'ai-usage.timer enabled enabled\n' > "$d/timerlist"
    printf 'success\n' > "$d/timerresult"
    printf 1 > "$d/dmesg.rc"
    : > "$d/dmesg.out"
    : > "$d/dmesg-all.out"
    printf 0 > "$d/dmesg-all.rc"
    : > "$d/journal-err.json"
    printf '{"MESSAGE":"fixture: kernel line 1"}\n{"MESSAGE":"fixture: kernel line 2"}\n{"MESSAGE":"fixture: kernel line 3"}\n' > "$d/journal-all.json"
    printf 0 > "$d/journal-err.rc"
    printf 0 > "$d/journal-all.rc"
    : > "$d/smi.out"
    printf 1 > "$d/smi.rc"
    : > "$d/lsmod"
    printf 'fixture-host\n' > "$d/hostname"
    printf 1 > "$d/dmesg_restrict"
    printf 'IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY\n' > "$d/listboots"
    printf ' -1 73a8e2fc20cc48749b3cbd24ed5dc7c1 Sun 2026-10-11 19:02:51 -03 Tue 2026-10-13 10:57:30 -03\n' >> "$d/listboots"
    printf '  0 d7f0bc8d938e4249b4a1f250cbfacf58 Tue 2026-10-13 11:02:03 -03 Wed 2026-10-14 11:42:34 -03\n' >> "$d/listboots"
    printf 0 > "$d/listboots.rc"
    printf 'active\n' > "$d/boottarget"
    printf 0 > "$d/boottarget.rc"
    printf '{"MESSAGE":"fixture: journal last entry"}\n' > "$d/journal-last"
    printf 0 > "$d/journal-last.rc"
    printf 'active\n' > "$d/timeractivestate"
    printf 0 > "$d/timeractivestate.rc"
    # memory-pressure arm fixture (S7-2): quiet cgroup tree, PSI, meminfo and the three
    # journal `--grep` arms — the live host's shape (95 memory.events files) in miniature
    mkdir -p "$d/cgroup/user.slice/user-1000.slice/user@1000.service" "$d/pressure"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/user@1000.service/memory.events"
    printf 'high 0\nmax 0\nfail 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.events"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.peak"
    printf 'pswpin 0\npswpout 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.stat"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.max"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.high"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.oom.group"
    printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n' > "$d/pressure/memory"
    printf 'MemTotal: 1000000 kB\nMemAvailable: 900000 kB\nSwapTotal: 8000000 kB\nSwapFree: 8000000 kB\nShmem: 1000 kB\n' > "$d/meminfo"
    : > "$d/oom-kernel.json"; printf 0 > "$d/oom-kernel.rc"
    : > "$d/oom-attrib.json"; printf 0 > "$d/oom-attrib.rc"
    : > "$d/oom-sigkill.json"; printf 0 > "$d/oom-sigkill.rc"
  }

  fx_hash() { find "$1" -type f -exec sha256sum {} + | LC_ALL=C sort | sha256sum | cut -d' ' -f1; }

  fx_no_mutation() { # assert the fixture tree is byte-identical after a census run
    local d=$1 before=$2 after
    after=$(fx_hash "$d")
    if [ "$after" != "$before" ]; then bad "fixture mutated by census run ($d)"; fi
  }

  EXTRA_ENV=()
  check() { # check LABEL WANT_RC WANT_VERDICT WANT_RE [WANT_RE...]
    local label=$1 wrc=$2 wverdict=$3
    shift 3
    local out rc before re miss=''
    before=$(fx_hash "$FX")
    set +e
    out=$(env \
      TSUKUROI_FIXTURE="$FX" \
      TSUKUROI_PACMAN="$bin/pacman" \
      TSUKUROI_PACMAN_CONF="$bin/pacman-conf" \
      TSUKUROI_PACMAN_CONF_FILE="$FX/pacman.conf" \
      TSUKUROI_PACMAN_DB="$FX/pacmandb" \
      TSUKUROI_FOREIGN_BASELINE="$FX/fbase" \
      TSUKUROI_SYSTEMCTL="$bin/systemctl" \
      TSUKUROI_DMESG="$bin/dmesg" \
      TSUKUROI_JOURNALCTL="$bin/journalctl" \
      TSUKUROI_NVIDIA_SMI="$bin/nvidia-smi" \
      TSUKUROI_LSMOD="$bin/lsmod" \
      TSUKUROI_PCI_SYSFS="$FX/pci" \
      TSUKUROI_DEV_DIR="$FX/dev" \
      TSUKUROI_HOSTNAME_FILE="$FX/hostname" \
      TSUKUROI_DMESG_RESTRICT_FILE="$FX/dmesg_restrict" \
      TSUKUROI_CGROUP_ROOT="$FX/cgroup" \
      TSUKUROI_MEM_SLICE='user.slice/user-1000.slice' \
      TSUKUROI_PRESSURE_FILE="$FX/pressure/memory" \
      TSUKUROI_MEMINFO_FILE="$FX/meminfo" \
      "${EXTRA_ENV[@]}" \
      "$BASH" "$SELF" 2>&1)
    rc=$?
    set -e
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc wanted $wrc; output: $(printf '%s' "$out" | tail -n2 | tr '\n' '|')"
    elif ! printf '%s\n' "$out" | grep -q 'host=fixture-host'; then
      bad "$label: hostname override not honoured — possible host read"
    elif ! printf '%s\n' "$out" | grep -qE "^TSUKUROI_CENSUS: ${wverdict} \("; then
      bad "$label: verdict not ${wverdict}; got: $(printf '%s\n' "$out" | grep '^TSUKUROI_CENSUS:' | head -n1)"
    else
      for re in "$@"; do
        printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss '$re'"
      done
      if [ -n "$miss" ]; then
        bad "$label: plane evidence missing:$miss; got: $(printf '%s\n' "$out" | grep '^PLANE ' | tr '\n' '|')"
      else
        ok "$label (exit $rc, $wverdict)"
      fi
    fi
    fx_no_mutation "$FX" "$before"
    EXTRA_ENV=()
  }

  local case_home='healthy'
  mkdir -p "$work/fx"
  FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: all planes pass' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0'

  case_home='healthy-gpu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA GeForce RTX 5070, 610.57.04\n' > "$FX/smi.out"; printf 0 > "$FX/smi.rc"
  printf 'nvidia 12345678 42\nnvidia_uvm 1234567 0\n' > "$FX/lsmod"
  : > "$FX/dev/nvidia0"; : > "$FX/dev/nvidiactl"
  check 'healthy: nvidia present and answering' 0 HEALTHY \
    '^PLANE drivers: HEALTHY .*nvidia=present'

  case_home='healthy-dmesg'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"; : > "$FX/dmesg.out"
  printf 'fixture kernel line 1\nfixture kernel line 2\nfixture kernel line 3\n' > "$FX/dmesg-all.out"
  printf 0 > "$FX/dmesg-all.rc"
  check 'healthy: unrestricted dmesg ring preferred' 0 HEALTHY 'ring=dmesg .*kerr=0'

  case_home='healthy-benign-backup'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'backup file: alpha: /etc/alpha.conf (Modification time mismatch)\nbackup file: alpha: /etc/alpha.conf (SHA256 checksum mismatch)\nalpha: 10 total files, 0 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'healthy: rc=1 backup-only sample is not a defect' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0 backup_diffs=2'

  case_home='degraded-sample-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'warning: alpha: /usr/bin/alpha (Size mismatch)\nalpha: 10 total files, 1 altered file\nbeta: 20 total files, 2 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'degraded: Qkk sample drift' 1 DEGRADED '^PLANE packages: DEGRADED .*drift=3\[alpha,beta\]'

  case_home='degraded-foreign'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'elephant-a\nelephant-b\nelephant-c\n' > "$FX/pm"
  check 'degraded: foreign packages' 1 DEGRADED '^PLANE packages: DEGRADED .*foreign=3'

  # ---- round 7 foreign watch arm (lane S7-1): the r6 census rows as the accepted
  # baseline, exercised hit / embedded-default / new / version-drift / gone / absent.
  local r6base
  r6base=$(printf '%s\n' \
    'android-apktool-bin 3.0.3-1' 'elephant 2.21.0-1' 'elephant-bluetooth 2.21.0-1' \
    'elephant-calc 2.21.0-1' 'elephant-clipboard 2.21.0-1' 'elephant-desktopapplications 2.21.0-1' \
    'elephant-files 2.21.0-1' 'elephant-menus 2.21.0-1' 'elephant-providerlist 2.21.0-1' \
    'elephant-runner 2.21.0-1' 'elephant-symbols 2.21.0-1' 'elephant-todo 2.21.0-1' \
    'elephant-unicode 2.21.0-1' 'elephant-websearch 2.21.0-1' \
    'obsidian-cli-inspector 1.0.3-1' 'omarchy-walker 1.0.0-2')
  if [ "$(printf '%s\n' "$r6base" | wc -l)" -ne 16 ]; then
    bad 'fixture: r6 baseline literal is not 16 rows'
  fi

  case_home='healthy-foreign-baseline'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'healthy: foreign set equals the accepted baseline (16 rows, hit)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*foreign=16\(known=16 new=0 drift=0 gone=0\) base=file\(16\)'

  case_home='healthy-foreign-embedded'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  EXTRA_ENV=(TSUKUROI_FOREIGN_BASELINE=)
  check 'healthy: embedded r6 snapshot is the default source' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*foreign=16\(known=16 new=0 drift=0 gone=0\) base=r6\(16\)'

  case_home='degraded-foreign-new'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\nnew-tool-bin 4.2-1\n' "$r6base" > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: new foreign arrival is named' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=1 drift=0 gone=0\) base=file\(16\) new=\[new-tool-bin\]'

  case_home='degraded-foreign-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" | sed -E 's/^android-apktool-bin 3\.0\.3-1$/android-apktool-bin 3.0.4-1/' > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: baseline version change shows both versions' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=0 drift=1 gone=0\) base=file\(16\) drift=\[android-apktool-bin\(3\.0\.3-1->3\.0\.4-1\)\]'

  case_home='degraded-foreign-gone'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" | grep -v '^obsidian-cli-inspector ' > "$FX/pm"
  printf '%s\n' "$r6base" > "$FX/fbase"
  check 'degraded: baseline row no longer installed is never silent' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*new=0 drift=0 gone=1\) base=file\(16\) gone=\[obsidian-cli-inspector\]'

  case_home='degraded-foreign-baseline-absent'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' "$r6base" > "$FX/pm"
  EXTRA_ENV=(TSUKUROI_FOREIGN_BASELINE="$FX/fbase-absent")
  check 'degraded: absent baseline never reads HEALTHY' 1 DEGRADED \
    '^PLANE packages: DEGRADED .*foreign=16\(base=absent \[known/new/drift/gone unknown\]\)'

  case_home='degraded-pins'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'linux\n' > "$FX/pconf"
  check 'degraded: declared hold (IgnorePkg)' 1 DEGRADED '^PLANE packages: DEGRADED .*pins=linux'

  case_home='degraded-unit'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'broken.service loaded failed failed fixture failure\n' > "$FX/failedunits"
  check 'degraded: failed unit' 1 DEGRADED '^PLANE systemd: DEGRADED .*failed=1'

  case_home='degraded-timer'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'failed\n' > "$FX/timerresult"
  check 'degraded: timer last run failed' 1 DEGRADED '^PLANE systemd: DEGRADED .*timer_fail=1'

  case_home='degraded-kerr'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"MESSAGE":"Out of memory: Killed process 42"}\n{"MESSAGE":"Buffer I/O error on dev sr0"}\n{"MESSAGE":"other kernel complaint"}\n' > "$FX/journal-err.json"
  check 'degraded: kernel error ring' 1 DEGRADED '^PLANE drivers: DEGRADED .*kerr=3'

  case_home='blocked-lck'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pacmandb/db.lck"
  check 'blocked: pacman db.lck' 2 BLOCKED '^PLANE packages: BLOCKED .*db\.lck=present'

  case_home='blocked-pacman-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PACMAN="$bin/pacman-absent")
  check 'blocked: pacman binary missing' 2 BLOCKED '^PLANE packages: BLOCKED .*pacman=missing'

  case_home='blocked-sample-error'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'error: package %s was not found\n' "'alpha'" > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'blocked: sample probe error' 2 BLOCKED 'sample probe error'

  case_home='blocked-bus'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'Failed to connect to bus: No such file or directory\n' > "$FX/sysrunning"
  printf 1 > "$FX/sysrunning.rc"
  check 'blocked: systemd user bus unreachable' 2 BLOCKED '^PLANE systemd: BLOCKED .*unusable rc=1'

  case_home='blocked-gpu'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA-SMI has failed because it could not communicate with the NVIDIA driver\n' > "$FX/smi.out"
  printf 6 > "$FX/smi.rc"
  check 'blocked: nvidia hardware, driver offline' 2 BLOCKED 'nvidia-smi not answering'

  case_home='blocked-rings'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/dmesg.rc"; printf 1 > "$FX/journal-err.rc"; printf 1 > "$FX/journal-all.rc"
  check 'blocked: both kernel rings unusable' 2 BLOCKED 'kernel ring unusable'

  case_home='blocked-empty-ring'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"; : > "$FX/dmesg.out"; : > "$FX/dmesg-all.out"; printf 0 > "$FX/dmesg-all.rc"
  : > "$FX/journal-all.json"
  check 'blocked: empty ring is not a clean bill' 2 BLOCKED 'kernel ring empty'

  case_home='healthy-journal'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: journal/boot plane in the rollup' 0 HEALTHY \
    '^TSUKUROI_CENSUS: HEALTHY \(packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY\)' \
    '^PLANE journal: HEALTHY \(boots=2 current=yes target=graphical\.target:active err=0 \(coredump=0 kernel=0 other=0\); failedhist=0; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0\)'

  case_home='degraded-boot-errors'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"SYSLOG_IDENTIFIER":"systemd-coredump","MESSAGE":[103,111,100,111,116]}\n{"SYSLOG_IDENTIFIER":"kernel","MESSAGE":"Buffer I/O error on dev sr0"}\n{"SYSLOG_IDENTIFIER":"sddm-helper","MESSAGE":"gkr-pam could not unlock the login keyring"}\n{"SYSLOG_IDENTIFIER":"limine-snapper-sync","MESSAGE":"No Snapper config found"}\n' > "$FX/journal-err.json"
  check 'degraded: journal boot errors at entry level' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*err=4 \(coredump=1 kernel=1 other=2\)'

  case_home='degraded-failedhist'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '{"SYSLOG_IDENTIFIER":"systemd","MESSAGE":"Failed to start foo.service - Foo.","_SYSTEMD_UNIT":"foo.service"}\n{"SYSLOG_IDENTIFIER":"systemd","MESSAGE":"bar.service: Failed with result exit-code."}\n' > "$FX/journal-err.json"
  check 'degraded: failed services history from journal' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*failedhist=2\[bar\.service,foo\.service\]'

  case_home='degraded-timer-drift'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'inactive\n' > "$FX/timeractivestate"
  check 'degraded: enabled timer not armed (drift)' 1 DEGRADED \
    '^PLANE journal: DEGRADED .*timer_drift=1 .*\(ai-usage\.timer=inactive\)'

  case_home='blocked-journal-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_JOURNALCTL="$bin/journalctl-absent")
  check 'blocked: journalctl missing (fails closed)' 2 BLOCKED '^PLANE journal: BLOCKED .*journalctl=missing'

  case_home='blocked-boot-record'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/listboots"
  check 'blocked: boot record missing' 2 BLOCKED '^PLANE journal: BLOCKED .*boot record'

  case_home='blocked-boot-target'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'inactive\n' > "$FX/boottarget"
  printf 3 > "$FX/boottarget.rc"
  check 'blocked: boot target not reached' 2 BLOCKED '^PLANE journal: BLOCKED .*graphical\.target=inactive'

  case_home='blocked-journal-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/journal-err.json"
  : > "$FX/journal-last"
  check 'blocked: empty journal is not a clean bill' 2 BLOCKED '^PLANE journal: BLOCKED .*no entries'

  case_home='blocked-journal-err'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/journal-err.rc"
  check 'blocked: journal err stream unreadable' 2 BLOCKED '^PLANE journal: BLOCKED .*err stream unreadable'

  # ---- round-5 mutation hardening (lane S5-1, 2026-10-14): one case per survivor class
  # from the census-v2 mutation sweep (tameshi's mutate-and-run.sh, 23 single-edit
  # defects, first pass 13 killed / 10 survived — the label suffixes name the defect
  # each case kills): D02 empty local db, D05 nonroot-artifact count, D06 bounded sample
  # size, D09 unreadable timer Result, D10 scope state degraded, D12 missing /dev node,
  # D14/D15 driver class counts, D19 unreadable PCI inventory, D20 journal timer plane.
  case_home='blocked-empty-pkgdb'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/pq"
  check 'blocked: empty local db is not a pass (D02)' 2 BLOCKED \
    '^PLANE packages: BLOCKED .*pacman -Qq listed no packages'

  case_home='healthy-nonroot-artifact'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'warning: alpha: /boot/amd-ucode.img (Permission denied)\nalpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n' > "$FX/qkk.out"
  printf 1 > "$FX/qkk.rc"
  check 'healthy: privilege artifacts counted, not drift (D05)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*drift=0 backup_diffs=0 nonroot_artifacts=1'

  case_home='healthy-sample-bound'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_SAMPLE_N=2)
  check 'healthy: bounded -Qkk sample honors its size (D06)' 0 HEALTHY \
    '^PLANE packages: HEALTHY .*sample=2\(alpha,beta\)'

  case_home='degraded-timer-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  : > "$FX/timerresult"
  check 'degraded: empty timer Result is an unknown, not a failure (D09)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*timer_fail=0 timer_unknown=1'

  case_home='degraded-scope'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'degraded\n' > "$FX/sysrunning"
  printf 1 > "$FX/sysrunning.rc"
  check 'degraded: user scope state degraded (D10)' 1 DEGRADED \
    '^PLANE systemd: DEGRADED .*state=degraded'

  case_home='blocked-no-node'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/pci/0000:01:00.0"; printf '0x10de\n' > "$FX/pci/0000:01:00.0/vendor"
  printf 'NVIDIA GeForce RTX 5070, 610.57.04\n' > "$FX/smi.out"; printf 0 > "$FX/smi.rc"
  printf 'nvidia 12345678 42\n' > "$FX/lsmod"
  check 'blocked: nvidia module loaded but no /dev node (D12)' 2 BLOCKED \
    '^PLANE drivers: BLOCKED .*no /dev/nvidia\* node'

  case_home='degraded-kerr-classes'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"
  printf 'Out of memory: Killed process 42\nBuffer I/O error on dev sr0\nNVRM: Xid 13: graphics fault\nfixture: unattributed kernel error\n' > "$FX/dmesg.out"
  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*kerr=4 \(oom=1 io=1 gpu=1 other=1\)'

  case_home='blocked-pci-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PCI_SYSFS="$FX/no-pci-inventory")
  check 'blocked: unreadable PCI inventory is not a pass (D19)' 2 BLOCKED \
    '^PLANE drivers: BLOCKED .*PCI inventory unreadable'

  case_home='degraded-jrn-timer-plane'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 1 > "$FX/timerlist.rc"
  check 'degraded: journal timer plane unreadable, drift unknown (D20)' 2 BLOCKED \
    '^PLANE journal: DEGRADED .*timer plane unreadable \[drift unknown\]'

  # ---- round 7 memory-pressure arm (lane S7-2): the round-6 OOM-event plane's classes
  # (corpus/knowledge/oom-event-plane.md §8 C1-C6) as live evidence on the drivers line,
  # exercised quiet / presence-flag / classes-with-the-ring / swap anchors / `.local` /
  # named-unknown / blocked.
  case_home='healthy-mem-quiet'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  check 'healthy: memory-pressure arm quiet (S7-2)' 0 HEALTHY \
    '^PLANE drivers: HEALTHY .*mem=\[HEALTHY\] C1_kernel_oom=0 C2_sysd_oom=0 C3_sigkill=0' \
    'mem=\[HEALTHY\].*C4_present=0 C4_local=0; C5_swap_fail=0 C5_swap_peak_pct=0% C5_pswp=0/0' \
    'guards=max/max oom\.group=0; r6 vocab: oom-event-plane\.md §8'

  case_home='degraded-mem-presence'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 7\noom_group_kill 0\nsock_throttled 0\n' \
    > "$FX/cgroup/user.slice/memory.events"
  check 'degraded: memory arm — oom_kill is a presence flag, not a count (S7-2)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*mem=\[DEGRADED\] .*C4_sweep=5 C4_present=1\[user\.slice\] C4_local=0'

  case_home='degraded-mem-classes'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 0 > "$FX/dmesg.rc"
  printf 'Out of memory: Killed process 1732581 (python3)\n' > "$FX/dmesg.out"
  printf '{"MESSAGE":"Out of memory: Killed process 1732581 (python3)"}\n' > "$FX/oom-kernel.json"
  printf '%s\n' '{"MESSAGE":"app.scope: The kernel OOM killer killed some processes in this unit."}' \
    '{"MESSAGE":"user-1000.slice: The kernel OOM killer killed some processes in this unit."}' \
    > "$FX/oom-attrib.json"
  printf '%s\n' '{"MESSAGE":"Main process exited, code=killed, status=9/KILL"}' \
    '{"MESSAGE":"a.service: Failed with result (signal)."}' \
    '{"MESSAGE":"b.scope: Failed with result (oom-kill)."}' > "$FX/oom-sigkill.json"
  check 'degraded: memory arm — ring oom class and C1/C2/C3 reported together (S7-2)' 1 DEGRADED \
    '^PLANE drivers: DEGRADED .*kerr=1 \(oom=1 io=0 gpu=0 other=0\)' \
    'mem=\[DEGRADED\] C1_kernel_oom=1 C2_sysd_oom=2 C3_sigkill=3'

  case_home='degraded-mem-swap'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'high 0\nmax 0\nfail 5922849\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.events"
  printf '36744949760\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.swap.peak"
  printf 'pswpin 72117252\npswpout 93795670\n' > "$FX/cgroup/user.slice/user-1000.slice/memory.stat"
  printf 'SwapTotal: 35917176 kB\nMemAvailable: 19482144 kB\nShmem: 6882556 kB\n' > "$FX/meminfo"
  check 'degraded: memory arm — swap-pressure anchors C5 (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72117252/93795670'

  case_home='degraded-mem-local'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 2\noom_group_kill 0\nsock_throttled 0\n' \
    > "$FX/cgroup/user.slice/memory.events.local"
  check 'degraded: memory arm — memory.events.local flag reported separately (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*C4_present=0 C4_local=1'

  case_home='degraded-mem-psi-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_PRESSURE_FILE="$FX/no-such-pressure")
  check 'degraded: memory arm — unreadable PSI is a named unknown, not a pass (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*unknown=\[C6-psi\]'

  case_home='degraded-mem-slice-unknown'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_MEM_SLICE='user.slice/no-such-slice')
  check 'degraded: memory arm — unreadable slice anchors are a named unknown (S7-2)' 1 DEGRADED \
    'mem=\[DEGRADED\] .*unknown=\[C5-slice\]'

  case_home='blocked-mem-unreadable'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  EXTRA_ENV=(TSUKUROI_CGROUP_ROOT="$FX/no-cgroup" TSUKUROI_JOURNALCTL="$bin/journalctl-absent")
  check 'blocked: memory arm — no cgroup and no journal: no class readable (S7-2)' 2 BLOCKED \
    'mem=\[BLOCKED\]'

  printf 'TSUKUROI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n' \
    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL))" "$PASS" "$FAIL"
  [ "$FAIL" -eq 0 ]
}

# ---- main --------------------------------------------------------------------
main() {
  local selftest=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --selftest) selftest=1; shift ;;
      --sample)
        SAMPLE_N=${2:-}
        case "$SAMPLE_N" in
          '' | *[!0-9]*) printf 'tsukuroi-census: --sample needs a positive integer\n' >&2; exit 2 ;;
        esac
        [ "$SAMPLE_N" -gt 0 ] || { printf 'tsukuroi-census: --sample needs a positive integer\n' >&2; exit 2; }
        shift 2
        ;;
      --help | -h) usage; exit 0 ;;
      *) printf 'tsukuroi-census: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
  done

  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi

  local host
  host=$(head -n1 "$HOSTNAME_FILE" 2>/dev/null | tr -d '\r' || true)
  host=${host:-unknown}
  printf 'tsukuroi-census %s — host=%s — %s — read-only\n' \
    "$VERSION" "$host" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  probe_packages
  probe_systemd
  probe_drivers
  probe_mem_arm
  DRV_V=$(worse "$DRV_V" "$MEM_V")
  probe_journal

  printf 'PLANE packages: %s (%s)\n' "$PKG_V" "$PKG_NOTE"
  printf 'PLANE systemd: %s (%s)\n' "$SYS_V" "$SYS_NOTE"
  printf 'PLANE drivers: %s (%s; mem=%s)\n' "$DRV_V" "$DRV_NOTE" "$MEM_NOTE"
  printf 'PLANE journal: %s (%s)\n' "$JRN_V" "$JRN_NOTE"

  local roll=HEALTHY
  roll=$(worse "$roll" "$PKG_V")
  roll=$(worse "$roll" "$SYS_V")
  roll=$(worse "$roll" "$DRV_V")
  roll=$(worse "$roll" "$JRN_V")

  printf 'TSUKUROI_CENSUS: %s (packages=%s systemd=%s drivers=%s journal=%s)\n' \
    "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V"

  case "$roll" in
    HEALTHY)  exit 0 ;;
    DEGRADED) exit 1 ;;
    BLOCKED)  exit 2 ;;
    *)        exit 2 ;;
  esac
}

main "$@"