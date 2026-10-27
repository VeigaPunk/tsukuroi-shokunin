VERDICT: supports

# C2ExecFinalQuotes — item C2-1: every `**Quote.**` line and every line-number claim at the tip

Seat: C2ExecFinalQuotes (w2, leaf). Tested revision `8eee79db608b5815c325a5af7cbfdeac50eda9f4`.
Entry: `corpus/knowledge/btrfs-scrub-record-r44.md`, blob `8fb2ac7671c2b811938ba41aea2054a7cd68f1af`,
sha256 `a4b975a04453405df4ed03c4a1c5fd9917f422b9bc3f146b09fa14a994308676`, 149 lines.
The identical blob exists at w1's integration commit `071ab0d1` (`git diff --stat 071ab0d1 <tip> --
<entry>` is empty), so this re-check covers exactly the quote set w2 inherits: w1 changed no quote
after integrating.

## Result

```
quotes checked: 33 (exact 8, indent-only 24, prefix 1); prose line claims: 12; support checks: 10; bad: 0
```

0 bad. Every one of the 33 `**Quote.**` lines resolves to the file and line it names, inside the
digest-verified snapshot of the revision under test, with the quoted text present at that line; none
is wrong-file, wrong-line or wrong-text. All 12 line-number claims in the prose (2 kernel `scrub.c`,
2 `dev-replace.c`, 8 `capture.txt`) resolve as well. No claim is falsified, so this item does not
falsify w1's work.

Snapshots are extracted from `<rev>:<path>` by my own script and checked against the frozen
manifests before any comparison: r42 `scrub.c` `48df2e2f…f0801`, r43 `ioctl.c` `7b3488f2…4ba01`,
r44 `scrub.c` `f347931b…938ca5b8`, `sysfs.c` `ce146120…731c43`, `btrfs-scrub@.timer`
`9a0b6cc2…96f8ad`, `btrfs-scrub@.service` `eaa7af92…b240252`, `PKGBUILD` `3b803e8b…c10ce98`, and
the md header's own `capture.txt` digest `efb52388…3e84900`. The older two were re-confirmed from
their fetch logs: r42 = `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`
(btrfs-progs v7.1, so `S237 scrub.c` and `S242 scrub.c` really are the two different files the entry
says they are), r43 = `.../gregkh/linux/v7.2.11/fs/btrfs/ioctl.c`.

Match quality: 8 quotes reproduce their line byte-for-byte; 24 reproduce it modulo leading
indentation (the corpus convention in rounds 42 and 43); 1 is a strict prefix of its line (below).
I also checked that a quote's text is not merely present *somewhere*: the comparison is against the
single line the md names, and where the same stripped text occurs elsewhere (5 cases: `scrub.c:3331`,
`scrub.c:3333`, `ioctl.c:3141`, `sysfs.c:72`, `sysfs.c:2044`) I read the surrounding function and
confirmed the named line is the intended occurrence (`btrfs_scrub_progress` 3321-3337,
`btrfs_ioctl_scrub_progress` 3126-3145, the `BTRFS_ATTR_RW` macro body 72-74,
`btrfs_devinfo_scrub_speed_max_store` 2031-2047).

## The two w1 narrowings specifically

SR7 narrowed text (`btrfs_scrub_dev` also serves device replace; attach/clear line numbers added):
the signature at 3079-3081 carries `bool readonly, bool is_dev_replace)` (the quoted line 3081),
3148 uses the argument in the refusal branch (`(!is_dev_replace &&`), the attach at 3159 follows the
last refusal `goto out` (3154) and precedes all scrub work, and the clear at 3222 follows
`scrub_enumerate_chunks` (3208) and the progress copy (3215) while preceding the finalize tail
(`scrub_workers_put` 3225). The sentence "every return path leaves the field as it found it" holds
structurally: the returns in `btrfs_scrub_dev` (3079-3254) are 3095, 3111 and the
`goto out`/`out_free_ctx` at 3116/3124/3134/3143/3154 — all before the attach — plus 3240/3247 after
the clear, and there is no `return`/`goto` at all between 3159 and 3222, so every path that attaches
also clears. The `dev-replace.c` citation the narrowing introduced (`lines 701-703 and 1265-1268`,
the pre-wave-1 draft said 1265-1267) is not in the pinned set; I fetched it fresh on two channels
(kernel.org plain and raw.githubusercontent, byte-identical, sha256
`f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a`) and both spans are exactly
`btrfs_scrub_dev(..., &dev_replace->scrub_progress, false, true)` call sites — the corrected
`1265-1268` span is the right one.

SR8 new in-memory sentence: `btrfs_devinfo_scrub_speed_max_store` (2031-2047) is `memparse` 2040,
`skip_spaces` 2042, `if (*endptr != 0) return -EINVAL;` 2043-2044, `WRITE_ONCE(device->scrub_speed_max,
limit);` 2045, `return len;` 2046 — nothing else on the write path, so "written with `WRITE_ONCE` …
nothing on this write path persists it" is source-backed; the `READ_ONCE` halves are sysfs.c:2028
(show) and scrub.c:1380 (throttle, `if (bwlimit == 0) return;` 1381-1382). The
persistence/`kzalloc_obj` half is explicitly flagged `[inference]` and lies outside the frozen set
(`volumes.h`/`volumes.c` are not snapshotted), which is how the entry states it. `BTRFS_ATTR_RW`
(72-74) really does expand to `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)`, so the entry's mode
0644 claim is exact.

## Notes, not falsifiers

1. `md:69` / `sysfs.c:72` is a strict prefix of its line: the source line ends with the `#define`
   body's continuation (`#define BTRFS_ATTR_RW(...)\t\t\t\`), and the quote stops at `)`. The content
   is right and the counter's rule is substring containment (`q in src[n-1]`), so nothing fails; it
   is the only quote in the entry that is not the whole line modulo indentation.
2. `md:31` / `scrub.c:3081` sits outside the frozen counter's SR7 windows
   `(3140,3165) (3215,3226) (3321,3337)` — it is the widened signature line the w1 narrowing added.
   The counter needs ≥ 1 in-window quote per row and 8 SR7 quotes remain in-window, so the counter's
   predicate is untouched; recorded only so nobody reads the window list as exhaustive.
3. `PKGBUILD:100/101` are quoted with their two leading spaces stripped and without the enclosing
   `package()`/`install` indentation context; the FETCH.txt note "lines 99-101 install both units"
   matches the file (99 is the comment `# install scrub service/timer`, 100/101 the two `install`
   lines, 102 the closing brace).

## Proposed text (optional, cosmetic only — do not disturb the frozen claim)

At `md:69`, either keep the line continuation or mark the truncation so the quote is byte-faithful:

```
**Quote.** `S243` sysfs.c:72: "#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)"
```
→
```
**Quote.** `S243` sysfs.c:72: "#define BTRFS_ATTR_RW(_prefix, _name, _show, _store) \\"
```

and, since the 3081 quote is a declaration continuation, optionally name the declaration once at
`md:31`:

```
**Quote.** `S242` scrub.c:3081: "bool readonly, bool is_dev_replace)"   [signature starts 3079]
```

Neither is needed for any conjunct; the item's evidence does not depend on them.

## Script

`check_quotes.py` (also at `.ufo/waves/round-44/w2/C2ExecFinalQuotes/check_quotes.py`, sha256
`8f5b493b9bf01d87e1d7acfb720f0754ad13951f054232f68146a1bd0791cd00`). Run:
`TMPDIR=$PWD python3 check_quotes.py 8eee79db608b5815c325a5af7cbfdeac50eda9f4 --extras`
(exit 0 iff `bad == 0`; `--extras` enables the fresh `dev-replace.c` corroboration).

```python
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
```

## Result at `8eee79db608b5815c325a5af7cbfdeac50eda9f4` (verbatim `run-tip.log`)

```
ok   digest .ufo/waves/round-42/frozen/src/scrub.c = 48df2e2f468f7db7...
ok   digest .ufo/waves/round-43/frozen/src/ioctl.c = 7b3488f2f8356313...
ok   digest .ufo/waves/round-44/frozen/src/scrub.c = f347931b795c738d...
ok   digest .ufo/waves/round-44/frozen/src/sysfs.c = ce146120f29ac29c...
ok   digest .ufo/waves/round-44/frozen/src/PKGBUILD = 3b803e8b05d84900...
ok   digest .ufo/waves/round-44/frozen/src/btrfs-scrub@.timer = 9a0b6cc23f7bd97b...
ok   digest .ufo/waves/round-44/frozen/src/btrfs-scrub@.service = eaa7af92d28bfa89...
ok   digest .ufo/waves/round-44/frozen/hostcap/capture.txt = efb523889035cba6... (md header claim)
snapshots: 8 files verified; md 150 lines at 8eee79db608b

ok   md:31 S242 scrub.c:3081 match-modulo-indent
ok   md:33 S242 scrub.c:3147 match-modulo-indent
ok   md:35 S242 scrub.c:3153 match-modulo-indent
ok   md:37 S242 scrub.c:3159 match-modulo-indent
ok   md:39 S242 scrub.c:3222 match-modulo-indent
ok   md:41 S242 scrub.c:3321 exact
ok   md:43 S242 scrub.c:3331 match-modulo-indent
ok   md:45 S242 scrub.c:3333 match-modulo-indent
ok   md:47 S242 scrub.c:3336 match-modulo-indent
ok   md:49 S240 ioctl.c:3139 match-modulo-indent
ok   md:51 S240 ioctl.c:3141 match-modulo-indent
ok   md:69 S243 sysfs.c:72 prefix of line (omitted tail '\t\t\t\\')
ok   md:71 S243 sysfs.c:74 match-modulo-indent
ok   md:73 S243 sysfs.c:2028 match-modulo-indent
ok   md:75 S243 sysfs.c:2040 match-modulo-indent
ok   md:77 S243 sysfs.c:2042 match-modulo-indent
ok   md:79 S243 sysfs.c:2044 match-modulo-indent
ok   md:81 S243 sysfs.c:2048 exact
ok   md:83 S242 scrub.c:1380 match-modulo-indent
ok   md:85 S242 scrub.c:1381 match-modulo-indent
ok   md:102 S244 PKGBUILD:100 match-modulo-indent
ok   md:104 S244 PKGBUILD:101 match-modulo-indent
ok   md:106 S244 btrfs-scrub@.timer:5 exact
ok   md:108 S244 btrfs-scrub@.timer:7 exact
ok   md:110 S244 btrfs-scrub@.timer:8 exact
ok   md:112 S244 btrfs-scrub@.timer:11 exact
ok   md:114 S244 btrfs-scrub@.service:9 exact
ok   md:116 S244 btrfs-scrub@.service:10 exact
ok   md:118 S237 scrub.c:1293 match-modulo-indent
ok   md:120 S237 scrub.c:1295 match-modulo-indent
ok   md:122 S237 scrub.c:421 match-modulo-indent
ok   md:124 S237 scrub.c:1546 match-modulo-indent
ok   md:126 S237 scrub.c:969 match-modulo-indent
ok   md~17 claim r44/scrub.c:3159 => dev->scrub_ctx = sctx;
ok   md~17 claim r44/scrub.c:3222 => dev->scrub_ctx = NULL;
ok*  md~17 claim EXTRA/dev-replace.c lines 701-703 => ret = btrfs_scrub_dev(fs_info, src_device->devid, 0, / btrfs_device_get_total_bytes(src_device), / &dev_replace->scrub_progress, false, true  (fresh fetch, not a frozen snapshot)
ok*  md~17 claim EXTRA/dev-replace.c lines 1265-1268 => ret = btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid, / dev_replace->committed_cursor_left, / btrfs_device_get_total_bytes(dev_replace-  (fresh fetch, not a frozen snapshot)
ok   md~53 claim hostcap/capture.txt:1 => captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000
ok   md~87 claim hostcap/capture.txt:4 => scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0
ok   md~87 claim hostcap/capture.txt:1 => captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000
ok   md~128 claim hostcap/capture.txt:5 => wants_btrfs_scrub_instances 0
ok   md~128 claim hostcap/capture.txt:6 => is_enabled_btrfs-scrub@-.timer disabled
ok   md~128 claim hostcap/capture.txt:7 => installed_unit 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad  /usr/lib/systemd/system/btrfs-scrub@.timer
ok   md~128 claim hostcap/capture.txt:8 => installed_unit eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252  /usr/lib/systemd/system/btrfs-scrub@.service
ok   md~128 claim hostcap/capture.txt:9 => pacman_owner /usr/lib/systemd/system/btrfs-scrub@.timer is owned by btrfs-progs 7.1-1

ok   SR7 narrow: btrfs_scrub_dev signature carries is_dev_replace
ok   SR7 narrow: is_dev_replace drives a refusal branch (3148)
ok   SR7 narrow: attach at 3159 is after the last refusal goto
ok   SR7 narrow: no return/goto between attach (3159) and clear (3222)
ok   SR7 narrow: clear at 3222 precedes the finalize tail
ok   SR8 narrow: store writes WRITE_ONCE (sysfs.c:2045)
ok   SR8 narrow: show reads READ_ONCE (sysfs.c:2028)
ok   SR8 narrow: throttle reads READ_ONCE (scrub.c:1380)
ok   SR8 narrow: BTRFS_ATTR_RW really expands to mode 0644 (72-74)
ok   hostcap: installed timer/service digests equal the pinned ones

NOTE md:31 SR7 quote S242 scrub.c:3081 lies outside the counter's SR7 windows [(3140, 3165), (3215, 3226), (3321, 3337)] (counter needs >= 1 in-window)
ok   quotes outside their row's counter windows: 1 of 33 (counter predicate needs in_window >= 1 per row; all rows keep in-window quotes)

quotes checked: 33 (exact 8, indent-only 24, prefix 1); prose line claims: 12; support checks: 10; bad: 0
```

## Scope, guards, and what this item does not decide

- Read-only seat: I read the lane's git objects with `git show`/`git diff` and ran one read-only
  `curl` per channel for `dev-replace.c`; no lane file, no tracked file outside this report and its
  receipts, no git/jj mutation in the lane, no service/timer/sysfs/mount/scrub command, no pacman
  and no sudo. Every write stayed under `/fast/scratch/hyaku/tsukuroi-r44/C2ExecFinalQuotes`
  (removed on exit) and the two artefact paths below. No tool installs were needed or made.
- This item tests quotes and line numbers only. It does not re-run the C1 arm, the frozen counter's
  verdict, or the SR7/SR8/SR9 verdict conjuncts — those belong to the C1 and C2Rev/C2Crit seats; my
  support checks above only establish that the narrowed sentences the counters lean on are
  source-backed at the tip.
- Retained evidence: `run-tip.log` (verbatim below),
  `.ufo/waves/round-44/w2/C2ExecFinalQuotes/{check_quotes.py,run-tip.log,evidence.md}`, and the
  snapshot digests listed in `evidence.md`. `/tmp` held nothing.
- Risks: the `dev-replace.c` spans are corroborated, not pinned — they stay `[inference]` in the
  entry, as written. If a later round pins `dev-replace.c`, that is a new source row, not a defect
  here. Quote-quality notes 1-3 above are cosmetic.
