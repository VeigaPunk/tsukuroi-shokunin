#!/usr/bin/env python3
# Build .ufo/waves/round-73/w1-spec.json for the round-73 v1 wave (12 seats, band 8-16).
# Committed as wave evidence, not run by anything else.
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
W = ".ufo/waves/round-73"
DECL = "749371321c00f04d98c29d2c26b57d75a92d7e37"
BASE = "eb1057575d5d8b940c4846e21611674cf5571aea"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r73"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + f"""
## You are an L2 seat of tsukuroi lane round 73 (hyaku run 15), wave w1

Round 73 has **two frozen claims**, declared before any data at commit `{DECL}` (base `{BASE}`):

- **C1 depth (lowest tied axis, 8).** A new entry `corpus/knowledge/systemd-unit-load-plane-r73.md`
  with six rule rows UL1-UL6 on the systemd unit-load merge plane, sourced from three systemd **v262**
  snapshots (`man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c`) committed byte-exact at
  `{LANE}/{W}/before/src/`. Counter: `python3 tools/count-ul-rows-r73.py --revision <REV>`
  (sha256 `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6`); target
  `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0.
- **C2 freshness (9).** Three routed defects from the round-72 closure close in committed bytes
  (lesson correction, instrument-digest erratum, capability refresh). Checker:
  `python3 tools/check-r72-routed-r73.py --revision <REV>`
  (sha256 `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e`); target
  `ROUTED_STALE=0 ROUTED_OK=3/3`, rc 0; at base it reads `ROUTED_STALE=3`.

Both instruments and their `--selftest` modes are **frozen**: you may attack them, you may not edit them
in the lane repo. If an attack proves a defect, write the defect, the exact command and the observed
output; the L1 repairs and, per the declaration's frozen rule, re-runs the before control with the final
instrument and records old->new digests.

## What an attack seat owes

Attack seats (reviewer, critic, mutation-tester) **falsify**: re-run each counting command, re-open each
source at the pinned tag, try to satisfy a predicate without doing the work (a content-free row, a
fabricated quote, an unanchored block, a scripted writer that copies quotes), and report each attempt as
`held` / `survived` with the command and the output. A finding with no command is a guess.

## Paths, scratch and write scope

- Lane repo (read-only for you except your own wave-dir files): `{LANE}`.
- Your outputs: `{LANE}/{W}/w1/<YOUR-SEAT-NAME>/`. Every `Report:` trailer path the validator renders is
  relative to `{LANE}` — write it at `{LANE}/<that path>`.
- Scratch: `mkdir -p {SCRATCH}/<YOUR-SEAT-NAME>` and start every shell with
  `S={SCRATCH}/<YOUR-SEAT-NAME>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`.
  Copy outputs you need to keep into your wave-dir first; **delete the scratch dir before you yield**
  and treat a leftover tree as your own defect. Never write under `/tmp`; pass `TMPDIR=$S` to every
  tool that honours it.
- **Never** run `git commit`, `git add`, `git stash`, `git checkout`, `git reset`, `git push`, or any
  mutating `jj` command anywhere. Never create a git fixture in the lane: any fixture repo is
  `D=$(mktemp -d -p "$S") && git -C "$D" init -q` and every later call names `-C "$D"`; verify
  `git -C "$D" rev-parse --show-toplevel` is `$D` first. Never write into the fleet root
  `/home/vgpnk/Projects/shokunin` (no `.ufo/`, no report, no `SCORECARD.md` there).
- Never edit a sibling lane (`../mori-shokunin`, `../kama-shokunin`, ...), `MANIFEST.json`,
  `.ufo/state/`, `.ufo/watchdog.log`, `~/.omp/agent/config.yml`, or any MCP config.
- Never send `agent://all`. If you must coordinate, message the L1 `TsukuroiR73`.
- **Write your binding file first.** Your first write into your wave dir is `<seat>.md` with two lines —
  `status: in-progress` and `verdict: pending` — plus a minimal honest body; deepen it afterwards. A seat
  cut mid-turn without that file binds nothing (QUALITY 96).

## Tooling

You may install or upgrade tools that help the task (read `/home/vgpnk/.omp/agent/RULES.md` first:
official channels only, record tool/version/channel/reason in your report). **All pacman transactions
are PAUSED host-wide** until the operator clears the host-recovery L0 question: use `uv tool`, `npx`, or
an official binary in `~/.local/bin`; never `pacman -S/-Sy/-Syu/-U/-R`. If a fetch needs the network it
is read-only and fine.

## Host facts you may rely on (re-measure, do not trust)

Linux 7.2.11-arch1-1, systemd 262.1-1-arch, kmod 34.2. The committed host readings are
`{LANE}/{W}/before/host.txt`: 12 search-path directories, `passim.service` and
`systemd-networkd-wait-online.service` masked to `/dev/null`, `user@1000.service` reading both
`/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf` and
`/etc/systemd/system/user@.service.d/faster-shutdown.conf`, `getty@tty1.service` resolving to
`getty@.service`. The lane is read-only: never start, stop, mask, unmask, enable, disable or edit a unit.
"""


def item(name, role, axes, milestone, body):
    return {
        "name": name,
        "role": role,
        "axes": axes,
        "milestone": milestone,
        "item": name,
        "prompt": CONTEXT + "\n## Your item\n\n" + body.strip() + "\n",
    }


items = [
    item("S1Scout", "scout", ["depth", "C1", "sources"],
         "independent second-route re-fetch of the three v262 snapshots, quote locations, host re-capture",
         f"""
Independently prove the three pinned snapshots are the upstream v262 bytes and that the six planned
quotes sit where the round says. Do not trust the committed digests until you recompute them.

1. Fetch each file by a **second route** — `https://github.com/systemd/systemd/raw/v262/<path>` and/or
   `https://codeload.github.com/systemd/systemd/tar.gz/refs/tags/v262` — and compare with the committed
   bytes and with `{LANE}/{W}/before/src/SHA256SUMS`; report `ROUTE2_OK=<n>/3` and any byte delta.
2. For each of the six planned quotes, print the file and the exact line numbers where the quote starts
   and ends after whitespace normalization:
   - `manifest` (systemd.unit.xml): "Unit files found in directories listed earlier override files with
     the same name in directories lower in the list"; "Multiple drop-in files with different names are
     applied in lexicographic order, regardless of which of the directories they reside in".
   - `unit.c`: "For masked files check if they are still so"; "any drop-ins that are masked are simply
     omitted from the list".
   - `install.c`: "Unit %s is masked, ignoring."; "Unit %s is an alias to a non-existent unit, ignoring."
   Record each as `quote=<file>:<start>-<end>` and say whether the line numbers the note should cite.
3. Re-capture the host surface read-only and diff against `before/host.txt`: `systemd-analyze unit-paths`,
   `systemctl list-unit-files --state=masked --no-legend`, `systemctl show -p DropInPaths -p
   FragmentPath -p LoadState user@1000.service getty@tty1.service`, `find /etc/systemd/system -maxdepth 1
   -type l -lname /dev/null | wc -l`. Report every delta with its command.
4. Check one thing the round does not claim and say so explicitly if it is unheld: whether
   `/usr/lib/systemd/system/*.d/` drop-ins are visible without privilege in each of the three
   directories (`/etc`, `/run`, `/usr/lib`), with `ls -ld` output.

Write `{LANE}/{W}/w1/S1Scout/report.md` with: `ROUTE2_OK`, the six `quote=` lines, the host delta table
(empty is a result), and a `## Limits` section for anything you could not verify.
"""),
    item("E1Counter", "executor", ["depth", "C1", "counter"],
         "independent exercise of the frozen C1 counter and a scripted non-reader control",
         f"""
Exercise the frozen C1 counter (`{LANE}/tools/count-ul-rows-r73.py`) as an adversary, not as its author.

1. Run `TMPDIR=$S python3 {LANE}/tools/count-ul-rows-r73.py --selftest` and
   `--revision {BASE}` (expect rc 128 `UL_NOTE absent`). Paste both.
2. Build an independent mirror of the note under `$S/mirror` (copy `before/src` and a registry with
   S304-S306) and write your own six UL rows from the pinned snapshots, without copying the sample rows
   in the tool. Run the counter with `--fixture "$S/mirror"`. Report `met`, and per row the `UL_ROW`
   line.
3. **Scripted non-reader control** (QUALITY 81): write a script under `$S` that fetches the three pinned
   files, takes the first token-bearing line as the quote and fills the statement with words recovered
   from the file's own bytes, then scores it. Report whether the frozen predicate admits it (`met=1`) and
   name the clause that stops it if not.
4. Clause isolation: for each frozen clause (id contiguity, statement words, grounding, source kind,
   digest, map binding, anchor binding, quote location, quote length, snapshot reuse) produce one fixture
   that violates only that clause and report the printed finding token. Note any clause you cannot
   isolate.
5. Report the counter's own blind spot: a row that keeps every token but **negates** its statement should
   still read `met=1` — prove it and record it as a named limit, not a defect.

Write `{LANE}/{W}/w1/E1Counter/report.md` with the command outputs and a `## Survived` / `## Killed`
table. Do not edit the tool; propose exact replacement lines in the report if you find a defect.
"""),
    item("E2Routed", "executor", ["freshness", "C2", "receipts"],
         "C2 repair drafts scored against the frozen routed checker plus tamper probes",
         f"""
Prepare the three C2 repairs as **drafts** and prove the frozen checker
(`{LANE}/tools/check-r72-routed-r73.py`, sha256 `93f034e3...`) accepts them only when they are real.

1. Run `--selftest` and `--revision {BASE}`; paste both (expect rc 0 selftest; `ROUTED_STALE=3` at base).
2. In `$S/fixture/` build a `--root` fixture with the lane's `SCORECARD.md` and
   `corpus/lessons/round-72.md` **copied**, then draft inside it:
   (a) an appended correction block in the r72 lesson naming `R72-LESSON-SUPERSEDED-CLAIMS`, both
   superseded sentences and the landed `gate-selftest` / ten-case state;
   (b) an appended SCORECARD erratum naming `R72-C3-INSTRUMENT-DIGEST-DRIFT`, the digests
   `df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` ->
   `2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc`, the repaired checker's repairs
   and the same-instrument receipt path `{LANE}/.ufo/waves/round-72/after/selftest-selftest-after.txt`;
   (c) an appended capability-refresh block restating `gate-selftest` as **ten** cases with the receipt
   path.
   Score it: `python3 {LANE}/tools/check-r72-routed-r73.py --root $S/fixture` must print
   `ROUTED_STALE=0 ROUTED_OK=3/3`.
3. Tamper probes (each must read rc 1 and name its finding): remove the digest line; rename the heading
   so the block is prose; put every token in a paragraph outside a `##` block; claim the old repair was a
   denial ("no repair was needed"); change `ten` to `nine`. Report the exact output of each.
4. Verify the underlying facts yourself: `git -C {LANE} show {BASE}:corpus/lessons/round-72.md | grep -n
   "No capability row enters this round\\|nine hermetic cases"`; the r72 cascade digest
   `sha256sum {LANE}/tools/check-r71-routed-r72.py`; the receipt's last line
   `grep -c "SELFTEST: PASS" {LANE}/.ufo/waves/round-72/after/selftest-selftest-after.txt`; and the
   capability row text in `SCORECARD.md` (search `gate-selftest`).

Write `{LANE}/{W}/w1/E2Routed/report.md` with the draft blocks **verbatim** (the L1 adopts them) and the
probe table. State which drafted sentence you could not ground.
"""),
    item("E3HostProbe", "executor", ["operability", "C1", "probe"],
         "read-only host probe for the unit-load surface with failure-mode tests",
         f"""
Build a read-only probe (draft in scratch; the L1 decides whether it lands) that measures the
unit-load surface the C1 entry describes, and show what it does when `systemctl` is absent.

1. Write `$S/unit-load-probe.sh` (bash, no privileged command, no unit mutation) emitting one
   `key=value` line per reading, each token validated against a closed pattern (QUALITY 84):
   `SEARCHPATH dirs=<n> first=<path> etc_before_usr=<0|1>` from `systemd-analyze unit-paths`;
   `MASKED count=<n> targets=/dev/null:<n>` from `systemctl list-unit-files --state=masked` plus
   `readlink` on `/etc/systemd/system/<unit>`;
   `DROPINS unit=<name> paths=<n> etc=<n> usr=<n>` from `systemctl show -p DropInPaths`;
   `TEMPLATE instance=<name> fragment=<basename> template=1` from `systemctl show -p FragmentPath`;
   `UNITSTATE unit=<name> load=<state>`.
2. Run it, capture the output into your wave dir. Then run it with a stub `PATH` that hides
   `systemctl` (a `$S/bin` dir with a `systemctl` that exits 127, placed first on `PATH`) and show every
   line degradating to `BLOCKED reason=tool-absent` rather than printing a wrong count.
3. Test the echo guard: plant a fake unit name containing a `|` and a newline in a fixture directory
   (`$S/fixtures/etc/systemd/system/`), point the probe at it by an override the probe honours
   (`TSUKUROI_UNIT_DIRS` or equivalent you define) and show the forged line cannot escape the grammar.
4. Report what a probe like this must never do here (mask/unmask/enable/disable/edit) and whether it
   belongs in the census or stays a probe.

Write `{LANE}/{W}/w1/E3HostProbe/report.md` (or `probe.sh` + `report.md`) with the three receipts and a
`## Limits` section. Do not add it to `tools/`; the L1 integrates.
"""),
    item("SC1Entry", "scribe", ["depth", "C1", "note"],
         "C1 knowledge entry draft: six UL rows in the frozen row format plus host prose and limits",
         f"""
Draft the C1 entry exactly in the frozen row format so the counter can score it.

1. Read `{LANE}/{W}/before/src/` (three snapshots) and `{LANE}/tools/count-ul-rows-r73.py` (the row
   format and clauses). Work only from the snapshots and the committed host readings.
2. Write `{LANE}/{W}/w1/SC1Entry/systemd-unit-load-plane-r73.md` as the **whole note**, in this shape:
   - front matter paragraph: what the plane is, why repair needs it, the pinned tag v262 and the host's
     262.1-1-arch, and that upstream line anchors are not host-build line numbers (QUALITY 103).
   - the six rows, one line each, exactly: `| UL<n> | <statement> | source=S<id> |
     snapshot=<basename> | digest=<64 hex> | quote="<quote>" |`, ids UL1-UL6 contiguous, statements at
     least 12 words and grounded in the snapshot, quotes at most 25 words and located verbatim. Use
     S304 for `systemd.unit.xml` (UL1, UL2), S305 for `unit.c` (UL3, UL4), S306 for `install.c`
     (UL5, UL6). The digests are in `{LANE}/{W}/before/src/SOURCES.json`.
     Cover: the load path and `SYSTEMD_UNIT_PATH`; drop-in merge order and `/etc`>`/run`>`/usr/lib`
     precedence with cross-directory lexicographic order; the reload condition (drop-in set change or
     newer drop-in, masked drop-ins omitted); masking by empty file **or** `/dev/null` symlink and the
     `null_or_empty` still-masked test; `unit_file_mask` writing the `/dev/null` symlink and the
     `masked`/`masked-runtime` install modes; `[Install] Alias=` parsed at enable time with a dangling
     alias ignored.
   - a `## Host readings` section: one row per reading with the exact command and observed value from
     `{LANE}/{W}/before/host.txt` (search path, two masks, the user@1000 template+prefix drop-ins, the
     getty@tty1 template fallback). Mark anything you re-measured yourself with its date.
   - a `## Limits` section: what the host does not show (no instance-specific drop-in here, no alias
     symlink read, no `SYSTEMD_UNIT_PATH` set), and that the plane is documented order, not a measured
     resolution of every fragment on this host.
3. Self-check before you yield: `cp` your note into a scratch mirror with the committed `before/src` and
   a 3-row registry, then run `python3 {LANE}/tools/count-ul-rows-r73.py --fixture "$S/mirror"` and paste
   the result. If it reads `met=0`, fix the row, not the counter.

Write your draft at the path above plus `{LANE}/{W}/w1/SC1Entry/report.md` naming the counter output.
"""),
    item("SC2Sources", "scribe", ["depth", "C1", "registry"],
         "registry rows S304-S306, Gate quotes, search log and one honest rejection",
         f"""
Draft the registry and gate text for C1. Nothing is appended by you; the L1 appends.

1. Read `{LANE}/corpus/SOURCES.md` (registry schema, 11 columns, no `|` inside a cell; current last id
   S303) and the contract in `/home/vgpnk/Projects/shokunin/CORPUS.md` section *SOURCES.md*.
2. Draft three rows S304, S305, S306 for the three v262 snapshots: `kind` docs/code, `tier` A, `scope`
   naming the exact rule set the snapshot grounds, `anchor` naming the file **basename plus tag v262 and
   the line ranges** (the counter requires the snapshot basename to appear in the anchor cell),
   `teaches` one grounded benefit, `status` mined, `opened` 2026-11-03, `recheck` on-release, `used-by`
   `corpus/knowledge/systemd-unit-load-plane-r73.md`. The `source` cell must contain the URL from
   `{LANE}/{W}/before/src/SOURCES.json`.
3. Draft the lesson's `## Gate` block: per new row the URL, the access date, and one ≤25-word quote with
   its `file:line` location (quote the snapshot text you actually opened).
4. Draft a `## Search log` entry in the PRISMA-inspired shape: question, queries, where searched, date,
   identified / screened / included / excluded counts, exclusion reasons, stop rationale.
5. **One honest rejection is required this round** (routed defect R72-GATE-NO-REJECT): open at least one
   candidate source that does not clear the bar and write its row as
   `REJECTED: <reason>; flip: <what would change the verdict>` — with the fetch command and the observed
   status. A real candidate: the systemd *release* page `https://api.github.com/repos/systemd/systemd/
   releases/tags/v262` (already S283 in this registry — check it, do not duplicate) or the Arch package
   page `https://archlinux.org/packages/core/x86_64/systemd/` (build provenance only), or
   `man/systemd.unit.5` from man.archlinux.org (a rendered copy of the same man page, not independent
   evidence). Verify the duplicate/collision with the census check before you propose any id.

Write `{LANE}/{W}/w1/SC2Sources/rows.md` (the three rows verbatim, ready to append),
`{LANE}/{W}/w1/SC2Sources/gate.md` and `{LANE}/{W}/w1/SC2Sources/report.md`.
"""),
    item("SC3Index", "scribe", ["depth", "C1", "skill"],
         "SKILL decision table, PROVINCE promotion note, README index and registry row drafts",
         f"""
Draft the index/doc deltas C1 owes, as text the L1 can append.

1. Read `{LANE}/SKILL.md` (the decision-table style and the *Gate and probe registry — round71
   superseding current rows* table plus the round-72 continuation below it),
   `{LANE}/PROVINCE.md` (the Core / Frontier structure and the round-70/71/72 promotion paragraphs) and
   `{LANE}/corpus/README.md` (the per-round coverage index).
2. Draft a **repair decision table** for the new plane, keyed by symptom, each row a mechanism plus the
   rule ids it rests on and the read-only command that confirms it:
   | symptom | mechanism | row | check |
   - "my drop-in is ignored" → wrong directory precedence or a same-named drop-in higher up;
   - "my override vanishes after a package update" → /usr/lib drop-in vs /etc unit file precedence;
   - "the unit says changed on disk / needs reload" → drop-in set change or newer drop-in;
   - "the unit is masked" → empty file or /dev/null symlink, and `LoadState=masked`;
   - "masked but still enabled" → `UnitFileState` vs `LoadState` (host: systemd-networkd-wait-online);
   - "the instance has no file" → template fallback and instance/template drop-in lookup.
   Every claim must cite UL1-UL6 or a host reading; no new facts.
3. Draft the `PROVINCE.md` append: a **Frontier → Core** paragraph for the unit-load merge plane stating
   what is Core (the documented merge/precedence/mask/reload reading), what stays Frontier (the effective
   resolved value of a specific unit's merged configuration on this host — not measured; host-build line
   numbers), and what stays operator-owned (mask/unmask/enable/disable/edit/daemon-reload).
4. Draft the `corpus/README.md` round-73 index section: the note path, the rows, the sources, and the
   frontier sentence.
5. Draft the gate-registry continuation row for `count-ul-rows-r73` (name, kind probe/gate, entry
   command, verdict map 0/1/128/-3, self-test `--selftest` with eleven named cases, pinned values, write
   scope `$TMPDIR` only, owner) and, separately, the row for `check-r72-routed-r73` (five self-test
   cases). Do not break the table's single-header rule (QUALITY 92).

Write `{LANE}/{W}/w1/SC3Index/deltas.md` with each draft in its own fenced block labelled by target file.
"""),
    item("C1Connector", "connector", ["adjacency", "C1", "overlap"],
         "sibling-overlap scan for systemd unit-load ground and a held-corpus restatement check",
         f"""
Find out whether the ground C1 claims is already held by a sibling lane or restated inside this corpus.

1. Sibling scan (read-only): grep each sibling `PROVINCE.md` and `SKILL.md` under
   `/home/vgpnk/Projects/shokunin/*-shokunin/` for the terms `drop-in`, `dropin`, `mask`, `unit load`,
   `systemd/system`, `FragmentPath`, `UnitFileState`, `daemon-reload`. For each hit decide
   `owns | adjacent | none` against `/home/vgpnk/Projects/shokunin/{LANE.split('/')[-1]}/PROVINCE.md` and
   record the sibling, the path:line, the quoted boundary sentence and the decision. Candidates worth
   checking: mori (memory/oom units), kumitate (dispatch units), mado (desktop units), kama (serving
   units), tameshi (method).
2. Held-corpus restatement check: for each of the twelve `corpus/knowledge/` files that mention
   `drop-in`, read the surrounding lines and decide whether it already states a merge/precedence/mask
   **rule** (it would make C1 a restatement) or only observes a named file. Quote the line you judged.
3. Write the overlap table with an explicit `REPORTED, NOT ABSORBED` column: anything a sibling owns is
   reported to the L1 for the report, never edited.

Write `{LANE}/{W}/w1/C1Connector/report.md` with the table and a one-line verdict:
`GROUND_UNHELD=yes|no` plus the evidence that decides it.
"""),
    item("R1Reviewer", "reviewer", ["depth", "C1", "attack"],
         "per-row entailment verdicts on the six UL rows against the pinned sources",
         f"""
Adversarially review the six planned UL rows. Token overlap is not entailment (QUALITY 81/90): read the
source and decide whether the row's **statement** is what the source says.

1. Re-open `{LANE}/{W}/before/src/` (or re-fetch at tag v262) and read each anchored region.
2. For each row UL1-UL6, write a verdict `holds | partly holds | fails`, the source line range you read,
   the quoted sentence, and — for `partly holds`/`fails` — the exact corrected sentence you would accept.
   Pay attention to: whether "overrides the same name" is stated for unit files only; whether drop-ins
   really "beat unit files wherever located" (read the man text, it says drop-in files under those
   directories take precedence); whether the reload condition is "path list differs OR newer mtime"
   (read `unit_need_daemon_reload`); whether masking is "empty file or /dev/null symlink" and whether the
   *highest-priority* path decides; whether `alias to a non-existent unit` is "ignored" at enable time
   and what the code actually does (`INSTALL_CHANGE_IS_DANGLING`).
3. Check the host claims independently: re-run `systemctl show -p DropInPaths -p FragmentPath -p
   LoadState user@1000.service getty@tty1.service` and `find /etc/systemd/system -maxdepth 1 -type l
   -lname /dev/null`. Report any delta from `before/host.txt`.
4. Name every statement that would be true of a different systemd version but is not established at
   v262 — the host runs 262.1-1-arch (an Arch build), and the sources are the upstream tag.

Write `{LANE}/{W}/w1/R1Reviewer/report.md` with a `| row | verdict | source line | reason |` table and a
final line `ROWS_HOLD=<n>/6`.
"""),
    item("R2Reviewer", "reviewer", ["freshness", "C2", "attack"],
         "attack the C2 routed repairs and the instrument-digest claim",
         f"""
Attack C2: is each routed defect real, and would the planned repair actually close it?

1. Re-derive the three defects at base `{BASE}`:
   - `git -C {LANE} show {BASE}:corpus/lessons/round-72.md | grep -n "No capability row enters this
     round\\|nine hermetic cases"` and the SCORECARD/LOG lines that supersede them;
   - `git -C {LANE} show {BASE}:SCORECARD.md | grep -n "df8a59c7\\|2610ff43"` — is the old digest frozen
     in the declaration and the tip tool different? Compute `sha256sum {LANE}/tools/check-r71-routed-r72.py`
     and compare with both;
   - the capability row text and the receipt `{LANE}/.ufo/waves/round-72/after/selftest-selftest-after.txt`
     — how many cases does the receipt actually report, and what does the row say?
2. Try to satisfy the frozen checker **without** doing the work: write fixture files under `$S` where the
   erratum block exists but denies the repair, where the correction quotes the superseded sentences only
   to say they were right, where the capability refresh says "ten" but names the wrong receipt. Score each
   with `python3 {LANE}/tools/check-r72-routed-r73.py --root $S/<case>` and report `held` (checker passes,
   so the defect is not really closed) or `survived`.
3. Judge the *direction* of the repair: a block that names the right tokens while contradicting them is the
   round-72 named limit. Say whether the drafted repair texts (ask the L1 for `E2Routed`'s draft, or draft
   your own) read as a correction to a reader, and quote the sentence that would fail that test.
4. Verify that the checker cannot be fed by the declaration's own quotation of a heading — the r72
   unanchored-regex defect — with a fixture whose only matching text sits inside a paragraph.

Write `{LANE}/{W}/w1/R2Reviewer/report.md` with the probe table, the two digest values you measured, and a
final `C2_CLOSABLE=yes|partly|no` line with reasons.
"""),
    item("K1Critic", "critic", ["calibration", "C1", "C2", "attack"],
         "critique the round-73 declaration: controls, channels, sizing, and which conjunct is unfalsifiable",
         f"""
Attack the declaration itself (`{LANE}/SCORECARD.md` heading `## Round 73 — declaration`, commit
`{DECL}`). Nine specific lines of attack; report D1..Dn with severity and the evidence.

1. **Held ground.** Is "the merge/precedence plane is unheld" true? Read every `drop-in` mention in
   `corpus/knowledge/` and say whether any states a rule C1 claims as new.
2. **Do-nothing control.** `{LANE}/{W}/before/absence-controls.txt`: could a do-nothing round reach the
   after-state? Name the cheapest fake that reaches `UL_ROWS=6 ... met=1` without reading a source — and
   then say which frozen clause stops it.
3. **Counter channels.** Which clause is lexical only? Construct a row whose statement negates its
   snapshot and keeps the vocabulary, score it with the frozen counter, and report `met`.
4. **Selftest integrity.** `--selftest` copies the committed snapshots. Can a replacement counter that
   prints the expected lines fake its own verdict? Which committed artefact would catch it and which
   would not?
5. **Instrument-change rule.** The declaration pre-commits to re-running the before control with the final
   instrument. Is that enough to make before/after same-instrument evidence, and what is still missing
   (name the receipt that must exist)?
6. **Claim sizing.** Is C2's predicate one concrete value a closure can re-derive with one command? Is
   C1's after-state sized to what one round can land? Name any universal clause that is not enumerated.
7. **Separability.** Show a concrete scenario where C2 verifies while C1 has not landed, and vice versa.
8. **Sources rejection.** The round promises one refused candidate for R72-GATE-NO-REJECT. Is a refusal
   of a duplicate/render/summary source a real exercise of the gate's taste, or a rubber stamp? Say what a
   real rejection would look like here.
9. **Fabrication risk.** Where could this round's receipts be fabricated wholesale, and which command
   would a non-author run to catch it?

Write `{LANE}/{W}/w1/K1Critic/report.md`, each defect with `severity: high|medium|low`, the command, the
output, and the fix. A defect you cannot demonstrate is `opinion`, not a finding.
"""),
    item("M1Mutation", "mutation-tester", ["operability", "C1", "C2", "mutation"],
         "clause-isolated mutant batteries against both frozen instruments",
         f"""
Mutation-test both frozen instruments and report the kill matrix.

1. `count-ul-rows-r73.py`: copy it into `$S` (never edit the lane file). Produce one mutant per frozen
   clause by disabling exactly that check (id contiguity, statement words, grounding, source kind,
   digest, map binding, anchor binding, quote location, quote length, snapshot reuse, malformed-row
   counting, target arithmetic). Score each mutant against the committed selftest and against a fixture
   mirror that only that clause can reject. Report `killed | survived` per mutant with the command.
2. `check-r72-routed-r73.py`: the same for its required tokens (each of the six lesson tokens, the two
   digests, the receipt path, the capability tokens) and for the block-heading anchor. Report survivors.
3. For each survivor, state the class (`clause not exercised by the selftest`, `fixture shares one
   literal shape`, `answer-key readable`, …) and what fixture would kill it.
4. Score the committed selftest suites themselves: how many cases assert a *named finding id* versus only
   an exit code? A case that asserts only rc is weaker; count them.

Write `{LANE}/{W}/w1/M1Mutation/report.md` with the two matrices (`| mutant | clause | verdict |`) and a
final `SURVIVORS=<n> classes=<list>` line.
"""),
]

spec = {
    "wave": "w1",
    "reportDir": f"{W}/w1",
    "maxLanes": 256,
    "context": CONTEXT,
    "items": items,
}

path = pathlib.Path(f"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/{W}/w1-spec.json")
path.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print(path, "items:", len(items), "roles:", {i["role"] for i in items})
print("attack seats:", sum(1 for i in items if i["role"] in {"reviewer", "critic", "mutation-tester", "labrat"}),
      "of", len(items))
