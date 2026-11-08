# Limine gate r92 — the battery's oracle channel, and the visibility era at 12.9.5

source: S377 (Python 3 docs, `-P`/`-I`), S378 (bubblewrap manual), S379 (Limine v12.9.6 `common/lib/config.c`), S380 (Limine v12.9.6 ChangeLog), S381 (Limine issue #700), all opened 2026-11-08; S352/S353/S361/S362/S374-S376 re-opened from the pinned tag files
recheck: re-open S379/S380 on any `limine` package update (cadence on-release, the V2 boundary moves with upstream); re-run `python3 tools/limine-pin-battery-r92.py --isolation-check` on any python or bubblewrap upgrade (30d), and re-open S377/S378 then
verified-at: 2026-11-08

Round 92. Two independent facts the lane did not hold: (a) why a battery that launches the gate as a
child process cannot certify a gate that reads the battery's own oracle, and what a launcher must do
to close the read channels; (b) that the global-section visibility rule the gate models is
version-selected, and where the boundary sits.

## OI — the oracle channel and the launcher contract

OI1. **The r91 battery handed the judge to its subject.** It ran `[sys.executable, gate, ...]`
(`tools/limine-pin-battery-r91.py:1635`), so a `tools/`-resident gate had the battery's own directory
as `sys.path[0]`; importing `limine-pin-battery-r91.py` and calling `Case.finish()` /
`want_on_panic()` / `want_unverified()` answered every consequence, `on_panic` and U1 field without
modelling any rule. Measured at `2d7e09e1`: `tools/sibling-oracle-forgery.py` reads `82/82 verdict
met` rc 0 (`.ufo/waves/round-91/w1/ScribeLesson/receipts/channel-open.json`).

OI2. **A private copy closes the sibling and `sys.path` channels.** The gate's bytes are copied into a
directory that holds nothing else, and `python3 -I` runs the copy: `-P` keeps the script's directory
off `sys.path`, `-I` implies `-P`, `-E` and `-s`, so neither the copy's directory nor the user site is
importable and every `PYTHON*` variable is ignored (S377). The measured probe reports
`sibling_files: ["gate.py"]` and a `sys_path` without the copy directory
(`limine-pin-battery-r92.py --isolation-check`).

OI3. **A mount and PID namespace closes absolute-path, `/proc` and environment channels.** The
launcher runs `bwrap --unshare-all --die-with-parent --new-session --clearenv` with only `/usr` and
`/etc` read-only, a fresh `/dev`, `/proc` and `/tmp`, the case directory and the gate copy mounted
read-only, cwd set to the case directory, `PATH=/usr/bin HOME=/tmp LC_ALL=C TMPDIR=/tmp` (S378:
`--unshare-all` unshares user, ipc, pid, net, uts and cgroup; `--clearenv` unsets everything except
`PWD`). The probe sees an empty root apart from the allowlist, `lane_visible: false`,
`battery_visible: false`, PIDs `["1","2"]`, and only the four variables the launcher sets.

OI4. **What the launcher does not close.** Inference from behaviour (timing, the shape of a fixture,
the number of runs) and a gate that reimplements the rule text honestly are outside the contract;
the battery's 89 families certify rule-following, not authorship. A control that crashes is an
`error:` row, never evidence of rejection (QUALITY 126), which is why every channel control degrades
to a wrong-but-valid verdict instead of raising.

## EV — the visibility era boundary

EV1. **v12.9.4 cut once, with a first-line exception.** `init_config` set `config_ready`, built the
tree, then walked back from the first entry's `/` to `config_addr` and NULed `c[-1]` only when
`c > config_addr`; when the first physical line was itself an entry line the guard was false and the
whole file stayed visible (S376, raw 638-650; v12.9.4 behaviour confirmed by the r91 families).

EV2. **v12.9.5 parses in place and the exception is gone.** `create_menu_tree()` scans forward for the
first line-initial `/`, cuts before it (`if (p > config_addr) { *(p - 1) = '\0'; }`, raw 328-330), then
NULs the end of the label line (raw 362-365). `config_get_value` reads the same buffer afterwards
(`config_ready` raw 666, `menu_tree = create_menu_tree()` raw 668, the accessor raw 733+), so a config
whose first line is an entry line exposes **no** global key (S379). The gate's V2 rule mirrors this:
from 12.9.5 on the global section is the lines before the first entry line, with no exception.

EV3. **v12.9.5 and v12.9.6 are one rule for this clause.** The two pinned `config.c` files are
byte-identical (sha256 `a940acae…` both, `.ufo/waves/round-92/before/src/SHA256SUMS`), so the gate maps
every `>= 12.9.5` to one era instead of enumerating releases.

EV4. **Upstream states the change as intended.** ChangeLog 12.9.6: *"A config whose first line is an
entry has had no global options since 12.9.5, whereas every option in it used to count as global"*
(S380); issue #700 (S381, community tier C, lead only) traces the same `p == config_addr` skip and adds
the NixOS `extraConfig` effect. S380 is the authoritative statement; S381 corroborates.

EV5. **The host is still in the older era, and will not be for long.** `pacman -Q limine` reads
`limine 12.9.4-1` and `limine --version` reads `Limine 12.9.4` this round; Arch `extra` already ships
`12.9.6-1` (ScoutDrift r91 §3). The gate's default is therefore `12.9.4` (the installed package) and
the flag is the operator's declaration of the target — the gate never guesses the host version by
shelling out, so its answer is a function of the conf and the declared version only.

## Where the gate's answers change (r92 family map)

| family | `--limine-version` | first line | expected answer |
|---|---|---|---|
| ERA-FLE-PANIC-A | 12.9.4 | `/entry` | mismatch → `prompt` (key visible) |
| ERA-FLE-PANIC-B | 12.9.6 | `/entry` | mismatch → `panic` (key invisible) |
| ERA-FLE-MEASURED-A | 12.9.4 | `/entry` | `on_panic: halt` with `--tpm-present 1` |
| ERA-FLE-MEASURED-B | 12.9.6 | `/entry` | `on_panic: menu` (key invisible) |
| ERA-GLOBAL-KEY-A/B | 12.9.5 / 12.9.6 | header + `/entry` | `prompt` both — the flag must not move a non-first-line case |
| ERA-DEFAULT | flag omitted | `/entry` | `prompt` — the default is 12.9.4 |

Everything else in the r92 roster answers identically in both eras, because the cut position is the
same whenever a non-entry line precedes the first entry.
