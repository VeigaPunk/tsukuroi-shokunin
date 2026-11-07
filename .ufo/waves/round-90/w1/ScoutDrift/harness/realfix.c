#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
static size_t s94(char *config_addr, size_t config_size){
#include "strip94.c.body"
    return config_size;
}
static size_t s96(char *config_addr, size_t config_size){
#include "strip96.c.body"
    return config_size;
}
static char *get_value(const char *cfg, const char *key) {
    size_t klen = strlen(key);
    for (size_t i = 0; cfg[i]; i++) {
        if (!strncasecmp(&cfg[i], key, klen) && cfg[i+klen] == ':') {
            if (i && cfg[i-1] != '\n') continue;
            i += klen + 1;
            while (cfg[i]==' '||cfg[i]=='\t') i++;
            size_t vl=0; while (cfg[i+vl] != '\n' && cfg[i+vl]) vl++;
            char *o=malloc(vl+1); memcpy(o,&cfg[i],vl); o[vl]=0; return o;
        }
    }
    return NULL;
}
/* upstream uri_resolve hash rules (12.9.4 and 12.9.6 identical) */
static int hash_len_check(const char *v) {
    const char *lp = strchr(v, '('); if(!lp) return -1;
    const char *rp = strstr(lp, "):/"); if(!rp) return -1;
    const char *tail = rp+3; const char *h = strrchr(tail, '#'); if(!h) return -1;
    int len = 0; for (const char *p=h+1; *p; p++) len++;
    return len;  /* 128 => OK */
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    static char buf[1<<16];
    size_t n = fread(buf, 1, sizeof buf - 2, f); fclose(f);
    size_t cs = n + 2;
    char *a = calloc(1, cs+8), *b = calloc(1, cs+8);
    memcpy(a, buf, n); memcpy(b, buf, n);
    a[cs-2]='\n'; b[cs-2]='\n'; a[cs-1]='\0'; b[cs-1]='\0';
    s94(a, cs); s96(b, cs);
    char *v94 = get_value(a, "PATH"), *v96 = get_value(b, "PATH");
    /* gate model: per line, remove CR, strip blanks both ends */
    char *g = strdup(buf); for(char*q=g;*q;q++) if(*q=='\r') *q=' ';
    char *gv=NULL, *save=strdup(g);
    for(char *ln=strtok(save,"\n"); ln; ln=strtok(NULL,"\n")) {
        char *t=strdup(ln); size_t L=strlen(t);
        while(L&&(t[0]==' '||t[0]=='\t')){memmove(t,t+1,L);L--;}
        while(L&&(t[L-1]==' '||t[L-1]=='\t'))t[--L]=0;
        char *c=strchr(t,':'); if(c){char*v=c+1;while(*v==' '||*v=='\t')v++;gv=strdup(v);} free(t);
    }
    printf("upstream v12.9.4 : PATH value hash-length = %d  => %s\n", hash_len_check(v94),
           hash_len_check(v94)==128 ? "hash OK (LP-MISMATCH/OK)" : "URI_ERROR 'hash must be 128 characters long' -> PANIC");
    printf("upstream v12.9.6 : PATH value hash-length = %d  => %s\n", hash_len_check(v96),
           hash_len_check(v96)==128 ? "hash OK (LP-MISMATCH/OK)" : "URI_ERROR -> PANIC");
    printf("gate/battery model: PATH value hash-length = %d  => %s\n", hash_len_check(gv),
           hash_len_check(gv)==128 ? "hash OK (LP-MISMATCH/OK)" : "hash-format error");
    printf("\n94 value tail: %s\n96 value tail: %s\nmodel value tail: %s\n",
           v94+strlen(v94)-6, v96+strlen(v96)-6, gv+strlen(gv)-6);
    return 0;
}
