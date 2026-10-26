#!/usr/bin/env python3
"""Legal-shape exhaustive check of PA8 against the host and the pinned source.

Legal per PKGBUILD.5 (frozen snapshot): pkgver has no ':' '/' '-' whitespace;
pkgrel is digits[.digits]; epoch is digits or absent.
"""
import itertools, random, sys
import diff as D

EPOCHS = ["", "0:", "1:", "2:", "10:"]
VERS = ["1.0", "1.0.1", "1.0a", "0.1", "1.10", "2.0", "1_0", "1+0", "a",
        "1.0.r1", "999"]
RELS = ["", "-1", "-2", "-10", "-1.0", "-1.1", "-1.10", "-99"]

FULL = [e + v + r for e in EPOCHS for v in VERS for r in RELS]


def split_legal(full):
    e, v = "0", full
    if ":" in full:
        e, v = full.split(":", 1)
    r = None
    if "-" in v:
        cut = v.rfind("-")
        v, r = v[:cut], v[cut + 1:]
    return e, v, r


def main():
    pairs = [(a, b) for a in FULL for b in FULL]
    print(f"legal versions: {len(FULL)}  pairs: {len(pairs)}")
    ref = D.ref(pairs)
    pred = [D.predicate(a, b, "pointer", "digits") for a, b in pairs]
    mism = [(pairs[i], ref[i], pred[i]) for i in range(len(pairs)) if ref[i] != pred[i]]
    print(f"PA8 three-step rule vs pinned source over legal space: {len(mism)} mismatches")
    for m in mism[:10]:
        print("  ", m)

    rng = random.Random(7)
    sample = rng.sample(pairs, 8000)
    hv = [D.host(a, b) for a, b in sample]
    rv = D.ref(sample)
    hm = [(sample[i], hv[i], rv[i]) for i in range(len(sample)) if hv[i] != rv[i]]
    print(f"host vs pinned source on {len(sample)} sampled legal pairs: {len(hm)} mismatches")
    for m in hm[:10]:
        print("  ", m)

    # invariant A: a higher epoch decides alone
    bad = [(a, b, D.predicate(a, b)) for a, b in pairs
           if split_legal(a)[0] != split_legal(b)[0]
           and ((D.rpmvercmp(split_legal(a)[0], split_legal(b)[0]) > 0) !=
                (D.host(a, b) > 0))]
    # cheap check on a sample of the epoch-differing pairs (host spawns are costly)
    sample_a = rng.sample([p for p in pairs if split_legal(p[0])[0] != split_legal(p[1])[0]], 1500)
    bad = [(a, b, hv := D.host(a, b)) for a, b in sample_a
           if (D.rpmvercmp(split_legal(a)[0], split_legal(b)[0]) > 0) != (hv > 0)]
    print(f"invariant A (epoch decides alone) on {len(sample_a)} pairs: {len(bad)} violations")
    for m in bad[:10]:
        print("  ", m)

    # invariant B: equal pkgver, one side without pkgrel -> 0
    badB = []
    for a, b in sample:
        ea, va, ra = split_legal(a)
        eb, vb, rb = split_legal(b)
        if va == vb and ((ra is None) != (rb is None)):
            h = D.host(a, b)
            if h != 0:
                badB.append((a, b, h))
    print(f"invariant B (pkgver equal, one side lacks pkgrel -> 0): {len(badB)} violations")
    for m in badB[:10]:
        print("  ", m)

    # invariant D: differing pkgver -> result independent of pkgrel
    badD = []
    base = [(a, b) for a in FULL for b in FULL
            if split_legal(a)[1] != split_legal(b)[1]]
    for a, b in rng.sample(base, 1200):
        ea, va, ra = split_legal(a)
        eb, vb, rb = split_legal(b)
        h1 = D.host(a, b)
        pa = a.split(":", 1)[0] + ":" if ":" in a else ""
        pb = b.split(":", 1)[0] + ":" if ":" in b else ""
        a2 = pa + va + "-1"
        b2 = pb + vb + "-2"
        h2 = D.host(a2, b2)
        if (h1 > 0) != (h2 > 0) or (h1 == 0) or (h2 == 0):
            badD.append((a, b, h1, a2, b2, h2))
    print(f"invariant D (pkgrel irrelevant once pkgver differs), 1200 pairs: {len(badD)} violations")
    for m in badD[:10]:
        print("  ", m)


if __name__ == "__main__":
    main()
