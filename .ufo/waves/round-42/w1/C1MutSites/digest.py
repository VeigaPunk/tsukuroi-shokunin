import json
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/w1/C1MutSites'
for n in ['base', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6']:
    d = json.load(open(f'{L}/{n}.json'))
    print(f"== {n} rev={d['revision'][:12]} verdict={d['verdict']} inv={d['invariant']}/{d['cases']} "
          f"non_inv={d['non_invariant']} ns={d['ns_invariant']}/3 selftest={d['selftest_pass']} "
          f"(rc={d['selftest_rc']}, {d['selftest_label'][:70]}) default_equal={d['default_equal']} token={d['token']}")
    for c in d['non_invariant']:
        pc = d['per_case'][c]
        extra = '; '.join(pc['large_lines_not_in_small'][:2])
        print(f"   {c}: small_rc={pc['small_rc']} large_rc={pc['large_rc']} large_extra[:2]={extra[:220]!r}")
    for k, nc in sorted(d.get('ns_cases', {}).items()):
        if not nc['invariant']:
            print(f"   {k}: small={nc['small'][:110]!r} large={nc['large'][:110]!r} err_tail={nc.get('stderr_tail','')[-110:]!r}")
