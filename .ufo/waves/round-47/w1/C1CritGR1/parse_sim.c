/* Simulation harness: verbatim transcription of snapshot functions
 * S246 cmdline.c:153-200 (memparse), S246 vsprintf.c:79-101,112-115
 * (simple_strntoull/simple_strtoull), S246 kstrtox.c:26-40,58-95
 * (_parse_integer_fixup_radix/_parse_integer_limit), plus the S243
 * sysfs.c:2040-2044 store tail. Kernel helpers shimmed with identical
 * semantics (linux/ctype.h, linux/overflow.h, linux/string.h).
 */
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <errno.h>

#define noinline
#define likely(x) (x)
#define unlikely(x) (x)
#define fallthrough /* fall through */
#define KSTRTOX_OVERFLOW 0x80000000u


#include <stdbool.h>
#define true 1
#define false 0
#define ULLONG_MAX_VAL (~0ULL)

/* --- shims: include/linux/ctype.h --- */
static int shim_isupper(unsigned char c){ return c>='A'&&c<='Z'; }
static unsigned char _tolower(unsigned char c){ if (shim_isupper(c)) c += 'a'-'A'; return c; }
static int isxdigit_(unsigned char c){ return (c>='0'&&c<='9')||(c>='a'&&c<='f')||(c>='A'&&c<='F'); }
static int isspace_(unsigned char c){ return c==' '||c=='\t'||c=='\n'||c=='\v'||c=='\f'||c=='\r'; }
#define isxdigit(c) isxdigit_((unsigned char)(c))
#define isspace(c) isspace_((unsigned char)(c))

/* --- shims: linux/overflow.h --- */
static int check_shl_overflow(unsigned long long a, unsigned int s, unsigned long long *d){
    if (s >= 64) { if (a) return 1; *d = 0; return 0; }
    if (a > (ULLONG_MAX_VAL >> s)) return 1;
    *d = a << s; return 0;
}
#define check_mul_overflow(a,b,d) __builtin_mul_overflow(a,b,d)
#define check_add_overflow(a,b,d) __builtin_add_overflow(a,b,d)

static const char *skip_spaces(const char *str){ while (isspace(*str)) str++; return str; }

/* ==== S246 kstrtox.c:26-40 verbatim ==== */
noinline
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

/* ==== S246 kstrtox.c:58-95 verbatim ==== */
noinline
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
		if (unlikely(res & (~0ull << 60))) {
			if (check_mul_overflow(res, base, &res) ||
			    check_add_overflow(res, val, &res)) {
				res = ULLONG_MAX_VAL;
				overflow = KSTRTOX_OVERFLOW;
			}
		} else {
			res = res * base + val;
		}
	}
	*p = res;
	return rv | overflow;
}

/* ==== S246 vsprintf.c:79-101 verbatim ==== */
noinline
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

/* ==== S246 vsprintf.c:112-115 verbatim ==== */
noinline
unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
	return simple_strntoull(cp, endp, base, INT_MAX);
}

/* ==== S246 cmdline.c:153-200 verbatim ==== */
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
			ret = ULLONG_MAX_VAL;
		endptr++;
	}

	if (retptr)
		*retptr = endptr;

	return ret;
}

/* ==== S243 sysfs.c:2040-2046 store tail ==== */
static int store(const char *buf, unsigned long long *limit_out)
{
	char *endptr;
	unsigned long long limit;
	limit = memparse(buf, &endptr);
	/* There could be trailing '\n', also catch any typos after the value. */
	endptr = (char *)skip_spaces(endptr);
	if (*endptr != 0)
		return -EINVAL;
    /* WRITE_ONCE(device->scrub_speed_max, limit); */
	*limit_out = limit;
	return 0;
}

int main(void)
{
	struct { const char *in; const char *note; } cases[] = {
		{ "100M",   "row: 104857600 accept" },
		{ "100m",   "row: 104857600 accept" },
		{ "010",    "row: 8 accept" },
		{ "0x10",   "row: 16 accept" },
		{ "10MB",   "row: EINVAL" },
		{ "10 M",   "row: EINVAL" },
		{ "-1",     "row: EINVAL" },
		{ "\n",     "row: 0 accept, clears limit" },
		{ "K",      "edge: bare suffix, no digit" },
		{ "0",      "edge: zero" },
		{ "16384E", "edge: shift overflow" },
		{ "10E",    "edge: shift overflow" },
		{ "18446744073709551616", "edge: unshifted overflow 2^64" },
		{ "18446744073709551615", "edge: ULLONG_MAX exact" },
		{ "10M ",   "edge: trailing space after suffix" },
		{ " 10",    "edge: leading space" },
		{ "010K",   "edge: octal+suffix" },
		{ "0x\n",   "edge: 0x no hexdigit" },
		{ "10\t\n", "edge: tab before newline" },
		{ "0xg",    "edge: 0x non-hexdigit" },
		{ "100M100", "edge: digit after suffix" },
		{ "08",     "edge: bad octal digit" },
	};
	size_t n = sizeof(cases)/sizeof(cases[0]);
	for (size_t i = 0; i < n; i++) {
		unsigned long long lim = 0;
		int rc = store(cases[i].in, &lim);
		printf("in=%-24s rc=%-8s limit=%llu  (%s)\n",
		       cases[i].in,
		       rc == -EINVAL ? "EINVAL" : "ACCEPT",
		       rc == 0 ? lim : 0ULL,
		       cases[i].note);
	}
	return 0;
}
