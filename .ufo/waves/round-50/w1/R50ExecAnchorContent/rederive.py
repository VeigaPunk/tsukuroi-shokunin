#!/usr/bin/env python3
"""Re-derive every ADJ anchor by content, independently of the round-50 counter."""
import json, hashlib, subprocess, sys, os, re

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.join(SCRATCH, "PROVINCE.md")
REG = os.path.join(SCRATCH, "adjacency-anchors-r19.json")
FLEET = "/home/vgpnk/Projects/shokunin"

def git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    return p.returncode, (p.stdout if binary else p.stdout.decode("utf-8", "replace")), p.stderr.decode("utf-8", "replace")

def sha(b):
    return hashlib.sha256(b).hexdigest()

# --- parse the ADJ table (ADJ-01..ADJ-07) for class per row -------------------
prov_text = open(PROV, encoding="utf-8").read()
prov_lines = prov_text.split("\n")

adj_class = {}   # ADJ-nn -> set of OUT ids named in its anchor column
adj_rows = {}
for i, ln in enumerate(prov_lines, 1):
    m = re.match(r"^\| (ADJ-0[1-7]) \|", ln)
    if not m:
        continue
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    aid = cells[0]
    outcell = cells[-1]
    ids = re.findall(r"OUT-\d{3}", outcell)
    adj_rows[aid] = {"line": i, "cells": cells, "out_ids": ids}
    for oid in ids:
        adj_class.setdefault(oid, set()).add(aid)

# --- parse the round-19 anchor table rows ------------------------------------
anchor_rows = {}
in_sec = False
for i, ln in enumerate(prov_lines, 1):
    if ln.startswith("## Adjacent — portable ownership anchors (round 19)"):
        in_sec = True
        continue
    if in_sec and ln.startswith("## "):
        break
    if not in_sec or not ln.startswith("| OUT-"):
        continue
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    # Anchor | ADJ row | Sibling file @ commit | Heading | Quote | Proposition
    if len(cells) < 6:
        print("PARSE-WARN row", i, "cells", len(cells), file=sys.stderr)
    anchor, adjrow, sibcell, heading, quote = cells[0], cells[1], cells[2], cells[3], cells[4]
    m = re.match(r"^`([^`]+)/PROVINCE\.md` @ `([0-9a-f]+)`$", sibcell)
    if not m:
        print("PARSE-FAIL sibling cell", repr(sibcell), file=sys.stderr)
        continue
    sib, abbrev = m.group(1), m.group(2)
    def unbt(s):
        return s[1:-1] if len(s) > 1 and s.startswith("`") and s.endswith("`") else s
    anchor_rows[anchor] = {
        "line": i, "adj_row": adjrow, "sibling": sib, "abbrev": abbrev,
        "heading_cell": heading, "heading": unbt(heading),
        "quote_cell": quote, "quote": unbt(quote),
    }

registry = json.load(open(REG, encoding="utf-8"))
outbound = {r["id"]: r for r in registry["outbound"]}
print("registry outbound ids:", sorted(outbound))
print("ADJ table rows:", {k: v["out_ids"] for k, v in adj_rows.items()})
print("anchor table rows:", sorted(anchor_rows))
print()

results = []
for oid in sorted(anchor_rows):
    row = anchor_rows[oid]
    reg = outbound.get(oid)
    res = {"id": oid, "adj_row": row["adj_row"], "sibling": row["sibling"],
           "abbrev": row["abbrev"], "checks": {}, "notes": []}
    c = res["checks"]
    sibrepo = os.path.join(FLEET, row["sibling"])
    res["sibrepo"] = sibrepo
    if not os.path.isdir(os.path.join(sibrepo, ".git")) and not os.path.isdir(os.path.join(sibrepo, ".jj")):
        res["notes"].append("sibling repo missing: " + sibrepo)
    if reg is None:
        res["notes"].append("no registry row for " + oid)
        results.append(res); continue

    full = reg["sibling_commit"]
    # registry vs table consistency
    c["registry_commit_full"] = full
    c["abbrev_is_prefix"] = full.startswith(row["abbrev"])
    c["reg_heading_eq_table"] = reg["heading"] == row["heading"]
    c["reg_quote_eq_table"] = reg["quote"] == row["quote"]
    c["reg_sibling_eq_table"] = reg["sibling"] == row["sibling"]
    c["reg_path"] = reg["sibling_path"]

    # 1. commit exists in sibling repo
    rc, out, err = git(sibrepo, "cat-file", "-t", full)
    c["commit_exists"] = (rc == 0 and out.strip() == "commit")
    if not c["commit_exists"]:
        res["notes"].append("commit %s not a commit in %s (rc=%d %s)" % (full, sibrepo, rc, err.strip()[:200]))
        results.append(res); continue

    # 2. blob digest
    rc, blob, err = git(sibrepo, "show", "%s:PROVINCE.md" % full, binary=True)
    c["show_rc"] = rc
    if rc != 0:
        res["notes"].append("show failed: " + err.strip()[:200])
        results.append(res); continue
    digest = sha(blob)
    c["digest"] = digest
    c["digest_registry"] = reg["sibling_blob_sha256"]
    c["digest_eq_registry"] = (digest == reg["sibling_blob_sha256"])
    c["digest_eq_province_listed"] = None  # filled later from portable digest list
    btext = blob.decode("utf-8", "replace")
    blines = btext.split("\n")

    # 3. heading present
    c["heading_present"] = row["heading"] in btext
    if c["heading_present"]:
        c["heading_line"] = next(i for i, l in enumerate(blines, 1) if l.strip() == row["heading"].strip())
        c["heading_is_title"] = c["heading_line"] == 1
        c["heading_exact_line"] = blines[c["heading_line"] - 1].strip() == row["heading"].strip()

    # 4. quote verbatim substring + line(s)
    qlines = [i for i, l in enumerate(blines, 1) if row["quote"] in l]
    c["quote_present"] = row["quote"] in btext
    c["quote_lines"] = qlines
    c["quote_line_registry"] = reg.get("quote_line")
    c["quote_line_matches_registry"] = (reg.get("quote_line") in qlines) if qlines else False

    # 5. class match: ADJ class in anchor row vs ADJ table row
    table_classes = sorted(adj_class.get(oid, []))
    c["adj_table_classes"] = table_classes
    c["class_match"] = (row["adj_row"] in table_classes) if table_classes else False
    if row["adj_row"] == "Core":
        c["class_match"] = "n/a-Core"

    # live leg
    rc, tip, err = git(sibrepo, "rev-parse", "HEAD")
    tip = tip.strip()
    c["tip"] = tip
    c["pin_is_ancestor_of_tip"] = None
    if rc == 0 and tip:
        rc2, _, _ = git(sibrepo, "merge-base", "--is-ancestor", full, tip)
        c["pin_is_ancestor_of_tip"] = (rc2 == 0)
        rc3, liveblob, err3 = git(sibrepo, "show", "%s:PROVINCE.md" % tip, binary=True)
        if rc3 == 0:
            ltext = liveblob.decode("utf-8", "replace")
            c["live_digest"] = sha(liveblob)
            c["live_digest_eq_pin"] = (c["live_digest"] == digest)
            lql = [i for i, l in enumerate(ltext.split("\n"), 1) if row["quote"] in l]
            c["live_quote_present"] = row["quote"] in ltext
            c["live_quote_lines"] = lql
        else:
            c["live_quote_present"] = None
            res["notes"].append("live show failed: " + err3.strip()[:200])
    results.append(res)

# portable digest list from PROVINCE section
portable = {}
for ln in prov_lines:
    m = re.match(r"^- (OUT-\d{3}) `([^`]+)` @ ([0-9a-f]{40}) sha256 ([0-9a-f]{64})$", ln)
    if m:
        portable[m.group(1)] = {"path": m.group(2), "commit": m.group(3), "sha256": m.group(4)}
for r in results:
    p = portable.get(r["id"])
    if p:
        r["checks"]["portable_list_present"] = True
        r["checks"]["portable_commit_eq_registry"] = p["commit"] == r["checks"].get("registry_commit_full")
        r["checks"]["portable_sha_eq_registry"] = p["sha256"] == r["checks"].get("digest_registry")
        r["checks"]["portable_sha_eq_observed"] = p["sha256"] == r["checks"].get("digest")
        r["checks"]["portable_path"] = p["path"]
    else:
        r["checks"]["portable_list_present"] = False

json.dump({"adj_rows": adj_rows and {k: {"line": v["line"], "out_ids": v["out_ids"]} for k, v in adj_rows.items()},
           "anchor_rows": anchor_rows, "portable": portable, "results": results},
          open(os.path.join(SCRATCH, "rederive.json"), "w"), indent=1)

# human table
hdr = ["id", "adj", "commit_exists", "digest_eq", "heading", "quote", "qline", "qline=reg", "class", "anc", "live_q"]
print("%-8s %-7s %-6s %-6s %-7s %-6s %-6s %-6s %-6s %-5s %-6s" % tuple(hdr))
for r in results:
    c = r["checks"]
    print("%-8s %-7s %-6s %-6s %-7s %-6s %-6s %-6s %-6s %-5s %-6s" % (
        r["id"], r["adj_row"], c.get("commit_exists"), c.get("digest_eq_registry"),
        c.get("heading_present"), c.get("quote_present"), c.get("quote_lines"),
        c.get("quote_line_matches_registry"), c.get("class_match"),
        c.get("pin_is_ancestor_of_tip"), c.get("live_quote_present")))
print()
for r in results:
    if r["notes"]:
        print(r["id"], "NOTES:", r["notes"])
