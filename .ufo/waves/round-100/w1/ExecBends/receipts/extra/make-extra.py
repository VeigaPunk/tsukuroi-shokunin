import hashlib
gate = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py"
src = open(gate, "rb").read()
target = (b'    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
          b'            "limine_version": limine_version,\n')
assert src.count(target) == 1, src.count(target)
def make(path, comp):
    expr = ('    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
            '            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "%s" '
            'else limine_version),  # SCRATCH extra falsifier (first component %s)\n' % (comp, comp))
    out = src.replace(target, expr.encode())
    assert out != src
    open(path, "wb").write(out)
    print(path, hashlib.sha256(out).hexdigest())
make("extra/key12.py", "12")
make("extra/key13.py", "13")
