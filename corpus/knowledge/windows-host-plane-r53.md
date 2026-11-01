source: S258 S259 (rows in `corpus/SOURCES.md`, both opened 2026-10-31) plus the dated host captures under `.ufo/waves/round-53/after/` of this repo (`win-census-live.txt`, `native-path-view.txt`, `win-census-selftest.txt`)
verified-at: 2026-10-31 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; git 2.55.0.windows.3, gh 2.101.0, node v24.21.0, Python 3.13.15; census capture 2026-10-31)
recheck: 30d — re-run `python tools/win-host-census-r53.py --selftest` (expect PASS, 20 cases) and the live run; compare the four plane verdicts with `.ufo/waves/round-53/after/win-census-live.txt`; re-open S258/S259 on upstream content change

# The Windows host tool-state plane (round 53)

Scope: the current host (Windows 10.0.26200 x64, Git Bash session) — tool presence, PATH health,
interpreter identity and git plumbing state. This is a new surface for the lane: rounds 1-52
instrumented an Arch Linux host whose probes (pacman, systemd, journalctl, btrfs, nvidia-smi) do not
exist here (measured absent, `corpus/knowledge/host-transition-drift-r53.md` D1-D7). The executable
instrument is `tools/win-host-census-r53.py` (registry row `win-host-census-r53`); the table below is
its decision content. Detection and report only — every repair named here is operator-owned and none
was executed.

| id | question | probe (read-only) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| W1 | Which interpreter name runs Python here? | `command -v python python3`; census `PLANE python` | `python` resolves outside `WindowsApps` and runs (`runs=yes`) | `python3` resolving into a `...\Microsoft\WindowsApps\` directory is the Store App-execution-alias stub: running it prints `Python was not found...` and exits 49 (measured 2026-10-31). The upstream docs give `python3.exe` as a real installed name (S259), so the name itself is not the defect — the resolving directory is | Invoke lane tools with `python`, never `python3`, on this host; disable the alias or install a real interpreter — operator | S259 + `.ufo/waves/round-53/after/win-census-live.txt` |
| W2 | Where does a bare tool name resolve? | `where.exe <name>` (or `command -v` in bash); census `PLANE tools` | one unambiguous hit outside `WindowsApps` | `where` searches the current directory and the PATH directories and appends PATHEXT extensions to an extension-less pattern (S258), so a name-only hit can be the Store stub class or a same-name binary from an earlier entry; a resolving path inside a `WindowsApps` directory classifies `stub` without executing it | Treat the resolved path, not the hit count, as the evidence; classify by directory; repair (alias hygiene) operator | S258 |
| W3 | Is PATH healthy? | census `PLANE path` (`classify_path_entries` over `os.environ["PATH"]`); `python -` counting one-liner | `missing=0 dup_values=0 empty=0` | Measured 2026-10-31 (native view): 51 entries, 3 entries whose directory does not exist, 5 values appearing exactly twice (a later duplicate silently shadows the earlier one), and a per-session `fnm_multishells` entry that dies with its session — scripts depending on it fail in every other session | Prune dead entries, dedupe the doubled values, replace the per-session fnm dir with a stable node path — operator (`native-path-view.txt` holds the per-entry census) | capture `.ufo/waves/round-53/after/native-path-view.txt` |
| W4 | Is the lane commit identity configured? | `git config user.name` / `git config user.email` in the lane repo | `tsukuroi-shokunin` / `tsukuroi@shokunin.local` (measured 2026-10-31) | An unset identity makes lane commits carry the operator identity — a conformance defect per PROTOCOL.md §Lane authorship | `git config user.name/email` once in the repo — measured set here; nothing owed | census `PLANE git` `identity=set` |
| W5 | Do the historical census and its selftest run on this host? | `bash tools/tsukuroi-census.sh --selftest` under a time budget | (original host) 168/168 PASS | Non-runnable here: 40 of 168 cases in 90 s (rc 124, timeout) and still 40 PASS / 0 FAIL / no summary line at 420 s (rc 124) — per-case process spawn cost under MSYS makes the fixture harness exceed any reasonable budget. A partial PASS list is not a passing selftest | Do not cite the 168-case PASS on this host; use `tools/win-host-census-r53.py` for host state; porting the old selftest is a separate claim | captures `scratch` outputs summarized in `.ufo/waves/round-53/after/win-census-live.txt` companion note in `host-transition-drift-r53.md` D7 |
| W6 | Which required host tools exist? | census `PLANE tools` | `required=5/5`, Linux-only tools absent-by-class | Any required tool (git, gh, node, python, bash) absent degrades; git absent blocks. The six Linux-only tools (pacman, systemctl, journalctl, btrfs, nvidia-smi, jq) are absent on this host by host class — counted `linux_absent=6`, never a degradation | Install only on an operator decision; absence is the expected state, not drift | `.ufo/waves/round-53/after/win-census-live.txt` |
| W7 | Is git plumbing safe on this host? | version probe + the campaign binding | git 2.55.0.windows.3, gh 2.101.0 (measured) | The git index is unreliable on this host (NTFS-uncheckoutable paths in fleet trees): the round contract bans `git status`, `add -A`, `checkout .`, `stash`, `read-tree` and routes every lane commit through the plumbing helper `campaign/treecommit.py` (index-free: hash-object/ls-tree/mktree/commit-tree/update-ref) | Keep using the plumbing helper for lane commits; no repair to run | `.ufo/prompts/tsukuroi-round-53.md` §0 (fleet repo) + `campaign/treecommit.py` docstring |

## Repair plans (operator-gated; none executed this round)

- RP1 (python3 stub): remove or disable the `python3` App execution alias (Settings > Apps > Advanced
  app settings) or install a CPython `python3.exe` shim ahead of it in PATH. Verify with
  `python3 --version` exiting 0 and `python tools/win-host-census-r53.py` python plane GREEN.
- RP2 (PATH hygiene): delete the 3 entries whose directories are absent, dedupe the 5 doubled values,
  and stop persisting the per-session `fnm_multishells` directory (use fnm's shell hook instead).
  Verify with `PLANE path GREEN` (`missing=0 dup_values=0 empty=0`).
- RP3 (old selftest port, optional): the 168-case fixture harness needs a batched-process runner or a
  native port before its PASS can mean anything on this host; until then the old census remains a
  Linux-host instrument.

## Limits

Host-state rows (W1, W3, W4, W6) are captures of 2026-10-31 and drift with the host; W5's budget
numbers are wall-clock facts of this session's machine load, not constants. S258 describes the
Windows Server 2025-era `where` documentation (updated 2025-09-22 per its frontmatter) — client
Windows behavior is treated as the same class until a client-specific contradiction is opened. The
gate's selftest injects resolvers and proves logic only; the live leg is the host reading (both are
required before any C1 verdict).
