# Results

The sibling artifact `w1/ExecProbeR36/probe-child-env-allowlist-r36.py` was absent when checked. Therefore no fixture was run against the landed/sibling probe normalizer; all four probe-normalization results remain **unverified / dependency outstanding**. The standalone fixture classifier did emit one row for each class (captured in `classifier-output.txt`); that is not a probe-normalization pass. No pass or gap is claimed for the sibling implementation.

Expected fixture behavior for wave 2 is in `classes.md` and is emitted by `classify_norm_fixtures.py`:

| Fixture | Expected class | Expected behavior | Probe result |
|---|---|---|---|
| `SHORT_HASH=deadbee` | short hash | Normalize 7-character lowercase hex token in parity material. | Not run: probe absent. |
| `FIXTURE_PATH=.../adjacency-git-4e5f6071/fixture-tree` | fixture/scratch path components | Normalize only volatile sandbox components; preserve stable suffix/structure. | Not run: probe absent. |
| `GIT_CEILING_DIRECTORIES=.../t0245a7535668` | run-private GIT_CEILING/TMPDIR | Canonicalize exact run TMPDIR when carried as the intentional private ceiling. | Not run: probe absent. |
| `XDG_CONFIG_HOME=.../home/.config` | HOME-derived config path | Normalize dynamic private HOME prefix, retain `/.config`. | Not run: probe absent. |

The harness itself is a classifier/expected-form generator, not the probe normalizer. Its output is retained separately in `classifier-output.txt`; that output must not be read as a probe conformance pass.
