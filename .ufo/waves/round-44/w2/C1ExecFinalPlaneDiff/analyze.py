#!/usr/bin/env python3
"""C1ExecFinalPlaneDiff analyzer: exact, derived diffs of six live census captures.

Rules (from the seat spec): drop the header (the only line carrying a timestamp) and the SCRUB
line, then diff. Any leftover difference must recur between two runs of one revision.
No hard-coded field lists: the differing-token set is derived from the captures.
"""
import hashlib
import itertools
import json
import pathlib
import re
import sys

OUT = pathlib.Path("/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff/out")
RUNS = [(rev, n) for n in (1, 2, 3) for rev in ("base", "tip")]
RUNS.sort(key=lambda r: r[1])
HDR = re.compile(r"^tsukuroi-census census-v2 — host=\S+ — \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ — read-only$")
TSISH = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ")


def load(rev, n):
    raw = (OUT / f"out-{rev}-{n}.txt").read_text().splitlines()
    assert HDR.match(raw[0]), raw[0]
    body = raw[1:]
    scrub = [ln for ln in body if ln.startswith("SCRUB ")]
    kept = [ln for ln in body if not ln.startswith("SCRUB ")]
    return raw, body, scrub, kept


def kind(line):
    return line.split(":")[0] if ":" in line else line.split()[0]


def tokens(line):
    return line.split(" ")


def keyed(tok):
    return tok.split("=", 1)[0] if "=" in tok else None


def pair_diff(a, b):
    """Return list of (line_idx, kind, [(key, va, vb)...], structural_note)."""
    out = []
    if len(a) != len(b):
        out.append((-1, "<line-count>", [], f"{len(a)} vs {len(b)} lines"))
        return out
    for i, (la, lb) in enumerate(zip(a, b)):
        if la == lb:
            continue
        ta, tb = tokens(la), tokens(lb)
        subs = []
        if len(ta) == len(tb):
            for x, y in zip(ta, tb):
                if x != y:
                    subs.append((keyed(x) or keyed(y) or f"<pos:{x}|{y}>", x, y))
        else:
            # split on '=' runs is not stable; fall back to a diff of the token multisets
            sa, sb = set(ta), set(tb)
            for x in ta:
                if x not in sb:
                    subs.append((keyed(x) or x, x, ""))
            for y in tb:
                if y not in sa:
                    subs.append((keyed(y) or y, "", y))
        out.append((i, kind(la), subs, "" if len(ta) == len(tb) else f"tokens {len(ta)} vs {len(tb)}"))
    return out


def mask(lines, fields):
    pat = re.compile(r"\b(" + "|".join(re.escape(f) for f in sorted(fields)) + r")=[^;)\s]*")
    return [pat.sub(lambda m: m.group(1) + "=<masked>", ln) for ln in lines]


def main():
    caps = {}
    for rev, n in RUNS:
        raw, body, scrub, kept = load(rev, n)
        # the header must be the ONLY timestamp-bearing line
        extra_ts = [ln for ln in body if TSISH.search(ln)]
        caps[(rev, n)] = dict(raw=raw, body=body, scrub=scrub, kept=kept, extra_ts=extra_ts)
        print(f"[load] {rev}-{n}: raw={len(raw)} kept={len(kept)} scrub={len(scrub)} "
              f"extra-timestamp-lines={len(extra_ts)}")
        if extra_ts:
            for ln in extra_ts:
                print("       TIMESTAMP-BEARING:", ln[:120])

    # --- structure: same number of kept lines, same line kinds except the SCRUB insertion point
    keeplens = {k: len(v["kept"]) for k, v in caps.items()}
    print("\n[structure] kept line counts:", keeplens)
    shapes = {k: [kind(ln) for ln in v["kept"]] for k, v in caps.items()}
    base_shape = shapes[("base", 1)]
    for k, s in shapes.items():
        assert s == base_shape, (k, s)
    print("[structure] every kept file has the same line kinds:", base_shape)

    # --- SCRUB line stability
    scrub_lines = {k: v["scrub"] for k, v in caps.items()}
    print("[scrub] base counts:", {k: len(v) for k, v in scrub_lines.items() if k[0] == "base"},
          " tip counts:", {k: len(v) for k, v in scrub_lines.items() if k[0] == "tip"})
    tip_scrub = {tuple(v) for k, v in scrub_lines.items() if k[0] == "tip"}
    print("[scrub] distinct tip SCRUB line tuples:", len(tip_scrub))
    for t in tip_scrub:
        print("       ", t)

    # --- all 15 pairs
    pairs = list(itertools.combinations(sorted(caps, key=lambda k: (k[1], k[0])), 2))
    all_fields = set()
    print("\n[pairs] differing tokens per pair (after dropping header + SCRUB):")
    report = {}
    for ka, kb in pairs:
        d = pair_diff(caps[ka]["kept"], caps[kb]["kept"])
        fields = sorted({f for _, _, subs, _ in d for f, _, _ in subs})
        same = ka[0] == kb[0]
        tag = "SAME-REV" if same else "cross-rev"
        all_fields.update(fields)
        report[(ka, kb)] = (fields, d)
        print(f"  {ka[0]}-{ka[1]} vs {kb[0]}-{kb[1]}  [{tag}]  lines={len(d)}  fields={fields}")
        for i, kd, subs, note in d:
            print(f"      line[{kd}] subs={len(subs)} {note}")
            for f, x, y in subs:
                print(f"        {f}: {x} -> {y}")

    print("\n[fields] union of differing fields over all 15 pairs:", sorted(all_fields))

    # cross-rev union vs same-rev union
    cross = set().union(*[f for (ka, kb), (f, _) in report.items() if ka[0] != kb[0]]) if report else set()
    same = set().union(*[f for (ka, kb), (f, _) in report.items() if ka[0] == kb[0]]) if report else set()
    print("[fields] cross-rev union:", sorted(cross))
    print("[fields] same-rev union:", sorted(same))
    print("[fields] cross-rev minus same-rev (revision effect):", sorted(cross - same))

    # --- masked hashes: mask only fields that ever differ
    print("\n[masked] sha256 of header-dropped, SCRUB-dropped, fields-masked body:")
    digests = {}
    for k in sorted(caps, key=lambda k: (k[1], k[0])):
        m = mask(caps[k]["kept"], all_fields)
        h = hashlib.sha256("\n".join(m).encode()).hexdigest()
        digests[k] = h
        print(f"  {k[0]}-{k[1]}  {h}")
    print("[masked] distinct digests:", len(set(digests.values())))

    # --- every field-differing line must be confined to PLANE lines; rollup must be byte-identical
    differing_kinds = {kd for (f, d) in report.values() for (_, kd, _, _) in d}
    print("[scope] line kinds that ever differ:", sorted(differing_kinds))
    rollup = {k: [ln for ln in v["kept"] if ln.startswith("TSUKUROI_CENSUS:")] for k, v in caps.items()}
    rollup_set = {tuple(v) for v in rollup.values()}
    print("[rollup] distinct rollup lines across six runs:", len(rollup_set))
    for r in rollup_set:
        print("        ", r)
    plane_ok = all(ln.startswith(("PLANE ", "HANDOFF ", "DRIFT ", "STORAGE ")) or ln.startswith("TSUKUROI_CENSUS:")
                   for ln in caps[("base", 1)]["kept"])
    print("[scope] every kept line is a known fixed-shape line:", plane_ok)

    # --- exit codes
    rcs = {k: (OUT / f"rc-{k[0]}-{k[1]}.txt").read_text().strip() for k in caps}
    print("\n[rc] exit codes:", {f"{k[0]}-{k[1]}": v for k, v in sorted(rcs.items(), key=lambda kv: kv[0][1])})
    print("[rc] distinct exit codes:", sorted(set(rcs.values())))

    # --- non-PLANE verdict tokens (the status words) must be identical
    verdicts = {}
    for k, v in caps.items():
        verdicts[k] = [ln.split(" (")[0] for ln in v["kept"]]
    same_verdicts = len({tuple(v) for v in verdicts.values()}) == 1
    print("[verdict-words] identical in all six runs:", same_verdicts)

    (OUT / "analysis.json").write_text(json.dumps({
        "fields_union": sorted(all_fields),
        "cross_rev_union": sorted(cross),
        "same_rev_union": sorted(same),
        "revision_effect_fields": sorted(cross - same),
        "masked_digests": {f"{k[0]}-{k[1]}": v for k, v in digests.items()},
        "differing_kinds": sorted(differing_kinds),
        "rcs": {f"{k[0]}-{k[1]}": v for k, v in sorted(rcs.items(), key=lambda kv: kv[0][1])},
        "rollup_lines": [list(r) for r in rollup_set],
        "scrub_tip_distinct": [list(t) for t in tip_scrub],
        "scrub_base_lines": sum(len(v) for k, v in scrub_lines.items() if k[0] == "base"),
        "verdict_words_identical": same_verdicts,
    }, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
