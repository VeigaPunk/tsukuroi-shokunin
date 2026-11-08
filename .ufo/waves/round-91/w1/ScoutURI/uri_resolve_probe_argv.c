#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdnoreturn.h>
static bool optional_resource = false;
noreturn void panic(bool m, const char *f, ...){ (void)m; va_list a; va_start(a,f); vprintf(f,a); va_end(a); printf("\n"); exit(9);} 
#define URI_ERROR(FMT, ...) do { if (!optional_resource) { panic(true, FMT, ##__VA_ARGS__); } printf("PRINT-ONLY " FMT "\n", ##__VA_ARGS__); } while (0)
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
int main(int argc, char **argv){
  char *res=NULL,*root=NULL,*path=NULL,*hash=NULL;
  bool ok=uri_resolve(argv[1],&res,&root,&path,&hash);
  printf("%d|%s|%s|%s|%s\n", ok?1:0, res?res:"", root?root:"", path?path:"", hash?hash:"NULL");
  return 0;
}
