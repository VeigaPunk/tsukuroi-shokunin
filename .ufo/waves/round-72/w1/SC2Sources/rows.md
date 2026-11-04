# Round 72 — C1 registry rows S301–S303 (draft)

Three rows, 11 cells each, no pipe inside any cell; S301 (man page), S302 (libkmod config), S303
(modprobe tool). The frozen counter `tools/count-md-rows-r72.py` binds each MD row to one of these at
the same revision and requires: the row's `source` cell contains the exact `src/SOURCES.json` URL for
the cited snapshot; the row's `anchor` cell contains that snapshot's basename; `kind` is a source kind
and not `own-work`.

## Status: the ids are already in the working tree (uncommitted, not my write)

When this draft was finished, `corpus/SOURCES.md` in the lane working tree already carried S301–S303
and two r72 prose bullets: `git diff --stat corpus/SOURCES.md` reads `1 file changed, 6 insertions(+)`,
and `git diff` shows three added `| S30x` rows plus two added `- Round-72 …` bullets at EOF. My write
scope excludes the lane tree, so I wrote nothing there; the rows below are the source-seat draft and a
delta against what landed, not a landed artifact.

Both sets bind to the frozen counter. The probe
`.ufo/waves/round-72/probes/SC2Sources/registry-row-check.txt` runs the counter's own `registry_rows()`
twice: over the working tree alone (PASS for kind, source-url and anchor-basename on all three) and
over the working tree with these draft rows overriding by id (also all PASS; the parser keys by id).

### Delta the L1 may take (precision only; nothing here changes a claim)

- D1 — landed S302 anchor starts the insertion function at line 915 and ends it at 960. The function
  `conf_files_insert_sorted` is lines 920–971 (`struct conf_file` at 914–918, `return 0;` at 970). The
  `-EEXIST` arm is 941–943 and the insert calls are 955–960, so the claim is covered but the range
  clips both ends. Proposed replacement fragment: `lines 920-971 (conf_files_insert_sorted …)`.
- D2 — landed S302 anchor places `kmod_config_new` at 1020–1085; the function opens at 1014 and its
  `kmod_config_parse_kcmdline(config);` call is line 1083, so `1014-1085` states the same claim with
  the real function start.
- D3 — landed S303 anchor `260-300` for `command_do` is correct as scoped: the function is 260–313 and
  the dry-run return is 298–299. No change proposed.
- D4 — both landed prose bullets sit at EOF, i.e. inside `## Leads (unopened)` (that heading is line
  390), not in `## Search log`; the search-log bullet also carries counts but no exclusion reasons and
  no stop rationale. `search-log.md` supplies a placement-correct paragraph carrying both.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S301 | kmod v34 man/modprobe.d.5.scd — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd?h=v34 | docs | A | The documented modprobe configuration plane: the configuration directory list in SYNOPSIS read order, suppression of a same-named file in later directories, one lexicographic ordering across directories, and complete versus partial replacement | tag v34, snapshot .ufo/waves/round-72/before/src/modprobe.d.5.scd, lines 7-17 (SYNOPSIS directory list in precedence order), 40-50 (CONFIGURATION DIRECTORIES AND PRECEDENCE: once a filename is loaded the same name in subsequent directories is ignored; all files sorted lexicographic regardless of directory; complete replacement by higher priority and partial replacement by later ordering), 52-53 (MODPROBE_OPTIONS may alter the directories) | One benefit: the manual gives both the read order and the two replacement modes, so a same-named file in a higher-priority directory replaces a whole file while a later-ordered file only partially replaces it | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S302 | kmod v34 libkmod/libkmod-config.c — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/libkmod/libkmod-config.c?h=v34 | code | A | The libkmod implementation of config-file discovery and parse order: sorted insertion keyed on the basename with an -EEXIST duplicate rejection, one list shared by every directory in config_paths order, and the /proc/cmdline parse run after the file loop | tag v34, snapshot .ufo/waves/round-72/before/src/libkmod-config.c, lines 920-971 (conf_files_insert_sorted: strcmp insert position and -EEXIST when a name compares equal), 974-1012 (conf_files_list inserts every directory entry into the same list), 1014-1085 (kmod_config_new: config_paths loop in array order, parse loop over the list, kmod_config_parse_kcmdline called last), 637-766 (the kcmdline parser that reads /proc/cmdline) | One benefit: the code shows one basename-ordered list and the -EEXIST return that drops a second copy of a name, followed by the command-line parse after the file loop | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S303 | kmod v34 tools/modprobe.c — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/tools/modprobe.c?h=v34 | code | A | modprobe's option-to-flag mapping for the two execution claims: what -n sets and which calls it short-circuits, the alias-only blacklist flag applied unconditionally, and the extra flag --use-blacklist adds | tag v34, snapshot .ufo/waves/round-72/before/src/modprobe.c, lines 36 and 41 (dry_run and use_blacklist statics), 62 (--use-blacklist option entry), 298-299 and 323-324 (dry-run returns before system() and before module removal), 623-629 (KMOD_PROBE_DRY_RUN set from dry_run, ALIAS_ONLY always set, APPLY_BLACKLIST only when use_blacklist), 807-809 (case 'b' sets use_blacklist), 836-838 (case 'n' sets dry_run) | One benefit: -n only sets dry_run, which returns before the install command and before removal, while the alias-only blacklist flag is unconditional and --use-blacklist adds the broader one | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |

## Gate quotes

Each quote below was located verbatim in the committed snapshot under whitespace normalization and is at
most 25 words. `pipe=`/`dq=` record whether the quote text contains `|` or `"` — the two characters the MD
row grammar forbids (a pipe anywhere in a cell, a double quote inside the quote cell). Location here is
token-aligned, which is stricter than the frozen counter's rule (`norm(quote) in norm(snapshot)`, plain
substring): a quote may in fact end mid-token, e.g. right before the literal `\n"` of a C usage string.
Access date 2026-11-03 for all three URLs; digests are the committed ones.

### S301 — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd?h=v34

- L43–44, 20 words, pipe=no, dq=no: `Once a file of a given filename is loaded, any file of the same name in subsequent directories is ignored.`
- L46–47, 15 words, pipe=no, dq=no: `All configuration files are sorted in lexicographic order, regardless of the directory they reside in.`
- L49–50, 12 words, pipe=no, dq=no: `or partially replaced (by having a configuration file that is ordered later).`
- L77–78, 14 words, pipe=no, dq=no: `keyword indicates that all of that particular module's internal aliases are to be ignored.`

### S302 — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/libkmod/libkmod-config.c?h=v34

- L937–938, 8 words, pipe=no, dq=no: `if ((cmp = strcmp(name, cf->name)) <= 0) break;`
- L974, 7 words, pipe=no, dq=no: `Insert configuration files in @list, ignoring duplicates`
- L1025–1026, 14 words, pipe=no, dq=no: `for (i = 0; config_paths[i] != NULL; i++) { const char *path = config_paths[i];`
- L1077–1078, 7 words, pipe=no, dq=no: `if (fd >= 0) kmod_config_parse(config, fd, fn);`
- L1083, 1 word, pipe=no, dq=no: `kmod_config_parse_kcmdline(config);`
- L637, 5 words, pipe=no, dq=no: `static int kmod_config_parse_kcmdline(struct kmod_config *config)`

### S303 — https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/tools/modprobe.c?h=v34

- L298–299, 4 words, pipe=no, dq=no: `if (dry_run) goto end;`
- L323–324, 4 words, pipe=no, dq=no: `if (dry_run) return 0;`
- L807–809, 6 words, pipe=no, dq=no: `case 'b': use_blacklist = 1; break;`
- L836–838, 6 words, pipe=no, dq=no: `case 'n': dry_run = 1; break;`
- L626, 3 words, pipe=yes, dq=no: `flags |= KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY;` — unusable in an MD row

## MD-row quote candidates (for SC1Entry, not a gate)

- MD1 directory precedence → S301 L43–44.
- MD2 lexicographic ordering and partial replacement → S301 L46–47 (ordering) plus L49–50 (partial replacement); one quote per row, so a single row can only carry one of the two.
- MD3 sorted insertion and duplicate rejection → S302 L937–938 (insert position) or L974 (the "ignoring duplicates" comment).
- MD4 command line parsed after the files → S302 L1083 (the call) or L637 (the parser signature).
- MD5 dry-run prints and executes nothing → S303 L298–299 or L836–838.
- MD6 blacklist alias-only versus --use-blacklist → S303 L807–809; the unconditional alias-only flag itself sits on L626, whose `|=` makes that line unusable as a quote cell.
