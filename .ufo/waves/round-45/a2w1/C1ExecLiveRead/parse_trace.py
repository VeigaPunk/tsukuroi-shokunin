import re, sys, json
WRITE = re.compile(r'O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND')
def unq(s):
    # strace escapes; keep raw enough for path identity
    return s
def parse(path):
    events = []
    with open(path, 'r', errors='replace') as f:
        for line in f:
            m = re.match(r'^(\d+)\s+(\w+)\((.*)\)\s+=\s+(-?\d+|\?)(.*)$', line.rstrip('\n'))
            if not m:
                # unfinished / resumed / signal / exit lines
                continue
            pid, call, args, ret, rest = m.groups()
            if call in ('open','openat'):
                q = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
                if not q: continue
                p = q[0]
                flags = args.split('"',2)[2] if args.count('"')>=2 else ''
                if call=='openat':
                    flags = args.split(',',2)[2] if args.count(',')>=2 else ''
                if WRITE.search(flags) or re.search(r'\b0?[0-9]*\b', '') :
                    pass
                wr = bool(WRITE.search(flags))
                events.append(dict(pid=pid, call=call, path=p, ret=ret, write=wr, flags=flags.strip()))
            elif call == 'creat':
                q = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
                events.append(dict(pid=pid, call=call, path=q[0] if q else '', ret=ret, write=True, flags=''))
            elif call in ('mkdir','mkdirat','unlink','unlinkat','rmdir'):
                q = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
                events.append(dict(pid=pid, call=call, path=q[-1] if q else '', ret=ret, write=True, flags=''))
            elif call in ('rename','renameat','renameat2','link','linkat','symlink','symlinkat'):
                q = re.findall(r'"((?:[^"\\]|\\.)*)"', args)
                events.append(dict(pid=pid, call=call, path=' -> '.join(q), ret=ret, write=True, flags=''))
    return events
def summarize(path):
    ev = parse(path)
    writes = [e for e in ev if e['write']]
    succ = [e for e in writes if e['ret'].isdigit() and int(e['ret'])>=0]
    return ev, writes, succ
for name in sys.argv[1:]:
    ev, writes, succ = summarize(name)
    print(f'== {name}: traced-parseable={len(ev)} write-events={len(writes)} success={len(succ)}')
    for e in succ:
        print(f"  OK   {e['call']:9s} {e['path']}  [{e['flags'][:90]}]")
    fails = [e for e in writes if e not in succ]
    for e in fails:
        print(f"  FAIL {e['call']:9s} {e['path']}  ret={e['ret']} [{e['flags'][:60]}]")
