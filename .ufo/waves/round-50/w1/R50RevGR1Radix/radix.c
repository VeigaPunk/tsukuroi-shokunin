
/* ---- harness prelude: kernel helpers stubbed, pinned bodies verbatim below ---- */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdlib.h>
#include <stddef.h>

/* linux/compiler_attributes.h: #define fallthrough __attribute__((__fallthrough__)) */
#define fallthrough __attribute__((__fallthrough__))
#define noinline __attribute__((noinline))
#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)
#define EXPORT_SYMBOL(x)
#define KSTRTOX_OVERFLOW (1u << 31)

/* include/linux/kstrtox.h: #define _tolower(c) ((c) | 0x20) */
static inline unsigned int _tolower_stub(unsigned int c) { return c | 0x20u; }
#define _tolower(c) _tolower_stub((unsigned int)(c))

/* include/linux/ctype.h isxdigit() for the ASCII set */
static inline int isxdigit_stub(int c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
}
#define isxdigit(c) isxdigit_stub((int)(c))

/* include/linux/ctype.h isspace() for the ASCII set */
static inline int isspace_stub(int c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
}

/* include/linux/overflow.h generic versions */
#define check_mul_overflow(a, b, d) __builtin_mul_overflow((a), (b), (d))
#define check_add_overflow(a, b, d) __builtin_add_overflow((a), (b), (d))
static inline bool check_shl_overflow(unsigned long long a, unsigned int s,
                                      unsigned long long *d) {
    if (s >= sizeof(a) * 8) { *d = a; return true; }
    *d = a << s;
    if (a != *d >> s) return true;
    return false;
}

/* lib/string.c skip_spaces() */
static char *skip_spaces(const char *str) {
    while (isspace_stub(*str)) ++str;
    return (char *)str;
}
/* ---- end prelude ---- */

/* ===== lib/kstrtox.c:26-40 (verbatim) ===== */
const char *_parse_integer_fixup_radix(const char *s, unsigned int *base)
{
	if (*base == 0) {
		if (s[0] == '0') {
			if (_tolower(s[1]) == 'x' && isxdigit(s[2]))
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

/* ===== lib/kstrtox.c:58-95 (verbatim) ===== */
unsigned int _parse_integer_limit(const char *s, unsigned int base, unsigned long long *p,
				  size_t max_chars)
{
	unsigned int rv, overflow = 0;
	unsigned long long res;

	res = 0;
	for (rv = 0; rv < max_chars; rv++, s++) {
		unsigned int c = *s;
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
		/*
		 * Check for overflow only if we are within range of
		 * it in the max base we support (16)
		 */
		if (unlikely(res & (~0ull << 60))) {
			if (check_mul_overflow(res, base, &res) ||
			    check_add_overflow(res, val, &res)) {
				res = ULLONG_MAX;
				overflow = KSTRTOX_OVERFLOW;
			}
		} else {
			res = res * base + val;
		}
	}
	*p = res;
	return rv | overflow;
}

/* ===== lib/kstrtox.c:98-101 (verbatim) ===== */
unsigned int _parse_integer(const char *s, unsigned int base, unsigned long long *p)
{
	return _parse_integer_limit(s, base, p, INT_MAX);
}

/* ===== lib/vsprintf.c:79-101 (verbatim) ===== */
static unsigned long long simple_strntoull(const char *startp, char **endp, unsigned int base, size_t max_chars)
{
	const char *cp;
	unsigned long long result = 0ULL;
	size_t prefix_chars;
	unsigned int rv;

	cp = _parse_integer_fixup_radix(startp, &base);
	prefix_chars = cp - startp;
	if (prefix_chars < max_chars) {
		rv = _parse_integer_limit(cp, base, &result, max_chars - prefix_chars);
		/* FIXME */
		cp += (rv & ~KSTRTOX_OVERFLOW);
	} else {
		/* Field too short for prefix + digit, skip over without converting */
		cp = startp + max_chars;
	}

	if (endp)
		*endp = (char *)cp;

	return result;
}

/* ===== lib/vsprintf.c:112-115 (verbatim) ===== */
unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
	return simple_strntoull(cp, endp, base, INT_MAX);
}

/* ===== lib/cmdline.c:153-200 (verbatim) ===== */
unsigned long long memparse(const char *ptr, char **retptr)
{
	char *endptr;	/* local pointer to end of parsed string */
	unsigned long long ret = simple_strtoull(ptr, &endptr, 0);
	unsigned int shl = 0;

	/* Consume valid suffix even in case of overflow. */
	switch (*endptr) {
	case 'E':
	case 'e':
		shl += 10;
		fallthrough;
	case 'P':
	case 'p':
		shl += 10;
		fallthrough;
	case 'T':
	case 't':
		shl += 10;
		fallthrough;
	case 'G':
	case 'g':
		shl += 10;
		fallthrough;
	case 'M':
	case 'm':
		shl += 10;
		fallthrough;
	case 'K':
	case 'k':
		shl += 10;
		fallthrough;
	default:
		break;
	}

	if (shl && likely(ptr != endptr)) {
		/* Have valid suffix with preceding number. */
		if (unlikely(check_shl_overflow(ret, shl, &ret)))
			ret = ULLONG_MAX;
		endptr++;
	}

	if (retptr)
		*retptr = endptr;

	return ret;
}

/* replica of the pinned store body (S243 sysfs.c:2031-2047); the container_of lookup and
   the WRITE_ONCE target are replaced by a file-scope variable, nothing else changes. */
static unsigned long long device_scrub_speed_max = 0;
static ssize_t store(const char *buf, size_t len)
{
    char *endptr;
    unsigned long long limit;

    limit = memparse(buf, &endptr);
    /* There could be trailing '\n', also catch any typos after the value. */
    endptr = skip_spaces(endptr);
    if (*endptr != 0)
        return -22;
    device_scrub_speed_max = limit;
    return (ssize_t)len;
}

struct kase { const char *bytes; const char *label; };

int main(void)
{
    struct kase cases[] = {
        {"100M\n",          "named: 100M"},
        {"100m\n",          "named: 100m"},
        {"010\n",           "named: 010"},
        {"0x10\n",          "named: 0x10"},
        {"10MB\n",          "named: 10MB"},
        {"10 M\n",          "named: 10 M"},
        {"-1\n",            "named: -1"},
        {"\n",              "named: bare newline"},
        {"0X10\n",          "extra: 0X10 (upper X)"},
        {"0x\n",            "extra: 0x no hex digit"},
        {"0X\n",            "extra: 0X no hex digit"},
        {"+10\n",           "extra: leading +"},
        {" 100\n",          "extra: leading space"},
        {"\t100\n",         "extra: leading tab"},
        {"M\n",             "extra: suffix only, no digits"},
        {"K\n",             "extra: K only"},
        {"0\n",             "extra: 0"},
        {"1K\n",            "extra: 1K"},
        {"1k\n",            "extra: 1k"},
        {"1G\n",            "extra: 1G"},
        {"1E\n",            "extra: 1E"},
        {"100M \n",         "extra: suffix then space"},
        {"100M\n",          "extra: suffix then newline"},
        {"100M\t\n",        "extra: suffix then tab+newline"},
        {"100 \n",          "extra: number then space+newline"},
        {"100\n \n",        "extra: number then newline+space+newline"},
        {"100Mx\n",         "extra: suffix then junk"},
        {"0x10M\n",         "extra: hex then suffix"},
        {"08\n",            "extra: 08 (octal rejects 8)"},
        {"0x1g\n",          "extra: hex digit then non-hex"},
        {"1e3\n",           "extra: 1e3 (e is the E suffix)"},
        {"18446744073709551615\n", "extra: 2^64-1"},
        {"18446744073709551616\n", "extra: 2^64 (decimal overflow)"},
        {"0xFFFFFFFFFFFFFFFFK\n",  "extra: suffix shift overflow"},
        {"0xFFFFFFFFFFFFFFFFKK\n", "extra: suffix overflow + second letter"},
        {"1024K\n",         "extra: 1024K"},
        {"\n\n",            "extra: two newlines"},
        {"",                "extra: empty write buffer"},
    };
    size_t i, n = sizeof(cases) / sizeof(cases[0]);
    for (i = 0; i < n; i++) {
        char *endp = NULL;
        unsigned long long raw = memparse(cases[i].bytes, &endp);
        ssize_t rc = store(cases[i].bytes, strlen(cases[i].bytes));
        if (rc < 0)
            printf("%-42s | memparse=%-20llu endptr=%td | store=EINVAL(%zd)\n",
                   cases[i].label, raw, (ptrdiff_t)(endp - cases[i].bytes), rc);
        else
            printf("%-42s | memparse=%-20llu endptr=%td | store=ACCEPT(%zd) limit=%llu\n",
                   cases[i].label, raw, (ptrdiff_t)(endp - cases[i].bytes), rc,
                   device_scrub_speed_max);
        device_scrub_speed_max = 0;
    }
    return 0;
}
