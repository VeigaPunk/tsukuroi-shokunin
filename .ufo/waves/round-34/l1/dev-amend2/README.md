# L1 development runs of the C1 probe after amendment 2 (not receipts)

Probe VERSION 6, sha256 `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`, run from the lane
working tree against the L1 scratch clone, 2026-10-23 ~09:08Z.

| candidate | pairs | leaking | note |
|---|---|---|---|
| `e1bec241` the drafted change | 27 | 0 | no any-name value, no execveat, no unparsed record |
| `6de666c4` declaration commit | 27 | 27 | any-name clause also fires on every names/quiet pair |
| `b3242da6` dummy (work replaced) | 27 | 18 | base parity |
| `3d77dab9` drafted change plus `ZZ_KEY=os.path.expanduser("~")` in boot-chain's git env | 27 | 3 | names and quiet fire only through the any-name clause (`ZZ_KEY`), which amendment 1 bytes would miss |
