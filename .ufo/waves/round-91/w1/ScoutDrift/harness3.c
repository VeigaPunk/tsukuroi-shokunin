// Empirical harness: compiles UPSTREAM Limine v12.9.4 and v12.9.6 config-parsing
// bytes verbatim (extracted mechanically from the upstream clones) and measures
// what config_get_value(NULL, 0, "HASH_MISMATCH_PANIC") can actually see.
//
// The point: the r91 V1 rule freezes v12.9.4's global-section visibility.
// v12.9.5/12.9.6 rewrote create_menu_tree(); we measure whether the
// global section Limine still exposes changed.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

#define SEPARATOR '\n'
#define MAX_MENU_NESTING 64

struct menu_entry {
    char *name;
    struct menu_entry *parent;
    struct menu_entry *sub;
    bool expanded;
    char *body;
    struct menu_entry *next;
    char *comment;
    bool skipped_computed;
    bool skipped;
    bool dup_index_computed;
    size_t dup_index;
};

static char *config_addr;
static size_t config_size;
static bool config_ready = false;
static bool bad_config = false;
static const char *lastkey;
static struct menu_entry *menu_tree;

static void *ext_mem_alloc(uint64_t n) { return calloc(1, n ? n : 1); }
#define MAX_MENU_NESTING 64
static void *ext_mem_alloc_counted(uint64_t n, uint64_t s) { return calloc(1, n * s ? n * s : 1); }
static void panic(bool _a, const char *fmt, ...) { (void)fmt; }
static void pmm_free(void *p, uint64_t n) { (void)n; free(p); }
#define strdup(s) harness_strdup(s)
static char *harness_strdup(const char *s) { return s ? __builtin_strdup(s) : NULL; }

// ---- upstream v12.9.4 bytes ----
#include "part_94_cgen.c"
#include "part_94_helpers.c"
#include "part_94_cgv.c"
#include "part_94_cge.c"
#include "part_94_ctr.c"

// v12.9.4 init_config tail: the cut.
static void v94_cut(void) {
    size_t s;
    char *c = config_get_entry(&s, 0);
    if (c != NULL) {
        while (*c != '/' && c > config_addr) {
            c--;
        }
        if (*c == '/' && c > config_addr) {
            c[-1] = 0;
        }
    }
}



// ---- shared: run94 (from harness.c) ----
#include "part_run94.c"
static void run94(const char *text);

// ==== upstream v12.9.6 common/lib/config.c raw 298-407, VERBATIM ====
#include "part_95_ctr.c"
// =====================================================================

static void run96v(const char *text) {
    config_size = strlen(text) + 2;
    config_addr = ext_mem_alloc(config_size);
    memcpy(config_addr, text, strlen(text));
    config_addr[config_size - 2] = '\n';
    config_addr[config_size - 1] = '\0';
    { size_t write = 0; bool als = true;
      for (size_t read = 0; read < config_size - 1; read++) {
        char c = config_addr[read];
        if (c == '\r') continue;
        if (als && (c == ' ' || c == '\t')) continue;
        if (c == '\n') { while (write > 0 && (config_addr[write-1]==' '||config_addr[write-1]=='\t')) write--; als = true; }
        else als = false;
        config_addr[write++] = c;
      }
      while (write > 0 && (config_addr[write-1]==' '||config_addr[write-1]=='\t')) write--;
      config_addr[write++] = '\0'; config_size = write; }
    config_ready = true;
    menu_tree = create_menu_tree_95v();
    const char *v0 = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
    char vbuf[64]; snprintf(vbuf, sizeof vbuf, "%s", v0 ? v0 : "(null)");
    const char *m0 = config_get_value(NULL, 0, "MEASURED_BOOT");
    char mbuf[64]; snprintf(mbuf, sizeof mbuf, "%s", m0 ? m0 : "(null)");
    printf("v12.9.5(verbatim upstream file)  hash_mismatch_panic=%-8s measured_boot=%-8s visible=[%s]\n",
           vbuf, mbuf, config_addr);
}

int main(void) {
    { const char *N = "hash_mismatch_panic: no\nmeasured_boot: yes\n";
      printf("== N: no entry line at all ==\n"); run94(N); run96v(N); }
    { const char *E = "/Shell\nprotocol: efi\n";
      printf("== E: entry-first, no global keys at all ==\n"); run94(E); run96v(E); }
    const char *A = "hash_mismatch_panic: no\n/Shell\nprotocol: efi\npath: boot():/x#abc\n";
    const char *B = "/Shell\nprotocol: efi\npath: boot():/x#abc\nhash_mismatch_panic: no\n";
    const char *D = "/Shell\nprotocol: efi\nmeasured_boot: yes\n";
    printf("== A: global panic BEFORE first entry ==\n");  run94(A); run96v(A);
    printf("== B: global panic AFTER first entry, first line is entry ==\n"); run94(B); run96v(B);
    printf("== D: measured_boot AFTER first entry, first line is entry ==\n"); run94(D); run96v(D);
    return 0;
}
