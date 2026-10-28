import json,sys
for p in sys.argv[1:]:
    t=open(p,encoding='utf-8',errors='replace').read().strip().split('\n')
    try: d=json.loads(t[-1])
    except Exception: print(p,'NONJSON:',t[-1][:300]); continue
    keys=['verdict','error','revision','adj_rows','linked_rows','bare_ranges','anchors_ok','registry_ok','anchors_checker_rc','quote_at_pin_ok','live_quote_ok','stub_fails','display_bound_ok','quote_specific_ok','digests_bound_ok','display_forge_fails','override_blocked','r50_blind','r50_problems','note']
    print(p.split('/')[-1], {k:d[k] for k in keys if k in d})
