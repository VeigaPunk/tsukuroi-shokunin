#!/usr/bin/env python3
"""E1Counter round-74: build independent mirror + isolation fixtures + scripted non-reader.

Rows here are written independently by this seat from the pinned v262 snapshots;
no row is copied from the tool's synthetic self-test rows.
Every quote is asserted verbatim (whitespace-normalized) in its snapshot.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
SRC = LANE / ".ufo/waves/round-74/before/src"
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("/fast/scratch/hyaku/tsukuroi-r74/E1Counter/fixtures").resolve()

SNAPDIR = ".ufo/waves/round-74/before/src"
NOTE = "corpus/knowledge/systemd-unit-fragment-plane-r74.md"
REGISTRY = "corpus/SOURCES.md"
MAP = SNAPDIR + "/SOURCES.json"

NAMES = ("unit-file.c", "load-fragment.c", "unit-file.h")
DIG = {n: hashlib.sha256((SRC / n).read_bytes()).hexdigest() for n in NAMES}
MAP_DATA = json.loads((SRC / "SOURCES.json").read_text(encoding="utf-8"))

REG = {
    "S309": ("unit-file.c", "code",
             "unit-file.c lines 58-125 symlink alias validation and lines 364-573 search path lookup"),
    "S310": ("load-fragment.c", "code",
             "load-fragment.c lines 6245-6253 null_or_empty mask and lines 6285-6310 builtin_unit_lookup fallback"),
    "S311": ("unit-file.h", "code",
             "unit-file.h lines 7-23 UnitFileState enum and lines 25-33 unit_type_may_alias predicate"),
}

# (id, snapshot, source, statement, quote)
ROWS = [
    ("UF1", "unit-file.c", "S309",
     "Unit search paths are processed in strict priority order where highest priority directories are evaluated first and duplicate unit filenames in lower directories are ignored",
     "Search paths are ordered by priority (highest first), and we need to maintain this order."),
    ("UF2", "unit-file.c", "S309",
     "Unit symlink aliases validate target names and reject self aliases returning ELOOP while mismatched target name types return EXDEV",
     "if (streq(src, dst)) return log_debug_errno(SYNTHETIC_ERRNO(ELOOP),"),
    ("UF3", "unit-file.h", "S311",
     "Static inline bool unit_type_may_alias for unittype type evaluates in_set with unit_service unit_socket unit_target unit_device unit_timer unit_path",
     "static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH); }"),
    ("UF4", "unit-file.h", "S311",
     "Typedef enum unitfilestate defines unit_file_enabled unit_file_enabled_runtime unit_file_linked unit_file_linked_runtime unit_file_masked unit_file_masked_runtime unit_file_static and unit_file_disabled",
     "UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME, UNIT_FILE_STATIC,"),
    ("UF5", "load-fragment.c", "S310",
     "When fragment inspection matches null_or_empty the unit load_state becomes unit_masked unless perpetual unit property keeps unit_loaded",
     "u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */"),
    ("UF6", "load-fragment.c", "S310",
     "Missing fragments for system units fall back to builtin_unit_lookup while on-disk unit files and masks unconditionally override built-ins",
     "const char *data = builtin_unit_lookup(u->id); if (data) {"),
]

ROW_RE = re.compile(
    r'^\| UF(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')


def norm(s):
    return " ".join(s.split())


def read_snap(name):
    return (SRC / name).read_text(encoding="utf-8", errors="replace")


def row_line(rid, snap, src, stmt, quote, digest=None):
    assert "|" not in stmt and "|" not in quote and '"' not in quote, rid
    return (f'| {rid} | {stmt} | source={src} | snapshot={snap} | '
            f'digest={digest or DIG[snap]} | quote="{quote}" |')


def note_text(rows):
    return "# round-74 C1 note (E1Counter independent mirror)\n\n" + "\n".join(rows) + "\n"


def registry_text(kinds=None, url_overrides=None, anchor_overrides=None, dupe_sid=None):
    kinds = kinds or {}
    url_overrides = url_overrides or {}
    anchor_overrides = anchor_overrides or {}
    out = [
        "# SOURCES — fixture mirror (E1Counter)",
        "",
        "| ID | Title | Kind | Tier | Scope | Location | Summary | Status | Date | Recheck | Used-by | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, (name, kind, anchor) in REG.items():
        url = url_overrides.get(sid, MAP_DATA[name]["url"])
        anch = anchor_overrides.get(sid, anchor)
        k = kinds.get(sid, kind)
        out.append(f"| {sid} | mirror {name} — {url} | {k} | A | "
                   f"fixture mirror of {name} | {anch} | mirror entry | mined "
                   f"| 2026-11-04 | on-release | {NOTE} | |")
    if dupe_sid:
        out.append(out[-1].replace("S311", dupe_sid))
    return "\n".join(out) + "\n"


def map_text(mut=None):
    snaps = dict(MAP_DATA)
    if mut:
        mut(snaps)
    return json.dumps(snaps, indent=2) + "\n"


def write_tree(root, rows, kinds=None, map_mut=None, files=None, registry=None):
    root = Path(root)
    src = root / SNAPDIR
    src.mkdir(parents=True, exist_ok=True)
    for n in NAMES:
        (src / n).write_bytes((SRC / n).read_bytes() if not files or n not in files
                              else files[n])
    (src / "SOURCES.json").write_text(map_text(map_mut) if not isinstance(map_mut, str) else map_mut)
    (root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    (root / NOTE).write_text(note_text(rows))
    (root / REGISTRY).parent.mkdir(parents=True, exist_ok=True)
    (root / REGISTRY).write_text(registry if registry is not None else registry_text(kinds))


def verify_rows(rows):
    for line in rows:
        m = ROW_RE.match(line)
        assert m, f"row does not parse: {line[:60]}"
        snap = m.group("snap")
        assert norm(m.group("quote")) in norm(read_snap(snap)), f"quote not verbatim in {snap}: {m.group('quote')}"
        qwords = len(m.group("quote").split())
        assert 4 <= qwords <= 25, f"quote words out of bounds: {qwords}"
        assert m.group("digest") == DIG[snap]


def base_rows():
    rows = [row_line(*r) for r in ROWS]
    verify_rows(rows)
    return rows


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    rows = base_rows()
    base = OUT / "mirror"
    write_tree(base, rows)
    made = ["mirror"]

    def var(name, mutate):
        d = OUT / name
        shutil.copytree(base, d)
        mutate(d)
        made.append(name)

    # 1. iso-id-gap: non-contiguous ID (UF6 renamed UF7)
    def iso_id_gap(d):
        p = d / NOTE
        p.write_text(p.read_text().replace("| UF6 |", "| UF7 |", 1))

    # 2. iso-id-dupe: duplicate ID (UF2 renamed UF1)
    def iso_id_dupe(d):
        p = d / NOTE
        p.write_text(p.read_text().replace("| UF2 |", "| UF1 |", 1))

    # 3. iso-words-short: statement words < 12 (8 words)
    def iso_words_short(d):
        p = d / NOTE
        new = row_line("UF1", "unit-file.c", "S309",
                       "Unit search paths are processed in strict order",
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 4. iso-ground-zero: completely ungrounded tokens (0 shared)
    def iso_ground_zero(d):
        p = d / NOTE
        new = row_line("UF1", "unit-file.c", "S309",
                       "Zebra quokka wombat xylophone nostril platypus marmalade truffle blizzard kumquat yonder zeppelin flagon",
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 5. iso-ground-low: shared ratio < 0.5 (6 shared out of 14 total tokens = 0.43)
    def iso_ground_low(d):
        p = d / NOTE
        # Shared tokens: unit, search, paths, processed, strict, priority (6 tokens)
        # Extra non-shared tokens: zebra, quokka, wombat, xylophone, nostril, platypus, marmalade, truffle (8 tokens)
        new = row_line("UF1", "unit-file.c", "S309",
                       "Unit search paths are processed in strict priority while zebra quokka wombat xylophone nostril platypus marmalade truffle graze peacefully",
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 6. iso-src-unreg: unregistered source S999
    def iso_src_unreg(d):
        p = d / NOTE
        p.write_text(p.read_text().replace("source=S309", "source=S999", 1))

    # 7. iso-src-ownwork: registry row has kind own-work
    def iso_src_ownwork(d):
        (d / REGISTRY).write_text(registry_text(kinds={"S309": "own-work"}))

    # 8. iso-src-badkind: registry row has invalid kind
    def iso_src_badkind(d):
        (d / REGISTRY).write_text(registry_text(kinds={"S309": "fabricated"}))

    # 9. iso-reg-dupid: duplicate registry S-ID
    def iso_reg_dupid(d):
        (d / REGISTRY).write_text(registry_text(dupe_sid="S309"))

    # 10. iso-snap-corrupt: snapshot bytes altered
    def iso_snap_corrupt(d):
        p = d / SNAPDIR / "unit-file.c"
        p.write_bytes(p.read_bytes() + b"\n")

    # 11. iso-digest-swap: row's digest != SOURCES.json digest
    def iso_digest_swap(d):
        p = d / NOTE
        p.write_text(p.read_text().replace(DIG["unit-file.c"], "0" * 64, 1))

    # 12. iso-map-corrupt: SOURCES.json digest changed
    def iso_map_corrupt(d):
        p = d / MAP
        data = json.loads(p.read_text())
        data["unit-file.c"]["sha256"] = "0" * 64
        p.write_text(json.dumps(data, indent=2) + "\n")

    # 13. iso-map-url: registry does not cite map URL
    def iso_map_url(d):
        (d / REGISTRY).write_text(registry_text(url_overrides={"S309": "https://example.org/uncited"}))

    # 14. iso-anchor-missing: registry anchor does not mention snapshot basename
    def iso_anchor_missing(d):
        (d / REGISTRY).write_text(registry_text(anchor_overrides={"S309": "unanchored description"}))

    # 15. iso-quote-absent: quote modified and not located in snapshot text
    def iso_quote_absent(d):
        p = d / NOTE
        new = row_line("UF1", "unit-file.c", "S309", ROWS[0][3],
                       "Search paths are ordered by random permutation and chaos.")
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 16. iso-quote-long: quote > 25 words (26 words)
    def iso_quote_long(d):
        p = d / NOTE
        long_q = " ".join(["word"] * 26)
        # Just put a 26 word quote
        new = f'| UF1 | {ROWS[0][3]} | source=S309 | snapshot=unit-file.c | digest={DIG["unit-file.c"]} | quote="{long_q}" |'
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 17. iso-quote-short: quote < 4 words (3 words) — addresses r74 MIN_QUOTE_WORDS fix
    def iso_quote_short(d):
        p = d / NOTE
        short_q = "Search paths are"
        new = f'| UF1 | {ROWS[0][3]} | source=S309 | snapshot=unit-file.c | digest={DIG["unit-file.c"]} | quote="{short_q}" |'
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 18. iso-quote-pipe: quote contains pipe character |
    def iso_quote_pipe(d):
        p = d / NOTE
        pipe_q = "Search paths are | ordered by priority"
        new = f'| UF1 | {ROWS[0][3]} | source=S309 | snapshot=unit-file.c | digest={DIG["unit-file.c"]} | quote="{pipe_q}" |'
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 19. iso-malformed-row: row does not match regex
    def iso_malformed_row(d):
        p = d / NOTE
        p.write_text(p.read_text().replace(rows[0], "| UF1 | malformed row without proper fields |", 1))

    # 20. iso-reuse-3: snapshot cited 3 times (> MAX_SNAPSHOT_REUSE 2)
    def iso_reuse_3(d):
        p = d / NOTE
        # Change UF3 (which cites unit-file.h) to cite unit-file.c
        new_uf3 = row_line("UF3", "unit-file.c", "S309",
                           ROWS[0][3] + " secondary variant with sufficient words and ground",
                           ROWS[0][4])
        p.write_text(p.read_text().replace(rows[2], new_uf3, 1))

    # 21. iso-nonmap-mapfile: SOURCES.json is a JSON list not a dict
    def iso_nonmap_mapfile(d):
        p = d / MAP
        p.write_text('["not", "a", "dict"]\n')

    # 22. iso-empty-quote: quote="" (empty quote defect test)
    def iso_empty_quote(d):
        p = d / NOTE
        new = f'| UF1 | {ROWS[0][3]} | source=S309 | snapshot=unit-file.c | digest={DIG["unit-file.c"]} | quote="" |'
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # --- blind spots (expected rc 0 / met=1) -------------------------------
    # 23. blind-negate: statement negated with "never", tokens preserved
    def blind_negate(d):
        p = d / NOTE
        neg_stmt = "Unit search paths are never processed in strict priority order where highest priority directories are evaluated first and duplicate unit filenames in lower directories are ignored"
        new = row_line("UF1", "unit-file.c", "S309", neg_stmt, ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 24. blind-unanchored-quote: quote from license header, statement technical
    def blind_unanchored_quote(d):
        p = d / NOTE
        lic_q = "/* SPDX-License-Identifier: LGPL-2.1-or-later */"
        new = row_line("UF1", "unit-file.c", "S309", ROWS[0][3], lic_q)
        p.write_text(p.read_text().replace(rows[0], new, 1))

    # 25. blind-dupecontent: UF2 duplicates UF1 statement and quote identically
    def blind_dupecontent(d):
        p = d / NOTE
        new_uf2 = row_line("UF2", "unit-file.c", "S309", ROWS[0][3], ROWS[0][4])
        p.write_text(p.read_text().replace(rows[1], new_uf2, 1))

    var("iso-id-gap", iso_id_gap)
    var("iso-id-dupe", iso_id_dupe)
    var("iso-words-short", iso_words_short)
    var("iso-ground-zero", iso_ground_zero)
    var("iso-ground-low", iso_ground_low)
    var("iso-src-unreg", iso_src_unreg)
    var("iso-src-ownwork", iso_src_ownwork)
    var("iso-src-badkind", iso_src_badkind)
    var("iso-reg-dupid", iso_reg_dupid)
    var("iso-snap-corrupt", iso_snap_corrupt)
    var("iso-digest-swap", iso_digest_swap)
    var("iso-map-corrupt", iso_map_corrupt)
    var("iso-map-url", iso_map_url)
    var("iso-anchor-missing", iso_anchor_missing)
    var("iso-quote-absent", iso_quote_absent)
    var("iso-quote-long", iso_quote_long)
    var("iso-quote-short", iso_quote_short)
    var("iso-quote-pipe", iso_quote_pipe)
    var("iso-malformed-row", iso_malformed_row)
    var("iso-reuse-3", iso_reuse_3)
    var("iso-nonmap-mapfile", iso_nonmap_mapfile)
    var("iso-empty-quote", iso_empty_quote)
    var("blind-negate", blind_negate)
    var("blind-unanchored-quote", blind_unanchored_quote)
    var("blind-dupecontent", blind_dupecontent)

    # --- scripted non-reader control --------------------------------------
    scripted = OUT / "scripted"
    write_tree(scripted, base_rows())
    srows, picks = [], []
    per = [
        ("unit-file.c", "S309", 0),
        ("unit-file.c", "S309", 1),
        ("load-fragment.c", "S310", 0),
        ("load-fragment.c", "S310", 1),
        ("unit-file.h", "S311", 0),
        ("unit-file.h", "S311", 1),
    ]
    STOP = set("""
    that this with from into than then them they their there these those which while where when
    have has had been being were was are its it's not but for and the a an of to in on at by as or
    is are do does did can could would should may might must shall will one two three also such
    more most less least other others same different only over under about across after before
    each every both all any some no nor own same very just even still yet because since until
    """.split())

    for i, (snap, src, which) in enumerate(per, start=1):
        text = read_snap(snap)
        candidates = []
        for line in text.splitlines():
            n = norm(line)
            if 4 <= len(n.split()) <= 24 and "|" not in n and '"' not in n and not n.startswith("|"):
                candidates.append(n)
        quote = candidates[which]
        toks, seen = [], set()
        for tok in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text):
            t = tok.lower()
            if len(t) >= 4 and t not in STOP and t not in seen:
                seen.add(t)
                toks.append(t)
        block = toks[which * 16:(which + 1) * 16]
        stmt = " ".join(block)
        srows.append(row_line(f"UF{i}", snap, src, stmt, quote))
        picks.append((f"UF{i}", snap, which, quote[:50], len(stmt.split())))
    verify_rows(srows)
    (scripted / NOTE).write_text(note_text(srows))
    made.append("scripted")

    return made, picks, rows, srows


if __name__ == "__main__":
    made, picks, mrows, srows = build()
    print("built:", " ".join(made))
    print(f"total fixtures: {len(made)}")
