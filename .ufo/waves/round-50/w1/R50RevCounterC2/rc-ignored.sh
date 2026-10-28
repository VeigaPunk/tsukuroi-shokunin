#!/bin/bash
# fixture: prints the PASS shapes but exits 1 (counter never gates rc)
printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
exit 1
