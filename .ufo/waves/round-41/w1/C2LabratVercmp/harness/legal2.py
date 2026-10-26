#!/usr/bin/env python3
"""PA8's rule text, split by the documented grammar (not by parseEVR), vs the
pinned-source reference over the whole legal grid, plus host-observed invariants.
"""
import diff as D
from legal import EPOCHS, VERS, RELS, split_legal, FULL


def text_rule(a, b):
    """PA8 as written: epoch (absent = 0), then version, then release iff both carry one."""
    e1, v1, r1 = split_legal(a)
    e2, v2, r2 = split_legal(b)
    ret = D.rpmvercmp(e1, e2)
    if ret == 0:
        ret = D.rpmvercmp(v1, v2)
        if ret == 0 and r1 is not None and r2 is not None:
            ret = D.rpmvercmp(r1, r2)
    return ret


def run(name, cases, ok):
    bad = []
    for c in cases:
        h = D.host(c[0], c[1])
        if not ok(c, h):
            bad.append(c + (h,))
    print(f"{name}: {len(cases)} cases, {len(bad)} violations")
    for m in bad[:8]:
        print("   ", m)
    return bad


pairs = [(a, b) for a in FULL for b in FULL]
ref = D.ref(pairs)
pred = [text_rule(a, b) for a, b in pairs]
mism = [(pairs[i], ref[i], pred[i]) for i in range(len(pairs)) if ref[i] != pred[i]]
print(f"PA8 text (documented grammar) vs pinned source, {len(pairs)} legal pairs: "
      f"{len(mism)} mismatches")
for m in mism[:10]:
    print("   ", m)

def strip(e):
    return e[:-1] if e.endswith(":") else e


# A: a higher epoch decides alone
casesA = []
for e1 in EPOCHS:
    for e2 in EPOCHS:
        if D.rpmvercmp(strip(e1) or "0", strip(e2) or "0") == 0:
            continue
        for v1 in VERS:
            for v2 in VERS:
                casesA.append((e1 + v1 + "-1", e2 + v2 + "-99"))
        if len(casesA) > 1200:
            break
run("A epoch decides alone", casesA[:1200],
    lambda c, h: (D.rpmvercmp(strip(split_legal(c[0])[0]),
                              strip(split_legal(c[1])[0])) > 0) == (h > 0))

# B: equal pkgver, one side without pkgrel -> 0
casesB = [(e + v, e + v + r) for e in EPOCHS for v in VERS for r in RELS[1:]]
run("B equal pkgver, one side lacks pkgrel -> 0", casesB, lambda c, h: h == 0)

# C: equal epoch and pkgver, both with pkgrel -> sign of the release comparison
casesC = [(e + v + r1, e + v + r2) for e in ["", "0:", "1:"]
          for v in ["1.0", "2.0"] for r1 in RELS[1:] for r2 in RELS[1:]]
run("C release decides when both carry one", casesC,
    lambda c, h: (h > 0) == (D.rpmvercmp(split_legal(c[0])[2], split_legal(c[1])[2]) > 0))

# D: differing pkgver -> pkgrel never consulted
casesD = [(e1 + v1 + "-1", e2 + v2 + "-2") for e1 in ["", "1:"] for e2 in ["", "2:"]
          for v1 in ["1.0", "1.10", "2.0"] for v2 in ["1.0", "1.9", "999"] if v1 != v2]
run("D pkgrel irrelevant when pkgver differs", casesD,
    lambda c, h: (h > 0) == ((D.rpmvercmp(strip(split_legal(c[0])[0]),
                                         strip(split_legal(c[1])[0])) > 0)
                             or (D.rpmvercmp(strip(split_legal(c[0])[0]),
                                             strip(split_legal(c[1])[0])) == 0
                                 and D.rpmvercmp(split_legal(c[0])[1],
                                                 split_legal(c[1])[1]) > 0)))
