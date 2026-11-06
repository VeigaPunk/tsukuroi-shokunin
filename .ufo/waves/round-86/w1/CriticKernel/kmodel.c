/* Mechanical transcription of Linux v7.2 boot-option parsing for the hibernation options.
   Sources (pinned, .ufo/waves/round-86/before/src/):
     kernel/params.c:79-95 parameqn/dash2underscore; kernel/params.c:161-212 parse_args
     init/main.c:201-228 obsolete_checksetup; init/main.c:463-476 repair_env_string;
     init/main.c:503-545 unknown_bootoption; init/main.c:1011-1017 start_kernel parse order
     lib/cmdline.c:237-284 next_arg (v7.2 upstream); lib/kstrtox.c:58-95 _parse_integer_limit
     kernel/power/hibernate.c:46 resume_file init; :1402-1465 handlers; :982-1010 find_resume_device
     block/early-lookup.c:244-253 early_lookup_bdev dispatch
   Nothing here is a kernel build: it is a transcription used to predict the parse. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>

static int noresume, nohibernate, resume_wait;
static unsigned resume_delay;
static char resume_file[256] = ""; /* CONFIG_PM_STD_PARTITION="" on the host, /proc/config.gz */

static char dash2underscore(char c){ return c=='-'?'_':c; }
static int parameqn(const char *a,const char *b,size_t n){ size_t i; for(i=0;i<n;i++) if(dash2underscore(a[i])!=dash2underscore(b[i])) return 0; return 1; }

static char *skip_spaces(char *s){ for(;;s++){ if(!*s) return s; if(!isspace(*s)) return s; } }

static char *next_arg(char *args, char **param, char **val)
{
	unsigned int i, equals = 0; int in_quote = 0, quoted = 0;
	if (*args == '"') { args++; in_quote = 1; quoted = 1; }
	for (i = 0; args[i]; i++) {
		if (isspace((unsigned char)args[i]) && !in_quote) break;
		if (equals == 0) { if (args[i] == '=') equals = i; }
		if (args[i] == '"') in_quote = !in_quote;
	}
	*param = args;
	if (!equals) *val = NULL;
	else {
		args[equals] = '\0'; *val = args + equals + 1;
		if (**val == '"') { (*val)++; if (args[i-1] == '"') args[i-1] = '\0'; }
	}
	if (quoted && i > 0 && args[i-1] == '"') args[i-1] = '\0';
	if (args[i]) { args[i] = '\0'; args += i + 1; } else args += i;
	return skip_spaces(args);
}

static void repair_env_string(char *param, char *val)
{
	if (!val) return;
	if (val == param + strlen(param) + 1) val[-1] = '=';
	else if (val == param + strlen(param) + 2) { val[-2] = '='; memmove(val-1, val, strlen(val)+1); }
	else { fprintf(stderr,"BUG repair\n"); exit(3); }
}

/* lib/kstrtox.c:58-95 as reached by simple_strntoull (lib/vsprintf.c:79-97): on overflow ULLONG_MAX. */
static unsigned long long parse_u64(const char *s)
{
	unsigned long long res = 0; int overflow = 0;
	if (*s=='0' && (s[1]=='x'||s[1]=='X')) return 0; /* base 10 is forced by "%llu" */
	for (; *s; s++) {
		unsigned int c = (unsigned char)*s, val;
		if (c>='0'&&c<='9') val=c-'0'; else break;
		if (val>=10) break;
		if (res & (~0ULL<<60)) {
			if (__builtin_mul_overflow(res,(unsigned long long)10,&res) || __builtin_add_overflow(res,(unsigned long long)val,&res)) { res=ULLONG_MAX; overflow=1; }
		} else res = res*10+val;
	}
	return res;
}

static char *SETUPS[] = {"noresume","resume_offset=","resume=","hibernate=","resumewait","resumedelay=","nohibernate",NULL};

static int r_setup(char *str){ if(noresume) return 1; strncpy(resume_file,str,255); return 1; }
static unsigned long long swsusp_resume_block;
static int o_setup(char *str){ unsigned long long o; if(noresume) return 1; if(*str>='0'&&*str<='9'){ o=parse_u64(str); swsusp_resume_block=o; } return 1; }
static int h_setup(char *str){
	if(!strncmp(str,"noresume",8)) noresume=1;
	else if(!strncmp(str,"nocompress",10)) ;
	else if(!strncmp(str,"no",2)) { noresume=1; nohibernate=1; }
	else if(!strncmp(str,"protect_image",13)) ;
	return 1;
}
static int nr_setup(char *str){ noresume=1; return 1; }
static int nh_setup(char *str){ noresume=1; nohibernate=1; return 1; }

static int obsolete_checksetup(char *line)
{
	for (int k=0; SETUPS[k]; k++) {
		int n = strlen(SETUPS[k]);
		if (parameqn(line, SETUPS[k], n)) {
			char *rest = line + n;
			if (!strcmp(SETUPS[k],"noresume")) return nr_setup(rest);
			if (!strcmp(SETUPS[k],"nohibernate")) return nh_setup(rest);
			if (!strcmp(SETUPS[k],"resume=")) return r_setup(rest);
			if (!strcmp(SETUPS[k],"resume_offset=")) return o_setup(rest);
			if (!strcmp(SETUPS[k],"hibernate=")) return h_setup(rest);
			return 1; /* resumewait / resumedelay: ignore */
		}
	}
	return 0;
}

static char *strnchr_local(const char *s, size_t n, int c){ size_t i; for(i=0;i<n;i++){ if(!s[i]) return NULL; if(s[i]==c) return (char*)(s+i);} return NULL; }

static char *unknown_bootoption(char *param, char *val)
{
	size_t len = strlen(param);
	if (!strncmp(param,"BOOT_IMAGE=",11)) return NULL;
	repair_env_string(param,val);
	if (obsolete_checksetup(param)) return NULL;
	if (strnchr_local(param,len,'.')) return NULL;   /* unused module parameter */
	return NULL;
}

/* block/early-lookup.c:244-253 dispatch: what early_lookup_bdev() would try. */
static const char *lookup_class(const char *n)
{
	if (!strncmp(n,"PARTUUID=",9)) return "devt_from_partuuid";
	if (!strncmp(n,"PARTLABEL=",10)) return "devt_from_partlabel";
	if (!strncmp(n,"/dev/",5)) return "devt_from_devname";
	return "devt_from_devnum";
}

int main(int argc, char **argv)
{
	char buf[4096], *args, *param, *val;
	unsigned long long off_before = swsusp_resume_block;
	if (argc < 2) return 2;
	/* start_kernel: parse_args("Booting kernel", static_command_line, ...) */
	strncpy(buf, argv[1], sizeof buf - 1);
	args = skip_spaces(buf);
	while (*args) {
		args = next_arg(args, &param, &val);
		if (!val && strcmp(param, "--") == 0) {
			printf("PARSE-STOP: '--' at offset -> remainder goes to init argv/env, no __setup runs\n");
			break;
		}
		unknown_bootoption(param, val);
	}
	printf("noresume=%d nohibernate=%d resume_file=\"%s\" swsusp_resume_block=%llu(0x%llx)%s\n",
	       noresume, nohibernate, resume_file, swsusp_resume_block, swsusp_resume_block,
	       off_before==swsusp_resume_block ? "" : "");
	if (noresume || nohibernate) { printf("KERNEL: hibernation unavailable / no resume attempted\n"); return 0; }
	if (!strlen(resume_file)) { printf("KERNEL: find_resume_device -> -ENOENT (hibernate.c:984): no resume\n"); return 0; }
	printf("KERNEL: find_resume_device(%s) via %s ; resume attempted there\n", resume_file, lookup_class(resume_file));
	return 0;
}
