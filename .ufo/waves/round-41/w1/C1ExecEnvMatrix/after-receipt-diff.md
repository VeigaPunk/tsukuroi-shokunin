# C1 counter determinism: declared after receipt vs this seat's two runs

after receipt: revision 568c397da11339aed65181be598414f268835555, branch_tip c7c40c0f370bcbaf4246de70a08c017119607c0f, finished_utc 2026-10-26T17:23:56Z, result PASS
jobs1: revision 568c397da11339aed65181be598414f268835555, branch_tip 71851d636ab1bffaf8fee5016617c88878a666f1, result PASS
jobs6: revision 568c397da11339aed65181be598414f268835555, branch_tip 20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7, result PASS

| mutant | after fail_count | jobs1 | jobs6 | after first_fails hostname-guard |
|---|---|---|---|---|
| M1-VA-device-literal | 6 | 6 | 6 | 0 |
| M2-VB-root-mountpoint | 6 | 5 | 5 | 1 |
| M3-VC-substring-btrfs | 1 | 1 | 1 | 0 |
| M4-VG-subvolid-256 | 6 | 5 | 5 | 1 |
| M5-a-grep-count | 2 | 1 | 1 | 1 |
| M6-b-fstype-casefold | 1 | 1 | 1 | 0 |
| M7-e-guard-drops-blocked | 1 | 1 | 1 | 0 |
| M8-subvol-at-literal | 5 | 5 | 5 | 0 |
| M9-last-line-only | 3 | 2 | 2 | 1 |
| H5-mountpoint-absolute | 1 | 1 | 1 | 0 |
| H6-source-devonly | 1 | 1 | 1 | 0 |
| H9-subvolkey-option | 2 | 1 | 1 | 1 |
| H10-count-exactly-one | 1 | 1 | 1 | 0 |

extra after-receipt FAIL text (verbatim): "hostname override not honoured — possible host read"
every after-receipt kill confirmed on storage-arm labels only:
  M1-VA-device-literal       killed=True confirmed=True confirm=6 storage=6 hostname=0
  M2-VB-root-mountpoint      killed=True confirmed=True confirm=5 storage=5 hostname=0
  M3-VC-substring-btrfs      killed=True confirmed=True confirm=1 storage=1 hostname=0
  M4-VG-subvolid-256         killed=True confirmed=True confirm=5 storage=5 hostname=0
  M5-a-grep-count            killed=True confirmed=True confirm=1 storage=1 hostname=0
  M6-b-fstype-casefold       killed=True confirmed=True confirm=1 storage=1 hostname=0
  M7-e-guard-drops-blocked   killed=True confirmed=True confirm=1 storage=1 hostname=0
  M8-subvol-at-literal       killed=True confirmed=True confirm=5 storage=5 hostname=0
  M9-last-line-only          killed=True confirmed=True confirm=2 storage=2 hostname=0
  H5-mountpoint-absolute     killed=True confirmed=True confirm=1 storage=1 hostname=0
  H6-source-devonly          killed=True confirmed=True confirm=1 storage=1 hostname=0
  H9-subvolkey-option        killed=True confirmed=True confirm=1 storage=1 hostname=0
  H10-count-exactly-one      killed=True confirmed=True confirm=1 storage=1 hostname=0
