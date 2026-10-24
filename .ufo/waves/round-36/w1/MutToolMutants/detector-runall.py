import json, subprocess, sys, os
sys.path.insert(0,'/tmp/mutw')
import det2
W='/tmp/mutw'
LANE='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='189d8a080ba8d508d5faab12cad9e688aee91dab'
CASES = {
 'm1': ('tools/check-revision-binding.py', ['--tools-revision', REV, '--branch', 'master'], 240),
 'm1s': ('tools/check-revision-binding.py', ['--selftest'], 240),
 'm2': ('tools/check-report-receipts.py', ['--report', LANE+'/SCORECARD.md', '--lane', LANE, '--revision', REV], 180),
 'm3': ('tools/score-census-handoff-r32.py', ['--revision', REV, '--lane', LANE, '--scenarios', '1', '--timeout', '60'], 240),
 'm4': ('tools/mutants-btrfs-space-r30.py', [], 240),
 'm5': ('tools/run-receipt.py', ['--revision', REV, '--tool-revision', REV, '--lane', LANE, '--out', '/tmp/mutw/rec.jsonl', '--timeout', '120', '--', 'tools/probe-child-env-allowlist-r34.py', '--version'], 240),
 'm6': ('tools/check-report-receipts.py', ['--report', LANE+'/SCORECARD.md', '--lane', LANE, '--revision', REV], 180),
}
which = sys.argv[1:] or list(CASES)
out={}
for tag in which:
    tool, argv, to = CASES[tag]
    trees = [('pristine', os.path.join(W,'changed'))] + ([('mutant', os.path.join(W,tag))] if tag!='pristine' else [])
    if tag=='pristine':
        trees=[('pristine', os.path.join(W,'changed'))]
    for name, tree in trees:
        r = det2.run_case(tree, tool, argv, timeout=to)
        out.setdefault(tag, {})[name]=r
        print(tag, name, json.dumps({k:r[k] for k in ('rc','timed_out','seconds','n_children','n_marker_leaks','n_nonfixed_path')}), flush=True)
json.dump(out, open('/tmp/mutw/det-results.json','w'), indent=1)
