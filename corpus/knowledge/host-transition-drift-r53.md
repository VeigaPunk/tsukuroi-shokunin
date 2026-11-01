source: own-work host captures `.ufo/waves/round-53/after/` (`win-census-live.txt`, `native-path-view.txt`, `win-census-selftest.txt`) and the round-start probe transcript summarized in LOG.md "Round 53 — declaration"; naming-class fact from S259
verified-at: 2026-10-31 (host: Windows 10.0.26200 x64, Git Bash bash 5.3.15; probes run 2026-10-31, read-only)
recheck: 30d or on any host change — re-run `python tools/win-host-census-r53.py` and the D1-D6 probe loop `for t in pacman systemctl journalctl btrfs nvidia-smi jq; do command -v $t; done`; a changed row gets an appended correction, never an in-place edit

# Host-transition drift register (round 53)

The lane's rounds 1-52 instrumented an Arch Linux host. Round 53 runs on a different host (Windows
10.0.26200 x64, Git Bash / MSYS session). This register flags every Linux-only surface the operative
census, SKILL checklist and PROVINCE declare, with the probe that measured it on the current host, the
observed result and the drift class. Stale items are flagged, not silently dropped; the PROVINCE
correction is recorded below. Detection only — no uninstall, install, alias change or PATH edit was
executed; every repair stays operator-owned (`windows-host-plane-r53.md` RP1-RP3).

| id | declared surface (where) | probe (read-only, 2026-10-31) | observed on this host | class | recheck |
|---|---|---|---|---|---|
| D1 | pacman package plane (SKILL packages arm; census `probe_packages_arm`; PROVINCE Core) | `command -v pacman` | ABSENT | stale-here (valid for its Linux host class) | 30d / on host change |
| D2 | systemd user units + timers plane (SKILL systemd arm; PROVINCE Core) | `command -v systemctl` | ABSENT | stale-here | 30d / on host change |
| D3 | journal/boot plane (`journalctl -b`, coredumpctl; SKILL journal arm; PROVINCE Core) | `command -v journalctl` | ABSENT | stale-here | 30d / on host change |
| D4 | storage integrity plane (`btrfs device stats`, scrub record, error_stats; PROVINCE Core r38/r44) | `command -v btrfs` | ABSENT | stale-here | 30d / on host change |
| D5 | driver/firmware plane (`nvidia-smi`, dkms, kernel modules; PROVINCE Core) | `command -v nvidia-smi` | ABSENT | stale-here | 30d / on host change |
| D6 | census dependency `jq` (used by journal/census capture pipelines) | `command -v jq` | ABSENT | stale-here (census tool dependency) | 30d / on host change |
| D7 | old census selftest completion (round-50 receipt: 168/168 PASS on the Linux host) | `bash tools/tsukuroi-census.sh --selftest` under 90 s, then 420 s | rc 124 both budgets; 40 PASS / 0 FAIL / no summary line (40 of 168 cases reached) — the historical PASS does not reproduce here | stale-here (instrument non-runnable, not falsified) | 30d / on host change |
| D8 | interpreter naming in every registry/corpus counting command (`python3 tools/...`) | `python3 --version` vs `python --version` | `python3` prints `Python was not found...` and exits 49 (Store App-execution-alias stub; S259 gives python3.exe as a real installed name elsewhere); `python` is Python 3.13.15 | broken-here (counting commands must spell `python` on this host) | 30d / on host change |
| D9 | PATH health (implicit premise of every bare-tool probe) | census `PLANE path` | 51 entries, 3 entries with absent directories, 5 values appearing twice, per-session `fnm_multishells` entry (native view; `native-path-view.txt`) | degraded-here | 30d / on host change |
| D10 | PROVINCE declared surfaces resolving here (Core table: pacman/systemd/journal/driver/btrfs) | read PROVINCE.md; cross-check D1-D5 | 0 of the Core probe commands resolve on this host; PROVINCE corrected 2026-10-31 with the dated host-transition record (see below) | corrected-this-round | on host change |
| D11 | git index plumbing on NTFS (campaign binding: index-free commits via `campaign/treecommit.py`; `git status`/`add -A`/`stash` banned by the round contract) | helper docstring + contract §0 (fleet repo `.ufo/prompts/tsukuroi-round-53.md`) | binding confirmed this round: all lane commits routed through treecommit.py plumbing | documented-here (operator rule, not repairable by the lane) | on contract change |
| D12 | node shim stability (a required tool's resolution path) | `command -v node` (2026-10-31) | resolves into `.../fnm_multishells/16640_1793492086173/node` — the directory name carries a per-session identifier, so the path is session-bound [inference: a second session resolves a different `fnm_multishells` dir; not probed from a second session this round] | fragile-here | 30d / on host change |

## PROVINCE correction (protocol work, §absent-surface rule)

PROVINCE.md gained the dated section "Round-53 host transition" this round: the Core surfaces remain
declared for the Linux host class they were minted on; on the current Windows host they read
ABSENT/BLOCKED (D1-D7); the Windows tool/PATH/interpreter/git state is the new documented surface,
served by `tools/win-host-census-r53.py`; the correction is logged in LOG.md. No Core surface was
re-homed and no sibling scope absorbed.

## Limits

The register records presence/absence and completion facts of 2026-10-31; it does not claim the Linux
knowledge is wrong — the entries stay valid for their host class, and their recheck procedures name
Linux tools that simply do not resolve here (that is what D1-D7 flag). D7's budget numbers are
wall-clock facts of this session's load. D12's second-session behavior is labeled inference, not a
probe; a later round that opens a second session can measure it and append the correction.
