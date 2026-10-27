#!/usr/bin/env python3
"""C1-11 independent identity harness (seat C1ExecIndependent, round 46 w1).

Does NOT import or call the round-46 counter. It takes the census at the
declared implementation revision, derives 30 byte-level variants of it
(appended random comment bytes with and without a final newline, CRLF line
ends in an appended comment, a UTF-8 multibyte comment, an appended empty
line, a 1 MB appended comment block), runs `bash <file> --identity` for each,
and compares every field of the printed identity line against values computed
here from the variant file with sha256sum, md5sum, wc -c, wc -l, the file's
own rollup printf (plane list) and its VERSION/exit_map literals.

Usage: harness.py <base-census> <scratch-dir> <log-file>
"""

import os
import random
import re
import subprocess
import sys

BASE, SCRATCH, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
VDIR = os.path.join(SCRATCH, "v")
os.makedirs(VDIR, exist_ok=True)
RNG = random.Random(46)  # fixed seed: "random" bytes, reproducible run

PRINTABLE = tuple(chr(c) for c in range(0x20, 0x7F))


def rand(n):
    return "".join(RNG.choice(PRINTABLE) for _ in range(n))


UTF8 = ["caf\u00e9 \u2615 \u65e5\u672c\u8a9e",
        "\U0001f9ea scrub_speed_max \U0001f6e0",
        "\u00fcn\u00efc\u00f6d\u00e9" * 200,
        "\u4e2d\u6587" + rand(60) + "\u00e9\u00e8\u00ea"]


def block_1m(seed_text, final_newline=True):
    """Return exactly 1048576 bytes of '#' comment lines."""
    target = 1048576
    rng = random.Random(462)
    out = []
    size = 0
    while size < target:
        body = "".join(rng.choice(PRINTABLE) for _ in range(64))
        line = "# " + body + "\n"
        if size + len(line) > target:
            line = line[: target - size]
            if final_newline:
                line = line[:-1] + "\n"
            else:
                if line.endswith("\n"):
                    line = line[:-1] + rng.choice(PRINTABLE)
        out.append(line)
        size += len(line)
    data = "".join(out).encode()
    assert len(data) == target, len(data)
    return data


def variants():
    """(name, description, appended-bytes) in the 30-variant plan."""
    v = []
    # A: appended random comment, final newline (5)
    for i, n in enumerate([8, 40, 200, 1000, 4096], 1):
        v.append((f"A{i}", f"appended-random-comment-{n}B-final-newline",
                  ("\n# " + rand(n) + "\n").encode()))
    # B: appended random comment, NO final newline (5)
    for i, n in enumerate([8, 40, 200, 1000, 4096], 1):
        v.append((f"B{i}", f"appended-random-comment-{n}B-no-final-newline",
                  ("\n# " + rand(n)).encode()))
    # C: CRLF line ends in the appended comment (4). The appended region starts on a fresh
    # LF line so the CRLF belongs to the comment only; the base census ends without a final
    # newline, so a bare "\r\n" would splice CR onto the last argv word of `main "$@"`.
    v.append(("C1", "appended-CRLF-comment-final-CRLF",
              ("\n# " + rand(24) + "\r\n").encode()))
    v.append(("C2", "appended-CRLF-comment-no-final-EOL",
              ("\n# " + rand(24) + "\r\n# " + rand(12)).encode()))
    v.append(("C3", "appended-two-CRLF-comment-lines",
              ("\n# " + rand(16) + "\r\n# " + rand(16) + "\r\n").encode()))
    v.append(("C4", "appended-CRLF-comment-1KB",
              ("\n# " + rand(1024) + "\r\n").encode()))
    # D: UTF-8 multibyte comment (4)
    for i, txt in enumerate(UTF8, 1):
        v.append((f"D{i}", f"appended-utf8-multibyte-comment-{i}",
                  ("\n# " + txt + "\n").encode()))
    # E: appended empty / whitespace-only lines (3)
    v.append(("E1", "appended-one-empty-line", b"\n"))
    v.append(("E2", "appended-two-empty-lines", b"\n\n"))
    v.append(("E3", "appended-whitespace-only-line", b"\n   \n"))
    # F: 1 MB appended comment block (3)
    v.append(("F1", "appended-1MiB-comment-block-final-newline",
              b"\n" + block_1m("many", True)))
    v.append(("F2", "appended-1MiB-comment-block-no-final-newline",
              b"\n" + block_1m("many", False)))
    v.append(("F3", "appended-single-1MiB-comment-line",
              b"\n# " + rand(1048576 - 2).encode() + b"\n"))
    # G: combinations (6)
    v.append(("G1", "appended-comment-no-space-after-hash",
              ("\n#" + rand(20) + "\n").encode()))
    v.append(("G2", "appended-three-comment-lines-final-newline",
              ("\n# " + rand(10) + "\n# " + rand(10) + "\n# " + rand(10) + "\n").encode()))
    v.append(("G3", "appended-three-comment-lines-no-final-newline",
              ("\n# " + rand(10) + "\n# " + rand(10) + "\n# " + rand(10)).encode()))
    v.append(("G4", "appended-utf8-no-final-newline",
              ("\n# \u00fcn\u00efc\u00f6d\u00e9 " + rand(10)).encode()))
    v.append(("G5", "appended-utf8-CRLF-final-CRLF",
              ("\n# \u65e5\u672c\u8a9e " + rand(10) + "\r\n").encode()))
    v.append(("G6", "appended-empty-line-then-comment-no-final-newline",
              ("\n\n# " + rand(30)).encode()))
    assert len(v) == 30, len(v)
    return v


def tool_stdin(tool, path):
    with open(path, "rb") as f:
        r = subprocess.run([tool], stdin=f, capture_output=True)
    assert r.returncode == 0, (tool, r.stderr)
    return r.stdout.decode().split()[0]


def text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def expected(path):
    t = text(path)
    ver = re.search(r"^VERSION='([^']*)'", t, re.M).group(1)
    roll = re.search(r"^  printf 'TSUKUROI_CENSUS: %s \(.*$", t, re.M)
    planes = ""
    if roll:
        planes = ",".join(x[:-3] for x in re.findall(r"[a-z-]+=%s", roll.group(0)))
    return {
        "version": ver,
        "sha256": tool_stdin("sha256sum", path),
        "md5": tool_stdin("md5sum", path),
        "bytes": wc(path, "-c"),
        "lines": wc(path, "-l"),
        "planes": planes,
        "exit_map": "0:HEALTHY,1:DEGRADED,2:BLOCKED",
        "verified": "yes",
    }


def wc(path, flag):
    with open(path, "rb") as f:
        r = subprocess.run(["wc", flag], stdin=f, capture_output=True)
    assert r.returncode == 0, (flag, r.stderr)
    return r.stdout.decode().strip()


ID_RE = re.compile(
    r"^TSUKUROI_CENSUS_IDENTITY: version=(\S+) sha256=(\S+) md5=(\S+)"
    r" bytes=(\S+) lines=(\S+) planes=(\S+) exit_map=(\S+) verified=(\S+)$")
FIELDS = ("version", "sha256", "md5", "bytes", "lines", "planes", "exit_map", "verified")


def parse_identity(line):
    m = ID_RE.match(line)
    return dict(zip(FIELDS, m.groups())) if m else None


def run_identity(path, argpath):
    r = subprocess.run(["bash", argpath, "--identity"], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def main():
    base = open(BASE, "rb").read()
    base_sha = tool_stdin("sha256sum", BASE)
    assert base.endswith(b'main "$@"'), "base census shape unexpected"
    log = []
    log.append("harness: independent C1-11 identity check (does not import the round-46 counter)")
    log.append(f"bash: {subprocess.run(['bash','--version'],capture_output=True).stdout.decode().splitlines()[0]}")
    log.append(f"base census: {BASE}")
    log.append(f"base bytes={len(base)} sha256={base_sha} md5={tool_stdin('md5sum', BASE)}")
    log.append(f"base rollup planes={expected(BASE)['planes']}")
    log.append("")

    matched = 0
    mismatched = 0
    rel_matched = 0
    rel_mismatched = 0
    names = []
    for name, desc, app in variants():
        path = os.path.join(VDIR, f"{name}.sh")
        with open(path, "wb") as f:
            f.write(base + app)
        want = expected(path)
        rc, out, err = run_identity(path, path)
        lines = [l for l in out.splitlines() if l]
        got = parse_identity(lines[0]) if len(lines) == 1 else None
        diffs = []
        if rc != 0:
            diffs.append(f"exit {rc} wanted 0 (stderr: {err.strip()!r})")
        if len(lines) != 1:
            diffs.append(f"wanted exactly one line, got {len(lines)}: {out!r}")
        if got is None and len(lines) == 1:
            diffs.append("identity line did not parse")
        if got:
            for f in FIELDS:
                if got[f] != want[f]:
                    diffs.append(f"{f}: printed={got[f]!r} expected={want[f]!r}")
            if got["sha256"] == base_sha:
                diffs.append("sha256 equals the base census digest (constant writer)")
            if got["verified"] != "yes":
                diffs.append(f"verified={got['verified']!r} wanted yes")
        # relative-path invocation from the scratch dir: same file, same fields
        rel = subprocess.run(["bash", f"v/{name}.sh", "--identity"], capture_output=True, cwd=SCRATCH)
        rel_lines = [l for l in rel.stdout.decode("utf-8", "replace").splitlines() if l]
        rel_ok = (rel.returncode == 0 and len(rel_lines) == 1
                  and parse_identity(rel_lines[0]) == got)
        rel_matched += 1 if rel_ok else 0
        rel_mismatched += 0 if rel_ok else 1
        status = "MATCH" if not diffs else "MISMATCH"
        if diffs:
            mismatched += 1
        else:
            matched += 1
        names.append(name)
        log.append(f"{name} [{desc}] appended={len(app)}B file_bytes={want['bytes']} "
                   f"file_lines={want['lines']} -> {status}")
        log.append(f"  printed: {lines[0] if lines else ''}")
        log.append(f"  expected: version={want['version']} sha256={want['sha256']} "
                   f"md5={want['md5']} bytes={want['bytes']} lines={want['lines']} "
                   f"planes={want['planes']} exit_map={want['exit_map']} verified=yes")
        for d in diffs:
            log.append(f"  MISMATCH {d}")
        if not rel_ok:
            log.append(f"  RELATIVE-PATH MISMATCH rc={rel.returncode} out={rel.stdout!r} "
                       f"stderr={rel.stderr!r}")
        log.append(f"  relative-path run: {'MATCH' if rel_ok else 'MISMATCH'}")
    log.append("")
    log.append(f"SUMMARY absolute-path: {matched}/{matched + mismatched} matched, "
               f"{mismatched} mismatched")
    log.append(f"SUMMARY relative-path: {rel_matched}/{rel_matched + rel_mismatched} matched, "
               f"{rel_mismatched} mismatched")
    log.append(f"VARIANTS: {len(names)} ({','.join(names)}); distinct-from-base sha256: "
               f"{sum(1 for n in names if tool_stdin('sha256sum', os.path.join(VDIR, n + '.sh')) != base_sha)}/{len(names)}")
    text_out = "\n".join(log) + "\n"
    with open(LOG, "w") as f:
        f.write(text_out)
    print(text_out)


if __name__ == "__main__":
    main()
