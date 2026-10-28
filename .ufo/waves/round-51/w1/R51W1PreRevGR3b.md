VERDICT: defect-found
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

Seat R51W1PreRevGR3b, uncounted pre-read of row GR3 at 2732ee6c06108c031c4d8043239b994e0504eb2f (`corpus/knowledge/btrfs-scrub-grounding-r45.md`, lines 181-226). Not a counted verdict.

## Setup checks (observed)

- Entry extracted with `git show 2732ee6c…:corpus/knowledge/btrfs-scrub-grounding-r45.md` to scratch; 348 lines. Section headers at lines 14, 56, 181, 227, 240, 269.
- `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` printed `section_sha256.GR3 = 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` (also GR1 8eff9637…, GR2 27aa7abb…, both match the FROZEN values); `structural_ok: 1`, `problems: []`. My hash matches; no divergence.
- `lint-grounding-r51.py --revision 2732ee6c…` → `verdict: PASS`, `lint_ok: 3`, `rows_clean: 3`, `gap_ok: 1`, `gaps_computed: 62`, `cite_bad: 0`, `quote_bad: 0`; GR3: `cites: 6`, `quotes: 12`, `problems: []`. (The lint does not check clauses; everything below is from reading the cited bytes.)
- Snapshot digests (`sha256sum`, compared with each directory's `SHA256SUMS`):
  - S248 = `.ufo/waves/round-45/frozen/src/systemd.kill.xml`: 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72 (matches the listed line).
  - S244 = `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service`: eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252 (`sha256sum -c` OK).
  - S237 = `.ufo/waves/round-42/frozen/src/scrub.c`: 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 (`sha256sum -c` OK); it is btrfs-progs v7.1 `cmds/scrub.c` (`corpus/SOURCES.md:246`).
  - S249 = `.ufo/waves/round-45/frozen/hostcap/capture.txt`: f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 (matches). `hostcap/capture.sh` = c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc (matches `SOURCES.md:258`).
- Note: the entry's header line 1 maps S244 to the round-44 directory, S237 to the round-42 directory, and S248 to the round-45 directory, as above.

## Defects

### D1 — the -B no-fork clause cites a line that does not set it (citation support)

Entry (lines 192-193): "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1512`)".

Pinned bytes: `S237 scrub.c:1512` is only the guard `	if (do_background) {`. The `-B` setting is `scrub.c:1292-1293`: `case 'B':` / `do_background = false;` (default `do_background = true;` at `scrub.c:1247`). Line 1512 does not show that `-B` disables the fork.

Replacement for the clause: "With `-B` the start does not fork into the background (btrfs-progs `scrub.c:1293` sets `do_background = false` in `case 'B'`; the fork is guarded at `scrub.c:1512`)".

Admission side effect: `SOURCES.md:246` declares S237 ranges `67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945`, which does not contain 1293. The `### Range gaps (R51)` S237 bullet (entry line 271, currently `421, 439, 1546`) must therefore regenerate to include 1293 (`--emit-gaps`); the entry's own Limits text (lines 261-263) says the lint fails otherwise.

### D2 — the SIGTERM default and the "every remaining process … receives it" clause are not supported by the lines cited for them (citation support)

Entry (lines 184-186): "which this unit sets to SIGINT instead of the SIGTERM default; because the unit sets no `KillMode=`, the default `control-group` applies and every remaining process in the unit's control group receives it."

Pinned bytes:
- The SIGTERM default is not cited anywhere in the row. It is `S248 systemd.kill.xml:112`: "Defaults to <constant>SIGTERM</constant>." Also `:84-85`: "Processes will first be terminated via <constant>SIGTERM</constant> (unless the signal to send is changed via <varname>KillSignal=</varname> …)".
- The cited `:68` says "all remaining processes in the control group of this unit will be killed on unit stop"; it does not say which signal. The signal is named at `:84-85`.

Replacement: "which this unit sets to SIGINT instead of the SIGTERM default (`systemd.kill.xml:112`, `:84-85`); because the unit sets no `KillMode=`, the default `control-group` applies (`systemd.kill.xml:101`) and every remaining process in the unit's control group is killed on stop (`systemd.kill.xml:68`) with that first signal (`:84-85`), so every remaining process receives it."

All of those lines are inside the S248 declared range (registry lines 62-116); no gap-block change is needed for D2.

### D3 — "in this order" omits the optional SIGHUP the pinned man page defines (omission)

Entry (lines 183-186): "signals the running `btrfs scrub start -B` in this order under systemd v262. First the unit's `KillSignal=` … Right after that signal systemd sends SIGCONT."

Pinned bytes: `S248 systemd.kill.xml:84-87`: "Processes will first be terminated via SIGTERM … Optionally, this is immediately followed by a SIGHUP (if enabled with SendSIGHUP=)." The row's sequence is therefore not universal: a SIGHUP is sent when `SendSIGHUP=` is enabled.

Host: `btrfs-scrub@.service:6-10` (S244) sets no `SendSIGHUP` (`grep -c SendSIGHUP` → 0). `capture.txt` (S249) does not query `SendSIGHUP` at all (`grep` finds only line 3 for `KillSignal`); its unit-level drop-in directories are empty (`capture.txt:7`, `unit_dropins ` with no value), but that check does not cover `/usr/lib/systemd/system/*.d` or `/run`.

Replacement, inserted after "Right after that signal systemd sends SIGCONT.": "A SIGHUP follows only if `SendSIGHUP=` is enabled (`systemd.kill.xml:84-87`); the packaged unit does not set it (`btrfs-scrub@.service:6-10`) and `capture.txt` does not query it, so on this host the sequence without SIGHUP is [inference: no SendSIGHUP was read from a drop-in outside the directories capture.txt:7 lists]."

Lint note: `:84-87` is inside the S248 declared range; no gap change.

### D4 — "so SIGINT reaches that handler" holds only from scrub.c:1546; the row states it for the whole run (universal over timing)

Entry (lines 193-194): "installs its SIGINT handler on the mount's descriptor (`scrub.c:1546`, `:439`), so SIGINT reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)."

Pinned bytes:
- Inside `scrub_start` (`scrub.c:1233` to `:1758`) the only SIGINT disposition change on the no-fork path is `scrub_handle_sigint_child(fdmnt)` at `scrub.c:1546`. Every `sigaction` call in the file is in the helper bodies at `:428`, `:433`, `:438`, `:443`; `:1522` (`scrub_handle_sigint_parent`) runs only on the fork path that `-B` skips (see D1).
- Between `:1343` (`fdmnt = btrfs_open_mnt(path)`) and `:1545`, `scrub.c` installs no SIGINT handler (device-limit reads and writes at `:1413-1414`, `:1449`). A SIGINT in that window reaches whatever disposition the process inherited; that disposition is not pinned by any row source [inference].
- `scrub.c:1710` calls `scrub_handle_sigint_child(-1)`, which sets `SIG_DFL` (`scrub.c:439`, `fd == -1 ? SIG_DFL : …`) before `out:`; the handler window is therefore `:1546` through `:1710`.

Replacement for the clause: "…and, from `scrub.c:1546` until `scrub.c:1710` resets it, installs its SIGINT handler on the mount's descriptor (`scrub.c:439` selects it for `fd != -1`), so SIGINT in that window reaches that handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9, `scrub.c:421`). A SIGINT that arrives before `scrub.c:1546` meets no handler installed by `scrub.c`; the disposition it then has is inherited from systemd and not pinned here [inference]."

Admission side effect: `scrub.c:1710` is outside S237's declared ranges (`SOURCES.md:246`), so it joins the S237 gap bullet with 1293 (expected bullet: `- S237 scrub.c: 421, 439, 1293, 1546, 1710`; regenerate with `--emit-gaps` and check the output rather than trusting this line).

## Checked and supported (read against pinned bytes)

- `S244 btrfs-scrub@.service:9` "KillSignal=SIGINT" (exact line) and `:10` "ExecStart=/usr/bin/btrfs scrub start -B %f" (exact). The unit has no `KillMode=` and no `TimeoutStopSec=` (full file read, 10 lines).
- `S248 systemd.kill.xml:68` (control-group kills all remaining processes on stop; the quote is the whole line, truncated at its end as the entry quotes it).
- `S248 :91` (TimeoutStopSec delay has passed) and `:96-97` (termination request repeated with SIGKILL or FinalKillSignal=, unless disabled via SendSIGKILL=). "unless SendSIGKILL=no" is a paraphrase of "disabled via the SendSIGKILL= option" (the value `no` is not in the line; wording only, not a defect).
- `S248 :101` "Defaults to control-group." (KillMode default) and `:108` (KillSignal controls the first signal).
- `S248 :114-115` "right after sending the signal specified in this setting, systemd will always send SIGCONT" (the entry's "Right after that signal systemd sends SIGCONT" is supported).
- `S237 scrub.c:421` (`ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);` inside `scrub_sigint_record_progress`, `:417-424`), `:439` (handler selection), `:1546` (`scrub_handle_sigint_child(fdmnt);`). The quotes are exact lines.
- `S237 scrub.c:1512` as the fork guard (`if (do_background) {`).
- Host: `capture.txt:2` (kernel line carries `systemd 262 (262-1-arch)`); `:3` (`KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9`, `FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service`, queried for `btrfs-scrub@-.service` by `capture.sh`); `:4` (`10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`); `:5` (`dropin_owner … 10-faster-shutdown.conf none`). `capture.sh` header: read-only, "no start, stop or enable"; "No unit was started or stopped" is supported.
- `[inference]` marks: the "every system unit" sentence (line 190) and the canceled-record sentence (lines 195-196) are marked and are undecided by the pinned bytes. Optional strengthening (not a defect): `scrub.c:412-415` states the intent "makes the master process record the current progress status before exiting"; citing it next to the marked inference would show the reader what the code says and what it does not establish.
- Universal words: "every" (line 186) is supported by `:68`/`:84-85`; "first" (line 184) by `:84`; "always" appears only in the pinned text (`:114`). No other universal in the row goes unsupported beyond D2-D4.

## Not checked

- The SIGINT = 2 and SIGKILL = 9 numeric mapping (`KillSignal=2`, `FinalKillSignal=9` at `capture.txt:3`) is standard Linux signal numbering; no pinned row source states it. Not a defect here; a reader may want it cited to signal(7).
- `systemd-system.conf(5)` was not pinned (the row marks this).
- Only the GR3 row and the Range gaps and Limits sections of the entry were read; `How this changes OS triage` (lines 227-238) was not read, per the item's scope.
- Nothing was run on the host beyond the read-only capture already in S249; no unit was started or stopped.

## Tooling

No tools were installed or upgraded. Commands run: `git show`, `sha256sum`, `sha256sum -c` on S244 and S237 snapshot directories, `grep`/`awk`/`sed` reads, `check-scrub-admission-r51.py --section-hash --no-base-check`, `lint-grounding-r51.py --revision …`.
