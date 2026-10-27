import re, sys, collections
MUT = {'mkdir','mkdirat','rmdir','unlink','unlinkat','rename','renameat','renameat2','link','linkat','symlink','symlinkat','creat'}
WRITE = re.compile(r'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND')
CALL = re.compile(r'^(\d+)\s+(\w+)\((.*)$')
RES  = re.compile(r'^(.*)\)\s+=\s+(-?\d+|\?)(.*)$')
def events(path):
    pend = {}
    ev = []
    for i, raw in enumerate(open(path, errors='replace'), 1):
        line = raw.rstrip('\n')
        m = CALL.match(line)
        if m:
            pid, call, rest = m.groups()
            if '<unfinished ...>' in rest:
                pend[(pid, call)] = (i, rest.replace('<unfinished ...>', ''))
                continue
            r = RES.match(rest)
            if r: ev.append((i, pid, call, r.group(1), r.group(2)))
            continue
        m2 = re.match(r'^(\d+)\s+<\.\.\. (\w+) resumed>(.*)$', line)
        if m2:
            pid, call, rest = m2.groups()
            pre = pend.pop((pid, call), None)
            if pre is None: continue
            r = RES.match(pre[1] + rest)
            if r: ev.append((pre[0], pid, call, r.group(1), r.group(2)))
            continue
    leftovers = len(pend)
    return ev, leftovers
def split_args(call, args):
    # returns (path(s), flags) best-effort
    q = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
    flags = ''
    if call in ('open','openat'):
        # flags text = everything after the last quoted string
        idx = args.rfind('"')
        flags = args[idx+1:] if idx >= 0 else ''
        return ([q[0]] if q else [], flags)
    return (q, '')
def classify(p):
    if p.startswith('/dev/') or p.startswith('/proc/') or p.startswith('/sys/'):
        return 'pseudo'
    return 'fs'
def run(path):
    ev, left = events(path)
    W = []   # write-mode opens
    M = []   # mutating calls
    allcalls = collections.Counter()
    for ln, pid, call, args, ret in ev:
        allcalls[call] += 1
        if call in ('openat','open'):
            paths, flags = split_args(call, args)
            if paths and WRITE.search(flags):
                W.append((ln, pid, call, paths[0], flags.strip(), ret))
        elif call in MUT:
            paths, _ = split_args(call, args)
            M.append((ln, pid, call, ' -> '.join(paths), ret))
    return dict(ev=ev, left=left, W=W, M=M, calls=allcalls)
def norm(p):
    return re.sub(r'\.#lk0x[0-9a-f]+\.', '.#lk0xADDR.', p)
def report(name):
    d = run(name)
    succ = [w for w in d['W'] if w[5].lstrip('-').isdigit() and int(w[5]) >= 0]
    fail = [w for w in d['W'] if w not in succ]
    ms = [m for m in d['M'] if m[4].lstrip('-').isdigit() and int(m[4]) >= 0]
    mf = [m for m in d['M'] if m not in ms]
    print(f"== {name}")
    print(f"   completed events={len(d['ev'])} unfinished-leftover={d['left']}")
    print(f"   write-mode opens: {len(d['W'])} (success {len(succ)}, failed {len(fail)})")
    print(f"   mutating calls: {len(d['M'])} (success {len(ms)}, failed {len(mf)})")
    byclass = collections.Counter(classify(w[3]) for w in succ)
    print(f"   successful write-mode opens by path class: {dict(byclass)}")
    for w in succ:
        print(f"     L{w[0]} pid={w[1]} {w[2]} {w[3]} [{w[4][:80]}] ret={w[5]}")
    print("   failed write-mode opens (no file created):")
    for w in fail:
        print(f"     L{w[0]} pid={w[1]} {w[2]} {w[3]} [{w[4][:80]}] ret={w[5]}")
    print("   mutating calls successful:", [(m[0], m[2], m[3], m[4]) for m in ms] or 'none')
    print("   failed mutating calls:", [(m[0], m[2], m[3], m[4]) for m in mf])
    fs = sorted({classify(w[3])+':'+norm(w[3]) for w in d['W']} | {norm(m[3]) for m in d['M']})
    return set(fs), d
si, di = report(sys.argv[1])
sb, db = report(sys.argv[2])
print("\n== SET DIFF (normalized write-target/mutation paths)")
print("impl-only:", sorted(si - sb) or 'none')
print("base-only:", sorted(sb - si) or 'none')
print("shared   :", sorted(si & sb))
