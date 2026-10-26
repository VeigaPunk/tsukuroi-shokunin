VERDICT: holds
ROW: PA4
lines checked: frozen/src/add.c:168-206

Seat C2RevPA4, item C2-4a, 2026-10-26. Row PA4 read at the pinned commit with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 9cc9aa77e30e0e23de2d4d2697b3b218ada02969:corpus/knowledge/alpm-package-anatomy-r41.md`.
No lsp device is available in this seat; every check below is a line-numbered read of the pinned
snapshot or a shell count/hash, with the observed output shown.

1. Snapshot equals live source. Fetched
   https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c on 2026-10-26
   (`curl -fsSL`, 22431 bytes): `sha256sum` = fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1,
   identical to the add.c line of `.ufo/waves/round-41/frozen/src/SHA256SUMS` and to `sha256sum` of
   `.ufo/waves/round-41/frozen/src/add.c` itself (both files hashed in one command, one shared digest).
   The frozen lines are therefore the live lines at 54d9411.

2. Rule clause -> code clause (frozen/src/add.c; numbers from the raw read of 168-206 and grep):
   - ".INSTALL becomes install" add.c:173-174; ".CHANGELOG becomes changelog" add.c:175-176;
     ".MTREE becomes mtree" add.c:177-178 — the strcmp chain in extract_db_file (function spans 168-189).
   - "inside the local database entry <name>-<version>/" add.c:186-188:
     `snprintf(filename, PATH_MAX, "%s%s-%s/%s", _alpm_db_path(handle->db_local), newpkg->name,
     newpkg->version, dbfile)`; the entry directory is created just before extraction by
     _alpm_local_db_prepare (add.c:493, comment at add.c:491-492 "prepare directory for database entries
     so permissions are correct after changelog/install script installation").
   - "each with mode 0644" add.c:185 `archive_entry_set_perm(entry, 0644);` before extraction. The perm is
     honored because perform_extraction (add.c:113-166) passes ARCHIVE_EXTRACT_PERM (add.c:119) through
     archive_write_disk_set_options (add.c:135) into archive_read_extract2 (add.c:137). The mode is forced
     by libalpm, not inherited from the archive; the rule states the outcome the code produces.
   - "every other root dot file ... is skipped" add.c:179-184: `else if(*entryname == '.')` logs
     "skipping extraction of '%s'", calls archive_read_data_skip(archive), returns 0 — nothing is written.
     extract_single_file routes every dot-leading entry to extract_db_file (add.c:204-206); the install
     loop calls extract_single_file for every archive entry (add.c:560), and the DBONLY branch calls
     extract_db_file directly for dot entries (add.c:529-530). Occurrence counts in the pinned add.c:
     PKGINFO 0, BUILDINFO 0, MTREE 1 (grep -c), so .PKGINFO and .BUILDINFO can only reach the skip
     branch — "included" is exact, and .MTREE has exactly one handling site, the mapping at 177-178.
   - "kept for future use" mirrors the code's own comment at add.c:180, "reserve all files starting with
     '.' for future possibilities", which is exactly the quoted source-cell text. The files are not
     persisted anywhere (archive_read_data_skip discards the entry); the reservation is of the dot-file
     namespace. Read as the comment's rationale, the clause is supported.
   - "During install": both branches of the commit_single_pkg extraction loop route dot entries to
     extract_db_file (DBONLY add.c:525-534; normal add.c:535-561); no transaction flag gates the mapping.
   - Presence condition: the mapping applies to members the package actually carries; the row's own host
     cell quantifies this (install 51/1409, changelog 0/1409), so the opening sentence reads as a
     selection statement — which members are stored vs skipped — not "every package gets all three
     files". No missing condition changes the meaning.
   - Value cell ".INSTALL=install .CHANGELOG=changelog .MTREE=mtree" is add.c:173-178 verbatim.

3. Quote position. Source cell cites "S230 add.c:168-189" quoting "/* reserve all files starting with '.'
   for future possibilities */" — that comment is at add.c:180, inside 168-189; extract_db_file ends at
   189 (raw read of 168-206). Cited range and quote both check.

4. Host cell vs capture. Command:
   `awk -F'\t' 'NR>1{n++; mt+=$4; ins+=$5; cl+=$6; dot+=$7} END{printf "rows=%d mtree=%d install=%d changelog=%d dotfiles=%d\n", n, mt, ins, cl, dot}' localdb-anatomy.tsv`
   observed: `rows=1409 mtree=1409 install=51 changelog=0 dotfiles=0` — exactly the host cell's
   "mtree 1409 of 1409, install 51 of 1409, changelog 0 of 1409, dot-files 0 of 1409 entries".
   The numbers are measured, not asserted: hostcap/capture.sh:14 defines has() as a file-existence test
   (`[ -f "$d/$1" ]`) per /var/lib/pacman/local/*/ entry (loop capture.sh:12-24) and capture.sh:15 counts
   root dot files with `find -mindepth 1 -maxdepth 1 -name '.*'`. Integrity: `sha256sum -c MANIFEST.sha256`
   in hostcap -> all six files OK. capture-meta.txt: captured_utc 2026-10-26T16:14:04Z,
   pacman 7.1.0.r9.g54d9411-3 — matches the entry's verified-at line. The host cell claims only presence
   counts; it does not claim the 0644 modes (the capture records no modes), so nothing unmeasured is
   presented as measured.

5. Not done: no pacman query or transaction was run (transactions are paused host-wide; the frozen capture
   is the host evidence); the 0644 mode is verified in source only, not against the host's db files; rows
   PA1-PA3 and PA5-PA8 belong to other seats and were not judged.

Receipts: .ufo/waves/round-41/w1/C2RevPA4/live-add.c (fetched upstream file, 22431 bytes) and
.ufo/waves/round-41/w1/C2RevPA4/receipts.txt (hashes, occurrence counts, capture aggregate, manifest check).
