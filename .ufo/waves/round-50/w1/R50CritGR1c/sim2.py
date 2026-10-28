# Faithful model of cmdline.c:153-200 (memparse), vsprintf.c:79-115 (simple_strtoull/
# simple_strntoull), kstrtox.c:26-40 (_parse_integer_fixup_radix) and sysfs.c:2031-2047.
ULLONG_MAX = (1 << 64) - 1
SPACE = " \t\n\v\f\r"
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

def isxdigit(c):
    return len(c) == 1 and c in "0123456789abcdefABCDEF"

def fixup_radix(s, base):
    # kstrtox.c:28-39 ; s is a string with a trailing NUL modelled as ""
    if base == 0:
        if s[0:1] == '0':
            s1 = s[1:2]; s2 = s[2:3]
            base = 16 if (s1.lower() == 'x' and isxdigit(s2)) else 8
        else:
            base = 10
    if base == 16 and s[0:1] == '0' and s[1:2].lower() == 'x':
        s = s[2:]
    return s, base

def parse_integer_limit(s, base, max_chars):
    val = n = 0
    for ch in s:
        if n >= max_chars: break
        i = DIGITS.find(ch.lower())
        if i < 0 or i >= base: break
        val = val * base + i; n += 1
    return n, val

def simple_strtoull(buf, i):
    # vsprintf.c:112-115 -> simple_strntoull(buf[i:], 0, INT_MAX)
    s = buf[i:]
    s2, base = fixup_radix(s, 0)                 # vsprintf.c:86
    prefix = len(s) - len(s2)                    # vsprintf.c:87
    n, val = parse_integer_limit(s2, base, 2**31 - 1)   # vsprintf.c:89
    return val, i + prefix + n                   # vsprintf.c:91-98

def memparse(buf, i):
    ret, j = simple_strtoull(buf, i)             # cmdline.c:156
    shl = 0
    ch = buf[j:j+1]
    if ch in "Ee": shl += 10
    if ch in "EePp": shl += 10
    if ch in "EePpTt": shl += 10
    if ch in "EePpTtGg": shl += 10
    if ch in "EePpTtGgMm": shl += 10
    if ch in "EePpTtGgMmKk": shl += 10
    if shl and j != i:                            # cmdline.c:189
        overflow = ret != 0 and (shl >= 64 or (ret >> (64 - shl)) != 0)
        ret = ULLONG_MAX if overflow else ret << shl   # cmdline.c:191-192
        j += 1                                    # cmdline.c:193
    return ret, j

def store(buf):
    # buf already carries a trailing NUL; an embedded NUL terminates the C string.
    limit, j = memparse(buf, 0)                   # sysfs.c:2040
    while j < len(buf) and buf[j] in SPACE:       # sysfs.c:2042 skip_spaces
        j += 1
    if j < len(buf):                              # sysfs.c:2043 *endptr != 0
        return ("-EINVAL", None)
    return ("accept", limit)

cases = [
    ("100M\n", "accept", 104857600), ("100m\n", "accept", 104857600),
    ("010\n", "accept", 8), ("0x10\n", "accept", 16), ("0X10\n", "accept", 16),
    ("10MB\n", "-EINVAL", None), ("10 M\n", "-EINVAL", None), ("-1\n", "-EINVAL", None),
    ("\n", "accept", 0), ("100 \n", "accept", 100), ("K\n", "-EINVAL", None),
    ("0xK\n", "-EINVAL", None), ("08\n", "-EINVAL", None), ("1K\n", "accept", 1024),
    ("1E\n", "accept", 1 << 60), ("16E\n", "accept", ULLONG_MAX),
    ("18446744073709551615K\n", "accept", ULLONG_MAX),
    ("100\0junk\n", "accept", 100),
]
bad = 0
for buf, want, wantv in cases:
    got, val = store(buf)
    ok = got == want and val == wantv
    bad += (not ok)
    print(f"{'PASS' if ok else 'FAIL'} {buf!r:26} -> {got} {val!r} (row: {want} {wantv!r})")
print("mismatches:", bad)
