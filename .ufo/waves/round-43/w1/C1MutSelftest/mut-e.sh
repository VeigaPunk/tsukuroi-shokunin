#!/usr/bin/env bash
# boot-chain-audit.sh — per-limine-entry next-boot verdict audit
# (tsukuroi-shokunin, round 17, seat BootAuditTool; lane TsukuroiR17).
#
# Answers exactly one question, read-only: "for every kernel entry limine will offer at
# the next boot, is the initramfs root path consistent with the late hooks' root path,
# and which entries carry an unproven or unclassified combination?"
#
# The axis: after the operator's 2026-10-20 09:15 `pacman -Syu` (mkinitcpio 41.1 -> 42.2,
# linux 7.2.3 -> 7.2.11), freshly built UKIs mount the real root at /sysroot while the
# configured late hooks (btrfs-overlayfs:4, plymouth:11) still address /new_root. In the
# 42.2 images the extracted /new_root is a symlink to sysroot (mkinitcpio's
# init_functions:1212-1213 creates it), which keeps the hooks working — the v1 reading of
# /new_root as an empty directory was superseded by the namespace emulation evidence in
# .ufo/waves/round-17/l1-capture/overlay-emulation.txt. This tool derives that per limine
# entry from image bytes only; it predicts nothing it cannot read.
#
# Verdict rules (corpus/knowledge/boot-chain-r17.json, schema tsukuroi-boot-chain-v2,
# first match wins):
#   1. efi_path is not a kernel UKI                 -> NOT-A-KERNEL-ENTRY
#   2. selected_this_boot (firmware LoaderEntrySelected or LimineLastBootedEntry names the
#      entry's menu path), the image's file mtime is before boot start (the file that
#      booted), and no /etc or /usr boot-chain input is newer than boot start
#                                                 -> BOOTED-OBSERVED
#   3. snapshot is null and selected_this_boot is false
#                                                 -> UNTESTED
#   4. init_sysroot_refs > 0, init_new_root_refs == 0, image_new_root == symlink->sysroot,
#      both hook roots == /new_root               -> PATH-ALIASED-EMULATED
#   5. init_new_root_refs > 0, init_sysroot_refs == 0, image_new_root == directory,
#      both hook roots == /new_root               -> CONSISTENT-PRE42
#   6. otherwise                                  -> UNTESTED
#
# "Kernel UKI" is decided from the image bytes: every mkinitcpio 42 UKI carries a `.uname`
# PE section (mkinitcpio:541); a PE that lacks it (the /EFI/BOOT/BOOTX64.EFI limine loader
# fallback) is NOT-A-KERNEL-ENTRY. Any entry the tool cannot evaluate (unreadable file,
# unextractable image, missing init or VERSION in the extracted tree, unreadable
# limine.conf, unvalidated path) reports EVALUATION-ERROR, counts as `unknown`, and forces
# the summary UNKNOWN — never a fake pass. A kernel entry that lands on rule 6 while it
# is a snapshot entry or is firmware-selected is an unclassified combination: the verdict
# stays UNTESTED but it also counts as `unknown`, so the summary can never read
# CONSISTENT over a combination the rules do not name.
#
# Selected-entry resolution: limine names booted menu entries by their menu path; this
# host shows LoaderEntrySelected "Omarchy.linux" and LimineLastBootedEntry
# "Omarchy/linux" (supplement-capture.txt). The tool builds each entry's menu path from
# the `/`-stack it was parsed under (components without their leading slashes, `+`
# stripped) and accepts either a `/` or a `.` join as the firmware spelling.
#
# Booted-file stability: rule 2 requires the image file's mtime to be before boot start.
# The booted file's sha256 is not separately observable (the ESP namespace is unreadable
# from an unprivileged shell), so rule 2's sha-equality clause is carried by identifying
# the firmware-selected path and proving that file unchanged: mtime before boot start and
# no newer /etc or /usr boot-chain input. The ESP is mounted fmask/dmask=0077 under a 0700
# /boot on this host, so the mtime is read with `sudo -n stat -c %Y` (L1 integration fix,
# round 17: the unprivileged stat always failed and BOOTED-OBSERVED was unreachable); if
# that read fails the proven-booted flag stays false and the selected entry falls through
# to the rules below (typically PATH-ALIASED-EMULATED for a 42.2 image). The `selected`
# TSV column still reports the firmware fact. The /etc+/usr input set is: /etc/fstab /etc/crypttab /etc/mkinitcpio.conf
# /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio
# /usr/lib/modules (every kernel tree, not only the running one: round-19 falsify
# FxRevAuditRules showed a newer linux-lts module tree was invisible to the old
# <uname -r> path). An image under EFI/Linux whose .uname cannot be extracted is an
# EVALUATION-ERROR (UNKNOWN), never a non-kernel app.
# limine.conf itself is deliberately excluded: a post-boot rewrite changes the menu, not
# the booted image, and this audit is exactly about the menu change.
#
# Output (stdout): a TSV header, one TSV row per limine `path:` record, a `# counts ...`
# line, then exactly one `TSUKUROI_BOOTCHAIN: CONSISTENT|DEGRADED|UNKNOWN`.
# Columns, in order:
#   label efi sha256 b2_ok uname VERSION init_sysroot_refs init_new_root_refs
#   image_new_root latehooks overlay_root plymouth_root rootflags snapshot snapshot_ro
#   selected verdict
# `b2_ok` is `ok` when the computed b2sum equals the 128-hex hash limine.conf pins,
# `MISMATCH` when it does not, `-` when the entry carries no hash; it is reported, never
# a verdict input. `image_new_root` is `symlink->sysroot`, `symlink-><other target>`,
# `directory`, `other`, `absent`, or `-` for non-kernel/unextracted entries. `snapshot` is
# the snapper number parsed from rootflags; `snapshot_ro` the btrfs `ro` property when
# readable, `-` otherwise (report-only; v2 rules do not consume it). `selected` is the
# firmware efivar fact.
#
# Exit map: 0 CONSISTENT | 1 DEGRADED | 2 UNKNOWN.
#   UNKNOWN wins over CONSISTENT: any EVALUATION-ERROR, any unclassified combination
#   (rule-6 UNTESTED on a snapshot or selected entry), zero kernel entries, or an
#   unreadable limine.conf. DEGRADED is kept in the vocabulary for forward compatibility;
#   no v2 verdict maps to it, so exit 1 is never emitted under this schema.
#   Usage errors also exit 2.
#
# Modes:
#   --live      audit the running host under the sentinel contract:
#               * refuses to run as root (EUID 0) — an unprivileged audit cannot write
#                 outside its mktemp tree by accident of privilege;
#               * the ONLY privileged steps are `sudo -n cat -- <efi> > <work>/copy` per
#                 image, `sudo -n cat -- /boot/limine.conf` and `sudo -n stat -c %Y` of each
#                 image (stdout only); every hash, objcopy and lsinitcpio runs unprivileged
#                 on the copy;
#               * `path:` values are validated against
#                 ^boot\(\):/[A-Za-z0-9._/-]+(#[0-9a-f]{128})?$ and `..` components are
#                 rejected; nothing else is interpreted or sourced;
#               * each image is extracted one at a time inside a subshell cd'd into its
#                 own private mktemp directory, never with `lsinitcpio -a`, and no
#                 extracted file is ever sourced;
#               * every removal runs a guarded rm that refuses paths outside the private
#                 work tree, after `chmod -R u+w` on exactly the mktemp path.
#   --selftest  hermetic: fake limine.conf files and fake extracted-initramfs trees under
#               a mktemp directory; asserts parser, verdict function, analyzer and the
#               whole audit pipeline against >= 12 independently fixed expectations,
#               including a config containing `$(touch canary)` that must leave no canary.
#               No sudo, no /boot, no host read. Exit 0 pass, 1 fail, 2 harness error.
#   --help      this text.
#
# Fixture overrides (selftest only; a non-empty BOOTCHAIN_FIXTURE makes every host read
# take its fixture branch, and --live refuses while it is set). <fx> below is
# $BOOTCHAIN_FIXTURE/$(basename <efi path>):
#   <fx>/sha256           image sha256 column value
#   <fx>/b2sum            image b2sum value
#   <fx>/uname            .uname content -> kernel entry (absence is an error unless a
#                         marker file decides otherwise)
#   <fx>/not-a-uki        marker: this path is not a kernel UKI
#   <fx>/unreadable       marker: the image cannot be read (EVALUATION-ERROR)
#   <fx>/snapshot_ro      btrfs ro value for a snapshot entry
#   <fx>/mtime            file mtime epoch, anything else means unverifiable
#   <fx>/extract/         an extracted initramfs tree (init, VERSION, config, hooks/,
#                         new_root)
#   <fxdir>/loader_entries        firmware-selected menu path strings, one per line
#   <fxdir>/btime                 boot epoch
#   <fxdir>/boot_inputs_newer     0|1
#
# Read-only guarantee: live mode writes only under $WORK (mktemp -d, mode 700, umask 077);
# every privileged command is a `sudo -n cat`/`sudo -n stat` read or a `>` redirect into $WORK. No
# package, service, bootloader, initramfs or kernel state is touched.
#
# Label convention: limine labels are lines of one or more `/` plus a name; nesting depth
# is the slash count. A path-bearing entry nested three or more levels deep is labelled
# `<parent> <leaf>` (limine snapshot layout: `///<date> ////linux`); shallower entries use
# their own label (`//linux`, `/EFI fallback`). This reproduces the limine_label values in
# corpus/knowledge/boot-chain-r17.json. The menu path chain for efivar matching is the
# full ancestor stack regardless of depth.

set -uo pipefail
umask 077

PROG=${0##*/}
WORK=''
IMG_COPY=''
EXTRACT_DIR=''
BOOTCHAIN_FIXTURE=${BOOTCHAIN_FIXTURE:-}
LIVE_CONF=/boot/limine.conf
ESP_ROOT=/boot

# --------------------------------------------------------------------------- helpers

usage() {
    awk 'NR == 1 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "$0"
}

guarded_rm() { # refuse to remove anything except exactly our private mktemp trees
    local p=$1
    [ -n "$p" ] || return 0
    case $p in
        "${WORK:-/nonexistent-work}" | "${WORK:-/nonexistent-work}"/* | \
        "${SELFTEST_TMP:-/nonexistent-selftest}" | "${SELFTEST_TMP:-/nonexistent-selftest}"/*)
            [ -e "$p" ] || return 0
            chmod -R u+rwX -- "$p" 2>/dev/null || true
            rm -rf -- "$p"
            ;;
        *)
            printf '%s: refusing rm of non-work path: %s\n' "$PROG" "$p" >&2
            return 1
            ;;
    esac
}

cleanup() {
    [ -n "$WORK" ] && guarded_rm "$WORK"
}

init_work() { # private work dir; refuse when it cannot be confined to mktemp
    local created
    created=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain.XXXXXX") || return 1
    chmod 700 -- "$created" 2>/dev/null || { rm -rf -- "$created"; return 1; }
    case $created in
        /*) ;;
        *) rm -rf -- "$created"; return 1 ;;
    esac
    WORK=$created
    mkdir -p -- "$WORK/img" "$WORK/copy" || { guarded_rm "$WORK"; return 1; }
    trap cleanup EXIT
    trap 'exit 2' INT TERM HUP
    return 0
}

# Every created path resolves through work_path; absolute input or a `..` component is
# refused so nothing escapes $WORK.
work_path() {
    local rel=$1
    case $rel in
        '' | /* | *..*)
            printf '%s: refusing unsafe work path: %s\n' "$PROG" "$rel" >&2
            return 1
            ;;
    esac
    printf '%s/%s\n' "$WORK" "$rel"
}

fixture_mode() { [ -n "$BOOTCHAIN_FIXTURE" ]; }

fx_dir() { printf '%s/%s\n' "$BOOTCHAIN_FIXTURE" "$(basename -- "$1")"; }

cmdline_token() { # <cmdline> <key> -> first `key=value` value
    local cmdline=$1 key=$2 tok
    local -; set -f   # no pathname expansion of limine.conf text
    for tok in $cmdline; do
        case $tok in
            "$key"=*)
                printf '%s\n' "${tok#*=}"
                return 0
                ;;
        esac
    done
    printf '\n'
}

snapshot_number() { # <rootflags value> -> snapper number, empty when not a snapshot
    local rf=$1
    if [[ $rf =~ \.snapshots/([0-9]+)/snapshot ]]; then
        printf '%s\n' "${BASH_REMATCH[1]}"
    fi
    return 0
}

host_efi() { # conf-relative efi path -> host path (boot(): paths live under the ESP root)
    printf '%s%s\n' "$ESP_ROOT" "$1"
}

snapshot_host_path() { # <rootflags value> -> host path for `btrfs property get -t subvol`
    local rf=$1 sub
    sub=${rf#subvol=}
    sub=${sub%%,*}
    sub=${sub#/}
    sub=${sub#@}
    sub=${sub#/}
    printf '/%s\n' "$sub"
}

# --------------------------------------------------------------------------- primitives
# Each primitive has a live branch and a fixture branch. The fixture branch never calls
# sudo and never touches /boot.

stage_image() { # <efi> -> sets IMG_COPY; only privileged step (sudo -n cat) in live mode
    if fixture_mode; then
        IMG_COPY=''
        [ -f "$(fx_dir "$1")/unreadable" ] && return 1
        return 0
    fi
    local c m1 m2
    c=$(work_path "copy/$ENTRY_IDX.efi") || return 1
    STAGED_MTIME=''
    # Bind the mtime to the copied bytes (wave-2 FxAuditPrivilege finding 1): read it
    # before and after the copy and refuse a file that changed meanwhile.
    m1=$(sudo -n stat -c %Y -- "$(host_efi "$1")" 2>/dev/null) || m1=''
    if sudo -n cat -- "$(host_efi "$1")" >"$c" 2>/dev/null; then
        m2=$(sudo -n stat -c %Y -- "$(host_efi "$1")" 2>/dev/null) || m2=''
        if [ -n "$m1" ] && [ "$m1" != "$m2" ]; then
            return 1
        fi
        STAGED_MTIME=$m1
        IMG_COPY=$c
        return 0
    fi
    return 1
}

entry_sha256() { # <efi> -> hex digest
    if fixture_mode; then
        local f
        f=$(fx_dir "$1")/sha256
        [ -f "$f" ] || return 1
        tr -d '\n' <"$f"
        return 0
    fi
    sha256sum -- "$IMG_COPY" 2>/dev/null | awk '{print $1}'
}

entry_b2sum() { # <efi> -> 128-hex b2sum
    if fixture_mode; then
        local f
        f=$(fx_dir "$1")/b2sum
        [ -f "$f" ] || return 1
        tr -d '\n' <"$f"
        return 0
    fi
    b2sum -- "$IMG_COPY" 2>/dev/null | awk '{print $1}'
}

image_identity() { # <efi> -> kernel | not-kernel | error
    if fixture_mode; then
        local d
        d=$(fx_dir "$1")
        if [ -f "$d/unreadable" ]; then
            printf 'error\n'
        elif [ -f "$d/not-a-uki" ]; then
            printf 'not-kernel\n'
        elif [ -s "$d/uname" ]; then
            printf 'kernel\n'
        elif [ -f "$d/uname" ]; then
            printf 'not-kernel\n'   # same rule as live: an empty .uname is no kernel
        else
            printf 'error\n'
        fi
        return 0
    fi
    local dst
    [ -n "$IMG_COPY" ] || { printf 'error\n'; return 0; }
    dst=$(work_path "img/$ENTRY_IDX.uname") || { printf 'error\n'; return 0; }
    # objcopy exits 0 and writes an empty file when .uname is absent (plain EFI apps such as
    # the Limine fallback BOOTX64.EFI), so a kernel UKI needs a non-empty .uname section.
    # Round-19 falsify (FxScoutAuditRules, FxRevAuditRules): an unparseable image under
    # EFI/Linux must be an evaluation error, not silently subtracted as a non-kernel app,
    # or the summary can read CONSISTENT over an image that was never checked.
    if objcopy -O binary --only-section=.uname "$IMG_COPY" "$dst" 2>/dev/null && [ -s "$dst" ]; then
        printf 'kernel\n'
    else
        case "$1" in
            *[Ee][Ff][Ii]/[Ll]inux/*) printf 'error\n' ;;
            *) printf 'not-kernel\n' ;;
        esac
    fi
}

entry_uname() { # <efi> -> kernel release from the .uname section
    if fixture_mode; then
        tr -d '\n' <"$(fx_dir "$1")/uname"
        return 0
    fi
    tr -d '\0\n' <"$WORK/img/$ENTRY_IDX.uname"
}

extract_entry() { # <efi> -> sets EXTRACT_DIR to a private mktemp extraction dir
    local efi=$1 d img
    EXTRACT_DIR=''
    d=$(mktemp -d "$WORK/tree.XXXXXX") || return 1
    if fixture_mode; then
        if cp -R "$(fx_dir "$efi")/extract/." "$d/" 2>/dev/null; then
            EXTRACT_DIR=$d
            return 0
        fi
        guarded_rm "$d"
        return 1
    fi
    img=$(work_path "img/$ENTRY_IDX.initrd") || { guarded_rm "$d"; return 1; }
    if ! objcopy -O binary --only-section=.initrd "$IMG_COPY" "$img" 2>/dev/null; then
        guarded_rm "$d"
        return 1
    fi
    # lsinitcpio -x extracts into the current directory; run it inside the private tree.
    if (cd -- "$d" && TMPDIR="$WORK" lsinitcpio -x "$img" >/dev/null 2>&1); then
        EXTRACT_DIR=$d
        return 0
    fi
    guarded_rm "$d"
    return 1
}

analyze_tree() { # <tree> -> sysroot TAB newroot TAB VERSION TAB latehooks TAB
                 #           overlay_root TAB plymouth_root TAB new_root_kind
    local tree=$1 sys new version late overlay ply kind tgt
    [ -f "$tree/init" ] || return 1
    [ -f "$tree/VERSION" ] || return 1
    sys=$(grep -oF '/sysroot' "$tree/init" | wc -l | tr -d '[:space:]')
    new=$(grep -oF '/new_root' "$tree/init" | wc -l | tr -d '[:space:]')
    version=$(head -n 1 "$tree/VERSION" | tr -d '[:space:]')
    late='-'
    if [ -f "$tree/config" ]; then
        late=$(sed -n 's/^LATEHOOKS="\(.*\)"$/\1/p' "$tree/config" | head -n 1)
    fi
    [ -n "$late" ] || late='-'
    overlay='-'
    if [ -f "$tree/hooks/btrfs-overlayfs" ]; then
        overlay=$(sed -n 's/^[[:space:]]*root_mnt="\([^"]*\)".*/\1/p' "$tree/hooks/btrfs-overlayfs" | head -n 1)
    fi
    [ -n "$overlay" ] || overlay='-'
    ply='-'
    if [ -f "$tree/hooks/plymouth" ]; then
        ply=$(sed -n 's/.*--new-root-dir=\([^[:space:]"]*\).*/\1/p' "$tree/hooks/plymouth" | head -n 1)
    fi
    [ -n "$ply" ] || ply='-'
    if [ -L "$tree/new_root" ]; then
        tgt=$(readlink -- "$tree/new_root")
        case $tgt in
            sysroot | ./sysroot | /sysroot) kind='symlink->sysroot' ;;
            *) kind="symlink->$tgt" ;;
        esac
    elif [ -d "$tree/new_root" ]; then
        kind='directory'
    elif [ -e "$tree/new_root" ]; then
        kind='other'
    else
        kind='absent'
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$sys" "$new" "$version" "$late" "$overlay" "$ply" "$kind"
    return 0
}

snapshot_ro() { # <efi> <host path> -> true | false | -   (report only)
    if fixture_mode; then
        local f
        f=$(fx_dir "$1")/snapshot_ro
        if [ -f "$f" ]; then
            tr -d '[:space:]' <"$f"
        else
            printf -- '-\n'
        fi
        return 0
    fi
    local out
    command -v btrfs >/dev/null 2>&1 || { printf -- '-\n'; return 0; }
    if ! out=$(btrfs property get -t subvol "$2" ro 2>/dev/null); then
        printf -- '-\n'
        return 0
    fi
    case $out in
        *ro=true*) printf 'true\n' ;;
        *ro=false*) printf 'false\n' ;;
        *) printf -- '-\n' ;;
    esac
}

mtime_for() { # <efi> -> epoch seconds | -   (unverifiable without a readable ESP)
    if fixture_mode; then
        local f
        f=$(fx_dir "$1")/mtime
        if [ -f "$f" ]; then
            tr -d '[:space:]' <"$f"
        else
            printf -- '-\n'
        fi
        return 0
    fi
    # The ESP is root-only (0700 /boot, fmask/dmask 0077): read the mtime with `sudo -n stat`,
    # a metadata read whose output goes only to stdout (no root write into $WORK).
    # The mtime read around the copy in stage_image(), so it describes the hashed bytes.
    if [[ ${STAGED_MTIME:-} =~ ^[0-9]+$ ]]; then
        printf '%s\n' "$STAGED_MTIME"
    else
        printf -- '-\n'
    fi
}

btime_epoch() {
    if fixture_mode; then
        local f
        f="$BOOTCHAIN_FIXTURE/btime"
        if [ -f "$f" ]; then
            tr -d '[:space:]' <"$f"
        else
            printf -- '-\n'
        fi
        return 0
    fi
    awk '/^btime /{print $2; exit}' /proc/stat 2>/dev/null
}

inputs_newer_than() { # <epoch> <start point>... -> 1 when find lists an entry newer than epoch, else 0
    # R43-C1: decide on find's output, never on its exit status. find exits 1 when a start
    # point is missing or a directory is unreadable; under `set -o pipefail` that status used
    # to mask a listed match (`find … | grep -q .`), so a newer input read as "none newer".
    local epoch=$1 hit
    shift
    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
    if [ -n "$hit" ]; then
        printf '1\n'
    else
        printf '0\n'
    fi
}

boot_inputs_newer() { # 0 = no /etc or /usr boot-chain input newer than boot start
    if fixture_mode; then
        local f
        f="$BOOTCHAIN_FIXTURE/boot_inputs_newer"
        if [ -f "$f" ]; then
            tr -d '[:space:]' <"$f"
        else
            printf '0\n'
        fi
        return 0
    fi
    local btime
    btime=$(btime_epoch)
    if [ -z "$btime" ]; then
        printf '1\n'
        return 0
    fi
    inputs_newer_than "$btime" /etc/fstab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d \
        /etc/default/limine /etc/limine-snapper-sync.conf \
        /usr/lib/initcpio /usr/lib/modules
}

loader_entries() { # firmware-selected menu path spellings, one per line
    local v found=0
    if fixture_mode; then
        [ -f "$BOOTCHAIN_FIXTURE/loader_entries" ] && cat -- "$BOOTCHAIN_FIXTURE/loader_entries"
        return 0
    fi
    for v in /sys/firmware/efi/efivars/LoaderEntrySelected-* \
        /sys/firmware/efi/efivars/LimineLastBootedEntry-*; do
        [ -f "$v" ] || continue
        found=1
        tail -c +5 -- "$v" 2>/dev/null | tr -d '\0'
        printf '\n'
    done
    if [ "$found" -eq 0 ] && [ -d /sys/firmware/efi/efivars ]; then
        printf '%s: no LoaderEntrySelected/LimineLastBootedEntry efivar readable; every entry reports selected=false\n' \
            "$PROG" >&2
    fi
}

entry_selected() { # <menu path chain> -> true | false
    local chain=$1 cand_dot sel
    cand_dot=${chain//\//.}
    while IFS= read -r sel; do
        [ -n "$sel" ] || continue
        if [ "$sel" = "$chain" ] || [ "$sel" = "$cand_dot" ]; then
            printf 'true\n'
            return 0
        fi
    done < <(loader_entries)
    printf 'false\n'
}

# --------------------------------------------------------------------------- parser

# parse_limine_conf <conf> -> records:
#   label SOH efi SOH b2 SOH cmdline SOH menu-path chain SOH pathok
# Records use \x01 as the field separator (tabs are IFS whitespace and would collapse
# empty fields in `read`; cmdline is allowed to be empty and must survive). Only `path:`
# lines become records; `cmdline:` attaches to the open record (or the next one if it
# appears before its path). Paths are validated against
# ^boot\(\):/[A-Za-z0-9._/-]+(#[0-9a-f]{128})?$ and `..` is rejected (pathok=0). Comment
# lines and unknown keys are ignored; conf text is data, never evaluated.
parse_limine_conf() {
    local conf=$1 raw line slashes depth name label chain efi b2 cmdline rest pathok
    local cur_label='' cur_efi='' cur_b2='' cur_cmdline='' cur_chain='' cur_pathok=''
    local pending_cmdline='' have=0 i
    local -a stack_label=() stack_name=()

    while IFS= read -r raw || [ -n "$raw" ]; do
        line=${raw#"${raw%%[![:space:]]*}"}
        line=${line%"${line##*[![:space:]]}"}
        case $line in
            '' | '#'*) continue ;;
        esac
        case $line in
            path:*)
                if [ "$have" = 1 ]; then
                    printf '%s\001%s\001%s\001%s\001%s\001%s\n' \
                        "$cur_label" "$cur_efi" "$cur_b2" "$cur_cmdline" "$cur_chain" "$cur_pathok"
                fi
                rest=${line#path:}
                rest=${rest#"${rest%%[![:space:]]*}"}
                if [[ $rest =~ ^boot\(\):/([A-Za-z0-9._/-]+)(#[0-9a-f]{128})?$ ]] &&
                    [[ ${BASH_REMATCH[1]} != *..* ]]; then
                    efi="/${BASH_REMATCH[1]}"
                    b2=${BASH_REMATCH[2]#\#}
                    pathok=1
                else
                    efi=$rest
                    b2=''
                    pathok=0
                fi
                cur_label=$label
                cur_efi=$efi
                cur_b2=$b2
                cur_cmdline=$pending_cmdline
                cur_chain=$chain
                cur_pathok=$pathok
                pending_cmdline=''
                have=1
                ;;
            cmdline:*)
                cmdline=${line#cmdline:}
                cmdline=${cmdline#"${cmdline%%[![:space:]]*}"}
                if [ "$have" = 1 ]; then
                    cur_cmdline=$cmdline
                else
                    pending_cmdline=$cmdline
                fi
                ;;
            /*)
                if [ "$have" = 1 ]; then
                    printf '%s\001%s\001%s\001%s\001%s\001%s\n' \
                        "$cur_label" "$cur_efi" "$cur_b2" "$cur_cmdline" "$cur_chain" "$cur_pathok"
                    have=0
                    pending_cmdline=''
                fi
                slashes=${line%%[!/]*}
                depth=${#slashes}
                name=${line#"$slashes"}
                name=${name#+}
                [ -n "$name" ] || continue
                stack_label[depth]=$line
                stack_name[depth]=$name
                if [ "$depth" -ge 3 ]; then
                    label="${stack_label[depth - 1]:-} $line"
                else
                    label=$line
                fi
                chain=''
                for ((i = 1; i <= depth; i++)); do
                    [ -n "${stack_name[i]:-}" ] && chain+="${chain:+/}${stack_name[i]}"
                done
                ;;
        esac
    done <"$conf"

    if [ "$have" = 1 ]; then
        printf '%s\001%s\001%s\001%s\001%s\001%s\n' \
            "$cur_label" "$cur_efi" "$cur_b2" "$cur_cmdline" "$cur_chain" "$cur_pathok"
    fi
}

# --------------------------------------------------------------------------- verdict
# Schema tsukuroi-boot-chain-v2, rules applied in order.
verdict_for() { # kernel proven_booted selected has_snapshot sysrefs newrefs
                # image_new_root overlay_root plymouth_root
    local kernel=$1 booted=$2 selected=$3 hassnap=$4 sys=$5 new=$6 kind=$7 overlay=$8 ply=$9
    if [ "$kernel" != 1 ]; then
        printf 'NOT-A-KERNEL-ENTRY\n'
        return 0
    fi
    if [ "$booted" = 1 ]; then
        printf 'BOOTED-OBSERVED\n'
        return 0
    fi
    if [ "$hassnap" != 1 ] && [ "$selected" != 1 ]; then
        printf 'UNTESTED\n'
        return 0
    fi
    if [ "$sys" -gt 0 ] && [ "$new" -eq 0 ] && [ "$kind" = 'symlink->sysroot' ] &&
        [ "$overlay" = /new_root ] && [ "$ply" = /new_root ]; then
        printf 'PATH-ALIASED-EMULATED\n'
        return 0
    fi
    if [ "$new" -gt 0 ] && [ "$sys" -eq 0 ] && [ "$kind" = directory ] &&
        [ "$overlay" = /new_root ] && [ "$ply" = /new_root ]; then
        printf 'CONSISTENT-PRE42\n'
        return 0
    fi
    printf 'UNTESTED\n'
}

# --------------------------------------------------------------------------- audit

ENTRY_IDX=0

audit() { # <conf path> -> TSV + counts + summary on stdout; exit 0/1/2
    local conf=$1
    local -a labels=() efis=() shas=() b2oks=() unames=() versions=() sysrefs=() newrefs=()
    local -a kinds=() lates=() overlays=() plies=() rflags=() snaps=() snapros=()
    local -a sels=() mtimes=() kernels=() states=()
    local n=0 l e b c ch ok
    local rootflags sn ident s computed u tup a bb cc dd ee ff kk sel mtime
    local btime newer
    local i booted hassnap sel_flag verdict summary rc
    local booted_n=0 aliased_n=0 pre42_n=0 untested_n=0 notkernel_n=0 unknown_n=0 mismatch_n=0

    while IFS=$'\x01' read -r l e b c ch ok; do
        ENTRY_IDX=$n
        IMG_COPY=''
        labels[n]=$l
        efis[n]=$e
        rootflags=$(cmdline_token "$c" rootflags)
        rflags[n]=$rootflags
        sn=$(snapshot_number "$rootflags")
        snaps[n]=${sn:--}
        shas[n]='-'
        b2oks[n]='-'
        unames[n]='-'
        versions[n]='-'
        sysrefs[n]=0
        newrefs[n]=0
        kinds[n]='-'
        lates[n]='-'
        overlays[n]='-'
        plies[n]='-'
        snapros[n]='-'
        sels[n]=false
        mtimes[n]='-'
        kernels[n]=0
        states[n]=ok

        if [ "$ok" != 1 ]; then
            states[n]=error          # path failed validation (`..`, bad scheme, bad hash)
        elif ! stage_image "$e"; then
            states[n]=error          # unreadable /boot file
        else
            ident=$(image_identity "$e")
            case $ident in
                error) states[n]=error ;;
                *) : ;;
            esac
            if [ "${states[n]}" = ok ]; then
                if s=$(entry_sha256 "$e"); then
                    shas[n]=$s
                else
                    states[n]=error
                fi
            fi
            if [ "${states[n]}" = ok ]; then
                if [ -n "$b" ]; then
                    if computed=$(entry_b2sum "$e") &&
                        [ "${#computed}" -eq 128 ] && [ "$computed" = "${b,,}" ]; then
                        b2oks[n]=ok
                    else
                        b2oks[n]=MISMATCH
                    fi
                fi
                if [ "$ident" = kernel ]; then
                    kernels[n]=1
                    if u=$(entry_uname "$e"); then
                        unames[n]=$u
                    fi
                    if extract_entry "$e"; then
                        if tup=$(analyze_tree "$EXTRACT_DIR"); then
                            IFS=$'\t' read -r a bb cc dd ee ff kk <<<"$tup"
                            sysrefs[n]=$a
                            newrefs[n]=$bb
                            versions[n]=$cc
                            lates[n]=$dd
                            overlays[n]=$ee
                            plies[n]=$ff
                            kinds[n]=$kk
                        else
                            states[n]=error
                        fi
                        guarded_rm "$EXTRACT_DIR"
                        EXTRACT_DIR=''
                    else
                        states[n]=error
                    fi
                    if [ "${states[n]}" = ok ]; then
                        mtimes[n]=$(mtime_for "$e")
                        sels[n]=$(entry_selected "$ch")
                        if [ -n "$sn" ]; then
                            snapros[n]=$(snapshot_ro "$e" "$(snapshot_host_path "$rootflags")")
                        fi
                    fi
                fi
            fi
            if [ -n "$IMG_COPY" ]; then
                guarded_rm "$IMG_COPY"
                IMG_COPY=''
            fi
        fi
        n=$((n + 1))
    done < <(parse_limine_conf "$conf")

    newer=$(boot_inputs_newer)
    btime=$(btime_epoch)

    printf 'label\tefi\tsha256\tb2_ok\tuname\tVERSION\tinit_sysroot_refs\tinit_new_root_refs\timage_new_root\tlatehooks\toverlay_root\tplymouth_root\trootflags\tsnapshot\tsnapshot_ro\tselected\tverdict\n'
    for ((i = 0; i < n; i++)); do
        booted=0
        if [ "${states[i]}" = error ]; then
            verdict=EVALUATION-ERROR
            unknown_n=$((unknown_n + 1))
        else
            hassnap=0
            [ "${snaps[i]}" != '-' ] && hassnap=1
            if [ "${kernels[i]}" = 1 ] && [ "${sels[i]}" = true ] && [ "$newer" = 0 ] &&
                [[ ${mtimes[i]} =~ ^[0-9]+$ ]] && [[ $btime =~ ^[0-9]+$ ]] &&
                [ "${mtimes[i]}" -lt "$btime" ]; then
                booted=1
            fi
            if [ "${sels[i]}" = true ]; then
                sel_flag=1
            else
                sel_flag=0
            fi
            verdict=$(verdict_for "${kernels[i]}" "$booted" "$sel_flag" "$hassnap" \
                "${sysrefs[i]}" "${newrefs[i]}" "${kinds[i]}" "${overlays[i]}" "${plies[i]}")
            case $verdict in
                BOOTED-OBSERVED) booted_n=$((booted_n + 1)) ;;
                PATH-ALIASED-EMULATED) aliased_n=$((aliased_n + 1)) ;;
                CONSISTENT-PRE42) pre42_n=$((pre42_n + 1)) ;;
                UNTESTED) untested_n=$((untested_n + 1)) ;;
                NOT-A-KERNEL-ENTRY) notkernel_n=$((notkernel_n + 1)) ;;
            esac
            # A snapshot or firmware-selected entry that lands on rule 6 is an
            # unclassified combination: it must never pass a CONSISTENT summary.
            if [ "$verdict" = UNTESTED ] && { [ "$hassnap" = 1 ] || [ "$sel_flag" = 1 ]; }; then
                unknown_n=$((unknown_n + 1))
            fi
        fi
        [ "${b2oks[i]}" = MISMATCH ] && mismatch_n=$((mismatch_n + 1))
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
            "${labels[i]}" "${efis[i]}" "${shas[i]}" "${b2oks[i]}" "${unames[i]}" \
            "${versions[i]}" "${sysrefs[i]}" "${newrefs[i]}" "${kinds[i]}" \
            "${lates[i]}" "${overlays[i]}" "${plies[i]}" "${rflags[i]}" "${snaps[i]}" \
            "${snapros[i]}" "${sels[i]}" "$verdict"
    done

    local kernel_eval=$((n - notkernel_n - unknown_n))
    if [ "$unknown_n" -gt 0 ] || [ "$n" -eq 0 ] || [ "$kernel_eval" -le 0 ]; then
        summary=UNKNOWN
        rc=2
    else
        summary=CONSISTENT
        rc=0
    fi
    printf '# counts entries=%d kernels=%d booted=%d path-aliased=%d pre42=%d untested=%d not-kernel=%d unknown=%d b2_mismatch=%d\n' \
        "$n" "$kernel_eval" "$booted_n" "$aliased_n" "$pre42_n" \
        "$untested_n" "$notkernel_n" "$unknown_n" "$mismatch_n"
    printf 'TSUKUROI_BOOTCHAIN: %s\n' "$summary"
    return "$rc"
}

# --------------------------------------------------------------------------- selftest

st_pass=0
st_fail=0
st_total=0

st_check() { # <case name> <expected> <actual>
    st_total=$((st_total + 1))
    if [ "$2" = "$3" ]; then
        st_pass=$((st_pass + 1))
    else
        st_fail=$((st_fail + 1))
        printf 'FAIL %s: expected [%s] got [%s]\n' "$1" "$2" "$3"
    fi
}

mk_init() { # <tree> <sysroot refs> <new_root refs>
    local tree=$1 sys=$2 new=$3 i
    mkdir -p -- "$tree"
    : >"$tree/init"
    for ((i = 0; i < sys; i++)); do
        printf '# mount /sysroot %d\n' "$i" >>"$tree/init"
    done
    for ((i = 0; i < new; i++)); do
        printf '# mount /new_root %d\n' "$i" >>"$tree/init"
    done
}

mk_uki_fx() { # <fxdir> <sha> <b2> <uname> <version> <sys> <new> <overlay> <ply>
              # <new_root kind: symlink|dir|absent|other|symlink->TARGET> [snapro] [mtime]
    local d=$1 sha=$2 b2=$3 uname=$4 version=$5 sys=$6 new=$7 overlay=$8 ply=$9
    local kind=${10:-} snapro=${11:-} mtime=${12:-}
    mkdir -p -- "$d/extract/hooks"
    printf '%s\n' "$sha" >"$d/sha256"
    printf '%s\n' "$b2" >"$d/b2sum"
    printf '%s\n' "$uname" >"$d/uname"
    printf '%s\n' "$version" >"$d/extract/VERSION"
    mk_init "$d/extract" "$sys" "$new"
    printf 'LATEHOOKS="plymouth btrfs-overlayfs"\n' >"$d/extract/config"
    printf '#!/usr/bin/ash\nrun_latehook() {\n\troot_mnt="%s"\n}\n' "$overlay" \
        >"$d/extract/hooks/btrfs-overlayfs"
    printf '#!/usr/bin/ash\nrun_latehook(){\n  plymouth update-root-fs --new-root-dir=%s\n}\n' "$ply" \
        >"$d/extract/hooks/plymouth"
    case $kind in
        symlink)
            mkdir -p -- "$d/extract/sysroot"
            ln -s sysroot "$d/extract/new_root"
            ;;
        dir) mkdir -p -- "$d/extract/new_root" ;;
        other) printf 'x\n' >"$d/extract/new_root" ;;
        'symlink->'* ) ln -s "${kind#symlink->}" "$d/extract/new_root" ;;
        absent) : ;;
        *) : ;;
    esac
    [ -n "$snapro" ] && printf '%s\n' "$snapro" >"$d/snapshot_ro"
    [ -n "$mtime" ] && printf '%s\n' "$mtime" >"$d/mtime"
    return 0
}

st_mk_fallback_fx() { # <fxdir>
    local d=$1
    mkdir -p -- "$d"
    printf 'deadbeef\n' >"$d/sha256"
    printf 'deadbeef\n' >"$d/b2sum"
    : >"$d/not-a-uki"
}

run_selftest() {
    local T fx conf out rc got verdicts row H128
    T=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain-selftest.XXXXXX") || {
        printf 'TSUKUROI_BOOTCHAIN_SELFTEST: FAIL harness (mktemp)\n'
        return 2
    }
    trap 'guarded_rm "${T:-}" 2>/dev/null || true' EXIT
    SELFTEST_TMP=${T:-}
    fx="$T/fixtures"
    mkdir -p -- "$fx"
    BOOTCHAIN_FIXTURE=$fx
    WORK=$T/work
    mkdir -p -- "$WORK" "$WORK/img" "$WORK/copy"
    H128=$(printf 'a%.0s' $(seq 128))

    # ---- parser cases -----------------------------------------------------
    conf="$T/p1.conf"
    cat >"$conf" <<EOF
# comment line with /a/slash
default_entry: 2
timeout: 3
/+Omarchy
//linux
  comment: Kernel version: 7.2.11-arch1-1
  path: boot():/EFI/Linux/omarchy_linux.efi#$H128
  cmdline: quiet rootflags=subvol=@ rw
//lts
  path: boot():/EFI/Linux/omarchy_linux-lts.efi#$H128
  cmdline: quiet rootflags=subvol=@ rw
EOF
    out=$(parse_limine_conf "$conf")
    got=$(printf '%s\n' "$out" | wc -l | tr -d '[:space:]')
    st_check 'p1-record-count' 2 "$got"
    got=$(printf '%s\n' "$out" | sed -n 1p)
    st_check 'p1-first-record' \
        "//linux"$'\x01'"/EFI/Linux/omarchy_linux.efi"$'\x01'"$H128"$'\x01'"quiet rootflags=subvol=@ rw"$'\x01'"Omarchy/linux"$'\x01'1 \
        "$got"

    conf="$T/p2.conf"
    cat >"$conf" <<EOF
/+Omarchy
  //Snapshots
    ///2026-10-20 09:29:19
    comment: pre-aur
    ////linux
    path: boot():/boot-history/omarchy_linux.efi_sha256_2e9c#$H128
    cmdline: quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/2/snapshot rw
EOF
    out=$(parse_limine_conf "$conf")
    got=$(printf '%s\n' "$out" | sed -n 1p)
    st_check 'p2-snapshot-label-and-record' \
        "///2026-10-20 09:29:19 ////linux"$'\x01'"/boot-history/omarchy_linux.efi_sha256_2e9c"$'\x01'"$H128"$'\x01'"quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/2/snapshot rw"$'\x01'"Omarchy/Snapshots/2026-10-20 09:29:19/linux"$'\x01'1 \
        "$got"
    got=$(printf '%s\n' "$out" | while IFS=$'\x01' read -r _ _ _ c _ _; do
        snapshot_number "$(cmdline_token "$c" rootflags)"
    done)
    st_check 'p2-snapshot-number' 2 "$got"

    conf="$T/p3.conf"
    cat >"$conf" <<'EOF'
/EFI fallback
  comment: fallback loader, not a kernel
  path: boot():/EFI/BOOT/BOOTX64.EFI
EOF
    out=$(parse_limine_conf "$conf")
    got=$(printf '%s\n' "$out" | sed -n 1p)
    st_check 'p3-fallback-no-hash' \
        "/EFI fallback"$'\x01'"/EFI/BOOT/BOOTX64.EFI"$'\x01'""$'\x01'""$'\x01'"EFI fallback"$'\x01'1 "$got"

    conf="$T/p4.conf"
    cat >"$conf" <<EOF
default_entry: 2
# //not-a-label
//linux
	comment: indented key, tab
	cmdline: rootflags=subvol=@ rw quiet
	path: boot():/EFI/Linux/omarchy_linux.efi#$H128
EOF
    out=$(parse_limine_conf "$conf")
    got=$(printf '%s\n' "$out" | wc -l | tr -d '[:space:]')
    st_check 'p4-comment-and-indent-count' 1 "$got"
    got=$(printf '%s\n' "$out" | sed -n 1p)
    st_check 'p4-cmdline-before-path' \
        "//linux"$'\x01'"/EFI/Linux/omarchy_linux.efi"$'\x01'"$H128"$'\x01'"rootflags=subvol=@ rw quiet"$'\x01'"linux"$'\x01'1 "$got"

    conf="$T/p5.conf"
    cat >"$conf" <<'EOF'
//bad
  path: boot():/../etc/passwd#eeee
  cmdline: x
//badd
  path: boot():/x.efi#nothex
  cmdline: y
//ok
  path: boot():/x.efi
  cmdline: z
EOF
    out=$(parse_limine_conf "$conf")
    got=$(printf '%s\n' "$out" | awk -F'\x01' '{print $6}' | paste -sd, -)
    st_check 'p5-path-validation' '0,0,1' "$got"

    # ---- selection matching ----------------------------------------------
    printf 'Omarchy.linux\n' >"$fx/loader_entries"
    st_check 's1-selected-dot-match' true "$(entry_selected 'Omarchy/linux')"
    st_check 's2-selected-miss' false "$(entry_selected 'Omarchy/linux-lts')"
    printf 'Omarchy/linux\n' >"$fx/loader_entries"
    st_check 's3-selected-slash-match' true "$(entry_selected 'Omarchy/linux')"
    if guarded_rm /etc/passwd >/dev/null 2>&1; then
        got=allowed
    else
        got=refused
    fi
    st_check 's4-guarded-rm-refuses-outsider' refused "$got"

    # ---- verdict function (schema v2) ------------------------------------
    st_check 'v1-not-a-kernel' NOT-A-KERNEL-ENTRY "$(verdict_for 0 0 0 0 0 0 - - -)"
    st_check 'v2-booted' BOOTED-OBSERVED "$(verdict_for 1 1 1 0 7 0 'symlink->sysroot' /new_root /new_root)"
    st_check 'v3-non-snapshot-not-selected' UNTESTED "$(verdict_for 1 0 0 0 7 0 'symlink->sysroot' /new_root /new_root)"
    st_check 'v4-path-aliased' PATH-ALIASED-EMULATED "$(verdict_for 1 0 0 1 7 0 'symlink->sysroot' /new_root /new_root)"
    st_check 'v5-v42-directory-untested' UNTESTED "$(verdict_for 1 0 0 1 7 0 directory /new_root /new_root)"
    st_check 'v6-consistent-pre42' CONSISTENT-PRE42 "$(verdict_for 1 0 0 1 0 7 directory /new_root /new_root)"
    st_check 'v7-pre42-plymouth-mismatch' UNTESTED "$(verdict_for 1 0 0 1 0 7 directory /new_root /sysroot)"
    st_check 'v8-selected-not-proven-still-aliased' PATH-ALIASED-EMULATED "$(verdict_for 1 0 1 0 7 0 'symlink->sysroot' /new_root /new_root)"
    st_check 'v9-mixed-refs-untested' UNTESTED "$(verdict_for 1 0 0 1 3 3 'symlink->sysroot' /new_root /new_root)"
    st_check 'v10-booted-beats-snapshot' BOOTED-OBSERVED "$(verdict_for 1 1 1 1 7 0 'symlink->sysroot' /new_root /new_root)"

    # ---- extracted-tree analyzer -----------------------------------------
    mk_init "$T/tree-a" 5 2
    printf '42.2\n' >"$T/tree-a/VERSION"
    mkdir -p -- "$T/tree-a/hooks" "$T/tree-a/sysroot"
    ln -s sysroot "$T/tree-a/new_root"
    printf 'run_latehook() {\n\troot_mnt="/new_root"\n}\n' >"$T/tree-a/hooks/btrfs-overlayfs"
    printf '  plymouth update-root-fs --new-root-dir=/new_root\n' >"$T/tree-a/hooks/plymouth"
    printf 'EARLYHOOKS="udev"\nHOOKS="udev encrypt"\nLATEHOOKS="plymouth btrfs-overlayfs"\n' >"$T/tree-a/config"
    got=$(analyze_tree "$T/tree-a")
    st_check 'a1-tree-fields' \
        $'5\t2\t42.2\tplymouth btrfs-overlayfs\t/new_root\t/new_root\tsymlink->sysroot' "$got"

    mk_init "$T/tree-b" 0 0
    printf '41.1\n' >"$T/tree-b/VERSION"
    mkdir -p -- "$T/tree-b/new_root"
    got=$(analyze_tree "$T/tree-b")
    st_check 'a2-tree-directory' $'0\t0\t41.1\t-\t-\t-\tdirectory' "$got"

    # ---- end-to-end: corpus mirror (schema v2 verdicts) -------------------
    local sha_a=2e9c9bdc532bff808af24b7c2b896660835ca965d5dcd9cf731d94e8bf079fe8
    local sha_b=2d49da06b20afd09d9ac3d3a6575d85b8977307d820604bfedc945c4ce97a8b8
    local sha_c=0f1e3c84b2d6db2c2af14cf5f072ab3abdafaeccc883d45805c8850d9bfbdef0
    local b2_a=822299bbdaf0d4ede97d341fd5fcfa73fb3ca3942b7dcc597a79e7b46e69ec8f3eaabb194c431112de1c97b15345f1ca64adb0438b94d8fc8100cd393ce98024
    local b2_b=6c1893df2144b71b7f2fbf95fe61f94aa1178968e002fb86c809581d14512d60130dde89cd21e96392216bb5ae622aede82b1f3e916694f820bf17c780ac03db
    local b2_c=2832912269f8e0f0cd4b7434d126938b9986af3ff3c27737054696daa53aaf9ce18e32edbb99d731f5bf4da7cb86826d754f16627d93619cc5db19e4769bf71c

    mk_uki_fx "$fx/omarchy_linux.efi" "$sha_a" "$b2_a" 7.2.11-arch1-1 42.2 7 0 /new_root /new_root symlink '' 1
    mk_uki_fx "$fx/omarchy_linux-lts.efi" "$sha_b" "$b2_b" 6.18.57-2-lts 42.2 7 0 /new_root /new_root symlink
    mk_uki_fx "$fx/omarchy_linux.efi_sha256_$sha_a" "$sha_a" "$b2_a" 7.2.11-arch1-1 42.2 7 0 /new_root /new_root symlink true
    mk_uki_fx "$fx/omarchy_linux-lts.efi_sha256_$sha_b" "$sha_b" "$b2_b" 6.18.57-2-lts 42.2 7 0 /new_root /new_root symlink true
    mk_uki_fx "$fx/omarchy_linux.efi_sha256_$sha_c" "$sha_c" "$b2_c" 7.2.3-arch1-3 41.1 0 7 /new_root /new_root dir true
    st_mk_fallback_fx "$fx/BOOTX64.EFI"

    printf 'Omarchy.linux\n' >"$fx/loader_entries"
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"

    local e1="$T/e1.conf"
    cat >"$e1" <<EOF
default_entry: 2
/+Omarchy
  //linux
  path: boot():/EFI/Linux/omarchy_linux.efi#$b2_a
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=@ rw
  //linux-lts
  path: boot():/EFI/Linux/omarchy_linux-lts.efi#$b2_b
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=@ rw
     //Snapshots
     ///2026-10-20 09:29:19
     ////linux
     path: boot():/boot-history/omarchy_linux.efi_sha256_$sha_a#$b2_a
     cmdline: quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/2/snapshot rw
     ////linux-lts
     path: boot():/boot-history/omarchy_linux-lts.efi_sha256_$sha_b#$b2_b
     cmdline: quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/2/snapshot rw
     ///2026-10-20 09:03:02
     ////linux
     path: boot():/boot-history/omarchy_linux.efi_sha256_$sha_c#$b2_c
     cmdline: quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/1/snapshot rw
/EFI fallback
  path: boot():/EFI/BOOT/BOOTX64.EFI
EOF
    out=$(audit "$e1")
    rc=$?
    verdicts=$(printf '%s\n' "$out" | awk -F'\t' 'NR>1 && $1 !~ /^#/ && $1 !~ /^TSUKUROI/ {print $17}' | paste -sd, -)
    st_check 'e1-verdict-sequence' \
        'BOOTED-OBSERVED,UNTESTED,PATH-ALIASED-EMULATED,PATH-ALIASED-EMULATED,CONSISTENT-PRE42,NOT-A-KERNEL-ENTRY' \
        "$verdicts"
    got=$(printf '%s\n' "$out" | sed -n 's/^TSUKUROI_BOOTCHAIN: //p')
    st_check 'e1-summary' CONSISTENT "$got"
    st_check 'e1-exit' 0 "$rc"
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR>1 && $1 !~ /^#/ && $1 !~ /^TSUKUROI/ {print $9}' | paste -sd, -)
    st_check 'e1-newroot-kinds' \
        'symlink->sysroot,symlink->sysroot,symlink->sysroot,symlink->sysroot,directory,-' "$got"
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR>1 && $1 !~ /^#/ && $1 !~ /^TSUKUROI/ {print $16}' | paste -sd, -)
    st_check 'e1-selected-column' 'true,false,false,false,false,false' "$got"

    # ---- end-to-end: consistent fallback-only host -----------------------
    rm -rf -- "$fx"
    mkdir -p -- "$fx"
    mk_uki_fx "$fx/old.efi" "$sha_c" "$b2_c" 7.2.3-arch1-3 41.1 0 7 /new_root /new_root dir
    st_mk_fallback_fx "$fx/BOOTX64.EFI"
    printf 'Omarchy.linux\n' >"$fx/loader_entries"
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e2="$T/e2.conf"
    cat >"$e2" <<EOF
//old
  path: boot():/EFI/Linux/old.efi#$b2_c
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=@ rw
/EFI fallback
  path: boot():/EFI/BOOT/BOOTX64.EFI
EOF
    out=$(audit "$e2")
    rc=$?
    got=$(printf '%s\n' "$out" | sed -n 's/^TSUKUROI_BOOTCHAIN: //p')
    st_check 'e2-summary' CONSISTENT "$got"
    st_check 'e2-exit' 0 "$rc"

    # ---- end-to-end: unreadable entry ------------------------------------
    rm -rf -- "$fx"
    mkdir -p -- "$fx/broken.efi"
    : >"$fx/broken.efi/unreadable"
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e3="$T/e3.conf"
    cat >"$e3" <<EOF
//broken
  path: boot():/EFI/Linux/broken.efi#$H128
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=@ rw
EOF
    out=$(audit "$e3")
    rc=$?
    got=$(printf '%s\n' "$out" | sed -n 's/^TSUKUROI_BOOTCHAIN: //p')
    st_check 'e3-summary' UNKNOWN "$got"
    st_check 'e3-exit' 2 "$rc"
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR==2 {print $17}')
    st_check 'e3-verdict' EVALUATION-ERROR "$got"

    # ---- end-to-end: empty .uname is not a kernel (live/fixture parity) ---
    rm -rf -- "$fx"
    mkdir -p -- "$fx/plain.efi"
    printf 'cafe\n' >"$fx/plain.efi/sha256"
    printf 'cafe\n' >"$fx/plain.efi/b2sum"
    : >"$fx/plain.efi/uname"
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e5="$T/e5.conf"
    cat >"$e5" <<EOF
/plain
  path: boot():/EFI/BOOT/plain.efi
EOF
    out=$(audit "$e5")
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR==2 {print $17}')
    st_check 'e5-empty-uname-not-kernel' NOT-A-KERNEL-ENTRY "$got"

    # ---- end-to-end: empty conf ------------------------------------------
    local e4="$T/e4.conf"
    : >"$e4"
    out=$(audit "$e4")
    rc=$?
    got=$(printf '%s\n' "$out" | sed -n 's/^TSUKUROI_BOOTCHAIN: //p')
    st_check 'e4-summary' UNKNOWN "$got"
    st_check 'e4-exit' 2 "$rc"

    # ---- end-to-end: unclassified snapshot combo -------------------------
    rm -rf -- "$fx"
    mkdir -p -- "$fx"
    mk_uki_fx "$fx/snap.efi" "$sha_a" "$b2_a" 7.2.11-arch1-1 42.2 7 0 /new_root /new_root absent true
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e5="$T/e5.conf"
    cat >"$e5" <<EOF
//snap
  path: boot():/EFI/Linux/snap.efi#$b2_a
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=/@/.snapshots/7/snapshot rw
EOF
    out=$(audit "$e5")
    rc=$?
    got=$(printf '%s\n' "$out" | sed -n 's/^TSUKUROI_BOOTCHAIN: //p')
    st_check 'e5-unknown-combo-never-consistent' UNKNOWN "$got"
    st_check 'e5-exit' 2 "$rc"
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR==2 {print $17}')
    st_check 'e5-verdict' UNTESTED "$got"

    # ---- end-to-end: injection safety ------------------------------------
    rm -rf -- "$fx"
    mkdir -p -- "$fx"
    mk_uki_fx "$fx/safe.efi" "$sha_a" "$b2_a" 7.2.11-arch1-1 42.2 7 0 /new_root /new_root symlink '' 1
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e6="$T/e6.conf"
    # The cmdline carries a literal command-substitution string; the label carries one too.
    # If this script ever evaluated conf text, a file named `canary` would appear.
    cat >"$e6" <<'EOF'
//safe$(touch canary)
  path: boot():/EFI/Linux/safe.efi#822299bbdaf0d4ede97d341fd5fcfa73fb3ca3942b7dcc597a79e7b46e69ec8f3eaabb194c431112de1c97b15345f1ca64adb0438b94d8fc8100cd393ce98024
  cmdline: quiet $(touch canary) root=/dev/mapper/root rootflags=subvol=@ rw
//evil
  path: boot():/../evil.efi#eeee00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
  cmdline: quiet
EOF
    (cd -- "$T" && audit "$e6" >/dev/null)
    rc=$?
    if [ -e "$T/canary" ] || [ -e canary ]; then
        got=present
    else
        got=absent
    fi
    st_check 'e6-no-canary' absent "$got"
    st_check 'e6-invalid-path-exit' 2 "$rc"

    # ---- end-to-end: selected but unproven (mtime unverifiable) ----------
    rm -rf -- "$fx"
    mkdir -p -- "$fx"
    mk_uki_fx "$fx/cur.efi" "$sha_a" "$b2_a" 7.2.11-arch1-1 42.2 7 0 /new_root /new_root symlink
    printf 'Omarchy.linux\n' >"$fx/loader_entries"
    printf '1000\n' >"$fx/btime"
    printf '0\n' >"$fx/boot_inputs_newer"
    local e7="$T/e7.conf"
    cat >"$e7" <<EOF
/+Omarchy
//linux
  path: boot():/EFI/Linux/cur.efi#$b2_a
  cmdline: quiet root=/dev/mapper/root rootflags=subvol=@ rw
EOF
    out=$(audit "$e7")
    rc=$?
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR==2 {print $17}')
    st_check 'e7-selected-unproven-verdict' PATH-ALIASED-EMULATED "$got"
    got=$(printf '%s\n' "$out" | awk -F'\t' 'NR==2 {print $16}')
    st_check 'e7-selected-flag' true "$got"
    st_check 'e7-exit' 0 "$rc"

    # ---- R43-C1: a missing start point must not mask a newer input ---------
    local bi="$T/bootinputs"
    mkdir -p -- "$bi/d/sub"
    : >"$bi/old"
    : >"$bi/d/sub/f"
    touch -d @1000 -- "$bi/old" "$bi/d/sub/f" "$bi/d/sub" "$bi/d"
    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
    st_check 'R43-C1-missing-start-point-none-newer' 0 "$got"
    touch -d @3000 -- "$bi/d/sub/f"
    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" "$bi/d")
    st_check 'R43-C1-missing-start-point-deep-newer' 1 "$got"
    got=$(inputs_newer_than 2000 "$bi/old" "$bi/d")
    st_check 'R43-C1-all-present-deep-newer' 1 "$got"

    if [ "$st_fail" -eq 0 ]; then
        printf 'TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=%d failed=0\n' "$st_total"
        return 0
    fi
    printf 'TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=%d failed=%d\n' "$st_total" "$st_fail"
    return 1
}

# --------------------------------------------------------------------------- main

main() {
    local mode=''

    while [ $# -gt 0 ]; do
        case $1 in
            --live) mode=live ;;
            --selftest) mode=selftest ;;
            --help | -h) usage; return 0 ;;
            *)
                printf '%s: unknown argument: %s\n' "$PROG" "$1" >&2
                usage >&2
                return 2
                ;;
        esac
        shift
    done

    case $mode in
        selftest)
            run_selftest
            return $?
            ;;
        live)
            if [ -n "$BOOTCHAIN_FIXTURE" ]; then
                printf '%s: refusing --live while BOOTCHAIN_FIXTURE is set\n' "$PROG" >&2
                printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
                return 2
            fi
            if [ "${EUID:-1}" -eq 0 ]; then
                printf '%s: refusing --live as root: the audit must run unprivileged\n' "$PROG" >&2
                printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
                return 2
            fi
            ;;
        *)
            printf '%s: one of --live, --selftest, --help is required\n' "$PROG" >&2
            usage >&2
            printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
            return 2
            ;;
    esac

    local missing='' c
    for c in sudo cat objcopy lsinitcpio sha256sum b2sum find awk sed grep basename \
        mktemp stat tail tr head wc readlink uname chmod rm; do
        command -v "$c" >/dev/null 2>&1 || missing="$missing $c"
    done
    if [ -n "$missing" ]; then
        printf '%s: missing required command(s):%s\n' "$PROG" "$missing" >&2
        printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
        return 2
    fi

    if ! init_work; then
        printf '%s: cannot create a private mktemp work dir (TMPDIR=%s); refusing\n' \
            "$PROG" "${TMPDIR:-/tmp}" >&2
        printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
        return 2
    fi

    local conf=$WORK/limine.conf
    if ! sudo -n cat -- "$LIVE_CONF" >"$conf" 2>/dev/null; then
        printf '%s: cannot read %s through sudo -n; refusing to guess\n' "$PROG" "$LIVE_CONF" >&2
        printf 'TSUKUROI_BOOTCHAIN: UNKNOWN\n'
        return 2
    fi

    audit "$conf"
    return $?
}

main "$@"
