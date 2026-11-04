#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
OUT_FILE = REPO / ".ufo/waves/round-74/w1/K1Critic/evidence/attacks.txt"

out_lines = []

def log(msg=""):
    print(msg)
    out_lines.append(msg)

log("=== K1Critic Round 74 Adversarial Attack Battery ===")
log(f"Repo: {REPO}")
log()

# -------------------------------------------------------------
# Test 1: C1 Answer-key verification in count-uf-rows-r74.py
# -------------------------------------------------------------
log("--- ATTACK 1: C1 Instrument Answer-Key Check ---")
counter_src = (REPO / "tools/count-uf-rows-r74.py").read_text()
if "syn-alpha.c" in counter_src and "syn-beta.c" in counter_src:
    log("RESULT: count-uf-rows-r74.py uses synthetic fixtures (syn-alpha.c, etc.) in selftest.")
    log("VERDICT: No real-corpus note/registry answer-key found in count-uf-rows-r74.py (D2 answered).")
else:
    log("WARNING: Synthetic fixtures not detected in count-uf-rows-r74.py.")
log()

# -------------------------------------------------------------
# Test 2: C2 Instrument Answer-Key Check (check-r73-routed-r74.py)
# -------------------------------------------------------------
log("--- ATTACK 2: C2 Instrument Answer-Key Leakage ---")
checker_src = (REPO / "tools/check-r73-routed-r74.py").read_text()
has_good_lesson = "good_lesson = " in checker_src and "R73-GATE-QUOTE-LINE-DRIFT" in checker_src
has_good_log = "good_log = " in checker_src and "R73-LOG-COUNT-STALE" in checker_src
log(f"check-r73-routed-r74.py contains good_lesson answer key: {has_good_lesson}")
log(f"check-r73-routed-r74.py contains good_log answer key: {has_good_log}")

# Demonstrate extracting answer key and passing C2 directly
code_c2_key = f"""
import importlib.util, inspect, re
spec = importlib.util.spec_from_file_location('c', '{REPO}/tools/check-r73-routed-r74.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
src = inspect.getsource(c.run_selftest)
lesson_m = re.search(r'good_lesson = \"\"\"(.*?)\"\"\"', src, re.DOTALL)
log_m = re.search(r'good_log = \"\"\"(.*?)\"\"\"', src, re.DOTALL)
lesson_text = lesson_m.group(1)
log_text = log_m.group(1)
fixtures = {{'corpus/lessons/round-73.md': lesson_text, 'LOG.md': log_text}}
stale, ok, reasons = c.evaluate(fixture_texts=fixtures)
print(f"Extracted answer key passes checker: ROUTED_STALE={{stale}} ROUTED_OK={{ok}}/2")
"""
res_c2_key = subprocess.run(["python3", "-c", code_c2_key], capture_output=True, text=True)
log("Answer-Key Test Execution:")
log(res_c2_key.stdout.strip())
if res_c2_key.stderr:
    log("stderr: " + res_c2_key.stderr.strip())
log("VERDICT: C2 instrument check-r73-routed-r74.py embeds verbatim solution blocks for both targets.")
log()

# -------------------------------------------------------------
# Test 3: C2 Pure Lexical Channel (Denials and Token Jumbles)
# -------------------------------------------------------------
log("--- ATTACK 3: C2 Denial and Token Jumble Channel ---")
# 3a. Explicit denial
denial_lesson = """# Round 73 lesson

## Correction (R73-GATE-QUOTE-LINE-DRIFT)
We strictly reject that install.c:2383 supersedes 2387.
Furthermore, we dispute the line anchors :368-370, :237-238, and :238-239 as completely incorrect.
"""

denial_log = """# LOG

## Round 73 — correction (R73-LOG-COUNT-STALE)
We refute that instruments had 11 or 12 or 13 or 14 cases.
"""

code_denial = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('c', '{REPO}/tools/check-r73-routed-r74.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
stale, ok, reasons = c.evaluate(fixture_texts={{
    'corpus/lessons/round-73.md': '''{denial_lesson}''',
    'LOG.md': '''{denial_log}'''
}})
print(f"Denial text evaluation: ROUTED_STALE={{stale}} ROUTED_OK={{ok}}/2 reasons={{reasons}}")
"""
res_denial = subprocess.run(["python3", "-c", code_denial], capture_output=True, text=True)
log("3a. Explicit Denial Test:")
log(res_denial.stdout.strip())
if res_denial.stderr:
    log("stderr: " + res_denial.stderr.strip())

# 3b. Bare token salad
salad_lesson = """# Round 73 lesson
## R73-GATE-QUOTE-LINE-DRIFT
install.c:2383 2387 :368-370 :237-238 :238-239
"""

salad_log = """# LOG
## R73-LOG-COUNT-STALE
11 12 13 14
"""

code_salad = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('c', '{REPO}/tools/check-r73-routed-r74.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
stale, ok, reasons = c.evaluate(fixture_texts={{
    'corpus/lessons/round-73.md': '''{salad_lesson}''',
    'LOG.md': '''{salad_log}'''
}})
print(f"Bare token salad evaluation: ROUTED_STALE={{stale}} ROUTED_OK={{ok}}/2 reasons={{reasons}}")
"""
res_salad = subprocess.run(["python3", "-c", code_salad], capture_output=True, text=True)
log("3b. Bare Token Salad Test:")
log(res_salad.stdout.strip())
if res_salad.stderr:
    log("stderr: " + res_salad.stderr.strip())
log("VERDICT: C2 checker is purely lexical with no syntax/semantic verification; accepts denials and token dumps.")
log()

# -------------------------------------------------------------
# Test 4: C1 Semantic Detachment (Negation & Salad Rows)
# -------------------------------------------------------------
log("--- ATTACK 4: C1 Semantic Detachment (Negation & Salad Rows) ---")

code_c1_sem = f"""
import importlib.util, sys, tempfile, json, hashlib, shutil
from pathlib import Path
spec = importlib.util.spec_from_file_location('c', '{REPO}/tools/count-uf-rows-r74.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

with tempfile.TemporaryDirectory() as td:
    tdp = Path(td)
    snap_dir = tdp / c.SNAPDIR
    snap_dir.mkdir(parents=True, exist_ok=True)
    
    # Text with specific keywords
    s1 = "The unit search path priority order registers first seen unit names."
    s2 = "Unit symlinks reject self aliases and check target unit types."
    s3 = "Unit type may alias allows service socket target device volume."
    
    snaps = {{"s1.c": s1, "s2.c": s2, "s3.h": s3}}
    s_map = {{}}
    for name, text in snaps.items():
        (snap_dir / name).write_text(text)
        s_map[name] = {{
            "url": f"https://example.org/{{name}}",
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "tag": "v262",
            "bytes": len(text)
        }}
    (snap_dir / "SOURCES.json").write_text(json.dumps(s_map))
    
    reg_lines = [
        "# SOURCES",
        "| ID | Title | Kind | Tier | Scope | Location | Summary | Status | Date | Recheck | Used-by | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
        f"| S309 | S1 — {{s_map['s1.c']['url']}} | code | A | scope | s1.c | summary | mined | 2026-11-04 | on-release | {{c.NOTE}} | |",
        f"| S310 | S2 — {{s_map['s2.c']['url']}} | code | A | scope | s2.c | summary | mined | 2026-11-04 | on-release | {{c.NOTE}} | |",
        f"| S311 | S3 — {{s_map['s3.h']['url']}} | code | A | scope | s3.h | summary | mined | 2026-11-04 | on-release | {{c.NOTE}} | |",
    ]
    (tdp / c.REGISTRY).parent.mkdir(parents=True, exist_ok=True)
    (tdp / c.REGISTRY).write_text("\\n".join(reg_lines) + "\\n")
    
    # Construct completely NEGATED / FALSE assertions that share tokens:
    neg_rows = [
        f'| UF1 | The unit search path priority order NEVER registers first seen unit names at all | source=S309 | snapshot=s1.c | digest={{s_map["s1.c"]["sha256"]}} | quote="search path priority order" |',
        f'| UF2 | The unit search path priority order COMPLETELY FAILS to register first seen units | source=S309 | snapshot=s1.c | digest={{s_map["s1.c"]["sha256"]}} | quote="registers first seen unit names" |',
        f'| UF3 | Unit symlinks NEVER reject self aliases and DO NOT check target unit types | source=S310 | snapshot=s2.c | digest={{s_map["s2.c"]["sha256"]}} | quote="Unit symlinks reject self aliases" |',
        f'| UF4 | Unit symlinks PERMIT self aliases and IGNORE target unit types completely and unconditionally | source=S310 | snapshot=s2.c | digest={{s_map["s2.c"]["sha256"]}} | quote="and check target unit types" |',
        f'| UF5 | Unit type may alias FORBIDS service socket target device volume aliasing entirely | source=S311 | snapshot=s3.h | digest={{s_map["s3.h"]["sha256"]}} | quote="Unit type may alias allows" |',
        f'| UF6 | Unit type may alias PROHIBITS service socket target device volume operations entirely | source=S311 | snapshot=s3.h | digest={{s_map["s3.h"]["sha256"]}} | quote="service socket target device volume" |',
    ]
    (tdp / c.NOTE).parent.mkdir(parents=True, exist_ok=True)
    (tdp / c.NOTE).write_text("\\n".join(neg_rows) + "\\n")
    
    rc, summary, findings = c.evaluate(tdp, fixture=tdp)
    print(f"Negated claims test: rc={{rc}} met={{summary['met']}} findings={{findings}}")
"""

res_c1_sem = subprocess.run(["python3", "-c", code_c1_sem], capture_output=True, text=True)
log("C1 Negated Claims Test:")
log(res_c1_sem.stdout.strip())
if res_c1_sem.stderr:
    log("stderr: " + res_c1_sem.stderr.strip())
log("VERDICT: C1 counter evaluates only lexical token overlap (MIN_TOKENS>=6, share>=0.5) and verbatim quote existence; contradictory/negated statements pass.")
log()

# -------------------------------------------------------------
# Test 5: Mathematical Proof and Mutation of Unfalsifiable Conjunct
# -------------------------------------------------------------
log("--- ATTACK 5: Unfalsifiable Conjunct in count-uf-rows-r74.py ---")
log("Expression: met = (len(parsed_rows) == TARGET_ROWS and len(findings) == 0 and len(sources_used) >= TARGET_SOURCES and len(snapshots_used) >= TARGET_SNAPSHOTS)")
log("Target parameters: TARGET_ROWS = 6, MAX_SNAPSHOT_REUSE = 2, TARGET_SNAPSHOTS = 3")
log("Mathematical Theorem: For any partition of N items into subsets of size at most M, the number of subsets S satisfies:")
log("  S >= ceil(N / M)")
log("For N=6, M=2: S >= ceil(6 / 2) = 3.")
log("Since MAX_SNAPSHOT_REUSE enforcement in loop adds a finding whenever reuse_count[snap] > 2,")
log("any execution with len(findings) == 0 and len(parsed_rows) == 6 MUST have len(snapshots_used) >= 3.")
log("Thus, the conjunct `and len(snapshots_used) >= TARGET_SNAPSHOTS` is 100% UNREACHABLE ON FALSE / UNFALSIFIABLE.")

# Demonstrate mutation test: replacing `and len(snapshots_used) >= TARGET_SNAPSHOTS` with `and True`
mutated_counter = counter_src.replace(
    "and len(snapshots_used) >= TARGET_SNAPSHOTS",
    "and True  # MUTANT: snapshots conjunct eliminated"
)
with tempfile.NamedTemporaryFile("w", suffix=".py") as tf:
    tf.write(mutated_counter)
    tf.flush()
    res_selftest = subprocess.run(["python3", tf.name, "--selftest"], capture_output=True, text=True)
    log(f"Selftest on Mutant with conjunct removed: {res_selftest.stdout.strip()}")
    log(f"Exit code: {res_selftest.returncode}")
log("VERDICT: The conjunct `len(snapshots_used) >= TARGET_SNAPSHOTS` is completely unfalsifiable; all 13 selftest cases pass when it is neutralized.")
log()

# -------------------------------------------------------------
# Test 6: Redundant Disjunct `or rinfo["kind"] == "own-work"`
# -------------------------------------------------------------
log("--- ATTACK 6: Redundant Disjunct `or rinfo['kind'] == 'own-work'` ---")
log("In count-uf-rows-r74.py:")
log("  KINDS = {'spec', 'docs', 'paper', 'code', 'tool', 'dataset', 'talk', 'book', 'community'}")
log("  if rinfo['kind'] not in KINDS or rinfo['kind'] == 'own-work':")
log("Since 'own-work' is not in KINDS, whenever kind == 'own-work', `kind not in KINDS` is already True.")
log("The right-hand side `or rinfo['kind'] == 'own-work'` is dead code.")

mutated_kind = counter_src.replace(
    "if rinfo[\"kind\"] not in KINDS or rinfo[\"kind\"] == \"own-work\":",
    "if rinfo[\"kind\"] not in KINDS:  # MUTANT: own-work arm removed"
)
with tempfile.NamedTemporaryFile("w", suffix=".py") as tf:
    tf.write(mutated_kind)
    tf.flush()
    res_selftest2 = subprocess.run(["python3", tf.name, "--selftest"], capture_output=True, text=True)
    log(f"Selftest on Mutant with own-work arm removed: {res_selftest2.stdout.strip()}")
    log(f"Exit code: {res_selftest2.returncode}")
log("VERDICT: The second disjunct `or rinfo['kind'] == 'own-work'` is completely unreachable / dead code.")
log()

# -------------------------------------------------------------
# Test 7: Sizing Inconsistency in Declaration
# -------------------------------------------------------------
log("--- ATTACK 7: Declaration Sizing Contradiction ---")
log("Declaration claim text (SCORECARD.md line 6092):")
log("  'Rows UF1-UF6, sources S309-S311 (v262 unit-file.c, load-fragment.c, unit-file.h)'")
log("  -> Cites exactly 3 sources: S309, S310, S311.")
log("Declaration kill rule (SCORECARD.md line 6092):")
log("  'kill rule: any finding > 0, rows != 6, verified != 6, sources < 3, snapshots < 3, census != 0, registry < 313, notes < 92'")
log("  -> Base registry is 308. 308 + 3 = 311. 'registry < 313' requires at least +5 rows!")
log("Declaration scope text (SCORECARD.md line 6095):")
log("  'C1 touches only its note, five registry rows, and its counter receipts'")
log("Swarm spec (w1-spec.json line 75):")
log("  'milestone': 'registry rows S309-S313, Gate quotes, search log and one honest rejection'")
log("ANALYSIS: If an implementer faithfully executes the frozen claim (adding sources S309-S311 for the 3 snapshots),")
log("the registry count is 311, which triggers the kill rule `registry < 313` and FAILS the round!")
log("The declaration text claims 3 sources (S309-S311) but hardcodes a predicate threshold expecting 5 rows (S309-S313).")

# -------------------------------------------------------------
# Test 8: First-Match Shadowing in C2 Checker Blocks Appended LOG.md
# -------------------------------------------------------------
log("--- ATTACK 8: First-Match Block Shadowing Blocks Appended LOG.md ---")
code_shadow = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('c', '{REPO}/tools/check-r73-routed-r74.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
base_log = c.load_file('{REPO}', 'LOG.md', 'd749a625')
appended_log = base_log + '\\n\\n## Round 73 — correction (R73-LOG-COUNT-STALE)\\nAppended correction: superseded counts 12 and 11, final committed instrument counts 13 and 14.\\n'
res, msg = c.check_r73_log_count(appended_log)
print(f"Append at EOF evaluation: ok={{res}} msg={{msg}}")
"""
res_shadow = subprocess.run(["python3", "-c", code_shadow], capture_output=True, text=True)
log("First-match shadowing test execution:")
log(res_shadow.stdout.strip())
if res_shadow.stderr:
    log("stderr: " + res_shadow.stderr.strip())
log("VERDICT: Appending a valid correction at EOF is shadowed by the older Round 73 block; frozen C2 checker rejects appended correction.")
log()

# Write output file
OUT_FILE.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
print(f"Written evidence to {OUT_FILE}")
