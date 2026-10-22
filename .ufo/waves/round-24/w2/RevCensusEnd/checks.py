#!/usr/bin/env python3
# Read-only census checks for the tsukuroi corpus/SOURCES.md (RevCensusEnd, round 24 wave 2).
# Reads the lane registry, lesson and git tree (read-only). Writes only to stdout.
import collections
import datetime
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SOURCES = os.path.join(LANE, "corpus/SOURCES.md")
LESSON = os.path.join(LANE, "corpus/lessons/round-24.md")
TODAY = datetime.date(2026, 10, 22)
COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "usedby"]
KIND = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
TIER = {"A", "B", "C"}
STATUS = {"queued", "mined", "rejected"}
NEW_FIRST = 87  # first row added by round 24 (S087)


def num(k):
    return int(k[1:])


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def urls(text):
    return re.findall(r"https?://[^\s|;,]+", text)


def url_key(u):
    # Mirrors sources-census.sh url_of: fragment and one trailing slash removed, host lowercased.
    u = re.sub(r"#[^ ]*$", "", u)
    u = re.sub(r"/$", "", u)
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return u[:n].lower() + u[n:] if n >= 0 else u.lower()


def page_key(u):
    return url_key(u).split("?")[0]


def main():
    raw = open(SOURCES, encoding="utf-8", newline="").read()
    lines = raw.split("\n")
    rows = {}
    nf_counter = collections.Counter()
    non_s_pipe = []
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("|") or s.startswith("| id |") or re.match(r"^\|[-|]+\|$", s):
            continue
        parts = s.split("|")
        nf_counter[len(parts)] += 1
        cells = [p.strip() for p in parts[1:-1]]
        if not cells or not re.fullmatch(r"S\d{3,}", cells[0]):
            non_s_pipe.append(i)
            continue
        if len(parts) != 13:
            continue
        row = dict(zip(COLS, cells))
        row["line"] = i
        rows[cells[0]] = row
    print("bytes", len(raw.encode("utf-8")), "lines", len(lines), "CR", raw.count("\r"), "TAB", raw.count("\t"))
    print("pipe-line NF counts", dict(nf_counter), "non-S pipe lines", non_s_pipe)
    print("registry rows", len(rows), "line range", min(r["line"] for r in rows.values()), max(r["line"] for r in rows.values()))
    ids = sorted(num(k) for k in rows)
    print("ids contiguous S001..S%03d" % ids[-1], ids == list(range(1, ids[-1] + 1)))
    print("enum violations", [k for k, r in rows.items() if r["kind"] not in KIND or r["tier"] not in TIER or r["status"] not in STATUS])
    for col in ("tier", "status", "kind"):
        print("count by", col, dict(collections.Counter(r[col] for r in rows.values())))
    print("count by tier x status", dict(collections.Counter((r["tier"], r["status"]) for r in rows.values())))
    print("count by kind x tier", dict(collections.Counter((r["kind"], r["tier"]) for r in rows.values())))
    new = {k: r for k, r in rows.items() if num(k) >= NEW_FIRST}
    print("round-24 rows", len(new), "tier", dict(collections.Counter(r["tier"] for r in new.values())),
          "status", dict(collections.Counter(r["status"] for r in new.values())),
          "kind", dict(collections.Counter(r["kind"] for r in new.values())),
          "opened", dict(collections.Counter(r["opened"] for r in new.values())))
    before_pages = {page_key(u) for k, r in rows.items() if num(k) < NEW_FIRST for u in urls(r["source"])}
    rereg = sorted([k for k, r in new.items() if any(page_key(u) in before_pages for u in urls(r["source"]))], key=num)
    print("round-24 rows re-registering a page already in S001-S086", rereg, len(rereg))
    all_pages = {url_key(u) for r in rows.values() for u in urls(r["source"])}
    before_all = {url_key(u) for k, r in rows.items() if num(k) < NEW_FIRST for u in urls(r["source"])}
    print("distinct normalized URLs now", len(all_pages), "before round", len(before_all))
    print("rows with a URL", sum(1 for r in rows.values() if urls(r["source"])), "rows without a URL", sum(1 for r in rows.values() if not urls(r["source"])))
    print("opened invalid or after 2026-10-22", [(k, r["opened"]) for k, r in rows.items() if parse_date(r["opened"]) is None or parse_date(r["opened"]) > TODAY])
    print("recheck values", dict(collections.Counter(r["recheck"] for r in rows.values())))
    print("recheck outside documented vocabulary", [(k, r["recheck"]) for k, r in rows.items()
                                                    if r["recheck"] not in ("90d", "180d", "on-release")
                                                    and parse_date(r["recheck"]) is None
                                                    and not re.fullmatch(r"\d+d", r["recheck"])])

    # W04 emulation: same first URL seen earlier under a scope not seen earlier for that URL.
    seen_url, seen_pair, w04 = set(), set(), []
    for k in sorted(rows, key=num):
        us = urls(rows[k]["source"])
        if not us:
            continue
        u = url_key(us[0])
        pair = (u, rows[k]["scope"])
        if u in seen_url and pair not in seen_pair:
            w04.append(k)
        seen_url.add(u)
        seen_pair.add(pair)
    print("W04 emulation (first URL, as sources-census.sh)", w04, len(w04))
    pair_count = collections.Counter((url_key(urls(r["source"])[0]), r["scope"]) for r in rows.values() if urls(r["source"]))
    print("same URL and same scope pairs (E04 candidates)", [p for p, c in pair_count.items() if c > 1])
    forms = collections.defaultdict(set)
    for k, r in rows.items():
        for u in urls(r["source"]):
            forms[page_key(u)].add((url_key(u), k))
    print("same page under different URL strings", {pg: sorted({k for _, k in v}, key=num)
                                                  for pg, v in forms.items() if len({f for f, _ in v}) > 1})

    # used-by: existence, HEAD tracking and row-id citation for mined rows.
    tracked = set(subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.split("\n"))
    issues = []
    all_paths = set()
    for k, r in rows.items():
        ub = r["usedby"]
        if r["status"] == "mined" and ub == "—":
            issues.append((k, "mined with no used-by"))
        if ub == "—":
            continue
        for p in (x.strip() for x in ub.split(",")):
            all_paths.add(p)
            full = os.path.join(LANE, p)
            if not os.path.isfile(full):
                issues.append((k, "missing on disk", p))
                continue
            if p not in tracked:
                issues.append((k, "not tracked at HEAD", p))
            if r["status"] == "mined":
                text = open(full, encoding="utf-8", errors="replace").read()
                if not re.search(r"\b%s\b" % k, text):
                    issues.append((k, "path does not cite row id", p))
    print("distinct used-by paths", len(all_paths))
    print("used-by issues", issues)
    print("non-mined rows with used-by", [(k, r["status"], r["usedby"]) for k, r in rows.items()
                                          if r["status"] != "mined" and r["usedby"] != "—"])

    # Local own-work and tool paths in the source cell must exist.
    missing = []
    for k, r in rows.items():
        if urls(r["source"]) and r["kind"] != "own-work":
            continue
        for tok in re.findall(r'[^\s;,()\[\]"“”]+', r["source"]):
            tok = tok.rstrip(".:;,)")
            if "/" not in tok or tok.startswith("http") or not re.search(r"(\.[A-Za-z0-9]+|/)$", tok):
                continue
            full = tok if tok.startswith("/") else os.path.join(LANE, tok)
            if not os.path.exists(full):
                missing.append((k, tok))
    print("own-work or tool local paths missing", missing)
    print("rows with no URL and kind other than own-work", [(k, r["kind"]) for k, r in rows.items()
                                                           if not urls(r["source"]) and r["kind"] != "own-work"])
    print("rows with more than one URL", [(k, len(urls(r["source"]))) for k, r in rows.items() if len(urls(r["source"])) > 1])

    # teaches contract: rejected rows read REJECTED: <reason>; flip: <change>.
    fmt = []
    for k, r in rows.items():
        t = r["teaches"]
        if r["status"] == "rejected" and not re.match(r"^(supersedes S\d{3} — )?REJECTED: .+; flip: .+$", t):
            fmt.append((k, "rejected format"))
        if r["status"] != "rejected" and "REJECTED" in t:
            fmt.append((k, "REJECTED text on non-rejected row"))
    print("teaches format issues", fmt)
    sup = [(k, t) for k, r in rows.items() for t in re.findall(r"supersedes (S\d{3})", r["teaches"])]
    print("supersedes pairs", sup, "bad targets", [(k, t) for k, t in sup if t not in rows or num(t) >= num(k)])
    print("supersedes not leading in teaches", [k for k, r in rows.items()
                                                 if "supersedes" in r["teaches"] and not r["teaches"].startswith("supersedes S")])
    refs = collections.Counter(re.findall(r"\bS(\d{3,})\b", raw))
    print("S-id tokens in file", len(refs), "dangling", sorted("S" + x for x in refs if "S" + x not in rows))
    pat = re.compile(r"op://|token|passw|secret|api[_-]?key|bearer|session|cookie|private|localhost|127\.0\.0\.1|192\.168\.|authorization|x-access", re.I)
    print("credential-like substrings (line, word)", [(i, m.group(0)) for i, l in enumerate(lines, 1) for m in pat.finditer(l)])

    # Search log: one prose note per bounded search.
    search_start = next(i for i, l in enumerate(lines, 1) if l.startswith("## Search log"))
    leads_start = next(i for i, l in enumerate(lines, 1) if l.startswith("## Leads"))
    print("Search log lines", search_start, "to", leads_start)
    print("round-24 or 2026-10-22 mentions inside Search log", [(i, l[:80]) for i, l in enumerate(lines, 1)
                                                                if search_start < i < leads_start and re.search(r"[Rr]ound ?-?24|2026-10-22", l)])
    notes = [(i, l[:50]) for i, l in enumerate(lines, 1) if search_start < i < leads_start and re.search(r"^(Round|round|Round18|Round-)", l.strip())]
    print("last round-labelled Search log note", notes[-1] if notes else None)

    # Lesson disclosure of the W04 delta and Gate table shape.
    lesson = open(LESSON, encoding="utf-8").read().split("\n")
    header = next(l for l in lesson if l.startswith("| Row | URL |"))
    print("lesson Gate header", header)
    print("lesson Gate has access-date column", "access" in header.lower(), "| location column", "location" in header.lower())
    w04_line = next(l for l in lesson if "New duplicate-scope warnings" in l)
    print("lesson W04 sentence", w04_line[w04_line.find("New duplicate-scope warnings"):])
    print("new W04 pages named in lesson", {
        "archlinux.org/news (S087)": "archlinux.org/news" in w04_line,
        "System_maintenance (S092)": "System_maintenance" in w04_line,
        "pacman.8 (S089, S090)": "pacman.8" in w04_line,
        "btrfs-overlayfs (S098)": "btrfs-overlayfs" in w04_line,
        "MR 482 (S095)": "482" in w04_line,
    })
    print("lesson Gate quote for S087", next(l for l in lesson if l.startswith("| S087 |"))[:200])


if __name__ == "__main__":
    main()
