# fixture skill

## Gate and probe registry — round1 superseding current rows

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| limine-pins | gate | `python3 tools/check-limine-pins.py` (default `auto`) | 0 ok;1 bad;2 cannot | `python3 tools/check-limine-pins.py --selftest` (3 fixtures) | schema `tsukuroi-fixture-gate-v1` | none | fixture |
| limine-pin-battery-r96 | gate | `python3 tools/limine-pin-battery-r96.py --gate <PATH>` | 0 met (every family in the literal FAMILY_ROSTER, 4, passed all 2 cases); 1 unmet; 2 usage | none | roster 4 (four families) | none | fixture |
| check-r96-calibration | probe | `python3 tools/check-r96-calibration.py` | 0 ok;1 findings;2 usage | `python3 tools/check-r96-calibration.py --selftest` (2 cases) | ids | none | fixture |
| make-r96-bends | library | `python3 tools/make-r96-bends.py` | 0 ok;1 mismatch;2 unused | none | VARIANTS N01,N03 | fixture dir | fixture |
