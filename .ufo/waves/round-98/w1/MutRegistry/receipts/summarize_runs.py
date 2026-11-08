import glob, json, os, sys
for path in sorted(sys.argv[1:]):
    try:
        d = json.load(open(path))
    except Exception as exc:
        print("%s PARSE-FAIL %s" % (os.path.basename(path), exc)); continue
    runs = d if isinstance(d, list) else [d]
    for i, r in enumerate(runs):
        if "case_log" not in r:
            print("%s run%d NOT-A-BATTERY-RUN keys=%s" % (os.path.basename(path), i, sorted(r)[:6])); continue
        errs = sum(1 for e in r["case_log"] if e.get("error"))
        print("%s run%d families %d/%d verdict %s failed [%s] cases %d error_rows %d"
              % (os.path.basename(path), i, r["families_passed"], r["families_total"], r["verdict"],
                 ",".join(r["failed_families"]), r["cases"], errs))
