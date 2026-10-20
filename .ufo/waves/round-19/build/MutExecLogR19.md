# MutExecLogR19

Model: openai-codex/gpt-6.1-sol. Axes: operability (actual capture compatibility), calibration (non-vacuous rejection); constraint: byte-exact restoration. Author-side mutation evidence only; no admission authority.

- [obs] Isolated `--no-hardlinks` clone started at `452a054677f6b18284917d7c08c45361f91c25ac`; origin removed. Expected detector: pristine PASS → mutated EXEC-STEER-VIOLATION → restored PASS. Setup: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutExecLogR19.txt:5-23.
- [obs] Pristine commit `b10240740ea68b010278ac174c63c1cae3501396`: PASS, `exec_violation_count=0`. Output: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutExecLogR19.txt:30-33.
- [obs] One mutant appended two inert lines: `$ pacman -Qi limine` and `$ bash -c 'pacman -Q snapper'`. Commit `b8b7e34ceed06392f8b991c8b63f5a4221ac3aa6`: FAIL, exit 1, two EXEC-STEER-VIOLATION findings at capture lines 614 and 615 respectively. Neither probe executed. Output: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutExecLogR19.txt:35-47.
- [obs] Exact-byte restoration committed as `70b894ba8941f4c598fc3931c203b33f8141148c`: PASS, zero violations; original capture unchanged. Before/restored SHA256 `2b1dc96a80781d6994ab42de934bcb548f32b9fc529461b719168f301924fbce`; mutant `ba0769bfd6ee96b9ba2fb69326cf186dcb64f1fd5ce6c435796f30886834fa6e`. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutExecLogR19.txt:42-58.
- [obs] Rejected preliminary hashing of decorated/truncated `read :raw` output; retained only exact-file-byte SHA256 measurements. No installs/updates or production-source changes. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutExecLogR19.txt:63-65.
- [inf] **KILLED**, including the disguised form by its separate finding site. This establishes failure capability for these two forms, not exhaustive shell coverage; no detector fix needed for this probe.

Scope: executed=mktemp -d,git clone --no-hardlinks,git checkout -B master,git remote remove origin,cp,git add,git commit,python3 tools/check-recheck-commands.py
