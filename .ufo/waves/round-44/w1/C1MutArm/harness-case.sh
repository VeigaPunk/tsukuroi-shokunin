#!/usr/bin/env bash
set -u
lib=$1; case_name=$2
FX=$(mktemp -d /fast/scratch/hyaku/tsukuroi-r44/C1MutArm/harness/fx.XXXXXX)
trap 'chmod -R u+rwx -- "$FX" 2>/dev/null; rm -rf -- "$FX"' EXIT
export TSUKUROI_BTRFS_SYSFS="$FX/btrfs" TSUKUROI_SCRUB_DIR="$FX/scrub" TSUKUROI_TIMER_WANTS="$FX/wants"
U=12345678-1234-1234-1234-123456789abc
case "$case_name" in
  e) mkdir -p "$FX/btrfs/$U/devinfo/1"; printf '\n' > "$FX/btrfs/$U/devinfo/1/scrub_speed_max" ;;
  h) mkdir -p "$FX/btrfs/$U/devinfo/1"; printf '00\n' > "$FX/btrfs/$U/devinfo/1/scrub_speed_max" ;;
  j) mkdir -p "$FX/btrfs/$U/devinfo/1" "$FX/scrub"
     printf '104857600\n' > "$FX/btrfs/$U/devinfo/1/scrub_speed_max"
     ln -s /etc/hostname "$FX/scrub/scrub.status.$U" ;;
  k) mkdir -p "$FX/wants"; : > "$FX/wants/btrfs-scrub.timer"
     ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@home.timer" ;;
  l) mkdir -p "$FX/btrfs" "$FX/scrub"; chmod 0444 "$FX/btrfs"
     printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$U"; chmod 644 "$FX/scrub/scrub.status.$U" ;;
  a) UU=1A2B3C4D-1234-1234-1234-ABCDEF123456
     mkdir -p "$FX/btrfs/$U/devinfo/1" "$FX/scrub"
     printf '0\n' > "$FX/btrfs/$U/devinfo/1/scrub_speed_max"
     printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$U"
     printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$UU"
     printf 'scrub status:1\n' > "$FX/scrub/scrub.status.${U}_tmp" ;;
esac
. "$lib"
probe_scrub_record
printf '%s\n' "$SCRUB_LINE"
