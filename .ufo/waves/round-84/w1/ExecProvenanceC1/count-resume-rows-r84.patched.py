#!/usr/bin/env python3
"""Round-84 C1 counter: sourced, host-measured rows in the hibernate-resume entry.

Usage:
  count-resume-rows-r84.py --revision REV [--repo DIR] [--entry PATH]
  count-resume-rows-r84.py --root DIR [--entry PATH]
  count-resume-rows-r84.py --selftest [--revision REV] [--repo DIR]

Both input paths run the same predicate. --revision reads every file with
`git show REV:path` (scrubbed environment); --root reads files under DIR.

Frozen predicate (C1, round 84). A row COUNTS iff all hold:
  R1 id matches ^HR[0-9]+$ and is unique in the entry;
  R2 statement is a string of at least 8 words;
  R3 source.snapshot names an entry snapshot whose path is listed in the
     frozen source manifest (.ufo/waves/round-84/before/src/SHA256SUMS) with
     the same sha256 the entry declares, and the file bytes hash to it;
  R4 source.quote is 6-25 words (whitespace-normalised) and source.lines
     [a,b] is the EXACT minimal raw-line span whose normalised text contains
     the quote (a<=b; dropping line a or line b loses the quote);
  R5 host.receipt names an entry receipt listed in the frozen host manifest
     (.ufo/waves/round-84/before/host/SHA256SUMS) with matching sha256, and
     host.value (non-empty) has host.lines [c,d] as its exact minimal span;
  R6 the row's normalised quote and its (snapshot, a, b) differ from every
     earlier counted row.
Both manifests are themselves pinned by sha256 constants below; a manifest
whose bytes differ is cannot-evaluate (rc 2) before any row is scored.

Verdict: met (rc 0) iff counted >= 7, failed == 0 and the counted rows cite
>= 4 distinct snapshots; otherwise unmet (rc 1). Missing or unparseable entry,
manifest pin mismatch or a git error: cannot-evaluate (rc 2), JSON on stdout.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

ENTRY = "corpus/knowledge/hibernate-resume-plane-r84.json"
SRC_MANIFEST = ".ufo/waves/round-84/before/src/SHA256SUMS"
HOST_MANIFEST = ".ufo/waves/round-84/before/host/SHA256SUMS"
MANIFEST_PINS = {
    SRC_MANIFEST: "5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef",
    HOST_MANIFEST: "4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6",
}
TARGET_ROWS = 7
TARGET_SNAPSHOTS = 4
GIT_ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "HOME": "/nonexistent"}


class CannotEvaluate(Exception):
    pass


class Reader:
    def __init__(self, root=None, revision=None, repo=None):
        self.root, self.revision, self.repo = root, revision, repo or os.getcwd()

    def get(self, path):
        if self.revision:
            p = subprocess.run(["git", "-C", self.repo, "show", f"{self.revision}:{path}"],
                               capture_output=True, env=GIT_ENV, timeout=60)
            if p.returncode != 0:
                return None
            return p.stdout
        full = os.path.join(self.root, path)
        try:
            with open(full, "rb") as fh:
                return fh.read()
        except OSError:
            return None


def norm(s):
    return " ".join(s.split())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def parse_manifest(data, base):
    out = {}
    for line in data.decode("utf-8", "replace").splitlines():
        m = re.match(r"^([0-9a-f]{64})  (\S+)$", line)
        if m:
            out[f"{base}/{m.group(2)}"] = m.group(1)
    return out


def exact_span(lines, a, b, needle):
    """lines: list of raw lines (1-based a..b). True iff [a,b] is the minimal span."""
    if not (isinstance(a, int) and isinstance(b, int)) or isinstance(a, bool) or isinstance(b, bool):
        return False, "lines-not-int"
    if not (1 <= a <= b <= len(lines)):
        return False, "lines-out-of-range"
    n = norm(needle)
    if not n:
        return False, "empty-needle"
    if n not in norm(" ".join(lines[a - 1:b])):
        return False, "not-in-span"
    if a < b and (n in norm(" ".join(lines[a:b])) or n in norm(" ".join(lines[a - 1:b - 1]))):
        return False, "span-not-minimal"
    return True, "ok"


def evaluate(reader, entry_path=ENTRY):
    manifests, by_kind = {}, {}
    for mpath, pin in MANIFEST_PINS.items():
        data = reader.get(mpath)
        if data is None:
            raise CannotEvaluate(f"manifest-absent:{mpath}")
        if sha(data) != pin:
            raise CannotEvaluate(f"manifest-pin-mismatch:{mpath}")
        parsed = parse_manifest(data, os.path.dirname(mpath))
        by_kind["snapshot" if mpath == SRC_MANIFEST else "receipt"] = parsed
        manifests.update(parsed)
    raw = reader.get(entry_path)
    if raw is None:
        raise CannotEvaluate(f"entry-absent:{entry_path}")
    try:
        entry = json.loads(raw.decode("utf-8"))
        rows = entry["rows"]
        snaps = entry["snapshots"]
        receipts = entry["receipts"]
        assert isinstance(rows, list) and isinstance(snaps, dict) and isinstance(receipts, dict)
    except Exception as e:  # noqa: BLE001 - any parse failure is cannot-evaluate
        raise CannotEvaluate(f"entry-unparseable:{type(e).__name__}")

    cache = {}

    def load(kind, key):
        table = snaps if kind == "snapshot" else receipts
        d = table.get(key) if isinstance(key, str) else None
        if not isinstance(d, dict) or not isinstance(d.get("path"), str):
            return None, f"{kind}-undeclared"
        path, declared = d["path"], d.get("sha256")
        if kind == "snapshot" and not str(d.get("url", "")).startswith("https://"):
            return None, "snapshot-url-not-https"
        kind_manifest = by_kind[kind]
        if kind_manifest.get(path) is None:
            return None, f"{kind}-not-in-frozen-manifest"
        if declared != kind_manifest[path]:
            return None, f"{kind}-declared-sha-differs-from-manifest"
        if path not in cache:
            data = reader.get(path)
            cache[path] = data
        data = cache[path]
        if data is None:
            return None, f"{kind}-absent"
        if sha(data) != kind_manifest[path]:
            return None, f"{kind}-bytes-differ-from-manifest"
        return data.decode("utf-8", "replace").split("\n"), "ok"

    results, seen_ids, dup_ids = [], set(), set()
    for r in rows:
        rid = r.get("id") if isinstance(r, dict) else None
        if rid in seen_ids:
            dup_ids.add(rid)
        seen_ids.add(rid)
    counted_quotes, counted_spans, counted_snaps = set(), set(), set()
    counted = failed = 0
    for r in rows:
        reason = "ok"
        rid = r.get("id") if isinstance(r, dict) else None
        try:
            if not isinstance(rid, str) or not re.fullmatch(r"HR[0-9]+", rid):
                reason = "R1-bad-id"
            elif rid in dup_ids:
                reason = "R1-duplicate-id"
            elif not isinstance(r.get("statement"), str) or len(r["statement"].split()) < 8:
                reason = "R2-statement"
            else:
                src, host = r.get("source") or {}, r.get("host") or {}
                lines, why = load("snapshot", src.get("snapshot"))
                if lines is None:
                    reason = "R3-" + why
                else:
                    q = src.get("quote")
                    if not isinstance(q, str) or not (6 <= len(q.split()) <= 25):
                        reason = "R4-quote-length"
                    else:
                        a, b = (src.get("lines") or [None, None])[:2] if isinstance(src.get("lines"), list) and len(src.get("lines")) == 2 else (None, None)
                        ok, why = exact_span(lines, a, b, q)
                        if not ok:
                            reason = "R4-" + why
                if reason == "ok":
                    hl, why = load("receipt", host.get("receipt"))
                    v = host.get("value")
                    if hl is None:
                        reason = "R5-" + why
                    elif not isinstance(v, str) or not v.strip():
                        reason = "R5-empty-value"
                    else:
                        c, d = host.get("lines") if isinstance(host.get("lines"), list) and len(host.get("lines")) == 2 else (None, None)
                        ok, why = exact_span(hl, c, d, v)
                        if not ok:
                            reason = "R5-" + why
                if reason == "ok":
                    nq = norm(src["quote"])
                    span = (src["snapshot"], src["lines"][0], src["lines"][1])
                    if nq in counted_quotes or span in counted_spans:
                        reason = "R6-duplicate-quote-or-span"
                    else:
                        counted_quotes.add(nq)
                        counted_spans.add(span)
                        counted_snaps.add(src["snapshot"])
        except Exception as e:  # noqa: BLE001 - a malformed row fails, it never crashes the count
            reason = f"row-malformed:{type(e).__name__}"
        if reason == "ok":
            counted += 1
        else:
            failed += 1
        results.append({"id": rid, "reason": reason})
    met = counted >= TARGET_ROWS and failed == 0 and len(counted_snaps) >= TARGET_SNAPSHOTS
    return {"verdict": "met" if met else "unmet", "counted": counted, "failed": failed,
            "distinct_snapshots": len(counted_snaps), "target_rows": TARGET_ROWS,
            "target_snapshots": TARGET_SNAPSHOTS, "rows": results}


def run_eval(reader, entry_path):
    try:
        res = evaluate(reader, entry_path)
        return (0 if res["verdict"] == "met" else 1), res
    except CannotEvaluate as e:
        return 2, {"verdict": "cannot-evaluate", "reason": str(e), "counted": 0}


# ---------------------------------------------------------------- selftest
def _copy_inputs(reader, root):
    """Materialise the frozen manifests and every file they list under root."""
    for mpath in MANIFEST_PINS:
        data = reader.get(mpath)
        if data is None:
            raise CannotEvaluate(f"selftest-input-absent:{mpath}")
        os.makedirs(os.path.join(root, os.path.dirname(mpath)), exist_ok=True)
        with open(os.path.join(root, mpath), "wb") as fh:
            fh.write(data)
        for path in parse_manifest(data, os.path.dirname(mpath)):
            b = reader.get(path)
            os.makedirs(os.path.join(root, os.path.dirname(path)), exist_ok=True)
            with open(os.path.join(root, path), "wb") as fh:
                fh.write(b if b is not None else b"")


def _random_entry(root, rng, nrows, nsnaps):
    src_m = parse_manifest(open(os.path.join(root, SRC_MANIFEST), "rb").read(), os.path.dirname(SRC_MANIFEST))
    host_m = parse_manifest(open(os.path.join(root, HOST_MANIFEST), "rb").read(), os.path.dirname(HOST_MANIFEST))
    snaps = {f"s{i}": {"url": "https://example.invalid/" + os.path.basename(p), "path": p, "sha256": h}
             for i, (p, h) in enumerate(sorted(src_m.items()))}
    recs = {f"h{i}": {"path": p, "sha256": h} for i, (p, h) in enumerate(sorted(host_m.items()))}
    keys = rng.sample(sorted(snaps), nsnaps)
    rows, used = [], set()
    tries = 0
    while len(rows) < nrows and tries < 10000:
        tries += 1
        k = keys[len(rows) % len(keys)]
        lines = open(os.path.join(root, snaps[k]["path"]), encoding="utf-8", errors="replace").read().split("\n")
        i = rng.randrange(len(lines))
        words = lines[i].split()
        if len(words) < 8:
            continue
        q = " ".join(words[:rng.randint(6, min(10, len(words)))])
        if norm(q) in used or (k, i) in used or norm(q) in norm(" ".join(lines[:i])) or norm(q) in norm(" ".join(lines[i + 1:])):
            continue
        hk = rng.choice(sorted(recs))
        hl = open(os.path.join(root, recs[hk]["path"]), encoding="utf-8", errors="replace").read().split("\n")
        cands = [(j, t) for j, l in enumerate(hl) for t in l.split() if len(t) >= 3]
        j, tok = rng.choice(cands)
        if norm(tok) in norm(" ".join(hl[:j])):
            continue  # need the first occurrence so [j+1, j+1] is minimal
        used.add(norm(q))
        used.add((k, i))
        rows.append({"id": f"HR{len(rows) + 1}", "statement": "positive control row built from a random snapshot span by the selftest",
                     "source": {"snapshot": k, "lines": [i + 1, i + 1], "quote": q},
                     "host": {"receipt": hk, "lines": [j + 1, j + 1], "value": tok}})
    return {"snapshots": snaps, "receipts": recs, "rows": rows}


def selftest(reader):
    rng = random.Random()  # unseeded: a control that memorises fixtures cannot follow
    cases = []
    tmp = tempfile.mkdtemp(prefix="r84-c1-")
    try:
        root = os.path.join(tmp, "lane")
        _copy_inputs(reader, root)
        ep = ENTRY

        def write(entry):
            os.makedirs(os.path.join(root, os.path.dirname(ep)), exist_ok=True)
            with open(os.path.join(root, ep), "w", encoding="utf-8") as fh:
                json.dump(entry, fh)

        def check(label, entry, want_rc, pred=lambda r: True):
            if entry is None:
                p = os.path.join(root, ep)
                if os.path.exists(p):
                    os.remove(p)
            else:
                write(entry)
            rc, res = run_eval(Reader(root=root), ep)
            ok = rc == want_rc and pred(res)
            cases.append({"case": label, "pass": ok, "rc": rc, "want_rc": want_rc,
                          "counted": res.get("counted"), "verdict": res.get("verdict")})

        base = _random_entry(root, rng, TARGET_ROWS, TARGET_SNAPSHOTS)
        check("P1-random-valid-rows-met", base, 0, lambda r: r["counted"] == TARGET_ROWS)
        check("D0-do-nothing-entry-absent", None, 2)
        e = json.loads(json.dumps(base)); e["rows"][0]["source"]["quote"] = "this sentence was never written in any pinned snapshot here"
        check("F1-fabricated-quote", e, 1, lambda r: r["rows"][0]["reason"] == "R4-not-in-span")
        # F2a doctored snapshot: inject the fabricated quote and declare the new digest
        e = json.loads(json.dumps(base)); k = e["rows"][0]["source"]["snapshot"]; p = os.path.join(root, e["snapshots"][k]["path"])
        orig = open(p, "rb").read()
        fake = b"this sentence was never written in any pinned snapshot here\n" + orig
        with open(p, "wb") as fh:
            fh.write(fake)
        e["snapshots"][k]["sha256"] = sha(fake)
        e["rows"][0]["source"].update({"lines": [1, 1], "quote": "this sentence was never written in any pinned snapshot here"})
        check("F2a-doctored-snapshot-declared-digest", e, 1, lambda r: r["rows"][0]["reason"].startswith("R3-"))
        # F2b doctor the manifest too: the manifest pin refuses before any row
        mp = os.path.join(root, SRC_MANIFEST); morig = open(mp, "rb").read()
        with open(mp, "wb") as fh:
            fh.write(morig.replace(sha(orig).encode(), sha(fake).encode()))
        check("F2b-doctored-snapshot-and-manifest", e, 2)
        with open(mp, "wb") as fh:
            fh.write(morig)
        with open(p, "wb") as fh:
            fh.write(orig)
        e = json.loads(json.dumps(base)); e["rows"] = [dict(e["rows"][0], id=f"HR{i + 1}") for i in range(TARGET_ROWS)]
        check("F3-one-row-duplicated", e, 1, lambda r: r["counted"] == 1)
        e = json.loads(json.dumps(base)); s = e["rows"][0]["source"]; a = s["lines"][0]
        s["lines"] = [a - 1, a] if a > 1 else [a, a + 1]
        check("F4-widened-span", e, 1, lambda r: r["rows"][0]["reason"] == "R4-span-not-minimal")
        e = json.loads(json.dumps(base)); e["rows"][0]["host"]["value"] = "zz-fabricated-host-value-zz"
        check("F5-fabricated-host-value", e, 1, lambda r: r["rows"][0]["reason"] == "R5-not-in-span")
        e = json.loads(json.dumps(base)); e["rows"] = e["rows"][:TARGET_ROWS - 1]
        check("F6-one-row-short", e, 1, lambda r: r["counted"] == TARGET_ROWS - 1 and r["failed"] == 0)
        e = _random_entry(root, rng, TARGET_ROWS, TARGET_SNAPSHOTS - 1)
        check("F7-too-few-snapshots", e, 1, lambda r: r["failed"] == 0 and r["distinct_snapshots"] == TARGET_SNAPSHOTS - 1)
        e = json.loads(json.dumps(base)); e["rows"][0]["host"]["receipt"] = "nope"
        check("F8-undeclared-receipt", e, 1, lambda r: r["rows"][0]["reason"] == "R5-receipt-undeclared")
        with open(os.path.join(root, ep), "w") as fh:
            fh.write("{not json")
        rc, res = run_eval(Reader(root=root), ep)
        cases.append({"case": "F9-unparseable-entry", "pass": rc == 2, "rc": rc, "want_rc": 2,
                      "counted": res.get("counted"), "verdict": res.get("verdict")})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    passed = sum(c["pass"] for c in cases)
    return {"selftest": f"PASS ({len(cases)} cases, {passed} passed, {len(cases) - passed} failed)"
            if passed == len(cases) else f"FAIL ({len(cases)} cases, {passed} passed, {len(cases) - passed} failed)",
            "cases": cases}, (0 if passed == len(cases) else 1)


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--revision")
    g.add_argument("--root")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--entry", default=ENTRY)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        reader = Reader(revision=a.revision, repo=a.repo) if a.revision else Reader(root=a.root or a.repo)
        try:
            res, rc = selftest(reader)
        except CannotEvaluate as e:
            res, rc = {"selftest": "CANNOT-EVALUATE", "reason": str(e)}, 2
        print(json.dumps(res, indent=1))
        return rc
    if not (a.revision or a.root):
        ap.error("one of --revision or --root is required")
    reader = Reader(revision=a.revision, repo=a.repo) if a.revision else Reader(root=a.root)
    rc, res = run_eval(reader, a.entry)
    print(json.dumps(res, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
