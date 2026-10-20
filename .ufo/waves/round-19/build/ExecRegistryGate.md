# ExecRegistryGate — C3

[obs] Drafted `.ufo/waves/round-19/build/files/tools/check-registry-coverage.py` with revision binding, unique-highest table selection, coverage/row findings, baseline tool-set counts, and sorted JSON output (`.ufo/waves/round-19/build/files/registry-gate-NOTES.md:3`).

[obs] Hermetic selftest passed: 12/12 cases; CLI help exposes the requested flags (`.ufo/waves/round-19/build/files/registry-gate-NOTES.md:7`).

[obs] The authorized baseline run is red as expected: 14 tools, 13 rows, only `tools/_revision.py` missing (`.ufo/waves/round-19/build/files/registry-gate-baseline.stdout:1`; interpretation and closure cross-check: `.ufo/waves/round-19/build/files/registry-gate-NOTES.md:5,9`).

[unk] No post-integration revision run was authorized; L1 owns integration and the final gate invocation (`.ufo/waves/round-19/build/files/registry-gate-NOTES.md:13`). No tools were installed. Answering model: openai-codex/gpt-6-luna.

Scope: executed=mktemp -d, git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tmp.pXnBuiAD2J/lane, git -C /tmp/tmp.pXnBuiAD2J/lane checkout 452a054677f6b18284917d7c08c45361f91c25ac, git -C /tmp/tmp.pXnBuiAD2J/lane remote remove origin, python3 tools/check-registry-coverage.py --selftest, python3 tools/check-registry-coverage.py --help, python3 tools/check-registry-coverage.py --revision 452a054677f6b18284917d7c08c45361f91c25ac > /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/registry-gate-baseline.stdout