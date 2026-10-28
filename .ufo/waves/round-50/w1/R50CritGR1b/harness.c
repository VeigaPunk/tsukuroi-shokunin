#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>

#define KSTRTOX_OVERFLOW (1u << 31)
static int my_tolower(int c){ return tolower(c); }
static const char *_parse_integer_fixup_radix(const char *s, unsigned int *base){
  if (*base == 0) { if (s[0]=='0'){ if(my_tolower(s[1])=='x' && isxdigit((unsigned char)s[2])) *base=16; else *base=8; } else *base=10; }
  if (*base==16 && s[0]=='0' && my_tolower(s[1])=='x') s+=2;
  return s;
}
static unsigned int _parse_integer_limit(const char *s, unsigned int base, unsigned long long *p, size_t max_chars){
  unsigned int rv, overflow=0; unsigned long long res=0;
  for (rv=0; rv<max_chars; rv++, s++){
    unsigned int c=*s, lc=my_tolower(c), val;
    if ('0'<=c&&c<='9') val=c-'0';
    else if ('a'<=lc&&lc<='f') val=lc-'a'+10;
    else break;
    if (val>=base) break;
    if (res & (~0ull << 60)) { if (__builtin_mul_overflow(res,(unsigned long long)base,&res)||__builtin_add_overflow(res,(unsigned long long)val,&res)){res=ULLONG_MAX;overflow=KSTRTOX_OVERFLOW;} }
    else res = res*base+val;
  }
  *p=res; return rv|overflow;
}
static unsigned long long simple_strntoull(const char *startp, char **endp, unsigned int base, size_t max_chars){
  const char *cp; unsigned long long result=0; size_t prefix_chars; unsigned int rv;
  cp=_parse_integer_fixup_radix(startp,&base); prefix_chars=cp-startp;
  if (prefix_chars<max_chars){ rv=_parse_integer_limit(cp,base,&result,max_chars-prefix_chars); cp+=(rv&~KSTRTOX_OVERFLOW);} else cp=startp+max_chars;
  if (endp) *endp=(char*)cp; return result;
}
static unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base){ return simple_strntoull(cp,endp,base,INT_MAX); }
static int check_shl_overflow(unsigned long long a, unsigned int s, unsigned long long *r){ if(!s){*r=a;return 0;} return __builtin_mul_overflow(a,1ULL<<s,r); }
static unsigned long long memparse(const char *ptr, char **retptr){
  char *endptr; unsigned long long ret=simple_strtoull(ptr,&endptr,0); unsigned int shl=0;
  switch(*endptr){ case 'E': case 'e': shl+=10; /*fall*/ case 'P': case 'p': shl+=10; case 'T': case 't': shl+=10;
  case 'G': case 'g': shl+=10; case 'M': case 'm': shl+=10; case 'K': case 'k': shl+=10; default: break; }
  if (shl && ptr!=endptr){ if (check_shl_overflow(ret,shl,&ret)) ret=ULLONG_MAX; endptr++; }
  if (retptr) *retptr=endptr; return ret;
}
/* store: buf is NUL-terminated as sysfs guarantees */
static int store(const char *buf, unsigned long long *out){
  char *endptr; unsigned long long limit=memparse(buf,&endptr);
  while (*endptr && isspace((unsigned char)*endptr)) endptr++;   /* skip_spaces */
  if (*endptr!=0) return -22; /* -EINVAL */
  *out=limit; return 0;
}
int main(void){
  const char *cases[]={"100M","100m","010","0x10","10MB","10 M","-1","\n","0","0K","M","0X10"," 10","10\n","0x","99999999999999999999999K"};
  for (unsigned i=0;i<sizeof(cases)/sizeof(*cases);i++){
    unsigned long long v=0; int rc=store(cases[i],&v);
    if (rc) printf("%-30s -> EINVAL\n", cases[i][0]=='\n'?"<bare newline>":cases[i]);
    else printf("%-30s -> accepted value=%llu\n", cases[i][0]=='\n'?"<bare newline>":cases[i], v);
  }
  return 0;
}
