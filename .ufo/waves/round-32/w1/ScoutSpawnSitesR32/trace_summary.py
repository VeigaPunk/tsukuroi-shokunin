import collections, glob, os, re

S = '/fast/scratch/hyaku/tsukuroi-r32/ScoutSpawnSitesR32/runs'
LINE = re.compile(r'^(\d+)\s+execve\("([^"]*)", \[(.*?)\], \[(.*)\]\) = 0')
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')
for d in sorted(glob.glob(S + '/*-A')):
    execs = []
    for ln in open(d + '/trace', errors='replace'):
        m = LINE.match(ln)
        if m:
            argv = STR.findall(m.group(3))
            env = dict(s.split('=', 1) if '=' in s else (s, '') for s in STR.findall(m.group(4)))
            execs.append((m.group(2), argv, env))
    ambient = execs[0][2]
    progs = collections.Counter()
    added = collections.defaultdict(set)
    passed = collections.defaultdict(set)
    changed = collections.defaultdict(set)
    for fname, argv, env in execs[1:]:
        key = fname
        if 'python' in os.path.basename(fname):
            key = 'python ' + (os.path.basename(argv[1]) if len(argv) > 1 else '?')
        progs[key] += 1
        for k, v in env.items():
            if k not in ambient:
                added[key].add(k)
            elif ambient[k] == v:
                passed[key].add(k)
            else:
                changed[key].add(k)
    print('==', os.path.basename(d)[:-2], 'ambient_names=%d execs_after_first=%d' % (len(ambient), len(execs) - 1))
    for k, n in sorted(progs.items()):
        print('   %s x%d | ambient passed unchanged: %d of %d | overridden: %s | added: %s' % (
            k, n, len(passed[k]), len(ambient), ','.join(sorted(changed[k])), ','.join(sorted(added[k]))))
