#!/usr/bin/env python3
"""Independent re-implementation of the frozen round-84 C1 row predicate (R1-R6).

Written from the *predicate text* in the docstring of
tools/count-resume-rows-r84.py, not from its code.  It scores every row of
corpus/knowledge/hibernate-resume-plane-r84.json against the frozen manifests
and reports, per row: my reason, the cited raw lines, local minimality,
global minimality, and (with --counter) agreement with the frozen counter.

Readings of ambiguous predicate wording (disclosed so a reviewer can differ):
  * "whitespace-normalised" = `" ".join(text.split())`; word counts are
    `len(norm(text).split())`.
  * "the EXACT minimal raw-line span ... (a<=b; dropping line a or line b
    loses the quote)" is read literally: containment in the join of lines
    a..b, and removing either end line loses the quote.  A single-line span
    is therefore trivially minimal.  A stricter GLOBAL reading (no shorter
    span anywhere in the file contains the quote) is also computed and
    reported as `global_minimal`, but does not drive the verdict.
  * "path is listed in the frozen source manifest" means the path must be a
    key of .ufo/waves/round-84/before/src/SHA256SUMS; the host manifest does
    not satisfy R3 (and vice versa for R5).

Usage:
  check.py --repo LANE [--entry PATH] [--revision REV] [--counter TOOL]
  exit 0 met / 1 unmet / 2 cannot-evaluate (same convention as the counter).
"""
import argparse
import bisect
import hashlib
import json
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/hibernate-resume-plane-r84.json"
SRC_MANIFEST = ".ufo/waves/round-84/before/src/SHA256SUMS"
HOST_MANIFEST = ".ufo/waves/round-84/before/host/SHA256SUMS"
SRC_PIN = "5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef"
HOST_PIN = "4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6"
TARGET_ROWS = 7
TARGET_SNAPSHOTS = 4
GIT_ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "HOME": "/nonexistent"}


class CannotEvaluate(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    return " ".join(s.split())


class Reader:
    def __init__(self, repo, revision=None):
        self.repo = repo
        self.revision = revision

    def get(self, path):
        if self.revision:
            p = subprocess.run(["git", "-C", self.repo, "show", f"{self.revision}:{path}"],
                               capture_output=True, env=GIT_ENV, timeout=120)
            return p.stdout if p.returncode == 0 else None
        try:
            with open(os.path.join(self.repo, path), "rb") as fh:
                return fh.read()
        except OSError:
            return None


def parse_manifest(data, base):
    """standard sha256sum lines: '<64 hex>  <name>' -> {base/name: hex}."""
    out = {}
    for line in data.decode("utf-8", "replace").splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+(\S.*)$", line)
        if m:
            name = m.group(2).lstrip("*")
            out[f"{base}/{name}"] = m.group(1)
    return out


def build_index(lines):
    """Normalised whole-file text plus a char-offset -> line map."""
    toks, starts, parts = [], [], []
    pos = 0
    for ln, text in enumerate(lines, 1):
        for t in text.split():
            toks.append((ln, t))
            starts.append(pos)
            parts.append(t)
            pos += len(t) + 1
    return {"text": " ".join(parts), "toks": toks, "starts": starts}


def occurrences(ix, needle):
    out, p = [], ix["text"].find(needle)
    while p >= 0:
        out.append(p)
        p = ix["text"].find(needle, p + 1)
    return out


def occ_lines(ix, p, n):
    i = bisect.bisect_right(ix["starts"], p) - 1
    j = bisect.bisect_right(ix["starts"], p + n - 1) - 1
    return ix["toks"][i][0], ix["toks"][j][0]


def best_span(ix, needle):
    best = None
    for p in occurrences(ix, needle):
        lo, hi = occ_lines(ix, p, len(needle))
        if best is None or (hi - lo) < (best[1] - best[0]):
            best = (lo, hi)
    return best


def span_check(lines, ix, a, b, needle):
    """Literal reading of R4/R5 span rule; also returns the global-minimum span."""
    if not (isinstance(a, int) and isinstance(b, int)) or isinstance(a, bool) or isinstance(b, bool):
        return {"ok": False, "why": "lines-not-int"}
    if not (1 <= a <= b <= len(lines)):
        return {"ok": False, "why": "lines-out-of-range"}
    n = norm(needle)
    if not n:
        return {"ok": False, "why": "empty-needle"}
    if n not in norm(" ".join(lines[a - 1:b])):
        return {"ok": False, "why": "not-in-span"}
    if a < b:
        drop_first = norm(" ".join(lines[a:b]))       # 1-based a+1 .. b
        drop_last = norm(" ".join(lines[a - 1:b - 1]))  # 1-based a .. b-1
        if n in drop_first or n in drop_last:
            return {"ok": False, "why": "span-not-minimal-local"}
    best = best_span(ix, n)
    global_minimal = None if best is None else (best[1] - best[0]) == (b - a)
    return {"ok": True, "why": "ok", "best_span": None if best is None else list(best),
            "global_minimal": global_minimal}


def evaluate(reader, entry_path=ENTRY):
    manifests, pins = {}, {}
    for mpath, pin in ((SRC_MANIFEST, SRC_PIN), (HOST_MANIFEST, HOST_PIN)):
        data = reader.get(mpath)
        if data is None:
            raise CannotEvaluate(f"manifest-absent:{mpath}")
        pins[mpath] = {"expected": pin, "observed": sha(data)}
        if sha(data) != pin:
            raise CannotEvaluate(f"manifest-pin-mismatch:{mpath}")
    src_manifest = parse_manifest(reader.get(SRC_MANIFEST), os.path.dirname(SRC_MANIFEST))
    host_manifest = parse_manifest(reader.get(HOST_MANIFEST), os.path.dirname(HOST_MANIFEST))
    manifests["source"] = src_manifest
    manifests["host"] = host_manifest

    raw = reader.get(entry_path)
    if raw is None:
        raise CannotEvaluate(f"entry-absent:{entry_path}")
    try:
        entry = json.loads(raw.decode("utf-8"))
        rows = entry["rows"]
        snaps = entry["snapshots"]
        receipts = entry["receipts"]
        assert isinstance(rows, list) and isinstance(snaps, dict) and isinstance(receipts, dict)
    except Exception as e:  # noqa: BLE001
        raise CannotEvaluate(f"entry-unparseable:{type(e).__name__}")

    cache = {}

    def load(kind, key, manifest_kind, evidence_name):
        table = snaps if kind == "snapshot" else receipts
        d = table.get(key) if isinstance(key, str) else None
        if not isinstance(d, dict) or not isinstance(d.get("path"), str):
            return None, f"{evi_prefix(kind)}-undeclared", None
        path, declared = d["path"], d.get("sha256")
        man = manifests[manifest_kind]
        if path not in man:
            return None, f"{evi_prefix(kind)}-not-in-{manifest_kind}-manifest", None
        if declared != man[path]:
            return None, f"{evi_prefix(kind)}-declared-sha-differs-from-{manifest_kind}-manifest", None
        if path not in cache:
            cache[path] = reader.get(path)
        data = cache[path]
        if data is None:
            return None, f"{evi_prefix(kind)}-absent", None
        if sha(data) != man[path]:
            return None, f"{evi_prefix(kind)}-bytes-differ-from-{manifest_kind}-manifest", None
        text = data.decode("utf-8", "replace")
        lines = text.split("\n")
        return lines, "ok", {"path": path, "declared_sha": declared, "manifest_sha": man[path],
                             "bytes_sha": sha(data), "url": d.get("url")}

    seen_ids = {}
    for r in rows:
        rid = r.get("id") if isinstance(r, dict) else None
        seen_ids[rid] = seen_ids.get(rid, 0) + 1

    counted_quotes, counted_spans, counted_snaps, counted_snap_paths = set(), set(), set(), set()
    results = []
    counted = failed = 0
    for r in rows:
        res = {"id": r.get("id") if isinstance(r, dict) else None}
        reason = "ok"
        try:
            rid = res["id"]
            if not isinstance(rid, str) or not re.fullmatch(r"HR[0-9]+", rid):
                reason = "R1-bad-id"
            elif seen_ids.get(rid, 0) > 1:
                reason = "R1-duplicate-id"
            elif not isinstance(r.get("statement"), str) or len(r["statement"].split()) < 8:
                reason = "R2-statement"
            else:
                res["statement_words"] = len(r["statement"].split())
                src = r.get("source") if isinstance(r.get("source"), dict) else {}
                host = r.get("host") if isinstance(r.get("host"), dict) else {}
                slines, why, sev = load("snapshot", src.get("snapshot"), "source", "snapshot")
                if slines is None:
                    reason = "R3-" + why
                else:
                    res["snapshot"] = src.get("snapshot")
                    res["snapshot_evidence"] = sev
                    q = src.get("quote")
                    if not isinstance(q, str) or not (6 <= len(norm(q).split()) <= 25):
                        reason = "R4-quote-length"
                    else:
                        res["quote_words"] = len(norm(q).split())
                        slines2 = src.get("lines")
                        if isinstance(slines2, list) and len(slines2) == 2:
                            a, b = slines2
                        else:
                            a = b = None
                        sc = span_check(slines, build_index(slines), a, b, q)
                        res["source_span"] = {"lines": [a, b], **sc,
                                              "text": slines[a - 1:b] if isinstance(a, int) and isinstance(b, int)
                                              and 1 <= a <= b <= len(slines) else None}
                        if not sc["ok"]:
                            reason = "R4-" + sc["why"]
                if reason == "ok":
                    hlines, why, hev = load("receipt", host.get("receipt"), "host", "receipt")
                    v = host.get("value")
                    if hlines is None:
                        reason = "R5-" + why
                    elif not isinstance(v, str) or not v.strip():
                        reason = "R5-empty-value"
                    else:
                        res["receipt"] = host.get("receipt")
                        res["receipt_evidence"] = hev
                        hlines2 = host.get("lines")
                        if isinstance(hlines2, list) and len(hlines2) == 2:
                            c, d = hlines2
                        else:
                            c = d = None
                        hc = span_check(hlines, build_index(hlines), c, d, v)
                        res["host_span"] = {"lines": [c, d], **hc,
                                            "text": hlines[c - 1:d] if isinstance(c, int) and isinstance(d, int)
                                            and 1 <= c <= d <= len(hlines) else None}
                        if not hc["ok"]:
                            reason = "R5-" + hc["why"]
                if reason == "ok":
                    nq = norm(src["quote"])
                    span = (src["snapshot"], src["lines"][0], src["lines"][1])
                    if nq in counted_quotes or span in counted_spans:
                        reason = "R6-duplicate-quote-or-span"
                    else:
                        counted_quotes.add(nq)
                        counted_spans.add(span)
                        counted_snaps.add(src["snapshot"])
                        counted_snap_paths.add(snaps[src["snapshot"]]["path"])
        except Exception as e:  # noqa: BLE001
            reason = f"row-malformed:{type(e).__name__}"
        res["reason"] = reason
        res["ok"] = reason == "ok"
        counted += res["ok"]
        failed += (not res["ok"])
        results.append(res)

    met = counted >= TARGET_ROWS and failed == 0 and len(counted_snaps) >= TARGET_SNAPSHOTS
    return {"verdict": "met" if met else "unmet", "counted": counted, "failed": failed,
            "distinct_snapshots": len(counted_snaps), "target_rows": TARGET_ROWS,
            "target_snapshots": TARGET_SNAPSHOTS,
            "distinct_snapshot_paths": len(counted_snap_paths),
            "manifest_pins": pins, "rows": results}


def evi_prefix(kind):
    return "snapshot" if kind == "snapshot" else "receipt"


def run_counter(counter, repo, revision, entry):
    cmd = [sys.executable, counter]
    if revision:
        cmd += ["--revision", revision, "--repo", repo]
    else:
        cmd += ["--root", repo]
    cmd += ["--entry", entry]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=repo, timeout=180)
    try:
        return p.returncode, json.loads(p.stdout)
    except json.JSONDecodeError:
        return p.returncode, {"verdict": "unparseable", "stdout": p.stdout, "stderr": p.stderr}


def compare(res, counter_res):
    by_id = {r["id"]: r for r in counter_res.get("rows", [])}
    out = []
    for r in res["rows"]:
        c = by_id.get(r["id"])
        c_reason = c.get("reason") if c else None
        out.append({"id": r["id"], "mine": r["reason"], "frozen": c_reason,
                    "agree_status": (r["ok"] == (c_reason == "ok")) if c else None,
                    "agree_reason": r["reason"] == c_reason})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--revision")
    ap.add_argument("--entry", default=ENTRY)
    ap.add_argument("--counter")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    reader = Reader(a.repo, a.revision)
    try:
        res = evaluate(reader, a.entry)
        rc = 0 if res["verdict"] == "met" else 1
    except CannotEvaluate as e:
        res = {"verdict": "cannot-evaluate", "reason": str(e), "counted": 0}
        rc = 2
    if a.counter:
        crc, cres = run_counter(a.counter, a.repo, a.revision, a.entry)
        res["frozen_counter"] = {"rc": crc, "verdict": cres.get("verdict"),
                                 "counted": cres.get("counted"), "failed": cres.get("failed")}
        if "rows" in res and "rows" in cres:
            res["agreement"] = compare(res, cres)
    text = json.dumps(res, indent=1)
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return rc


if __name__ == "__main__":
    sys.exit(main())
