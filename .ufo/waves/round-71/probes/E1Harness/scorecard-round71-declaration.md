## Round 71 — declaration (2026-11-04, base `930d5530`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line **9** / window **3**
unchanged; none retired. A capability entered at round 70 (`xfs-stats-arm`), so the stagnation window is
at 1 of 3 and the nudge does **not** waive the lowest-axis duty. Two claims on two distinct axes
(depth; operability).

Pre-declaration receipts, disclosed in order; all under `.ufo/waves/round-71/before/`.

(a) **Source snapshots** fetched and read before this text, committed byte-exact under `before/src/` with
`SHA256SUMS` (`sha256sum -c` rc 0) and `SOURCES.json` (snapshot → URL, tag, access date, digest), all at
Linux stable **v7.2.11** (the host's own kernel): `Documentation/admin-guide/kernel-parameters.rst`
sha256 `45587d8e…88799`, `kernel/params.c` sha256 `923610d5…782a4`, `include/linux/moduleparam.h`
sha256 `220f2dac…14846`, `kernel/module/main.c` sha256 `e1e1a1c8…95929`. Access date **2026-11-04**.

(b) **Host capture**, read-only (`before/host.txt`, `capture.sh`): kernel `7.2.11-arch1-1`; **136** modules
publish a `parameters` directory and **829** parameter files exist; `nvidia_drm` exposes
`color_pipeline fbdev modeset vblank`, all `-r--r--r--`, `modeset=Y`; `nvidia` exposes 0444
`NVreg_*` parameters; `nvidia_uvm` parameters are `-rw-r--r--` (root-writable) and **no** parameter file
is writable by the unprivileged reader; `/sys/module/btrfs/parameters/read_policy` is **absent**
(the `perm == 0` case S287 names); `modprobe.d` holds 3 files under `/etc` and 4 under `/usr/lib`
(paths and modes only — contents were never read).

(c) **Held-ground sweep** (`before/novelty-sweep.txt`): at base, `modprobe.d`, `kernel-parameters`,
`module_blacklist`, `NVreg`, `module_param`, `kernel_param_ops` and `param_attr_store` each read **0**
file hits across `corpus/ SKILL.md PROVINCE.md`; no knowledge note names the module-parameter surface
(`git ls-tree … | grep -iE 'module|param'` → none); the six notes that mention `/sys/module` read only
`version`/`taint` state.

(d) **Do-nothing controls** (`before/absence-controls.txt`, base `930d5530`): C1 note `git cat-file -e`
rc **128**; C1 counter rc **128**; `^| MP[n]` rows **0**; `R71-C2` labels **0**; per-case-timeout tokens
**0**; selftest **214** PASS rc 0; registry **296** rows; **88** knowledge notes; canonical census
validate rc **0**.

(e) **Frozen counter and its pre-data battery**: `tools/count-mp-rows-r71.py` sha256
`fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`; battery
`before/control/battery.txt` (**12 cases: 1 well-formed control + 11 mutants**) — the control reads
`MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `met=1` rc 0; the eleven mutants
(content-free statement, unbound source, absent quote, short statement, five rows, duplicate id,
snapshot reuse 3, ungrounded statement, malformed invisible row, digest swap) each read `met=0` rc 1.

(f) **Baselines**: `before/selftest-base.txt` → `PASS (214 cases, 214 passed, 0 failed)` rc 0;
`before/census-live-base.txt` → `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED
drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` rc 1; `before/redbefore-timeout.txt`
→ a blocking probe under the selftest's own call shape ends at an **external** 20 s bound with rc **124**
and **0** verdict lines, and the pre-fix census carries 0 `R71-C2` labels and 0 per-case-timeout tokens.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — four new registry rows) | `corpus/knowledge/module-parameter-plane-r71.md` states the kernel module-parameter surface the lane never held: a parameter is visible under `/sys/module/<name>/parameters/` only when its `perm` is nonzero; the file mode **is** the parameter's `perm` and a store handler exists only when a write bit is set; the `kernel_param_ops` contract (set returns 0 or `-errno`, get returns a length or `-errno`, both optional); an unknown parameter is warned and **ignored**, so a typo does not fail the load; `module_blacklist=` refuses the load; and the two specification routes (cmdline `mod.param=v`, modprobe `mod.param=v`) with built-ins requiring the cmdline; rows `MP1`–`MP6`, each `\| MP<n> \| <statement, >= 12 words> \| source=S### \| snapshot=<file> \| digest=<64-hex> \| quote="<text>" \|` | note absent rc **128**, counter absent rc **128**, `^\| MP[n]` rows **0**, registry **296** rows → note present, counter present, `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `MP_TARGET … met=1`, registry **300** rows | `python3 tools/count-mp-rows-r71.py --revision <REV>`; `git show <REV>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` | any row failing a clause, any MP-shaped line that does not parse, one snapshot cited more than twice, fewer than 6 rows / 4 sources / 4 snapshots, or `met=0` → the claim fails |
| C2 | operability (9; capability `selftest-case-timeout`) | `tools/tsukuroi-census.sh` bounds every selftest case: each case child is started in its own process group, polled to a per-case bound (`TSUKUROI_SELFTEST_CASE_TIMEOUT`, default 60 s), killed TERM then KILL when it exceeds it, and reported as a `FAIL` line naming the case and `timeout`; a hermetic self-check case proves the bound fires on a blocking child and does **not** fire on a child that finishes; read-only, no host write, never a verdict term | `R71-C2` labels **0**, per-case-timeout tokens **0**, selftest **214** → labels **>= 3**, selftest `PASS (N cases, N passed, 0 failed)` with **N >= 217**, the suite finishing under an external 300 s bound, and the self-check case asserting both the kill and the no-false-positive arm | `bash tools/tsukuroi-census.sh --selftest \| tail -1`; `grep -c 'R71-C2' tools/tsukuroi-census.sh` | the suite hangs at the external bound, a `R71-C2` case passes with the harness removed (mutation), or the timeout path reports a non-timeout failure → the claim fails |

Causal separability: C1 touches only its note, four registry rows, its counter and receipts; C2 touches
only `tools/tsukuroi-census.sh`. Each verifies without the other. Both predicates are frozen here, before
any note, registry row, census case or receipt exists; the counter and its battery are committed with this
declaration.

Routed repairs this round as work, not as claims (`corpus/lessons/round-70-verifier-spotcheck.md` §5):
D1 the stale selftest tallies in `PROVINCE.md`, `corpus/README.md` and `SKILL.md` corrected append-only
against the final receipt line; D2 the unbacked final-revision re-run claims replaced by committed receipts
at the measured revision; D3 the `count-xs-rows-r70.py` shebang corrected to `python3`; D4 the r70-planned
frozen-counter amendments (statement substance, anchor binding, invisible row, snapshot reuse) carried into
this round's counter. Assimilation: **none** — the open L0 `tsukuroi | round-64` addendum still rules the
merge package quarantined. `considerthese`: no proposal mined; the measured status of the four proposals in
`considerthese/2026-10-26.md` is recorded in the lesson, and the scoreboard is continued as the standing
ledger.

Wave w1: one v1 wave, band 8–16, **14 seats**; seat shape and counts are fixed in
`.ufo/waves/round-71/w1-spec.json`.

**planned (next round):** the C1 counter's remaining bookkeeping channels if attack finds any; the r70
arm's literal-predicate amendment (`present + absent + unreadable == mounts`, a named verifier-side
enumerator for `error`/`log`); the AR resolve-then-count debt; no amendment of this round's frozen
predicates.
