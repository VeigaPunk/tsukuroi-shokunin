#!/usr/bin/env python3
"""Byte-level comparison of the C1/C2 sentences in claims.json vs the plan
(.ufo/plans/round-96.md) and the frozen plan (.ufo/waves/round-96/before/plan-frozen.md).

Normalisation: collapse all runs of whitespace (incl. newlines) to a single space,
strip ends.  Then compare predicate / target / kill / counting for C1 and C2.
"""
import json
import re
import sys
import difflib

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS.sub(" ", s).strip()


def plan_sections(text: str):
    """Return {'C1': {...}, 'C2': {...}} of field -> normalised sentence."""
    out = {}
    # Split on the claim headings
    parts = re.split(r"^### (C[12]) — .*$", text, flags=re.M)
    # parts[0] = preamble; then alternating key, body
    for i in range(1, len(parts), 2):
        key = parts[i]
        body = parts[i + 1]
        fields = {}
        cur = None
        buf = []
        for line in body.splitlines():
            m = re.match(r"^\*\*(Predicate|Target|Kill rule|Counting command)\.\*\*\s*(.*)$", line)
            if m:
                if cur:
                    fields[cur] = norm(" ".join(buf))
                cur = m.group(1).lower().replace(" ", "_")
                buf = [m.group(2)]
            elif cur is not None:
                # stop at the next bold field or a '---' separator / header
                if line.startswith("**") or line.startswith("---") or line.startswith("## "):
                    fields[cur] = norm(" ".join(buf))
                    cur, buf = None, []
                else:
                    buf.append(line)
        if cur:
            fields[cur] = norm(" ".join(buf))
        out[key] = fields
    return out


def report(label, a, b, diffs):
    if a == b:
        print(f"[IDENTICAL] {label}")
        return
    diffs.append(label)
    print(f"[DIFFERENT] {label}")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ctx = 40
        print(f"   op={tag} A[{i1}:{i2}]={a[max(0,i1-ctx):i2+ctx]!r}")
        print(f"          B[{j1}:{j2}]={b[max(0,j1-ctx):j2+ctx]!r}")


def main():
    claims = json.load(open(f"{LANE}/.ufo/waves/round-96/claims.json"))["claims"]
    plan = open(f"{LANE}/.ufo/plans/round-96.md").read()
    frozen = open(f"{LANE}/.ufo/waves/round-96/before/plan-frozen.md").read()

    diffs = []

    # 0. plan vs frozen plan: whole file
    print("== step 0: .ufo/plans/round-96.md vs .ufo/waves/round-96/before/plan-frozen.md ==")
    report("whole file (normalised)",
           norm(plan), norm(frozen), diffs)
    print("   raw byte equality:",
          open(f"{LANE}/.ufo/plans/round-96.md", "rb").read()
          == open(f"{LANE}/.ufo/waves/round-96/before/plan-frozen.md", "rb").read())

    ps = plan_sections(plan)
    fs = plan_sections(frozen)
    print("\n== step 0b: plan sections vs frozen-plan sections ==")
    for k in ("C1", "C2"):
        for f in sorted(set(ps.get(k, {})) | set(fs.get(k, {}))):
            report(f"{k}.{f}", ps.get(k, {}).get(f, ""), fs.get(k, {}).get(f, ""), diffs)

    for src_name, src in (("plan", ps), ("frozen-plan", fs)):
        print(f"\n== step 1: claims.json vs {src_name} ==")
        for cid in ("C1", "C2"):
            c = claims[cid]
            fields = {
                "predicate": "predicate",
                "target": "target",
                "kill": "kill_rule",
                "counting": "counting_command",
            }
            for ckey, pkey in fields.items():
                report(f"{cid}.{ckey}", norm(c[ckey]), src.get(cid, {}).get(pkey, ""), diffs)

    print("\n== summary ==")
    if diffs:
        print(f"DIFFERENCES FOUND ({len(diffs)}):")
        for d in diffs:
            print("  -", d)
        return 1
    print("NO DIFFERENCES: every C1/C2 sentence is byte-identical after whitespace normalisation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
