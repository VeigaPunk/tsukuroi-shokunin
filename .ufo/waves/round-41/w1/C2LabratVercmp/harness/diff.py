#!/usr/bin/env python3
"""Differential: host vercmp vs pinned-source refvercmp vs PA8 textual predicate.

All scratch files stay under the seat scratch dir.
"""
import itertools, random, subprocess, sys, re

REF = "./refvercmp"
ALPHA = "0123456789abcdefghijklmnopqrstuvwxyz"


def rpmvercmp(a, b):
    """Faithful transliteration of the pinned rpmvercmp (version.c:95-236)."""
    if a == b:
        return 0
    one, two = 0, 0  # indices; emulate pointer walking
    n1, n2 = len(a), len(b)
    p1 = p2 = 0
    while one < n1 and two < n2:
        while one < n1 and not a[one].isalnum():
            one += 1
        while two < n2 and not b[two].isalnum():
            two += 1
        if not (one < n1 and two < n2):
            break
        if (one - p1) != (two - p2):
            return -1 if (one - p1) < (two - p2) else 1
        p1, p2 = one, two
        if a[p1].isdigit():
            while p1 < n1 and a[p1].isdigit():
                p1 += 1
            while p2 < n2 and b[p2].isdigit():
                p2 += 1
            isnum = True
        else:
            while p1 < n1 and a[p1].isalpha():
                p1 += 1
            while p2 < n2 and b[p2].isalpha():
                p2 += 1
            isnum = False
        sone, stwo = a[one:p1], b[two:p2]
        if sone == "":
            return -1
        if stwo == "":
            return 1 if isnum else -1
        if isnum:
            sone_s, stwo_s = sone.lstrip("0"), stwo.lstrip("0")
            if len(sone_s) > len(stwo_s):
                return 1
            if len(stwo_s) > len(sone_s):
                return -1
            sone, stwo = sone_s, stwo_s
        if sone != stwo:
            return -1 if sone < stwo else 1
        one, two = p1, p2
    if one >= n1 and two >= n2:
        return 0
    rest_one = "" if one >= n1 else a[one]
    rest_two = "" if two >= n2 else b[two]
    if (rest_one == "" and not rest_two.isalpha()) or (rest_one != "" and rest_one.isalpha()):
        return -1
    return 1


def parse_evr_pinned(evr):
    """parseEVR (version.c:39-77): digit run then ':' => epoch, else epoch '0'."""
    i = 0
    while i < len(evr) and evr[i].isdigit():
        i += 1
    s = i
    dash = evr.rfind("-", s) if "-" in evr[s:] else -1
    if s < len(evr) and evr[s] == ":":
        epoch = evr[:s] or "0"
        version = evr[s + 1:]
    else:
        epoch = "0"
        version = evr
    if dash != -1:
        release = evr[dash + 1:]
        # version is the slice of evr from its own start up to the dash
        vstart = s + 1 if (s < len(evr) and evr[s] == ":") else 0
        version = evr[vstart:dash]
    else:
        release = None
    return epoch, version, release


def predicate(a, b, release_mode="pointer", epoch_mode="digits"):
    """PA8's three-step rule, with selectable readings of the vague clauses."""
    def split(evr):
        e, v, r = parse_evr_pinned(evr)
        if epoch_mode == "first_colon" and ":" in evr:
            head, rest = evr.split(":", 1)
            e, v = (head or "0"), rest
            if "-" in rest:
                cut = rest.rfind("-")
                v, r = rest[:cut], rest[cut + 1:]
            else:
                r = None
        if release_mode == "nonempty" and r == "":
            r = None
        return e, v, r
    e1, v1, r1 = split(a)
    e2, v2, r2 = split(b)
    ret = rpmvercmp(e1, e2)
    if ret == 0:
        ret = rpmvercmp(v1, v2)
        if ret == 0 and r1 is not None and r2 is not None:
            ret = rpmvercmp(r1, r2)
    return ret


def host(a, b):
    p = subprocess.run(["vercmp", a, b], capture_output=True, text=True)
    return int(p.stdout.strip())


def ref(pairs):
    out = []
    for i in range(0, len(pairs), 400):
        chunk = pairs[i:i + 400]
        args = [x for pair in chunk for x in pair]
        p = subprocess.run([REF] + args, capture_output=True, text=True)
        for line in p.stdout.splitlines():
            out.append(int(line.split("\t")[2]))
    return out


TOK = ["0", "1", "2", "9", "10", "01", "a", "z", "alpha", "0.1", "1.0", "1.10",
       "1.0.0", "1.0a", "1_0", "1+0", "1.0.1", "999", "0.0"]
SEP = ["", ".", "-", ":", "..", "~", "_", "+"]


def gen(rng):
    def one():
        parts = [rng.choice(TOK)]
        for _ in range(rng.randint(0, 3)):
            parts.append(rng.choice(SEP))
            parts.append(rng.choice(TOK))
        s = "".join(parts)
        if rng.random() < 0.25:
            s = rng.choice(["", "0", "1", "01", "2", "10"]) + ":" + s
        if rng.random() < 0.05:
            s = s + "-"
        if rng.random() < 0.03:
            s = "-" + s
        return s
    return one()


def main():
    rng = random.Random(41041)
    pairs = []
    # exhaustive small alphabet: every 1-3 char string over a dense edge alphabet
    small = ["0", "1", "-", ":", ".", "a"]
    for n in (1, 2, 3):
        for tup in itertools.product(small, repeat=n):
            pairs.append("".join(tup))
    combos = [(x, y) for x in pairs for y in pairs]
    rng.shuffle(combos)
    pairs = combos[:4000]
    pairs += [(gen(rng), gen(rng)) for _ in range(4000)]

    h = [host(a, b) for a, b in pairs]
    r = ref(pairs)
    p_ptr = [predicate(a, b, "pointer", "digits") for a, b in pairs]
    p_ne = [predicate(a, b, "nonempty", "digits") for a, b in pairs]
    p_fc = [predicate(a, b, "pointer", "first_colon") for a, b in pairs]

    def report(name, pred):
        mism = [(pairs[i], h[i], pred[i]) for i in range(len(pairs)) if h[i] != pred[i]]
        print(f"{name}: {len(mism)} / {len(pairs)} disagree")
        seen = {}
        for pr, hv, pv in mism:
            key = (hv, pv)
            seen.setdefault(key, []).append(pr)
        for key, ex in sorted(seen.items()):
            print(f"  host={key[0]} pred={key[1]} n={len(ex)} ex={ex[:6]}")

    ref_mism = [(pairs[i], h[i], r[i]) for i in range(len(pairs)) if h[i] != r[i]]
    print(f"host vs pinned-source ref: {len(ref_mism)} / {len(pairs)} disagree")
    for m in ref_mism[:10]:
        print("  ", m)
    report("PA8 text, release=pointer (code reading)", p_ptr)
    report("PA8 text, release=nonempty (literal reading)", p_ne)
    report("PA8 text, epoch=first_colon (naive reading)", p_fc)


if __name__ == "__main__":
    main()
