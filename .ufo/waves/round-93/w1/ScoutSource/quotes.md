# Located quotes — ScoutSource (round 93, wave w1)

Every quote below was verified by whitespace-normalised substring match against the pinned bytes
in `pins/` (digests in `pins/SHA256SUMS`; URL / HTTP status / byte count / access date in
`pin-table.tsv`). Access date for every fetch: **2026-11-08 (UTC), 06:10–06:12Z**.
Word counts are given so the ≤25-word contract limit is checkable.

| id | file (tag) | raw lines | quote | words | sha256 of file |
|---|---|---|---|---|---|
| Q1 | `common/lib/config.c` (v12.9.5) | 328-330 | `if (p > config_addr) { *(p - 1) = '\0'; }` | 8 | a940acae… |
| Q2 | `common/lib/config.c` (v12.9.5) | 362-365 | `if (*p == '\n') { *p = '\0'; p++; }` | 8 | a940acae… |
| Q3 | `common/lib/config.c` (v12.9.5) | 298 | `static struct menu_entry *create_menu_tree(void) {` | 7 | a940acae… |
| Q4 | `ChangeLog` (v12.9.5) | 8-9 | `Parse the config in linear time. Configs with thousands of entries were slow to load.` | 14 | d2e08cc4… |
| Q5 | `ChangeLog` (v12.9.6) | 13-16 | `Document that global options must come before the first entry, as has been the case since 4.0.` | 17 | ab280b45… |
| Q6 | `ChangeLog` (v12.9.6) | 13-16 | `A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global.` | 25 | ab280b45… |
| Q7 | `ChangeLog` (v12.9.6) | 16 | `Fixes #700.` | 2 | ab280b45… |
| Q8 | `host/limine.c` (v12.9.5) | 2035 | `puts("Limine " LIMINE_VERSION);` | 4 | 4da21c7c… |
| Q9 | `host/limine.c` (v12.9.5) | 2031 | `puts(LIMINE_VERSION);` | 2 | 4da21c7c… |
| Q10 | `host/limine.c` (v12.9.5) | 2002 | `#define LIMINE_VERSION "%VERSION%"` | 3 | 4da21c7c… |
| Q11 | `host/limine.c` (v12.9.5) | 2090 | `|| strcmp(argv[1], "--version") == 0) {` | 6 | 4da21c7c… |
| Q12 | `host/limine.c` (v12.9.5) | 2091 | `return version(argc - 1, &argv[1]);` | 6 | 4da21c7c… |
| Q13 | `host/limine.c` (v12.9.5) | 2047 | `printf("    --version         Print the Limine version (like the `version` command)\n");` | 9 | 4da21c7c… |

## The four quotes the seat item named

- **(a) the cut `if (p > config_addr) …` at the v12.9.5 tag** — **Q1**, raw **328-330**, in
  `create_menu_tree()` (Q3, raw 298).
- **(b) the label-end NUL** — **Q2**, raw **362-365**.
- **(c) the ChangeLog line naming the parser change** — **Q4**, v12.9.5 `ChangeLog` raw **8-9**
  ("Parse the config in linear time…"). The v12.9.6 statement of the same rule is Q5+Q6+Q7,
  raw **13-16**.
- **(d) the version print line** — **Q8**, `host/limine.c` raw **2035**. The dispatch that
  reaches it is Q11+Q12, raw **2090-2091**; the bare-version form is Q9, raw **2031**; the
  substituted constant is Q10, raw **2002**.

## The file that prints the version — a negative locator, recorded as such

The version is **not** printed by `common/lib/misc.c`. Measured on the pinned v12.9.5 copy
(`pins/limine-v12.9.5-common_lib_misc.c`, sha256 `3b81e321…`):

- `grep -c 'Limine '` → **0**
- `grep -c -- '--version'` → **0**
- `grep -c 'LIMINE_VERSION'` → **0**

The print is in **`host/limine.c`** (Q8). `LIMINE_VERSION` is a build-time placeholder: raw 2002
(Q10) defines it as `"%VERSION%"`, and `GNUmakefile.in` raw **170** substitutes it —
`$(SED) 's/%VERSION%/@PACKAGE_VERSION@/g;s/%COPYRIGHT%/@LIMINE_COPYRIGHT@/g' <…/host/limine.c`
— so the printed number is the **package** version, not a constant in the source.
