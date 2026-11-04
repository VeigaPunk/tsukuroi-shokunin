# modprobe configuration plane — round 72

source: S301 (kmod v34 `man/modprobe.d.5.scd`); S302 (kmod v34 `libkmod/libkmod-config.c`); S303 (kmod v34 `tools/modprobe.c`)
verified-at: round-72 declaration `6b42676`; snapshots `.ufo/waves/round-72/before/src/` (`sha256sum -c SHA256SUMS` 3/3 OK)
recheck: on-release of the kmod tag the host runs (host kmod 34.2; snapshots at tag v34); procedure: `python3 tools/count-md-rows-r72.py --revision <REV>` must print `MD_VERIFIED=6 … met=1` rc 0

The modprobe configuration plane the lane never held: which directories are read
and in what order, how the files from all of them are ordered against each other,
what libkmod does with a repeated filename, when the kernel command line enters
the same config object, what `-n` actually suppresses, and how far a `blacklist`
line reaches. Every rule row is anchored to one committed snapshot under
`.ufo/waves/round-72/before/src/`; the digests are the sha256 of those exact
bytes, and the quote cell carries the sentence the row was written from.

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| MD1 | Configuration files are read from directories in SYNOPSIS order of precedence: once a file of a given filename is loaded, any file of the same name in subsequent directories is ignored. | source=S301 | snapshot=modprobe.d.5.scd | digest=aa1a869e57db31c8187a436b5eab3047394da5fd779794e1cdd4ccad598ee46e | quote="Once a file of a given filename is loaded, any file of the same name in subsequent directories is ignored." |
| MD2 | All configuration files are sorted in lexicographic order regardless of the directory they reside in, so a configuration file can be completely replaced by a new file with the same name in a directory of higher priority, or partially replaced by a configuration file that is ordered later. | source=S301 | snapshot=modprobe.d.5.scd | digest=aa1a869e57db31c8187a436b5eab3047394da5fd779794e1cdd4ccad598ee46e | quote="All configuration files are sorted in lexicographic order, regardless of the directory they reside in." |
| MD3 | conf_files_insert_sorted keeps one config list ordered by strcmp name; on a duplicate config file the DBG line reports ignoring duplicate config file and the insertion returns EEXIST, so the later path is never parsed. | source=S302 | snapshot=libkmod-config.c | digest=ae520a0721aad0bc61c7b13369fccf8e46fc408d8c0884fda9260a05da7ceb11 | quote="Ignoring duplicate config file" |
| MD4 | kmod_config_new opens every configuration file in the list and then calls kmod_config_parse_kcmdline(config), so kernel command line module options are added to the same config object. | source=S302 | snapshot=libkmod-config.c | digest=ae520a0721aad0bc61c7b13369fccf8e46fc408d8c0884fda9260a05da7ceb11 | quote="kmod_config_parse_kcmdline(config);" |
| MD5 | If dry_run is set, the install path prints out the command and returns before system executes it, and the remove path returns before kmod_module_remove_module, so modprobe does not execute operations. | source=S303 | snapshot=modprobe.c | digest=1e8e352634026e6618f37c0aee9974cf51427bfa3a77d12bcd2220ea8a71bf3f | quote="Do not execute operations, just print out" |
| MD6 | modprobe adds KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY for a resolved alias and KMOD_PROBE_APPLY_BLACKLIST only with --use-blacklist, so blacklist is not applied to a module named on the command line. | source=S303 | snapshot=modprobe.c | digest=1e8e352634026e6618f37c0aee9974cf51427bfa3a77d12bcd2220ea8a71bf3f | quote="Apply blacklist to resolved alias." |

## Why these six

The plane has one read path and one refusal path. The read path starts from a
fixed list of directories: the SYNOPSIS names `@SYSCONFDIR@/modprobe.d`,
`/run/modprobe.d`, `/usr/local/lib/modprobe.d`, `@DISTCONFDIR@/modprobe.d` and
`/lib/modprobe.d` in that order, and the text states that order is the
precedence order, with a filename already loaded suppressing every later
directory's file of that name (MD1). Inside that walk the files are not grouped
by directory: libkmod inserts each basename into a single list ordered by
`strcmp` (`conf_files_insert_sorted`), so iteration is lexicographic across all
directories, and that is what makes a later-ordered file a partial replacement
while a same-name file in a higher-priority directory is a complete replacement
(MD2). The same insertion point is the duplicate gate: when `strcmp` returns
zero the function logs at DBG and returns `-EEXIST` without inserting, so the
second copy — whichever directory it came from — is never opened (MD3). Only
after the whole list has been parsed does `kmod_config_new` call
`kmod_config_parse_kcmdline(config)`, which is why command-line module options
land in the same config object as the file rules instead of a separate one
(MD4).

The refusal path is narrower than it looks. `dry_run` does not stop the plan
from being printed: `SHOW` emits the command, and only then do the install and
remove paths return before `system` or `kmod_module_remove_module` is reached
(MD5). Blacklisting is applied to alias resolution unconditionally
(`KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY` is always OR'd in) and to the module
itself only when `-b/--use-blacklist` sets `use_blacklist`, so a `blacklist`
line stops alias-triggered loads but not a module named directly (MD6).

## Decision table

Host shapes from the read-only capture `before/host.txt` (paths, modes and names
only) mapped to a verdict and an operator action. "Evidence" names the rule row
that decides the verdict; "host" means the shape itself is in the capture.

| # | observed shape | verdict | operator action | evidence |
|---|---|---|---|---|
| D1 | `/lib/modprobe.d` and `/usr/lib/modprobe.d` both present; `/lib` resolves to `/usr/lib` | one physical directory behind two SYNOPSIS entries; MD1's walk does not read it twice and neither entry shadows the other | audit `/usr/lib/modprobe.d` once; do not assume a `/lib` copy can shadow a `/usr/lib` copy | MD1 + host |
| D2 | `/run/modprobe.d` absent | the slot contributes no files; the parse continues past a failed `stat` | none; absence is a normal state, not a defect | MD1 + host |
| D3 | the same `.conf` name in `/etc/modprobe.d` and `/usr/lib/modprobe.d` | the `/etc` copy is loaded first and the later same name is ignored entirely — complete replacement, never a merge | read the `/etc` copy; distro changes to the `/usr/lib` copy will not take effect | MD1, MD3 + host |
| D4 | an `install` line in a `/etc/modprobe.d` file | modprobe runs that command instead of inserting the module; `-n` prints the command and executes nothing | review with `modprobe -n`, and keep `--ignore-install` inside the command to stop recursion | MD5 |
| D5 | `blacklist` plus an explicit `modprobe <module>` | the explicit name is still inserted: blacklist is alias-only without `-b` | add `-b` to make the explicit name refused, or accept that the `blacklist` line only stops alias routes | MD6 |
| D6 | `-b` on an alias | the alias is resolved with the blacklist applied, so a blacklisted target is refused instead of inserted | expect the refusal; drop `-b` when the load must go through | MD6 |

## Limits

- **Lexical-substance channel.** The frozen counter verifies grounding
  lexically: a statement passes when it shares at least six distinct
  non-stopword tokens of length four or more with the snapshot and at least half
  of its distinct tokens occur there. A statement can therefore be lexically
  grounded while entailing something the snapshot does not say. The defence is
  the quote cell and the hand reading of the cited regions, not the counter; the
  counter measures provenance, not entailment.
- **No host file content was read.** The capture records paths, modes and names
  only, and this round read no `/etc/modprobe.d` or `/usr/lib/modprobe.d` file.
  No `blacklist`, `install` or `options` line was observed on this host, so D4,
  D5 and D6 are shape-independent rule applications, not observations; D1, D2
  and D3 rest on the captured path shapes.
- **Snapshot tag versus host build.** The three snapshots are kmod **v34**
  bytes; the host reports kmod **34.2**. The rows state the v34 source text, and
  the difference between tag and installed build is not measured here.
- **Debug visibility.** MD3's message and its `-EEXIST` return are DBG-level:
  the duplicate is silent at default verbosity, so an operator cannot see the
  suppression without debug logging.
- **Placeholders.** The man page states the first and fourth directories as
  `@SYSCONFDIR@` and `@DISTCONFDIR@`; this note maps them to `/etc/modprobe.d`
  and `/usr/lib/modprobe.d` because the host capture shows those two paths, and
  the mapping is not itself stated in the snapshot.

## Provenance re-verification — round 81 (appended, 2026-11-04)

The header's operative `verified-at:` line named the round-72 declaration commit and the snapshot
manifest check but carried no ISO date, so `tools/check-knowledge-header.py` reported
`KNOWLEDGE-HEADER-VALUE` for this note. The date is supplied here as an appended superseding line
rather than by editing the filed header; the snapshot set was re-verified this round, not assumed.

verified-at: 2026-11-04 — snapshots re-verified at round 81: `sha256sum -c SHA256SUMS` in
`.ufo/waves/round-72/before/src/` returns 3/3 OK (modprobe.d.5.scd, libkmod-config.c, modprobe.c);
the round-72 declaration commit `6b42676` named in the header above is unchanged.
