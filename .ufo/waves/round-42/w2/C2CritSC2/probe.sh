#!/usr/bin/env bash
# read-only probe: mount a private tmpfs at /var/lib inside `unshare -rm` and let the installed
# btrfs-progs v7.1 binary read one crafted record. No host path is written.
set -u
S=$1; FSID=$2; rec=$3
unshare -rm bash -c 'mount -t tmpfs tmpfs /var/lib 2>&1 || exit 90
mkdir -p /var/lib/btrfs || exit 91
cp "$1" "/var/lib/btrfs/scrub.status.$2" || exit 92
btrfs --version
btrfs scrub status -d -R /
echo "STATUS_EXIT=$?"' _ "$S/ns/$rec" "$FSID"
