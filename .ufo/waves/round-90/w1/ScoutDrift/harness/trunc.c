/* Byte-level: what does upstream v12.9.4's init_config tail leave readable as the
   "global" region of config_addr? Uses upstream's verbatim config_get_entry + the
   verbatim init_config tail (config.c raw 640-650). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
static char *config_addr; static bool config_ready=false;
#define SEPARATOR '\n'
static void *ext_mem_alloc(uint64_t n){return calloc(1,n);} 
static void pmm_free(void *p,uint64_t n){free(p);}
static char *config_get_entry(size_t *size,size_t index){
    if(!config_ready||config_addr==NULL)return NULL; char *ret; char *p=config_addr;
    for(size_t i=0;i<=index;i++){ while(*p!='/'){if(!*p)return NULL;p++;} p++; if((p-1)!=config_addr&&*(p-2)!='\n')i--; }
    do{p++;}while(*p!='\n'&&*p!='\0'); ret=p;
cont: while(*p!='/'&&*p)p++; if(*p&&*(p-1)!='\n'){p++;goto cont;} *size=p-ret; return ret;
}
static void init_tail_1294(void){
    config_ready=true;
    size_t s; char *c=config_get_entry(&s,0);
    if(c!=NULL){ while(*c!='/'&&c>config_addr)c--; if(*c=='/'&&c>config_addr)c[-1]=0; }
}
static void probe(const char *label,const char *text){
    size_t n=strlen(text);
    config_addr=calloc(1,n+8); memcpy(config_addr,text,n); config_addr[n]='\n'; config_addr[n+1]='\0';
    init_tail_1294();
    printf("  %s\n    config_addr after init_config (upstream v12.9.4) = \"", label);
    for(size_t i=0;config_addr[i];i++){ unsigned char c=config_addr[i];
        if(c=='\n')printf("\\n"); else if(c==' ')printf("_"); else putchar(c);} printf("\"\n");
}
int main(void){
    probe("A) global line then entry", "timeout: 5\nhash_mismatch_panic: no\n/entry1\nprotocol: efi\n");
    probe("B) FIRST LINE is an entry", "/entry1\nprotocol: efi\nhash_mismatch_panic: no\n");
    probe("C) global line, option inside entry", "timeout: 5\n/entry1\nprotocol: efi\nhash_mismatch_panic: no\n");
    return 0;
}
