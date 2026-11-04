# Round-73 registry rows — draft for append (SC2Sources)

State before appending, measured from the lane root on 2026-11-03:

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          -> 303
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++}
  END{print n+0}' corpus/SOURCES.md                                          -> 0
awk ... print i | sort | uniq -d                                              -> (empty)
grep -c 'man/systemd.unit.xml' corpus/SOURCES.md                              -> 0
grep -c 'src/core/unit.c' corpus/SOURCES.md                                   -> 0
grep -c 'src/shared/install.c' corpus/SOURCES.md                              -> 0
grep -c 'man.archlinux.org/man/systemd.unit' corpus/SOURCES.md                -> 0
grep -c 'archlinux.org/packages/core/x86_64/systemd' corpus/SOURCES.md        -> 0
```

Last used id is **S303**, so the three admitted rows take **S304-S306** and the two refusals take
**S307-S308**. The S304/S305/S306 assignment follows the snapshot order the frozen counter's own
`SAMPLE_SOURCES` map uses (`systemd.unit.xml` -> S304, `unit.c` -> S305, `install.c` -> S306).

Each row below is one line, 11 cells, no `|` inside a cell. Copy verbatim into the registry table after
S303. The three `used-by` paths name the C1 note; append the rows and the note in the same commit, or the
census check `mined rows whose used-by paths do not exist` prints `missing:` for all three.

| S304 | systemd v262 man/systemd.unit.xml — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml | docs | A | The documented systemd unit-load merge plane that grounds UL1-UL2: the compiled load-path override rule, replacement of the load path by SYSTEMD_UNIT_PATH, and the drop-in precedence and lexicographic merge rule | man/systemd.unit.xml at tag v262, lines 233-248 (drop-in directories, etc over run over usr/lib, drop-ins over unit files, lexicographic merge) and 364-378 (Unit File Load Path override sentence and SYSTEMD_UNIT_PATH replacement); snapshot sha256 eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6 | The documented order decides which of two same-named fragments or drop-ins wins before any manager runs: an earlier load-path directory beats a later one, drop-ins beat unit files wherever located, and differently named drop-ins merge in lexicographic order regardless of the directory | mined | 2026-11-03 | on-release | corpus/knowledge/systemd-unit-load-plane-r73.md |
| S305 | systemd v262 src/core/unit.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | code | A | The manager-side staleness and masked-state plane that grounds UL3-UL4: the daemon-reload trigger set and the null-or-empty test that keeps a mask live | src/core/unit.c at tag v262, lines 3859-3915 (fragment_mtime_newer with the masked null_or_empty branch, unit_need_daemon_reload drop-in list equality, masked drop-ins omitted) and 1439-1451 (UNIT_MASKED early return in unit_load_fragment_and_dropin); snapshot sha256 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7 | The reload flag is structural and mtime-based together: a differing drop-in path list, a newer fragment or drop-in mtime, or a masked path that stopped being null-or-empty each raise it, so editing a drop-in without a reload leaves the running manager on the old bytes | mined | 2026-11-03 | on-release | corpus/knowledge/systemd-unit-load-plane-r73.md |
| S306 | systemd v262 src/shared/install.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c | code | A | The install-time mask and alias plane that grounds UL5-UL6: the dev/null mask symlink with its runtime-versus-persistent config path, the generator-mask refusal, and the dangling alias change report | src/shared/install.c at tag v262, lines 340-355 (INSTALL_CHANGE_IS_MASKED, INSTALL_CHANGE_IS_MASKED_GENERATOR and INSTALL_CHANGE_IS_DANGLING reports), 2350-2391 (unit_file_mask writes a /dev/null symlink and UNIT_FILE_RUNTIME selects the runtime config path) and 2393-2445 (unit_file_unmask refuses a generator mask); snapshot sha256 c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d | A mask is a symlink to /dev/null at the config path chosen by UNIT_FILE_RUNTIME, and a mask that a generator supplies is reported as unmaskable instead of being removed, so the two planes and the generator refusal are distinguishable from the mask being absent | mined | 2026-11-03 | on-release | corpus/knowledge/systemd-unit-load-plane-r73.md |
| S307 | Arch rendered systemd.unit(5), systemd 262.1 — https://man.archlinux.org/man/systemd.unit.5 | docs | A | Arch's rendered systemd.unit(5) page as packaging output, screened for divergence from the v262 upstream manual page held as S304 | Rendered HTML, footer systemd 262.1; 135978 bytes, HTTP 200, sha256 69dba09794c028cbb69c7210b52c705f2e6df103def4ab099c082913fd927916 identical across two fetches on 2026-11-03; carries the load-path override and drop-in lexicographic sentences verbatim, the SYSTEMD_UNIT_PATH sentence once markup is stripped, and 0 line-anchor markers | REJECTED: the rendered page reproduces the same upstream manual text already pinned as S304 in every merge and precedence sentence compared, at renderer version 262.1 rather than tag v262, and its HTML carries 0 line-anchor markers, so it grounds no rule S304 does not and cannot supply a tag-pinned line anchor; flip: a rendered page carrying an Arch patch that changes the merge, precedence or mask wording, which would make it evidence of packaging drift | rejected | 2026-11-03 | on-release | — |
| S308 | Arch core/systemd package page, 262.1-1 — https://archlinux.org/packages/core/x86_64/systemd/ | docs | A | Build provenance of the Arch core/systemd package the host runs: version, packager and build date as a packaging record, not a rule statement | Package page title Arch Linux - systemd 262.1-1 (x86_64), Last Packager Christian Hesse, Build Date 2026-10-17 08:46 UTC; 101009 bytes, HTTP 200 on 2026-11-03; no content digest claimed because two consecutive fetches differ only in a per-response CSP nonce at line 2966 (sha256 a058f5bdcac929f51d3a0f1370cb68dc43a5db90ee448200986f329ec568be07 then 2cb1b0c221f81423d654493fff8c8f83dfadfb5fadcdaae68c00a38f76379727) | REJECTED: the page is build provenance only (version 262.1-1, packager, build date) and contains no drop-in, load path or masked text (case-insensitive occurrence count 0), while the host's installed version is an own-work reading rather than a rule source; flip: a package page or linked changelog entry naming a packaging change to the unit-loading code or the man page | rejected | 2026-11-03 | on-release | — |

## Measurement log for the two refusals

```
# rendered man page, twice
curl -sS -L --max-time 45 -o man.1.html -w '%{http_code} %{size_download}' \
  https://man.archlinux.org/man/systemd.unit.5
  -> 200 135978   sha256 69dba09794c028cbb69c7210b52c705f2e6df103def4ab099c082913fd927916
curl ... -o man.2.html https://man.archlinux.org/man/systemd.unit.5
  -> 200 135978   sha256 69dba09794c028cbb69c7210b52c705f2e6df103def4ab099c082913fd927916   (cmp: identical)
grep -o 'systemd 262\.[0-9]' man.1.html                                  -> systemd 262.1
grep -c 'id="l[0-9]\+"\|data-line' man.1.html                            -> 0
grep -o -F 'override files with the same name in' man.1.html | wc -l     -> 1
grep -o -F 'lexicographic order, regardless of' man.1.html | wc -l       -> 2
grep -o -F 'Drop-in files under any of these directories take precedence' man.1.html | wc -l -> 1
# rendered text of the SYSTEMD_UNIT_PATH paragraph, tags stripped
"When the variable $SYSTEMD_UNIT_PATH is set, the contents of this variable overrides the unit load path."

# package page, twice
curl ... -o pkg.1.html https://archlinux.org/packages/core/x86_64/systemd/
  -> 200 101009   sha256 a058f5bdcac929f51d3a0f1370cb68dc43a5db90ee448200986f329ec568be07
curl ... -o pkg.2.html https://archlinux.org/packages/core/x86_64/systemd/
  -> 200 101009   sha256 2cb1b0c221f81423d654493fff8c8f83dfadfb5fadcdaae68c00a38f76379727
diff pkg.1.html pkg.2.html                                               -> 2 lines, one hunk:
  2966c2966
  < <script type="text/javascript" nonce="BMWveAknmhoyT6Y5QHujQw==">
  > <script type="text/javascript" nonce="WkENqw3PhTF0UT/wHegemg==">
grep -ci 'drop-in\|load path\|masked' pkg.1.html                          -> 0
grep -o '<title>[^<]*' pkg.1.html                                        -> <title>Arch Linux - systemd 262.1-1 (x86_64)
Last Packager: Christian Hesse      Build Date: 2026-10-17 08:46 UTC
```
