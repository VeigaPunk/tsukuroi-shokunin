# C1-X5 signal matrix — frozen census ae99f021, spaced TMPDIR, bash 5.3.20(1)
# signals to the census bash pid unless noted; one run at a time; fixture offset = wrapper mktemp
# timestamp minus process start

| trial | signal(s) | rc | fixture created (offset s) | fixture after exit | fixture after my cleanup | PASS line | note |
|---|---|---|---|---|---|---|---|
| baseline | - | 0 | True (0.011) | False | False | True | no signal; full selftest (60.9 s) |
| int | SIGINT@2.021 | 130 | True (n/a) | False | False | False | SIGINT to pid |
| term | SIGTERM@2.021 | 143 | True (n/a) | False | False | False | SIGTERM to pid |
| hup | SIGHUP@2.021 | -1 | True (n/a) | False | False | False | SIGHUP to pid; dies by signal (Python rc -1) |
| quit | SIGQUIT@2.021 | 0 | True (0.01) | False | False | True | SIGQUIT ignored by bash; run completed (88.0 s) |
| kill | SIGKILL@2.021 | -9 | True (n/a) | True | True | False | SIGKILL; no trap can run |
| term2 | SIGTERM@2.021,SIGTERM@2.021 | 143 | True (n/a) | False | False | False | TERM, second TERM ~0.2 ms later |
| term-early | SIGTERM@0.3 | 143 | True (0.015) | False | False | False | TERM at 0.30 s |
| int-group | SIGINT@2.021 | 130 | True (n/a) | False | False | False | SIGINT to process group (Ctrl-C) |
| term2b | SIGTERM@2.021,SIGTERM@2.122 | 143 | True (0.011) | False | False | False | TERM, second TERM 100 ms later |
| sweep-030 | SIGTERM@0.03 | 143 | True (0.013) | False | False | False | TERM at 0.03 s |
| sweep-050 | SIGTERM@0.05 | 143 | True (0.013) | False | False | False | TERM at 0.05 s |
| sweep-070 | SIGTERM@0.07 | 143 | True (0.013) | False | False | False | TERM at 0.07 s |
| sweep-090 | SIGTERM@0.091 | 143 | True (0.011) | False | False | False | TERM at 0.09 s |
| sweep-110 | SIGTERM@0.11 | 143 | True (0.01) | False | False | False | TERM at 0.11 s |
| sweep-130 | SIGTERM@0.13 | 143 | True (0.013) | False | False | False | TERM at 0.13 s |
| sweep-150 | SIGTERM@0.15 | 143 | True (0.013) | False | False | False | TERM at 0.15 s |
| sweep-180 | SIGTERM@0.18 | 143 | True (0.011) | False | False | False | TERM at 0.18 s |
| sweep-210 | SIGTERM@0.21 | 143 | True (0.01) | False | False | False | TERM at 0.21 s |
| sweep-240 | SIGTERM@0.24 | 143 | True (0.01) | False | False | False | TERM at 0.24 s |
| sweep-270 | SIGTERM@0.27 | 143 | True (0.01) | False | False | False | TERM at 0.27 s |
| sweep-300 | SIGTERM@0.3 | 143 | True (0.011) | False | False | False | TERM at 0.30 s |
| sweep-330 | SIGTERM@0.33 | 143 | True (0.011) | False | False | False | TERM at 0.33 s |
| sweep-360 | SIGTERM@0.36 | 143 | True (0.011) | False | False | False | TERM at 0.36 s |

Duplicate trial names (baseline, quit, term-early) resolved to the rerun: the first-batch working
directory was re-created for the receipt rerun, so those three rows come from the rerun.
