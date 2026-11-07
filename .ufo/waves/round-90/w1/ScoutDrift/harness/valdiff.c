#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static size_t s94(char *config_addr, size_t config_size){
#include "strip94.c.body"
    return config_size;
}
static size_t s96(char *config_addr, size_t config_size){
#include "strip96.c.body"
    return config_size;
}
/* r90 model value: per physical line -> raw.replace("\r","") then .strip(" \t"),
   then take after ':' and lstrip(" \t"). */
static void model_val(const char *line, char *out) {
    char t[512]; size_t k=0,L=strlen(line);
    for(size_t i=0;i<L;i++) if(line[i]!='\r') t[k++]=line[i];
    t[k]=0; size_t s=0,e=k;
    while(s<e&&(t[s]==' '||t[s]=='\t'))s++;
    while(e>s&&(t[e-1]==' '||t[e-1]=='\t'))e--;
    memmove(t,t+s,e-s); t[e-s]=0;
    char *c=strchr(t,':'); if(!c){out[0]=0;return;}
    c++; while(*c==' '||*c=='\t')c++;
    snprintf(out,512,"%s",c);
}
static void upstream_val(const char *buf, char *out) {
    char *c=strchr(buf,':'); if(!c){out[0]=0;return;}
    c++; while(*c==' '||*c=='\t')c++;
    size_t l=strcspn(c,"\n"); memcpy(out,c,l); out[l]=0;
}
static uint32_t st=7; static uint32_t xr(void){st^=st<<13;st^=st>>17;st^=st<<5;return st;}
int main(void){
    const char *keys[]={"path","kernel_path","image_path","module_path","dtb_path","global_dtb","wallpaper","term_font","hash_mismatch_panic","measured_boot","protocol"};
    const char *vals[]={"boot():/rel#HASH","no","yes","efi","boot():/x#HASH"};
    long t_lf=0,t_crlf=0,d94_lf=0,d96_lf=0,d94_crlf=0,d96_crlf=0;
    for(long t=0;t<200000;t++){
        char kb[32],vb[64];
        snprintf(kb,sizeof kb,"%s",keys[xr()%11]);
        snprintf(vb,sizeof vb,"%s",vals[xr()%5]);
        int lead=xr()%4, sp=xr()%3, trail=xr()%4, crlf=xr()%2;
        char line[512]; size_t o=0;
        for(int i=0;i<lead;i++) line[o++]=(xr()&1)?' ':'\t';
        o+=snprintf(line+o,sizeof(line)-o,"%s:",kb);
        for(int i=0;i<sp;i++) line[o++]=(xr()&1)?' ':'\t';
        o+=snprintf(line+o,sizeof(line)-o,"%s",vb);
        for(int i=0;i<trail;i++) line[o++]=(xr()&1)?' ':'\t';
        if(crlf){line[o++]='\r';line[o++]='\n';} else line[o++]='\n';
        /* upstream buffer: file bytes + '\n' + '\0' */
        size_t cs=o+2;
        char *a=calloc(1,cs+8),*b=calloc(1,cs+8);
        memcpy(a,line,o);memcpy(b,line,o);
        a[cs-2]='\n';b[cs-2]='\n';a[cs-1]='\0';b[cs-1]='\0';
        s94(a,cs); s96(b,cs);
        char mv[512],v94[512],v96[512];
        char content[512]; size_t clen=o;
        if (clen && line[clen-1]=='\n') clen--;
        if (clen && line[clen-1]=='\r') clen--;
        memcpy(content,line,clen); content[clen]=0;
        model_val(content,mv); upstream_val(a,v94); upstream_val(b,v96);
        int e94=strcmp(mv,v94)!=0, e96=strcmp(mv,v96)!=0;
        if(crlf){t_crlf++; if(e94)d94_crlf++; if(e96)d96_crlf++;}
        else     {t_lf++;   if(e94)d94_lf++;   if(e96)d96_lf++;}
        free(a);free(b);
    }
    printf("r90 R1 model vs upstream, key-line VALUE (after ':'), 200000 trials:\n");
    printf("  LF  lines : %ld   model!=12.9.4 : %ld (%.3f%%)   model!=12.9.6 : %ld (%.3f%%)\n",
           t_lf,d94_lf,100.0*d94_lf/t_lf,d96_lf,100.0*d96_lf/t_lf);
    printf("  CRLF lines: %ld   model!=12.9.4 : %ld (%.3f%%)   model!=12.9.6 : %ld (%.3f%%)\n",
           t_crlf,d94_crlf,100.0*d94_crlf/t_crlf,d96_crlf,100.0*d96_crlf/t_crlf);
    return 0;
}
