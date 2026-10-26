Receipts for seat C2ExecLogOracle (item C2-9), round 39 wave 1.

oracle.py            independent parser, written from the pacman.log line grammar only
                     (no import of tools/check-transaction-order-r39.py); prints JSON + per-tx table
oracle-capture.txt   oracle.py on .ufo/waves/round-39/frozen/txcapture/pacman.log
oracle-live.txt      oracle.py on /var/log/pacman.log (same numbers; see drift.txt)
drift.txt            byte identity of live log vs capture, line counts, oracle diff
windows.py/out       second, independent state machine (per-window phase distribution of
                     hook-running and ALPM-SCRIPTLET lines)
prehook.py/out       TO5 host count: 17 PreTransaction hooks, first-install line, Pre-phase runs
selftest.py/out      fixture with known answers + 4 mutants (sensitivity / negative controls)
