import importlib.util, json, re, sys, subprocess, os
spec = importlib.util.spec_from_file_location('c', 'repo/tools/check-adjacency-overlap.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
def contains_anchor(needle, haystack):
    needle, haystack = c.norm(needle), c.norm(haystack)
    return bool(re.search(r'(?<![\w])(?<![\w][.\-@/:])%s(?![\w]|[.\-@/:]\w)' % re.escape(needle), haystack))
c.contains_anchor = contains_anchor
shas = {json.loads(l)['variant']: json.loads(l)['sha'] for l in open(sys.argv[1])}
for v in ('control', 'f-b10-version-cut', 'f-b10-unit-name-cut', 'f-b10-hyphen-cut', 'p-b9-ov4-lane-other-sentence', 'p-b9-ov2-lane-drifted-target', 'p-ov6-quote-line-corrected'):
    code, out = c.evaluate(os.path.abspath('repo'), shas[v], '/home/vgpnk/Projects/shokunin')
    print(v, code, out['anchored_rows'], {k: x for k, x in out['rows'].items() if x})
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf): rc = c.selftest()
d = json.loads(buf.getvalue()); print('selftest', rc, d['cases'], d['failed'])
