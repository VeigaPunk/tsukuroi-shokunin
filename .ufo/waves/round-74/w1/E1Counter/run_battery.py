#!/usr/bin/env python3
"""E1Counter round-74: execute all fixtures against tools/count-uf-rows-r74.py and record results."""
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
TOOL = LANE / "tools/count-uf-rows-r74.py"
FX_DIR = Path("/fast/scratch/hyaku/tsukuroi-r74/E1Counter/fixtures")

# (fixture_name, expected_rc, expected_token_in_output_or_stderr, description)
BATTERY = [
    ("mirror", 0, "met=1", "Independent mirror written from v262 snapshots"),
    ("scripted", 0, "met=1", "Scripted non-reader (100% snapshot vocabulary, candidate quote)"),
    ("blind-negate", 0, "met=1", "Blind spot: negated claim with vocabulary preserved"),
    ("blind-unanchored-quote", 0, "met=1", "Blind spot: license header quote unanchored to claim"),
    ("blind-dupecontent", 0, "met=1", "Blind spot: identical statement and quote duplicated across rows"),
    ("iso-id-gap", 1, "non-contiguous IDs", "Isolation: non-contiguous row IDs (UF1..UF5, UF7)"),
    ("iso-id-dupe", 1, "duplicate UF id 1", "Isolation: duplicate UF row ID"),
    ("iso-words-short", 1, "short statement", "Isolation: statement < 12 words"),
    ("iso-ground-zero", 1, "too few shared tokens", "Isolation: ungrounded statement (0 shared tokens)"),
    ("iso-ground-low", 1, "shared share too low", "Isolation: token share ratio < 0.50"),
    ("iso-src-unreg", 1, "source S999 not in registry", "Isolation: unregistered source S999"),
    ("iso-src-ownwork", 1, "invalid kind own-work", "Isolation: source kind is own-work"),
    ("iso-src-badkind", 1, "invalid kind fabricated", "Isolation: source kind is invalid"),
    ("iso-reg-dupid", 1, "UF_REGISTRY duplicate id", "Isolation: duplicate S-ID in registry"),
    ("iso-snap-corrupt", 1, "byte mismatch", "Isolation: snapshot file modified"),
    ("iso-digest-swap", 1, "digest mismatch", "Isolation: row digest mismatch with SOURCES.json"),
    ("iso-map-corrupt", 1, "digest mismatch", "Isolation: SOURCES.json digest mismatch"),
    ("iso-map-url", 1, "does not cite URL", "Isolation: registry source cell missing map URL"),
    ("iso-anchor-missing", 1, "does not anchor", "Isolation: registry anchor cell missing snapshot basename"),
    ("iso-quote-absent", 1, "quote not located in snapshot", "Isolation: quote altered from snapshot text"),
    ("iso-quote-long", 1, "quote length out of bounds", "Isolation: quote > 25 words"),
    ("iso-quote-short", 1, "quote length out of bounds", "Isolation: quote < 4 words"),
    ("iso-quote-pipe", 1, "quote contains pipe", "Isolation: quote contains pipe |"),
    ("iso-malformed-row", 1, "malformed row shape", "Isolation: malformed row shape"),
    ("iso-reuse-3", 1, "cited 3 > 2", "Isolation: snapshot cited 3 times (> MAX_SNAPSHOT_REUSE 2)"),
    ("iso-nonmap-mapfile", 1, "UF_MAP malformed", "Isolation: SOURCES.json root is not a dict"),
    ("iso-empty-quote", 1, "quote length out of bounds", "Isolation: quote is empty string quote=\"\""),
]

def run():
    passed = 0
    failed = 0
    runs_txt = []
    runs_txt.append("================================================================================")
    runs_txt.append("E1Counter round-74: Frozen C1 Counter Tamper Battery & Fixture Execution Log")
    runs_txt.append(f"Tool: {TOOL}")
    runs_txt.append("================================================================================\n")

    for name, exp_rc, exp_token, desc in BATTERY:
        fx_path = FX_DIR / name
        cmd = ["python3", str(TOOL), "--fixture", str(fx_path)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        rc = res.returncode
        out = res.stdout.strip()
        err = res.stderr.strip()
        combined = f"{out}\n{err}".strip()

        ok = (rc == exp_rc) and (exp_token in combined)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        line = f"[{status}] {name:25} rc={rc:3} (exp {exp_rc:3}) token='{exp_token}'"
        print(line)
        runs_txt.append(f"--- Case: {name} ---")
        runs_txt.append(f"Description: {desc}")
        runs_txt.append(f"Command: {' '.join(cmd)}")
        runs_txt.append(f"Verdict: {status} (rc={rc}, expected_rc={exp_rc})")
        runs_txt.append(f"Required token: '{exp_token}' (found={exp_token in combined})")
        if out:
            runs_txt.append(f"Stdout:\n{out}")
        if err:
            runs_txt.append(f"Stderr:\n{err}")
        runs_txt.append("")

    summary = f"BATTERY RESULTS: {passed} passed, {failed} failed out of {len(BATTERY)} cases"
    print(summary)
    runs_txt.append(summary)
    
    # Write runs log
    out_log = Path("/fast/scratch/hyaku/tsukuroi-r74/E1Counter/counter-runs.txt")
    out_log.write_text("\n".join(runs_txt) + "\n")
    return failed == 0

if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
