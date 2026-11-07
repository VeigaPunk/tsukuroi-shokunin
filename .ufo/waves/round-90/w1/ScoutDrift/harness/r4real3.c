
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
#include <stdbool.h>
#define URI_ERROR(...) do { } while (0)
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

int main(void){
    char H[129]; for(int i=0;i<128;i++) H[i]='a'; H[128]=0;
    const char *names[] = {"boot():/x#H","():/x#H","hdd(0:1):/x#H","bogus:/x#H","$boot():/x#H",
                           "$$boot():/x#H","BOOT():/x#H","boot(2):/x#H","boot():/x#H","Boot():/x#H"};
    int nullhits=0, okhits=0;
    for (unsigned k=0;k<sizeof(names)/sizeof(names[0]);k++){
        char uri[256];
        const char *n=names[k];
        size_t pre=strlen(n)-3;                 /* strip the "#H" tail */
        snprintf(uri,sizeof uri,"%.*s%s",(int)pre,n,H);
        char *r=NULL,*ro=NULL,*pa=NULL,*h=NULL;
        bool ok = uri_resolve(uri,&r,&ro,&pa,&h);
        printf("  uri_resolve(\"%-22s\") -> %-5s  resource=%s%s%s\n", n, ok?"true":"false",
               r?"\"":"(NULL)", r?r:"", r?"\"":"");
        if(ok){ okhits++; if(r==NULL) nullhits++; }
    }
    printf("  => successful resolves: %d ; resource==NULL among them: %d  => \"No resource specified\" branch %s\n",
           okhits, nullhits, nullhits?"REACHABLE":"UNREACHABLE (dead code) in v12.9.4");
    return 0;
}
