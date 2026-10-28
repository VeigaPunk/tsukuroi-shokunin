# Transcription of the pinned bodies: cmdline.c:153-201 (memparse), vsprintf.c:78-115,
# kstrtox.c:26-40 (fixup radix), kstrtox.c:57-95 (_parse_integer_limit), sysfs.c:2031-2047.
ULLONG_MAX = (1<<64)-1
OVERFLOW = 1<<31
def ch(s,i): return s[i] if i < len(s) else '\0'          # C string: past end reads NUL
def isxdigit(c): return c in "0123456789abcdefABCDEF"
def _tolower(c): return c.lower() if 'A'<=c<='Z' else c
def isspace(c): return c in " \t\n\v\f\r"
def fixup(s, base):                                        # kstrtox.c:26-40
    if base == 0:
        if ch(s,0) == '0':
            if _tolower(ch(s,1)) == 'x' and isxdigit(ch(s,2)): base = 16
            else: base = 8
        else: base = 10
    if base == 16 and ch(s,0)=='0' and _tolower(ch(s,1))=='x': s = s[2:]
    return s, base
def parse_int_limit(s, base, max_chars):                   # kstrtox.c:57-95
    res, overflow, rv = 0, 0, 0
    while rv < max_chars:
        c = ch(s,rv); lc = _tolower(c)
        if '0' <= c <= '9': val = ord(c)-48
        elif 'a' <= lc <= 'f': val = ord(lc)-87
        else: break
        if val >= base: break
        if res & (0xF << 60):
            if res*base > ULLONG_MAX or res*base+val > ULLONG_MAX:
                res = ULLONG_MAX; overflow = OVERFLOW
            else: res = res*base+val
        else: res = res*base+val
        rv += 1
    return res, rv|overflow
def simple_strntoull(startp, base, max_chars):             # vsprintf.c:78-101
    cp, base = fixup(startp, base)
    prefix = len(startp)-len(cp)
    if prefix < max_chars:
        result, rv = parse_int_limit(cp, base, max_chars-prefix)
        consumed = rv & ~OVERFLOW
        end = startp.find(cp) + prefix + consumed if False else prefix+consumed
    else:
        result, end = 0, max_chars
    return result, end
def simple_strtoull(s, base): return simple_strntoull(s, base, 2**31-1)   # vsprintf.c:112-115
def memparse(ptr):                                         # cmdline.c:153-201
    ret, endptr = simple_strtoull(ptr, 0)
    shl = 0
    for c in ('E','P','T','G','M','K'):
        if ch(ptr,endptr) in (c, c.lower()):
            shl = 10*(6-('E','P','T','G','M','K').index(c)); break  # E falls through all six: 60; K: 10
    if shl and 0 != endptr:                                # ptr != endptr
        if ret > (ULLONG_MAX >> shl): ret = ULLONG_MAX
        else: ret = ret << shl
        endptr += 1
    return ret, endptr
def store(buf):                                            # sysfs.c:2031-2047
    limit, e = memparse(buf)
    while ch(buf,e) and isspace(ch(buf,e)): e += 1         # skip_spaces
    if ch(buf,e) != '\0': return ('-EINVAL', None)
    return ('accepted', limit)
cases = ["100M","100m","010","0x10","10MB","10 M","-1","\n","","1K","4E","0X1f","08","0","0K","100M\n"]
for c in cases: print(repr(c), '->', store(c))
