2026-11-03T22:56:01Z
# N1Sentinel — round 68 boundary sweep (tsukuroi, hyaku run 15, wave w1)

Seat: `N1Sentinel` (sentinel). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (HEAD `3f6edcc9`
at sweep start and at end). Fleet root: `/home/vgpnk/Projects/shokunin` (HEAD `ce99b22a` → `f812ba6b`;
other lanes only, §5). Scratch: `/fast/scratch/hyaku/tsukuroi-r68/N1Sentinel` (deleted on exit; every
command and its verbatim output are pasted below, so no receipt depends on the deleted scratch).

Read-only seat. No remediation performed and none permitted (lane boundary: detection only). No `sudo`, no
pacman transaction, no `systemctl`, no `pkill`, no git/jj mutation, no subagent dispatch, no background job,
no network fetch. No write except this file.

## Measurement window (stated because the wave moved)

The wave's write surface was measured **three** times, and the first quiet test was only a lull — recorded
here so the numbers are not mistaken for a different moment:

- dispatch `22:31:21Z`; `drafts/c1`, `drafts/c2`, `probes/` were empty at sweep start (first artifact
  `22:33:30Z`).
- all 12 seats' primary reports present `22:40:07Z`; 24 files hash-stable across `22:41:04Z → 22:41:44Z`
  (**this lull was not the end**: `c1/count-rw-r68.py`, `c1/E2-report.md`, `probes/c1-battery.txt` were
  rewritten at `22:44Z`, `m1-vs-e2-counter.txt`/`lesson-round-68.md`/`SC2-report.md`/`M1-report.md` at
  `22:46Z`, and two large registry drafts landed at `22:49Z`).
- final state: **quiet for 180 s** (`22:49:5xZ → 22:52:48Z`), measured at `22:52:57Z`:
  27 files (26 + this report), 414,816 bytes total, 391,817 bytes excluding this report.

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T22:52:57Z
$ find <wave>/drafts <wave>/probes -type f | wc -l
27
$ du -sb <wave>/drafts <wave>/probes | awk '{s+=$1} END{print s}'
414816
```

## Verdict

| # | sweep | keys | verdict | defects |
|---|---|---|---|---|
| 3 | credential / boundary grep | `CREDENTIAL_HITS=1` | 1 hit, **fixture marker, not a secret** (§2) | 0 |
| 4 | privilege + pacman sweep | `PRIV_EXECUTED=0` `PRIV_NAMED=3` | all 3 are *named-as-forbidden* (§3) | 0 |
| 5 | bare relative `.ufo/` in drafts | `RELATIVE_OFIUFO=135` (occurrences; 118 lines, 13 files) | named, not failures; **9** are cwd-dependent command operands (§4) | 0 |
| 6 | after-wave state diff | `NEW_FLEET_PATHS=0` `NEW_LANE_PATHS=2` (13 post-landing, L1-owned) | 1 tracked lane file modified by the **L1**, not a seat (§5, §5b) | 0 |

Named for the L1, not scored as defects: OBS-1 (tracked erratum write, declaration-vs-landing mismatch),
OBS-2 (landing-order hazard: the C1 note cites S286/S287 that the registry does not define), OBS-3 (step-5
pipeline is vacuous as written), OBS-4 (the draft gate's write surface is its own selftest sandbox, inherited
from the base tool). §6 also records the two hash cross-checks that hold.

## 1. Start state (lane and fleet), line counts

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T22:31:33Z
$ git -C <lane> status --porcelain > $S/lane-start.txt ; wc -l < $S/lane-start.txt
7
$ git -C <fleet> status --porcelain > $S/fleet-start.txt ; wc -l < $S/fleet-start.txt
4
```

lane-start.txt (7 lines):

```
?? .ufo/waves/round-66/w1.ready.dispatched
?? .ufo/waves/round-67/w1.ready.dispatched
?? .ufo/waves/round-68/w1-dispatch.json
?? .ufo/waves/round-68/w1-run.stderr
?? .ufo/waves/round-68/w1.ready
?? .ufo/waves/round-68/w1.ready.dispatched
?? .ufo/waves/round-68/w1/
```

fleet-start.txt (4 lines, all operator `.scratch/`, the item's carve-outs):

```
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
?? .scratch/run13-state.json
?? .scratch/run15-kernel.py
```

## 2. Credential and boundary grep (item step 3) — `CREDENTIAL_HITS=1`

```
$ grep -rnE --exclude=N1-boundary.md 'op://|BEGIN (RSA|OPENSSH|PGP) PRIVATE|ghp_[A-Za-z0-9]{20,}|password\s*=' \
      <wave>/drafts <wave>/probes 2>/dev/null
<wave>/drafts/c2/R2-attack.md:67:   Probe: a fake token `ghp_EXAMPLEFIXTURE000000000000000000` on the source line of p13.
rc=0   (1 line; expected 0)
```

Classification: **seeded fixture marker, not key material.**

1. The line says `a fake token`; the body is the literal string `EXAMPLEFIXTURE` + zeros, not random base62.
2. Shape disagrees with a real GitHub PAT (`ghp_` + 36 characters = 40 total); this body is 32:

```
$ grep -o 'ghp_[A-Za-z0-9]*' <wave>/drafts/c2/R2-attack.md | awk '{print length($0)-4" chars after ghp_"}'
32 chars after ghp_
7 chars after ghp_          # second match is the inline `ghp_EXAMPLE` of the verification command
```

3. Its purpose is the opposite of a leak: attack (f) of R2 proves the gate does **not** echo note text into
   its JSON — it plants a token-shaped string on a fixture note's `source:` line and greps the output
   (`$ grep -c 'ghp_EXAMPLE' fxA.json → 0`, `R2-attack.md:68`). The string exists in prose only; `ghp_`
   occurs on 1 line of the 26 measured files.

The `CREDENTIAL_HITS=1` figure excludes this report; this report quotes the same fixture string once in its
own classification, so a post-report replay prints **2**, both the same deliberately-fake string. No other
credential shape appears: zero `op://`, zero private-key blocks, zero `password=`. **Impact: none.**
Residual (named): a mechanical secret scanner will flag that line, so do not paste `R2-attack.md` verbatim
into a scanned surface.

## 3. Privilege and pacman sweep (item step 4) — `PRIV_EXECUTED=0` `PRIV_NAMED=3`

```
$ grep -rnE --exclude=N1-boundary.md '\bsudo\b|pkexec|pacman -S[^Q]|pacman -Sy|pacman -Syu|systemctl (start|stop|restart|enable|disable)|pkill -f' \
      <wave>/drafts <wave>/probes 2>/dev/null
drafts/c1/connector-overlap.md:152:  no pacman, no systemctl, no sudo, no network fetch.
drafts/c2/E1-report.md:169:sudo, no service action. Scratch `/fast/scratch/hyaku/tsukuroi-r68/E1Probe` is
drafts/c2/R2-attack.md:84:Commands run (all read-only … ): … `git init`/`commit` in fixture repos under scratch only, … No sudo, no pacman, no service calls, no writes to the lane.
rc=0   (3 lines)
```

| file:line | text | class |
|---|---|---|
| `c1/connector-overlap.md:152` | "No host command beyond read-only `grep`/`sed -n`/`sha256sum`/`ls`/`git show\|cat-file\|log\|diff` was run; no pacman, no systemctl, no sudo, no network fetch." | named-as-forbidden |
| `c2/E1-report.md:169` | "No tool was installed or upgraded (no channel used); no pacman transaction, no sudo, no service action." | named-as-forbidden |
| `c2/R2-attack.md:84` | "… No sudo, no pacman, no service calls, no writes to the lane." | named-as-forbidden |

**PRIV_EXECUTED=0** — no hit is an invocation. Re-running the same regex restricted to shell-prompt lines
over the measured files (this report excluded, because it quotes the pattern):

```
$ grep -rnE --exclude=N1-boundary.md '^[[:space:]]*\$ .*(\bsudo\b|pkexec|pacman -S[^Q]|systemctl (start|stop|restart|enable|disable)|pkill -f)' <wave>/drafts <wave>/probes ; echo rc=$?
rc=1            <- zero matches
$ grep -rnE '^[[:space:]]*\$ .*(\bsudo\b|pkexec|pacman -S[^Q]|systemctl (start|stop|restart|enable|disable)|pkill -f)' <wave>/drafts <wave>/probes
drafts/c2/N1-boundary.md:…:$ grep -rnE '\bsudo\b|pkexec|pacman -S[^Q]|pacman -Sy|pacman -Syu|systemctl (start|stop|restart|enable|disable)|pkill -f' \
rc=0            <- the only prompt-line hit in the tree is this report's own quotation of the pattern
```

The three statements are true of the receipts they sit in: every host command in the wave is a read-only
binary (`grep`, `sed -n`, `awk`, `sha256sum`, `ls`, `stat`, `python3 -B`, `git
cat-file/show/ls-tree/rev-parse/merge-base/status/log/diff`) plus `git clone --shared` reads. No `/tmp`
path is cited anywhere in the wave:

```
$ grep -rn --exclude=N1-boundary.md '/tmp' <wave>/drafts <wave>/probes
rc=1            <- zero matches
```

`git` writes named by the wave are sandbox-scoped and asserted:

```
$ grep -rnE 'git (-C [^ ]+ )?(init|add|commit|checkout|reset|stash|push|pull|rebase|update-ref|switch|restore)' <wave>/drafts <wave>/probes
… 13 hits in 5 files (c2/E1-report.md 2, c2/R2-attack.md 3, c2/S2Scout-gate-rules.md 2,
  c2/S2Scout-host-and-rules.md 1, probes/c2-red-before.txt 3; none in the two large registry drafts)
$ sed -n '1,12p' <wave>/probes/c2-red-before.txt
2026-11-03T22:35:18Z
== sandbox identity guard
$ git -C /fast/scratch/hyaku/tsukuroi-r68/E1Probe/lane rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r68/E1Probe/lane
guard=ok
== fixture commit on throwaway branch r68-red-before
$ git -C /fast/scratch/hyaku/tsukuroi-r68/E1Probe/lane rev-parse HEAD   # sandbox base before fixture
42400ec65c45709ade07a92ed72d1277e3478bbb
$ git -C /fast/scratch/hyaku/tsukuroi-r68/E1Probe/lane checkout -q -b r68-red-before
rc=0
```

Every mutating call carries `-C` on a path under `/fast/scratch/hyaku/tsukuroi-r68/` (a `git clone --shared`
of the lane, or a `git init` fixture), and the toplevel assertion precedes the first mutation in the receipt
that shows a mutation sequence. The lane is never a mutation target: at end of sweep the two claim paths are
absent there (`ls tools/check-knowledge-refs-r68.py`, `ls corpus/knowledge/linux-v73-pinwatch-r68.md` → `No
such file or directory`, rc 2).

## 4. Bare relative `.ufo/` references (item step 5) — `RELATIVE_OFIUFO=135`

The item's pipeline is **vacuous as written**, so its 0 must not be read as "no relative references":

```
$ grep -rnE '(^|[^/a-zA-Z0-9_.-])\.ufo/' <wave>/drafts/c1 <wave>/drafts/c2 2>/dev/null | grep -v '/home/vgpnk' | head -20
rc=0   (0 lines)
```

`grep -rn` prefixes every match with the file's path, every file path contains `/home/vgpnk/…`, so
`grep -v '/home/vgpnk'` drops 100 % of lines by construction. Corrected count (per occurrence, match only):

```
$ grep -rnoE '(^|[^/a-zA-Z0-9_.-])\.ufo/[A-Za-z0-9._/-]*' --exclude=N1-boundary.md <wave>/drafts/c1 <wave>/drafts/c2 2>/dev/null | wc -l
135
$ … | cut -d: -f1,2 | sort -u | wc -l          # lines carrying at least one
118
$ … | cut -d: -f1 | sort -u | wc -l            # files
13
```

Per file: `c2/registry-round68-section.md` 43, `c2/registry-round64-table.md` 43, `c1/lesson-round-68.md`
15, `c1/SC1-report.md` 7, `c1/E2-report.md` 5, `c1/sources-rows.md` 4, `c1/note.md` 4, `c1/SC2-report.md` 4,
`c2/quality-101.md` 3, `c2/E1-report.md` 3, `c1/connector-overlap.md` 2, `c2/R2-attack.md` 1,
`c1/R1-attack.md` 1. Zero in `probes/`.

Most are documentation pointers — including the 86 in the two 71 KB registry drafts, which are provenance
cells (`provenance at .ufo/waves/round-36/l1/…`). Not failures by themselves, per the item. The subset that
matters is the **10 occurrences on `$ `-prefixed command lines**, because there a relative operand resolves at
the process cwd, which for a seat is the FLEET root:

```
$ grep -rnE --exclude=N1-boundary.md '^[[:space:]]*\$ .*(^|[^/a-zA-Z0-9_.-])\.ufo/' <wave>/drafts/c1 <wave>/drafts/c2
drafts/c1/E2-report.md:73:    $ sha256sum .ufo/waves/round-68/drafts/c1/note.md
drafts/c1/R1-attack.md:17:$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file blob 3f6edcc9:.ufo/waves/round-68/before/src/v73-fs_btrfs_sysfs.c | sha256sum
drafts/c1/SC1-report.md:42:    $ python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py .ufo/waves/round-68/drafts/c1/note.md
drafts/c1/SC1-report.md:98:    $ sed -n '2,3p' .ufo/waves/round-68/before/host.txt
drafts/c1/SC2-report.md:12:    $ awk -F'|' '/^\| S28[67] /{print NF}' .ufo/waves/round-68/drafts/c1/sources-rows.md
drafts/c1/SC2-report.md:16:    $ awk '/^\| S28[67] /{print gsub(/\|/,"|")}' .ufo/waves/round-68/drafts/c1/sources-rows.md
drafts/c1/SC2-report.md:45:    $ grep -nE '^## ' .ufo/waves/round-68/drafts/c1/lesson-round-68.md
drafts/c1/SC2-report.md:50:    $ grep -c '^## Mistakes' .ufo/waves/round-68/drafts/c1/lesson-round-68.md
drafts/c1/sources-rows.md:19:    $ awk -F'|' '/^\| S28[67] /{print NF}' .ufo/waves/round-68/drafts/c1/sources-rows.md
drafts/c1/sources-rows.md:25:    $ awk '/^\| S28[67] /{n=gsub(/\|/,"|"); print n}' .ufo/waves/round-68/drafts/c1/sources-rows.md
rc=0            (receipt lines keep their 4-space indentation)
```

- **9** are cwd-dependent filesystem operands (`E2-report.md` ×1, `SC1-report.md` ×2, `SC2-report.md` ×4,
  `sources-rows.md` ×2). Replayed from the fleet root they fail:

```
$ ls -la /home/vgpnk/Projects/shokunin/.ufo/waves/round-68/drafts/c1/sources-rows.md
ls: cannot access '/home/vgpnk/Projects/shokunin/.ufo/waves/round-68/drafts/c1/sources-rows.md': No such file or directory
rc=2
```

- **1** (`c1/R1-attack.md:17`) is not cwd-relative: `.ufo/…` follows the `:` of the git object spec
  `3f6edcc9:<path>`, resolved under an absolute `-C`, so it is portable.

Impact: 9 receipts are reproducible only from the lane root and none states the `cd`. Smallest remediation:
requote those command lines with the absolute lane prefix at integration (draft edit, not a seat rewrite).

## 5. After the wave — state diff (item step 6)

End snapshot `2026-11-03T22:40:40Z`; re-checked at `22:52:57Z` (identical):

```
$ git -C <lane> status --porcelain > $S/lane-end.txt ; wc -l < $S/lane-end.txt
10
$ git -C <fleet> status --porcelain > $S/fleet-end.txt ; wc -l < $S/fleet-end.txt
4
$ diff -u $S/lane-start.txt $S/lane-end.txt
--- …/lane-start.txt
+++ …/lane-end.txt
@@ -1,5 +1,8 @@
+ M corpus/lessons/round-67.md
 ?? .ufo/waves/round-66/w1.ready.dispatched
 ?? .ufo/waves/round-67/w1.ready.dispatched
+?? .ufo/waves/round-68/drafts/
+?? .ufo/waves/round-68/probes/
 ?? .ufo/waves/round-68/w1-dispatch.json
 ?? .ufo/waves/round-68/w1-run.stderr
 ?? .ufo/waves/round-68/w1.ready
rc=1
$ diff -u $S/fleet-start.txt $S/fleet-end.txt
rc=0            <- no line appeared or disappeared
```

`NEW_LANE_PATHS=2` — `?? .ufo/waves/round-68/drafts/` and `?? .ufo/waves/round-68/probes/`, the wave's own
allowed write surfaces (27 files under them at the end). **0 out-of-scope lane paths.**
`NEW_FLEET_PATHS=0` — fleet porcelain byte-identical to start.

The one new **tracked** lane modification and its attribution:

```
$ git -C <lane> diff --stat -- corpus/lessons/round-67.md
 corpus/lessons/round-67.md | 15 +++++++++++++++
$ stat -c '%n mtime=%y' <lane>/corpus/lessons/round-67.md
…/corpus/lessons/round-67.md mtime=2026-11-03 19:31:39.798730952 -0300      (= 22:31:39Z, 18 s after dispatch)
```

Attributed to the **L1**, not a seat, from the L1's own transcript (`history://TsukuroiR68`):

```
178|→ bash(grep -rn "grep -c -i limit" corpus/lessons/round-67.md …) ⇒ ok · 6 lines
182|Confirmed: 14 matching lines, 21 occurrences. Appending the erratum to round-67's lesson as a new block (never an in-place edit).
187|→ edit([tsukuroi-shokunin/corpus/lessons/round-67.md#A86E] PUT >127: ## Erratum (round 68) — R67-POSITIVE-CONTROL-COMMAND-MISM…) ⇒ ok · 18 lines
```

Append-only (`## Erratum (round 68) — R67-POSITIVE-CONTROL-COMMAND-MISMATCH`, +15 lines at EOF), and it is
the standing duty the declaration names. **Not a seat defect, no misroot.** See OBS-1.

Fleet HEAD moved during the window, entirely from other lanes — no commit touches this lane:

```
$ git -C <fleet> log -3 --format='%h %ci %s'
f812ba6b 2026-11-03 19:41:58 -0300 round-60: tabi report
0f5a47dc 2026-11-03 19:41:02 -0300 round-60: tabi L0 questions
cc9c0a6d 2026-11-03 19:34:08 -0300 round-68: kengaku dispatch evidence (hyaku inline attempt 1)
$ git -C <fleet> log --oneline ce99b22a..HEAD -- 'tsukuroi-shokunin' ; echo rc=$?
rc=0            <- empty
$ git -C <fleet> diff --name-only ce99b22a..HEAD
.ufo/l0-questions.md
.ufo/prompts/kengaku-round-68.md
.ufo/reports/round-60/tabi.md
MANIFEST.json
```

`MANIFEST.json` (`22:32:49Z`) and `.ufo/watchdog.log` (`22:43Z`) also carry mid-window mtimes; both are
other-lane/orchestrator writes — `MANIFEST.json` is committed and clean (`git diff --quiet -- MANIFEST.json`
rc 0; last commit `b49a89c5 … kengaku r67 closure, non-author`) and `watchdog.log` is gitignored
(`.gitignore:10`). Sibling repos `kaidoku/`, `tabi/`, `souji/` show their own tracked writes at `22:40-22:44Z`
inside their own repos (separate git roots; not fleet-tracked). None is a tsukuroi write.

## 5b. L1 integration window (captured after the wave, attributed)

At `22:54:51Z` the lane showed **18** porcelain lines: the L1 had begun landing (mtimes `22:50-22:51Z`). The
diff against the wave-time snapshot is entirely integration work:

```
$ git -C <lane> status --porcelain > $S/lane-integration.txt ; wc -l < $S/lane-integration.txt
18
$ diff -u $S/lane-end.txt $S/lane-integration.txt
+ M LOG.md
+ M SKILL.md
+ M corpus/QUALITY.md
+ M corpus/README.md
+ M corpus/SOURCES.md
  M corpus/lessons/round-67.md
 …
+?? corpus/knowledge/linux-v73-pinwatch-r68.md
+?? corpus/lessons/round-68.md
+?? tools/check-knowledge-refs-r68.py
diff_rc=1
```

The 12 additions are L1 integration writes on the lane's own tracked/integration paths — **not** seat writes
and **not** fleet-root paths (fleet porcelain still 4 lines, `NEW_FLEET_PATHS=0`). `NEW_LANE_PATHS` for the
post-wave snapshot stays **2** (the two wave dirs); the post-landing figure is **13** (5 `M` + 8 `??`), all
L1-owned. Editing tracked files is the L1's privilege and duty; no seat wrote one.

Measured read-only at that snapshot:

1. **Append-only holds.** `git diff --stat` over the five edited files = `133 insertions(+), 0 deletions`;
   `git diff -- corpus/SOURCES.md | grep -c '^-[^-]'` → `0`; SOURCES 285 → 287 rows, S286 at line 296 and
   S287 at 297.
2. **OBS-2 is resolved by landing order.** The note and its two rows arrived together, and every S-id on the
   landed note's `source:` line resolves (my own oracle, not the gate — a read-only seat cannot run the
   selftest-certified tool on a landed revision):

```
$ sed -n '1p' <lane>/corpus/knowledge/linux-v73-pinwatch-r68.md | grep -oE 'S[0-9]{3,}' | sort -u | wc -l
7
$ grep -oE '^\| S[0-9]{3,} ' <lane>/corpus/SOURCES.md | tr -d '| ' | sort -u | wc -l
287
$ comm -23 <note ids> <registry ids>          # dangling
rc=0            <- empty: 0 dangling ids
```

3. **Attestation does not transfer: the landed bytes are not the attested draft bytes.**

```
$ sha256sum <lane>/tools/check-knowledge-refs-r68.py <wave>/drafts/c2/check-knowledge-refs-r68.py
ada32b1320a3a4ff7a96591ce37710c7f74e80c3a7e189e867c3d8d2e30ddac1  tools/check-knowledge-refs-r68.py
d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5  …/drafts/c2/check-knowledge-refs-r68.py
$ diff -u <draft> <landed> | grep -c '^+' ; … '^-' ; … '^@@'
36 / 12 / 6 hunks
$ sha256sum <lane>/corpus/knowledge/linux-v73-pinwatch-r68.md <wave>/drafts/c1/note.md
71cbc4efda6cd1961145578034e80d6988cea38fd171467bea65c582941f5bc5  corpus/knowledge/linux-v73-pinwatch-r68.md
1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b  …/drafts/c1/note.md
```

- The tool diff is **semantic, not cosmetic**: `ID = re.compile(r"S[0-9]{3,}")` replaces `\bS\d{3,}\b`
  (exactly R2's attack-3 glued-id falsification), a fenced-registry rule is added (R2 attack 5), and the
  docstring moves QUALITY 98 → 101. Line numbers cited by the wave shift (E1's `397`/`500` are `408`/`524`).
- The note diff (+7/−4, 2 hunks) is R1's registry-scope limit plus "five named" wording; the row count
  survives (`| RWn |` = 6 in both, ids RW1-RW6).
- Consequence: `probes/c2-selftest.txt` (19/19 PASS) and E1's red-before receipt certify the **draft** bytes;
  no receipt in the wave certifies the landed gate. The integration gate must run `--selftest` on the landed
  bytes and record the landed sha256, and C1's counter must be re-run on the landed note (6 RW rows, but
  different bytes).
4. **No bytecode written by the landings.** `ls <lane>/tools/__pycache__` → `No such file or directory`; the
   landed tool keeps `sys.dont_write_bytecode = True` (line 48) and its only write-capable pair is the
   selftest sandbox (`tempfile.mkdtemp` 408, `shutil.rmtree` 524).

## 6. Observations (not boundary defects)

**OBS-1 — tracked erratum write; declaration says "round-68 lesson", bytes landed in round-67's.** The
declaration reads "the round-67 routed defect R67-POSITIVE-CONTROL-COMMAND-MISMATCH is corrected by an
appended erratum in the round-68 lesson"; the appended block is in `corpus/lessons/round-67.md` and
self-describes as being "carried by the round-68 lesson as a Mistakes row". Reconcile the wording at
integration so the receipt chain names the file that changed. Also: it is a tracked mutation inside the
measured window, so the before/after census must be dated against `22:31:39Z`.

**OBS-2 — landing-order hazard: the C1 note cites ids the registry does not define yet.**

```
$ sed -n '1p' <wave>/drafts/c1/note.md
source: S138, S149, S158, S182, S185, S286, S287 — the pinned upstream files …
$ grep -nE '^\| S28[67] \|' <lane>/corpus/SOURCES.md ; echo rc=$?
rc=1            <- neither S286 nor S287 in the tracked registry (last rows S284, S285)
$ grep -cE '^\| S[0-9]+ \|' <lane>/corpus/SOURCES.md
285
```

Landing the note before (or without) the S286/S287 rows makes the new gate report `KNOWLEDGE-REF-DANGLING`
for both ids at the landed revision. [INFERENCE — not run: proving it needs a commit containing the note,
which a read-only seat cannot make; the mechanism is proven for this exact shape by the wave's own fixture,
`probes/c2-red-before.txt:28` → `"dangling_count": 1 … "ref": "S999"`.] Remediation: land the two rows in the
same commit as the note, or first. **Resolved at integration (§5b.2):** the note and both rows landed together
and all 7 note ids resolve against the 287-row registry.

**OBS-3 — step 5's pipeline is vacuous** (§4): `grep -v '/home/vgpnk'` cannot separate content from grep's
own `-n` filename prefix. A later round reusing this step should filter on the match body or use `-h`.

**OBS-4 — the draft gate's only write-capable code is its `--selftest` sandbox**, inherited from the base:

```
$ grep -nE '\.write\(|open\([^)]*["'"'"'](w|a|w\+|ab)["'"'"']|os\.(remove|unlink|rename|mkdir|makedirs|chmod)|shutil\.(copy|move|rmtree)|tempfile\.' <draft>
397:    repo = Path(tempfile.mkdtemp(prefix="knowledge-refs-gate-"))
500:        shutil.rmtree(repo, ignore_errors=True)
$ grep -nE 'git\(|subprocess\.(run|check_output|Popen)' <draft> | head
110:def git(repo, *args, timeout=60):
120:    kind = git(repo, "cat-file", "-t", spec)
125:    proc = git(repo, "show", spec)
133:    listing = git(repo, "ls-tree", "-r", "--name-only", sha, SCOPE)
326:def sandbox_git(repo, *args):
339:    sandbox_git(repo, "add", *sorted(tree))
340:    sandbox_git(repo, "commit", "-q", "-m", "fixture")
$ sed -n '47,49p' <draft>
import sys

sys.dont_write_bytecode = True  # the shared-module import stays read-only
```

The production path runs only `cat-file`, `show`, `ls-tree`, `rev-parse`, `merge-base` through
`git --no-pager -C`; no `/tmp` path is written by any receipt.

**Hash cross-checks that hold** (so the L1 can trust the draft chain): `c1/E2-report.md` self-attests
`count-rw-r68.py` `b93f5912…438458` and `c1-battery.txt` `5ff7a184…fcc260` — both match the measured bytes;
`c2/E1-report.md` attests the gate draft `d4390b7a…7858d5` — matches the measured draft.

## 7. Artifact inventory measured (26 files, excluding this report)

```
4d3c279bfaa6f2b4b8793a28fd5d43515ffdbd1908913547780ce9a3783907a9  drafts/c1/connector-overlap.md
b93f5912d91be4787c5c595e10f5a15501cd64e9af6cd87916b28cd350438458  drafts/c1/count-rw-r68.py
a1ca17c006947de65ae0be6b2d3d92f270405eab66155d67b37e1da54aed9c77  drafts/c1/E2-report.md
677c164be9cf80317b01970c6c7798254534c9e28eb0dae7c5e3a11e8610fb48  drafts/c1/K1-falsify.md
045328ca4838a1c0d835773edbc82f13eede24954e92c6e0f4e50327b759d07a  drafts/c1/lesson-round-68.md
6649ac6cc66a8d08af994e981b1c2f74a8e83d44ab0115615b67eb3bb6f9f487  drafts/c1/M1-report.md
1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b  drafts/c1/note.md
e0cd25d80fc78d013b54a2f5b947d6e6efe932e96be47b26ffa6d9a49c482656  drafts/c1/R1-attack.md
731a79c4a9727fa503b0e9876b1d07570e5917e8d2d74cc869eec921b503e25c  drafts/c1/S1Scout-verify.md
ec90439489fa685980ab77ce33ab6b16a513e84f8cac135897c86fbee2e2e690  drafts/c1/SC1-report.md
b8734b08bccefcadb6bef118406b13cafee4b8740234e34c2cc1f93011deb571  drafts/c1/SC2-report.md
4001ae93c9f51e1dd1a90c9b08b296129ad28b654c15e1f04bae00b8797103b1  drafts/c1/sources-rows.md
d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5  drafts/c2/check-knowledge-refs-r68.py
34b263e0c55e52755e1e7db216f7aff1123403d8d571dc9c4c576a34a63847af  drafts/c2/E1-report.md
5d89bef969a28baf12224840fdf6eb4da1ee9c33fd95d3729f4f8dd5c75c79b4  drafts/c2/quality-101.md
e52b914e78fa89dccf4d99b301f406f1883668ca41dc33125cf2433b074d367e  drafts/c2/R2-attack.md
a98c40cd37fb40ffc8394c0e9490031b160a4bbefb4189b292d06339b6a2e137  drafts/c2/registry-round64-table.md
674cbed977aca34232fe069f3d7c0a155cbce5cd053cef6076b407f8ac33bfd5  drafts/c2/registry-round68-section.md
4b8a9246389e15fe2106c96f70f0e2b2ebfa08e37af581a6c5fb7053c34f2627  drafts/c2/S2Scout-gate-rules.md
7f3632f03ae3c8c60e2954f388eb03c2dc593c2325ab7dbc2804a7d13daeddba  drafts/c2/S2Scout-host-and-rules.md
5ff7a184334ee624ca074fec5483e3b427f16292192b0e295fadfff47cffc260  probes/c1-battery.txt
d13731b21edc04c6d77f19cd812ce9d42d6bb47f2a9a59c7bd8a033541777cf0  probes/c2-live-base.json
022929df929c08dc8114ff171509457b8b608844bf0696c31fd3eb06585b983d  probes/c2-red-before.txt
b0000cd3b0a3784b79cd549aae94fa4986ab4f73630248c1d08d691e8872f7c6  probes/c2-selftest.txt
62864038e5b39b7ed3672ec9f98c8db458be6277686c8ad501bc50dcad13c711  probes/m1-kill-matrix.txt
441b06304240685f31a31c99dd240e933faf3f519b0cf6626fb567f51c3dd9aa  probes/m1-vs-e2-counter.txt
```

Two paths the spec's seat list does not name also landed, both inside `drafts/c2`: `registry-round64-table.md`
(71,509 B) and `registry-round68-section.md` (72,493 B, an append-only registry continuation adding the
`check-knowledge-refs-r68` row). They are within the allowed surface and pass all four sweeps; they are
named here only so the L1 knows where 195 KB of the wave's drafts came from.

## 8. Boundary surface this seat reached

Read-only only: `git status/diff/log/rev-parse/merge-base/cat-file/ls-files/check-ignore` in the lane and the
fleet root; `find/stat/sha256sum/grep/sed -n/awk/wc/du/date/ls/file` on local paths; one read of
`history://TsukuroiR68`. No pacman, no `sudo`, no service or journal action, no git/jj write, no network, no
subagent dispatch, no background job, no write outside this file.
