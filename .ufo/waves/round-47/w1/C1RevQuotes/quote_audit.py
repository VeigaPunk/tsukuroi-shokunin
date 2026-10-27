#!/usr/bin/env python3
"""C1RevQuotes independent quote audit parser (own implementation, not the frozen counter).

Parses **Quote.** lines from GR1/GR2/GR3 of the freeze-revision grounding doc, maps S###/file/line
to the pinned snapshots, and compares quoted text to the cited line with whitespace normalization.
"""
import hashlib, json, re, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
DOC = Path("/fast/scratch/hyaku/tsukuroi-r47/C1RevQuotes/grounding.md")

SRC = LANE / ".ufo/waves/round-45/frozen/src"
SRC44 = LANE / ".ufo/waves/round-44/frozen/src"
SRC42 = LANE / ".ufo/waves/round-42/frozen/src"
HOSTCAP = LANE / ".ufo/waves/round-45/frozen/hostcap/capture.txt"

SMAP = {
    "S246": SRC, "S247": SRC, "S248": SRC,
    "S242": SRC44, "S243": SRC44, "S244": SRC44,
    "S237": SRC42,
}
# pinned digests copied from each dir's SHA256SUMS (verified earlier via sha256sum -c)
EXPECTED = {
    "cmdline.c": "1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d",
    "dev-replace.c": "f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a",
    "systemd.kill.xml": "448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72",
    "kstrtox.c": "0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4",
    "vsprintf.c": "cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca",
    "scrub.c": "f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8",   # S242 round-44
    "sysfs.c": "ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43",
    "btrfs-scrub@.service": "eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252",
    "scrub.c|S237": "48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801",  # round-42
}

QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` (\S+):(\d+): "(.*)"\s*$')
H2_RE = re.compile(r'^## ')

def norm(s: str) -> str:
    return " ".join(s.split())

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    lines = DOC.read_text().splitlines()
    # locate headers
    hdr_idx = {}
    for i, l in enumerate(lines, 1):
        if l.startswith("## "):
            hdr_idx.setdefault(l.strip(), []).append(i)
    # row extents with fail-closed unexpected-header rule
    rows = {}
    bounds = [("GR1", "## GR1", "## GR2"), ("GR2", "## GR2", "## GR3"),
              ("GR3", "## GR3", "## How this changes OS triage")]
    structural_problems = []
    for name, start, end in bounds:
        if start not in hdr_idx:
            structural_problems.append(f"{name}: start header {start} missing")
            continue
        s = hdr_idx[start][0]
        if end not in hdr_idx:
            structural_problems.append(f"{name}: end header {end} missing")
            continue
        e = hdr_idx[end][0]
        if e <= s:
            structural_problems.append(f"{name}: end header {end} misordered before {start}")
            continue
        interior = [l for l in lines[s:e-1] if H2_RE.match(l)]
        if interior:
            structural_problems.append(f"{name}: unexpected '## ' inside extent: {interior}")
        rows[name] = (s, e)
    quotes = []
    for name, (s, e) in rows.items():
        for ln in range(s, e):
            m = QUOTE_RE.match(lines[ln-1])
            if m:
                quotes.append((name, ln, m.group(1), m.group(2), int(m.group(3)), m.group(4)))
    results = []
    digest_ok = True
    for row, qln, sid, fname, lineno, text in quotes:
        base = SMAP.get(sid)
        if base is None:
            results.append((row, qln, sid, fname, lineno, "FAIL", f"source {sid} not in pinned map"))
            continue
        fpath = base / fname
        if not fpath.exists():
            results.append((row, qln, sid, fname, lineno, "FAIL", "snapshot file missing"))
            continue
        key = fname if sid != "S237" else "scrub.c|S237"
        actual = sha256(fpath)
        if EXPECTED.get(key) != actual:
            digest_ok = False
            results.append((row, qln, sid, fname, lineno, "FAIL", f"digest mismatch {actual}"))
            continue
        fline = fpath.read_text(errors="replace").splitlines()[lineno-1]
        if norm(fline) == norm(text):
            verdict = "VERIFY"
            note = ""
        else:
            verdict = "FAIL"
            note = f"line={norm(fline)!r}"
        results.append((row, qln, sid, fname, lineno, verdict, note))
    n_verify = sum(1 for r in results if r[5] == "VERIFY")
    n_fail = sum(1 for r in results if r[5] == "FAIL")
    print(json.dumps({
        "structural_problems": structural_problems,
        "row_extents": {k: list(v) for k, v in rows.items()},
        "quote_count": len(quotes),
        "verify": n_verify, "fail": n_fail, "digests_ok": digest_ok,
        "per_quote": [[r, q, f"{s} {f}:{n}", v, note] for r, q, s, f, n, v, note in results],
    }, indent=1))

if __name__ == "__main__":
    main()
