#!/usr/bin/env python3
"""R2Reviewer (round-74 w1) attack battery against the frozen C2 instrument
tools/check-r73-routed-r74.py. Mutant DRAFT fixtures run through
evaluate(fixture_texts=...) — no repo bytes are touched.

Each case records expected vs got. MISMATCH rows are checker surprises.
"""
import importlib.util
import pathlib

REPO = pathlib.Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
spec = importlib.util.spec_from_file_location("chk", REPO / "tools/check-r73-routed-r74.py")
chk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chk)

LESSON = "corpus/lessons/round-73.md"
LOG = "LOG.md"
lesson_tip = (REPO / "corpus/lessons/round-73.md").read_text()
log_tip = (REPO / LOG).read_text()

R73_HEAD = "## Round 73 (2026-11-03) — the systemd unit-load merge plane, and three r72 routed repairs"
assert log_tip.count(R73_HEAD) == 1, "R73 log heading anchor not unique"

GOOD_LESSON_BLOCK = (
    "## Round 73 — correction (R73-GATE-QUOTE-LINE-DRIFT) (round-74 append)\n"
    "In the Gate table the S306 quote sits at install.c:2383, superseding the recorded install.c:2387;\n"
    "the S304 anchors are corrected to :368-370 (superseding :367-370), :237-238 (superseding :236-238)\n"
    "and :238-239 (superseding :238-240).\n")

GOOD_LOG_BLOCK = (
    "## Round 73 — correction (R73-LOG-COUNT-STALE) (round-74 append)\n"
    "The Round 73 entry above cited superseded mid-wave counts: a twelfth selftest case (12) and\n"
    "eleven cases (11). The final committed instruments carry 13 cases (tools/count-ul-rows-r73.py,\n"
    "sha256 1f22c26b…) and 14 cases (tools/check-r72-routed-r73.py, sha256 ad853877…).\n")

# LOG variant that passes item 2 (correction block inserted BEFORE the R73 entry block)
log_pass = log_tip.replace(R73_HEAD, GOOD_LOG_BLOCK + "\n" + R73_HEAD, 1)

cases = []  # (name, exp_stale, exp_ok, lesson_text, log_text)

def case(name, exp_stale, exp_ok, lesson, log):
    cases.append((name, exp_stale, exp_ok, {LESSON: lesson, LOG: log}))

# ---------- item 1: lesson gate-quote correction ----------
case("L0-control-append", 0, 2, lesson_tip + "\n" + GOOD_LESSON_BLOCK, log_pass)

case("L1-omit-install.c:2383", 1, 1, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "The S306 quote stands at install.c:2387 as recorded; the S304 anchors read :368-370, :237-238 and :238-239.\n",
     log_pass)

case("L2-omit-2387-superseded", 1, 1, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "The S306 quote sits at install.c:2383; the S304 anchors read :368-370, :237-238 and :238-239.\n",
     log_pass)

case("L3-omit-third-S304-anchor", 1, 1, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "The S306 quote sits at install.c:2383 superseding install.c:2387; the S304 anchors read :368-370 and :237-238.\n",
     log_pass)

case("L4-omit-all-S304-anchors", 1, 1, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "The S306 quote sits at install.c:2383 superseding install.c:2387.\n",
     log_pass)

case("L5-substring-drift-wrong-numbers", 0, 2, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "The S306 quote sits at install.c:23831, superseding 12387; the S304 anchors are :368-3700, :237-2380 and :238-2390.\n",
     log_pass)

case("L6-denial-inversion", 0, 2, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "This proposed correction is REJECTED after re-measure: install.c:2383, install.c:2387, :368-370, :237-238\n"
     "and :238-239 were all misread by the spot-check; the Gate quotes stand exactly as originally recorded.\n",
     log_pass)

case("L7-id-tokens-in-unrelated-block", 0, 2,
     lesson_tip.replace("## Gate\n",
                        "## Gate\n"
                        "Tracked routed defect R73-GATE-QUOTE-LINE-DRIFT (install.c:2383 supersedes 2387;\n"
                        ":368-370, :237-238, :238-239) is recorded in this section, no correction appended.\n", 1),
     log_pass)

case("L8-shadow-first-id-block-no-tokens", 1, 1,
     lesson_tip.replace("## Gate\n", "## Gate\nTracked routed defect: R73-GATE-QUOTE-LINE-DRIFT — see the correction below.\n", 1)
     + "\n" + GOOD_LESSON_BLOCK,
     log_pass)

case("L10-bare-token-list-no-sentence", 0, 2, lesson_tip + "\n" +
     "## Correction (R73-GATE-QUOTE-LINE-DRIFT)\n"
     "install.c:2383, 2387, :368-370, :237-238, :238-239\n",
     log_pass)

# ---------- item 2: LOG count correction ----------
lesson_pass = lesson_tip + "\n" + GOOD_LESSON_BLOCK

case("G1-append-at-EOF (spot-check's stated shape)", 1, 1, lesson_pass, log_tip + "\n" + GOOD_LOG_BLOCK)

case("G2-insert-before-R73-entry", 0, 2, lesson_pass, log_pass)

case("G3-in-block-paragraph-append", 0, 2, lesson_pass,
     log_tip + "\nCorrection (R73-LOG-COUNT-STALE): the twelfth/eleven (12/11) figures above are superseded;\n"
     "the final committed instruments carry 13 and 14 cases.\n")

case("G4-id-less-fallback-block", 0, 2, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (selftest counts)\n"
                     "The selftest counts 12 (twelfth case) and 11 (eleven cases) cited above are superseded;\n"
                     "the final committed counts are 13 and 14 cases.\n\n" + R73_HEAD, 1))

case("G5-finals-as-substring-1314", 0, 2, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (R73-LOG-COUNT-STALE)\n"
                     "The final committed instruments read 1314 cases combined; the twelfth and eleven figures\n"
                     "cited above are stale.\n\n" + R73_HEAD, 1))

case("G6-direction-inversion", 0, 2, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (R73-LOG-COUNT-STALE)\n"
                     "Re-measure shows the final committed counts are 12 and 11; the mid-wave figures 13 and 14\n"
                     "were wrong and stand superseded.\n\n" + R73_HEAD, 1))

case("G7-omit-superseded-12-11", 1, 1, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (R73-LOG-COUNT-STALE)\n"
                     "The final committed instruments carry 13 and 14 cases.\n\n" + R73_HEAD, 1))

case("G8-omit-finals-13-14 (live tip mode)", 1, 1, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (R73-LOG-COUNT-STALE)\n"
                     "The twelfth (12) and eleven (11) counts above were mid-wave figures.\n\n" + R73_HEAD, 1))

# ---------- instrument-digest binding ----------
case("G10-counts-attributed-to-wrong-instruments", 0, 2, lesson_pass,
     log_tip.replace(R73_HEAD,
                     "## Round 73 — correction (R73-LOG-COUNT-STALE)\n"
                     "The mid-wave counts 12 and 11 are superseded; the round-74 instruments\n"
                     "tools/count-uf-rows-r74.py and tools/check-r73-routed-r74.py carry the final committed\n"
                     "counts 13 and 14 cases.\n\n" + R73_HEAD, 1))

# ---------- tip baseline ----------
case("TIP-baseline-unrepaired", 2, 0, lesson_tip, log_tip)

fails = 0
print(f"{'case':46s} {'exp':8s} {'got':8s} verdict  reason")
for name, exp_stale, exp_ok, fx in cases:
    stale, ok, reasons = chk.evaluate(fixture_texts=fx)
    verdict = "ok" if (stale, ok) == (exp_stale, exp_ok) else "MISMATCH"
    if verdict == "MISMATCH":
        fails += 1
    print(f"{name:46s} {exp_stale}/{exp_ok:<6d} {stale}/{ok:<6d} {verdict:8s} {reasons}")
print(f"\nBATTERY: {len(cases)} cases, {fails} mismatches vs my model of the checker")
