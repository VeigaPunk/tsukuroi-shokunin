/* Faithful port of the two parsers from pinned sources — factual claims verified by executing pinned shapes through byte-identical cut logic.
   v12.9.4: init_config 642-650 + config_get_entry 686-720 + config_get_value 778-818.
   v12.9.5/6: create_menu_tree 298-407 + config_get_value 727-771. Stubs replace mem/print/panic. */
#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
static char *config_addr;
static bool config_ready = false;
static const char *lastkey;
#define SEPARATOR '\n'
static char buf[4096];
static char *dup_or_null(char *r){ if(!r) return NULL; char *d=malloc(strlen(r)+1); strcpy(d,r); return d; }
static char *config_get_value(const char *config, size_t index, const char *key) {
    if (!key || !config_ready) return NULL;
    if (config == NULL) config = config_addr;
    if (config == NULL) return NULL;
    size_t key_len = strlen(key);
    for (size_t i = 0; config[i]; i++) {
        if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {
            if (i && config[i - 1] != SEPARATOR) continue;
            if (index--) continue;
            i += key_len + 1;
            while (config[i] == ' ' || config[i] == '\t') i++;
            size_t value_len;
            for (value_len = 0; config[i + value_len] != SEPARATOR && config[i + value_len]; value_len++) {}
            if (value_len >= 4096) value_len = 4095;
            memcpy(buf, config + i, value_len); buf[value_len] = '\0';
            lastkey = config + i; return buf;
        }
    }
    return NULL;
}
/* v12.9.4 config_get_entry (body start pointer), verbatim logic */
static char *config_get_entry(size_t *size, size_t index) {
    if (!config_ready || config_addr == NULL) return NULL;
    char *ret; char *p = config_addr;
    for (size_t i = 0; i <= index; i++) {
        while (*p != '/') { if (!*p) return NULL; p++; }
        p++;
        if ((p - 1) != config_addr && *(p - 2) != '\n') i--;
    }
    do { p++; } while (*p != '\n' && *p != '\0');
    ret = p;
cont:
    while (*p != '/' && *p) p++;
    if (*p && *(p - 1) != '\n') { p++; goto cont; }
    *size = p - ret; return ret;
}
/* v12.9.4 init_config tail: create_menu_tree loop is read-only, then 642-650 */
static void run_v124(const char *text) {
    size_t len = strlen(text);
    config_addr = malloc(len + 2);
    memcpy(config_addr, text, len + 1);
    config_ready = true;
    /* create_menu_tree(NULL,1,0) reads entries but does not mutate buffer in v12.9.4 */
    size_t s; char *c = config_get_entry(&s, 0);
    if (c != NULL) {
        while (*c != '/' && c > config_addr) c--;
        if (*c == '/' && c > config_addr) { c[-1] = 0; }
    }
}
/* v12.9.5/6 create_menu_tree: forward scan + in-place cut + label-end NUL + body NUL */
struct menu_entry_stub { char *name; char *body; };
static void run_v126(const char *text) {
    size_t len = strlen(text);
    config_addr = malloc(len + 2);
    memcpy(config_addr, text, len + 1);
    char *p = config_addr;
    while (*p != '\0') {
        if (*p == '/' && (p == config_addr || *(p - 1) == '\n')) break;
        p++;
    }
    if (*p == '\0') { config_ready = true; return; }
    if (p > config_addr) { *(p - 1) = '\0'; }
    /* verbatim 332-380 loop (entries table stubbed) */
    while (*p != '\0') {
        size_t depth = 0;
        while (*p == '/') { depth++; p++; }
        bool default_expanded = (*p == '+');
        if (default_expanded) p++;
        while (*p == ' ' || *p == '\t') p++;
        char *name = p;
        while (*p != '\n' && *p != '\0') p++;
        if (*p == '\n') { *p = '\0'; p++; }
        char *body = "";
        if (*p != '/') {
            body = p;
            while (*p != '\0') {
                if (*p == '/' && *(p - 1) == '\n') break;
                p++;
            }
            if (p > body && *(p - 1) == '\n') { *(p - 1) = '\0'; }
        }
    }



    config_ready = true;
}
static void query(const char *label, void (*run)(const char *), const char *text) {
    run(text);
    char *v1 = dup_or_null(config_get_value(NULL, 0, "hash_mismatch_panic"));
    char *v2 = dup_or_null(config_get_value(NULL, 0, "measured_boot"));
    printf("%s\n  config_addr bytes: ", label);
    size_t n = strlen(config_addr);
    for (size_t i = 0; i < n; i++) printf("%02x ", (unsigned char)config_addr[i]);
    printf("\n  hash_mismatch=%s measured_boot=%s\n", v1 ? v1 : "NULL", v2 ? v2 : "NULL");
    free(config_addr); config_addr = NULL; config_ready = false;
}
int main(void) {
    const char *S1 = "hash_mismatch_panic: no\nmeasured_boot: yes\n/Shell\n    protocol: efi\n    path: boot():/EFI/BOOT/none.efi\n";
    const char *S2 = "/Shell\n    protocol: efi\n    path: boot():/EFI/BOOT/none.efi\nhash_mismatch_panic: no\nmeasured_boot: yes\n";
    const char *S3 = "/Shell\n    protocol: efi\n    path: boot():/EFI/BOOT/none.efi\n";
    const char *S4 = "timeout: 5\ndash_dash_dash: 1\n";
    query("S1 global-key-before-entry v12.9.4", run_v124, S1);
    query("S1 global-key-before-entry v12.9.6", run_v126, S1);
    query("S2 entry-first+key-after-body v12.9.4", run_v124, S2);
    query("S2 entry-first+key-after-body v12.9.6", run_v126, S2);
    query("S3 entry-first-no-key v12.9.4", run_v124, S3);
    query("S3 entry-first-no-key v12.9.6", run_v126, S3);
    query("S4 no-entry v12.9.4", run_v124, S4);
    query("S4 no-entry v12.9.6", run_v126, S4);
    /* S5: blank first line then entry then key (V1 non-first-line) */
    const char *S5 = "\n/Shell\n    protocol: efi\nhash_mismatch_panic: no\n";
    query("S5 blank-line-then-entry+key v12.9.4", run_v124, S5);
    query("S5 blank-line-then-entry+key v12.9.6", run_v126, S5);
    /* S6: leading-space entry line, first physical line */
    const char *S6 = "  /Shell\n    protocol: efi\nhash_mismatch_panic: no\n";
    query("S6 leading-space-entry-first v12.9.4", run_v124, S6);
    query("S6 leading-space-entry-first v12.9.6", run_v126, S6);
    return 0;
}
