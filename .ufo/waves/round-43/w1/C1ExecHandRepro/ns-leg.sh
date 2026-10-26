#!/bin/bash
# Runs INSIDE a private user+mount namespace (created by run-leg.sh).
# $1 = scenario name, $2 = uid to drop to before calling (empty = stay ns root)
# Echoes one line per (script,scenario) measurement plus the raw find diagnostics.
set -uo pipefail

SCEN=$1
DROP=${2:-}

BT=$(awk '/^btime /{print $2; exit}' /proc/stat)
echo "PROBE btime=$BT scenario=$SCEN drop_uid=${DROP:-none} ns_uid=$(id -u) propagation=$(findmnt -no PROPAGATION /)"
echo "PROBE find=$(command -v find) version=$(find --version 2>&1 | head -1)"
echo "PROBE grep=$(command -v grep) version=$(grep --version 2>&1 | head -1)"

# Do not let anything we mount here leak into the host mount namespace.
mount --make-rprivate / || { echo "FATAL make-rprivate"; exit 90; }

OLD=$((BT - 5000))
NEW=$((BT + 100))

mount -t tmpfs -o size=32m tmpfs /etc || { echo "FATAL mount /etc"; exit 91; }
mount -t tmpfs -o size=8m  tmpfs /usr/lib/initcpio || { echo "FATAL mount initcpio"; exit 92; }
mount -t tmpfs -o size=8m  tmpfs /usr/lib/modules  || { echo "FATAL mount modules"; exit 93; }
chmod 0755 /etc /usr/lib/initcpio /usr/lib/modules

mkdir -p /etc/repro
cp /fast/scratch/hyaku/base-boot-chain-audit.sh /etc/repro/base.sh
cp /fast/scratch/hyaku/fix-boot-chain-audit.sh  /etc/repro/fix.sh
# strip the final `main "$@"` line: these are libraries, we call boot_inputs_newer directly
sed '$ d' /etc/repro/base.sh > /etc/repro/base-lib.sh
sed '$ d' /etc/repro/fix.sh  > /etc/repro/fix-lib.sh
grep -c '^main "\$@"$' /etc/repro/base-lib.sh /etc/repro/fix-lib.sh || true

# --- the six declared boot-chain start points, minus crypttab (scenario decides that one)
: >/etc/fstab
: >/etc/mkinitcpio.conf
mkdir -p /etc/mkinitcpio.conf.d
: >/etc/mkinitcpio.conf.d/hosted.conf
mkdir -p /etc/default
: >/etc/default/limine
: >/etc/limine-snapper-sync.conf
# /etc/crypttab is ABSENT only in the failopen scenario (that absence is the trigger)
case $SCEN in
    crypttab-known|nothing-newer|unreadable-dir) : >/etc/crypttab ;;
    *) : ;;
esac

# --- /usr/lib/initcpio population
: >/usr/lib/initcpio/install-old
# --- /usr/lib/modules population
case $SCEN in
    nothing-newer) mkdir -p /usr/lib/modules/6.0.0-old; : >/usr/lib/modules/6.0.0-old/modules.dep ;;
    *) mkdir -p /usr/lib/modules/7.2.11-arch1-1; : >/usr/lib/modules/7.2.11-arch1-1/modules.dep ;;
esac

# --- every file old, then every directory old (start points are directories too)
find /etc /usr/lib/initcpio /usr/lib/modules -exec touch -h -d "@$OLD" {} +
case $SCEN in
    failopen|crypttab-known|unreadable-dir)
        # only the FILE is newer; every directory keeps its old mtime (a newer directory
        # would itself match and -quit before find ever reaches the missing start point)
        touch -d "@$NEW" /usr/lib/modules/7.2.11-arch1-1/modules.dep
        ;;
    *) : ;;
esac
chmod 0755 /etc/repro; chmod 0644 /etc/repro/*.sh

echo "--- find, exactly as both versions invoke it (start points in the script's order)"
find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
     /etc/default/limine /etc/limine-snapper-sync.conf \
     /usr/lib/initcpio /usr/lib/modules \
     -newermt "@$BT" -print -quit 2>/dev/null
echo "FIND_RC=$?"
echo "--- same find with stderr kept"
find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
     /etc/default/limine /etc/limine-snapper-sync.conf \
     /usr/lib/initcpio /usr/lib/modules \
     -newermt "@$BT" -print -quit
echo "FIND_RC_STDERR=$?"
echo "--- pipefail demonstration, base form vs fix form"
( set -o pipefail
  find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
       /etc/default/limine /etc/limine-snapper-sync.conf \
       /usr/lib/initcpio /usr/lib/modules \
       -newermt "@$BT" -print -quit 2>/dev/null | grep -q . )
echo "BASE_PIPELINE_RC=$?"

if [ "$SCEN" = unreadable-dir ]; then
    chmod 0700 /etc/mkinitcpio.conf.d   # unreadable to a non-root in-namespace uid
    echo "NOTE mkinitcpio.conf.d mode $(stat -c %a /etc/mkinitcpio.conf.d) owner $(stat -c %u /etc/mkinitcpio.conf.d)"
fi

call_as() { # <script-lib> ; prints got=<0|1>
    local lib=$1 got
    # shellcheck disable=SC1090
    got=$(
        set -uo pipefail
        . "$lib"
        boot_inputs_newer
    )
    printf 'got=%s fixture_mode=%s BOOTCHAIN_FIXTURE=%s\n' "$got" \
        "$( ( . "$lib"; fixture_mode && echo true || echo false ) )" "${BOOTCHAIN_FIXTURE:-<unset>}"
}

if [ -z "$DROP" ]; then
    echo "MEASURE scenario=$SCEN uid=$(id -u) base $(call_as /etc/repro/base-lib.sh)"
    echo "MEASURE scenario=$SCEN uid=$(id -u) fix  $(call_as /etc/repro/fix-lib.sh)"
else
    echo "--- the same find invoked as the unprivileged uid (this is what boot_inputs_newer runs)"
    setpriv --reuid "$DROP" --regid "$DROP" --clear-groups /usr/bin/bash -c '
        set -uo pipefail
        echo "diag_uid=$(id -u)"
        find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
             /etc/default/limine /etc/limine-snapper-sync.conf \
             /usr/lib/initcpio /usr/lib/modules \
             -newermt "@'"$BT"'" -print -quit
        echo "DIAG_FIND_RC=$?"
        ( set -o pipefail
          find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
               /etc/default/limine /etc/limine-snapper-sync.conf \
               /usr/lib/initcpio /usr/lib/modules \
               -newermt "@'"$BT"'" -print -quit 2>/dev/null | grep -q . )
        echo "DIAG_PIPELINE_RC=$?"'
    for tag in base fix; do
        out=$(setpriv --reuid "$DROP" --regid "$DROP" --clear-groups /usr/bin/bash -c '
            set -uo pipefail
            . "/etc/repro/'"$tag"'-lib.sh"
            printf "uid=%s got=%s fixture_mode=%s BOOTCHAIN_FIXTURE=%s\n" "$(id -u)" "$(boot_inputs_newer)" \
                "$(fixture_mode && echo true || echo false)" "${BOOTCHAIN_FIXTURE:-<unset>}"')
        echo "MEASURE scenario=$SCEN $tag setpriv:$out"
    done
fi
echo "DONE scenario=$SCEN"
