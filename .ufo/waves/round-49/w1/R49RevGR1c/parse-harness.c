#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>
#undef _tolower
#undef isxdigit
typedef unsigned long long u64;
#define KSTRTOX_OVERFLOW (1U << 31)
#define _tolower(c) ((c) | 0x20)
#define isxdigit(c) isxdigit((unsigned char)(c))
static int check_shl_overflow_(u64 a, unsigned int s, u64 *d){
  if (s >= 64) { *d = 0; return a != 0; }
  *d = a << s;
  return (a >> (64 - s)) != 0;
}
#define check_shl_overflow(a,s,d) check_shl_overflow_((a),(s),(d))
#define check_mul_overflow(a,b,d) __builtin_mul_overflow((a),(b),(d))
#define check_add_overflow(a,b,d) __builtin_add_overflow((a),(b),(d))
static char *skip_spaces(const char *str){ while (isspace((unsigned char)*str)) ++str; return (char *)str; }
#define likely(x) (x)
#define unlikely(x) (x)
#define noinline __attribute__((noinline))
#define EXPORT_SYMBOL(x)
#define fallthrough __attribute__((fallthrough))
#include "radix.inc"
#include "parseint.inc"
#include "fns.inc"
#include "memparse.inc"
/* faithful copy of btrfs_devinfo_scrub_speed_max_store's parse+validate (sysfs.c:2037-2046) */
static long store(const char *buf, u64 *out){
  char *endptr; u64 limit;
  limit = memparse(buf, &endptr);
  endptr = skip_spaces(endptr);
  if (*endptr != 0) return -22; /* -EINVAL */
  *out = limit;
  return (long)strlen(buf);
}
int main(void){
  const char *in[] = {"100M","100m","010","0x10","0X10","10MB","10 M","-1","\n","100M\n","","0","00","08","1k","1K","1E","1P","17592186044416E","18446744073709551615K","0x","0xK"," 10M","1 ","+1","0x1f","5G"};
  for (unsigned i=0;i<sizeof(in)/sizeof(*in);i++){
    u64 v=0; long r=store(in[i],&v);
    printf("%-26s -> %s", (i==8?"\"\\n\"":(in[i][0]?in[i]:"\"\"")), r<0?"EINVAL":(r==0?"accepted(empty)":r>0?"ok":"?"));
    if (r>=0) printf(" limit=%llu", v);
    printf("\n");
  }
  return 0;
}
