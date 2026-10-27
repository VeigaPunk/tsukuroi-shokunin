import re, sys, collections
WRITE = re.compile(r'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND')
CREATE = {'creat','mknod','mknodat','mkdir','mkdirat','rename','renameat','renameat2',
          'link','linkat','symlink','symlinkat','truncate','unlink','unlinkat','rmdir'}
CALL = re.compile(r'^(\d+)\s+(\w+)\((.*)$')
RES  = re.compile(r'^(.*)\)\s+=\s+(-?\d+|\?)(.*)$')
def events(path):
    pend, ev = {}, []
    for i, raw in enumerate(open(path, errors='replace'), 1):
        line = raw.rstrip('\n')
        m = CALL.match(line)
        if m:
            pid, call, rest = m.groups()
            if '<unfinished ...>' in rest:
                pend[(pid, call)] = (i, rest.replace('<unfinished ...>', '')); continue
            r = RES.match(rest)
            if r: ev.append((i, pid, call, r.group(1), r.group(2), r.group(3)))
            continue
        m2 = re.match(r'^(\d+)\s+<\.\.\. (\w+) resumed>(.*)$', line)
        if m2:
            pid, call, rest = m2.groups(); pre = pend.pop((pid, call), None)
            if pre is None: continue
            r = RES.match(pre[1] + rest)
            if r: ev.append((pre[0], pid, call, r.group(1), r.group(2), r.group(3)))
    return ev, len(pend)
def q(args): return re.findall(r'"((?:[^"\\]|\\.)*)"', args)
def ok(ret): return ret.lstrip('-').isdigit() and int(ret) >= 0
def cls(p):
    return 'pseudo' if p.startswith(('/dev/','/proc/','/sys/')) else 'fs'
def norm(p):
    p = re.sub(r'\.#lk0x[0-9a-f]+\.', '.#lk0xADDR.', p)
    p = re.sub(r'/proc/self/task/\d+/comm', '/proc/self/task/TID/comm', p)
    p = re.sub(r'\.#lk0xADDR\.[^.]+\.\d+$', '.#lk0xADDR.HOST.PID', p)
    return p
def run(path):
    ev, left = events(path)
    cmds = {}
    writes, creates, execs = [], [], []
    for ln, pid, call, args, ret, tail in ev:
        if call == 'execve':
            argv = q(args); cmds.setdefault(pid, argv[0] if argv else '?')
            execs.append((ln, pid, argv))
            continue
        if call in ('open','openat','openat2'):
            paths = q(args)
            if not paths: continue
            idx = args.rfind('"'); flags = args[idx+1:]
            if WRITE.search(flags):
                writes.append((ln, pid, call, paths[0], flags.strip(), ret, tail.strip(), cmds.get(pid,'?')))
        elif call in CREATE:
            paths = q(args)
            creates.append((ln, pid, call, ' -> '.join(paths), ret, tail.strip(), cmds.get(pid,'?')))
    return dict(ev=ev, left=left, writes=writes, creates=creates, execs=execs, cmds=cmds)
def show(name):
    d = run(name)
    print(f"== {name}")
    print(f"   completed={len(d['ev'])} unfinished-left={d['left']} procs-exec={len(d['execs'])}")
    ws = [w for w in d['writes'] if ok(w[5])]; wf = [w for w in d['writes'] if not ok(w[5])]
    cs = [c for c in d['creates'] if ok(c[4])]; cf = [c for c in d['creates'] if not ok(c[4])]
    print(f"   write-mode opens={len(d['writes'])} success={len(ws)} failed={len(wf)}")
    print(f"   fs-class successful write-mode opens={len([w for w in ws if cls(w[3])=='fs'])}")
    print(f"   create/mutate calls={len(d['creates'])} success={len(cs)} failed={len(cf)}")
    print("   SUCCESS write-mode opens grouped:")
    g = collections.Counter((w[3], w[4]) for w in ws)
    for (p, f), n in sorted(g.items()): print(f"     {n:4d}x {p}  [{f}]")
    print("   FAILED write-mode opens:")
    for w in wf: print(f"     L{w[0]} {w[2]} {w[3]} [{w[4][:60]}] ret={w[5]} {w[6][:40]} cmd={w[7]}")
    print("   SUCCESS create/mutate:")
    for c in cs: print(f"     L{c[0]} {c[2]} {c[3]} ret={c[4]} {c[5][:40]} cmd={c[6]}")
    print("   FAILED create/mutate:")
    for c in cf: print(f"     L{c[0]} {c[2]} {c[3]} ret={c[4]} {c[5][:40]} cmd={c[6]}")
    sets = {cls(w[3])+':'+norm(w[3]) for w in d['writes']} | {norm(c[3]) for c in d['creates']}
    return sets, d
si, di = show(sys.argv[1]); sb, db = show(sys.argv[2])
print("\n== NORMALIZED SET DIFF")
print("impl-only:", sorted(si - sb) or 'none')
print("base-only:", sorted(sb - si) or 'none')
print("shared:", len(si & sb))
