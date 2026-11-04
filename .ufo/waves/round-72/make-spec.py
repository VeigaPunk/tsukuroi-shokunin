#!/usr/bin/env python3
"""Build .ufo/waves/round-72/w1-spec.json — tsukuroi round 72, one v1 wave (band 8-16, 12 seats).

Deterministic: same inputs -> same spec. Run from anywhere:
    python3 .ufo/waves/round-72/make-spec.py
"""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
DECL = "6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e"
GODSPEED = (
    "/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n"
    "2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large "
    "batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or "
    "verbose plans. Act directly via tool calls.\n\n"
)

CONTEXT = GODSPEED + f"""You are an L2 seat of tsukuroi lane round 72 (hyaku run 15), wave w1 — the round's ONLY wave (v1 band 8-16, 12 seats). Host: canonical Linux/omp host (Arch). Lane: {LANE}. Declaration commit (frozen before data): {DECL}. Read SCORECARD.md "Round 72 — declaration" at that commit; the predicates there are frozen — never reinterpret, never amend, never substitute a counter of your own.

YOUR WRITE SCOPE (hard): only {LANE}/.ufo/waves/round-72/w1/<YourSeatName>/ and {LANE}/.ufo/waves/round-72/probes/<YourSeatName>/ (create your own subdirectory). Never write, stage, commit or push in {LANE} (the lane tree), the fleet repo /home/vgpnk/Projects/shokunin, any sibling lane, /home/vgpnk/Projects/shokuknow, .ufo/state, .scratch, MANIFEST.json or .ufo/watchdog.log. Never run mutating git/jj commands anywhere; a sandbox read-only copy is created only as `git clone --shared {LANE} <scratch>/clone` and every git call names `-C <scratch>/clone`. The L1 is the only writer of the lane tree and the only one who commits.

SCRATCH: S=/fast/scratch/hyaku/tsukuroi-r72/<YourSeatName>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT (or python finally). Never use /tmp for anything over 50 MB; delete your tree before you yield and report if you could not. A tool that writes under /tmp regardless of TMPDIR is a defect you must report.

EVERY PATH IS ABSOLUTE. Every `Report:` trailer path the validator renders is relative to {LANE} — write it at {LANE}/<that path>. Never message agent://all; you are a leaf: no delegation, no background jobs, no sub-swarm. Finish inside ~25 minutes of work.

TOOLING (operator authorization 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file no install at all. Never run pacman -S/-Sy/-Syu/-U/-R. Never restart a host service.

READ-ONLY HOST: no writes to /sys, /proc, /etc, /boot, package state, service state, module parameters, or modprobe.d config files; `sudo -n` is allowed only for read-only queries your item names; never `sudo` interactively. Reading the CONTENT of /etc/modprobe.d or /usr/lib/modprobe.d files is out of bounds this round (the lane records paths and modes only); `modprobe --showconfig` is therefore also out of bounds.

BOUNDARY: the lane is read-only detection and report. Secrets are shape-only (never read or echo key material, tokens, session bytes). Host serials, WWIDs and hostnames beyond the fixture host name are not needed.

CLAIM CONTEXT — FROZEN in SCORECARD.md "Round 72 — declaration":
- C1 depth (lowest non-retired, 8 tied with adjacency; SOURCED — planned registry rows S301/S302/S303): the note `corpus/knowledge/modprobe-config-plane-r72.md` carries exactly six rule rows MD1-MD6. Row grammar (one physical line, exactly 7 pipe cells, no pipe inside a cell, no double quote inside the quote cell): `| MD<n> | <statement >= 12 words> | source=S### | snapshot=<file> | digest=<64 lowercase hex> | quote="<verbatim text from that snapshot, <= 25 words, no double quote>" |`. The frozen counter `tools/count-md-rows-r72.py` (sha256 d615c653f32a29af3a4355d882041b8543ff56882b3225f7e3eedf173d8706a6) requires per row: unique contiguous id; statement >= 12 words; >= 6 distinct non-stopword tokens (len >= 4) shared with the row's snapshot text AND shared/total >= 0.5; `source=` a registry id at the same revision whose `kind` is a source kind and not own-work; snapshot exists under .ufo/waves/round-72/before/src with sha256 == digest; digest equals the map digest in src/SOURCES.json AND that map URL appears in the registry row's source cell; the registry anchor cell contains the snapshot basename; quote <= 25 words and located verbatim (whitespace-normalized). Any MD-shaped line that does not parse is a malformed-row finding. No snapshot may be cited more than twice. Target: rows == 6 and verified == 6 and distinct sources >= 3 and distinct snapshots >= 3.
- Committed snapshots (read them; never re-write them): {LANE}/.ufo/waves/round-72/before/src/{{modprobe.d.5.scd, libkmod-config.c, modprobe.c}} with SHA256SUMS and SOURCES.json (kmod v34; host kmod 34.2). Digests: modprobe.d.5.scd aa1a869e57db31c8187a436b5eab3047394da5fd779794e1cdd4ccad598ee46e; libkmod-config.c ae520a0721aad0bc61c7b13369fccf8e46fc408d8c0884fda9260a05da7ceb11; modprobe.c 1e8e352634026e6618f37c0aee9974cf51427bfa3a77d12bcd2220ea8a71bf3f. URLs are in src/SOURCES.json (git.kernel.org plain at h=v34). Planned registry ids: S301 = man/modprobe.d.5.scd, S302 = libkmod/libkmod-config.c, S303 = tools/modprobe.c.
- The six planned propositions: MD1 directory precedence (SYNOPSIS order; first file of a name suppresses the same name later); MD2 lexicographic ordering across all directories with partial replacement by a later-ordered file; MD3 libkmod rejects a duplicate filename at sorted insertion so only one copy is parsed; MD4 the kernel command line is parsed into the same config object after the files; MD5 dry-run prints the plan and executes nothing; MD6 blacklist is alias-only by default and unconditional only with --use-blacklist.
- C2 operability (9; capability `gate-selftest`): `tools/check-selftest-tally.py` gains a `--selftest` mode building every fixture under $TMPDIR, printing `SELFTEST: PASS (N cases, N passed, 0 failed)` with one named case line each, exit 0; >= 7 hermetic cases (matching figure; mismatched figure with a stable finding id; wrong label count; superseded-figure quote skip; out-of-scope battery figure; receipt with no PASS line -> rc 2). Before: rc 2, 0 case lines. Existing r70 self-demo verdict must not change (`added_figures_mismatched=0 receipt_cases=214 receipt_labels=18`, rc 0).
- C3 freshness (9): the r71 routed defects close in committed bytes — `.ufo/waves/round-71/after/count-mp-rows-final.txt` equals a fresh run of `tools/count-mp-rows-r71.py --revision 2b358d2d`; a SCORECARD `## Round 71 — receipt erratum` block names that receipt and revision; an appended correction in `corpus/knowledge/module-parameter-plane-r71.md` names R71-NOTE-MODPROBE-COUNT, the five /usr/lib/modprobe.d paths and the superseded four figure. Checker `tools/check-r71-routed-r72.py` (sha256 df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712); at base ROUTED_STALE=3 rc 1.
- Host facts (read-only capture {LANE}/.ufo/waves/round-72/before/host.txt): kernel 7.2.11-arch1-1; kmod 34.2; /etc/modprobe.d 3 names; /usr/lib/modprobe.d 5 names (README + 4 .conf); /run/modprobe.d and /usr/local/lib/modprobe.d absent; /lib resolves to /usr/lib so /lib/modprobe.d and /usr/lib/modprobe.d are one directory; /proc/cmdline carries no module.parameter token; 136 /sys/module/*/parameters dirs.
- Pre-data receipts: {LANE}/.ufo/waves/round-72/before/ (absence-controls.txt, novelty-sweep.txt, control/battery.txt 11/11, control/routed-battery.txt 5/5, src/SHA256SUMS).

ASSIMILATION: none this round (L0 tsukuroi | round-64 open and unanswered). Do not read or use /home/vgpnk/Projects/shokuknow/merge/tsukuroi/.
MISROOT GUARD: a relative path can land in the fleet repo; always name the absolute lane path.

YOUR FINAL MESSAGE: at most 12 lines — one line per receipt/draft path you wrote, then the KEY=VALUE results your item asks for. No narrative.
"""

ITEMS = [
    dict(
        name="S1Scout", role="scout", axes=["depth", "C1", "sources"],
        milestone="C1 source re-open by a second route, quote locations, host re-capture",
        task="""Independently re-open all three C1 sources and prove the committed snapshots are the upstream bytes.
1. S=/fast/scratch/hyaku/tsukuroi-r72/S1Scout; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. For each of modprobe.d.5.scd, libkmod-config.c, modprobe.c: fetch the URL in {lane}/.ufo/waves/round-72/before/src/SOURCES.json by a route OTHER than git.kernel.org's plain endpoint (e.g. raw.githubusercontent.com/kmod-project/kmod/v34/<path>), sha256 it, and compare with the committed snapshot and the map digest. Record ROUTE2_OK=<n>/3 and every mismatch.
3. Locate, with line numbers, six exact quotes the planned rows may carry: (a) modprobe.d.5.scd precedence sentence "Once a file of a given filename is loaded ..."; (b) the lexicographic-sort sentence; (c) libkmod-config.c `Ignoring duplicate config file`; (d) libkmod-config.c `kmod_config_parse_kcmdline(config);`; (e) modprobe.c dry-run usage line `Do not execute operations, just print out`; (f) modprobe.c `Apply blacklist to resolved alias.` and the `APPLY_BLACKLIST_ALIAS_ONLY` assignment. Flag any quote that is not verbatim, contains a pipe or a double quote, or exceeds 25 words.
4. Re-capture the host facts read-only (paths and modes only, never config contents, never `modprobe --showconfig`): kernel, kmod version, the five modprobe.d paths with modes, /lib resolution, /proc/cmdline, count of /sys/module/*/parameters.
5. Write {lane}/.ufo/waves/round-72/probes/S1Scout/{{route2.txt,quotes.tsv,host-enum.txt}} and a short .md report.
KEY=VALUE: ROUTE2_OK=, QUOTES_LOCATED=, PIPES_OR_QUOTES=, HOST_DRIFT=""".replace("{lane}", LANE)),
    dict(
        name="E1Mirror", role="executor", axes=["depth", "C1", "counter"],
        milestone="independent mirror harness: fixture note, counter run, independent reader",
        task="""Independently exercise the frozen C1 counter and build an independent reader.
1. S=/fast/scratch/hyaku/tsukuroi-r72/E1Mirror; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Build a fixture mirror under $S/mirror the way {lane}/.ufo/waves/round-72/before/control/battery.py does (copy the three snapshots and SOURCES.json from {lane}/.ufo/waves/round-72/before/src, write a corpus/SOURCES.md with S301-S303 and a six-row note). Run `python3 {lane}/tools/count-md-rows-r72.py --fixture $S/mirror` and record the exact output. Iterate your own fixture wording until it prints met=1; do not modify the counter.
3. Write an INDEPENDENT reader ($S/reader.py) that parses MD rows from a note by its own logic (not importing the counter) and checks: row count, id contiguity, quote located in the named snapshot (whitespace-normalized), digest == sha256 of the snapshot file, source id present in the registry, registry source cell contains the map URL, anchor cell contains the basename. Run it on your fixture and on a fixture where one quote is edited to a sentence from a DIFFERENT snapshot; it must read ok rows 6 / 6 and then 5 / 6.
4. Report every case where your reader and the counter disagree on the same input (row by row), and every clause the counter checks that your reader cannot.
5. Write {lane}/.ufo/waves/round-72/w1/E1Mirror/{{counter-run.txt,reader.py,reader-runs.txt}} and a short .md report.
KEY=VALUE: COUNTER_MET=, ROWS_OK=, READER_RED=, DISAGREEMENTS=""".replace("{lane}", LANE)),
    dict(
        name="E2GateSelftest", role="executor", axes=["operability", "C2", "gate"],
        milestone="C2 --selftest mode draft with hermetic fixtures and a red-before mutant",
        task="""Draft the C2 `--selftest` mode as a patch against {lane}/tools/check-selftest-tally.py. You are the only writer of this draft; the L1 applies it.
1. S=/fast/scratch/hyaku/tsukuroi-r72/E2GateSelftest; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Copy the tool into $S and work on the copy only.
2. Add a `--selftest` flag that: creates one temp root under $TMPDIR (honour TMPDIR; never hardcode /tmp), writes its own receipt/diff fixtures, runs the checker's core over them, and prints one line per case named `PASS (SELFTEST-<id>)` or `FAIL (SELFTEST-<id>)` plus a final `SELFTEST: PASS (N cases, N passed, 0 failed)`; exit 0 only when every case passes. Stable finding ids for mismatches (e.g. `SWEEP-MISMATCH`, `SWEEP-LABEL`, `SWEEP-NO-RECEIPT`).
3. Cases (>= 7): (a) added figure == receipt -> rc 0; (b) added figure != receipt -> mismatch with file:line; (c) label count wrong -> mismatch; (d) a line quoting a superseded figure -> SKIP, rc 0; (e) an out-of-scope battery figure ("11 cases") -> not scored; (f) receipt without a `PASS (N cases, ...)` line -> rc 2; (g) a green diff that names the census selftest -> pass.
4. Prove the suite able to fail: make a mutant copy where the mismatch branch is disabled; `--selftest` on it must exit non-zero with a named failing case. Save that receipt.
5. Prove the existing behaviour is unchanged: `python3 <copy> --receipt {lane}/.ufo/waves/round-70/after/selftest-after.txt --label R70-C2 --range 4035c1a0..40c35ee7 -- SCORECARD.md PROVINCE.md corpus/README.md SKILL.md` still reads `added_figures_mismatched=0 receipt_cases=214 receipt_labels=18` rc 0 (run it from the lane root, read-only).
6. Write {lane}/.ufo/waves/round-72/w1/E2GateSelftest/{{selftest.patch,selftest-after.txt,redbefore.txt}} and a short .md report naming every touched function and line range.
KEY=VALUE: PATCH_LINES=, CASES=, SELFTEST_RC=, REDBEFORE_RC=, SELFDEMO_RC=""".replace("{lane}", LANE)),
    dict(
        name="E3Routed", role="executor", axes=["freshness", "C3", "receipts"],
        milestone="C3 receipt re-derivation, erratum/correction drafts, tamper probes",
        task="""Prepare the C3 repairs against a scratch copy and attack the checker.
1. S=/fast/scratch/hyaku/tsukuroi-r72/E3Routed; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Run `python3 {lane}/tools/count-mp-rows-r71.py --revision 2b358d2d` from the lane root and save its full output. Draft the receipt file content ($S/count-mp-rows-final.txt) with the command line and the two summary lines exactly as printed.
3. Draft the SCORECARD erratum block text ($S/erratum.md) naming `.ufo/waves/round-71/after/count-mp-rows-final.txt` and revision `2b358d2d`, and the appended note correction text ($S/note-correction.md) naming R71-NOTE-MODPROBE-COUNT, the five `/usr/lib/modprobe.d` paths from {lane}/.ufo/waves/round-71/before/host.txt, and the superseded four-path figure.
4. Build a scratch mirror of the lane's three artefacts (receipt, SCORECARD block, corrected note) and run `python3 {lane}/tools/check-r71-routed-r72.py --fixture $S/mirror`; it must read ROUTED_STALE=0 rc 0. Then tamper the receipt summary (change one number) and show it reads ROUTED_STALE=1 rc 1.
5. Adversarial probes against the checker, each recorded: (i) a receipt whose lines are copied but whose revision is fabricated; (ii) an erratum block that names the receipt inside a sentence with no revision; (iii) a note correction that mentions five but not the defect id; (iv) a fixture where the receipt text is correct but the counter's real run differs (mutate one MP row in a shared clone). For each: does the checker catch it? Report false passes.
6. Write {lane}/.ufo/waves/round-72/w1/E3Routed/{{count-mp-rows-final.txt,erratum.md,note-correction.md,tamper-probes.txt}} and a short .md report.
KEY=VALUE: RECEIPT_LINES=, FIXTURE_STALE=, TAMPER_CAUGHT=, FALSE_PASSES=""".replace("{lane}", LANE)),
    dict(
        name="SC1Entry", role="scribe", axes=["depth", "C1", "knowledge"],
        milestone="C1 knowledge note draft MD1-MD6 against the frozen counter",
        task="""Draft the C1 knowledge entry at {lane}/.ufo/waves/round-72/w1/SC1Entry/modprobe-config-plane-r72.md.
1. S=/fast/scratch/hyaku/tsukuroi-r72/SC1Entry; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Open the three committed snapshots and read the cited regions. Write the entry with the provenance trio (`source:`, `verified-at:`, `recheck:`) then exactly six rule rows MD1-MD6, one physical line each, 7 pipe cells, no pipe or double quote inside a cell, following the grammar in the context above. Each statement >= 12 words and worded from the snapshot's own vocabulary; each quote verbatim, <= 25 words, located in the named snapshot.
3. Iterate against a fixture mirror: copy {lane}/.ufo/waves/round-72/before/control/battery.py's shape, replace the note with your draft, run `python3 {lane}/tools/count-md-rows-r72.py --fixture $S/mirror` until it prints `MD_VERIFIED=6 ... met=1` rc 0. Do not touch the counter.
4. Add a `## Decision table` mapping an observed host shape to a verdict and an operator action: /lib/modprobe.d and /usr/lib/modprobe.d resolve to one directory; /run/modprobe.d absent; a duplicate .conf name in /etc and /usr/lib; an `install` line; `blacklist` plus an explicit module name; `-b` on an alias. Mark each row's evidence.
5. Add a `## Limits` naming the lexical-substance channel (the counter checks grounding, not entailment) and that file contents were never read on this host.
6. Write {lane}/.ufo/waves/round-72/w1/SC1Entry/{{modprobe-config-plane-r72.md,counter-run.txt}} and a short .md report.
KEY=VALUE: ROWS=, COUNTER_MET=, QUOTES_LOCATED=, TABLE_ROWS=""".replace("{lane}", LANE)),
    dict(
        name="SC2Sources", role="scribe", axes=["depth", "C1", "sources"],
        milestone="S301-S303 registry rows, search log, leads update",
        task="""Draft the three C1 registry rows and the SOURCES.md prose.
1. S=/fast/scratch/hyaku/tsukuroi-r72/SC2Sources; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Read the current registry's S297-S300 rows (the shape to match) and the r71 search-log/leads entries.
2. Write {lane}/.ufo/waves/round-72/w1/SC2Sources/rows.md with S301 (man/modprobe.d.5.scd), S302 (libkmod/libkmod-config.c), S303 (tools/modprobe.c): 11 cells, no pipe inside a cell; kind docs/code/code, tier A, a scoped `scope` cell, an `anchor` cell naming the tag v34 AND the snapshot basename AND the line ranges, a one-benefit `teaches` cell, status `mined`, opened 2026-11-03, recheck `on-release`, used-by corpus/knowledge/modprobe-config-plane-r72.md.
3. For each row give the exact URL from {lane}/.ufo/waves/round-72/before/src/SOURCES.json and a <= 25-word located quote in a `## Gate quotes` section (URL, access date 2026-11-03, quote, line).
4. Draft `## Search log` (question, where searched, date 2026-11-03, identified/screened/included/excluded counts, exclusion reasons, stop rationale) and the `## Leads (unopened)` line that closes the r71 lead (kmod man page reached at `man/modprobe.d.5.scd`, opened this round; what remains unopened: kmod's `libkmod-config.c` config-path priority table in `libkmod.c`).
5. Write {lane}/.ufo/waves/round-72/w1/SC2Sources/{{rows.md,search-log.md,leads.md}} and a short .md report.
KEY=VALUE: ROWS=3, CELLS=11, QUOTES=3, SEARCH_LOG=yes""".replace("{lane}", LANE)),
    dict(
        name="SC3Index", role="scribe", axes=["coverage", "C1", "index"],
        milestone="PROVINCE/README/SKILL index drafts",
        task="""Draft the index and province text for the new plane (drafts only; the L1 lands them).
1. S=/fast/scratch/hyaku/tsukuroi-r72/SC3Index; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Draft {lane}/.ufo/waves/round-72/w1/SC3Index/province.md: a paragraph saying what is Core now (reading the modprobe configuration surface — which directories exist, their precedence, how a name is resolved and what a blacklist refuses), what stays operator-owned (editing any modprobe.d file, loading/unloading modules, changing blacklists), and what is explicitly NOT claimed (no config-content reading on this host, no module internals, no RE).
3. Draft {lane}/.ufo/waves/round-72/w1/SC3Index/readme-row.md: a `## Round 72` coverage-map row naming the note and S301-S303, plus a frontier sentence.
4. Draft {lane}/.ufo/waves/round-72/w1/SC3Index/skill-table.md: a decision table with >= 6 rows mapping an observed modprobe.d shape to a verdict and an operator action (duplicate .conf name across dirs; /lib and /usr/lib same directory; install command present; blacklist plus explicit module name; softdep; dry-run plan), each citing the note row (MD1-MD6).
5. Draft {lane}/.ufo/waves/round-72/w1/SC3Index/selftest-tally-row.md: the SKILL registry row update for `selftest-tally` replacing the self-demo column with `python3 tools/check-selftest-tally.py --selftest` and its exit map (0 all cases pass, 1 a case fails, 2 usage), for the L1 to land append-only.
6. Write the four drafts and a short .md report.
KEY=VALUE: TABLE_ROWS=, CITED_IDS=, WRITE_CLAIMS=0""".replace("{lane}", LANE)),
    dict(
        name="C1Connector", role="connector", axes=["adjacency", "C1", "overlap"],
        milestone="sibling-overlap scan for the modprobe/kernel-module config ground",
        task="""Scan for sibling-lane overlap with the new modprobe configuration ground.
1. S=/fast/scratch/hyaku/tsukuroi-r72/C1Connector; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read {lane}/PROVINCE.md ADJ-01..07 and the round-49/Round-66 anchor registers; then read (read-only) the sibling repos' PROVINCE.md/SKILL.md under /home/vgpnk/Projects/shokunin/*-shokunin/ for these terms: modprobe, modprobe.d, module load, blacklist, softdep, kernel module parameters, kmod.
3. Build a table: sibling lane | surface it claims | the exact line (path:line, <= 25-word quote) | overlap class (owned / adjacent / contested / none) | who should own the new plane.
4. Answer the specific question: does any lane claim module loading or modprobe configuration as its ground, and does this round's Core statement absorb it? If contested, say what the integrator should arbitrate; never absorb.
5. Also check the fleet-root `merge/tsukuroi/` index (read-only, no adoption; assimilation is closed this round) for a staged entry that names this surface, and record its id only.
6. Write {lane}/.ufo/waves/round-72/probes/C1Connector/{{overlap.tsv,report.md}}.
KEY=VALUE: LANES_SCANNED=, CONTESTED=, ABSORBED=0, STAGED_IDS=""".replace("{lane}", LANE)),
    dict(
        name="R1Reviewer", role="reviewer", axes=["depth", "C1", "attack"],
        milestone="semantic attack on C1 rows and counter channels",
        task="""Attack C1: re-derive every row and falsify its statement against the bytes.
1. S=/fast/scratch/hyaku/tsukuroi-r72/R1Reviewer; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read the SC1Entry draft (in {lane}/.ufo/waves/round-72/w1/SC1Entry/ if present; otherwise the note at the declaration's target path). For each MD row: quote the exact snapshot lines it cites, and judge whether the statement ENTAILS from them. Flag overreach (a sentence the bytes do not support), stale line anchors, a quote that is not verbatim, and any statement that is true of the man page but not of the implementation (or vice versa).
3. Re-run the frozen counter against a fixture mirror of the draft and report its exact output. Build 4 counter-channel probes of your own (e.g. a statement that negates its snapshot but keeps the vocabulary; a row whose quote lies in a different snapshot; a registry row with kind `community` at tier A; a note with an MD9 hidden in a fenced block) and record which the counter catches and which it does not.
4. Check host applicability of each row against {lane}/.ufo/waves/round-72/before/host.txt: which rows have a consequence on THIS host (e.g. /lib and /usr/lib one directory; the three /etc names; no /run/modprobe.d) and which are inert here.
5. Write {lane}/.ufo/waves/round-72/w1/R1Reviewer/{{review.md,verdicts.tsv,channels.txt}} with one verdict per row (`holds` / `partly` / `fails`) and a named correction for each `partly`/`fails`.
KEY=VALUE: ROWS_REVIEWED=, HOLDS=, PARTLY=, FAILS=, COUNTER_CHANNELS_UNCAUGHT=""".replace("{lane}", LANE)),
    dict(
        name="R2Reviewer", role="reviewer", axes=["operability", "C2", "attack"],
        milestone="attack the --selftest design and the routed checker",
        task="""Attack C2 and C3.
1. S=/fast/scratch/hyaku/tsukuroi-r72/R2Reviewer; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. C2: read the E2GateSelftest patch/draft (in {lane}/.ufo/waves/round-72/w1/E2GateSelftest/ if present; otherwise {lane}/tools/check-selftest-tally.py). Check that every case can fail for the reason it names (disable each branch and see which case notices), that the fixture root honours TMPDIR, that no case writes under /tmp, that the exit map (0/1/2) is exactly as declared, and that the existing r70 self-demo verdict is unchanged. Report cases that pass vacuously.
3. C3: attack {lane}/tools/check-r71-routed-r72.py. Try to make it print ROUTED_STALE=0 without doing the claimed work: a fabricated receipt with a plausible summary, an erratum block that names the receipt and revision but is not an erratum, a note correction that says five without the defect id. Then try to make it FAIL on a correct repair. Record each attempt and the observed verdict.
4. Also verify the r71 receipt re-derivation is real: change one byte in a scratch copy of `tools/count-mp-rows-r71.py` and show the fixture path still compares against the lane counter (i.e. a fixture cannot fake the re-derivation).
5. Write {lane}/.ufo/waves/round-72/w1/R2Reviewer/{{attacks.txt,findings.md}}.
KEY=VALUE: C2_VACUOUS_CASES=, C2_TMPDIR_LEAK=, C3_FALSE_PASSES=, C3_FALSE_FAILS=""".replace("{lane}", LANE)),
    dict(
        name="K1Critic", role="critic", axes=["calibration", "claims", "attack"],
        milestone="falsify the declaration's claims and every frozen predicate",
        task="""Falsify the round-72 declaration.
1. S=/fast/scratch/hyaku/tsukuroi-r72/K1Critic; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Read SCORECARD.md "Round 72 — declaration" (commit 6b42676) and every receipt it names under {lane}/.ufo/waves/round-72/before/.
2. For each of the three claims: enumerate every conjunct of the frozen predicate, name the command that measures it, and state whether the declaration's prose overclaims relative to the committed receipts. Check literal counts (battery cases, digests, row counts, note counts) against the files.
3. Check the do-nothing controls: does any claim's target survive a do-nothing control (e.g. would an empty note or a fabricated receipt reach the target)? Run the cheapest control you can and record its score.
4. Check causal separability and axis distinctness; check that at least one claim works the lowest non-retired axis and that the stagnation-window arithmetic (capabilities at r70 and r71 -> 2 of 3) is right against SCORECARD's capabilities tables.
5. Name every D-item (defect) with severity and the exact correction, and every place where the declaration should be amended append-only (never silently).
6. Write {lane}/.ufo/waves/round-72/w1/K1Critic/{{critique.md,controls.txt}}.
KEY=VALUE: CLAIMS=3, OVERCLAIMS=, CONTROL_REACHES=, D_ITEMS=""".replace("{lane}", LANE)),
    dict(
        name="M1Mutation", role="mutation-tester", axes=["calibration", "C1", "mutation"],
        milestone="mutation-test the C1 counter, the C3 checker and the C2 cases",
        task="""Mutation-test the round's three instruments.
1. S=/fast/scratch/hyaku/tsukuroi-r72/M1Mutation; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. C1 counter ({lane}/tools/count-md-rows-r72.py): copy it and build >= 8 source-level mutants, each removing or weakening ONE frozen clause (grounding share, token count, kind-not-own-work, map-digest, source-anchor binding, quote location, malformed-row finding, snapshot reuse). Score each mutant against (i) the well-formed control fixture and (ii) the matching bad fixture; a mutant is KILLED when the bad fixture still reads met=0 rc 1 or the control stops reading met=1. Report survivors and whether the committed battery catches them.
3. C3 checker ({lane}/tools/check-r71-routed-r72.py): >= 5 mutants (drop the re-derivation equality, accept a receipt without the revision, accept an erratum with the receipt only, drop the five-path check, accept a correction outside an appended section). Same kill rule.
4. C2 (if the draft exists): remove one case at a time from the draft's selftest and report which removal the suite itself notices.
5. Write {lane}/.ufo/waves/round-72/probes/M1Mutation/{{mutants.tsv,score.md}}.
KEY=VALUE: C1_MUTANTS=, C1_KILLED=, C3_MUTANTS=, C3_KILLED=, C2_BLIND=""".replace("{lane}", LANE)),
]


def main():
    spec = {
        "wave": "w1",
        "reportDir": ".ufo/waves/round-72/w1",
        "maxLanes": 256,
        "context": CONTEXT,
        "items": [
            {
                "name": it["name"], "role": it["role"], "axes": it["axes"],
                "milestone": it["milestone"], "item": it["name"],
                "prompt": GODSPEED + it["task"],
            }
            for it in ITEMS
        ],
    }
    out = Path(__file__).with_name("w1-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(f"wrote {out} items={len(spec['items'])} context={len(spec['context'])}")


if __name__ == "__main__":
    main()
