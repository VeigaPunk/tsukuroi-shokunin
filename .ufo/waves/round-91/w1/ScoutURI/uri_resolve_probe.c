#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdnoreturn.h>
static bool optional_resource = false;
noreturn void panic(bool allow_menu, const char *fmt, ...) { (void)allow_menu; printf("PANIC("); va_list ap; va_start(ap, fmt); vprintf(fmt, ap); va_end(ap); printf(")\n"); exit(7); }
#define URI_ERROR(FMT, ...) do { if (!optional_resource) { panic(true, FMT, ##__VA_ARGS__); } printf("PRINT " FMT "\n", ##__VA_ARGS__); } while (0)
bool uri_resolve(char *uri, char **resource, char **root, char **path, char **hash) {
    #define URI_BUF_SIZE 4096
    static char buf[URI_BUF_SIZE];

    size_t length = strlen(uri) + 1;
    if (length > URI_BUF_SIZE) {
        URI_ERROR("uri_resolve: URI too long (max %u)", URI_BUF_SIZE - 1);
        return false;
    }
    memcpy(buf, uri, length);
    uri = buf;

    *resource = *root = *path = *hash = NULL;

    // Get resource
    for (size_t i = 0; ; i++) {
        if (strlen(uri + i) < 1)
            return false;

        if (!strncmp(uri + i, "(", 1)) {
            *resource = uri;
            uri[i] = 0;
            uri += i + 1;
            break;
        }
    }

    // Get root
    for (size_t i = 0; ; i++) {
        if (strlen(uri + i) < 3)
            return false;

        if (!strncmp(uri + i, "):/", 3)) {
            *root = uri;
            uri[i] = 0;
            uri += i + 3;
            break;
        }
    }

    // Get path
    if (*uri == 0)
        return false;
    *path = uri;

    // Get hash
    for (int i = (int)strlen(uri) - 1; i >= 0; i--) {
        if (uri[i] != '#') {
            continue;
        }

        uri[i++] = 0;

        if (hash != NULL) {
            *hash = uri + i;
        }

        if (strlen(uri + i) != 128) {
            URI_ERROR("Blake2b hash must be 128 characters long");
            return false;
        }

        // Validate all 128 characters are valid hexadecimal
        for (size_t j = 0; j < 128; j++) {
            char c = uri[i + j];
            if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'))) {
                URI_ERROR("Blake2b hash contains invalid character at position %d", (int)j);
                return false;
            }
        }

        break;
    }

    return true;
}
static void run(const char *label, const char *v) {
  fflush(stdout);
  char *res=NULL,*root=NULL,*path=NULL,*hash=NULL; char buf[512]; strcpy(buf,v);
  bool ok=uri_resolve(buf,&res,&root,&path,&hash);
  printf("%-24s ret=%-5s", label, ok?"true":"FALSE");
  if(ok) printf(" res=[%s] root=[%s] path=[%s] hash=%s",res,root,path,hash?hash:"(null)");
  printf("\n");
}
int main(void) {
  char H[129]; for(int i=0;i<128;i++) H[i]="0123456789abcdef"[i%16]; H[128]=0;
  char v[512];
  run("L72 host value", "boot():/EFI/BOOT/BOOTX64.EFI");
  snprintf(v,512,"boot():/EFI/a.efi#%s",H); run("good 128-hex", v);
  run("no '('", "/EFI/BOOT/BOOTX64.EFI");
  run("no '):/'", "boot()/EFI/BOOT/BOOTX64.EFI");
  run("'boot():' only", "boot():");
  run("'boot():/' empty p", "boot():/");
  snprintf(v,512,"boot():/#%s",H); run("empty path + hash", v);
  snprintf(v,512,"boot():/EFI/a.efi#abc",H); run("3-hex hash", v);
  run("hash w/ non-hex z", "boot():/EFI/a.efi#0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdefz");
  run("empty resource '():/'", "():/EFI/BOOT/BOOTX64.EFI");
  run("empty string", "");
  printf("ALL DONE\n");
  return 0;
}
