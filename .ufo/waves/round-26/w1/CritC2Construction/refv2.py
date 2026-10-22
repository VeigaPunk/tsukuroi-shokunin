#!/usr/bin/env python3
"""Reference model of the round-26 C2 check set v2 changes only (K01-K06, K24-K27).

Implements the declared text at SCORECARD.md:900-905 (commit b13e991) literally,
with two readings of "section" where the text is ambiguous:
  flat  - a section runs from its heading to the next heading of any level;
  tree  - a section runs to the next heading of the same or higher level, and a
          line is excluded when any enclosing heading names round N without
          "measured outcome".
Reads SCORECARD.md, SHONEN.md and corpus notes through `git show REV:path`.
Prints one JSON object. Not the lane tool; a critic's model of the declaration.
"""
import json
import re
import subprocess
import sys

AXES = ("depth", "coverage", "operability", "freshness", "calibration", "adjacency")
ORD = r"[^0-9|\u2192\n]{0,12}?(\d{1,2})\s*(?:\u2192|->)\s*(\d{1,2})"


def show(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def ls(repo, rev):
    p = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                       capture_output=True, text=True, check=True)
    return set(p.stdout.split())


def headings(lines):
    out = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            out.append((i, len(m.group(1)), line))
    return out


def names_round(text, n):
    return re.search(r"(?<![A-Za-z0-9])[Rr]ound %d(?!\d)" % n, text) is not None


def excluded_lines(lines, n, mode):
    hs = headings(lines)
    bad = set()
    for k, (i, lvl, text) in enumerate(hs):
        if not names_round(text, n) or "measured outcome" in text:
            continue
        end = len(lines)
        for j, l2, _ in hs[k + 1:]:
            if mode == "flat" or l2 <= lvl:
                end = j
                break
        bad.update(range(i, end))
    return bad


def axes_table(lines):
    last = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Axes\s+[\u2014-]\s", line):
            last = i
    if last is None:
        return None
    m = re.search(r"\(round (\d+)\)\s*$", lines[last])
    n = int(m.group(1)) if m else None
    end = len(lines)
    for j in range(last + 1, len(lines)):
        if re.match(r"^##\s", lines[j]):
            end = j
            break
    blocks = []
    i = last + 1
    while i < end:
        if lines[i].lstrip().startswith("|"):
            b = i
            while i < end and lines[i].lstrip().startswith("|"):
                i += 1
            blocks.append((b, i))
        else:
            i += 1
    axis_blocks = [bk for bk in blocks
                   if lines[bk[0]].strip().strip("|").split("|")[0].strip().lower() == "axis"]
    lo, hi = (axis_blocks or blocks)[-1]
    scores = {}
    for line in lines[lo:hi]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0].lower() in AXES:
            mm = re.search(r"\d+", cells[1])
            scores[cells[0].lower()] = int(mm.group()) if mm else None
    return n, lo, hi, scores


def k01_k06(lines, mode):
    t = axes_table(lines)
    if t is None or t[0] is None:
        return {"exit": 2, "reason": "axes heading lacks (round N)"}
    n, lo, hi, scores = t
    bad = excluded_lines(lines, n, mode)
    res = {"N": n, "mode": mode, "checks": []}
    for k, axis in enumerate(AXES, 1):
        pat = re.compile(r"\b" + re.escape(axis) + r"\b" + ORD)
        obs = None
        for i, line in enumerate(lines):
            if lo <= i < hi or i in bad:
                continue
            for m in pat.finditer(line):
                a, b = int(m.group(1)), int(m.group(2))
                if 0 <= a <= 10 and 0 <= b <= 10:
                    obs = (b, i + 1, line.strip()[:110])
        st = scores.get(axis)
        res["checks"].append({
            "id": "K%02d" % k, "stated": st,
            "observed": obs[0] if obs else None,
            "line": obs[1] if obs else None,
            "text": obs[2] if obs else None,
            "status": "match" if obs and obs[0] == st else "mismatch"})
    return res


def boxes(shonen):
    ls_ = shonen.split("\n")
    idx = [i for i, l in enumerate(ls_) if re.match(r"^- \[", l)]
    idx.append(len(ls_))
    return ["\n".join(ls_[idx[k]:idx[k + 1]]) for k in range(len(idx) - 1)]


def k24_k27(repo, rev, paths):
    shonen = show(repo, rev, "SHONEN.md")
    out = []
    for k, box in enumerate(boxes(shonen)[:4]):
        notes = re.findall(r"corpus/knowledge/[A-Za-z0-9_.{},/-]*?\.md", box)
        bad = []
        for note in notes:
            if note not in paths:
                bad.append((note, "absent"))
                continue
            head = "\n".join(show(repo, rev, note).split("\n")[:20])
            m = re.search(r"\bsuperseded\b", head, re.I)
            if m:
                ln = head[:m.start()].count("\n") + 1
                bad.append((note, "superseded marker at line %d" % ln))
        out.append({"id": "K%02d" % (24 + k), "notes": notes, "problems": bad,
                    "status": "mismatch" if bad else "match"})
    return out


def main():
    repo, rev = sys.argv[1], sys.argv[2]
    lines = show(repo, rev, "SCORECARD.md").split("\n")
    paths = ls(repo, rev)
    res = {"revision": rev,
           "K01_K06_flat": k01_k06(lines, "flat"),
           "K01_K06_tree": k01_k06(lines, "tree"),
           "K24_K27": k24_k27(repo, rev, paths)}
    for key in ("K01_K06_flat", "K01_K06_tree"):
        r = res[key]
        if "checks" in r:
            r["mismatches"] = sum(c["status"] == "mismatch" for c in r["checks"])
    res["K24_K27_mismatches"] = sum(c["status"] == "mismatch" for c in res["K24_K27"])
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
