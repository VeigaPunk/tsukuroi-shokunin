/* Faithful emulation of Linux v7.2.11 lib/cmdline.c memparse() +
 * lib/vsprintf.c simple_strntoull() + lib/kstrtox.c _parse_integer_*() +
 * fs/btrfs/sysfs.c btrfs_devinfo_scrub_speed_max_store() tail check +
 * fs/kernfs/file.c buf[len]=0 + fs/sysfs/file.c count==0 gate.
 * Line-for-line transliteration; unsigned __int128 stands in for
 * check_mul_overflow/check_add_overflow/check_shl_overflow.
 */
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <stdint.h>

#define KSTRTOX_OVERFLOW    (1U << 31)

static int _tolower(unsigned char c) {
    if (c >= 'A' && c <= 'Z') return c + 'a' - 'A';
    return c;
}
static int isxdigit_c(unsigned char c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
}
/* kernfs guarantees isspace(0)==false; kernel _S = SP|space|tab|newline|v|f|r */
static int isspace_k(unsigned char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
}
static const char *skip_spaces(const char *s) { while (isspace_k((unsigned char)*s)) ++s; return s; }

static const char * _parse_integer_fixup_radix(const char *s, unsigned int *base)
{
    if (*base == 0) {
        if (s[0] == '0') {
            if (_tolower(s[1]) == 'x' && isxdigit_c(s[2]))
                *base = 16;
            else
                *base = 8;
        } else
            *base = 10;
    }
    if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')
        s += 2;
    return s;
}

static unsigned int _parse_integer_limit(const char *s, unsigned int base,
                  unsigned long long *p, size_t max_chars)
{
    unsigned int rv, overflow = 0;
    unsigned long long res;

    res = 0;
    for (rv = 0; rv < max_chars; rv++, s++) {
        unsigned int c = *(const unsigned char *)s;
        unsigned int lc = _tolower(c);
        unsigned int val;

        if ('0' <= c && c <= '9')
            val = c - '0';
        else if ('a' <= lc && lc <= 'f')
            val = lc - 'a' + 10;
        else
            break;
        if (val >= base)
            break;
        if (__builtin_expect(res & (~0ull << 60), 0)) {
            /* check_mul_overflow(res, base, &res) || check_add_overflow(res, val, &res) */
            __uint128_t m = (__uint128_t)res * base;
            __uint128_t a;
            if (m > ULLONG_MAX || (a = m + val) > ULLONG_MAX) {
                res = ULLONG_MAX;
                overflow = KSTRTOX_OVERFLOW;
            } else {
                res = (unsigned long long)a;
            }
        } else {
            res = res * base + val;
        }
    }
    *p = res;
    return rv | overflow;
}

static unsigned long long simple_strntoull(const char *startp, char **endp,
        unsigned int base, size_t max_chars)
{
    const char *cp;
    unsigned long long result = 0ULL;
    size_t prefix_chars;
    unsigned int rv;

    cp = _parse_integer_fixup_radix(startp, &base);
    prefix_chars = cp - startp;
    if (prefix_chars < max_chars) {
        rv = _parse_integer_limit(cp, base, &result, max_chars - prefix_chars);
        cp += (rv & ~KSTRTOX_OVERFLOW);          /* overflow flag masked */
    } else {
        cp = startp + max_chars;
    }
    if (endp)
        *endp = (char *)cp;
    return result;
}

static unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
    return simple_strntoull(cp, endp, base, INT_MAX);
}

static unsigned long long memparse(const char *ptr, char **retptr)
{
    char *endptr;
    unsigned long long ret = simple_strtoull(ptr, &endptr, 0);
    unsigned int shl = 0;

    switch (*endptr) {
    case 'E': case 'e': shl += 10; /* fallthrough */
    case 'P': case 'p': shl += 10; /* fallthrough */
    case 'T': case 't': shl += 10; /* fallthrough */
    case 'G': case 'g': shl += 10; /* fallthrough */
    case 'M': case 'm': shl += 10; /* fallthrough */
    case 'K': case 'k': shl += 10; /* fallthrough */
    default:
        break;
    }

    if (shl && __builtin_expect(ptr != endptr, 1)) {
        /* check_shl_overflow(ret, shl, &ret) */
        __uint128_t m = (__uint128_t)ret << shl;
        if (m > ULLONG_MAX)
            ret = ULLONG_MAX;
        else
            ret = (unsigned long long)m;
        endptr++;
    }
    if (retptr)
        *retptr = endptr;
    return ret;
}

/* emulate kernfs+sysfs+store on a raw user write of n bytes.
 * kernfs: buf = kmalloc(len+1); buf[len]=0; calls ops->write(...,buf,len).
 * sysfs : count==0 -> return 0, store never called.
 * store : returns -EINVAL or accepts. */
static const char *store_verdict(const char *user, size_t n, unsigned long long *setval, int *wrote)
{
    static char buf[8192];                 /* len+1 guaranteed; our inputs are small */
    memcpy(buf, user, n);
    buf[n] = '\0';                         /* kernfs/file.c:330 */
    *wrote = 0;
    if (n == 0) return "0-byte write: sysfs_kf_write returns 0, store not called"; /* sysfs/file.c:142 */
    char *endptr;
    unsigned long long limit = memparse(buf, &endptr);   /* btrfs sysfs.c:2040 */
    endptr = (char *)skip_spaces(endptr);                /* btrfs sysfs.c:2042 */
    if (*endptr != 0)
        return "EINVAL (rejected)";
    *setval = limit; *wrote = 1;
    return "accepted";
}

int main(void)
{
    struct { const char *label; const char *s; size_t n; } t[] = {
        /* GR1's worked examples */
        { "100M",      "100M", 4 },
        { "100m",      "100m", 4 },
        { "010",       "010", 3 },
        { "0x10",      "0x10", 4 },
        { "10MB",      "10MB", 4 },
        { "10 M",      "10 M", 4 },
        { "-1",        "-1", 2 },
        { "bare \\n",  "\n", 1 },
        /* echoes' actual byte stream */
        { "100M\\n",   "100M\n", 5 },
        /* attack candidates */
        { "overflow plain", "99999999999999999999", 20 },
        { "18446744073709551615", "18446744073709551615", 20 },
        { "18446744073709551616", "18446744073709551616", 20 },
        { "overflow+K", "99999999999999999999K", 21 },
        { "99999999999999999999Z", "99999999999999999999Z", 21 },
        { "0-byte write", "", 0 },
        { "spaces only", "   ", 3 },
        { "tab only", "\t", 1 },
        { "08",        "08", 2 },
        { "09",        "09", 2 },
        { "0o10",      "0o10", 4 },
        { "0X10",      "0X10", 4 },
        { "0x",        "0x", 2 },
        { "0xG",       "0xG", 3 },
        { " 100M",     " 100M", 5 },
        { "100M ",     "100M ", 5 },
        { "+100",      "+100", 4 },
        { "1e (exa)",  "1e", 2 },
        { "0x1e (hex)", "0x1e", 4 },
        { "embedded NUL 100\\0junk", "100\0junk", 8 },
        { "1K",        "1K", 2 },
        { "1G",        "1G", 2 },
        { "1T",        "1T", 2 },
        { "K alone",   "K", 1 },
        { "0",         "0", 1 },
        { "00",        "00", 2 },
    };
    printf("%-26s | %-70s | value\n", "input", "verdict");
    printf("---------------------------|------------------------------------------------------------------------|------\n");
    for (size_t i = 0; i < sizeof(t)/sizeof(t[0]); i++) {
        unsigned long long v = 0; int w = 0;
        const char *r = store_verdict(t[i].s, t[i].n, &v, &w);
        printf("%-26s | %-70s | %llu\n", t[i].label, r, w ? v : 0);
    }
    return 0;
}
