/* Faithful transcription of Limine v12.9.4 common/lib/uri.c uri_resolve (raw 32-107).
 * Prints the four out-parameters, or "FALSE" (the silent-false paths). */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#define URI_BUF_SIZE 4096
static bool uri_resolve(char *uri, char **resource, char **root, char **path, char **hash) {
    static char buf[URI_BUF_SIZE];
    size_t length = strlen(uri) + 1;
    if (length > URI_BUF_SIZE) return false;
    memcpy(buf, uri, length);
    uri = buf;
    *resource = *root = *path = *hash = NULL;
    for (size_t i = 0; ; i++) {
        if (strlen(uri + i) < 1) return false;
        if (!strncmp(uri + i, "(", 1)) { *resource = uri; uri[i] = 0; uri += i + 1; break; }
    }
    for (size_t i = 0; ; i++) {
        if (strlen(uri + i) < 3) return false;
        if (!strncmp(uri + i, "):/", 3)) { *root = uri; uri[i] = 0; uri += i + 3; break; }
    }
    if (*uri == 0) return false;
    *path = uri;
    for (int i = (int)strlen(uri) - 1; i >= 0; i--) {
        if (uri[i] != '#') continue;
        uri[i++] = 0;
        if (hash != NULL) *hash = uri + i;
        if (strlen(uri + i) != 128) return false;   /* URI_ERROR would panic; marked */
        break;
    }
    return true;
}
static void t(const char *v) {
    char *r=NULL,*ro=NULL,*p=NULL,*h=NULL;
    bool ok = uri_resolve(v,&r,&ro,&p,&h);
    printf("%-42s -> %s", v, ok?"TRUE ":"FALSE");
    if (ok) printf("  resource=\"%s\" root=\"%s\" path=\"%s\" hash=%s", r, ro, p, h?h:"(NULL)");
    printf("\n");
}
int main(void) {
    t("boot():/EFI/BOOT/BOOTX64.EFI");            /* host line 72: shape, no hash */
    t("boot():/EFI/Linux/x.efi");                   /* shape, no hash */
    t("plainname.efi");                             /* no '(' */
    t("boot()plainname.efi");                       /* '(' but no '):/' */
    t("boot():/x#");                                /* '#' but empty hash */
    t("boot():/x#abc");                             /* '#' but short hash */
    t("boot(123):/x");                              /* non-empty root */
    { char h[129]; for(int i=0;i<128;i++) h[i]="0123456789abcdef"[i%16]; h[128]=0;
      char v[200]; snprintf(v,sizeof v,"boot():/x#%s",h); t(v); }
    return 0;
}
