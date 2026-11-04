#!/usr/bin/env python3
"""Clause-isolated mutant battery for round-73 frozen instruments (M1Mutation).

Mutants live in $S only. Lane files are never written.
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path(os.environ["S"])
OUT = Path(os.environ["OUT"])
sys.dont_write_bytecode = True

UL = "ul_pristine.py"
C2 = "c2_pristine.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def norm(s):
    return " ".join(s.split())


def problems(out):
    ids = []
    for line in out.splitlines():
        if line.startswith("UL_ROW fail malformed-row"):
            ids.append("malformed-row")
        elif line.startswith("UL_ROW fail ids-not-contiguous"):
            ids.append("ids-not-contiguous")
        elif line.startswith("UL_ROW fail snapshot-reuse"):
            ids.append("snapshot-reuse")
        else:
            m = re.match(r"UL_ROW fail UL\d+ (.*)$", line)
            if m:
                ids.append(m.group(1))
    return ids


def summary(out):
    for line in out.splitlines():
        if line.startswith("UL_ROWS="):
            return line
    return ""


# ---------------------------------------------------------------- counter trees
def note_edit(mod, root, rid, fn):
    p = root / mod.NOTE
    out = []
    for line in p.read_text().splitlines():
        if line.startswith("| %s |" % rid):
            line = fn(line)
        out.append(line)
    p.write_text("\n".join(out) + "\n")


def note_append(mod, root, line):
    p = root / mod.NOTE
    p.write_text(p.read_text().rstrip("\n") + "\n" + line + "\n")


def field(line, key):
    m = re.search(r"(?:^| )%s=([^ |]+)" % key, line)
    return m.group(1) if m else None


def set_field(line, key, val):
    return re.sub(r"((?:^| )%s=)[^ |]+" % key, r"\g<1>" + val, line, count=1)


def set_quote(line, q):
    return re.sub(r'quote="[^"]*"', 'quote="' + q + '"', line, count=1)


def set_stmt(line, s):
    cells = line.split("|")
    cells[2] = " " + s + " "
    return "|".join(cells)


def reg_edit(mod, root, sid, idx, val):
    p = root / mod.REGISTRY
    out = []
    for line in p.read_text().splitlines():
        if line.startswith("| %s |" % sid):
            cells = line.split("|")
            cells[idx] = " " + val + " "
            line = "|".join(cells)
        out.append(line)
    p.write_text("\n".join(out) + "\n")


def snap_path(mod, root, name):
    return root / mod.SNAPDIR / name


def span(mod, root, n, from_end=False, avoid=(), name="systemd.unit.xml"):
    text = norm(snap_path(mod, root, name).read_text())
    toks = text.split(" ")
    rng = range(len(toks) - n - 1, -1, -1) if from_end else range(0, len(toks) - n)
    for i in rng:
        s = " ".join(toks[i:i + n])
        if any(c in s for c in '"|='):
            continue
        if any(a in s for a in avoid):
            continue
        return s
    raise SystemExit("no verbatim span found")


def map_edit(mod, root, fn):
    p = root / mod.MAP
    d = json.loads(p.read_text())
    fn(d["snapshots"])
    p.write_text(json.dumps(d, indent=2) + "\n")


# ---- fixtures: each violates exactly one clause -----------------------------
def f_contig(mod, root):
    note_edit(mod, root, "UL6", lambda l: l.replace("| UL6 |", "| UL7 |", 1))


def f_words(mod, root):
    note_edit(mod, root, "UL1",
              lambda l: set_stmt(l, "Unit files loaded earlier override directories lower name"))


def f_ground(mod, root):
    note_edit(mod, root, "UL6",
              lambda l: set_stmt(l, "Zebra quokka wombat xylophone nostril platypus "
                                    "marmalade truffle blizzard kumquat yonder zeppelin"))


def f_kind_bogus(mod, root):
    reg_edit(mod, root, "S306", 3, "blog")


def f_kind_own(mod, root):
    reg_edit(mod, root, "S306", 3, "own-work")


def f_digest(mod, root):
    p = snap_path(mod, root, "unit.c")
    p.write_bytes(p.read_bytes() + b"\n/* M1-MUTATED-BYTES */\n")


def f_mapdigest(mod, root):
    map_edit(mod, root, lambda s: s["unit.c"].__setitem__("sha256", "0" * 64))


def f_mapurl(mod, root):
    map_edit(mod, root, lambda s: s["unit.c"].__setitem__("url", 123))


def f_mapurl_none(mod, root):
    map_edit(mod, root, lambda s: s["unit.c"].__setitem__("url", None))


def f_srcbound(mod, root):
    reg_edit(mod, root, "S306", 2, "fixture install.c \u2014 https://example.invalid/install.c")


def f_anchor(mod, root):
    reg_edit(mod, root, "S304", 6, "the unit man page at tag v262 (load path and drop-in merge)")


def f_quoteloc(mod, root):
    note_edit(mod, root, "UL6",
              lambda l: set_quote(l, "Unit %s is not masked at all."))


def f_quotelen(mod, root):
    q = span(mod, root, 30)
    note_edit(mod, root, "UL1", lambda l: set_quote(l, q))


def f_quotepipe(mod, root):
    note_edit(mod, root, "UL1", lambda l: set_quote(l, "a | b"))


def f_reuse(mod, root):
    p = root / mod.NOTE
    lines = p.read_text().splitlines()
    ul1 = [l for l in lines if l.startswith("| UL1 |")][0]
    d = sha_file(snap_path(mod, root, "systemd.unit.xml"))
    stmt = ul1.split("|")[2].strip()
    quote = re.search(r'quote="([^"]*)"', ul1).group(1)

    def clone(l):
        l = set_field(l, "snapshot", "systemd.unit.xml")
        l = set_field(l, "source", "S304")
        l = set_field(l, "digest", d)
        l = set_quote(l, quote)
        return set_stmt(l, stmt)
    note_edit(mod, root, "UL3", clone)


def f_malformed(mod, root):
    note_append(mod, root, "| UL7 | junk row without the required cells |")


def f_seven(mod, root):
    # 7th row on a 4th snapshot/source, failing only statement-words
    src = snap_path(mod, root, "unit2.c")
    src.write_bytes(snap_path(mod, root, "unit.c").read_bytes())
    d = sha_file(src)
    url = "https://example.invalid/unit2.c"

    def add(snaps):
        snaps["unit2.c"] = {"url": url, "sha256": d}
    map_edit(mod, root, add)
    reg = root / mod.REGISTRY
    reg.write_text(reg.read_text().rstrip("\n") + "\n" +
                   "| S307 | fixture unit2.c \u2014 " + url + " | code | A | fixture scope "
                   "| unit2.c at tag v262 | fixture lesson | mined | 2026-11-03 "
                   "| on-release | \u2014 |\n")
    q = span(mod, root, 8, from_end=True, name="unit.c")
    cand = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", snap_path(mod, root, "unit.c").read_text()):
        if tok.lower() in mod.STOP or tok.lower() in cand:
            continue
        cand.append(tok.lower())
        if len(cand) == 8:
            break
    note_append(mod, root,
                '| UL7 | ' + " ".join(cand) + ' | source=S307 | snapshot=unit2.c | digest=' + d +
                ' | quote="' + q + '" |')


def f_tgtsrc(mod, root):
    # source S304 binds two map URLs + two anchors; UL3/UL4 cite unit.c under S304.
    urls = [sha_file(snap_path(mod, root, "systemd.unit.xml")), None]
    m = json.loads((root / mod.MAP).read_text())["snapshots"]
    src = "fixture systemd.unit.xml \u2014 " + m["systemd.unit.xml"]["url"] + \
          " and unit.c \u2014 " + m["unit.c"]["url"]
    reg_edit(mod, root, "S304", 2, src)
    reg_edit(mod, root, "S304", 6, "systemd.unit.xml and unit.c at tag v262")
    note_edit(mod, root, "UL3", lambda l: set_field(l, "source", "S304"))
    note_edit(mod, root, "UL4", lambda l: set_field(l, "source", "S304"))


def f_two_snap(mod, root):
    p = root / mod.NOTE
    lines = p.read_text().splitlines()
    ul1 = [l for l in lines if l.startswith("| UL1 |")][0]
    d = sha_file(snap_path(mod, root, "systemd.unit.xml"))
    stmt = ul1.split("|")[2].strip()
    quote = re.search(r'quote="([^"]*)"', ul1).group(1)

    def clone(l):
        l = set_field(l, "snapshot", "systemd.unit.xml")
        l = set_field(l, "source", "S304")
        l = set_field(l, "digest", d)
        l = set_quote(l, quote)
        return set_stmt(l, stmt)
    for rid in ("UL5", "UL6"):
        note_edit(mod, root, rid, clone)


def f_tokensalad(mod, root):
    p = root / mod.NOTE
    lines = p.read_text().splitlines()
    snaps = {}
    for name in ("systemd.unit.xml", "unit.c", "install.c"):
        snaps[name] = snap_path(mod, root, name).read_text()
    out = []
    for line in lines:
        if line.startswith("| UL"):
            name = field(line, "snapshot")
            toks = []
            for t in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", snaps[name]):
                if t.lower() in mod.STOP:
                    continue
                if t.lower() not in toks:
                    toks.append(t.lower())
                if len(toks) == 16:
                    break
            line = set_stmt(line, " ".join(toks))
        out.append(line)
    p.write_text("\n".join(out) + "\n")


def f_quote_unrelated(mod, root):
    stmt = [l for l in (root / mod.NOTE).read_text().splitlines()
            if l.startswith("| UL1 |")][0]
    avoid = tuple(w.lower() for w in stmt.split("|")[2].split())
    q = span(mod, root, 8, from_end=True, avoid=avoid[:6])
    note_edit(mod, root, "UL1", lambda l: set_quote(l, q))


def f_empty_quote(mod, root):
    p = root / mod.NOTE
    out = []
    for line in p.read_text().splitlines():
        if line.startswith("| UL"):
            line = set_quote(line, "")
        out.append(line)
    p.write_text("\n".join(out) + "\n")


def f_doctored(mod, root):
    p = snap_path(mod, root, "unit.c")
    p.write_bytes(p.read_bytes() + b"\n/* M1-DOCTORED-BYTES: not v262 */\n")
    nd = sha_file(p)

    def bump(snaps):
        snaps["unit.c"]["sha256"] = nd
    map_edit(mod, root, bump)
    for rid in ("UL3", "UL4"):
        note_edit(mod, root, rid, lambda l: set_field(l, "digest", nd))


FIXTURES = {
    "control": lambda mod, root: None,
    "contig": f_contig,
    "words": f_words,
    "ground": f_ground,
    "kind_bogus": f_kind_bogus,
    "kind_own": f_kind_own,
    "digest": f_digest,
    "mapdigest": f_mapdigest,
    "mapurl": f_mapurl,
    "mapurl_none": f_mapurl_none,
    "srcbound": f_srcbound,
    "anchor": f_anchor,
    "quoteloc": f_quoteloc,
    "quotelen": f_quotelen,
    "quotepipe": f_quotepipe,
    "reuse": f_reuse,
    "malformed": f_malformed,
    "seven": f_seven,
    "tgtsrc": f_tgtsrc,
    "two_snap": f_two_snap,
    "tokensalad": f_tokensalad,
    "quote_unrelated": f_quote_unrelated,
    "empty_quote": f_empty_quote,
    "doctored": f_doctored,
}

# ---- mutants: (name, clause, old, new, targeted fixtures) -------------------
UL_MUTANTS = [
    ("U01", "id contiguity",
     "contiguous = sorted(seen_ids) == list(range(1, len(seen_ids) + 1))",
     "contiguous = True", ["contig"]),
    ("U02", "statement words",
     "if words(stmt) < MIN_WORDS:", "if False:", ["words"]),
    ("U03", "grounding",
     "if hits < MIN_TOKENS or (total and hits / total < MIN_SHARE):",
     "if False:", ["ground"]),
    ("U04", "source kind (both arms)",
     'if regrow["kind"] not in KINDS or regrow["kind"] == "own-work":',
     "if False:", ["kind_bogus", "kind_own"]),
    ("U05", "source kind (KINDS membership arm)",
     'if regrow["kind"] not in KINDS or regrow["kind"] == "own-work":',
     'if regrow["kind"] == "own-work":', ["kind_bogus"]),
    ("U06", "source kind (own-work arm)",
     'if regrow["kind"] not in KINDS or regrow["kind"] == "own-work":',
     'if regrow["kind"] not in KINDS:', ["kind_own"]),
    ("U07", "digest (file vs note)",
     'if hashlib.sha256(snap_b).hexdigest() != m.group("digest"):',
     "if False:", ["digest"]),
    ("U08", "map binding (map digest)",
     'if not isinstance(entry, dict) or entry.get("sha256") != m.group("digest"):',
     'if not isinstance(entry, dict):', ["mapdigest"]),
    ("U09", "map binding (map url type)",
     'elif not isinstance(entry.get("url"), str):', "elif False:",
     ["mapurl_none", "mapurl"]),
    ("U10", "map binding (registry source cell carries url)",
     'if not url or url not in regrow["source"]:', "if False:", ["srcbound"]),
    ("U11", "anchor binding",
     'if snap_name not in regrow["anchor"]:', "if False:", ["anchor"]),
    ("U12", "quote location",
     "if norm(quote) not in norm(snap):", "if False:", ["quoteloc"]),
    ("U13", "quote length",
     "if words(quote) > MAX_QUOTE_WORDS:", "if False:", ["quotelen"]),
    ("U14", "quote pipe",
     'if "|" in quote:', "if False:", ["quotepipe"]),
    ("U15", "snapshot reuse",
     "over = {k: v for k, v in reuse.items() if v > MAX_SNAPSHOT_REUSE}",
     "over = {}", ["reuse"]),
    ("U16", "malformed-row counting",
     "                malformed += 1", "                malformed += 0", ["malformed"]),
    ("U17", "target arithmetic (verified==6)",
     "and verified == TARGET_ROWS", "and True", ["ground"]),
    ("U18", "target arithmetic (rows==6)",
     "len(rows) == TARGET_ROWS and verified", "True and verified", ["seven"]),
    ("U19", "target arithmetic (sources>=3)",
     "and len(sources) >= TARGET_SOURCES", "and True", ["tgtsrc"]),
    ("U21", "target arithmetic (malformed==0)",
     "met = (malformed == 0 and len(rows)", "met = (True and len(rows)", ["malformed"]),
    ("U20", "target arithmetic (snapshots>=3)",
     "and len(snaps) >= TARGET_SNAPSHOTS)", ")", ["two_snap"]),
]


def counter_case_table(mod):
    """Replicate the committed selftest cases; measure how isolated each fixture is."""
    base = Path(tempfile.mkdtemp(prefix="stc-", dir=str(S)))
    rows = []

    def add(cid, mut, expect_rc, token):
        root = base / cid
        mod.build_fixture(root)
        mut(root)
        buf = io.StringIO()
        rc = mod.score_tree(root, buf)
        out = buf.getvalue()
        pr = problems(out)
        rows.append({"case": cid, "rc": rc, "expect_rc": expect_rc, "token": token,
                     "token_present": token in out, "problems": pr,
                     "problem_count": len(pr),
                     "finding_ids": sum(1 for x in pr if not x.startswith("statement-words"))})

    def edit(rel, old, new):
        def _m(root):
            f = root / rel
            s = f.read_text()
            assert old in s, old[:40]
            f.write_text(s.replace(old, new, 1))
        return _m

    def drop6(root):
        f = root / mod.NOTE
        f.write_text("\n".join(l for l in f.read_text().splitlines()
                                if not l.startswith("| UL6 |")) + "\n")

    def dup5(root):
        f = root / mod.NOTE
        f.write_text("\n".join(l.replace("| UL6 |", "| UL5 |", 1) if l.startswith("| UL6 |") else l
                                for l in f.read_text().splitlines()) + "\n")

    def reuse(root):
        f = root / mod.NOTE
        out = []
        for l in f.read_text().splitlines():
            if l.startswith("| UL3 |"):
                l = l.replace("snapshot=unit.c", "snapshot=systemd.unit.xml")
            out.append(l)
        f.write_text("\n".join(out) + "\n")

    def dig(root):
        f = root / mod.NOTE
        out = []
        for l in f.read_text().splitlines():
            if l.startswith("| UL5 |"):
                l = re.sub(r"digest=[0-9a-f]{64}", "digest=" + "0" * 64, l)
            out.append(l)
        f.write_text("\n".join(out) + "\n")

    add("CONTROL", lambda r: None, 0, "UL_TARGET")
    add("SHORT", edit(mod.NOTE, mod.SAMPLE_ROWS[0][2], "Too short a statement"),
        1, "statement-words")
    add("UNREGISTERED", edit(mod.NOTE, "source=S306", "source=S999"), 1, "source-unregistered")
    add("QUOTE", edit(mod.NOTE, "Unit %s is masked, ignoring.", "Unit %s is not masked at all."),
        1, "quote-absent")
    add("FIVE", drop6, 1, "UL_ROWS=5")
    add("DUPID", dup5, 1, "duplicate-id")
    add("REUSE", reuse, 1, "snapshot-reuse")
    add("UNGROUNDED", edit(mod.NOTE, mod.SAMPLE_ROWS[5][2],
                           "Zebra quokka wombat xylophone nostril platypus marmalade truffle "
                           "blizzard kumquat yonder zeppelin"), 1, "statement-grounding")
    add("MALFORMED", lambda r: (r / mod.NOTE).write_text(
        (r / mod.NOTE).read_text() + "| UL7 | junk row without the required cells |\n"),
        1, "malformed-row")
    add("DIGEST", dig, 1, "digest-mismatch")
    add("OWNWORK", edit(mod.REGISTRY, "| code | A | fixture scope | install.c at",
                        "| own-work | A | fixture scope | install.c at"), 1, "source-kind")
    shutil.rmtree(base, ignore_errors=True)
    return rows


def build_fixture_trees(mod):
    base = Path(tempfile.mkdtemp(prefix="fx-", dir=str(S)))
    roots = {}
    for name, fn in FIXTURES.items():
        root = base / name
        mod.build_fixture(root)
        fn(mod, root)
        roots[name] = root
    return base, roots


def run(mod, root, out):
    buf = io.StringIO()
    try:
        rc = mod.score_tree(root, buf)
        err = ""
    except Exception as exc:  # instrument crash is a datum, not a driver failure
        rc = "EXC"
        err = "%s: %s" % (type(exc).__name__, exc)
        buf.write("TRACEBACK<" + err + ">")
    out.append((rc, buf.getvalue()))
    return rc, buf.getvalue()


def selftest(script, tag):
    tmp = S / ("st-" + tag)
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp))
    r = subprocess.run([sys.executable, str(script), "--selftest"],
                       capture_output=True, text=True, env=env)
    shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode, (r.stdout + r.stderr)


def gen_mutant(src_text, name, old, new):
    n = src_text.count(old)
    if n != 1:
        raise SystemExit("MUTANT %s: old occurs %d times: %r" % (name, n, old[:60]))
    return src_text.replace(old, new, 1)


def phase_counter():
    lane = S / "lane"
    pristine = lane / "tools" / UL
    mod = load("ul_pristine", pristine)
    text = pristine.read_text()
    base, roots = build_fixture_trees(mod)

    fx = {}
    print("== pristine fixture readings ==")
    for name in FIXTURES:
        rc, out = run(mod, roots[name], [])
        fx[name] = {"rc": rc, "problems": problems(out),
                    "summary": summary(out),
                    "met": "met=1" in out}
        print("%-16s rc=%s problems=%s | %s" %
              (name, rc, fx[name]["problems"], fx[name]["summary"]))
        if fx[name]["problems"] or rc:
            for line in out.splitlines():
                if line.startswith("UL_ROW fail") or line.startswith("UL_NOTE") \
                        or line.startswith("UL_MAP") or line.startswith("Traceback"):
                    print("    " + line[:160])
    print("\n== pristine control full output ==")
    print(run(mod, roots["control"], [])[1])

    results = []
    print("\n== mutant matrix ==")
    for name, clause, old, new, targets in UL_MUTANTS:
        mtext = gen_mutant(text, name, old, new)
        path = lane / "tools" / ("ul_%s.py" % name)
        path.write_text(mtext)
        changed = sum(1 for a, b in zip(text.splitlines(), mtext.splitlines()) if a != b)
        m = load("ul_" + name, path)
        src_rc, src_out = selftest(path, name)
        row = {"mutant": name, "clause": clause, "old": old, "new": new,
               "changed_lines": changed, "sha": sha_file(path),
               "selftest_rc": src_rc,
               "selftest_verdict": "killed" if src_rc == 3 else "survived",
               "targets": []}
        for t in targets:
            buf = io.StringIO()
            try:
                rc = m.score_tree(roots[t], buf)
            except Exception as exc:
                rc = "EXC"
                buf.write("TRACEBACK<%s: %s>" % (type(exc).__name__, exc))
            out = buf.getvalue()
            pr = problems(out)
            base_pr = fx[t]["problems"]
            if rc != fx[t]["rc"]:
                verdict = "killed"
            elif pr != base_pr:
                verdict = "token_lost"
            else:
                verdict = "survived"
            row["targets"].append({"fixture": t, "pristine_rc": fx[t]["rc"],
                                   "mutant_rc": rc, "pristine_problems": base_pr,
                                   "mutant_problems": pr, "verdict": verdict})
        results.append(row)
        tv = ",".join("%s:%s" % (x["fixture"], x["verdict"][0].upper()) for x in row["targets"]) or "none"
        print("%s %-46s diff=%s selftest=%-8s fixtures=%s" %
              (name, clause[:46], changed, row["selftest_verdict"], tv))
        if src_rc != 0:
            for line in src_out.splitlines():
                if line.startswith("FAIL") or line.startswith("SELFTEST"):
                    print("     selftest: " + line[:150])
        for x in row["targets"]:
            if x["verdict"] == "survived":
                print("     SURVIVED %s: pristine rc=%s %s / mutant rc=%s %s" %
                      (x["fixture"], x["pristine_rc"], x["pristine_problems"],
                       x["mutant_rc"], x["mutant_problems"]))

    cases = counter_case_table(mod)
    print("\n== committed counter selftest case isolation ==")
    for c in cases:
        print("%-12s rc=%s expect=%s token=%-20s present=%s problems=%s" %
              (c["case"], c["rc"], c["expect_rc"], c["token"], c["token_present"],
               c["problems"]))
    (OUT / "counter_matrix.json").write_text(json.dumps(
        {"fixtures": fx, "mutants": results, "selftest_cases": cases}, indent=2) + "\n")
    shutil.rmtree(base, ignore_errors=True)
    return fx, results


# ---------------------------------------------------------------- routed checker
GOOD_LESSON = ("## Correction (round 73, append-only)\n\n"
               "R72-LESSON-SUPERSEDED-CLAIMS: the sentences \"No capability row enters "
               "this round\" and \"nine hermetic cases\" are superseded; the landed state "
               "is the gate-selftest capability row and 10 cases.\n")


def lesson_block(cid=True, nocap=True, nine=True, gs=True, ten=None, ten10=True):
    body = ""
    if cid:
        body += "R72-LESSON-SUPERSEDED-CLAIMS: "
    body += "the sentences "
    quoted = []
    if nocap:
        quoted.append("\"No capability row enters this round\"")
    if nine:
        quoted.append("\"nine hermetic cases\"")
    body += " and ".join(quoted) if quoted else "in question"
    body += " are superseded; the landed state is the "
    if gs:
        body += "gate-selftest "
    body += "capability row and "
    if ten10:
        body += "10 cases."
    elif ten:
        body += "ten cases."
    else:
        body += "often updated cases."
    return "## Correction (round 73, append-only)\n\n" + body + "\n"


def digest_block(old=True, tip=True, receipt=True, same=True):
    body = "R72-C3-INSTRUMENT-DIGEST-DRIFT: check-r71-routed-r72.py moved from "
    body += "df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712" if old else "(old digest unstated)"
    body += " to "
    body += "2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc" if tip else "(tip digest unstated)"
    if same:
        body += "; the before control was re-run with the final instrument (same-instrument)"
    else:
        body += "; the before control was re-run"
    if receipt:
        body += " at .ufo/waves/round-72/after/selftest-selftest-after.txt"
    body += ".\n"
    return "## Round 72 \u2014 instrument digest erratum (appended round 73)\n\n" + body


def cap_block(gs=True, ten=True, ten10=True, receipt=True, often=False):
    body = ""
    if gs:
        body += "gate-selftest "
    body += "now prints "
    if often:
        body += "often "
    if ten:
        body += "ten cases "
    if ten10:
        body += "(10 cases)"
    if receipt:
        body += ", receipt .ufo/waves/round-72/after/selftest-selftest-after.txt"
    body += ".\n"
    return "## Capability refresh (round 73)\n\n" + body


def c2_texts(lesson=None, digest=None, cap=None):
    return {
        "corpus/lessons/round-72.md": "# L\n\n## Gate\n\nnothing\n\n" +
        (GOOD_LESSON if lesson is None else lesson),
        "SCORECARD.md": "# SC\n\n## Round 72 \u2014 measured outcome\n\nbody\n\n" +
        (digest_block() if digest is None else digest) + "\n" +
        (cap_block() if cap is None else cap),
    }


C2_FIXTURES = {
    "good": c2_texts(),
    "l_no_id": c2_texts(lesson=lesson_block(cid=False)),
    "l_no_nocap": c2_texts(lesson=lesson_block(nocap=False)),
    "l_no_nine": c2_texts(lesson=lesson_block(nine=False)),
    "l_no_gs": c2_texts(lesson=lesson_block(gs=False)),
    "l_no_ten": c2_texts(lesson=lesson_block(ten=False, ten10=True)),
    "l_no_10cases": c2_texts(lesson=lesson_block(ten=True, ten10=False)),
    "l_needany_gone": c2_texts(lesson=lesson_block(ten10=False)),
    "l_outside_block": c2_texts(lesson=lesson_block(cid=False) +
                                "\n## Note\n\nR72-LESSON-SUPERSEDED-CLAIMS is mentioned here.\n"),
    "d_no_old": c2_texts(digest=digest_block(old=False)),
    "d_no_tip": c2_texts(digest=digest_block(tip=False)),
    "d_no_receipt": c2_texts(digest=digest_block(receipt=False)),
    "d_receipt_only": c2_texts(digest=("## Round 72 \u2014 instrument digest erratum "
                                       "(appended round 73)\n\nR72-C3-INSTRUMENT-DIGEST-DRIFT: "
                                       "check-r71-routed-r72.py moved from "
                                       "df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712"
                                       " to "
                                       "2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc"
                                       "; receipt "
                                       ".ufo/waves/round-72/after/selftest-selftest-after.txt\n")),
    "d_needany_gone": c2_texts(digest=digest_block(receipt=False)),
    "d_no_needany": c2_texts(digest=("## Round 72 \u2014 instrument digest erratum "
                                     "(appended round 73)\n\nR72-C3-INSTRUMENT-DIGEST-DRIFT: "
                                     "check-r71-routed-r72.py moved from "
                                     "df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712"
                                     " to "
                                     "2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc"
                                     ".\n")),
    "l_no_ten_strict": c2_texts(lesson=(
        "## Correction (round 73, append-only)\n\n"
        "R72-LESSON-SUPERSEDED-CLAIMS: the claims \"No capability row enters this round\" "
        "and \"nine hermetic cases\" are superseded; the landed state is the gate-selftest "
        "capability row and 10 cases.\n")),
    "c_no_gs": c2_texts(cap=cap_block(gs=False)),
    "c_no_ten": c2_texts(cap=cap_block(ten=False, ten10=True)),
    "c_no_receipt": c2_texts(cap=cap_block(receipt=False)),
    "c_needany_gone": c2_texts(cap=("## Capability refresh (round 73)\n\ngate-selftest now "
                                    "often runs, receipt "
                                    ".ufo/waves/round-72/after/selftest-selftest-after.txt\n")),
    "c_receipt_only": c2_texts(cap=("## Capability refresh (round 73)\n\ngate-selftest ten "
                                    "receipt .ufo/waves/round-72/after/selftest-selftest-after.txt\n")),
    "anchor_midline": c2_texts(lesson=(
        "Prose prefix ## Correction (round 73, append-only) "
        "R72-LESSON-SUPERSEDED-CLAIMS: the sentences \"No capability row enters this round\" "
        "and \"nine hermetic cases\" are superseded; the landed state is the gate-selftest "
        "capability row and 10 cases.\n")),
    "heading_token": c2_texts(lesson=(
        "## Correction (round 73) R72-LESSON-SUPERSEDED-CLAIMS\n\n"
        "The sentences \"No capability row enters this round\" and \"nine hermetic cases\" are "
        "superseded; the landed state is the gate-selftest capability row and 10 cases.\n")),
    "substring_ten": c2_texts(cap=("## Capability refresh (round 73)\n\ngate-selftest now "
                                   "often runs; 10 cases are claimed, receipt "
                                   ".ufo/waves/round-72/after/selftest-selftest-after.txt\n")),
}

C2_MUTANTS = [
    ("C01", "lesson token R72-LESSON-SUPERSEDED-CLAIMS",
     '"R72-LESSON-SUPERSEDED-CLAIMS",', "", ["l_no_id"]),
    ("C02", "lesson token No capability row enters this round",
     '"No capability row enters this round",', "", ["l_no_nocap"]),
    ("C03", "lesson token nine hermetic cases",
     '"nine hermetic cases",', "", ["l_no_nine"]),
    ("C04", "lesson token gate-selftest",
     '"gate-selftest", "ten", "10 cases"],', '"ten", "10 cases"],', ["l_no_gs"]),
    ("C05", "lesson token ten",
     '"gate-selftest", "ten", "10 cases"],', '"gate-selftest", "10 cases"],',
     ["l_no_ten_strict"]),
    ("C06", "lesson token 10 cases",
     '"gate-selftest", "ten", "10 cases"],', '"gate-selftest", "ten"],', ["l_no_10cases"]),
    ("C07", "digest token OLD_DIGEST",
     "OLD_DIGEST, TIP_DIGEST", "TIP_DIGEST", ["d_no_old"]),
    ("C08", "digest token TIP_DIGEST",
     "OLD_DIGEST, TIP_DIGEST,", "OLD_DIGEST,", ["d_no_tip"]),
    ("C09", "digest need_any receipt alternative",
     '("same-instrument", "re-run", "re-ran", RECEIPT)', '("same-instrument", "re-run", "re-ran")',
     ["d_receipt_only"]),
    ("C10", "capability token gate-selftest",
     '"tokens": ["gate-selftest", "ten", RECEIPT]', '"tokens": ["ten", RECEIPT]', ["c_no_gs"]),
    ("C11", "capability token ten",
     '"tokens": ["gate-selftest", "ten", RECEIPT]', '"tokens": ["gate-selftest", RECEIPT]',
     ["c_no_ten"]),
    ("C12", "capability token RECEIPT",
     '"tokens": ["gate-selftest", "ten", RECEIPT]', '"tokens": ["gate-selftest", "ten"]',
     ["c_no_receipt"]),
    ("C13", "block-heading line-start anchor",
     'HEADING_RE = re.compile(r"^## .+", re.M)', 'HEADING_RE = re.compile(r"## .+", re.M)',
     ["anchor_midline"]),
    ("C14", "item-heading line-start anchor (lesson)",
     '"path": LESSON,\n        "heading": re.compile(r"^## .*(?i:correction|erratum).*$", re.M),',
     '"path": LESSON,\n        "heading": re.compile(r"## .*(?i:correction|erratum).*$", re.M),',
     ["anchor_midline"]),
    ("C15", "lesson need_any",
     '"need_any": [("10 cases", "ten cases", "ten hermetic cases")],',
     '"need_any": [],', ["l_needany_gone"]),
    ("C16", "digest need_any",
     '"need_any": [("same-instrument", "re-run", "re-ran", RECEIPT)],',
     '"need_any": [],', ["d_no_needany"]),
    ("C17", "capability need_any",
     '"need_any": [("10 cases", "ten cases", "ten names", "ten hermetic")],',
     '"need_any": [],', ["c_needany_gone"]),
]


def c2_score(mod, texts, tag):
    root = Path(tempfile.mkdtemp(prefix="c2-" + tag + "-", dir=str(S)))
    for rel, body in texts.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    buf = io.StringIO()
    rc = mod.evaluate(mod.readers("HEAD", str(root)), buf)
    out = buf.getvalue()
    shutil.rmtree(root, ignore_errors=True)
    return rc, out


def phase_c2():
    lane = S / "lane" / "tools"
    pristine = lane / C2
    mod = load("c2_pristine", pristine)
    text = pristine.read_text()

    fx = {}
    print("== c2 pristine fixture readings ==")
    for name, texts in C2_FIXTURES.items():
        rc, out = c2_score(mod, texts, name)
        fx[name] = {"rc": rc,
                    "stale": [l.split()[0] for l in out.splitlines() if "-STALE" in l]}
        print("%-18s rc=%s stale=%s" % (name, rc, fx[name]["stale"]))

    results = []
    print("\n== c2 mutant matrix ==")
    for name, clause, old, new, targets in C2_MUTANTS:
        mtext = gen_mutant(text, name, old, new)
        path = lane / ("c2_%s.py" % name)
        path.write_text(mtext)
        changed = sum(1 for a, b in zip(text.splitlines(), mtext.splitlines()) if a != b)
        m = load("c2_" + name, path)
        src_rc, src_out = selftest(path, name)
        row = {"mutant": name, "clause": clause, "old": old, "new": new,
               "changed_lines": changed, "sha": sha_file(path), "selftest_rc": src_rc,
               "selftest_verdict": "killed" if src_rc == 3 else "survived", "targets": []}
        for t in targets:
            rc, out = c2_score(m, C2_FIXTURES[t], name + t)
            changed_out = rc != fx[t]["rc"]
            row["targets"].append({"fixture": t, "pristine_rc": fx[t]["rc"],
                                   "mutant_rc": rc, "verdict": "killed" if changed_out else "survived"})
        results.append(row)
        tv = ",".join("%s:%s" % (x["fixture"], x["verdict"][0].upper()) for x in row["targets"])
        print("%s %-46s diff=%s selftest=%-8s fixtures=%s" %
              (name, clause[:46], changed, row["selftest_verdict"], tv))
        if src_rc != 0:
            for line in src_out.splitlines():
                if line.startswith("FAIL") or line.startswith("SELFTEST"):
                    print("     selftest: " + line[:150])

    (OUT / "c2_matrix.json").write_text(json.dumps(
        {"fixtures": fx, "mutants": results}, indent=2) + "\n")
    return fx, results


def one_fixture(name):
    mod = load("ul_pristine", S / "lane" / "tools" / UL)
    root = S / "single" / name
    shutil.rmtree(root, ignore_errors=True)
    mod.build_fixture(root)
    FIXTURES[name](mod, root)
    buf = io.StringIO()
    rc = mod.score_tree(root, buf)
    sys.stdout.write(buf.getvalue())
    print("rc=%d" % rc)


def one_mutant(name, fname):
    text = (S / "lane" / "tools" / UL).read_text()
    entry = [m for m in UL_MUTANTS if m[0] == name][0]
    mtext = gen_mutant(text, name, entry[2], entry[3])
    path = S / "lane" / "tools" / ("ul_one_%s.py" % name)
    path.write_text(mtext)
    print("mutant %s sha256=%s changed_lines=%d" %
          (name, sha_file(path),
           sum(1 for a, b in zip(text.splitlines(), mtext.splitlines()) if a != b)))
    mod = load("ul_one_" + name, path)
    root = S / "single" / ("mut_" + name + "_" + fname)
    shutil.rmtree(root, ignore_errors=True)
    mod.build_fixture(root)
    FIXTURES[fname](mod, root)
    buf = io.StringIO()
    rc = mod.score_tree(root, buf)
    sys.stdout.write(buf.getvalue())
    print("rc=%d" % rc)


def one_c2_fixture(name):
    mod = load("c2_pristine", S / "lane" / "tools" / C2)
    rc, out = c2_score(mod, C2_FIXTURES[name], name)
    sys.stdout.write(out)
    print("rc=%d" % rc)


def one_c2_mutant(name, fname):
    text = (S / "lane" / "tools" / C2).read_text()
    entry = [m for m in C2_MUTANTS if m[0] == name][0]
    mtext = gen_mutant(text, name, entry[2], entry[3])
    path = S / "lane" / "tools" / ("c2_one_%s.py" % name)
    path.write_text(mtext)
    print("mutant %s sha256=%s changed_lines=%d" %
          (name, sha_file(path),
           sum(1 for a, b in zip(text.splitlines(), mtext.splitlines()) if a != b)))
    mod = load("c2_one_" + name, path)
    rc, out = c2_score(mod, C2_FIXTURES[fname], name + fname)
    sys.stdout.write(out)
    print("rc=%d" % rc)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what == "fixture":
        one_fixture(sys.argv[2])
    elif what == "mutant":
        one_mutant(sys.argv[2], sys.argv[3])
    elif what == "c2fixture":
        one_c2_fixture(sys.argv[2])
    elif what == "c2mutant":
        one_c2_mutant(sys.argv[2], sys.argv[3])
    if what in ("counter", "all"):
        phase_counter()
    if what in ("c2", "all"):
        phase_c2()
