#!/usr/bin/env python3
"""Round-19 adjacency pointer extraction (L1, read-only git object reads only).

Reads immutable git objects of the fleet's sibling lane repos at their observed branch tips and of
this lane at its observed tip. Writes, under this directory:
  adjacency-pointers-r19.json  inbound (sibling -> tsukuroi path:line) and outbound
                               (tsukuroi PROVINCE.md -> sibling path:line) pointer census
  siblings/<lane>/<commit12>/<path>  byte copies of every outbound-cited sibling file at its tip
No host probe, no network, no write outside this directory, no git mutation.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

FLEET = Path("/home/vgpnk/Projects/shokunin")
LANE = FLEET / "tsukuroi-shokunin"
OUT = Path(__file__).resolve().parent
POINTER = re.compile(r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9_./~-]*/)?tsukuroi-shokunin/([A-Za-z0-9_./-]+?):([0-9][0-9,\-–]*[0-9]|[0-9])")
OUTBOUND = re.compile(r"\.\./([a-z0-9-]+)-shokunin/([A-Za-z0-9_./-]+?):([0-9][0-9,\-]*[0-9]|[0-9])")


def git(repo, *args):
    p = subprocess.run(["git", "--no-pager", "-C", str(repo), *args], capture_output=True)
    if p.returncode:
        raise SystemExit(f"git {args} in {repo} failed: {p.stderr.decode()[:200]}")
    return p.stdout


def branch_of(repo):
    for b in ("master", "main"):
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "-q", f"refs/heads/{b}"],
                          capture_output=True).returncode == 0:
            return b
    return None


def ranges(spec):
    out = []
    for part in spec.split(","):
        part = part.replace("\u2013", "-")  # en-dash ranges (r19 census v2, InClass068 caveat)
        if "-" in part:
            a, b = part.split("-", 1)
            out.append([int(a), int(b)])
        else:
            out.append([int(part), int(part)])
    return out


def main():
    # `--pin <census.json>` re-extracts at the lane/sibling tips recorded in an earlier census
    # (siblings commit concurrently; a re-run at moving tips would renumber inbound ids).
    pin = None
    if len(sys.argv) == 3 and sys.argv[1] == "--pin":
        pin = json.loads(Path(sys.argv[2]).read_text())
    lane_branch = "master"
    lane_tip = pin["lane_tip"] if pin else git(LANE, "rev-parse", f"refs/heads/{lane_branch}").decode().strip()
    inbound, siblings = [], {}
    for repo in sorted(FLEET.glob("*-shokunin")):
        name = repo.name[: -len("-shokunin")]
        if name == "tsukuroi" or not (repo / ".git").exists():
            continue
        br = branch_of(repo)
        if br is None:
            continue
        if pin is not None and name not in pin["siblings"]:
            continue
        tip = pin["siblings"][name]["tip"] if pin else git(repo, "rev-parse", f"refs/heads/{br}").decode().strip()
        siblings[name] = {"branch": br, "tip": tip}
        grep = subprocess.run(["git", "--no-pager", "-C", str(repo), "grep", "-I", "-n", "-E",
                               r"tsukuroi-shokunin/[A-Za-z0-9_./-]+:[0-9]", tip, "--"],
                              capture_output=True)
        for raw in grep.stdout.decode("utf-8", "replace").splitlines():
            _, path, line, text = raw.split(":", 3)
            for m in POINTER.finditer(text):
                inbound.append({"sibling": name, "sibling_branch": br, "sibling_commit": tip,
                                "sibling_path": path, "sibling_line": int(line),
                                "pointer": m.group(0), "target_path": m.group(1),
                                "target_ranges": ranges(m.group(2)),
                                "sibling_line_text": text.strip()[:600]})
    for i, rec in enumerate(inbound, 1):
        rec["id"] = f"IN-{i:03d}"
        try:
            body = git(LANE, "show", f"{lane_tip}:{rec['target_path']}").decode("utf-8", "replace").splitlines()
            rec["target_exists_at_lane_tip"] = True
            rec["target_line_count"] = len(body)
            rec["target_text_at_lane_tip"] = {f"{a}-{b}": "\n".join(body[a - 1:b])[:1500]
                                             for a, b in rec["target_ranges"]}
        except SystemExit:
            rec["target_exists_at_lane_tip"] = False
    outbound = []
    prov = git(LANE, "show", f"{lane_tip}:PROVINCE.md").decode().splitlines()
    for n, text in enumerate(prov, 1):
        for m in OUTBOUND.finditer(text):
            sib, path, spec = m.group(1), m.group(2), m.group(3)
            info = siblings.get(sib, {})
            rec = {"id": f"OUT-{len(outbound) + 1:03d}", "province_line": n, "pointer": m.group(0),
                   "sibling": sib, "sibling_path": path, "ranges": ranges(spec),
                   "sibling_branch": info.get("branch"), "sibling_commit": info.get("tip")}
            if info:
                blob = git(FLEET / f"{sib}-shokunin", "show", f"{info['tip']}:{path}")
                dest = OUT / "siblings" / sib / info["tip"][:12] / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(blob)
                rec["sibling_blob_sha256"] = hashlib.sha256(blob).hexdigest()
                rec["snapshot"] = str(dest.relative_to(LANE))
                lines = blob.decode("utf-8", "replace").splitlines()
                rec["sibling_line_count"] = len(lines)
                rec["cited_text_at_tip"] = {f"{a}-{b}": "\n".join(lines[a - 1:b])[:2000]
                                            for a, b in rec["ranges"]}
            outbound.append(rec)
    doc = {"schema": "tsukuroi-adjacency-pointers-r19-v1", "lane_branch": lane_branch,
           "lane_tip": lane_tip, "siblings": siblings,
           "counts": {"inbound": len(inbound), "outbound": len(outbound)},
           "inbound": inbound, "outbound": outbound}
    (OUT / "adjacency-pointers-r19.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(doc["counts"]), json.dumps(siblings))


if __name__ == "__main__":
    sys.exit(main())
