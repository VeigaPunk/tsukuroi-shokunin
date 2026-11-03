# SC1Scribe — C1 note draft (round 69, w1)

Seat: SC1Scribe (scribe), leaf, no delegation. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
base `acce353b`, declaration commit `920a9eea`. Scratch `/fast/scratch/hyaku/tsukuroi-r69/SC1Scribe`
removed at exit; every retained byte is in `probes/SC1Scribe/`.

## Behavior

Drafted `.ufo/waves/round-69/drafts/c1/note.md` (12246 bytes, 106 lines, 5 KR rows + Reading + Relation to
held ground + Limits + Falsifiers). After the L1's note-before-draft steer the entry is additive:
KR1/KR2 re-ground KT1/KT6 of `corpus/knowledge/kernel-taint-r27.md` at the running tag with the
required phrase and claim no new taint mechanism; the depth sits in KR3 (the `VERMAGIC_STRING`
composition rule and its `CONFIG` conditionals, including `CONFIG_PREEMPT_RT` versus
`CONFIG_PREEMPT_BUILD`), KR4 (the host module's string as the rule's instantiation, the release-token
consequence for the second tree, package ownership and the reboot-pending predicate) and KR5
(applicability, unknowns, named falsifiers). Header carries `source:` naming only S288 and S289,
`verified-at: 2026-11-03`, and `recheck: on-release` with a steer-safe (QUALITY 26) procedure.

Reviewer corrections applied (R1Reviewer-3), two rounds. First round: the timing claim was
re-measured rather than inferred (`journalctl -b -k -o short-iso` first line is the banner at
`2026-11-02T12:07:17-03:00`, 13754 lines this boot); receipt citations now name the exact probe
files that carry `dmesg_restrict`=1, `/sys/kernel/debug` mode 0700 and the `%NAME%`/`%VERSION%`
markers; KR5 was reframed so its quote supports the diagnostic claim; falsifiers now say which row
each observable kills. Second round narrowed three statements: KR4 now claims only that the
`6.18.57-2-lts` stamp differs from the stamp this kernel composes (the loader's comparison and its
force modes are outside the pins — no rejection claimed); KR5 says the taint names a cause rather
than a verdict, because the table spans benign and severe causes; the timing limit no longer claims
"nothing earlier was emitted", only that the journal cannot show a discarded line.

## Gates (run by this seat, on this seat's own artifact)

```
$ python3 mirror.py   # exact evaluate() clauses of drafts/c2/count-kr-rows-r69.py against note.md
KR_ROWS=5 KR_VERIFIED=5
KR_ROW KR1 ok ... KR_ROW KR5 ok
rc=0
```
(mirror = the frozen counter's clauses: 6 cells, `KR[0-9]+`, unique id, statement >= 12 words,
`source=S[0-9]{3,}` in the registry, bare snapshot basename readable under
`before/src/`, digest == sha256, `quote="(.*)"` 1..25 words, whitespace-normalised containment.
Registry = live `corpus/SOURCES.md` (287 ids) plus the two rows drafted at
`drafts/c1/sources-rows.md`, because S288/S289 are not in `## Registry` at base.)

```
$ cd .ufo/waves/round-69/before/src && sha256sum -c SHA256SUMS
tk-v7211.rst: OK
vm-v7211.h: OK
rc=0
```
Quote receipts (`quote-check.txt`): 19, 7, 16, 6, 19 words, each located at a byte offset in its
named snapshot, none containing `|`. `cmp -s` between `before/src/tk-v7211.rst` and the round-27
`S140.rst` → rc 0 (identical bytes, same sha256).

## Touched surfaces

- `.ufo/waves/round-69/drafts/c1/note.md` — written (the only deliverable file).
- `.ufo/waves/round-69/probes/SC1Scribe/{host-read,privilege-read,pacman-localdesc,timing-and-crosschecks,quote-check,note-selfcheck}.txt` — written, each starting with a UTC timestamp, each block `$ command` / verbatim output / rc.
- `.ufo/waves/round-69/w1/SC1Scribe.md` — this report.
- Nothing else. No tracked file, corpus file, registry row, counter, tool, state file or sibling
  path was modified; no git command beyond read-only `rev-parse`-free reads; no package
  transaction; no privileged read; no module load.

## Findings

1. `corpus/SOURCES.md` holds 287 rows at base and no S288/S289; the frozen counter scans only the
   `## Registry` section, so the two KR rows that cite S288/S289 verify only after those rows land
   there. The rows drafted at `drafts/c1/sources-rows.md` parse as ids S288 and S289 under the same
   row regex the counter uses.
2. The counter draft (`drafts/c2/count-kr-rows-r69.py`, sha256 `db2b4917…`) resolves `snapshot=` as
   a bare basename under `before/src` and uses a greedy `quote="(.*)"`; both were honoured. The
   note's `snapshot=` cells are bare filenames.
3. S288's snapshot is byte-identical to S140's v7.2 copy (`cmp -s` rc 0), so the taint rows record
   tag stability and the host reading, not a second mechanism — the additive framing is factual.
4. First kernel log line this boot is the banner at `2026-11-02T12:07:17-03:00`; the two `nvidia:`
   cause lines share that second, and the `Tainted:` prints follow at 16:49:24/16:49:45. 13754
   kernel lines are retained.
5. `modinfo -F vermagic` on `/usr/lib/modules/6.18.57-2-lts/kernel/arch/x86/crypto/aegis128-aesni.ko.zst`
   prints `6.18.57-2-lts SMP preempt mod_unload` (rc 0, `probes/SC1Scribe/lts-module-vermagic.txt`),
   so the release-token consequence rests on two module files, not only the running tree's dkms
   module. Disclosure: the first run of that probe was exploratory and its output was not retained;
   the receipt is a re-run taken at 2026-11-03T23:26:53Z to give the note a citable byte, and it
   reproduces the value the note cites.
6. `pacman -Qo /usr/lib/modules/<tree>` prints two owners per tree (kernel package plus
   `*-headers`); `pacman -Qo` on a missing path is rc 1 with an `error: No package owns …` line
   (S2Scout's datum, re-read here only as context). Neither is used as a number in the note.
7. The `desc` file under `/var/lib/pacman/local/linux-7.2.11.arch1-1/` uses `%NAME%`/`%VERSION%`
   markers at lines 1 and 4 with values on the following lines; a first attempt with
   `grep -E '^(NAME|VERSION)='` returned rc 1 and that wording was corrected before landing in the
   note's `recheck:`.
8. `dmesg_restrict` reads 1 and `/sys/kernel/debug` is mode 0700 root:root, so the root-only
   report limit in `## Limits` is evidenced, not assumed.

## Out of scope (not done, by design)

No counter authored or edited, no registry rows committed, no `lesson.md` content, no C2 census
code, no lane gate, no build/selftest, no commit/push, no `merge/tsukuroi/`, no considerthese, no
pacman, no privileged read, no module load. Left to L1: landing `note.md` as
`corpus/knowledge/kernel-taint-plane-r69.md` together with the two S288/S289 registry rows, then
running `tools/count-kr-rows-r69.py` at the landed revision.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/host-read.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/privilege-read.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/pacman-localdesc.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/timing-and-crosschecks.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/lts-module-vermagic.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/quote-check.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/SC1Scribe/note-selfcheck.txt`

SC1_ROWS=5 SC1_QUOTE_WORDS=19,7,16,6,19 SC1_SOURCE_IDS=S288,S289
SC1_PATH=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
