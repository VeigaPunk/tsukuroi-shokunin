#!/usr/bin/env python3
"""Generate one-clause forgers of base.py (r89 docstring R1-R8) + a combined diff.

Each forger is base.py with exactly one textual substitution (old -> new),
asserted to occur exactly once. Writes fx_<name>.py and forgers.diff.
"""
import difflib
import os
import stat
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.py")

F = []


def sub(name, clause, old, new):
    F.append((name, clause, old, new))


sub("f01_cr_kept", "R1 remove EVERY CR anywhere in the file",
    'text = raw.decode("utf-8", "surrogateescape").replace("\\r", "")',
    'text = raw.decode("utf-8", "surrogateescape").replace("\\r", "\\r")')

sub("f02_lead_tab_kept", "R1 leading spaces/tabs stripped (blanks = space and tab)",
    'def key_line(line):\n    """R1: line -> (key, value) or None."""\n    s = line.lstrip(" \\t")',
    'def key_line(line):\n    """R1: line -> (key, value) or None."""\n    s = line.lstrip(" ")')

sub("f03_trail_tab_kept", "R1 value trailing spaces/tabs stripped",
    '    value = s[j + 1:].lstrip(" \\t").rstrip(" \\t")',
    '    value = s[j + 1:].lstrip(" \\t").rstrip(" ")')

sub("f04_digits_in_key", "R1 key = letters/underscores then ':'",
    'KEYCHARS = set(string.ascii_letters + "_")',
    'KEYCHARS = set(string.ascii_letters + "_" + string.digits)')

sub("f05_equals_sep", "R1 key followed directly by ':' (not '=')",
    '    if j == 0 or j >= len(s) or s[j] != ":":',
    '    if j == 0 or j >= len(s) or s[j] not in ":=":')

sub("f06_comment_hash_stripped", "R1 a line whose first non-blank char is '#' is not a key line",
    '    if not s or s[0] == "#":\n        return None\n    j = 0',
    '    if not s:\n        return None\n    if s.startswith("#"):\n        s = s.lstrip("#").lstrip(" \\t")\n    j = 0')

sub("f07_drop_term_font", "R2 path-valued key list (..., wallpaper, term_font)",
    '    "global_dtb", "wallpaper", "term_font",',
    '    "global_dtb", "wallpaper",')

sub("f08_hash_first_hash", "R2 the hash is the text after the LAST '#'",
    '    h = value.rfind("#")',
    '    h = value.find("#")')

sub("f09_empty_path_not_pin", "R2 the path ... may be empty (an empty path is still a pin)",
    '    if h < j + 3:\n        return None\n    return value[:i]',
    '    if h < j + 3:\n        return None\n    if h == j + 3:\n        return None\n    return value[:i]')

sub("f10_len_ge_128", "R3 hash must be exactly 128 characters",
    'return len(h) == 128 and all(c in HEXCHARS for c in h)',
    'return len(h) >= 128 and all(c in HEXCHARS for c in h)')

sub("f11_upper_hex_rejected", "R3 128 characters of [0-9a-fA-F]",
    'HEXCHARS = set("0123456789abcdefABCDEF")',
    'HEXCHARS = set("0123456789abcdef")')

sub("f12_resource_case_insensitive", "R4 the resource name is compared case-sensitively",
    '    if res != "boot" or root != "":',
    '    if res.lower() != "boot" or root != "":')

sub("f13_all_dollars_dropped", "R4 ONE leading '$' (gzip marker) is dropped",
    '    res = resource[1:] if resource.startswith("$") else resource',
    '    res = resource.lstrip("$")')

sub("f14_root_ignored", "R4 only `boot` with an empty root resolves",
    '    if res != "boot" or root != "":',
    '    if res != "boot":')

sub("f15_dir_mismatch", "R5 a path naming a directory -> LP-MISSING",
    '    if not os.path.isfile(full):\n        return "LP-MISSING"',
    '    if not os.path.exists(full):\n        return "LP-MISSING"\n    if os.path.isdir(full):\n        return "LP-MISMATCH"')

sub("f16_gzip_decompressed", "R5 gzip files are NOT decompressed",
    '        with open(full, "rb") as f:\n            data = f.read()',
    '        with open(full, "rb") as f:\n            data = f.read()\n        if data[:2] == b"\\x1f\\x8b":\n            import gzip\n            data = gzip.decompress(data)')

sub("f17_hash_case_sensitive_cmp", "R5 compared with the hash case-insensitively",
    '    if digest.lower() == h.lower():',
    '    if digest.lower() == h:')

sub("f18_optional_key_case_sensitive", "R6 optional keys matched case-insensitively like every key",
    '                    elif klow in ("wallpaper", "term_font"):',
    '                    elif key in ("wallpaper", "term_font"):')

sub("f19_secure_boot_ignored", "R6 LP-MISMATCH -> panic when --secure-boot-enforced 1",
    '    enforced = sbe == "1"',
    '    enforced = False')

sub("f20_last_hmp_line", "R6/R8 the FIRST `hash_mismatch_panic` key line",
    '            if klow == "hash_mismatch_panic" and first_hmp is None:',
    '            if klow == "hash_mismatch_panic":')

sub("f21_no_value_case_insensitive", "R6 value equal to `no` case-insensitively",
    '                    elif first_hmp is not None and first_hmp[1].lower() == "no":',
    '                    elif first_hmp is not None and first_hmp[1] == "no":')

sub("f22_unresolved_before_degraded", "R7 precedence: DEGRADED then CANNOT-EVALUATE",
    '    if any(s in ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT") for s in statuses):\n        verdict, rc = "DEGRADED", 1\n    elif any(s == "LP-UNRESOLVED" for s in statuses):\n        verdict, rc = "CANNOT-EVALUATE", 2',
    '    if any(s == "LP-UNRESOLVED" for s in statuses):\n        verdict, rc = "CANNOT-EVALUATE", 2\n    elif any(s in ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT") for s in statuses):\n        verdict, rc = "DEGRADED", 1')

sub("f23_unreadable_conf_degraded", "R7 unreadable --conf -> CANNOT-EVALUATE rc 2, empty pin list",
    '    except OSError:\n        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [],\n                          "hash_mismatch_panic": None}))\n        return 2',
    '    except OSError:\n        print(json.dumps({"verdict": "DEGRADED", "rc": 1, "pins": [],\n                          "hash_mismatch_panic": None}))\n        return 1')

sub("f24_no_plus_removal", "R8 label without a leading '+'",
    '    s = s.lstrip("/")\n    if s.startswith("+"):\n        s = s[1:]',
    '    s = s.lstrip("/")')

sub("f25_trailing_plus_dropped", "R8 a trailing '+' stays",
    '    return s.strip(" \\t")',
    '    label = s.strip(" \\t")\n    if label.endswith("+"):\n        label = label[:-1]\n    return label')

sub("f26_entry_untrimmed", "R8 label trimmed of spaces/tabs at both ends",
    '    return s.strip(" \\t")',
    '    return s')

sub("f27_path_key_case_sensitive", "R2 path-valued keys matched case-insensitively",
    '            klow = key.lower()',
    '            klow = key')

sub("f28_optional_hashformat_panic", "R6 for LP-MISMATCH and LP-HASH-FORMAT: optional -> skip",
    '                    elif klow in ("wallpaper", "term_font"):\n                        cons = "skip"\n                    elif status == "LP-HASH-FORMAT":',
    '                    elif status == "LP-HASH-FORMAT":')

sub("f29_empty_pin_list_cannot", "R7 HEALTHY rc 0 also when the file holds no pin at all",
    '    statuses = [p["status"] for p in pins]',
    '    statuses = [p["status"] for p in pins]\n    if not statuses:\n        statuses = ["LP-UNRESOLVED"]')


sub("f30_vtab_ff_leading", "R1 a line that starts with any other character (form feed, vertical tab) is not a key line",
    'def key_line(line):\n    """R1: line -> (key, value) or None."""\n    s = line.lstrip(" \\t")',
    'def key_line(line):\n    """R1: line -> (key, value) or None."""\n    s = line.lstrip(" \\t\\v\\f")')

sub("f31_vtab_ff_trailing", "R1 any other trailing character (a vertical tab, a form feed) stays in the value",
    '    value = s[j + 1:].lstrip(" \\t").rstrip(" \\t")',
    '    value = s[j + 1:].lstrip(" \\t").rstrip(" \\t\\v\\f")')

sub("f32_hash_format_after_resolution", "R3 LP-HASH-FORMAT checked before resolution",
    '    if not hash_format_ok(h):\n        return "LP-HASH-FORMAT"\n    res = resource[1:] if resource.startswith("$") else resource\n    if res != "boot" or root != "":\n        return "LP-UNRESOLVED"',
    '    res = resource[1:] if resource.startswith("$") else resource\n    if res != "boot" or root != "":\n        return "LP-UNRESOLVED"\n    if not hash_format_ok(h):\n        return "LP-HASH-FORMAT"')

sub("f33_no_dollar_dropped", "R4 ONE leading '$' (gzip marker) is dropped from the resource",
    '    res = resource[1:] if resource.startswith("$") else resource',
    '    res = resource')

sub("f34_entry_column0", "R8 a line whose first non-blank character is '/'",
    'def entry_label(line):\n    """R8: line -> entry label or None."""\n    s = line.lstrip(" \\t")',
    'def entry_label(line):\n    """R8: line -> entry label or None."""\n    s = line')

sub("f35_one_slash_stripped", "R8 label = the line without its leading '/' characters",
    '    s = s.lstrip("/")',
    '    s = s[1:] if s.startswith("/") else s')

sub("f36_hmp_key_case_sensitive", "R8 hash_mismatch_panic key line (R1 rules: config keys match case-insensitively)",
    '            if klow == "hash_mismatch_panic" and first_hmp is None:',
    '            if key == "hash_mismatch_panic" and first_hmp is None:')

sub("f37_dir_conf_healthy", "R7 unreadable --conf (absent, a directory, ...) -> CANNOT-EVALUATE rc 2",
    '    try:\n        with open(conf, "rb") as f:\n            raw = f.read()\n    except OSError:',
    '    if os.path.isdir(conf):\n        print(json.dumps({"verdict": "HEALTHY", "rc": 0, "pins": [],\n                          "hash_mismatch_panic": None}))\n        return 0\n    try:\n        with open(conf, "rb") as f:\n            raw = f.read()\n    except OSError:')

sub("f41_value_lead_blank_kept", "R1 the value is the rest of the line with leading spaces/tabs removed",
    '    value = s[j + 1:].lstrip(" \\t").rstrip(" \\t")',
    '    value = s[j + 1:].rstrip(" \\t")')


def main():
    with open(BASE, encoding="utf-8") as f:
        base = f.read()
    diffs = []
    manifest = []
    for name, clause, old, new in F:
        n = base.count(old)
        if n != 1:
            print("BAD ANCHOR %s: count=%d" % (name, n), file=sys.stderr)
            return 1
        text = base.replace(old, new)
        path = os.path.join(HERE, "fx_%s.py" % name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
        manifest.append("%s\t%s" % (name, clause))
        d = difflib.unified_diff(base.splitlines(True), text.splitlines(True),
                                 fromfile="base.py", tofile="fx_%s.py" % name, n=2)
        diffs.append("".join(d))
    with open(os.path.join(HERE, "forgers.diff"), "w", encoding="utf-8") as f:
        f.write("\n".join(diffs))
    with open(os.path.join(HERE, "forgers.manifest.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")
    print("wrote %d forgers" % len(F))
    return 0


if __name__ == "__main__":
    sys.exit(main())
