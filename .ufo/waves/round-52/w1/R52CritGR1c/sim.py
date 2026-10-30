# Faithful model of the PINNED bytes only:
#  kstrtox.c:26-40 _parse_integer_fixup_radix ; kstrtox.c:58-95 _parse_integer_limit
#  vsprintf.c:79-101 simple_strntoull ; cmdline.c:153-200 memparse
KSTRTOX_OVERFLOW = (1 << 31)
def fixup_radix(s, base):
    i = 0
    if base == 0:
        if s[0] == '0':
            if s[1].lower() == 'x' and (len(s)>2 and s[2] in '0123456789abcdefABCDEF'):
                base = 16
            else:
                base = 8
        else:
            base = 10
    if base == 16 and s[0] == '0' and s[1].lower() == 'x':
        i = 2
    return i, base
def parse_limit(s, base, max_chars):
    res = 0; rv = 0; overflow = 0
    while rv < max_chars:
        c = s[rv]; lc = c.lower()
        if '0' <= c <= '9': val = ord(c) - 48
        elif 'a' <= lc <= 'f': val = ord(lc) - 97 + 10
        else: break
        if val >= base: break
        if res & (~0 << 60):
            pass
        res = res * base + val
        rv += 1
    return res, rv
def simple_strtoull(s):
    # vsprintf.c:79-101
    startp = s; cp_idx = 0
    pref, base = fixup_radix(s, 0)
    cp_idx = pref
    prefix_chars = pref
    max_chars = 2**31 - 1
    if prefix_chars < max_chars:
        result, rv = parse_limit(s[cp_idx:], base, max_chars - prefix_chars)
        cp_idx += rv
    else:
        cp_idx = 0 + max_chars
    return result, cp_idx   # cp_idx = index of endp
def memparse(ptr):
    ret, endp = simple_strtoull(ptr)
    shl = 0
    ch = ptr[endp] if endp < len(ptr) else '\0'
    order = ['E','P','T','G','M','K']
    for i,c in enumerate(order):
        if ch.lower() == c.lower():
            shl = 10 * (len(order) - i)
            break
    if shl and 0 != endp:
        if (ret >> (64 - shl)):
            ret = (1<<64) - 1
        else:
            ret = ret << shl
        endp += 1
    return ret, endp
def store(buf):
    limit, endp = memparse(buf)
    # skip_spaces (inferred: isspace)
    while endp < len(buf) and buf[endp] in ' \t\n\v\f\r':
        endp += 1
    if endp < len(buf) and buf[endp] != '\0':
        return 'EINVAL', None
    return 0, limit
cases = ['100M','100m','010','0x10','0X10','10MB','10 M','-1','\n','0x1E','0x1f','1K','1E','K','0xK','08','100 \n','0x10M','10M ','M']
for c in cases:
    r, lim = store(c + '\0')
    print(repr(c), '->', 'EINVAL' if r else f'limit={lim}')
