# ExecIsolationProbe — launcher channel probe (round 92 C1 operability)

Method: (1) `--isolation-check` run through the frozen r92 battery verbatim.
(2) Own probe gate `probe.py` (seat dir, lane untouched) run **through the frozen
battery's own `sandbox_argv`/`copy_gate`** via `runner.py` (`importlib` load of the
battery, `sandbox_argv(gpath, case, [sys.executable,"-I",gpath])`, cwd=case dir —
i.e. the identical launcher path as `run_battery`, without `run_battery`. (3) Same
probe `python3 -I probe.py` **without** sandbox, cwd=a case-like dir. Receipts in
`.ufo/waves/round-92/w1/ExecIsolationProbe/`: `isolation-check.json`,
`probe-inside.txt`, `probe-outside.txt`.

## 1. Frozen `--isolation-check` (verbatim, `isolation-check.json`)

```json
{"cwd": "/fast/scratch/hyaku/tsukuroi-r92/ExecIsolationProbe/isolation-check/limine-iso-s5nyri4m/case", "root": ["bin", "dev", "etc", "fast", "lib", "lib64", "proc", "sbin", "tmp", "usr"], "cwd_entries": [], "sibling_files": ["gate.py"], "lane_visible": false, "battery_visible": false, "env": {"PATH": "/usr/bin", "HOME": "/tmp", "LC_ALL": "C", "TMPDIR": "/tmp", "PWD": "/fast/scratch/hyaku/tsukuroi-r92/ExecIsolationProbe/isolation-check/limine-iso-s5nyri4m/case"}, "pids": ["1", "2"], "sys_path": ["/usr/lib/python314.zip", "/usr/lib/python3.14", "/usr/lib/python3.14/lib-dynload", "/usr/lib/python3.14/site-packages"]}
```
exit 0. Matches the frozen contract exactly (byte-verified instrument sha256
`fde864ea…` = r92 battery, `sandbox_argv` = the `--unshare-all --die-with-parent
--new-session --clearenv` allowlist; `python3 -I` ⇒ no script dir on `sys.path`).

## 2. Channel table — inside the launcher vs outside

| # | Channel (probe attempt) | Inside launcher | Outside (plain `python3 -I`) | Closed / uncertified |
|---|---|---|---|---|
| a | Vol 1: `os.listdir(dirname(__file__))` | `["gate.py"]` only | 5 entries (seat dir leftovers) | **Closed** |
| b | Import `limine_pin_battery_r92` after `sys.path.insert(0,·)` of own dir / lane `tools/` / `os.getcwd()` | all 3 `ModuleNotFoundError`; `dash_file_exists=False` for all three | own/cwd same (no battery there); `tools/` `dash_file_exists=True` but underscore-name import still fails (battery file name has dashes) | **Closed** for the underscore-name lookup; **uncertified** for the dash-name path (see c) |
| b′ | `spec_from_file_location` of the dash-named battery in own dir / `tools/` / cwd | `dash_file_loadable=True` (the call itself needs no file) but `dash_file_exists=False` ⇒ cannot load anything; no oracle reachable | `tools/` `dash_file_exists=True` (file readable — verified by c) | **Closed**: the loadable-check is vacuous; existence is what matters and is False inside |
| c | `open()` canonical lane battery path; `$PWD/../tools/…`; `~/.cache/…` | all 3 `FileNotFoundError`; `HOME=/tmp` | lane path **opens** (`#!/usr/bin/env p`); the other two still ENOENT (no such fixture layout — K3/K5 style relative/cache channels stay shut by geometry, not by the launcher) | **Closed** (all three) |
| d | `/proc` listing | `["1","2"]` (bwrap + python) | 4,607 PIDs | **Closed** (pid enumeration) |
| d | `/proc/1/cmdline` | **readable**, full bwrap argv incl. `--ro-bind <gate> <gate>` and `<case> <case>` paths + all flags | `systemd`'s cmdline (readable too) | **Not closed — residual argv-contents channel**: inside names the launcher, the private gate-copy path and the case-dir path (random `mkdtemp` names ⇒ case-count/randomness oracle, §4) |
| d | `/proc/self/environ` | 5 vars only | 274 vars (full caller env) | **Closed** (caller env gone); == `os.environ` below |
| e | `os.environ` | `{PATH:/usr/bin, HOME:/tmp, LC_ALL:C, TMPDIR:/tmp, PWD:<case>}` | 274 keys | **Closed** |
| f | Case dir contents | `esp/BOOTX64.EFI`, `limine.conf` only (walk-verified) | same | **Closed** (fixture is the only thing there) |
| g | `/tmp` leftovers from a previous case | `[]` (fresh `--tmpfs`) | 12,551 entries | **Closed** |
| s | `sys.path` | 4 stdlib-only entries; no script dir, no `PYTHONPATH` | identical (both `-I`) | **Closed** (matches `-I` contract) |
| s | `uname().nodename` | `plazir27` | `plazir27` | **Open by design** (host identity shared; the launcher does not unshare UTS) |
| s | `/usr`+`/etc` visible | full read access (incl. all site-packages, `arch-release`, `/etc` config) | same | **Open by design** (the `--ro-bind` allowlist); oracle is not there ⇒ no path to judge answers, but host software versions are observable (fingerprint channel) |
| s | `/dev` | `core fd full null ptmx pts random shm stderr stdin stdout tty urandom zero` | host `/dev` | **Fresh by replacement; minimal** (`--dev`): no leftovers; `/dev/null` write works — **write channel to `/dev` destinations open by design** |
| s | Network (`connect_ex` to 127.0.0.1:22 / 8.8.8.8:53 / 192.168.1.1:80) | 111 (refused) / 101 (unreachable) / 101 — **`--unshare-all` gives a private net ns with no route** | would connect locally | **Closed** (no external reach; local connect refused — no listening services in ns) |
| s | Writability: case dir / gate file | case-dir write → `EROFS`; gate file is `--ro-bind` | writable | **Case dir: closed (ro). Gate file: ro-bind. Gate *directory*: see below** |
| s | Writability: gate-copy *directory* (not the file) | **WRITE SUCCEEDS** (`WAS_WRITTEN` created, visible in-ns, gone after) — `sandbox_argv` mounts only `gate` as a file bind, not its parent dir, and `copy_gate`'s `mkdtemp` parent dirs are still writable on the host mount ns because the sandbox only overlays the 5 bind targets | writable | **UNCERTIFIED** (see §4): transient (dir is deleted by `isolation_check`/`run_battery` after exit), and not a read channel to the oracle — but it is a write channel the claim sentence does not describe |
| s | Own `argv` (`/proc/self/cmdline`) | `/usr/bin/python3␀-I␀<gate-copy path>` — reveals the **full random case/gate path to self** | `python3␀-I␀../probe.py` (relative) | **Residual** (same as /proc/1/cmdline: random-name oracle, timing-able) |

## 3. Fresh `/tmp` check

Inside probe: `g_tmp_entries = []`. Outside: 12,551 entries. The fresh-tmpfs half of
the claim holds; a second case in the same seat cannot inherit files from a first
through `/tmp`. (`HOME=/tmp` additionally makes `~/.cache` land on the same fresh
tmpfs.)

## 4. Channels the launcher does NOT close, and whether C1's wording covers them

The C1 predicate (round-92.md, battery docstring ISOLATION paragraph, receipt headers)
is a **read-path** contract: private gate copy, the bwrap allowlist, ro case+gate
mounts, cwd=case, cleared env, `-I`; controls read `unmet` (0/89, 0 errors). It says
nothing about: timing, behaviour/answers, argv contents, fixture shape, host
fingerprint, write channels, or transient state. Verdicts per channel:

| Residual channel | What remains open inside | Covered by claim wording? |
|---|---|---|
| **Timing** | Full wall-clock/CPU visibility (`time`, `time_ns`, `/proc/self/stat`); a gate can measure battery latency, retry counts, and answer patterns | **No — explicitly excluded** by the round-92 "Named limits" ("Timing and behavioural channels are not modelled … the sandbox closes read channels, not inference") |
| **Behaviour / answers** | A gate that reimplements the rule (or is recognised by its outputs) still reads `met` — indistinguishable from an honest implementation | **No — named limit** ("cannot tell an independent implementation from one that reimplements the rule text"); claim is about the oracle channel, not authorship |
| **argv contents** | `/proc/1/cmdline` and `/proc/self/cmdline` fully readable: launcher flags, and the **random `mkdtemp` gate/case path names** (PRNG state/order oracle: how many cases ran, ordering, work-dir tree outside the ns is enumerated — `ls /fast/…` succeeds inside because `/fast` is a bind-parent path prefix that also exists on the host mount view? see note) | **No** — outside the predicate |
| **Fixture shape** | Case dir = conf + ESP exactly; family structure (r91 vs r92 roster count, version fields, `--limine-version` values) is fully observable | **No** — fixture is the input, deliberately visible |
| **Host identity / fingerprints** | `uname().nodename` (`plazir27`), full `/usr` + `/etc` (site-packages, `arch-release`, hostname, /etc configs), CPU/memory via `/proc` | **No** — allowlist-by-design; versions are visible but carry no oracle |
| **Gate-dir write** | The gate-copy parent dir is writable inside (file `WAS_WRITTEN`); vanishes with the work dir after exit. Not an oracle read path; a transient write channel | **No** — predicate describes the gate *bytes* mount, not the parent dir; measured, reported, harmless to the claim (controls cannot use it to reach the battery) |
| **`/dev` write** | `/dev/null`, `/dev/full`, `ptmx` usable | **No** — needed for the gate to run (`--dev` fresh set); no data leaves the ns |

Note on path prefixes: `root` in `--isolation-check` lists `fast` at `/`. That is the
bwrap `--ro-bind <case> <case>` of the case path `/fast/scratch/…` — the bind source
path exists on the host, so `/fast` resolves as a prefix dir. Inside, `os.listdir`
of the host `tools/` dir still ENOENTs the battery file (the file itself is not
bound), which the probe verifies. The bind is path-prefix-visible, not content-visible.

## 5. Receipts & traceability

- `isolation-check.json` — frozen instrument, verbatim JSON, exit 0.
- `probe-inside.txt` — own probe via the frozen battery's `sandbox_argv`/`copy_gate`
  (imports the frozen `limine-pin-battery-r92.py` by path; sha256 `fde864ea29f1b61d9e8cdcb1063942e6c9b07bfdf81cec5766e804488542b166` verified before use), `BWRAP_ARGV` logged, full JSON stdout.
- `probe-outside.txt` — same probe with `python3 -I` in a case-like dir, no sandbox.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r92/ExecIsolationProbe/`
  (`probe.py`, `runner.py`, `case-outside/`, `probe-run/`, `isolation-check/`,
  `residual/`, `residual2/`). Lane untouched except this seat's receipt dir.
No tool installs (nothing needed; probe is stdlib-only).

## Verdict

C1 (operability) — **supported as measured**: every read channel the C1 predicate
names is closed inside the launcher (sibling-dir listing, sys.path import from all
three dirs, all three `open()` variants, `/proc` parent-argv **content** i.e. the
battery path is unreachable as a file, `os.environ`→5 vars, case-dir-only contents,
fresh `/tmp`=[]), confirmed by my own per-channel probe through the frozen battery's
`my launcher` path and by the frozen `--isolation-check` receipt. The channels the
launcher does **not** close (timing, behaviour/answers, argv contents incl. random
path names, fixture shape, host fingerprints, transient gate-dir write, `/dev`
write) are **not covered** by C1's wording — and two of them (timing, authorship) are
explicitly named limits in the frozen declaration, so this is **not a falsification**
of the claim; it is a delimitation. C2 is out of this seat's scope.

Risks/blockers: none for the claim. One observation for Main (not a defect): the
gate-copy **parent directory** is writable inside the sandbox (§4, "Gate-dir write"),
which the claim sentence ("gate copy read-only mounted") does not literally cover —
it refers to the file bind. The five controls cannot exploit it (no path to the
oracle), so the `unmet` readings stand.
