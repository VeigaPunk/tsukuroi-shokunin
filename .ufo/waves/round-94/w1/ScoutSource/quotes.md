# ScoutSource (round-94 w1) — located quotes

Each quote ≤25 words, with its line location in the pinned bytes
(`.ufo/waves/round-94/w1/ScoutSource/pins/`). Line numbers are raw file lines.

| # | pin | location | quote | words |
|---|---|---|---|---|
| Q1 | limine-v12.9.6-common_lib_config.c | raw 298 | `static struct menu_entry *create_menu_tree(void) {` | 6 |
| Q2 | limine-v12.9.6-common_lib_config.c | raw 328-330 | `if (p > config_addr) { *(p - 1) = '\0'; }` | 10 |
| Q3 | limine-v12.9.6-common_lib_config.c | raw 362-365 | `if (*p == '\n') { *p = '\0'; p++; }` | 9 |
| Q4 | limine-v12.9.6-common_lib_config.c | raw 407 | `}` (closes `create_menu_tree`, so the function spans 298-407) | 1 |
| Q5 | limine-v12.9.6-common_lib_config.c | raw 666 / 668 | `config_ready = true;` / `menu_tree = create_menu_tree();` | 4 / 5 |
| Q6 | limine-v12.9.6-host_limine.c | raw 2031 | `puts(LIMINE_VERSION);` | 2 |
| Q7 | limine-v12.9.6-host_limine.c | raw 2035 | `puts("Limine " LIMINE_VERSION);` | 4 |
| Q8 | limine-v12.9.6-host_limine.c | raw 2089-2091 | `strcmp(argv[1], "version") == 0 || strcmp(argv[1], "--version") == 0) { return version(argc - 1, &argv[1]); }` | 18 |
| Q9 | limine-v12.9.6-ChangeLog | raw 3 | `*** Release 12.9.6 ***` | 4 |
| Q10 | limine-v12.9.6-ChangeLog | raw 14-15 | `A config whose first line is an entry has had no global options since 12.9.5.` | 15 |
| Q11 | limine-v12.9.6-ChangeLog | raw 16 | `used to count as global. Fixes #700.` | 7 |
| Q12 | python-3.15-cmdline.html | `<title>` | `1. Command line and environment — Python 3.15.2 documentation` | 9 |
| Q13 | github-release-v12.9.6.json | `body`, line 1 | `Changelog can be found [here](https://github.com/Limine-Bootloader/Limine/blob/v12.9.6/ChangeLog).` | 10 |
| Q14 | man-archlinux-limine.1.html | "version" footer | `version 12.9.6` / `October 2026` (package `extra/limine` `12.9.6-1`) | 3 |
| Q15 | man-archlinux-limine.8.http404.html | `<title>` | `Page not found — Arch manual pages` | 6 |
