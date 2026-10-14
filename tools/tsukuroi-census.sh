#!/usr/bin/env bash
# tsukuroi-census.sh — three-plane host health census (tsukuroi-shokunin, round 2, TSUKUROI-R2-1).
#
# Answers exactly one question, read-only: "what is the state of the three owned host
# planes right now, and can it be assessed at all from an unprivileged shell".
# It never installs, upgrades, removes, restarts, or writes anything (PROVINCE.md:16-17);
# its whole product is verdict + evidence + suggested operator action.
#
# Plan anchor: plans/round-2.plan.md:3-9 — operability axis, "an executable health census
# (tools/tsukuroi-census.sh — packages/systemd/drivers planes) emits
# TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED with a firmware-style exit map, a hermetic
# --selftest on a fixture tree, and honest verdicts on the live host".
# Anti-claim: plans/round-2.plan.md:8 — any plane unreadable live -> BLOCKED arm fires,
# never a fake pass.
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
#             pacman -Qm | count, pacman-conf IgnorePkg IgnoreGroup, /etc/pacman.conf HoldPkg
#     pass    sample drift == 0 (rc may still be 1: backup-file diffs alone do not set rc —
#             SKILL.md:47-52, "a full sweep rc=1 is not corruption evidence"), foreign == 0,
#             IgnorePkg/IgnoreGroup empty
#     degrade sample drift > 0 (drift is pacman's own "N altered files" counts, which already
#             exclude `backup file:` diffs), foreign > 0 (unowned by any synced repo; the
#             accepted baseline is an operator question, not a script constant), or
#             IgnorePkg/IgnoreGroup non-empty (holds declared, SKILL.md:45), or pins unknown
#     block   pacman binary missing, pacman -Qq fails (local db unreadable), db.lck present
#             (interrupted transaction — SKILL.md:41,45), sample probe emits `error:` or rc
#             outside {0,1}
#     note    the sample is bounded on purpose: the full sweep costs ~17 s warm (SKILL.md:107)
#             and belongs to the operator checklist, not to a gate latency budget. The sample
#             rc never decides anything on its own; the drift count does.
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
# Read-only guarantee: no probe writes; the gate creates no files at all in live mode
# (selftest writes only under a mktemp dir named /tmp/tsukuroi-r2-1-selftest.XXXXXX).
# Secrets are never read: only public package/system unit/driver state is queried.
#
# Hermetic selftest: `--selftest` builds a /tmp fixture tree with a dispatcher stub for
# every probe command and re-invokes this script against it via env overrides. Each case
# asserts exit code + final verdict + plane substring, and asserts the fixture tree is
# byte-unchanged after the run (zero mutation). Every probe command and every host path
# read in live mode has an override below, so the selftest touches no host state:
#   TSUKUROI_PACMAN TSUKUROI_PACMAN_CONF TSUKUROI_PACMAN_CONF_FILE TSUKUROI_PACMAN_DB
#   TSUKUROI_SYSTEMCTL TSUKUROI_DMESG TSUKUROI_JOURNALCTL TSUKUROI_NVIDIA_SMI TSUKUROI_LSMOD
#   TSUKUROI_PCI_SYSFS TSUKUROI_DEV_DIR TSUKUROI_HOSTNAME_FILE TSUKUROI_DMESG_RESTRICT_FILE
#   TSUKUROI_SAMPLE_N TSUKUROI_TIMER_SCAN_MAX TSUKUROI_FIXTURE (selftest only)
#
# Sources: PROVINCE.md:5-12,16-18 · SKILL.md:20-31 (vocabulary), :33-45 (decision table),
# :47-83 (Qkk benign classes), :85-135 (update-safety checklist), :137-172 (boundary rule)
# · AGENTS.md:3-5 · corpus/QUALITY.md:1-5 · corpus/knowledge/package-state-plane.md,
# systemd-user-plane.md, driver-firmware-plane.md · plans/round-2.plan.md:3-9.
set -euo pipefail
umask 077

VERSION='census-v1'
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
SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
TIMER_SCAN_MAX=${TSUKUROI_TIMER_SCAN_MAX:-12}

CLASS_OOM='Out of memory|oom-kill|oom_reaper'
CLASS_IO='I/O error|Buffer I/O error|critical medium error|critical target error'
CLASS_GPU='NVRM|nvidia|NVIDIA|GSP|drm'

# ---- shared state ------------------------------------------------------------
PKG_V=BLOCKED PKG_NOTE='probe not run'
SYS_V=BLOCKED SYS_NOTE='probe not run'
DRV_V=BLOCKED DRV_NOTE='probe not run'

usage() {
  cat <<'EOF'
usage: tsukuroi-census.sh [--selftest] [--sample N] [--help]

  (no flags)   run the live read-only census over packages / systemd-user / drivers
  --selftest   hermetic fixture-tree test of every verdict arm (writes only under
               /tmp/tsukuroi-r2-1-selftest.*); exit 0 pass, 1 fail
  --sample N   packages plane: size of the pacman -Qkk sample (default 8)

Verdict line: TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=.. drivers=..)
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
  PKG_NOTE="$PKG_NOTE; foreign=$foreign_n; pins=${pins_names:-none}; holds=$holds; db.lck=absent"

  if [ "$drift" -gt 0 ]; then PKG_V=DEGRADED; fi
  if [ "$foreign_n" != '0' ]; then PKG_V=DEGRADED; fi
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

# ---- hermetic selftest -------------------------------------------------------
run_selftest() {
  local bin fx
  work=$(mktemp -d /tmp/tsukuroi-r2-1-selftest.XXXXXX)
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
      *list-units*failed*) out_of failedunits; exit "$(rc_of failedunits)" ;;
      *list-unit-files*) out_of timerlist; exit "$(rc_of timerlist)" ;;
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
      *"-p err"*) out_of journal-err.json; exit "$(rc_of journal-err)" ;;
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
  }

  fx_hash() { find "$1" -type f -exec sha256sum {} + | LC_ALL=C sort | sha256sum | cut -d' ' -f1; }

  fx_no_mutation() { # assert the fixture tree is byte-identical after a census run
    local d=$1 before=$2 after
    after=$(fx_hash "$d")
    if [ "$after" != "$before" ]; then bad "fixture mutated by census run ($d)"; fi
  }

  EXTRA_ENV=()
  check() { # check LABEL WANT_RC WANT_VERDICT WANT_RE
    local label=$1 wrc=$2 wverdict=$3 wre=$4 out rc before
    before=$(fx_hash "$FX")
    set +e
    out=$(env \
      TSUKUROI_FIXTURE="$FX" \
      TSUKUROI_PACMAN="$bin/pacman" \
      TSUKUROI_PACMAN_CONF="$bin/pacman-conf" \
      TSUKUROI_PACMAN_CONF_FILE="$FX/pacman.conf" \
      TSUKUROI_PACMAN_DB="$FX/pacmandb" \
      TSUKUROI_SYSTEMCTL="$bin/systemctl" \
      TSUKUROI_DMESG="$bin/dmesg" \
      TSUKUROI_JOURNALCTL="$bin/journalctl" \
      TSUKUROI_NVIDIA_SMI="$bin/nvidia-smi" \
      TSUKUROI_LSMOD="$bin/lsmod" \
      TSUKUROI_PCI_SYSFS="$FX/pci" \
      TSUKUROI_DEV_DIR="$FX/dev" \
      TSUKUROI_HOSTNAME_FILE="$FX/hostname" \
      TSUKUROI_DMESG_RESTRICT_FILE="$FX/dmesg_restrict" \
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
    elif ! printf '%s\n' "$out" | grep -qE -- "$wre"; then
      bad "$label: plane evidence '$wre' absent; got: $(printf '%s\n' "$out" | grep '^PLANE ' | tr '\n' '|')"
    else
      ok "$label (exit $rc, $wverdict)"
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

  printf 'PLANE packages: %s (%s)\n' "$PKG_V" "$PKG_NOTE"
  printf 'PLANE systemd: %s (%s)\n' "$SYS_V" "$SYS_NOTE"
  printf 'PLANE drivers: %s (%s)\n' "$DRV_V" "$DRV_NOTE"

  local roll=HEALTHY
  roll=$(worse "$roll" "$PKG_V")
  roll=$(worse "$roll" "$SYS_V")
  roll=$(worse "$roll" "$DRV_V")

  printf 'TSUKUROI_CENSUS: %s (packages=%s systemd=%s drivers=%s)\n' \
    "$roll" "$PKG_V" "$SYS_V" "$DRV_V"

  case "$roll" in
    HEALTHY)  exit 0 ;;
    DEGRADED) exit 1 ;;
    BLOCKED)  exit 2 ;;
    *)        exit 2 ;;
  esac
}

main "$@"