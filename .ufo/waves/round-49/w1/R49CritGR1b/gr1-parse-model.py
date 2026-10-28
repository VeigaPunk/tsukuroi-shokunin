# Receipt, seat R49CritGR1b: independent Python model of the pinned GR1 chain,
# transcribed line-by-line from
#   .ufo/waves/round-45/frozen/src/cmdline.c:153-200   (memparse)
#   .ufo/waves/round-45/frozen/src/vsprintf.c:79-115   (simple_strntoull / simple_strtoull, max_chars=INT_MAX)
#   .ufo/waves/round-45/frozen/src/kstrtox.c:26-40     (_parse_integer_fixup_radix)
#   .ufo/waves/round-44/frozen/src/sysfs.c:2031-2049   (btrfs_devinfo_scrub_speed_max_store)
# Helper bodies that live outside the pinned set (check_shl_overflow, skip_spaces,
# isxdigit, _tolower) are modelled at their documented/name-stated contract, which is
# exactly the reliance the row makes. No claim here is evidence about those helpers.
ULLONG_MAX = 2 ** 64 - 1
HEX = '0123456789abcdefABCDEF'
SPACE = ' \t\n\r\f\v'


def fixup_radix(s, base):
    # kstrtox.c:26-40
    if base == 0:
        if s[:1] == '0':
            if len(s) > 1 and s[1].lower() == 'x' and len(s) > 2 and s[2] in HEX:
                base = 16
            else:
                base = 8
        else:
            base = 10
    if base == 16 and s[:1] == '0' and len(s) > 1 and s[1].lower() == 'x':
        s = s[2:]
    return s, base


def parse_integer_limit(s, base):
    # kstrtox.c:58-... ; overflow pins res to ULLONG_MAX (kstrtox.c:50)
    res, rv = 0, 0
    while rv < len(s):
        c = s[rv]
        lc = c.lower()
        val = None
        if '0' <= c <= '9':
            val = ord(c) - 48
        elif 'a' <= lc <= 'f' and base == 16:
            val = ord(lc) - 87
        if val is None or val >= base:
            break
        res = ULLONG_MAX if res > (ULLONG_MAX - val) // base else res * base + val
        rv += 1
    return res, rv


def simple_strntoull(startp, base):
    # vsprintf.c:79-101 with max_chars = INT_MAX (vsprintf.c:114)
    cp, base = fixup_radix(startp, base)
    prefix = len(startp) - len(cp)
    res, rv = parse_integer_limit(cp, base)
    return res, startp[:prefix + rv]


SUFFIX_SHIFT = {'E': 60, 'e': 60, 'P': 50, 'p': 50, 'T': 40, 't': 40,
                'G': 30, 'g': 30, 'M': 20, 'm': 20, 'K': 10, 'k': 10}


def memparse(text):
    # cmdline.c:153-200
    ret, endp = simple_strntoull(text, 0)
    nxt = text[len(endp):len(endp) + 1]
    shl = SUFFIX_SHIFT.get(nxt, 0)
    if shl and len(endp) > 0:                      # cmdline.c:189  ptr != endptr
        v = ret << shl
        ret = v if v <= ULLONG_MAX else ULLONG_MAX  # cmdline.c:191-192
        endp = text[:len(endp) + 1]                 # cmdline.c:193  endptr++
    return ret, endp


def store(text):
    # sysfs.c:2040-2046
    limit, endp = memparse(text)
    i = len(endp)
    while i < len(text) and text[i] in SPACE:      # sysfs.c:2042 skip_spaces
        i += 1
    if i < len(text):                              # sysfs.c:2043
        return '-EINVAL'                           # sysfs.c:2044
    return limit                                   # sysfs.c:2045-2046


if __name__ == '__main__':
    for t in ['100M', '100m', '010', '0x10', '10MB', '10 M', '-1', '\n',
              '0', '1K', '4E', '0X1f', 'M', '0x', '08', '1024K',
              '18446744073709551616E', '999999999999999999999E']:
        print(repr(t).ljust(26), store(t))
