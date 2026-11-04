Verdict: scoped host receipts COMPLETE; source-correct configured limit=256M, file limit=32M, observed148.6M.
Unchecked/unobservable here: live daemon loaded configuration and startup min_use floor; parent owns integration gates. LESS_BY formula correction is recorded, not silently accepted.

# E2HostProbe — binding file (round 76 wave w1, executor seat)

Declaration commit `d5f0565bfb42a405ec024d8a5b0796514fb92002`; base `865b38c96c23ec0bcace8ca3ee884f860693ce43`.
Scope: read-only host probes for C1 (journald retention plane) + exact stale-carrier text for C2's `R76-JD-CONFIG-DRIFT` item. Writes confined to this seat dir + scratch. No git/jj mutations, no corpus edits, no vacuum/rotate/flush/restart.

## Final evidence binding
- `01-config.txt`: complete merged configuration; rc=0.
- `02-usage.txt`: all requested probes and outputs; all probe rc=0.
- `03-derivation.txt`: correct saturating-subtraction arithmetic; also exposes the erroneous requested min variant. Configured effective_limit=256M and SystemMaxFileSize=32M.
- `04-stale-carriers.txt`: exact historical text for all three carriers, line anchors, and narrow false-now explanations. Main file comments remain true; merged defaults-only is false.
- `05-usage-rule.txt`: allocated155832320 bytes rounds148.6M; logical209715200; maximum24MiB across13 files. No rotation schedule inferred.
- `report.md` and sibling `../E2HostProbe.md`: scoped findings, risks, parent handoff.
- Owned scratch tree removed successfully; no tool installation or integration verification performed.

Primary risk communicated to parent: LESS_BY means max(free-keep_free,0), not min; default KeepFree caps at4GiB. Journal usage cannot refute coredump-payload usage.
