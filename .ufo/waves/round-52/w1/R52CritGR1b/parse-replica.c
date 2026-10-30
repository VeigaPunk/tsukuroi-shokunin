#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>
#include <stdint.h>
#define KSTRTOX_OVERFLOW (1U<<31)
#define unlikely(x) (x)
#define likely(x) (x)
static int ktolower(int c){ return tolower(c); }
static int check_shl_overflow(unsigned long long a, unsigned int s, unsigned long long *b){ if (s<64 && a <= (ULLONG_MAX>>s)) { *b = a << s; return 0; } *b=ULLONG_MAX; return 1; }
static int _unused_cso(unsigned long long a, unsigned int s, unsigned long long *b){
    if (s>=64 || a > (ULLONG_MAX>>s)) { *b=ULLONG_MAX; return 1;} return 0;}
static const char *_parse_integer_fixup_radix(const char *s, unsigned int *base){
    if (*base == 0) { if (s[0]=='0') { if (ktolower(s[1])=='x' && isxdigit(s[2])) *base=16; else *base=8; } else *base=10; }
    if (*base==16 && s[0]=='0' && ktolower(s[1])=='x') s+=2;
    return s;
}
static unsigned int _parse_integer_limit(const char *s, unsigned int base, unsigned long long *p, size_t max_chars){
    unsigned int rv, overflow=0; unsigned long long res=0;
    for (rv=0; rv<max_chars; rv++, s++) { unsigned int c=*s, lc=ktolower(c), val;
        if ('0'<=c && c<='9') val=c-'0'; else if ('a'<=lc && lc<='f') val=lc-'a'+10; else break;
        if (val>=base) break;
        res = res*base + val; }
    *p=res; return rv|overflow;
}
static unsigned long long simple_strntoull(const char *startp, char **endp, unsigned int base, size_t max_chars){
    const char *cp; unsigned long long result=0ULL; size_t prefix_chars; unsigned int rv;
    cp=_parse_integer_fixup_radix(startp,&base); prefix_chars=cp-startp;
    if (prefix_chars<max_chars){ rv=_parse_integer_limit(cp,base,&result,max_chars-prefix_chars); cp += (rv & ~KSTRTOX_OVERFLOW);} else cp=startp+max_chars;
    if (endp) *endp=(char*)cp; return result;
}
static unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base){ return simple_strntoull(cp,endp,base,INT_MAX); }
static unsigned long long memparse(const char *ptr, char **retptr){
    char *endptr; unsigned long long ret=simple_strtoull(ptr,&endptr,0); unsigned int shl=0;
    switch (*endptr){
    case 'E': case 'e': shl+=10; /*fallthrough*/
    case 'P': case 'p': shl+=10; /*fallthrough*/
    case 'T': case 't': shl+=10; /*fallthrough*/
    case 'G': case 'g': shl+=10; /*fallthrough*/
    case 'M': case 'm': shl+=10; /*fallthrough*/
    case 'K': case 'k': shl+=10; /*fallthrough*/
    default: break; }
    if (shl && likely(ptr!=endptr)) { if (unlikely(check_shl_overflow(ret,shl,&ret))) ret=ULLONG_MAX; endptr++; }
    if (retptr) *retptr=endptr; return ret;
}
static char *skip_spaces(const char *str){ while (*str && isspace((unsigned char)*str)) str++; return (char*)str; }
int main(void){
    const char *cases[] = {"0x1E","0x1e","100M","100m","010","0x10","0X10","10MB","10 M","-1","\n","","K","0K","1G","1T","1P","1E","0x1A","0x","10", NULL};
    for (int i=0; cases[i]; i++){
        char *endptr=NULL; unsigned long long v=memparse(cases[i],&endptr);
        char *e2=skip_spaces(endptr);
        int accepted = (*e2==0);
        printf("%-8s value=%-14llu raw_end=[%s] after_skip=[%s] %s\n",
            cases[i][0]?cases[i]:"(empty)", v, endptr, e2, accepted?"ACCEPT":"EINVAL");
    }
    return 0;
}
