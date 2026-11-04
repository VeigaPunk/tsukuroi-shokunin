## Correction 3 (round 74, C2 routed repair; append-only)

R73-GATE-QUOTE-LINE-DRIFT: In the Gate section above, the Gate quotes table for round 73 carried line drift on two sources:
1. S306 (`src/shared/install.c`): the quote `"path = path_make_absolute(*name, config_path);"` was attributed to `install.c:2387`, but in the upstream systemd v262 snapshot the statement sits at install.c:2383 (line 2387 is `RET_GATHER(r, create_symlink(...));`), so install.c:2383 supersedes 2387.
2. S304 (`man/systemd.unit.xml`): the three cited quote anchors included surrounding non-quote lines. The corrected line anchors are :368-370 (superseding :367-370, removing the unquoted introductory clause on line 367), :237-238 (superseding :236-238, removing the preceding sentence tail on line 236), and :238-239 (superseding :238-240, removing the trailing blank line on line 240).
