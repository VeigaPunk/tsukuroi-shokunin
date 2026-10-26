#!/usr/bin/env python3
"""C1-5 kill-rule scope check: map every U0 diff hunk of tools/tsukuroi-census.sh
(base c8efaa3 -> impl 4476620) to its enclosing top-level function, computed from the
impl file's own `^name() {` headers and `^}` closers, heredoc-aware. Then sha256 each
function body at both revisions and report which differ."""
import hashlib, re, subprocess, sys

BASE, IMPL = "base.sh", "impl.sh"

HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
FUNC    = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{")
CLOSE   = re.compile(r"^\}$")

def scan(lines):
    """Return (list of (name,start,end)), set of heredoc-content line numbers (1-based)."""
    funcs, stack, cur, hd, hd_body = [], [], None, [], set()
    i = 0
    while i < len(lines):
        ln = lines[i]; no = i + 1
        if hd:
            hd_body.add(no)
            if ln.strip() == hd[0]:
                hd = None
            i += 1; continue
        m = HEREDOC.search(ln)
        if m:
            hd = (m.group(2),)
            i += 1; continue
        mf = FUNC.match(ln)
        if mf:
            if cur is not None:
                funcs.append(cur); stack.append(cur)
            cur = [mf.group(1), no, None]
            if ln.rstrip().endswith("}"):   # single-line definition, e.g. `have() { ...; }`
                cur[2] = no; funcs.append(tuple(cur)); cur = None
            i += 1; continue
        if CLOSE.match(ln) and cur is not None:
            cur[2] = no
            funcs.append(tuple(cur)); cur = None
        i += 1
    if cur is not None:
        funcs.append(tuple(cur))
    return funcs, hd_body

def load(path):
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        return f.read().split("\n")

def digest(lines, start, end):
    # trailing newline per line, body inclusive
    blob = "".join(l + "\n" for l in lines[start-1:end])
    return hashlib.sha256(blob.encode("utf-8", "surrogateescape")).hexdigest()

def main():
    bl, il = load(BASE), load(IMPL)
    bfuncs, bhdb = scan(bl)
    ifuncs, ihdb = scan(il)
    for tag, fs, n in (("base", bfuncs, len(bl)), ("impl", ifuncs, len(il))):
        bad = [f for f in fs if f[2] is None]
        if bad:
            print(f"PARSE-ERROR {tag}: unclosed {bad}"); sys.exit(2)
        for a, b in zip(fs, fs[1:]):
            if a[2] >= b[1]:
                print(f"PARSE-ERROR {tag}: overlap {a} / {b}"); sys.exit(2)
        print(f"parsed {tag}: {len(fs)} top-level functions over {n} lines, "
              f"{len(bhdb if tag=='base' else ihdb)} heredoc-content lines")

    ihash = {n: digest(il, s, e) for n, s, e in ifuncs}
    bhash = {n: digest(bl, s, e) for n, s, e in bfuncs}

    # hunk headers and new-side ranges from git diff -U0
    diff = subprocess.run(
        ["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "diff", "-U0",
         "c8efaa3f120834541f8de1e5e0367e8d1593bae6",
         "447662088dfd3155e31aed239179a79c1d1046c7",
         "--", "tools/tsukuroi-census.sh"],
        capture_output=True, text=True, check=True).stdout
    H = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
    allowed = ("probe_packages", "probe_update_safety", "run_selftest")
    print("\nHUNKS (impl-side line numbers, enclosing function from impl spans):")
    fired, touched, n = False, set(), 0
    for line in diff.split("\n"):
        m = H.match(line)
        if not m:
            continue
        n += 1
        bstart, bcnt, istart, icnt = (int(m.group(1)), int(m.group(2) or 1),
                                      int(m.group(3)), int(m.group(4) or 1))
        rng = list(range(istart, istart + icnt)) if icnt else [istart]
        owners = []
        for ln in rng:
            own = [f[0] for f in ifuncs if f[1] <= ln <= f[2]]
            owners.append((ln, own[0] if own else "TOP-LEVEL/OUTSIDE"))
        uniq = sorted({o for _, o in owners})
        githint = m.group(5).strip()
        ok = all(o in allowed for o in uniq)
        if not ok:
            fired = True
        touched.update(uniq)
        print(f"  hunk {n}: '@@ -{bstart},{bcnt} +{istart},{icnt} @@' git-hint={githint!r} -> "
              f"lines {rng[0]}..{rng[-1]} owner={uniq} {'IN-SCOPE' if ok else 'OUT-OF-SCOPE <<< KILL'}")
        for ln, o in owners:
            print(f"      {ln}: {o}")
    print(f"\nKILL RULE (hunk outside probe_packages/probe_update_safety/run_selftest): "
          f"{'FIRES' if fired else 'does not fire'}")
    print(f"touched functions: {sorted(touched)}")

    print("\nPER-FUNCTION sha256 (base c8efaa3 vs impl 4476620; body lines start..end incl. `}`):")
    names_b = [f[0] for f in bfuncs]; names_i = [f[0] for f in ifuncs]
    print(f"  same function list: {names_b == names_i}")
    diff_names = []
    for name, s, e in ifuncs:
        bs, be = next((f[1], f[2]) for f in bfuncs if f[0] == name)
        same = bhash[name] == ihash[name]
        if not same:
            diff_names.append(name)
        print(f"  {'DIFF' if not same else 'same'}  {name:<22} base {bhash[name][:16]} (L{bs}-{be})  "
              f"impl {ihash[name][:16]} (L{s}-{e})")
    print(f"\nfunctions whose bytes changed: {diff_names}")
    print(f"changed-function set == allowed set: {set(diff_names) == set(allowed)}")
    print(f"probe_storage_arm identical: {bhash.get('probe_storage_arm') == ihash.get('probe_storage_arm')}")
    unn = [n for n in diff_names if n not in allowed]
    print(f"unexpected changed functions: {unn}")

    # ---- parser self-validation: contiguity, closers, balance, gap purity ----
    for tag, lines, fs in (("base", bl, bfuncs), ("impl", il, ifuncs)):
        assert [f[1] for f in fs] == sorted(f[1] for f in fs), tag
        for name, st, en in fs:
            tail = lines[en-1]
            assert tail == "}" or (st == en and tail.rstrip().endswith("}")), (tag, name, en, tail)
            assert FUNC.match(lines[st-1]) or lines[st-1].startswith(name), (tag, name, st)
        gaps = [(fs[k][2], fs[k+1][1]) for k in range(len(fs)-1)]
        for gs, gn in gaps:
            for k in range(gs+1, gn):
                assert not FUNC.match(lines[k-1]) and lines[k-1] != "}", (tag, "gap", k, lines[k-1])
        bal = sum(l.count("{") - l.count("}") for k,l in enumerate(lines,1) if k not in (bhdb if tag=="base" else ihdb))
        print(f"validate {tag}: closers ok, gaps pure, brace balance (heredoc-excluded) = {bal}")
    num = subprocess.run(['git','-C','/home/vgpnk/Projects/shokunin/tsukuroi-shokunin','diff','--numstat',
        'c8efaa3f120834541f8de1e5e0367e8d1593bae6','447662088dfd3155e31aed239179a79c1d1046c7',
        '--','tools/tsukuroi-census.sh'],capture_output=True,text=True).stdout.strip()
    add, dele = num.split("\t")[:2]
    print(f"numstat: +{add} -{dele} lines in tools/tsukuroi-census.sh")

if __name__ == "__main__":
    main()
