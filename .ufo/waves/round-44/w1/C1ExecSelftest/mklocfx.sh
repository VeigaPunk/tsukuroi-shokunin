#!/usr/bin/env bash
# Build a scrub-record fixture with several detail entries so the detail ORDER is visible.
set -eu
FX=$1
U1=11111111-1111-1111-1111-111111111111
U2=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
U3=99999999-8888-7777-6666-555555555555
rm -rf -- "$FX"
mkdir -p "$FX/scrub" "$FX/wants" "$FX/btrfs/$U1/devinfo/1" "$FX/btrfs/$U1/devinfo/2" "$FX/btrfs/$U1/devinfo/3"
# devfr: 1 malformed, 2 limited (nonzero), 3 missing file -> three devinfo detail entries
printf 'fast\n' > "$FX/btrfs/$U1/devinfo/1/scrub_speed_max"
printf '104857600\n' > "$FX/btrfs/$U1/devinfo/2/scrub_speed_max"
# record directory: one good record (U1), one 000 record (U2 = unreadable+orphan),
# one _tmp, one progress non-socket, one symlinked record (not regular) -> ordered dir detail
printf 'x\n' > "$FX/scrub/scrub.status.$U1"
printf 'x\n' > "$FX/scrub/scrub.status.$U2"
chmod 000 "$FX/scrub/scrub.status.$U2"
printf 'x\n' > "$FX/scrub/scrub.status.${U1}_tmp"
printf 'x\n' > "$FX/scrub/scrub.progress.$U1"
ln -s /etc/hostname "$FX/scrub/scrub.status.$U3"
# timer wants: one instance link, the bare template, an unrelated timer
ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@home.timer"
ln -s /usr/lib/systemd/system/btrfs-scrub@.timer "$FX/wants/btrfs-scrub@-.timer"
: > "$FX/wants/btrfs-scrub@.timer"
: > "$FX/wants/fstrim.timer"
