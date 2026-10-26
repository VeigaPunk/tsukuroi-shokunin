VERDICT: supports

Seat C1ScoutProcMounts, item C1-17. Read-only; no lane file touched. Accessed 2026-10-26.
Fetched copy of proc.rst lived in scratch only (sha256 below); no tool installed.

## Quotes (<=25 words, located)

Q1 — namespace scope. https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html (man-pages 6.19, 2026-02-08), DESCRIPTION, `/proc/pid/mounts (since Linux 2.4.19)`:
"This file lists all the filesystems currently mounted in the process's mount namespace (see mount_namespaces(7))."
Same section, `/proc/mounts` paragraph: "this file became a link to /proc/self/mounts, which lists the mounts of the process's own mount namespace."
=> directly supports the arm's default TSUKUROI_PROC_MOUNTS=/proc/self/mounts being the calling process's own namespace view (the view inside `unshare -rm` for the counter).

Q2 — format pointer. Same page, same paragraph: "The format of this file is documented in fstab(5)." (The man page itself does NOT list the fields.)

Q3 — field order. https://man7.org/linux/man-pages/man5/fstab.5.html (util-linux 2.43.devel, 2026-05-24), DESCRIPTION:
"The third field (fs_vfstype). This field describes the type of the filesystem." Preceded by "The first field (fs_spec)" and "The second field (fs_file). This field describes the mount point". So order = source, mount point, fstype, options, freq, passno. Subtype notation: "defined by '.subtype' suffix. For example 'fuse.sshfs'". Escapes: "any spaces or tabs within the fields must be escaped using \040 or \011".
=> `read -r _src _mp fst _rest` at tools/tsukuroi-census.sh:1906-1908 takes fst = field 3, matching.

Q4 — kernel doc (v7.2 proc.rst, sha256 e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126 = the S148 hash; 2495 lines; fetched HTTP rc 0):
- line 778: " mounts       Mounted filesystems" — only mention of the `mounts` file; table row, no field order, no namespace statement.
- `mountinfo` section 3.5 lines 1965-1987, a DIFFERENT file with a different layout: fstype is field (m+2) after the "-" separator: line 1981 "(m+2) filesystem type: name of filesystem of the form "type[.subtype]""; line 1977 "(5) mount point: mount point relative to the process's root".
FINDING: proc.rst v7.2 does not state that /proc/[pid]/mounts is per-mount-namespace and does not give the mounts field order (grep "namespace" in proc.rst: no hit near mounts; commands: grep -n 'mounts\|mountinfo' proc.rst). Do not cite proc.rst for either claim; it only supports the mountinfo layout and the (m+2) fstype position, which the arm does not read. The two claims rest on proc_pid_mounts(5) + fstab(5), both man-pages-project/util-linux man pages, not kernel source.

Live check: `head -3 /proc/self/mounts` on host prints `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0` — 6 fields, fstype 3rd (consistent, not a substitute for the sources).

Page hashes at access (curl | sha256sum): proc_pid_mounts.5.html 9c3733214df50015c4599f0d3a05a508f7a8813999ea72352d5e6fb87a1287c3; fstab.5.html 0cde7f00a2e656d6ef107bc2535b172c71c78f46460de6eaf282adf0efce1829 (HTTP 200 for the first).

## Id caution
Registry tail at lane tip 394e1ba4 is S218, but .ufo/waves/round-39/assimilation/staged-ids lists S200..S346 (147 lines, tail S346). S219 is in staged-ids, so L1 must pick an id that does not collide with it; the row below uses S<next>.

## Proposed SOURCES row (11 columns: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by)

| S<next> | proc_pid_mounts(5) and fstab(5) — https://man7.org/linux/man-pages/man5/proc_pid_mounts.5.html and https://man7.org/linux/man-pages/man5/fstab.5.html | docs | A | What the mount table the census STORAGE arm reads (TSUKUROI_PROC_MOUNTS, default /proc/self/mounts) lists and the position of the filesystem type in each line | proc_pid_mounts(5) man-pages 6.19 DESCRIPTION `/proc/pid/mounts` and `/proc/mounts` paragraphs (page sha256 9c3733214df50015c4599f0d3a05a508f7a8813999ea72352d5e6fb87a1287c3); fstab(5) util-linux 2.43.devel, "The third field (fs_vfstype)" (page sha256 0cde7f00a2e656d6ef107bc2535b172c71c78f46460de6eaf282adf0efce1829); both opened 2026-10-26; the kernel proc.rst v7.2 (S148) has no per-namespace or `mounts` field statement, only mountinfo section 3.5 lines 1965-1987 | /proc/self/mounts lists the mounts of the reading process's own mount namespace, and its format is fstab(5): source, mount point, filesystem type (third field, subtype as `type.subtype`), options, dump, pass, with spaces escaped as \040, so a reader that splits on whitespace takes the type from field 3 | mined | 2026-10-26 | on-release | corpus/knowledge/pacman-transaction-order-r39.md |

(used-by above is a placeholder; replace with the file that cites the row — the lane's storage-hidden knowledge/census doc, not the transaction-order note, since this source is about the C1 arm.) Optional split if one-URL-per-row is enforced: row A proc_pid_mounts(5) teaching only the namespace statement, row B fstab(5) teaching only the field order.

## Not done
- No check of the lane's counter or census beyond reading tools/tsukuroi-census.sh:1896-1916 and :365-379.
- Did not verify mount_namespaces(7) content or that /proc/self/mounts reflects a tmpfs overmount (counter's job).
- No mountinfo parser proposal; the arm uses mounts.
