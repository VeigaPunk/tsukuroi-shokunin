#!/bin/bash
# C1-9 inner: runs INSIDE a private user+mount namespace as inner-root; builds one scrub view
# on the arm's DEFAULT paths, then drops to inner uid/gid 1 with setpriv and prints $SCRUB_LINE.
set -uo pipefail
umask 022
SCEN=${1:?scenario}
SCRATCH=/fast/scratch/hyaku/tsukuroi-r44/C1ExecHandReproFinal
CENSUS_LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
# the lane tree is not traversable by the caller uid (outer 100000), so the script under test is
# a byte-identical scratch copy; its sha256 is asserted against the lane file below
CENSUS=$SCRATCH/under-test/tsukuroi-census.sh
FX=$SCRATCH/fx
STUB=$SCRATCH/stub-bin
FSID=11111111-2222-3333-4444-555555555555
CALLER_UID=1
CALLER_GID=1

echo "### scenario=$SCEN"
echo "### namespace identity (inner root):"
id
echo "### uid_map:"; cat /proc/self/uid_map
echo "### gid_map:"; cat /proc/self/gid_map

mount -t tmpfs tmpfs /var/lib || { echo "FATAL mount /var/lib"; exit 90; }
mount -t tmpfs tmpfs /etc/systemd/system || { echo "FATAL mount /etc/systemd/system"; exit 90; }
mkdir -p /var/lib/btrfs /etc/systemd/system/timers.target.wants
chmod 755 /var/lib/btrfs /etc/systemd/system/timers.target.wants

wants_link() { ln -s "/usr/lib/systemd/system/$2" "/etc/systemd/system/timers.target.wants/$1"; }

case "$SCEN" in
  rootscrub)
    # root-scrub-like view: real btrfs sysfs root under /sys/fs/btrfs, plus /etc/systemd/system
    mount -t tmpfs tmpfs /sys/fs/btrfs || { echo "FATAL mount /sys/fs/btrfs"; exit 91; }
    mkdir -p "/sys/fs/btrfs/$FSID/devinfo/1" "/sys/fs/btrfs/$FSID/devinfo/2"
    printf '0\n' > "/sys/fs/btrfs/$FSID/devinfo/1/scrub_speed_max"
    printf '52428800\n' > "/sys/fs/btrfs/$FSID/devinfo/2/scrub_speed_max"
    # root scrub writes mode-0600 record files (header contract)
    : > "/var/lib/btrfs/scrub.status.$FSID"; chown 0:0 "/var/lib/btrfs/scrub.status.$FSID"; chmod 600 "/var/lib/btrfs/scrub.status.$FSID"
    # in-progress / failed update
    : > "/var/lib/btrfs/scrub.status.${FSID}_tmp"; chown 0:0 "/var/lib/btrfs/scrub.status.${FSID}_tmp"; chmod 644 "/var/lib/btrfs/scrub.status.${FSID}_tmp"
    # a `btrfs scrub start` progress socket
    python3 -c 'import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1])' "/var/lib/btrfs/scrub.progress.$FSID" || { echo "FATAL socket"; exit 92; }
    chmod 755 "/var/lib/btrfs/scrub.progress.$FSID"
    # a name btrfs-progs never writes: must be ignored
    : > "/var/lib/btrfs/scrub.readme"; chown 0:0 "/var/lib/btrfs/scrub.readme"; chmod 644 "/var/lib/btrfs/scrub.readme"
    # `systemctl enable btrfs-scrub@-.timer`: one instance link, the bare template, an unrelated timer
    wants_link 'btrfs-scrub@-.timer' 'btrfs-scrub@.timer'
    wants_link 'btrfs-scrub@.timer' 'btrfs-scrub@.timer'
    wants_link 'ai-usage.timer' 'ai-usage.timer'
    ;;
  control)
    # same sysfs view as rootscrub, no record/tmp/socket and no enabled timer instance
    mount -t tmpfs tmpfs /sys/fs/btrfs || { echo "FATAL mount /sys/fs/btrfs"; exit 91; }
    mkdir -p "/sys/fs/btrfs/$FSID/devinfo/1" "/sys/fs/btrfs/$FSID/devinfo/2"
    printf '0\n' > "/sys/fs/btrfs/$FSID/devinfo/1/scrub_speed_max"
    printf '52428800\n' > "/sys/fs/btrfs/$FSID/devinfo/2/scrub_speed_max"
    ;;
  sysfsnotdir)
    # sysfs root exists but is NOT a directory
    mount -t tmpfs tmpfs /sys/fs || { echo "FATAL mount /sys/fs"; exit 91; }
    printf '0\n' > /sys/fs/btrfs
    : > "/var/lib/btrfs/scrub.status.$FSID"; chown 0:0 "/var/lib/btrfs/scrub.status.$FSID"; chmod 644 "/var/lib/btrfs/scrub.status.$FSID"
    ;;
  orphan)
    # extra clause probe: a record whose fsid has no entry under the sysfs root is an orphan
    mount -t tmpfs tmpfs /sys/fs/btrfs || { echo "FATAL mount /sys/fs/btrfs"; exit 91; }
    mkdir -p "/sys/fs/btrfs/$FSID/devinfo/1"
    printf '0\n' > "/sys/fs/btrfs/$FSID/devinfo/1/scrub_speed_max"
    : > "/var/lib/btrfs/scrub.status.99999999-8888-7777-6666-555555555555"
    chown 0:0 "/var/lib/btrfs/scrub.status.99999999-8888-7777-6666-555555555555"
    chmod 644 "/var/lib/btrfs/scrub.status.99999999-8888-7777-6666-555555555555"
    ;;
  *) echo "FATAL unknown scenario $SCEN"; exit 93 ;;
esac

echo "### lane file under test (read-only):"
sha256sum "$CENSUS_LANE"
echo "### script actually executed (scratch copy), sha256:"
sha256sum "$CENSUS"
[ "$(sha256sum < "$CENSUS_LANE")" = "$(sha256sum < "$CENSUS")" ] && echo "### COPY_IDENTICAL: YES" || echo "### COPY_IDENTICAL: NO"

echo "### view built (as inner root):"
ls -la /var/lib/btrfs
ls -la /sys/fs/btrfs 2>&1 || true
ls -la /etc/systemd/system/timers.target.wants
snap() { find /var/lib/btrfs /etc/systemd/system -printf '%y %m %U %G %s %p\n' 2>/dev/null; case "$SCEN" in sysfsnotdir) find /sys/fs -maxdepth 1 -printf '%y %m %U %G %s %p\n' 2>/dev/null;; *) find /sys/fs/btrfs -printf '%y %m %U %G %s %p\n' 2>/dev/null;; esac; }
snap | LC_ALL=C sort > "$SCRATCH/pre-$SCEN.snap"
echo "### pre-run view snapshot: $(sha256sum < "$SCRATCH/pre-$SCEN.snap" | cut -d' ' -f1) entries=$(wc -l < "$SCRATCH/pre-$SCEN.snap")"

if [ -e "/var/lib/btrfs/scrub.status.$FSID" ]; then
  mode=$(stat -c %a "/var/lib/btrfs/scrub.status.$FSID")
  echo "### record present mode=$mode; readable by inner root? (expect yes)"
  head -c 0 "/var/lib/btrfs/scrub.status.$FSID" && echo "root-read OK"
  echo "### record (mode=$mode) readable by caller uid=$CALLER_UID gid=$CALLER_GID? (0600 => denial)"
  setpriv --reuid="$CALLER_UID" --regid="$CALLER_GID" --clear-groups -- \
    bash -c 'head -c 0 "/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555" && echo CALLER-READ-OK' 2>&1
else
  echo "### no record in this view"
fi
echo "### caller identity:"
setpriv --reuid="$CALLER_UID" --regid="$CALLER_GID" --clear-groups -- id

# --- the arm's own variable, printed as the unprivileged caller, on the DEFAULT paths ---
echo "### arm source: awk '/^probe_scrub_record\\(\\) \\{/,/^\\}$/' \$CENSUS  (integrated file)"
awk '/^probe_scrub_record\(\) \{/,/^\}$/' "$CENSUS" > "$SCRATCH/arm-probe.sh"
echo "### arm-probe.sh sha256: $(sha256sum "$SCRATCH/arm-probe.sh" | cut -d' ' -f1)  lines=$(wc -l < "$SCRATCH/arm-probe.sh")"
var_line=$(setpriv --reuid="$CALLER_UID" --regid="$CALLER_GID" --clear-groups -- \
  bash -c '. "$1"; SCRUB_DIR=/var/lib/btrfs; BTRFS_SYSFS=/sys/fs/btrfs; TIMER_WANTS=/etc/systemd/system/timers.target.wants; probe_scrub_record; printf "%s\n" "$SCRUB_LINE"' _ "$SCRATCH/arm-probe.sh")
arm_rc=$?
echo "SCRUB_LINE_VAR: $var_line"
echo "### arm_rc=$arm_rc"

# --- contract: records are read "by name and stat, never by content" ---
echo "### strace of the arm as caller uid=$CALLER_UID (file syscalls), log=$SCRATCH/strace-$SCEN.log"
: > "$SCRATCH/strace-$SCEN.log"; chmod 666 "$SCRATCH/strace-$SCEN.log"  # uid 1 writes the log
setpriv --reuid="$CALLER_UID" --regid="$CALLER_GID" --clear-groups -- \
  strace -f -qq -e trace=openat,newfstatat,getdents64 -o "$SCRATCH/strace-$SCEN.log" \
  bash -c '. "$1"; SCRUB_DIR=/var/lib/btrfs; BTRFS_SYSFS=/sys/fs/btrfs; TIMER_WANTS=/etc/systemd/system/timers.target.wants; probe_scrub_record; printf "%s\n" "$SCRUB_LINE"' _ "$SCRATCH/arm-probe.sh" > /dev/null
echo "### strace log lines: $(wc -l < "$SCRATCH/strace-$SCEN.log")"
echo "### openat on a record/tmp/socket NAME (expect none: stat only):"
grep -E 'openat\(.*scrub\.(status|progress)' "$SCRATCH/strace-$SCEN.log" || echo "none"
echo "### newfstatat count on record/tmp/socket names:"
grep -cE 'newfstatat\(.*scrub\.(status|progress)' "$SCRATCH/strace-$SCEN.log" || true
grep -oE 'newfstatat\(AT_FDCWD, "/var/lib/btrfs[^"]*"' "$SCRATCH/strace-$SCEN.log" | sort | uniq -c || true
echo "### openat of scrub_speed_max (the only content the arm reads):"
grep -oE 'openat\(AT_FDCWD, "/sys/fs/btrfs[^"]*"' "$SCRATCH/strace-$SCEN.log" | sort | uniq -c || echo "none"

# --- the integrated script, live mode, default scrub paths, as the unprivileged caller ---
echo "### census invocation: env <seams> \$(command -v bash) \$CENSUS  (no TSUKUROI_BTRFS_SYSFS / TSUKUROI_SCRUB_DIR / TSUKUROI_TIMER_WANTS)"
out=$SCRATCH/out-$SCEN.txt
setpriv --reuid="$CALLER_UID" --regid="$CALLER_GID" --clear-groups -- \
  env PATH="$STUB:/usr/bin:/bin" \
  TSUKUROI_PACMAN="$STUB/pacman" TSUKUROI_PACMAN_CONF="$STUB/pacman-conf" \
  TSUKUROI_PACMAN_CONF_FILE="$FX/pacman.conf" TSUKUROI_PACMAN_DB="$FX/pacmandb" \
  TSUKUROI_ROOT_DIR="$FX/root" TSUKUROI_FOREIGN_BASELINE="$FX/fbase" \
  TSUKUROI_SYSTEMCTL="$STUB/systemctl" TSUKUROI_DMESG="$STUB/dmesg" \
  TSUKUROI_JOURNALCTL="$STUB/journalctl" TSUKUROI_NVIDIA_SMI="$STUB/nvidia-smi" \
  TSUKUROI_LSMOD="$STUB/lsmod" TSUKUROI_EXPAC="$STUB/expac" \
  TSUKUROI_PCI_SYSFS="$FX/pci" TSUKUROI_DEV_DIR="$FX/dev" \
  TSUKUROI_HOSTNAME_FILE="$FX/hostname" TSUKUROI_DMESG_RESTRICT_FILE="$FX/dmesg_restrict" \
  TSUKUROI_CGROUP_ROOT="$FX/cgroup" TSUKUROI_MEM_SLICE='user.slice/user-1000.slice' \
  TSUKUROI_PRESSURE_FILE="$FX/pressure" TSUKUROI_MEMINFO_FILE="$FX/meminfo" \
  TSUKUROI_VMSTAT_FILE="$FX/vmstat" TSUKUROI_OOM_BASELINE="$FX/obase" \
  TSUKUROI_PACMAN_LOG="$FX/pacman.log" TSUKUROI_ETC_DIR="$FX/etc" \
  TSUKUROI_PROC_MOUNTS="$FX/mounts" \
  /bin/bash "$CENSUS" > "$out" 2>&1
census_rc=$?
echo "### census_rc=$census_rc"
echo "### SCRUB line(s) printed by the integrated script:"
grep -c '^SCRUB ' "$out"
grep '^SCRUB ' "$out"
echo "### rollup line:"
grep '^TSUKUROI_CENSUS: ' "$out"
echo "### all verdict-neutral arm lines (DRIFT/STORAGE/SCRUB):"
grep -E '^(DRIFT|STORAGE|SCRUB) ' "$out"
echo "### PLANE lines:"
grep '^PLANE ' "$out"
echo "### census stderr/intruders (non-expected lines):"
grep -vE '^(PLANE|DRIFT|STORAGE|SCRUB|HANDOFF|TSUKUROI_CENSUS)' "$out" || true

# expected line derived from the census header contract, not from the selftest
case "$SCEN" in
  rootscrub) exp='SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=1 unreadable=1 orphan=0 limited=1 timers=1 detail=11111111:2:speed_max=52428800' ;;
  control)   exp='SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:2:speed_max=52428800' ;;
  sysfsnotdir) exp='SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:not-directory' ;;
  orphan)    exp='SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=1 limited=0 timers=0' ;;
esac
got=$(grep '^SCRUB ' "$out" | head -n1)
echo "### EXPECTED (from header contract): $exp"
echo "### GOT:                            $got"
if [ "$got" = "$exp" ]; then echo "### CONTRACT_MATCH: YES"; else echo "### CONTRACT_MATCH: NO"; fi
echo "### SCRUB_LINE_VAR == line printed by the integrated script? -> $([ "$var_line" = "$got" ] && echo YES || echo NO)"
if [ "$var_line" = "$got" ]; then echo "### ARM_RC=0 and one-line print agree with the integrated output at the same revision"; fi
echo "### line order STORAGE < SCRUB < rollup:"
echo "     STORAGE at line $(grep -n '^STORAGE ' "$out" | cut -d: -f1), SCRUB at line $(grep -n '^SCRUB ' "$out" | cut -d: -f1), rollup at line $(grep -n '^TSUKUROI_CENSUS: ' "$out" | cut -d: -f1)"
snap | LC_ALL=C sort > "$SCRATCH/post-$SCEN.snap"
if cmp -s "$SCRATCH/pre-$SCEN.snap" "$SCRATCH/post-$SCEN.snap"; then
  echo "### ZERO_MUTATION: YES (view byte/type/mode/owner-identical after the live run)"
else
  echo "### ZERO_MUTATION: NO"; diff "$SCRATCH/pre-$SCEN.snap" "$SCRATCH/post-$SCEN.snap"
fi
echo "### END scenario=$SCEN"
