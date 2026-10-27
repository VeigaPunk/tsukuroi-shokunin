#!/usr/bin/env python3
"""
check-seat-receipts.py: Prototype validator for Quality Criterion 94
Verifies that:
1. File paths cited in seat reports resolve in Git at the given revision.
2. Explicit inventory/collision counts asserted in reports match companion line counts in the seat directory.
"""
import argparse, os, re, subprocess, sys

def check_citations(report_path, revision, lane_root):
    with open(report_path) as f:
        content = f.read()
    # Find cited relative paths under .ufo/ or corpus/ or tools/
    cited_paths = set(re.findall(r'[`\'"]((?:\.ufo|corpus|tools)/[a-zA-Z0-9_\-\./]+)[`\'"]', content))
    failures = []
    for p in sorted(cited_paths):
        if "..." in p or "*" in p:
            continue
        cmd = ["git", "-C", lane_root, "cat-file", "-e", f"{revision}:{p}"]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            failures.append(f"UNRESOLVED_CITATION: {p} (git cat-file -e rc={res.returncode})")
    return failures

def check_counts(report_path, seat_dir):
    with open(report_path) as f:
        content = f.read()
    failures = []
    # Match patterns like: "183 registry ids" or "30 intersections"
    m_reg = re.search(r'(\d+)\s+registry\s+ids', content, re.IGNORECASE)
    if m_reg:
        claimed_reg = int(m_reg.group(1))
        reg_file = os.path.join(seat_dir, "reg-ids")
        if not os.path.exists(reg_file):
            failures.append(f"MISSING_RECEIPT_FILE: {reg_file} (claimed {claimed_reg} registry ids, file missing)")
        else:
            with open(reg_file) as f:
                actual_reg = len([l for l in f if l.strip()])
            if claimed_reg != actual_reg:
                failures.append(f"COUNT_MISMATCH: claimed {claimed_reg} registry ids, {reg_file} has {actual_reg}")

    m_staged = re.search(r'(\d+)\s+staged\s+ids', content, re.IGNORECASE)
    if m_staged:
        claimed_staged = int(m_staged.group(1))
        staged_file = os.path.join(seat_dir, "staged-ids")
        if not os.path.exists(staged_file):
            failures.append(f"MISSING_RECEIPT_FILE: {staged_file} (claimed {claimed_staged} staged ids, file missing)")
        else:
            with open(staged_file) as f:
                actual_staged = len([l for l in f if l.strip()])
            if claimed_staged != actual_staged:
                failures.append(f"COUNT_MISMATCH: claimed {claimed_staged} staged ids, {staged_file} has {actual_staged}")

    m_col = re.search(r'(\d+)\s+intersections|(\d+)\s+collisions', content, re.IGNORECASE)
    if m_col:
        claimed_col = int(m_col.group(1) or m_col.group(2))
        col_file = os.path.join(seat_dir, "id-collisions.txt")
        if not os.path.exists(col_file):
            failures.append(f"MISSING_RECEIPT_FILE: {col_file}")
        else:
            with open(col_file) as f:
                actual_col = len([l for l in f if l.strip()])
            if claimed_col != actual_col:
                failures.append(f"COUNT_MISMATCH: claimed {claimed_col} collisions, but {col_file} has {actual_col} lines")
    return failures

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--seat-dir", required=True)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
    args = parser.parse_args()

    failures = []
    failures.extend(check_citations(args.report, args.revision, args.lane))
    failures.extend(check_counts(args.report, args.seat_dir))

    if failures:
        print(f"FAIL: {len(failures)} verification failure(s) in {args.report}:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"PASS: {args.report} is fully backed by receipts and valid git citations.")
        sys.exit(0)

if __name__ == "__main__":
    main()
