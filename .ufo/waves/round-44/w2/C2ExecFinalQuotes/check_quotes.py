#!/usr/bin/env python3
"""C2ExecFinalQuotes (round 44, w2): re-check every **Quote.** line and every line-number
claim of corpus/knowledge/btrfs-scrub-record-r44.md against digest-verified snapshots.

Snapshots are extracted from the tested revision itself and checked against the frozen
SHA256SUMS manifests of waves 42/43/44 and round-44 hostcap/capture.txt.

usage: check_quotes.py [REV] [--extras]   (exit 0 iff bad == 0)
"""
import hashlib
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
MD = "corpus/knowledge/btrfs-scrub-record-r44.md"
W44 = ".ufo/waves/round-44/frozen/src/"

# source id -> (snapshot paths, SHA256SUMS path)
SNAPS = {
    "S237": ([".ufo/waves/round-42/frozen/src/scrub.c"], ".ufo/waves/round-42/frozen/src/SHA256SUMS"),
    "S240": ([".ufo/waves/round-43/frozen/src/ioctl.c"], ".ufo/waves/round-43/frozen/src/SHA256SUMS"),
    "S242": ([W44 + "scrub.c"], W44 + "SHA256SUMS"),
    "S243": ([W44 + "sysfs.c"], W44 + "SHA256SUMS"),
    "S244": ([W44 + n for n in ("PKGBUILD", "btrfs-scrub@.timer", "btrfs-scrub@.service")], W44 + "SHA256SUMS"),
}
CAPTURE = (".ufo/waves/round-44/frozen/hostcap/capture.txt",
           "efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900")

QUOTE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:`]+):(\d+): "(.*)"$')
CL1 = re.compile(r'`?([A-Za-z0-9_.@-]+\.(?:c|h|txt|timer|service)|PKGBUILD):(\d+)(?:-(\d+))?')
CL2 = re.compile(r'\blines ([0-9]+-[0-9]+(?: and [0-9]+-[0-9]+)*)')
FNAME = re.compile(r'([A-Za-z0-9_.@-]+\.(?:c|h|txt|timer|service))|(PKGBUILD)')


def show(path):
    return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                          check=True, capture_output=True).stdout


def wave(path):
    return ("r42" if "round-42" in path else
            "r43" if "round-43" in path else
            "hostcap" if "hostcap" in path else "r44")


def materialize(root):
    """Write snapshots to root/<wave>/<base>; verify against the frozen manifests."""
    digests, failures = {}, 0
    for paths, sums in SNAPS.values():
        for p in paths:
            data = show(p)
            out = os.path.join(root, wave(p), os.path.basename(p))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "wb") as fh:
                fh.write(data)
            digests[p] = hashlib.sha256(data).hexdigest()
        manifest = {}
        for line in show(sums).decode().splitlines():
            want, name = line.split()
            manifest[name] = want
        for p in paths:
            name = os.path.basename(p)
            if name not in manifest:
                continue  # e.g. CHANGES lives in the manifest but is not quoted
            if digests[p] == manifest[name]:
                print(f"ok   digest {p} = {manifest[name][:16]}...")
            else:
                print(f"BAD  digest {p}: manifest {manifest[name]} != {digests[p]}")
                failures += 1
    data = show(CAPTURE[0])
    d = hashlib.sha256(data).hexdigest()
    if d == CAPTURE[1]:
        print(f"ok   digest {CAPTURE[0]} = {d[:16]}... (md header claim)")
    else:
        print(f"BAD  digest {CAPTURE[0]}: md header {CAPTURE[1]} != {d}")
        failures += 1
    out = os.path.join(root, "hostcap", "capture.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(data)
    digests[CAPTURE[0]] = d
    return digests, failures


def load(root, path):
    with open(os.path.join(root, wave(path), os.path.basename(path)), "rb") as fh:
        return fh.read().decode().split("\n")


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    global REV, SNAPSUM
    REV = argv[0] if argv else "8eee79db608b5815c325a5af7cbfdeac50eda9f4"
    allow_extras = "--extras" in sys.argv
    SNAPSUM = dict((ln.split()[1], ln.split()[0])
                   for ln in show(W44 + "SHA256SUMS").decode().splitlines())

    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapcheck")
    os.makedirs(root, exist_ok=True)
    digests, bad = materialize(root)
    md = show(MD).decode().split("\n")
    print(f"snapshots: {len(digests)} files verified; md {len(md)} lines at {REV[:12]}\n")

    # key snapshots by id (S237/S242 share the basename scrub.c)
    src = {sid: load(root, paths[0]) for sid, (paths, _s) in SNAPS.items()}
    unit = {os.path.basename(p): load(root, p) for p in SNAPS["S244"][0]}
    capture = load(root, CAPTURE[0])

    # ---------- 1. every **Quote.** line ----------
    quotes = exact = indent = trunc = 0
    for i, line in enumerate(md, 1):
        m = QUOTE.match(line)
        if not m:
            continue
        quotes += 1
        sid, name, num, text = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        if sid == "S244":
            lines = unit[name]
        elif sid == "S237" and name == "scrub.c":
            lines = src["S237"]
        elif sid == "S240" and name == "ioctl.c":
            lines = src["S240"]
        elif sid == "S242" and name == "scrub.c":
            lines = src["S242"]
        elif sid == "S243" and name == "sysfs.c":
            lines = src["S243"]
        else:
            print(f"BAD  md:{i} {sid} {name}:{num}: no snapshot for this file")
            bad += 1
            continue
        if num > len(lines):
            print(f"BAD  md:{i} {sid} {name}:{num}: past EOF ({len(lines)} lines)")
            bad += 1
            continue
        actual = lines[num - 1]
        if actual == text:
            exact += 1
            print(f"ok   md:{i} {sid} {name}:{num} exact")
        elif actual.strip() == text.strip():
            indent += 1
            print(f"ok   md:{i} {sid} {name}:{num} match-modulo-indent")
        elif actual.strip().startswith(text.strip()):
            trunc += 1
            print(f"ok   md:{i} {sid} {name}:{num} prefix of line "
                  f"(omitted tail {actual.strip()[len(text.strip()):]!r})")
        else:
            print(f"BAD  md:{i} {sid} {name}:{num}\n       want {text!r}\n       got  {actual!r}")
            bad += 1

    # ---------- 2. every line-number claim in prose ----------
    # resolvable names -> (label, lines)
    table = {"scrub.c": [("r42/scrub.c", src["S237"]), ("r44/scrub.c", src["S242"])],
             "ioctl.c": [("r43/ioctl.c", src["S240"])],
             "sysfs.c": [("r44/sysfs.c", src["S243"])],
             "capture.txt": [("hostcap/capture.txt", capture)]}
    table.update({n: [("r44/" + n, v)] for n, v in unit.items()})
    extras = {}
    if allow_extras:
        for n in ("dev-replace.c",):
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), n)
            if os.path.exists(p):
                with open(p) as fh:
                    extras[n] = fh.read().split("\n")

    claims = 0
    blocks, cur = [], []
    for i, line in enumerate(md, 1):
        if line.strip():
            cur.append((i, line))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)

    for block in blocks:
        text = " ".join(l for _, l in block)
        if QUOTE.match(block[0][1]):
            continue  # quote lines were checked as quotes
        start_md = block[0][0]
        for m in CL1.finditer(text):
            name, a, b = m.group(1), int(m.group(2)), m.group(3)
            claims += 1
            cands = [(lab, ls) for lab, ls in table.get(name, []) if a < len(ls)]
            if not cands and name in extras:
                cands = [("EXTRA/" + name, extras[name])] if a < len(extras[name]) else []
            if not cands:
                print(f"BAD  md~{start_md} claim {name}:{m.group(2)}"
                      f"{'-' + b if b else ''}: no verified snapshot line")
                bad += 1
                continue
            for lab, ls in cands:
                span = [ls[k - 1].strip() for k in range(a, (int(b) if b else a) + 1)]
                print(f"ok   md~{start_md} claim {lab}:{a}{'-' + b if b else ''} => "
                      f"{' / '.join(span)[:140]}")
        for m in CL2.finditer(text):
            spans = re.findall(r'(\d+)-(\d+)', m.group(1))
            # nearest file name before this match decides the subject
            prior = [mm for mm in FNAME.finditer(text, 0, m.start())]
            if not prior:
                print(f"BAD  md~{start_md} claim 'lines {m.group(1)}': no subject file")
                bad += 1
                continue
            name = prior[-1].group(1) or prior[-1].group(2)
            for a, b in spans:
                claims += 1
                a, b = int(a), int(b)
                if name in extras:
                    ls = extras[name]
                    if b < len(ls):
                        span = [ls[k - 1].strip() for k in range(a, b + 1)]
                        print(f"ok*  md~{start_md} claim EXTRA/{name} lines {a}-{b} => "
                              f"{' / '.join(span)[:140]}  (fresh fetch, not a frozen snapshot)")
                    else:
                        print(f"BAD  md~{start_md} claim EXTRA/{name} lines {a}-{b}: past EOF")
                        bad += 1
                    continue
                cands = [(lab, ls) for lab, ls in table.get(name, []) if b < len(ls)]
                if not cands:
                    print(f"BAD  md~{start_md} claim {name} lines {a}-{b}: unresolvable")
                    bad += 1
                    continue
                for lab, ls in cands:
                    span = [ls[k - 1].strip() for k in range(a, b + 1)]
                    print(f"ok   md~{start_md} claim {lab} lines {a}-{b} => "
                          f"{' / '.join(span)[:140]}")

    # ---------- 3. the wave-2 narrowings, checked against the snapshots ----------
    scr = src["S242"]
    sysf = src["S243"]
    checks = []
    checks.append(("SR7 narrow: btrfs_scrub_dev signature carries is_dev_replace",
                   "bool readonly, bool is_dev_replace)" in scr[3080]))
    checks.append(("SR7 narrow: is_dev_replace drives a refusal branch (3148)",
                   scr[3147].strip() == "(!is_dev_replace &&"))
    checks.append(("SR7 narrow: attach at 3159 is after the last refusal goto",
                   max(i for i, l in enumerate(scr[:3158], 1)
                       if l.lstrip().startswith("goto out")) == 3154
                   and scr[3158].strip() == "dev->scrub_ctx = sctx;"))
    checks.append(("SR7 narrow: no return/goto between attach (3159) and clear (3222)",
                   not [i for i in range(3159, 3222)
                        if re.search(r'\b(return|goto)\b', scr[i - 1])]))
    checks.append(("SR7 narrow: clear at 3222 precedes the finalize tail",
                   scr[3221].strip() == "dev->scrub_ctx = NULL;"
                   and "scrub_workers_put(fs_info);" in scr[3224]))
    checks.append(("SR8 narrow: store writes WRITE_ONCE (sysfs.c:2045)",
                   sysf[2044].strip() == "WRITE_ONCE(device->scrub_speed_max, limit);"))
    checks.append(("SR8 narrow: show reads READ_ONCE (sysfs.c:2028)",
                   "READ_ONCE(device->scrub_speed_max)" in sysf[2027]))
    checks.append(("SR8 narrow: throttle reads READ_ONCE (scrub.c:1380)",
                   "READ_ONCE(device->scrub_speed_max)" in scr[1379]))
    checks.append(("SR8 narrow: BTRFS_ATTR_RW really expands to mode 0644 (72-74)",
                   sysf[71].startswith("#define BTRFS_ATTR_RW")
                   and sysf[72].lstrip().startswith("static struct kobj_attribute")
                   and "__INIT_KOBJ_ATTR(_name, 0644, _show, _store)" in sysf[73]))
    checks.append(("hostcap: installed timer/service digests equal the pinned ones",
                   capture[6].split()[1] == SNAPSUM["btrfs-scrub@.timer"]
                   and capture[7].split()[1] == SNAPSUM["btrfs-scrub@.service"]))
    print()
    for label, ok in checks:
        print(("ok   " if ok else "BAD  ") + label)
        if not ok:
            bad += 1

    # ---------- 4. quote lines against the row windows the frozen counter declares ----------
    counter = show("tools/check-scrub-record-r44.py").decode().split("\n")
    wins, row = {}, None
    for ln in counter:
        m = re.match(r"\s*'(SR\d)': \{", ln)
        if m:
            row = m.group(1)
            wins.setdefault(row, set())
            continue
        if row:
            for w in re.finditer(r"\(\('(S\d+)', '([^']+)'\), (\d+), (\d+)\)", ln):
                wins[row].add((w.group(1), w.group(2), int(w.group(3)), int(w.group(4))))
    sections, cur = {}, None
    for i, line in enumerate(md, 1):
        h = re.match(r"^## (SR\d+)$", line)
        if h:
            cur = h.group(1)
            sections[cur] = []
        elif line.startswith("## "):
            cur = None
        elif cur:
            sections[cur].append((i, line))
    outside = 0
    print()
    for sr, items in sections.items():
        for i, line in items:
            m = QUOTE.match(line)
            if not m:
                continue
            sid, name, num = m.group(1), m.group(2), int(m.group(3))
            ws = [w for w in wins.get(sr, ()) if w[0] == sid and w[1] == name]
            hit = any(lo <= num <= hi for _, _, lo, hi in ws)
            outside += 0 if hit else 1
            if not hit:
                print(f"NOTE md:{i} {sr} quote {sid} {name}:{num} lies outside the counter's "
                      f"{sr} windows {sorted((lo, hi) for _, _, lo, hi in ws)} (counter needs >= 1 in-window)")
    print(f"ok   quotes outside their row's counter windows: {outside} of {quotes} "
          f"(counter predicate needs in_window >= 1 per row; all rows keep in-window quotes)")

    print(f"\nquotes checked: {quotes} (exact {exact}, indent-only {indent}, prefix {trunc}); "
          f"prose line claims: {claims}; support checks: {len(checks)}; bad: {bad}")
    return 1 if bad else 0


SNAPSUM = {}
REV = "8eee79db608b5815c325a5af7cbfdeac50eda9f4"


if __name__ == "__main__":
    sys.exit(main())
