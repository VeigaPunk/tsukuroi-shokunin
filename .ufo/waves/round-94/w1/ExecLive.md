# ExecLive — C2 live inventory leg (unprivileged probe + era visibility)

Gate: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py`
sha256 `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` (verified before use).
Scratch: `/fast/scratch/hyaku/tsukuroi-r94/ExecLive/` (tree left in place for Main's gate; NOT deleted — Main's post-integration sweep owns it; seat scratch otherwise contained).
Receipts: `.ufo/waves/round-94/w1/ExecLive/` (probe JSON, both era JSONs, strace log, flag-free JSON, staged fakes, identical confs).

Scope note: `/boot/limine.conf` is root-only; this seat did not attempt to read it. "Live" here = the probe (`probe_limine_version`) + flag-free gate runs against a fake conf/esp, plus the flag-free run against the host's real `limine` (12.9.4, `/usr/bin/limine --version` → `Limine 12.9.4`).

## Leg 1 — probe shapes

Staged copies of the committed fixtures (`.ufo/waves/round-94/before/fake-limine/`), each `chmod +x`, then `probe_limine_version(exe)` imported from the frozen gate. Raw fixture bodies verbatim:

| shape | raw | exec rc / stdout / stderr | `probe_limine_version` |
|---|---|---|---|
| `no-version-here` | `echo "no version here"` | rc 0, stdout `no version here\n`, stderr empty | **None** |
| `suffixed-rc` | `echo "Limine 12.9.6-rc1"` | rc 0, stdout `Limine 12.9.6-rc1\n`, stderr empty | **None** |
| `stderr-version` | `echo "Limine 12.9.6" >&2` | rc 0, stdout empty, stderr `Limine 12.9.6\n` | **None** |
| `era-b-real` | `echo "Limine 12.9.6"` | rc 0, stdout `Limine 12.9.6\n`, stderr empty | **`12.9.6`** |

Receipt: `leg1-probe.json` (`{"no-version-here":null,"suffixed-rc":null,"stderr-version":null,"era-b-real":"12.9.6"}`).
Verdict leg 1: **all three non-`era-b-real` shapes read None; `era-b-real` reads `12.9.6`.** Matches C1 AUTO-PROBE-SHAPES probe half (no-version / suffixed / stderr-only all refused by the probe).

Each of the three None shapes was also run end-to-end (fake `limine` on PATH, NO `--limine-version` flag, fake conf/esp): **rc 64, stdout 0 bytes**, stderr exactly:
```
usage: check-limine-pins.py [-h] [--conf CONF] [--esp ESP]
                            [--secure-boot-enforced {0,1}]
                            [--tpm-present {0,1}]
                            [--limine-version LIMINE_VERSION] [--live]
                            [--selftest]
check-limine-pins: --limine-version auto: `limine --version` probe failed
```
(all three shapes identical; stderr captured per-shape in scratch `refuse-*/err.txt`).

## Leg 2 — era visibility flip via flag-free auto probe

One conf, identical bytes both runs (sha256 `deddd91966…0fb0665d6f`, receipt `eraA/limine.conf` = `eraB/limine.conf`):
```
/e
protocol: efi
path: boot():/EFI/Linux/a.efi#<mismatch hash>   (128 hex, differs from blake2b of file content)
hash_mismatch_panic: no
```
ESP: `EFI/Linux/a.efi` = `kernel-a` for both. Fake `limine` on PATH per-subdir (eraA: `echo "Limine 12.9.4"`, eraB: `echo "Limine 12.9.6"`). Invocation (no `--limine-version`):
`python3 tools/check-limine-pins.py --conf <sub>/limine.conf --esp <sub>/esp --secure-boot-enforced 0`

| run | probe answer | rc | `limine_version` | `limine_version_source` | `visibility_era` | pin (line 3) consequence | `hash_mismatch_panic` |
|---|---|---|---|---|---|---|---|
| eraA (12.9.4) | 12.9.4 | 1 | 12.9.4 | probe | `pre-12.9.5` | `prompt` | `{line:4, value:no}` |
| eraB (12.9.6) | 12.9.6 | 1 | 12.9.6 | probe | `12.9.5+` | `panic` | `null` |

Receipts: `eraA-out.json` (sha256 `ea27ab3b…e35`), `eraB-out.json` (sha256 `5b40252e…e85`).
Verdict leg 2: **same conf reads `prompt` for era A and `panic` for era B.** Conf line 1 is an entry, so pre-12.9.5 keeps the body visible (`hash_mismatch_panic: no` seen, prompt) and 12.9.5+ cuts the global section at the first entry (`hash_mismatch_panic: null`, panic). Both runs stderr 0 bytes; JSON single line on stdout.

## Leg 2b — flag-free run against real installed limine

`which limine` → `/usr/bin/limine`; `limine --version` → `Limine 12.9.4` (+ copyright lines), rc 0.
Flag-free gate run (no flag, real PATH, scratch conf/esp): rc 1, `limine_version=12.9.4`, `limine_version_source=probe`, `visibility_era=pre-12.9.5`, stderr 0 bytes. Receipt: `flagfree-real.json`. Matches C2's "flag-free live run prints version 12.9.4 and source probe" (against a scratch conf; `/boot/limine.conf` not read).

## Leg 3 — probe never writes

Ran the eraA flag-free gate under `strace -f -e trace=openat,execve,mkdir,unlink,rename,write,connect,open` from an empty case dir. strace available: yes (`/usr/bin/strace`).

- Case dir before == after: empty (no temp file created). Receipt log: `leg3-strace.log` (202 lines).
- `execve`: 2 only — `python3 <gate> …` and `…/eraA/bin/limine ["limine","--version"]`.
- `openat`: all `O_RDONLY|O_CLOEXEC` except one failed `O_RDWR` probe by the shell child (`/dev/tty`, `ENXIO`, from the fake's tty handling, not the gate). Zero `O_WRONLY`/`O_CREAT` by the gate. The trace's only `write()` calls: fake writes `Limine 12.9.4\n` (14 B) to its stdout; gate writes the JSON verdict (861 B + `\n`) to stdout. Strace-traced stdout sha256 == untraced `eraA-out.json` (`ea27ab3b…e35`).
- No `connect`/`socket` lines in the trace (gate does none; subprocess probe has no network surface).
- Name-resolution/open targets are read-only system paths (`ld.so.cache`, locales, ssl cnf — Python/loader); gate-relevant opens: `check-limine-pins.py` (read), `eraA/limine.conf` (`O_RDONLY`), `eraA/esp/EFI/Linux/a.efi` (`O_RDONLY`).

Verdict leg 3: **probe writes nothing; stdout-only as claimed.** Caveat: the `strace -e` filter covered the traced syscalls only; no `mmap`/`pipe` enumeration, but the before/after case-dir check plus `O_CREAT`-absence covers the "no temp file" claim.

## Leg 4 — selftest sanity (supplementary)

`tools/check-limine-pins.py --selftest` → **PASS 39/39**, rc 0. Matches C2's "gate selftest PASS 39/39".

## Tool installs

None. strace and python3 pre-installed; no pacman/uv/npx installs performed (per seat spec, pacman paused; nothing needed).

## Risks / blockers

- Real `/boot/limine.conf` not read (root-only, unprivileged seat) — live leg is probe + scratch conf only, as specified.
- "Absent limine on PATH" CLI variant not run end-to-end (host has real `/usr/bin/limine`, so an empty-PATH run can't be staged without hiding the real binary); the absent case is covered by the selftest `probe-version` family (direct-path absent → None) and the three refusal runs above.

## Verdict

C2 (operability: `--limine-version` defaults to `auto`; flag-free run probes, records `limine_version`+`source:probe`, selects era from it, refuses rc 64 / empty stdout on probe failure; selftest 39/39) — **SUPPORTED** by legs 1–4 receipts. C1's AUTO-PROBE-SHAPES probe half (no-version / `12.9.6-rc1` suffixed / stderr-only all read None) — **SUPPORTED**; ten-digit REFUSAL-VERSIONS and battery-family claims were not in this seat's scope and are neither claimed nor falsified here.
