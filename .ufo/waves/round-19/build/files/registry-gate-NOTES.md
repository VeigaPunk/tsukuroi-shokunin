# Registry coverage gate draft

[obs] The draft uses the shared revision binder, reads committed regular blobs, selects the unique highest operative heading, and evaluates table coverage and row findings (`tools/check-registry-coverage.py:15-17,34-100,132-177,198-241`).

[obs] The bound baseline has the operative round-18 registry at `SKILL.md:1952-1970`; the closure records 14 tool files versus 13 rows and identifies `_revision.py` as the unregistered library (`corpus/lessons/round-18-verifier-spotcheck.md:171-173`).

[obs] Hermetic fixture selftest output: `PASS (12 cases, 12 passed, 0 failed)`. Cases cover clean, missing/duplicate/orphan rows, invalid kind, unresolved selftest flag, incomplete gate verdict, unique-highest selection, duplicate-highest and absent table, baseline split counts, and invalid revision (`tools/check-registry-coverage.py:397-520`). The authorized CLI help invocation exposed `--revision`, `--branch`, `--baseline-tools`, and `--selftest`.

[obs] Retained baseline run: `.ufo/waves/round-19/build/files/registry-gate-baseline.stdout:1` reports `FAIL`, 14 tools, 13 rows, 13 registered, one missing (`tools/_revision.py`), and finding `REGISTRY-ROW-MISSING`; exit 1 is expected for the documented closure defect.

[inf] `--baseline-tools` compares that revision's regular-file tool set with coverage in the inspected revision and lists newly present paths as `discovered_tools`; it does not treat a historical registry as operative.

[unk] No post-integration revision run was authorized; L1 owns integration and the final gate invocation.