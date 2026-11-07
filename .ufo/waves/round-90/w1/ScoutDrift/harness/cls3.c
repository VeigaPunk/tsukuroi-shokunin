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
static uint32_t st=20261106; static uint32_t xr(void){st^=st<<13;st^=st>>17;st^=st<<5;return st;}
int main(void){
  const char alpha[]=" \t\n\r\a\v\f/:a#"; size_t al=strlen(alpha);
  long trials=300000, diff=0, cls_trail=0, cls_other=0;
  for(long t=0;t<trials;t++){
    size_t n=2+(xr()%26);
    char *x=malloc(n+8);
    for(size_t i=0;i<n;i++) x[i]=alpha[xr()%al];
    /* upstream layout: file bytes f->size, buffer = f->size+2, [size-2]='\n' */
    size_t cs=n+2;
    char *a=calloc(1,cs+8), *b=calloc(1,cs+8);
    memcpy(a,x,n); memcpy(b,x,n);
    a[cs-2]='\n'; b[cs-2]='\n'; a[cs-1]='\0'; b[cs-1]='\0';
    s94(a,cs); s96(b,cs);
    size_t la=0; while(la<cs && a[la]) la++;
    size_t lb=0; while(lb<cs && b[lb]) lb++;
    if(la!=lb||memcmp(a,b,la)!=0){
      diff++;
      /* class: 94 == 96 after 94's trailing blanks (before '\n') are removed */
      char *norm=malloc(la+2); size_t k=0;
      for(size_t i=0;i<la;i++){
        if(a[i]=='\n'){ while(k>0&&(norm[k-1]==' '||norm[k-1]=='\t'))k--; norm[k++]='\n'; }
        else norm[k++]=a[i];
      }
      norm[k]=0; size_t ln=strlen(norm);
      if(ln==lb && memcmp(norm,b,ln)==0) cls_trail++;
      else { cls_other++; if(cls_other<=3){printf("OTHER in:");for(size_t i=0;i<n;i++)printf(" %02x",(unsigned char)x[i]);
        printf("\n 94:");for(size_t i=0;i<la;i++)printf(" %02x",(unsigned char)a[i]);
        printf("\n 96:");for(size_t i=0;i<lb;i++)printf(" %02x",(unsigned char)b[i]);printf("\n");} }
    }
    free(x);free(a);free(b);
  }
  printf("TRIALS %ld  DIFF %ld  class=12.9.4-keeps-trailing-blanks-before-CR %ld  class=other %ld\n",
         trials,diff,cls_trail,cls_other);
  return 0;
}
