#!/usr/bin/env python3
"""Generate one-clause forgers of base.py: each bends exactly one written r90 clause.

Every patch is asserted to apply exactly once; a forger whose patch does not change the source
is a bug in this generator, not a finding.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "base.py")
OUT = os.path.join(HERE, "forgers")

A_VALID = 'VALID_RESOURCES = (b"hdd", b"odd", b"boot", b"guid", b"uuid", b"fslabel", b"tftp")'
A_EFI = 'EFI_PROTOCOLS = (b"efi", b"uefi", b"efi_chainload")'
A_NAME = '    if name not in VALID_RESOURCES:\n        return "LP-BAD-RESOURCE"'
A_BOOTROOT = '    if name != b"boot" or root != b"":\n        return "LP-UNRESOLVED"'
A_PAREN = '    p = val.find(b"(")\n    if p < 0:\n        return None\n    q = val.find(b"):/", p + 1)'
A_LASTHASH = '    h = val.rfind(b"#")'
A_HASHFMT = '    if not HASH_RE.match(hashb):\n        return "LP-HASH-FORMAT"'
A_LINES = '    return data.replace(b"\\r", b"").split(b"\\n")'
A_KEYHEAD = ('    s = line.lstrip(b" \\t")\n    if not s or s[0:1] == b"#":\n'
             '        return None\n    i = s.find(b":")')
A_KEY = '    key = s[:i]'
A_VALUE = '    val = s[i + 1:].lstrip(b" \\t").rstrip(b" \\t")'
A_LABEL = '    s = line.lstrip(b" \\t").lstrip(b"/")'
A_BODY = ('        end = starts[n + 1] if n + 1 < len(starts) else len(lines)\n'
          '        body = list(enumerate(lines[start + 1:end], start=start + 2))')
A_IMAGE = ('        idx, _ = first_key_value(lines, b"path", body)\n'
           '        if idx is None:\n'
           '            idx, _ = first_key_value(lines, b"image_path", body)')
A_HMP = '    hmp_idx, hmp_val = first_key_value(lines, b"hash_mismatch_panic")'
A_MEASURED = '    imageline, mval = first_key_value(lines, b"measured_boot")'
A_CONS_UNRES = '        elif status == "LP-UNRESOLVED":\n            cons = "not-modelled"'
A_CONS_MISS = ('        elif status == "LP-MISSING":\n'
               '            cons = "panic" if i in img else "not-modelled"')
A_CONS_OPT = '        elif optional:\n            cons = "skip"'
A_CONS_MISMATCH = ('        else:  # LP-MISMATCH\n            if sb:\n                cons = "panic"\n'
                   '            elif no_hmp:\n                cons = "prompt"\n'
                   '            else:\n                cons = "panic"')
A_FAULTS = ('        if status in ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", '
            '"LP-BAD-RESOURCE"):\n            faults = True')
A_VERDICT = ('    if faults:\n        verdict, rc = "DEGRADED", 1\n'
             '    elif unresolved:\n        verdict, rc = "CANNOT-EVALUATE", 2')
A_UNREADABLE = ('    except OSError:\n        print(json.dumps({"verdict": "CANNOT-EVALUATE", '
                '"rc": 2, "on_panic": "menu",\n                          "pins": []}))\n'
                '        return 2')
A_REQUESTED = '    requested = sb or (mval is not None and mval == b"yes")'
A_ONPANIC = ('    if not requested:\n        on_panic = "menu"\n'
             '    elif a.tpm_present == 1:\n        on_panic = "halt"\n'
             '    elif a.tpm_present == 0:\n        on_panic = "menu"')
A_PRINT = ('    print(json.dumps({"verdict": verdict, "rc": rc, "on_panic": on_panic,\n'
           '                      "hash_mismatch_panic": hmp, "pins": pins}))')

FORGERS = [
    ("F01-resource-substring", "R4 the seven names matched by substring",
     [(A_NAME, '    if not any(r in name for r in VALID_RESOURCES):\n'
               '        return "LP-BAD-RESOURCE"')]),
    ("F02-empty-resource-boot", "R4 an empty resource name is invalid (defaults to boot)",
     [(A_NAME, '    if name == b"":\n        name = b"boot"\n'
               '    if name not in VALID_RESOURCES:\n        return "LP-BAD-RESOURCE"')]),
    ("F03-boot-any-root", "R4 only boot with an empty root resolves",
     [(A_BOOTROOT, '    if name != b"boot":\n        return "LP-UNRESOLVED"')]),
    ("F04-any-empty-root", "R4 only empty-root boot() resolves",
     [(A_BOOTROOT, '    if root != b"":\n        return "LP-UNRESOLVED"')]),
    ("F05-optional-missing-skip", "R6 optional skip covers only MISMATCH/HASH-FORMAT/BAD-RESOURCE",
     [(A_CONS_MISS, '            cons = "skip" if optional else '
                    '("panic" if i in img else "not-modelled")')]),
    ("F06-optional-unresolved-skip", "R6 LP-UNRESOLVED is never skip",
     [(A_CONS_UNRES, '        elif status == "LP-UNRESOLVED":\n'
                     '            cons = "skip" if optional else "not-modelled"')]),
    ("F07-no-means-skip", "R6 hash_mismatch_panic no -> prompt",
     [('            elif no_hmp:\n                cons = "prompt"',
       '            elif no_hmp:\n                cons = "skip"')]),
    ("F08-no-before-sb", "R6 secure-boot panic precedes the no -> prompt rule",
     [(A_CONS_MISMATCH, '        else:  # LP-MISMATCH\n            if no_hmp:\n'
                        '                cons = "prompt"\n            elif sb:\n'
                        '                cons = "panic"\n            else:\n'
                        '                cons = "panic"')]),
    ("F09-ce-before-degraded", "R7 DEGRADED outranks CANNOT-EVALUATE",
     [(A_VERDICT, '    if unresolved:\n        verdict, rc = "CANNOT-EVALUATE", 2\n'
                  '    elif faults:\n        verdict, rc = "DEGRADED", 1')]),
    ("F10-unreadable-healthy", "R7 unreadable conf -> CANNOT-EVALUATE rc 2 empty pins",
     [(A_UNREADABLE, '    except OSError:\n        print(json.dumps({"verdict": "HEALTHY", '
                     '"rc": 0, "on_panic": "menu",\n                          "pins": []}))\n'
                     '        return 0')]),
    ("F11-format-not-fault", "R7 LP-HASH-FORMAT is a fault",
     [(A_FAULTS, '        if status in ("LP-MISMATCH", "LP-MISSING", '
                 '"LP-BAD-RESOURCE"):\n            faults = True')]),
    ("F12-image-either-key", "R9 the image line is the first path, else the first image_path",
     [(A_IMAGE, '        idx = None\n        for _j, _ln in body:\n'
                '            _kl = key_line(_ln)\n'
                '            if _kl is not None and _kl[0] in (b"path", b"image_path"):\n'
                '                idx = _j\n                break')]),
    ("F13-image-path-only-if-pin", "R9 the image line need not be a pin",
     [(A_IMAGE, '        idx, _ = first_key_value(lines, b"path", body)\n'
                '        if idx is not None:\n'
                '            _kl = key_line(lines[idx - 1])\n'
                '            if _kl is None or parse_pin(_kl[1]) is None:\n'
                '                idx = None\n'
                '        if idx is None:\n'
                '            idx, _ = first_key_value(lines, b"image_path", body)')]),
    ("F14-efi-only", "R9 uefi/efi_chainload are efi chainload protocols",
     [(A_EFI, 'EFI_PROTOCOLS = (b"efi",)')]),
    ("F15-body-ends-at-blank", "R9 body runs to the next entry line or EOF",
     [(A_BODY, '        end = starts[n + 1] if n + 1 < len(starts) else len(lines)\n'
               '        for _k in range(start + 1, end):\n'
               '            if not lines[_k].strip(b" \\t"):\n'
               '                end = _k\n                break\n'
               '        body = list(enumerate(lines[start + 1:end], start=start + 2))')]),
    ("F16-tpm1-halt-always", "R10 --tpm-present 1 only matters when measured boot is requested",
     [(A_ONPANIC, '    if a.tpm_present == 1:\n        on_panic = "halt"\n'
                  '    elif not requested:\n        on_panic = "menu"\n'
                  '    elif a.tpm_present == 1:\n        on_panic = "halt"\n'
                  '    elif a.tpm_present == 0:\n        on_panic = "menu"')]),
    ("F17-tpm0-sb-halt", "R10 --tpm-present 0 -> menu",
     [('    elif a.tpm_present == 0:\n        on_panic = "menu"',
       '    elif a.tpm_present == 0:\n        on_panic = "halt" if sb else "menu"')]),
    ("F18-on-panic-omitted", "R10 the top-level object MUST carry on_panic",
     [(A_PRINT, '    print(json.dumps({"verdict": verdict, "rc": rc,\n'
                '                      "hash_mismatch_panic": hmp, "pins": pins}))')]),
    ("F19-measured-value-set", "R10 measured_boot is strcmp yes (not 1/true)",
     [(A_REQUESTED, '    requested = sb or (mval is not None and mval in '
                    '(b"yes", b"1", b"true"))')]),
    ("F20-value-rstrip-all", "R1 the value loses only trailing spaces/tabs",
     [(A_VALUE, '    val = s[i + 1:].lstrip(b" \\t").rstrip()')]),
    ("F21-comment-is-key", "R1 a line whose first non-blank character is # is not a key line",
     [(A_KEYHEAD, '    s = line.lstrip(b" \\t#")\n    if not s:\n        return None\n'
                  '    i = s.find(b":")')]),
    ("F22-blank-before-colon", "R1 the key is followed directly by ':'",
     [(A_KEYHEAD, '    s = line.lstrip(b" \\t")\n    if not s or s[0:1] == b"#":\n'
                  '        return None\n    i = s.find(b":")'),
      (A_KEY, '    key = s[:i].rstrip(b" \\t")')]),
    ("F23-first-hash", "R2 the hash is the text after the LAST #",
     [(A_LASTHASH, '    h = val.find(b"#")')]),
    ("F24-no-paren", "R2 the URI needs a '(' then '):/'",
     [(A_PAREN, '    p = val.find(b"(")\n    if p < 0:\n        _h = val.rfind(b"#")\n'
                '        _c = val.find(b":/")\n'
                '        if _c < 0 or _h < _c + 2:\n            return None\n'
                '        return val[:_c], b"", val[_c + 2:_h], val[_h + 1:]\n'
                '    q = val.find(b"):/", p + 1)')]),
    ("F25-splitlines", "R1 only CRs are removed and only \\n separates lines",
     [(A_LINES, '    _d = data.replace(b"\\r", b"")\n'
                '    for _sep in (b"\\x0b", b"\\x0c", b"\\x85"):\n'
                '        _d = _d.replace(_sep, b"\\n")\n'
                '    return _d.split(b"\\n")')]),
    ("F26-label-keeps-slash", "R8 the label drops its leading '/' characters",
     [(A_LABEL, '    s = line.lstrip(b" \\t")')]),
    ("F27-hmp-last", "R8 hash_mismatch_panic is the FIRST such key line",
     [(A_HMP, '    hmp_idx = hmp_val = None\n'
              '    for _j in range(len(lines) - 1, -1, -1):\n'
              '        _kl = key_line(lines[_j])\n'
              '        if _kl is not None and _kl[0] == b"hash_mismatch_panic":\n'
              '            hmp_idx, hmp_val = _j + 1, _kl[1]\n            break')]),
    ("F28-sb-needs-tpm1", "R10 --secure-boot-enforced 1 requests measured boot",
     [(A_REQUESTED, '    requested = (mval is not None and mval == b"yes") or '
                    '(sb and a.tpm_present == 1)')]),
    ("F29-optional-mismatch-panics", "R6 optional skip covers LP-MISMATCH",
     [(A_CONS_OPT, '        elif optional and status in ("LP-HASH-FORMAT", '
                   '"LP-BAD-RESOURCE"):\n            cons = "skip"')]),
    ("F30-cr-not-removed", "R1 every CR anywhere is removed",
     [(A_LINES, '    return data.split(b"\\n")')]),
    ("F31-value-rstrip-space-only", "R1 trailing blanks are spaces and tabs",
     [(A_VALUE, '    val = s[i + 1:].lstrip(b" \\t").rstrip(b" ")')]),
]


def main():
    src = open(SRC, "r", encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    for name, clause, patches in FORGERS:
        text = src
        for old, new in patches:
            n = text.count(old)
            if n != 1:
                print("FAIL %s: anchor count %d for %r" % (name, n, old[:60]))
                bad += 1
                break
            text = text.replace(old, new)
        else:
            path = os.path.join(OUT, name + ".py")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write('"""FORGER %s: bends one clause -- %s"""\n' % (name, clause))
                fh.write(text)
            os.chmod(path, 0o755)
    print("forgers=%d bad=%d" % (len(FORGERS) - bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
