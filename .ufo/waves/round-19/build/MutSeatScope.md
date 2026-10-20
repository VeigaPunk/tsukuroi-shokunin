# MutSeatScope

Model: openai-codex/gpt-6.1-sol. Axes: calibration, operability, byte-exact restoration.

[obs] In an isolated baseline clone, committed the requested two-seat fixture (`aa6e352ae6dbc7acdc8376c123b198978b77d600`). The unchanged 30-second detector requires exactly one unauthorized finding for `NoExecSeat.md`, none for the authorized seat: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutSeatScope.txt:52-59.

[obs] Mutated only gate line 88: `if EXEC_MARK not in seat.prompt:` → `if False:`. Pristine/restored: exit 1, exactly one `SCOPE-EXEC-UNAUTHORIZED`; mutated: exit 0, zero findings. All stderr empty: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutSeatScope.txt:61-88.

[inf] **KILLED** by the expected-red detector. Reject “baseline failure” and “green means survived”: the expected negative fixture passes its detector before/after restoration and fails under mutation: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutSeatScope.txt:102-106.

[obs] Restored bytes equal the retained original; SHA-256 before/restored `add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac`; mutated `2038c20005eaad627aeeeeafaa07ea41287907e04d7ebc88cd432bd8a45838c8`. Fixture hashes unchanged: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutSeatScope.txt:90-100.

[unk] Full-wave authorization and actual execution remain unmeasured. [obs] No installs; author-side probe only, no admission: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/build/files/MutSeatScope.txt:104-109.

Scope: executed=mktemp -d,git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tmp.4NjsguiM4d/lane,git -C /tmp/tmp.4NjsguiM4d/lane checkout -B master 452a054677f6b18284917d7c08c45361f91c25ac,git -C /tmp/tmp.4NjsguiM4d/lane remote remove origin,git -C /tmp/tmp.4NjsguiM4d/lane add -f -- .ufo/waves/round-19/scope-fixture/spec.json .ufo/waves/round-19/scope-fixture/AuthorizedSeat.md .ufo/waves/round-19/scope-fixture/NoExecSeat.md,git -C /tmp/tmp.4NjsguiM4d/lane -c user.name=tsukuroi-shokunin -c user.email=tsukuroi@shokunin.local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --no-verify -m 'test: round-19 two-seat authorization mutation fixture' -- .ufo/waves/round-19/scope-fixture/spec.json .ufo/waves/round-19/scope-fixture/AuthorizedSeat.md .ufo/waves/round-19/scope-fixture/NoExecSeat.md,python3 /tmp/tmp.4NjsguiM4d/lane/tools/check-seat-scope.py --wave .ufo/waves/round-19/scope-fixture --revision aa6e352,python3 /tmp/tmp.4NjsguiM4d/lane/tools/check-seat-scope.py --wave .ufo/waves/round-19/scope-fixture --revision aa6e352,python3 /tmp/tmp.4NjsguiM4d/lane/tools/check-seat-scope.py --wave .ufo/waves/round-19/scope-fixture --revision aa6e352
