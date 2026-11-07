
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
#include <stdbool.h>
static char *config_addr; static bool config_ready=false; static bool bad_config=false;
#define SEPARATOR '\n'
#define NOT_CHILD (-1)
#define DIRECT_CHILD 0
#define INDIRECT_CHILD 1
#define panic(...) do{}while(0)
static void *ext_mem_alloc(uint64_t n){return calloc(1,n);} 
static void pmm_free(void *p,uint64_t n){(void)p;(void)n;}
static size_t s94(char *config_addr,size_t config_size){
    // remove windows carriage returns and spaces at the start and end of lines, if any
    for (size_t i = 0; i < config_size; i++) {
        size_t skip = 0;
        if (config_addr[i] == ' ' || config_addr[i] == '\t') {
            while (i + skip < config_size && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')) {
                skip++;
            }
            if (i + skip < config_size && config_addr[i + skip] == '\n') {
                goto skip_loop;
            }
            skip = 0;
        }
        while (i + skip < config_size
            && ((config_addr[i + skip] == '\r')
                || ((!i || config_addr[i - 1] == '\n') && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')))
        ) {
            skip++;
        }
skip_loop:
        if (skip) {
            for (size_t j = i; j < config_size - skip; j++)
                config_addr[j] = config_addr[j + skip];
            config_size -= skip;
            i--; // re-examine character shifted into position i
        }
    }


    return config_size;
}
static size_t s96(char *config_addr,size_t config_size){
    size_t write = 0;
    bool at_line_start = true;
    for (size_t read = 0; read < config_size - 1; read++) {
        char c = config_addr[read];

        if (c == '\r') {
            continue;
        }

        if (at_line_start && (c == ' ' || c == '\t')) {
            continue;
        }

        if (c == '\n') {
            while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) {
                write--;
            }
            at_line_start = true;
        } else {
            at_line_start = false;
        }

        config_addr[write++] = c;
    }

    while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) {
        write--;
    }
    config_addr[write++] = '\0';
    config_size = write;


    return n;
}
static bool is_directory(size_t current_depth, size_t index) {
    switch (is_child(current_depth + 1, index + 1)) {
        default:
        case NOT_CHILD:
            return false;
        case INDIRECT_CHILD:
            bad_config = true;
            panic(true, "config: Malformed config file. Parentless child.");
        case DIRECT_CHILD:
            return true;
    }
}

static char *config_get_entry_name(size_t index) {
    if (!config_ready || config_addr == NULL)
        return NULL;

    char *p = config_addr;

    for (size_t i = 0; i <= index; i++) {
        while (*p != '/') {
            if (!*p)
                return NULL;
            p++;
        }
        p++;
        if ((p - 1) != config_addr && *(p - 2) != '\n')
            i--;
    }

    p--;

    size_t len = 0;
    while (p[len] != SEPARATOR && p[len] != '\0') {
        len++;
    }

    char *ret = ext_mem_alloc(len + 1);
    memcpy(ret, p, len);
    ret[len] = 0;
    return ret;
}

static char *config_get_entry(size_t *size, size_t index) {
    if (!config_ready || config_addr == NULL)
        return NULL;

    char *ret;
    char *p = config_addr;

    for (size_t i = 0; i <= index; i++) {
        while (*p != '/') {
            if (!*p)
                return NULL;
            p++;
        }
        p++;
        if ((p - 1) != config_addr && *(p - 2) != '\n')
            i--;
    }

    do {
        p++;
    } while (*p != '\n' && *p != '\0');

    ret = p;

cont:
    while (*p != '/' && *p)
        p++;

    if (*p && *(p - 1) != '\n') {
        p++;
        goto cont;
    }

    *size = p - ret;

    return ret;
}
char *config_get_value(const char *config, size_t index, const char *key) {
    // Static buffer for return values.
    // Callers must copy the result if they need persistence across calls.
    #define CONFIG_VALUE_BUF_SIZE 4096
    static char buf[CONFIG_VALUE_BUF_SIZE];

    if (!key || !config_ready)
        return NULL;

    if (config == NULL)
        config = config_addr;

    // config_ready does not imply a config file was loaded: the blank entry
    // editor sets it with config_addr still unset.
    if (config == NULL)
        return NULL;

    size_t key_len = strlen(key);

    for (size_t i = 0; config[i]; i++) {
        if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {
            if (i && config[i - 1] != SEPARATOR)
                continue;
            if (index--)
                continue;
            i += key_len + 1;
            while (config[i] == ' ' || config[i] == '\t') {
                i++;
            }
            size_t value_len;
            for (value_len = 0;
                 config[i + value_len] != SEPARATOR && config[i + value_len];
                 value_len++);
            if (value_len >= CONFIG_VALUE_BUF_SIZE) {
                value_len = CONFIG_VALUE_BUF_SIZE - 1;
            }
            memcpy(buf, config + i, value_len);
            buf[value_len] = '\0';
            lastkey = config + i;
            return buf;
        }
    }

/* ---- upstream 12.9.4 init_config tail (verbatim) ---- */
static void init_tail_1294(void){
    config_ready=true;
    size_t s; char *c=config_get_entry(&s,0);
    if(c!=NULL){ while(*c!='/'&&c>config_addr)c--; if(*c=='/'&&c>config_addr)c[-1]=0; }
}
/* ---- upstream 12.9.6 create_menu_tree NUL placement (verbatim) ---- */
static void tree_1296(void){
    char *p=config_addr; if(!p)return;
    while(*p!='\0'){ if(*p=='/'&&(p==config_addr||*(p-1)=='\n'))break; p++; }
    if(*p=='\0')return;
    if(p>config_addr)*(p-1)='\0';
    while(*p!='\0'){
        size_t depth=0; while(*p=='/'){depth++;p++;}
        bool de=(*p=='+'); if(de)p++; while(*p==' '||*p=='\t')p++;
        char *name=p; while(*p!='\n'&&*p!='\0')p++; if(*p=='\n'){*p='\0';p++;}
        char *body="";
        if(*p!='/'){ body=p; while(*p!='\0'){ if(*p=='/'&&*(p-1)=='\n')break; p++;} if(p>body&&*(p-1)=='\n')*(p-1)='\0'; }
        (void)name;(void)body;(void)depth;(void)de;
    }
}
/* ---- r90 model: FIRST key line in the whole file ---- */
static char *model_global(const char *text,const char *key){
    size_t kl=strlen(key); const char *p=text;
    while(*p){
        const char *e=strchr(p,'\n'); size_t L=e?(size_t)(e-p):strlen(p);
        char t[512]; size_t k=0; for(size_t i=0;i<L&&k<511;i++) if(p[i]!='\r') t[k++]=p[i];
        t[k]=0; size_t s=0; while(s<k&&(t[s]==' '||t[s]=='\t'))s++;
        char *v=t+s;
        if(!strncasecmp(v,key,kl)&&v[kl]==':'){ v+=kl+1; while(*v==' '||*v=='\t')v++; return strdup(v); }
        if(!e)break; p=e+1;
    }
    return NULL;
}
static void probe(const char *label,const char *text){
    size_t n=strlen(text);
    config_addr=calloc(1,n+8); memcpy(config_addr,text,n); config_addr[n]='\n'; config_addr[n+1]='\0';
    s94(config_addr,n+2); init_tail_1294();
    char *a=config_get_value(NULL,0,"HASH_MISMATCH_PANIC"); char *m94=a?strdup(a):NULL;
    config_addr=calloc(1,n+8); memcpy(config_addr,text,n); config_addr[n]='\n'; config_addr[n+1]='\0';
    s96(config_addr,n+2); tree_1296();
    char *b=config_get_value(NULL,0,"HASH_MISMATCH_PANIC"); char *m96=b?strdup(b):NULL;
    char *mm=model_global(text,"HASH_MISMATCH_PANIC");
    printf("  %s\n", label);
    printf("    r90 model (whole file)    : %s\n", mm?mm:"(absent)");
    printf("    upstream v12.9.4 (global) : %s\n", m94?m94:"(absent)");
    printf("    upstream v12.9.6 (global) : %s\n", m96?m96:"(absent)");
    int u_same = (!!m94==!!m96)&&(!m94||!m96||strcmp(m94,m96)==0);
    int m94s = (!!mm==!!m94)&&(!mm||!m94||strcmp(mm,m94)==0);
    int m96s = (!!mm==!!m96)&&(!mm||!m96||strcmp(mm,m96)==0);
    printf("    upstream 12.9.4 == upstream 12.9.6 : %s\n", u_same?"YES":"NO  *** CHANGED ***");
    printf("    r90 model == upstream v12.9.4 : %s   r90 model == upstream v12.9.6 : %s\n\n",
           m94s?"YES":"NO ", m96s?"YES":"NO ");
    free(m94);free(m96);free(mm);
}
int main(void){
    probe("A) global option BEFORE the first entry (ordinary config)",
          "timeout: 5\nhash_mismatch_panic: no\n/entry1\nprotocol: efi\n");
    probe("B) FIRST LINE IS an entry; the option sits inside that entry",
          "/entry1\nprotocol: efi\nhash_mismatch_panic: no\n");
    probe("C) option ONLY inside an entry (a global line precedes it)",
          "timeout: 5\n/entry1\nprotocol: efi\nhash_mismatch_panic: no\n");
    return 0;
}
