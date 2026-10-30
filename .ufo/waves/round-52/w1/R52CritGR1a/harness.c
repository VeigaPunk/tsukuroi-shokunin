#include <stdio.h>
#include <string.h>
#include <limits.h>
typedef unsigned long long u64; typedef unsigned int u32;
#define likely(x) __builtin_expect(!!(x),1)
#define unlikely(x) __builtin_expect(!!(x),0)
#define noinline __attribute__((noinline))
#define fallthrough __attribute__((fallthrough))
#define KSTRTOX_OVERFLOW (1U << (8*sizeof(unsigned long)-2))
static inline unsigned int ktolower(unsigned int c){ return c>='A'&&c<='Z'?c+('a'-'A'):c; }
#define _tolower(x) ktolower(x)
static inline int isxdigit_(unsigned int c){ return (c>='0'&&c<='9')||(c>='a'&&c<='f')||(c>='A'&&c<='F'); }
#define isxdigit(x) isxdigit_(x)
static inline int isspace_(int c){ return c==' '||c=='\t'||c=='\n'||c=='\r'||c=='\v'||c=='\f'; }
#define isspace(x) isspace_(x)
static inline int check_shl_overflow(u64 a, unsigned int s, u64 *d){ u64 t; if(__builtin_mul_overflow(a,(u64)1<<s,&t)){*d=t;return 1;} *d=t; return 0; }
static inline int check_mul_overflow(u64 a,u64 b,u64 *d){ return __builtin_mul_overflow(a,b,d); }
static inline int check_add_overflow(u64 a,u64 b,u64 *d){ return __builtin_add_overflow(a,b,d); }
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
noinline
unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)
{
	return simple_strntoull(cp, endp, base, INT_MAX);
}
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

static char *skip_spaces(const char *str){ while(isspace((unsigned char)*str)) str++; return (char*)str; }
static const char *store(const char *buf){
    char *endptr; u64 limit;
    limit = memparse(buf, &endptr);
    endptr = skip_spaces(endptr);
    if (*endptr != 0) return "EINVAL";
    return "OK";
}
static const char *store_nl_only(const char *buf){
    char *endptr; u64 limit;
    limit = memparse(buf, &endptr);
    while (*endptr == '\n') endptr++;
    if (*endptr != 0) return "EINVAL";
    return "OK";
}
int main(void){
    const char *cases[] = {"100M","100m","010","0x10","10MB","10 M","-1","\n","100\n","0x","0X10","0K","K","M","08","1K","1M","0x1f","10G","1E","18446744073709551615K","99999999999999999999999K","  10","10 ","","0x1","0b101","10\0junk","0xdeadbeef"};
    for (unsigned i=0;i<sizeof(cases)/sizeof(*cases);i++){
        const char *c=cases[i];
        u64 v; char *e;
        v = memparse(c,&e);
        printf("%-26s memparse=%-22llu rest=\"%s\"  store(isspace)=%-7s store(nl-only)=%s\n",
            (c[0]=='\n'?"<newline>":(c[0]=='\0'?"<NUL>":c)), v, e, store(c), store_nl_only(c));
    }
    return 0;
}
