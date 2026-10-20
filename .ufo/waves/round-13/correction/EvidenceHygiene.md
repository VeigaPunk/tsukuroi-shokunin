# Round 13 correction: EvidenceHygiene (UFO-FSD sentinel, leaf)

Scope: I reviewed round-12 evidence and registry patterns, plus the round-13 artifacts present at 2026-10-20 ~01:45 -03. The goal was to find secret and raw-journal risks before round-13 files land.
Evidence status: author-side. This file grants no admission authority.

The round-13 matrix correction concerns unit read-only views. It does not need journal bodies, process arguments or credential properties. Every risk below is an evidence-collection hazard; none is a correctness claim about the correction.

What I did: read-only `grep`/`jq`/`git show` counts over `.ufo/waves/round-12/**`, `.ufo/waves/round-13/correction/*`, `corpus/` and `SKILL.md`. I fetched two upstream systemd source files (`main`, unpinned). I did not read any credential path, journal, unit file or `/tmp` file contents. Hostnames and IDs are not repeated here.
Writes: this file only. Installs or updates: **none**.

## Axes
I scored two axes: hygiene (no new secret, argv, raw-journal or host-unique ID bytes in permanent history) and evidence power (the correction keeps the measured anchors it needs). The checks below do not cost the correction any evidence.

## Baseline facts (observed)
- **Wave directories are committed wholesale.** `.gitignore` lists only `.ufo/interactive-sessions/`, and `git ls-files .ufo/waves/round-12 | wc -l` returns `88`. Every round-13 seat file and orchestration JSON will become permanent history. History rewrites are destructive and forbidden, so cleanup must happen **before the first commit**.
- **Round 12 cleaned seat files before committing.** For each of `70fede2 670126f f3868cd 9574a18`, I counted added lines in `git show --format= <c> -- .ufo/waves/round-12`:
  - lines matching the journal prefix `[A-Za-z0-9_.-]+\[[0-9]{2,}\]: ` → `0`;
  - lines matching the hostname followed by `[` → `0`.
  - In HEAD, the only standalone 32-hex value is in `resumed/SimplifyR.md` (a census md5, not an ID).
- **The integrator marked what it removed.** Sanitized labels appear at `Issue6629.md:72`, `RootLive.md:80`, `MatrixCritic.md:27`, `resumed/Issue6629R.md:102`, `resumed/RootLiveR.md:129` and `resumed/OverlapHostR.md:47`. `resumed/SecurityR.md` §4 holds the reusable sweep pattern list.
- **Existing exposure is metadata, not secrets.** Round-12 files carry PIDs 1386/1520, an 8-character boot prefix, `uid=1000(<user>)`, the hostname, and a `subvolid=256,subvol=/@` root mount. The census stdout in `resumed/live-after.json` keeps its `host=` header. Older corpus entries contain full boot IDs and raw `name[PID]:` journal lines: `git grep` counts are aur-risk-plane 3, oom-event-plane 3, systemd-user-plane 4, degraded-triage-r4 1, kill-event-deep-r8 1. These are historical and should not be copied forward.

## Findings
| ID | Sev | Exploit / failure path | Evidence | Impact | Smallest remediation |
|---|---|---|---|---|---|
| H1 | Medium | The round-13 D2 recipe `journalctl -u … -o json \| jq 'select(.MESSAGE…)' → [._BOOT_ID, ._SYSTEMD_INVOCATION_ID, ._PID, …]` emits **full** 32-hex boot and invocation IDs. If anyone runs it and pastes the result into a wave file, those IDs become permanent history. | `correction/NoOralReview.md:42`; compare round-12's integrator removing "boot id and process identity" (`resumed/Issue6629R.md:102`) and the `boot8` prefix used in `resumed/MatrixCriticR.md:25-26`. | Host-unique identifiers committed permanently. They are not needed for the correction. | Keep message bodies in-process only. Persist counts plus 8-character prefixes. Use `--output-fields=` with a fixed allowlist. Never write `-o cat\|verbose\|json\|json-pretty` output to a file or `/tmp`. |
| H2 | Low-Med | A full `InvocationID=<32hex>` is already written in an uncommitted round-13 seat file. A wholesale commit would make it permanent. | `correction/NoOralReview.md:26`: my 32-hex count is 1. The other PID tokens there (`1386`/`1520`) are already in committed round-12 files. | Same as H1. | Before committing, the integrator truncates it to 8 characters or drops it (the C1 correction does not use it), and labels the cleanup the way round 12 did. Seat files are read-only to me. |
| H3 | Medium | `systemctl show -p ExecStartEx -p ExecStartPreEx -p ExecStartPostEx <unit>` prints `{ path=… ; argv[]=… ; flags=… }`. Run against a different `<unit>`, it dumps full arguments, which may include tokens. Unfiltered `systemctl show <unit>` also prints `Environment=`. `systemctl cat` prints the `ExecStart`/`Environment` lines. | Upstream `src/systemctl/systemctl-show.c:1564` (format string) and `:2315-2316` (`map_exec`), fetched from `main` and not pinned to 261.2. Round-13 recipe D1 at `NoOralReview.md:36` has no filter. Round 12 kept "only `flags=`… Argv not recorded" (`resumed/MatrixCriticR.md:17`). | Arguments and environment exposure in a reusable recipe. | Filter in-process before saving anything: `systemctl show -p ExecStartEx --value <unit> \| grep -o 'flags=[^;]*'`. Use only `-p` allowlists. Allow `systemctl cat` only when piped through a key-only `grep` (the `AclSemantics.md:70` / `MountErrors.md:141` shape). |
| H4 | Medium | A "complete namespace property set" could be extended with credential properties. systemd's D-Bus interface exposes `SetCredential` and `SetCredentialEncrypted` as `a(say)` **including the data bytes**, `LoadCredential` paths, and `StandardInputData` bytes. | Upstream `src/core/dbus-execute.c:1312-1314`, `:656`, `:436` (`main`). [inference] Whether `systemctl show -p SetCredential` renders those bytes was not tested and must not be tested. | Credential content read, which violates AGENTS.md ("shape-only"). | Use an explicit path-view allowlist only (ProtectSystem, ReadOnly/ReadWrite/BindReadOnly/Inaccessible paths, TemporaryFileSystem, RootDirectory/Image, Private*). Never use `--all`, credential `-p` names, or `busctl get-property` on these properties. |
| H5 | Low | `systemctl status` appends journal-tail **message bodies**. A committed round-12 excerpt still has this shape (a `Logged:` fragment that includes the snapper invocation). | `resumed/RootLiveR.md:63`. Everything else round 12 flagged was sanitized before commit (see baseline). | Raw-body leak path. | Use `systemctl show -p ActiveState -p SubState -p Result` or `is-active`; never use `status` output as evidence. Do not quote `RootLiveR.md:63` forward. Its history stays as-is. |
| H6 | Low | Kernel command-line records can carry `cryptdevice=`/`rd.luks.*`/`resume=` identifiers. | Round 12 kept only the `rootflags=` token (`resumed/MatrixCriticR.md:28`), which is the correct pattern. | Disk/LUKS identifier exposure. | Round 13 does not need the command line. If it is ever used, extract a single token in-process. |
| H7 | Medium (pending tool) | `tools/check-root-dac-correction.py --revision REV` was planned (CorrectionCheck seat; the file was absent at scan time). A `REV` beginning with `-` is parsed by git as an option. Inherited `GIT_DIR`/`GIT_WORK_TREE` can also redirect which repository is read. | `spec.json` item CorrectionCheck; the round-12 memfd reproducer shows that revisions are caller-supplied. | Forged pass/fail against the wrong object, or unintended git side effects. | Validate `REV` against `^[0-9A-Fa-f]{7,40}$\|^HEAD$` and resolve it with `git rev-parse --verify "<rev>^{commit}"`. Then run `git -C <lane-root> cat-file blob <oid>:<fixed path>` with list argv, no shell, and an environment cleared of `GIT_*`. Print only rule IDs, counts and exit code. The selftest uses a trap-cleaned temp directory and writes nothing else. |
| H8 | Info | Live census stdout carries the `host=` header and failed-unit/package names. | `resumed/live-after.json` (`host=` count 1). | Lane norm, not secret. | The C1 correction is prose/JSON. Store only the counter and exit code unless a full census line is itself the claim. |
| H9 | Info | GitHub API evidence. | `correction/IssueBot8047.md` uses unauthenticated curl and records public `user.login/id/author_association`. | None found. | If `gh api` or a token is used, never record headers, `GH_DEBUG` output or the token. Treat comment text as untrusted data and keep quotes to 25 words or fewer. |
| H10 | Info | `/tmp` is shared (1777). Round 12 left `/tmp/r12-census/{census-HEAD.sh,SOURCES-HEAD.md,root_mode_gate.py,…}` at mode 0644; these are copies of repo files, and raw outputs were deleted (`CensusScribe.md:35,118`). Files named `/tmp/*-r13.*` exist; contents not read, and the names suggest man/source fetches. | `ls -la /tmp/r12-census`; `ls -d /tmp/*r13*`. | Low on a single-user host. | Never write raw journal JSON or census output to `/tmp`. Delete scratch files when the round closes. |

## Round-13 scan (counts per file, `.ufo/waves/round-13/correction/*`)
- Patterns counted:
  - standalone 32-hex
  - `name[PID]: ` journal prefix
  - hostname
  - `_PID=|ExecMainPID=N|pid=NNN`
  - `argv[]=|path=/usr/bin`
  - snapper/watcher body strings
  - `authorization:|bearer |token=|password|GH_TOKEN`
- Result: all zero except:
  - `NoOralReview.md`: 32hex=1 (H2) and pid=3 (already public);
  - orchestration JSON credential hits: prose only ("Tooling authorization" ×2, "Passwordless `sudo`" ×64 repeated across prompts).
- No secret, token, environment dump or `/proc/*/environ|cmdline` read was found.
- The in-flight `root-dac-decision-r12.{md,json}` and `QUALITY.md` diffs add no host data. The superseding entry `root-dac-correction-r13.{md,json}` was absent at scan time.

## Rules for round-13 artifacts (what to check before committing)
1. Correction entries cite round-12 host observations by pointer. They do not re-embed PIDs, journal bounds or mount strings that C1 does not need.
2. Any new probe saves only allowlisted `-p` projections, counts, exit codes and ID prefixes. There is no raw `status`, `cat`, journal body, argument list or command line.
3. The integrator reruns the SecurityR §4 patterns over `.ufo/waves/round-13/**` and the new corpus files, and fixes and labels any hit before the first commit.
4. The narrow checker hardens its revision input (H7) and never prints file bytes or host state.

## Limits
- The scans are regex/heuristic, not a full PII or entropy audit.
- Live seats may still write after this scan.
- systemd source is from upstream `main`, not byte-matched to the local 261.2 build.
- H4's rendering behaviour is deliberately untested.
- `/tmp` file contents were not read.
