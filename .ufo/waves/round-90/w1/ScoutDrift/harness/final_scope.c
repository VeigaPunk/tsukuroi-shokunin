/* FINAL decisive harness.
   - upstream v12.9.4: verbatim strip loop (raw 528-551) + verbatim config_get_entry /
     config_get_value + verbatim init_config tail (the c[-1]=0 truncation).
   - upstream v12.9.6: verbatim strip loop (raw 551-580) + verbatim create_menu_tree NUL
     placement + verbatim config_get_value.
   - r90 model: per physical line, remove every CR, strip blanks at both ends, first
     key line in the WHOLE FILE.
   Reports, for each config shape, what each sees as the GLOBAL hash_mismatch_panic. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
#include <stdbool.h>
static char *config_addr; static bool config_ready=false;
#define SEPARATOR '\n'
static void *ext_mem_alloc(uint64_t n){return calloc(1,n);} 
static void pmm_free(void *p,uint64_t n){free(p);}
static size_t s94(char *config_addr, size_t config_size){
#include "strip94.c.body"
    return config_size;
}
static size_t s96(char *config_addr, size_t config_size){
#include "strip96.c.body"
    return config_size;
}
/* ---- upstream v12.9.4 ---- */
static char *config_get_entry(size_t *size,size_t index){
    if(!config_ready||config_addr==NULL)return NULL; char *ret; char *p=config_addr;
    for(size_t i=0;i<=index;i++){ while(*p!='/'){if(!*p)return NULL;p++;} p++; if((p-1)!=config_addr&&*(p-2)!='\n')i--; }
    do{p++;}while(*p!='\n'&&*p!='\0'); ret=p;
cont: while(*p!='/'&&*p)p++; if(*p&&*(p-1)!='\n'){p++;goto cont;} *size=p-ret; return ret;
}
static char *cgv(const char *config,size_t index,const char *key){
    static char buf[4096];
    if(!key||!config_ready)return NULL; if(config==NULL)config=config_addr; if(config==NULL)return NULL;
    size_t kl=strlen(key);
    for(size_t i=0;config[i];i++){
        if(!strncasecmp(&config[i],key,kl)&&config[i+kl]==':'){
            if(i&&config[i-1]!=SEPARATOR)continue; if(index--)continue;
            i+=kl+1; while(config[i]==' '||config[i]=='\t')i++;
            size_t vl=0; while(config[i+vl]!=SEPARATOR&&config[i+vl])vl++;
            if(vl>=4096)vl=4095; memcpy(buf,config+i,vl); buf[vl]=0; return buf;
        }
    }
    return NULL;
}
static void init_tail_1294(void){
    config_ready=true;
    size_t s; char *c=config_get_entry(&s,0);
    if(c!=NULL){ while(*c!='/'&&c>config_addr)c--; if(*c=='/'&&c>config_addr)c[-1]=0; }
}
/* ---- upstream v12.9.6 ---- */
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
/* ---- r90 model: first key line in the whole file ---- */
static char *model_global(const char *text,const char *key){
    const char *p=text; size_t kl=strlen(key);
    while(*p){
        const char *e=strchr(p,'\n'); size_t L=e?(size_t)(e-p):strlen(p);
        char t[512]; size_t k=0; for(size_t i=0;i<L&&k<511;i++) if(p[i]!='\r') t[k++]=p[i];
        t[k]=0;
        size_t s=0; while(s<k&&(t[s]==' '||t[s]=='\t'))s++;
        char *v=t+s; if(!strncasecmp(v,key,kl)&&v[kl]==':'){ v+=kl+1; while(*v==' '||*v=='\t')v++; return strdup(v); }
        if(!e)break; p=e+1;
    }
    return NULL;
}
static void probe(const char *label,const char *text){
    size_t n=strlen(text);
    config_addr=calloc(1,n+8); memcpy(config_addr,text,n); config_addr[n]='\n'; config_addr[n+1]='\0';
    s94(config_addr,n+2); config_ready=false; init_tail_1294();
    char *a=cgv(NULL,0,"HASH_MISMATCH_PANIC"); char *m94=a?strdup(a):NULL;
    config_addr=calloc(1,n+8); memcpy(config_addr,text,n); config_addr[n]='\n'; config_addr[n+1]='\0';
    s96(config_addr,n+2); config_ready=true; tree_1296();
    char *b=cgv(NULL,0,"HASH_MISMATCH_PANIC"); char *m96=b?strdup(b):NULL;
    char *mm=model_global(text,"HASH_MISMATCH_PANIC");
    printf("  %s\n", label);
    printf("    r90 model (whole file)      : %s\n", mm?mm:"(absent)");
    printf("    upstream v12.9.4 (global)   : %s\n", m94?m94:"(absent)");
    printf("    upstream v12.9.6 (global)   : %s\n", m96?m96:"(absent)");
    int same94 = (!!mm==!!m94)&&(!mm||!m94||strcmp(mm,m94)==0);
    int same96 = (!!mm==!!m96)&&(!mm||!m96||strcmp(mm,m96)==0);
    printf("    model==12.9.4: %s   model==12.9.6: %s   upstream12.9.4==12.9.6: %s\n\n",
        same94?"YES":"NO ", same96?"YES":"NO ",
        ((!!m94==!!m96)&&(!m94||!m96||strcmp(m94,m96)==0))?"YES":"NO ");
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
