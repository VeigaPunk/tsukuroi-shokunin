#!/usr/bin/env python3
"""R1Reviewer per-row evidence harness (round-74 w1).

Mirrors the frozen counter's mechanical rules (tools/count-uf-rows-r74.py) and adds
verbatim-quote line localization + token-sharing metrics. Read-only over the pinned
snapshots in .ufo/waves/round-74/before/src. No repo mutation.

NOTE: quote candidates may contain " * " markers — the counter normalizes whitespace
only, so multi-line block comments must be quoted WITH their continuation asterisks.
"""
import hashlib
import re
import sys
from pathlib import Path

SNAPDIR = Path(".ufo/waves/round-74/before/src")

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = set("""
that this with from into than then them they their there these those which while where when
have has had been being were was are its it's not but for and the a an of to in on at by as or
is are do does did can could would should may might must shall will one two three also such
more most less least other others same different only over under about across after before
each every both all any some no nor own same very just even still yet because since until
""".split())


def tokenize(text):
    return {w.lower() for w in WORD_RE.findall(text)} - STOP


def normalize_ws(s):
    return " ".join(s.split())


def load(name):
    raw = (SNAPDIR / name).read_bytes()
    text = raw.decode("utf-8", errors="replace")
    return raw, hashlib.sha256(raw).hexdigest(), normalize_ws(text), text.splitlines(), text


def locate(lines, quote):
    """Minimal (start,end) 1-based line window whose normalized join contains the quote."""
    q = normalize_ws(quote)
    best = None
    for i in range(len(lines)):
        acc = []
        for j in range(i, min(i + 14, len(lines))):
            acc.append(lines[j].strip())
            joined = " ".join(x for x in acc if x)
            if q in joined:
                span = (i + 1, j + 1)
                if best is None or (span[1] - span[0]) < (best[1] - best[0]):
                    best = span
                break
            if len(joined) > len(q) + 4000:
                break
    return best


def metrics(stmt, snap_text):
    st = tokenize(stmt)
    pt = tokenize(snap_text)
    shared = st & pt
    return len(st), sorted(st - pt), len(shared), (len(shared) / len(st) if st else 0.0)


def check_quote(snap, quote, label):
    raw, dig, norm, lines, _ = load(snap)
    loc = locate(lines, quote)
    present = normalize_ws(quote) in norm
    words = len(quote.split())
    pipe = "|" in quote
    ok = present and loc is not None and 4 <= words <= 25 and not pipe
    print(f"[{label}] snap={snap} present={present} lines={loc} words={words} pipe={pipe} -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_stmt(stmt, snap, label, min_words=12, min_tokens=6, min_share=0.5):
    _, _, _, _, text = load(snap)
    total, missing, n, ratio = metrics(stmt, text)
    ok = len(stmt.split()) >= min_words and n >= min_tokens and ratio >= min_share
    print(f"[{label}] snap={snap} stmt_words={len(stmt.split())} distinct_tokens={total} shared={n} ratio={ratio:.2f} -> {'PASS' if ok else 'FAIL'}")
    print(f"    missing_from_snapshot={missing}")
    return ok


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "receipts"

    for name in ("unit-file.c", "load-fragment.c", "unit-file.h"):
        raw, dig, _, _, _ = load(name)
        print(f"DIGEST {name} {dig} bytes={len(raw)}")

    if mode != "receipts":
        # mode == path to a note file: per-row mechanical review of actual UF rows
        note = Path(sys.argv[2])
        text = note.read_text(encoding="utf-8", errors="replace")
        ROW_RE = re.compile(
            r'^\| UF(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
            r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
            r'\| quote="(?P<quote>[^"]*)" \|$')
        for line_no, line in enumerate(text.splitlines(), 1):
            if not re.match(r'^\s*\|\s*UF[0-9]+\s*\|', line):
                continue
            m = ROW_RE.match(line)
            if not m:
                print(f"line {line_no}: MALFORMED ROW SHAPE: {line[:120]}...")
                continue
            g = m.groupdict()
            raw, dig, _, _, stext = load(g["snap"])
            import json
            smap = json.loads((SNAPDIR / "SOURCES.json").read_text())
            digest_ok = smap.get(g["snap"], {}).get("sha256") == g["digest"] and dig == g["digest"]
            print(f"--- UF{g['n']} (line {line_no}) src={g['src']} snap={g['snap']} digest_ok={digest_ok}")
            check_stmt(g["stmt"], g["snap"], f"UF{g['n']}-stmt")
            check_quote(g["snap"], g["quote"], f"UF{g['n']}-quote")
        sys.exit(0)

    # ---------- UF1: priority order + first-seen registration (unit-file.c) ----------
    check_quote("unit-file.c", "Search paths are ordered by priority (highest first), and we need to maintain this order.", "UF1-q1")
    check_quote("unit-file.c", "to something (incl. itself), it means that we have already seen it, and we should * ignore it here.", "UF1-q2")
    check_quote("unit-file.c", "if (hashmap_contains(ids, de->d_name)) continue;", "UF1-q3")

    # ---------- UF2: self-alias rejection + target name-type validation (unit-file.c) ----------
    check_quote("unit-file.c", "-ELOOP for an alias to self.", "UF2-q1")
    check_quote("unit-file.c", "-EXDEV if the target filename is not a valid unit name or doesn't match the source,", "UF2-q2")
    check_quote("unit-file.c", "if (streq(src, dst)) return log_debug_errno(SYNTHETIC_ERRNO(ELOOP),", "UF2-q3")
    check_quote("unit-file.c", '%s: symlink target name type \\"%s\\" does not match source, rejecting.', "UF2-q4")
    check_quote("unit-file.c", '%s: unit symlink target \\"%s\\" instance name doesn\'t match, rejecting.', "UF2-q5")
    check_quote("unit-file.c", '%s: symlink target \\"%s\\" has incompatible suffix, rejecting.', "UF2-q6")

    # ---------- UF3: unit_type_may_alias list (unit-file.h) ----------
    check_quote("unit-file.h", "static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);", "UF3-q1")

    # ---------- UF4: UnitFileState runtime variants (unit-file.h) ----------
    check_quote("unit-file.h", "UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME,", "UF4-q1")

    # ---------- UF5: null_or_empty mask, perpetual immune, zero mtime (load-fragment.c) ----------
    check_quote("load-fragment.c", "if (null_or_empty(&st)) { /* Unit file is masked */", "UF5-q1")
    check_quote("load-fragment.c", "u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */", "UF5-q2")
    check_quote("load-fragment.c", "u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;", "UF5-q3")

    # ---------- UF6: system-scope builtin fallback, on-disk overrides (load-fragment.c) ----------
    check_quote("load-fragment.c", "} else if (u->manager->runtime_scope == RUNTIME_SCOPE_SYSTEM) {", "UF6-q1")
    check_quote("load-fragment.c", "No fragment found on disk. For system units, fall back to a built-in copy if we have one * embedded.", "UF6-q2")
    check_quote("load-fragment.c", "On-disk files always take precedence (including masks), since we only get * here when nothing was found in the lookup paths.", "UF6-q3")
    check_quote("load-fragment.c", "const char *data = builtin_unit_lookup(u->id);", "UF6-q4")

    # ---------- clause canaries: committed C1 wording vs intended snapshot ----------
    clauses = [
        ("UF1", "unit-file.c", "unit search paths are processed in priority order with first-seen name registration ignoring lower duplicate filenames"),
        ("UF2", "unit-file.c", "unit symlinks reject self-aliases, require compatible instance/template types, and restrict aliasing to alias-capable unit types"),
        ("UF3", "unit-file.h", "unit_type_may_alias permits aliasing strictly for service, socket, target, device, and volume units"),
        ("UF4", "unit-file.h", "UnitFileState distinguishes enabled, linked, and masked states from their runtime variants"),
        ("UF5", "load-fragment.c", "a fragment matching null_or_empty sets UNIT_MASKED and zero mtime except for perpetual units which are immune from masking"),
        ("UF6", "load-fragment.c", "missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins"),
    ]
    for label, snap, stmt in clauses:
        check_stmt(stmt, snap, f"CANARY-{label}")

    # ---------- recommended entailed statements (author fix-up suggestions) ----------
    recs = [
        ("UF1", "unit-file.c", "Unit search paths are walked in priority order and a name already registered is skipped, so the first-seen copy wins"),
        ("UF2", "unit-file.c", "unit_validate_alias_symlink_or_warn returns ELOOP for a unit self-alias and EXDEV when the symlink target name type does not match source"),
        ("UF3", "unit-file.h", "unit_type_may_alias admits only UNIT_SERVICE UNIT_SOCKET UNIT_TARGET UNIT_DEVICE UNIT_TIMER UNIT_PATH so volume units can never carry aliases"),
        ("UF4", "unit-file.h", "UnitFileState separates UNIT_FILE_ENABLED from UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED from UNIT_FILE_LINKED_RUNTIME, and UNIT_FILE_MASKED from UNIT_FILE_MASKED_RUNTIME"),
        ("UF5", "load-fragment.c", "a null_or_empty fragment sets load_state to UNIT_MASKED and zero fragment_mtime except that perpetual units load as UNIT_LOADED instead"),
        ("UF6", "load-fragment.c", "missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins"),
    ]
    for label, snap, stmt in recs:
        check_stmt(stmt, snap, f"REC-{label}")
