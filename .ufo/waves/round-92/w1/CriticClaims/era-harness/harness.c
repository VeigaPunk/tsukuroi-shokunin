#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
const char *current_arch(void){return "x86_64";}
const char *current_firmware(void){return "uefi";}
const char *loader_arch(void){return "x86_64";}
bool secure_boot_active = false;
bool editor_enabled = true;


void panic(bool x, const char *fmt, ...){(void)x;(void)fmt;}
int digit_to_int(char c){ if(c>='0'&&c<='9')return c-'0'; if(c>='a'&&c<='f')return c-'a'+10; if(c>='A'&&c<='F')return c-'A'+10; return -1; }
bool case_insensitive_fopen = false;
struct file_handle *limine_fopen(struct volume *p, const char *path){(void)p;(void)path;return NULL;}
void limine_fclose(struct file_handle *f){(void)f;}
size_t limine_fread(struct file_handle *f, void *b, size_t o, size_t c){(void)f;(void)b;(void)o;(void)c;return 0;}
int init_config(size_t config_size);
char *config_get_value(const char *config, size_t index, const char *key);
void harness_set_addr(char *p, size_t sz);
int main(int argc, char **argv){
    if(argc<2){fprintf(stderr,"usage: harness conf [key...]\n");return 2;}
    FILE *f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
    fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
    size_t size=(size_t)n+2;
    char *buf=calloc(1,size); if(!buf)return 2;
    if(fread(buf,1,(size_t)n,f)!=(size_t)n){perror("read");return 2;}
    fclose(f);
    buf[n]='\n'; buf[n+1]='\0';
    harness_set_addr(buf,size);
    init_config(size);
    printf("{\"keys\":{");
    for(int i=2;i<argc;i++){
        const char *v=config_get_value(NULL,0,argv[i]);
        printf("%s\"%s\":", i>2?",":"", argv[i]);
        if(v) printf("\"%s\"", v); else printf("null");
    }
    printf("}, \"first_bytes\": \"");
    extern char *config_addr;
    for(int i=0;i<40 && config_addr[i];i++){ unsigned char c=config_addr[i]; if(c=='\n')printf("\\n"); else if(c>=32&&c<127)printf("%c",c); else printf("\\x%02x",c);}
    printf("\"}\n");
    return 0;
}
struct smbios_entry_point_64 *smbios_entry_64;
struct smbios_entry_point_32 *smbios_entry_32;
void acpi_get_smbios(void **a, void **b){(void)a;(void)b;}
void *smbios_get_table(uint64_t a, size_t s){(void)a;(void)s;return NULL;}
