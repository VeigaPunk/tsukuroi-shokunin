#!/usr/bin/env python3
"""Read-only replay of mori -> tsukuroi pointers. Writes TSV + JSON to argv[2]."""
import json, re, subprocess, sys, collections, os

MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
TIP = "db9eecfa876a865f799aa56856a780d299b4f067"
MREV = sys.argv[1]
OUT = sys.argv[2]

def git(repo, *a, check=True):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, errors="replace")
    if check and p.returncode:
        return None
    return p.stdout

_show = {}
def show(rev, path):
    k = (rev, path)
    if k not in _show:
        o = git(LANE, "show", f"{rev}:{path}")
        _show[k] = None if o is None else o.split("\n")
    return _show[k]

_commit = {}
def lane_commit(h):
    if h not in _commit:
        o = git(LANE, "rev-parse", "--verify", "--quiet", f"{h}^{{commit}}")
        _commit[h] = o.strip() if o else None
    return _commit[h]

lane_files_tip = set(git(LANE, "ls-tree", "-r", "--name-only", TIP).split("\n"))
lane_top = {f.split("/")[0] for f in lane_files_tip if f}
lane_files_all = set(filter(None, git(LANE, "log", "--all", "--name-only", "--format=", TIP).split("\n")))
mori_files = set(git(MORI, "ls-tree", "-r", "--name-only", MREV).split("\n"))
mori_base = {os.path.basename(f) for f in mori_files}
lane_base = {}
for f in lane_files_all:
    lane_base.setdefault(os.path.basename(f), set()).add(f)

LINES = r"(?::(\d+(?:[-–]\d+)?(?:,\s?\d+(?:[-–]\d+)?)*))?"
PATH = r"([A-Za-z0-9_][A-Za-z0-9_.\-/]*[A-Za-z0-9_])"
P_EXPL = re.compile(
    r"tsukuroi(?:-shokunin)?(?:@([0-9a-f]{7,40}):|/([0-9a-f]{7,40})/|/)" + PATH + LINES)
P_BARE = re.compile(r"`([A-Za-z0-9_.\-/]+\.(?:md|json|py|sh|txt))" + LINES)
P_COMMIT = re.compile(r"tsukuroi[^\s`]{0,20}[\s(`]{1,3}`?([0-9a-f]{7,40})`?")

def segs(lines):
    if not lines:
        return []
    out = []
    for s in re.split(r",\s?", lines):
        a, _, b = s.replace("–", "-").partition("-")
        out.append((int(a), int(b or a)))
    return out

_blame = {}
def blame_time(path, line):
    k = (path, line)
    if k not in _blame:
        o = git(MORI, "blame", "--porcelain", "-L", f"{line},{line}", MREV, "--", path)
        t = None
        if o:
            m = re.search(r"^committer-time (\d+)", o, re.M)
            t = int(m.group(1)) if m else None
        _blame[k] = t
    return _blame[k]

_era = {}
def era_commit(t):
    if t not in _era:
        o = git(LANE, "rev-list", "-1", f"--before={t}", TIP)
        _era[t] = o.strip() if o and o.strip() else None
    return _era[t]

def norm(s):
    return " ".join(s.split())

def classify(path, lines, ref):
    """Return (verdict, detail) for the pointer resolved at ref against TIP."""
    ref_txt = show(ref, path) if ref else None
    tip_txt = show(TIP, path)
    if ref_txt is None and tip_txt is None:
        return "UNRESOLVABLE", "path absent at reference commit and at tip"
    sg = segs(lines)
    if not sg:
        if tip_txt is None:
            return "UNRESOLVABLE", "path-only; present at reference, absent at tip"
        if ref_txt is None:
            return "RESOLVES", "path-only; absent at reference, present at tip"
        return "RESOLVES", "path-only"
    if ref_txt is None:
        return "UNRESOLVABLE", "path absent at reference commit (present at tip; lines unverifiable)"
    worst, parts = "RESOLVES", []
    rank = {"RESOLVES": 0, "DRIFTED": 1, "UNRESOLVABLE": 2}
    for a, b in sg:
        if b > len(ref_txt) or a < 1:
            v, d = "UNRESOLVABLE", f"{a}-{b} beyond reference length {len(ref_txt)}"
        elif tip_txt is None:
            v, d = "UNRESOLVABLE", f"{a}-{b} path absent at tip"
        else:
            blk = [norm(x) for x in ref_txt[a - 1:b]]
            tipn = [norm(x) for x in tip_txt]
            if tipn[a - 1:b] == blk:
                v, d = "RESOLVES", f"{a}-{b} same text same lines"
            else:
                n = len(blk)
                hits = [i + 1 for i in range(len(tipn) - n + 1) if tipn[i:i + n] == blk]
                if hits:
                    v, d = "DRIFTED", f"{a}-{b} -> {hits[0]}-{hits[0] + n - 1}" + (f" (+{len(hits)-1} more)" if len(hits) > 1 else "")
                else:
                    key = next((x for x in blk if len(x) >= 20), None)
                    loc = [i + 1 for i, x in enumerate(tipn) if key and x == key]
                    if loc:
                        v, d = "DRIFTED", f"{a}-{b} block edited; anchor line now at {loc[0]}"
                    else:
                        v, d = "UNRESOLVABLE", f"{a}-{b} text no longer at tip"
        parts.append(d)
        if rank[v] > rank[worst]:
            worst = v
    return worst, "; ".join(parts)

rows = []
for raw in open(sys.argv[3], encoding="utf-8", errors="replace"):
    rev, mpath, mline, content = raw.rstrip("\n").split(":", 3)
    mline = int(mline)
    found = []
    for m in P_EXPL.finditer(content):
        c1, c2, p, ln = m.groups()
        p = p.rstrip(".")
        if p.startswith("blob/") or p.startswith("tree/"):
            p = p.split("/", 2)[-1]
        if p.split("/")[0] not in lane_top:
            continue
        found.append(("explicit", c1 or c2, p, ln, m.group(0)))
    if "tsukuroi" in content:
        for m in P_BARE.finditer(content):
            p, ln = m.groups()
            if "tsukuroi" in p:
                continue
            base = os.path.basename(p)
            cands = {f for f in lane_base.get(base, set()) if not f.startswith(".ufo/")}
            if cands and base not in mori_base:
                full = p if p in cands else (sorted(cands)[0] if len(cands) == 1 else None)
                if full:
                    found.append(("bare", None, full, ln, m.group(0)))
        for m in P_COMMIT.finditer(content):
            h = m.group(1)
            if lane_commit(h):
                found.append(("commit", h, None, None, m.group(0)))
    for kind, c, p, ln, tok in found:
        rows.append(dict(mori_rev=rev[:12], mori_path=mpath, mori_line=mline, kind=kind,
                         named_commit=c, lane_path=p, lines=ln, token=tok,
                         quote=norm(content)[:240]))

results = {}
for r in rows:
    if r["kind"] == "commit":
        full = lane_commit(r["named_commit"])
        p = subprocess.run(["git", "-C", LANE, "merge-base", "--is-ancestor", full, TIP])
        r.update(ref=full[:12], verdict="RESOLVES" if p.returncode == 0 else "DRIFTED",
                 detail="commit exists, ancestor of tip" if p.returncode == 0 else "commit exists, not ancestor of tip")
        continue
    if r["named_commit"]:
        ref = lane_commit(r["named_commit"])
        basis = "named"
    else:
        t = blame_time(r["mori_path"], r["mori_line"])
        ref = era_commit(t) if t else None
        basis = "era"
    key = (r["lane_path"], r["lines"], ref)
    if key not in results:
        results[key] = classify(r["lane_path"], r["lines"], ref)
    v, d = results[key]
    if r["named_commit"] and not ref:
        v, d = "UNRESOLVABLE", "named commit not in lane"
    r.update(ref=(ref or "")[:12], basis=basis, verdict=v, detail=d)

with open(OUT + ".json", "w") as f:
    json.dump(rows, f, indent=1, ensure_ascii=False)
with open(OUT + ".tsv", "w") as f:
    cols = ["verdict", "kind", "lane_path", "lines", "named_commit", "ref", "detail", "mori_path", "mori_line", "token"]
    f.write("\t".join(cols) + "\n")
    for r in sorted(rows, key=lambda r: (r["lane_path"] or "", r["lines"] or "", r["mori_path"], r["mori_line"])):
        f.write("\t".join(str(r.get(c) or "") for c in cols) + "\n")
c = collections.Counter((r["verdict"]) for r in rows)
u = collections.Counter()
seen = set()
for r in rows:
    k = (r["lane_path"], r["lines"], r["named_commit"], r["verdict"])
    if k not in seen:
        seen.add(k); u[r["verdict"]] += 1
print("occurrences", len(rows), dict(c), "unique(path,lines,commit,verdict)", len(seen), dict(u))
