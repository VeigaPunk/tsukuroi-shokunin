/* Semantic harness: functions copied from pinned bytes
 *   S246 lib/cmdline.c, lib/vsprintf.c, lib/kstrtox.c (round-45 snapshot)
 *   S243 fs/btrfs/sysfs.c store (round-44 snapshot)
 * Shims: likely/unlikely/fallthrough macros, k_tolower, skip_spaces,
 * check_shl_overflow (kernel semantics for 0<=s<64: overflow iff a > ULLONG_MAX>>s),
 * check_mul_overflow/check_add_overflow via compiler builtins.
 */
#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include <limits.h>
#include <string.h>


typedef unsigned long long u64;
#define likely(x) (x)
#define unlikely(x) (x)
#define fallthrough __attribute__((fallthrough))
#define KSTRTOX_OVERFLOW (1U << 31)

static inline int k_tolower(int c) { return (c >= 'A' && c <= 'Z') ? c + 32 : c; }
static inline int k_isspace(int c) { return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r'; }
static inline int isxdigit(int c) { return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'); }
static inline const char *skip_spaces(const char *str)
{ while (k_isspace((unsigned char)*str)) ++str; return str; }
static inline bool check_shl_overflow(u64 a, int s, u64 *res)
{
	if (s < 0 || s >= 64) { *res = 0; return true; }
	if (a > (ULLONG_MAX >> s)) return true;
	*res = a << s;
	return false;
}
static inline bool check_mul_overflow(u64 a, unsigned int b, u64 *res)
{ return __builtin_mul_overflow(a, (u64)b, res); }
static inline bool check_add_overflow(u64 a, unsigned int b, u64 *res)
{ return __builtin_add_overflow(a, (u64)b, res); }

/* ---- pinned: lib/kstrtox.c:25-40 ---- */
const char *_parse_integer_fixup_radix(const char *s, unsigned int *base)
{
	if (*base == 0) {
		if (s[0] == '0') {
			if (k_tolower(s[1]) == 'x' && isxdigit(s[2]))
				*base = 16;
			else
				*base = 8;
		} else
			*base = 10;
	}
	if (*base == 16 && s[0] == '0' && k_tolower(s[1]) == 'x')
		s += 2;
	return s;
}

/* ---- pinned: lib/kstrtox.c:57-95 ---- */
unsigned int _parse_integer_limit(const char *s, unsigned int base,
				  unsigned long long *p, size_t max_chars)
{
	unsigned int rv, overflow = 0;
	unsigned long long res;

	res = 0;
	for (rv = 0; rv < max_chars; rv++, s++) {
		unsigned int c = *s;
		unsigned int lc = k_tolower(c);
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

/* ---- pinned: lib/vsprintf.c:78-115 ---- */
unsigned long long simple_strntoull(const char *startp, char **endp,
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
		cp += (rv & ~KSTRTOX_OVERFLOW);
	} else {
		cp = startp + max_chars;
	}

	if (endp)
		*endp = (char *)cp;

	return result;
}

unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
	return simple_strntoull(cp, endp, base, INT_MAX);
}

/* ---- pinned: lib/cmdline.c:153-200 ---- */
unsigned long long memparse(const char *ptr, char **retptr)
{
	char *endptr;
	unsigned long long ret = simple_strtoull(ptr, &endptr, 0);
	unsigned int shl = 0;

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
		if (unlikely(check_shl_overflow(ret, shl, &ret)))
			ret = ULLONG_MAX;
		endptr++;
	}

	if (retptr)
		*retptr = endptr;

	return ret;
}

/* ---- pinned: fs/btrfs/sysfs.c:2031-2047 (store body) ---- */
static int store(const char *buf, unsigned long long *out)
{
	char *endptr;
	unsigned long long limit = memparse(buf, &endptr);
	endptr = (char *)skip_spaces(endptr);
	if (*endptr != 0)
		return -22; /* -EINVAL */
	*out = limit;
	return 0;
}

int main(void)
{
	const char *in[] = {
		"100M", "100m", "010", "0x10", "0X10", "10MB", "10 M", "-1",
		"\n", "0\n", "K", "1K", "10", "0x", "08", "4096",
		"16E", "1E", "18446744073709551616", "18446744073709551616K",
		"1000000000000E", " 5", "5 ", "5\t\n", "+5", "0x1f", "0b101",
		NULL
	};
	int i;
	for (i = 0; in[i]; i++) {
		char *endptr;
		unsigned long long v = memparse(in[i], &endptr);
		unsigned long long out = 0;
		int rc = store(in[i], &out);
		printf("%-24s memparse=%-20llu endptr@%-2ld rc=%s value=%llu\n",
		       in[i][0] == '\n' ? "\\n" : in[i],
		       v, (long)(endptr - in[i]),
		       rc == 0 ? "ACCEPT" : "EINVAL", out);
	}
	return 0;
}
