#!/usr/bin/env python3
"""K-1 downstream patch-offset check (tsukuroi lane, round 42).

Read-only. For every upstream file:line pin the lane's newest knowledge entries
cite, resolve the package the host actually runs (`pacman -Qi`, read-only),
fetch the Arch packaging build at that installed tag, replay every packaging
patch against the pinned upstream blob, and report whether a packaging patch
touches the cited file and where the cited line lands in the built tree.

Nothing outside the cache dir is written; no package, service, mount or lane
file is touched. Network reads only (GitLab API/raw + upstream raw blobs).

Usage:
  patch-offset.py [--lane DIR] [--cache DIR] [--json OUT] [--no-apply]

Columns: pkg | upstream pin | cited file:line | arch tag | patches touching it
         | line-shift risk

Method
  1. `pacman -Qi <pkg>` gives the installed version = the Arch packaging tag.
  2. The PKGBUILD at that tag gives `source=()`: upstream ref plus the patch
     list, applied in array order (pacman PKGBUILD:90-102). A source name
     starting with `revertme-` is applied as `patch -RNp1` (PKGBUILD:97-99).
  3. Each cited file is copied from the pinned upstream ref into the cache and
     the packaging patches that name it are applied there. The cited line is
     then located by its own text (unique line match) in the patched copy:
     "shift +N -> :M" is observed, not modelled.
  4. When the anchor text is empty, duplicated or removed, a hunk model is
     used instead: hunks replayed line by line with the offsets `patch` reports
     folded in, so a line inside a hunk still maps exactly, a line after it
     moves by the net delta, and a line the patch deletes is named as such.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
GITLAB = "https://gitlab.archlinux.org"
TIMEOUT = 40

PKGS = {
    "pacman": {
        "packaging": "archlinux/packaging/packages/pacman",
        "raw": "https://gitlab.archlinux.org/pacman/pacman/-/raw/{ref}/{path}",
        "refsource": "_git_patch_level_commit",
        "notes": [
            "corpus/knowledge/pacman-hook-order-r38.md",
            "corpus/knowledge/pacman-transaction-order-r39.md",
            "corpus/knowledge/pacman-exec-environment-r40.md",
            "corpus/knowledge/alpm-package-anatomy-r41.md",
        ],
        "candidates": ["lib/libalpm/{f}", "src/pacman/{f}", "doc/{f}",
                       "scripts/{f}", "test/pacman/{f}", "{f}"],
        "pin": "pacman {ref}",
    },
    "btrfs-progs": {
        "packaging": "archlinux/packaging/packages/btrfs-progs",
        "raw": "https://git.kernel.org/pub/scm/linux/kernel/git/kdave/"
               "btrfs-progs.git/plain/{path}?h={ref}",
        "refsource": "tag",
        "notes": ["corpus/knowledge/btrfs-scrub-record-r42.md"],
        "candidates": ["cmds/{f}", "{f}", "common/{f}", "kernel-shared/{f}"],
        "pin": "btrfs-progs {ref}",
    },
    "systemd": {
        "packaging": "archlinux/packaging/packages/systemd",
        "raw": "https://raw.githubusercontent.com/systemd/systemd/{ref}/{path}",
        "refsource": "tag",
        "refs": ["v262.1", "v262"],
        "notes": ["corpus/knowledge/journalctl-v262-field-filter-r36.md"],
        "candidates": ["src/journal/{f}", "man/{f}", "src/shared/{f}",
                       "src/basic/{f}", "src/libsystemd/{f}", "{f}"],
        "pin": "systemd {ref}",
        # not cited by an r38-r42 entry; kept because the lane does cite v262 pins
        "context_only": True,
    },
}

PIN_RE = re.compile(
    r"(?<![\w/.-])(?P<path>(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.+-]+\.(?:c|h|in|"
    r"asciidoc|xml|raw|txt)):(?P<a>\d+)(?:-(?P<b>\d+))?"
)
BARE_RE = re.compile(r"(?<![\w/.-])(?P<path>CHANGES):(?P<a>\d+)(?:-(?P<b>\d+))?")


# ---------------------------------------------------------------- fetching
def fetch(url, cache):
    key = re.sub(r"[^A-Za-z0-9_.-]+", "_", url)[-180:]
    path = os.path.join(cache, key)
    if os.path.exists(path):
        with open(path, "rb") as fh:
            return fh.read()
    req = urllib.request.Request(url, headers={"User-Agent": "tsukuroi-patch-offset/1"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as exc:
            if exc.code in (400, 404):
                return None
            if exc.code < 500 or attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))
    tmp = path + ".part"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    return data


def text(url, cache):
    data = fetch(url, cache)
    return None if data is None else data.decode("utf-8", "replace")


# ---------------------------------------------------------------- pkgbuild
def parse_pkgbuild(src):
    out = {"source": []}
    for m in re.finditer(r"^(_?[A-Za-z0-9_]+)=(\S+)$", src, re.M):
        if m.group(1).endswith("sums") or m.group(1) in (
                "source", "validpgpkeys", "backup", "options"):
            continue
        out[m.group(1)] = m.group(2).strip("'\"")
    start = src.find("source=(")
    if start >= 0:
        i, depth = start + len("source="), 0
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        block = src[start + len("source=("):i]
        for line in block.splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            for tok in re.findall(r"'([^']*)'|\"([^\"]*)\"|([^\s)]+)", line):
                val = "".join(tok).strip()
                if val:
                    out["source"].append(val)
    return out


def patch_entries(pkgb):
    """-> [(applied_name, url_or_None, reversed)] in application order."""
    res = []
    for entry in pkgb["source"]:
        if not entry.endswith(".patch"):
            continue
        name, url = entry.split("::", 1) if "::" in entry else (entry, None)
        base = os.path.basename(name)
        res.append((base, url, base.startswith("revertme-")))
    return res


# ---------------------------------------------------------------- patches
def parse_patch(body, reverse):
    """-> {path: [dict(a,b,c,d,body=[sign+text])]} in pinned-tree coordinates."""
    files, cur, hunk = {}, None, None
    for raw in body.splitlines():
        m = re.match(r"^\+\+\+ b/(.+)$", raw)
        if m:
            cur = m.group(1).strip()
            files.setdefault(cur, [])
            hunk = None
            continue
        if raw.startswith("--- ") or raw.startswith("diff --git"):
            hunk = None
            continue
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", raw)
        if m and cur:
            hunk = {"a": int(m.group(1)), "b": int(m.group(2) or 1),
                    "c": int(m.group(3)), "d": int(m.group(4) or 1),
                    "body": []}
            files[cur].append(hunk)
            continue
        if hunk is not None and raw[:1] in (" ", "+", "-"):
            hunk["body"].append(raw)
    if reverse:
        for hunks in files.values():
            for h in hunks:
                h["a"], h["b"], h["c"], h["d"] = h["c"], h["d"], h["a"], h["b"]
                h["body"] = [{"+": "-", "-": "+"}.get(ln[0], ln[0]) + ln[1:]
                             for ln in h["body"]]
    return files


def apply_offsets(hunks, offsets):
    """Fold the offsets `patch` reported into the hunk ranges."""
    for h, off in zip(sorted(hunks, key=lambda x: x["a"]), offsets):
        h["a"] += off
        h["c"] += off
    return hunks


def map_line(hunks, line):
    """-> (state, built_line) from the hunk model. same|moved|removed|unknown."""
    shift = 0
    for h in sorted(hunks, key=lambda x: x["a"]):
        a, b, c, d = h["a"], h["b"], h["c"], h["d"]
        if line > a + b - 1:
            shift += d - b
            continue
        if line < a:
            break
        old, new = a, c
        for body_line in h["body"]:
            sign = body_line[0]
            if sign == " ":
                if old == line:
                    return ("moved" if new != line else "same"), new
                old += 1
                new += 1
            elif sign == "-":
                if old == line:
                    return "removed", None
                old += 1
            elif sign == "+":
                new += 1
        return "unknown", None
    return ("moved" if shift else "same"), line + shift


# ---------------------------------------------------------------- apply
def prepare_tree(pkg, path, blob, patches, cache):
    """Copy the pinned blob into the cache and apply the packaging patches.

    -> (built_text_or_None, offsets_by_patch_name, log_lines)
    """
    root = os.path.join(cache, "apply", pkg, re.sub(r"\W+", "_", path))
    shutil.rmtree(root, ignore_errors=True)
    dest = os.path.join(root, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(blob)
    offsets, log = {}, []
    for idx, (name, body, rev) in enumerate(patches):
        pfile = os.path.join(root, f"{idx}.patch")
        with open(pfile, "w", encoding="utf-8") as fh:
            fh.write(body)
        cmd = ["patch", "--batch", "-Np1", "-i", pfile]
        if rev:
            cmd.insert(2, "-R")
        res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        out = (res.stdout or "") + (res.stderr or "")
        got, cur_file, saw, failed = [], None, False, False
        for ln in out.splitlines():
            m = re.match(r"^patching file (.+)$", ln)
            if m:
                cur_file = m.group(1)
                saw = saw or cur_file == path
                continue
            m = re.match(r"^Hunk #\d+ succeeded at \d+ \(offset (-?\d+) lines?\)", ln)
            if m and cur_file == path:
                got.append(int(m.group(1)))
            elif re.match(r"^Hunk #\d+ FAILED", ln) and cur_file == path:
                failed = True
        if got:
            offsets[name] = got
        if failed:
            log.append(f"{name}: HUNK FAILED")
        elif not saw:
            log.append(f"{name}: file not in patch")
        elif got:
            log.append(f"{name}: applied, patch reported offsets {got}")
        else:
            log.append(f"{name}: applied clean")
    try:
        with open(dest, encoding="utf-8", errors="replace") as fh:
            return fh.read(), offsets, log
    except OSError:
        return None, offsets, log


def anchor_map(pinned_text, built_text, line):
    """Locate the pinned line's own text in the built file. -> built line|None."""
    if pinned_text is None or built_text is None:
        return None
    src = pinned_text.splitlines()
    if not (1 <= line <= len(src)):
        return None
    anchor = src[line - 1].strip()
    if len(anchor) < 8:  # short lines ('}', '', '}' of a block) are not anchors
        return None
    if sum(1 for l in src if l.strip() == anchor) != 1:
        return None
    hits = [i + 1 for i, l in enumerate(built_text.splitlines())
            if l.strip() == anchor]
    return hits[0] if len(hits) == 1 else None


# ---------------------------------------------------------------- lane
def collect_pins(lane, cfg):
    pins = []
    for rel in cfg["notes"]:
        path = os.path.join(lane, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        seen = set()
        for rx in (PIN_RE, BARE_RE):
            for m in rx.finditer(body):
                cited = m.group("path")
                base = os.path.basename(cited)
                if base.endswith(".raw"):
                    continue  # alpm-docs rendering, not a file of a host package
                key = (base, int(m.group("a")))
                if key in seen:
                    continue
                seen.add(key)
                pins.append({"note": rel, "cited": cited, "base": base,
                             "line": int(m.group("a")),
                             "line_end": int(m.group("b") or m.group("a")),
                             "has_dir": "/" in cited})
    return pins


def resolve_path(pin, patched_paths, cfg, ref, cache):
    if pin["has_dir"]:
        return pin["cited"]
    for path in patched_paths:
        if os.path.basename(path) == pin["base"]:
            return path
    for tmpl in cfg["candidates"]:
        cand = tmpl.format(f=pin["base"])
        if text(cfg["raw"].format(ref=ref, path=cand), cache) is not None:
            return cand
    return None


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE_DEFAULT)
    ap.add_argument("--cache", default=os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "tsukuroi-patch-offset"))
    ap.add_argument("--json")
    ap.add_argument("--no-apply", action="store_true",
                    help="skip applying patches; use the hunk model only")
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)

    rows, notes, ok = [], [], True
    for pkg, cfg in PKGS.items():
        try:
            qi = subprocess.run(["pacman", "-Qi", pkg], capture_output=True,
                                text=True, check=True).stdout
        except subprocess.CalledProcessError:
            notes.append(f"{pkg}: not installed on this host - skipped")
            continue
        tag = re.search(r"^Version\s*:\s*(\S+)", qi, re.M).group(1)
        pkgb_src = text(f"{GITLAB}/{cfg['packaging']}/-/raw/{tag}/PKGBUILD",
                        args.cache)
        if pkgb_src is None:
            notes.append(f"{pkg}: no packaging tag {tag} at GitLab")
            ok = False
            continue
        pkgb = parse_pkgbuild(pkgb_src)
        if cfg["refsource"] == "tag":
            refs = cfg.get("refs") or [f"v{pkgb.get('pkgver', tag.split('-')[0])}"]
        else:
            refs = [pkgb.get(cfg["refsource"]) or pkgb.get("_git_tag")]
        ref = refs[0]
        pin = cfg["pin"].format(ref=ref)

        api = urllib.parse.quote(cfg["packaging"], safe="")
        tree = text(f"{GITLAB}/api/v4/projects/{api}/repository/tree"
                    f"?ref={tag}&per_page=100", args.cache)
        tree_paths = {e["path"] for e in json.loads(tree)} if tree else set()

        bodies, per_file, order = {}, {}, []
        for name, url, rev in patch_entries(pkgb):
            body = text(url, args.cache) if url else text(
                f"{GITLAB}/{cfg['packaging']}/-/raw/{tag}/{name}", args.cache)
            if body is None:
                notes.append(f"{pkg}: patch {name} not fetchable at {tag}")
                ok = False
                continue
            bodies[name] = (body, rev)
            order.append(name)
            for path, hunks in parse_patch(body, rev).items():
                per_file.setdefault(path, []).append((name, hunks))
        if cfg.get("context_only"):
            notes.append(f"{pkg}: pins read from {', '.join(cfg['notes'])} "
                         f"(outside the r38-r42 entry window; kept because the "
                         f"lane cites v262 line pins)")
        for name, url, rev in patch_entries(pkgb):
            if not url and name not in tree_paths:
                notes.append(f"{pkg}: {name} named in source=() but absent at {tag}")

        pins = collect_pins(args.lane, cfg)
        built = {}
        for p in pins:
            path = resolve_path(p, per_file.keys(), cfg, ref, args.cache)
            if path is None and p["base"].endswith(".txt"):
                continue  # host-capture / packaging-file names, not upstream pins
            if path is None:
                rows.append({"pkg": pkg, "pin": pin, "cited": p["cited"],
                             "tag": tag, "patch": "?", "risk": "unresolved path"})
                continue
            hunks_all = [h for _, hl in per_file.get(path, []) for h in hl]
            names = sorted({n for n, _ in per_file.get(path, [])})
            shift, land, method = None, None, "-"
            if hunks_all and not args.no_apply:
                if path not in built:
                    blob = text(cfg["raw"].format(ref=ref, path=path), args.cache)
                    patches = [(n, bodies[n][0], bodies[n][1])
                               for n in order if n in names]
                    btext, offs, log = prepare_tree(pkg, path, blob or "",
                                                    patches, args.cache)
                    for n in offs:
                        for pname, hl in per_file.get(path, []):
                            if pname == n:
                                apply_offsets(hl, offs[n])
                    built[path] = (blob, btext, log)
                blob, btext, _ = built[path]
                land = anchor_map(blob, btext, p["line"]) if blob else None
                if land is not None:
                    shift, method = land - p["line"], "anchor"
            if hunks_all and method == "-":
                method = "model"
                state, land = map_line(hunks_all, p["line"])
                if state == "removed":
                    shift, land = "removed", None
                elif state == "unknown":
                    shift, land = "unknown", None
                else:
                    shift = land - p["line"]
            risk = "none"
            if shift == "removed":
                risk = "line removed by packaging"
            elif shift == "unknown":
                risk = "in-hunk (not mapped)"
            elif shift:
                risk = f"shift {shift:+d} -> :{land}"
            cited = path if not p["has_dir"] else p["cited"]
            rows.append({"pkg": pkg, "pin": pin,
                         "cited": f"{cited}:{p['line']}"
                         + (f"-{p['line_end']}" if p["line_end"] != p["line"] else ""),
                         "tag": tag, "patch": ",".join(names) or "-",
                         "risk": risk, "method": method})
            p["resolved"] = path
        notes.append(
            f"{pkg}: tag {tag}  pin {ref}  patches {len(order)}"
            f" [{', '.join(n + (' REVERSED' if bodies[n][1] else '') for n in order) or 'none'}]"
            f"  patched files: {', '.join(sorted(per_file)) or 'none'}")
        for path, (blob, btext, log) in sorted(built.items()):
            notes.append(f"{pkg}: {path}: " + "; ".join(log or ["no patches applied"]))
            if blob is None:
                notes.append(f"{pkg}: {path}: pinned blob unavailable")

    keys = ("pkg", "pin", "cited", "tag", "patch", "risk")
    widths = [max([len(r[k]) for r in rows] + [len(k)]) for k in keys]
    hdr = ("pkg", "upstream pin", "cited file:line", "arch tag",
           "patches touching it", "line-shift risk")
    print(" | ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(" | ".join([r["pkg"].ljust(widths[0]), r["pin"].ljust(widths[1]),
                          r["cited"].ljust(widths[2]), r["tag"].ljust(widths[3]),
                          r["patch"].ljust(widths[4]), r["risk"]]))
    print()
    drift = [r for r in rows if r["risk"] != "none"]
    by_method = {}
    for r in rows:
        by_method[r.get("method", "-")] = by_method.get(r.get("method", "-"), 0) + 1
    print(f"SUMMARY rows={len(rows)} risk_rows={len(drift)} "
          f"files_with_packaging_hunks="
          f"{len({r['cited'].split(':')[0] for r in drift})}")
    print("METHOD " + ", ".join(f"{k}={v}" for k, v in sorted(by_method.items())))
    for n in notes:
        print("NOTE " + n)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"rows": rows, "notes": notes}, fh, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
