#!/usr/bin/env python3
"""w04-classify.py — classify the duplicate-URL (W04) pairs that the fleet sources census reports.

Routed defect 5 (registry inflation) of round 24: the fleet census
(scripts/sources-census.sh, fleet repo) emits a W04 warning for every registry row that
re-uses a URL already seen under a different scope.  Between round 24 and the round-25
declaration the tsukuroi registry grew from 86 to 114 rows and the W04 count went from 9 to
21, because a row may only be opened on the round it is mined: a page that must be re-read
has to be registered as a *new* row instead of being re-checked in place.

This script is read-only.  It

  1. reads corpus/SOURCES.md at a named revision with `git show` (no write commands),
  2. re-implements the census' own W04 detection byte-for-byte (same URL normalisation,
     same scope key, same emission order),
  3. optionally cross-checks its own W04 set against the real census (--census), and
  4. classifies every W04 pair into exactly one of three classes:

       SAME_PAGE_RE_REGISTRATION   the same page is registered again under a new scope
                                   (registry inflation: the row should have been an
                                   in-place `recheck` update of the earlier row)
       SAME_SCOPE_DUPLICATE        the same URL is registered under the *same* scope
                                   (a hard duplicate; the census reports E04 for it)
       DIFFERENT_ANCHOR            the two rows cite different passages of one URL
                                   (legitimate: one page, several distinct anchors)

Classification is lexical and every signal is printed, so each pair can be audited.
The thresholds are documented in CLASS_* constants and can be overridden on the command
line for a re-run.

Usage:
  python3 tools-draft/w04-classify.py --repo <path> --revision <rev> [--census <script>]
                                       [--threshold <float>] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

# --------------------------------------------------------------------------- census parity

# scripts/sources-census.sh url_of(): first https?:// token, fragment stripped, trailing
# slash stripped, scheme stripped, host lower-cased, path kept verbatim.
CENSUS_URL_RE = re.compile(r"https?://[^\s|]+")


def census_url(source: str) -> str:
    """Reproduce the census' url_of() exactly."""
    m = CENSUS_URL_RE.search(source)
    if not m:
        return ""
    u = m.group(0)
    u = re.sub(r"#.*$", "", u)          # gawk: sub(/#[^ ]*$/,"",u)
    u = re.sub(r"/$", "", u)            # gawk: sub(/\/$/,"",u)
    u = re.sub(r"^[A-Za-z]+://", "", u)  # gawk: sub(/^[A-Za-z]+:\/\//,"",u)
    i = u.find("/")
    if i >= 0:
        u = u[:i].lower() + u[i:]
    else:
        u = u.lower()
    return u


def parse_registry(text: str) -> list[dict]:
    """Parse the ## Registry table exactly as the census' gawk program does."""
    rows: list[dict] = []
    in_registry = False
    for raw in text.splitlines():
        if re.match(r"^ {0,3}#[ \t]", raw):
            if re.match(r"^ {0,3}##[ \t]", raw):
                head = raw.lstrip(" ")[:].split("##", 1)[1]
                in_registry = head.strip() == "Registry"
                continue
            in_registry = False
            continue
        if not re.match(r"^ {0,3}\|", raw):
            continue
        line = re.sub(r"^ {0,3}", "", raw)
        cells = line.split("|")
        if len(cells) != 13:
            continue
        if cells[1].strip() == "id":
            continue
        if all(set(c) <= set("-: ") for c in cells[2:13]):
            continue
        rows.append(
            {
                "id": cells[1].strip(),
                "source": cells[2].strip(),
                "kind": cells[3].strip(),
                "tier": cells[4].strip(),
                "scope": cells[5].strip(),
                "anchor": cells[6].strip(),
                "teaches": cells[7].strip(),
                "status": cells[8].strip(),
                "opened": cells[9].strip(),
                "recheck": cells[10].strip(),
                "used_by": cells[11].strip(),
            }
        )
    return rows


def census_w04(rows: list[dict]) -> list[tuple[str, str]]:
    """Reproduce the census' W04 emission: (row id, normalised url) in file order."""
    url_seen: set[str] = set()
    url_scopes: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for r in rows:
        u = census_url(r["source"])
        scope_key = (u, r["scope"])
        if u and u in url_seen and scope_key not in url_scopes:
            out.append((r["id"], u))
        if u:
            url_seen.add(u)
            url_scopes.add(scope_key)
    return out


def census_same_scope_pairs(rows: list[dict]) -> list[tuple[str, str, str]]:
    """Rows that re-use a URL *and* the same scope (the census' E04 shape)."""
    seen: dict[tuple[str, str], str] = {}
    out = []
    for r in rows:
        u = census_url(r["source"])
        if not u:
            continue
        key = (u, r["scope"])
        if key in seen:
            out.append((seen[key], r["id"], u))
        else:
            seen[key] = r["id"]
    return out


# --------------------------------------------------------------------------- lexical signals

WORD_RE = re.compile(r"--?[A-Za-z0-9_]+|[A-Za-z0-9_]+(?:[-/][A-Za-z0-9_.]+)*")

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has", "have",
    "in", "is", "it", "its", "of", "on", "or", "that", "the", "their", "them", "then",
    "there", "these", "this", "those", "to", "was", "were", "which", "with", "not", "no",
    "do", "does", "did", "can", "cannot", "only", "other", "others", "such", "than",
    "when", "where", "while", "who", "why", "how", "all", "any", "each", "same", "so",
    "up", "out", "over", "under", "again", "further", "once", "here", "there", "both",
    "after", "before", "because", "if", "into", "more", "most", "some", "own", "very",
    "just", "also", "own", "one", "two", "per", "via", "yet", "ever", "shall", "should",
    "must", "may", "might", "will", "would", "said", "say", "says", "according",
}

# page furniture: words that describe the *document*, not the claim.
FURNITURE = {
    "page", "pages", "man", "manual", "footer", "header", "section", "sections",
    "paragraph", "paragraphs", "line", "lines", "opened", "dated", "date", "snapshot",
    "fetch", "fetched", "read", "reads", "sha256", "sha", "blob", "commit", "tag",
    "tags", "version", "versions", "opened", "recheck", "status", "scope", "anchor",
    "teaches", "kind", "tier", "id", "row", "rows", "source", "registry", "census",
    "§", "bullet", "quote", "quoted", "excerpt",
}

SUPERSEDE_RE = re.compile(
    r"(?i)\b(supersedes|superseded|restates|restated|replaces|replaced|re-?registers|"
    r"re-?registration|narrows|narrowed|reopens|reopen(ed)?|replaces)\b"
)
COMPLEMENT_RE = re.compile(r"(?i)\b(complements|complement|supplements|supplement|extends|extends)\b")

QUOTE_RE = re.compile(r'"([^"]{15,})"')
QUOTE_CURLY_RE = re.compile(r"“([^”]{15,})”")

IDENT_RE = re.compile(r"^(?:--?[A-Za-z][A-Za-z0-9-]*|[A-Za-z0-9_]*/[A-Za-z0-9_/]+|[A-Za-z0-9_]*_[A-Za-z0-9_]+|"
                      r"[A-Za-z]+[A-Z][A-Za-z]*=?)$")

CLASS_RE_REGISTRATION = "same-page re-registration with a different scope"
CLASS_SAME_SCOPE = "same scope duplicate"
CLASS_DIFFERENT_ANCHOR = "different anchor on one URL"


def norm_text(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def norm_scope(s: str) -> str:
    return re.sub(r"[\s.;,]+$", "", norm_text(s))


def content_tokens(s: str) -> list[str]:
    out = []
    for t in WORD_RE.findall(norm_text(s)):
        t = t.strip("-_")
        if not t or t in STOPWORDS or t in FURNITURE:
            continue
        if re.fullmatch(r"[\d.,:/-]+", t):
            continue
        out.append(t)
    return out


def quoted_spans(s: str) -> set[str]:
    spans = set()
    for m in QUOTE_RE.finditer(s):
        spans.add(norm_text(m.group(1)))
    for m in QUOTE_CURLY_RE.finditer(s):
        spans.add(norm_text(m.group(1)))
    return {sp for sp in spans if len(sp) >= 15}


OPTION_RE = re.compile(r"(?<![A-Za-z0-9_])--?[A-Za-z][A-Za-z0-9-]*")
CODEISH_RE = re.compile(r"[A-Za-z0-9_]*(?:[_/=][A-Za-z0-9_.]+)+")
CAMEL_RE = re.compile(r"(?<![A-Za-z0-9_])[a-z]+[A-Z][A-Za-z0-9]*")


def identifiers(s: str) -> set[str]:
    """Code-ish identifiers only: options, settings, paths, snake_case, CamelCase.

    Prose compounds ("package-manager", "read-only", "pre-upgrade") are *not*
    identifiers: two unrelated rows about one man page share them by accident, and
    counting them would turn every same-URL pair into a "re-registration".
    Single-letter options (-S, -R, -U) are dropped for the same reason.
    """
    out: set[str] = set()
    for m in OPTION_RE.finditer(s):
        tok = m.group(0).lstrip("-").lower()
        if len(tok) >= 2:
            out.add(tok)
    for m in CODEISH_RE.finditer(s):
        tok = m.group(0).lower()
        if len(tok) >= 3 and tok not in FURNITURE:
            out.add(tok)
    for m in CAMEL_RE.finditer(s):
        out.add(m.group(0).lower())
    return {t for t in out if t not in FURNITURE and t not in STOPWORDS}


def anchor_chunks(anchor: str) -> set[str]:
    """Locator phrases of the anchor cell: ';'/'§'/':'-delimited chunks, furniture dropped."""
    chunks = set()
    work = anchor.replace("§", ";")
    for part in re.split(r"[;:]", work):
        part = part.strip().strip("`").strip()
        if len(part) < 6:
            continue
        toks = [t for t in WORD_RE.findall(norm_text(part))]
        if not toks:
            continue
        furn = sum(1 for t in toks if t.strip("-") in FURNITURE or re.fullmatch(r"[\d.,/-]+", t))
        if furn >= max(1, int(0.6 * len(toks))):
            continue
        chunks.add(re.sub(r"\s+", " ", norm_text(part)))
    return chunks


def containment(a: list[str], b: list[str]) -> float:
    """intersection / min(|a|,|b|) over content words."""
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / min(len(sa), len(sb))


def mention_type(later_text: str, earlier_id: str) -> str:
    """How does the later row talk about the earlier row? none|supersede|complement|other."""
    kinds = set()
    for m in re.finditer(re.escape(earlier_id), later_text):
        ctx = later_text[max(0, m.start() - 90): m.end() + 90]
        if SUPERSEDE_RE.search(ctx):
            kinds.add("supersede")
        elif COMPLEMENT_RE.search(ctx):
            kinds.add("complement")
        else:
            kinds.add("other")
    if not kinds:
        return "none"
    for k in ("supersede", "complement", "other"):
        if k in kinds:
            return k
    return "none"


def pair_signals(earlier: dict, later: dict) -> dict:
    e_text = " ".join([earlier["scope"], earlier["anchor"], earlier["teaches"]])
    l_text = " ".join([later["scope"], later["anchor"], later["teaches"]])
    e_q = quoted_spans(e_text)
    l_q = quoted_spans(l_text)
    e_i = identifiers(e_text)
    l_i = identifiers(l_text)
    e_c = content_tokens(earlier["teaches"])
    l_c = content_tokens(later["teaches"])
    return {
        "mention": mention_type(l_text, earlier["id"]),
        "shared_quote": sorted(e_q & l_q),
        "shared_identifiers": sorted(e_i & l_i),
        "shared_anchor_chunks": sorted(anchor_chunks(earlier["anchor"]) & anchor_chunks(later["anchor"])),
        "content_containment": round(containment(l_c, e_c), 3),
        "scope_equal": norm_scope(earlier["scope"]) == norm_scope(later["scope"]),
    }


def classify(earlier: dict, later: dict, sig: dict, threshold: float) -> tuple[str, str]:
    """Return (class, the rule that decided it)."""
    if sig["scope_equal"]:
        return CLASS_SAME_SCOPE, "R0 identical scope string"
    if sig["mention"] == "supersede":
        return CLASS_RE_REGISTRATION, "R1 later row supersedes/restates the earlier row id"
    if sig["shared_quote"]:
        return CLASS_RE_REGISTRATION, "R2 both rows cite the same quoted passage"
    if sig["shared_anchor_chunks"]:
        return CLASS_RE_REGISTRATION, "R3 both rows cite the same anchor location"
    if len(sig["shared_identifiers"]) >= 2:
        return CLASS_RE_REGISTRATION, "R4 both rows cite the same code identifiers"
    if sig["content_containment"] >= threshold:
        return CLASS_RE_REGISTRATION, f"R5 later claim restates the earlier one (containment {sig['content_containment']})"
    return CLASS_DIFFERENT_ANCHOR, "R6 no shared evidence: distinct anchors on one page"


def counterpart_score(earlier: dict, later: dict, sig: dict) -> float:
    score = 0.0
    if sig["mention"] == "supersede":
        score += 6.0
    if sig["mention"] in ("supersede", "complement", "other"):
        score += 3.0
    score += 3.0 * len(sig["shared_quote"])
    score += 1.0 * min(len(sig["shared_identifiers"]), 3)
    score += 2.0 * sig["content_containment"]
    score += 1.0 * containment(content_tokens(later["scope"]), content_tokens(earlier["scope"]))
    return score


def pick_counterpart(candidates: list[dict], later: dict) -> tuple[dict, dict, float]:
    best = None
    for cand in candidates:
        sig = pair_signals(cand, later)
        score = counterpart_score(cand, later, sig)
        if best is None or score > best[2] + 1e-9:
            best = (cand, sig, score)
    return best


# --------------------------------------------------------------------------- census cross-check


def run_census(census: str, repo: str, revision: str, lane: str) -> tuple[list[str], int]:
    """Run the real census on the revision's SOURCES.md and return its W04 lines."""
    with tempfile.TemporaryDirectory(prefix="w04-classify-") as tmp:
        os.makedirs(os.path.join(tmp, "corpus"), exist_ok=True)
        target = os.path.join(tmp, "corpus", "SOURCES.md")
        blob = subprocess.run(
            ["git", "-C", repo, "show", f"{revision}:corpus/SOURCES.md"],
            check=True, capture_output=True, text=True,
        ).stdout
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(blob)
        for sub in ("knowledge", "lessons"):
            src = os.path.join(repo, "corpus", sub)
            dst = os.path.join(tmp, "corpus", sub)
            if os.path.isdir(src) and not os.path.exists(dst):
                os.symlink(src, dst)
        proc = subprocess.run(
            ["bash", census, "validate", "--today", "2026-10-22", "--file", target],
            capture_output=True, text=True,
        )
        w04 = [ln for ln in proc.stdout.splitlines() if "\tW04\t" in ln]
        return w04, proc.returncode


# --------------------------------------------------------------------------- main


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True, help="git repository holding corpus/SOURCES.md")
    ap.add_argument("--revision", required=True, help="revision to read corpus/SOURCES.md at")
    ap.add_argument("--census", help="path to the fleet scripts/sources-census.sh (cross-check)")
    ap.add_argument("--lane", default="tsukuroi", help="lane label used in census output")
    ap.add_argument("--threshold", type=float, default=0.35,
                    help="content-word containment that marks a re-registration (default 0.35)")
    ap.add_argument("--json", action="store_true", help="emit the pair table as JSON")
    ap.add_argument("--verbose", action="store_true", help="print the matching signals per pair")
    args = ap.parse_args(argv)

    blob = subprocess.run(
        ["git", "-C", args.repo, "show", f"{args.revision}:corpus/SOURCES.md"],
        check=True, capture_output=True, text=True,
    ).stdout
    rows = parse_registry(blob)
    by_id = {r["id"]: r for r in rows}
    order = {r["id"]: i for i, r in enumerate(rows)}
    w04 = census_w04(rows)

    # group rows by normalised url, keeping file order
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        u = census_url(r["source"])
        if u:
            groups[u].append(r)

    pairs = []
    for later_id, url in w04:
        later = by_id[later_id]
        candidates = [r for r in groups[url] if order[r["id"]] < order[later_id]]
        if not candidates:
            continue
        earlier, sig, score = pick_counterpart(candidates, later)
        klass, reason = classify(earlier, later, sig, args.threshold)
        pairs.append(
            {
                "later": later_id,
                "earlier": earlier["id"],
                "url": url,
                "class": klass,
                "reason": reason,
                "later_opened": later["opened"],
                "signals": sig,
                "counterpart_score": round(score, 3),
                "later_scope": later["scope"],
                "earlier_scope": earlier["scope"],
            }
        )

    counts = Counter(p["class"] for p in pairs)
    same_scope_pairs = census_same_scope_pairs(rows)

    if not args.json:
        print(f"repo        : {args.repo}")
        print(f"revision    : {args.revision}")
        print(f"registry    : {len(rows)} rows, {len(groups)} distinct URLs, "
              f"{sum(1 for v in groups.values() if len(v) > 1)} URLs used by more than one row")
        print(f"W04 (census-parity replica): {len(w04)}")
        if args.census:
            real, rc = run_census(args.census, args.repo, args.revision, args.lane)
            # the census prints "lane<TAB>W04<TAB><id> <text>"; the lane label is
            # "file" for --file runs, so compare the (id, text) payload only.
            def payload(lines):
                out = set()
                for ln in lines:
                    parts = ln.strip().split("\t")
                    if len(parts) < 3 or parts[1] != "W04":
                        continue
                    rowid, _, rest = parts[2].partition(" ")
                    out.add((rowid, rest))
                return out
            mine = {(rowid, f"duplicate url {url} across scopes") for rowid, url in w04}
            theirs = payload(real)
            print(f"census cross-check: exit {rc}, {len(theirs)} W04 lines, "
                  f"identical to replica: {theirs == mine}")
            if theirs != mine:
                for ln in sorted(theirs - mine):
                    print(f"  only in census : {ln}")
                for ln in sorted(mine - theirs):
                    print(f"  only in replica: {ln}")
        print(f"same URL+same scope pairs (E04 shape): {len(same_scope_pairs)} "
              f"{[f'{a}/{b}' for a, b, _ in same_scope_pairs]}")
        print()
        print("counts:")
        for k in (CLASS_RE_REGISTRATION, CLASS_SAME_SCOPE, CLASS_DIFFERENT_ANCHOR):
            print(f"  {counts.get(k, 0):>3}  {k}")
        print(f"  {sum(counts.values()):>3}  total W04 pairs")
        print()
        print("why (rule that decided each pair):")
        for rule, n in sorted(Counter(p["reason"].split(" ")[0] for p in pairs).items()):
            print(f"  {n:>3}  {rule}")
        print()
        print("re-registrations by the later row's opened date:")
        for opened, n in sorted(Counter(
                p["later_opened"] for p in pairs if p["class"] == CLASS_RE_REGISTRATION).items()):
            print(f"  {n:>3}  opened {opened}")
        sup = [p for p in pairs if p["signals"]["mention"] == "supersede"]
        print(f"re-registrations that explicitly supersede an existing row: {len(sup)} "
              f"({', '.join(p['later'] for p in sup)})")
        print(f"  of those, opened {sorted({p['later_opened'] for p in sup})[-1]}: "
              f"{sum(1 for p in sup if p['later_opened'] == '2026-10-22')}")
        print()
        print("pairs:")
        for p in pairs:
            s = p["signals"]
            sig = (f"mention={s['mention']} quotes={len(s['shared_quote'])} "
                   f"idents={len(s['shared_identifiers'])} chunks={len(s['shared_anchor_chunks'])} "
                   f"contain={s['content_containment']}")
            print(f"  {p['earlier']} -> {p['later']:<5} {p['class']:<46} {p['url'][:60]}")
            print(f"      {p['reason']}")
            print(f"      {sig}")
            if args.verbose:
                if s["shared_quote"]:
                    print(f"      quote : {s['shared_quote'][0][:110]}")
                if s["shared_identifiers"]:
                    print(f"      idents: {', '.join(s['shared_identifiers'])}")
                if s["shared_anchor_chunks"]:
                    print(f"      chunk : {s['shared_anchor_chunks'][0][:110]}")
                print(f"      scope : {p['earlier_scope'][:100]}")
                print(f"           -> {p['later_scope'][:100]}")
    else:
        print(json.dumps({"counts": dict(counts), "pairs": pairs}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
