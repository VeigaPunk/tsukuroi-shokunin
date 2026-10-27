/* SR8 verification harness: kernel v7.2.11 memparse / scrub_speed_max store
 * semantics, copied from the pinned sources (line refs in comments).
 * Sources under /fast/scratch/hyaku/tsukuroi-r44/C2ExecSysfsSR8:
 *   lib_vsprintf.c, lib_kstrtox.c, lib_string_helpers.c, lib_ctype.c,
 *   lib_cmdline.c, include_linux_ctype.h.
 * Store body: frozen/src/sysfs.c:2031-2047.
 * Build: gcc -O0 -std=gnu11 -o sr8 sr8_harness.c
 */
#include <stdio.h>
#include <string.h>
#include <limits.h>

/* include/linux/ctype.h:13-20 */
#define _U 0x01
#define _L 0x02
#define _D 0x04
#define _C 0x08
#define _P 0x10
#define _S 0x20
#define _X 0x40
#define _SP 0x80

/* lib/ctype.c:11-38, copied verbatim */
const unsigned char _ctype[] = {
_C,_C,_C,_C,_C,_C,_C,_C,				/* 0-7 */
_C,_C|_S,_C|_S,_C|_S,_C|_S,_C|_S,_C,_C,			/* 8-15 */
_C,_C,_C,_C,_C,_C,_C,_C,				/* 16-23 */
_C,_C,_C,_C,_C,_C,_C,_C,				/* 24-31 */
_S|_SP,_P,_P,_P,_P,_P,_P,_P,				/* 32-39 */
_P,_P,_P,_P,_P,_P,_P,_P,				/* 40-47 */
_D,_D,_D,_D,_D,_D,_D,_D,				/* 48-55 */
_D,_D,_P,_P,_P,_P,_P,_P,				/* 56-63 */
_P,_U|_X,_U|_X,_U|_X,_U|_X,_U|_X,_U|_X,_U,		/* 64-71 */
_U,_U,_U,_U,_U,_U,_U,_U,				/* 72-79 */
_U,_U,_U,_U,_U,_U,_U,_U,				/* 80-87 */
_U,_U,_U,_P,_P,_P,_P,_P,				/* 88-95 */
_P,_L|_X,_L|_X,_L|_X,_L|_X,_L|_X,_L|_X,_L,		/* 96-103 */
_L,_L,_L,_L,_L,_L,_L,_L,				/* 104-111 */
_L,_L,_L,_L,_L,_L,_L,_L,				/* 112-119 */
_L,_L,_L,_P,_P,_P,_P,_C,				/* 120-127 */
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,			/* 128-143 */
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,			/* 144-159 */
_S|_SP,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,	/* 160-175 */
_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,_P,	/* 176-191 */
_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,_U,	/* 192-207 */
_U,_U,_U,_U,_U,_U,_U,_P,_U,_U,_U,_U,_U,_U,_U,_L,	/* 208-223 */
_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,_L,	/* 224-239 */
_L,_L,_L,_L,_L,_L,_L,_P,_L,_L,_L,_L,_L,_L,_L,_L};	/* 240-255 */

/* include/linux/ctype.h:22-33, 34 */
#define __ismask(x) (_ctype[(int)(unsigned char)(x)])
#define isspace(c)	((__ismask(c)&(_S)) != 0)
#define isxdigit(c)	((__ismask(c)&(_D|_X)) != 0)
static inline unsigned char _tolower(unsigned char c)
{
	if (c >= 'A' && c <= 'Z')
		c += 'a' - 'A';
	return c;
}

#define KSTRTOX_OVERFLOW	(1U << 31)

/* lib/kstrtox.c:25-40 */
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

/* lib/kstrtox.c:56-92 */
unsigned int _parse_integer_limit(const char *s, unsigned int base,
				  unsigned long long *p, size_t max_chars)
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
		if (__builtin_expect(res & (~0ull << 60), 0)) {
			if (__builtin_mul_overflow(res, base, &res) ||
			    __builtin_add_overflow(res, val, &res)) {
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

/* lib/vsprintf.c:79-102 (simple_strntoull) */
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

/* lib/vsprintf.c:112-116 */
unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
	return simple_strntoull(cp, endp, base, INT_MAX);
}

/* lib/string_helpers.c:846-852 */
char *skip_spaces(const char *str)
{
	while (isspace(*str))
		++str;
	return (char *)str;
}

/* lib/cmdline.c:153-199 */
unsigned long long memparse(const char *ptr, char **retptr)
{
	char *endptr;
	unsigned long long ret = simple_strtoull(ptr, &endptr, 0);
	unsigned int shl = 0;

	switch (*endptr) {
	case 'E':
	case 'e':
		shl += 10;
		__attribute__((fallthrough));
	case 'P':
	case 'p':
		shl += 10;
		__attribute__((fallthrough));
	case 'T':
	case 't':
		shl += 10;
		__attribute__((fallthrough));
	case 'G':
	case 'g':
		shl += 10;
		__attribute__((fallthrough));
	case 'M':
	case 'm':
		shl += 10;
		__attribute__((fallthrough));
	case 'K':
	case 'k':
		shl += 10;
		__attribute__((fallthrough));
	default:
		break;
	}

	if (shl && __builtin_expect(ptr != endptr, 1)) {
		/* include/linux/overflow.h:192-202 check_shl_overflow(ret, shl, &ret) */
		unsigned long long _a_full = ret;
		unsigned int _to_shift = (shl >= 0 && (unsigned int)shl < 8 * sizeof(ret)) ? shl : 0;
		unsigned long long _d = (_a_full << _to_shift);
		int ovf = (_to_shift != (unsigned int)shl || (_d >> _to_shift) != _a_full);
		if (__builtin_expect(ovf, 0))
			ret = ULLONG_MAX;
		else
			ret = _d;
		endptr++;
	}
	if (retptr)
		*retptr = endptr;
	return ret;
}

/* fs/btrfs/sysfs.c:2031-2047 as reached through fs/sysfs/file.c:136-146
 * sysfs_kf_write (count==0 returns 0 before the store runs) */
static int scrub_speed_max_store(const char *buf, size_t count, unsigned long long *out)
{
	char *endptr;
	unsigned long long limit;

	if (!count)
		return -999;		/* not reached: 0-byte write is a no-op */
	limit = memparse(buf, &endptr);
	endptr = skip_spaces(endptr);
	if (*endptr != 0)
		return -22;			/* -EINVAL */
	*out = limit;
	return 0;
}

struct t { const char *in; int ok; unsigned long long val; };
static const struct t tests[] = {
	{"0\n", 1, 0},
	{"0", 1, 0},
	{"\n", 1, 0},
	{"1048576\n", 1, 1048576ULL},
	{"1K", 1, 1024ULL},
	{"1k\n", 1, 1024ULL},
	{"1M\n", 1, 1048576ULL},
	{"1m", 1, 1048576ULL},
	{"2G", 1, 2ULL << 30},
	{"2g", 1, 2ULL << 30},
	{"3T", 1, 3ULL << 40},
	{"3t", 1, 3ULL << 40},
	{"4P", 1, 4ULL << 50},
	{"4p", 1, 4ULL << 50},
	{"5E", 1, 5ULL << 60},
	{"5e", 1, 5ULL << 60},
	{"1M\n\n", 1, 1048576ULL},
	{"1M\t\r\v\f\n", 1, 1048576ULL},
	{"0x1000\n", 1, 4096ULL},
	{"010", 1, 8ULL},
	{"010M", 1, 8ULL << 20},
	{"18446744073709551615", 1, ULLONG_MAX},
	{"18446744073709551616", 1, ULLONG_MAX},
	{"1M ", 1, 1048576ULL},
	{" 1M", 0, 0},
	{"1 M", 0, 0},
	{"1MiB", 0, 0},
	{"1MB", 0, 0},
	{"1M x", 0, 0},
	{"K", 0, 0},
	{"1E1", 0, 0},
	{"-1", 0, 0},
	{"+1", 0, 0},
	{"1\n2", 0, 0},
	{"1\x01", 0, 0},
	{"1.5G", 0, 0},
	{"", 0, 0},	/* count==0: store not called (fs/sysfs/file.c:142) */
	{"1M\0junk", 1, 1048576ULL},	/* embedded NUL: kernfs NUL-terminates (fs/kernfs/file.c:330) */
	{"1M\xa0", 1, 1048576ULL},	/* byte 0xA0 is _S|_SP in lib/ctype.c:34 */
};

int main(void)
{
	size_t i, bad = 0;
	for (i = 0; i < sizeof(tests) / sizeof(tests[0]); i++) {
		unsigned long long v = 0;
		int r = scrub_speed_max_store(tests[i].in, strlen(tests[i].in), &v);
		int ok = (r == 0) ? 1 : 0;
		int good = ok == tests[i].ok && (!ok || v == tests[i].val);
		if (!good)
			bad++;
		printf("%-24s store=%s value=%-22llu expected=%s%s\n",
		       tests[i].in[0] ? tests[i].in : "(empty)",
		       ok ? "OK" : "EINVAL", ok ? v : 0ULL,
		       tests[i].ok ? "OK" : "EINVAL",
		       good ? "" : "   <<< MISMATCH");
	}
	printf("total=%zu mismatches=%zu\n",
	       sizeof(tests) / sizeof(tests[0]), bad);
	return bad ? 1 : 0;
}
