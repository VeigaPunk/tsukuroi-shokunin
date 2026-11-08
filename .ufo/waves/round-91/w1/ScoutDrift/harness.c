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
};

static char *config_addr;
static size_t config_size;
static bool config_ready = false;
static bool bad_config = false;
static const char *lastkey;
static struct menu_entry *menu_tree;

static void *ext_mem_alloc(uint64_t n) { return calloc(1, n ? n : 1); }
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

// ---- upstream v12.9.6 bytes ----
static char *config_get_value_96(const char *config, size_t index, const char *key);
static struct menu_entry *create_menu_tree_96(void);

static char *config_get_value_96(const char *config, size_t index, const char *key) {
    // upstream v12.9.6 common/lib/config.c raw 727-771 (byte-identical body to 12.9.4's)
    #define CONFIG_VALUE_BUF_SIZE 4096
    static char buf[CONFIG_VALUE_BUF_SIZE];
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
            for (value_len = 0; config[i + value_len] != SEPARATOR && config[i + value_len]; value_len++);
            if (value_len >= CONFIG_VALUE_BUF_SIZE) value_len = CONFIG_VALUE_BUF_SIZE - 1;
            memcpy(buf, config + i, value_len);
            buf[value_len] = '\0';
            lastkey = config + i;
            return buf;
        }
    }
    return NULL;
}

// The upstream v12.9.6 create_menu_tree() body, transcribed verbatim from
// common/lib/config.c raw 298-407 of tag v12.9.6.
static struct menu_entry *create_menu_tree_96(void) {
    struct menu_entry *root = NULL;
    struct menu_entry *last_at_depth[MAX_MENU_NESTING + 2] = {0};

    char *p = config_addr;
    if (p == NULL) {
        return NULL;
    }

    while (*p != '\0') {
        if (*p == '/' && (p == config_addr || *(p - 1) == '\n')) {
            break;
        }
        p++;
    }

    if (*p == '\0') {
        return NULL;
    }

    // One allocation for all the entries, as each of its own takes a page.
    size_t entry_count = 1;
    for (char *q = p + 1; *q != '\0'; q++) {
        if (*q == '/' && *(q - 1) == '\n') {
            entry_count++;
        }
    }
    struct menu_entry *entries = ext_mem_alloc_counted(entry_count, sizeof(struct menu_entry));
    size_t entries_used = 0;

    if (p > config_addr) {
        *(p - 1) = '\0';
    }

    while (*p != '\0') {
        size_t depth = 0;
        while (*p == '/') {
            depth++;
            p++;
        }

        if (depth > MAX_MENU_NESTING) {
            bad_config = true;
            panic(true, "config: Menu nesting too deep (max %u)", MAX_MENU_NESTING);
        }

        if (depth > 1 && last_at_depth[depth - 1] == NULL) {
            bad_config = true;
            panic(true, "config: Malformed config file. Parentless child.");
        }

        bool default_expanded = (*p == '+');
        if (default_expanded) {
            p++;
        }

        while (*p == ' ' || *p == '\t') {
            p++;
        }

        char *name = p;
        while (*p != '\n' && *p != '\0') {
            p++;
        }
        if (*p == '\n') {
            *p = '\0';
            p++;
        }

        char *body = "";
        if (*p != '/') {
            body = p;
            while (*p != '\0') {
                if (*p == '/' && *(p - 1) == '\n') {
                    break;
                }
                p++;
            }

            if (p > body && *(p - 1) == '\n') {
                *(p - 1) = '\0';
            }
        }

        struct menu_entry *entry = &entries[entries_used++];
        entry->name = name;
        entry->body = body;
        entry->parent = last_at_depth[depth - 1];
        entry->expanded = default_expanded;

        if (entry->parent != NULL) {
            if (entry->parent->sub == NULL) {
                entry->parent->sub = entry;
            }
        }

        if (last_at_depth[depth] != NULL && last_at_depth[depth]->parent == entry->parent) {
            last_at_depth[depth]->next = entry;
        } else if (depth == 1 && root == NULL) {
            root = entry;
        }

        last_at_depth[depth] = entry;
        for (size_t d = depth + 1; d <= MAX_MENU_NESTING; d++) {
            last_at_depth[d] = NULL;
        }
    }

    return root;
}

// ---- harness ----
static void run94(const char *text) {
    config_size = strlen(text) + 2;
    config_addr = ext_mem_alloc(config_size);
    memcpy(config_addr, text, strlen(text));
    config_addr[config_size - 2] = '\n';
    config_addr[config_size - 1] = '\0';
    { // upstream 12.9.4 strip loop (config.c raw 527-552)
        for (size_t i = 0; i < config_size; i++) {
            size_t skip = 0;
            if (config_addr[i] == ' ' || config_addr[i] == '\t') {
                while (i + skip < config_size && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')) {
                    skip++;
                }
                if (i + skip < config_size && config_addr[i + skip] == '\n') {
                    goto skip_loop;
                }
                skip = 0;
            }
            while (i + skip < config_size
                && ((config_addr[i + skip] == '\r')
                    || ((!i || config_addr[i - 1] == '\n') && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')))
            ) {
                skip++;
            }
skip_loop:
            if (skip) {
                for (size_t j = i; j < config_size - skip; j++)
                    config_addr[j] = config_addr[j + skip];
                config_size -= skip;
                i--;
            }
        }
    }
    config_ready = true;
    menu_tree = create_menu_tree(NULL, 1, 0);
    v94_cut();
    const char *v0 = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
    char vbuf[64]; snprintf(vbuf, sizeof vbuf, "%s", v0 ? v0 : "(null)");
    const char *m0 = config_get_value(NULL, 0, "MEASURED_BOOT");
    char mbuf[64]; snprintf(mbuf, sizeof mbuf, "%s", m0 ? m0 : "(null)");
    printf("v12.9.4  hash_mismatch_panic=%-8s measured_boot=%-8s visible=[%s]\n",
           vbuf, mbuf, config_addr);
}

static void run96(const char *text) {
    config_size = strlen(text) + 2;
    config_addr = ext_mem_alloc(config_size);
    memcpy(config_addr, text, strlen(text));
    config_addr[config_size - 2] = '\n';
    config_addr[config_size - 1] = '\0';
    { // upstream 12.9.6 strip loop (config.c raw 551-580)
        size_t write = 0;
        bool at_line_start = true;
        for (size_t read = 0; read < config_size - 1; read++) {
            char c = config_addr[read];
            if (c == '\r') continue;
            if (at_line_start && (c == ' ' || c == '\t')) continue;
            if (c == '\n') {
                while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) write--;
                at_line_start = true;
            } else {
                at_line_start = false;
            }
            config_addr[write++] = c;
        }
        while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) write--;
        config_addr[write++] = '\0';
        config_size = write;
    }
    config_ready = true;
    menu_tree = create_menu_tree_96();
    const char *v0 = config_get_value_96(NULL, 0, "HASH_MISMATCH_PANIC");
    char vbuf[64]; snprintf(vbuf, sizeof vbuf, "%s", v0 ? v0 : "(null)");
    const char *m0 = config_get_value_96(NULL, 0, "MEASURED_BOOT");
    char mbuf[64]; snprintf(mbuf, sizeof mbuf, "%s", m0 ? m0 : "(null)");
    printf("v12.9.6  hash_mismatch_panic=%-8s measured_boot=%-8s visible=[%s]\n",
           vbuf, mbuf, config_addr);
}

static void both(const char *label, const char *text) {
    printf("---- %s\n", label);
    run94(text);
    run96(text);
}

static void cmp_strip(const char *label, const char *text) {
    char *a = malloc(strlen(text) + 8), *b = malloc(strlen(text) + 8);
    // v12.9.4 strip
    size_t ca = strlen(text) + 2; memcpy(a, text, strlen(text)); a[ca-2]='\n'; a[ca-1]='\0';
    for (size_t i = 0; i < ca; i++) {
        size_t skip = 0;
        if (a[i] == ' ' || a[i] == '\t') {
            while (i + skip < ca && (a[i + skip] == ' ' || a[i + skip] == '\t')) skip++;
            if (i + skip < ca && a[i + skip] == '\n') goto sl;
            skip = 0;
        }
        while (i + skip < ca && ((a[i + skip] == '\r')
                || ((!i || a[i - 1] == '\n') && (a[i + skip] == ' ' || a[i + skip] == '\t')))) skip++;
sl:
        if (skip) { for (size_t j = i; j < ca - skip; j++) a[j] = a[j + skip]; ca -= skip; i--; }
    }
    // v12.9.6 strip
    size_t cb = strlen(text) + 2; memcpy(b, text, strlen(text)); b[cb-2]='\n'; b[cb-1]='\0';
    { size_t write = 0; bool als = true;
      for (size_t read = 0; read < cb - 1; read++) {
        char c = b[read];
        if (c == '\r') continue;
        if (als && (c == ' ' || c == '\t')) continue;
        if (c == '\n') { while (write > 0 && (b[write-1]==' '||b[write-1]=='\t')) write--; als = true; }
        else als = false;
        b[write++] = c;
      }
      while (write > 0 && (b[write-1]==' '||b[write-1]=='\t')) write--;
      b[write++] = '\0'; cb = write; }
    printf("%-34s 94=[", label); for (size_t q=0;a[q];q++) printf(a[q]=='\n'?"\\n":(a[q]=='\r'?"\\r":(a[q]=='\t'?"\\t":"%c")), a[q]);
    printf("] 96=["); for (size_t q=0;b[q];q++) printf(b[q]=='\n'?"\\n":(b[q]=='\r'?"\\r":(b[q]=='\t'?"\\t":"%c")), b[q]);
    printf("]  %s\n", strcmp(a,b)?"** DIFFER **":"same");
    free(a); free(b);
}

int main(void) {
    printf("=== R1 strip-loop equivalence (12.9.4 raw 527-552 vs 12.9.6 raw 551-580) ===\n");
    cmp_strip("plain", "key: value\n");
    cmp_strip("CR at EOL", "key: value\r\n");
    cmp_strip("CR internal", "ke\ry: value\n");
    cmp_strip("CR then blanks", "key: value\r  \n");
    cmp_strip("CR then newline then blanks", "key: value\r\n  next\n");
    cmp_strip("leading blanks", "   key: value\n");
    cmp_strip("trailing blanks", "key: value   \n");
    cmp_strip("both", "  key: value   \n");
    cmp_strip("blank-only line", "a\n   \nb\n");
    cmp_strip("tab blank", "\tkey:\tvalue\t\n");
    cmp_strip("vertical tab trailing", "key: value\v\n");
    cmp_strip("formfeed trailing", "key: value\f\n");
    cmp_strip("no trailing newline", "key: value");
    cmp_strip("CR only line", "a\r\nb\n");
    cmp_strip("multiple CR", "a\r\r\nb\n");
    cmp_strip("CR then blank line", "a\r\n\nb\n");
    cmp_strip("blank then CR", "a\n\rb\n");
    cmp_strip("entry slash line", "/Entry\n  protocol: efi\n");
    cmp_strip("hash at end", "path: boot():/x#abc\n");

    both("A: global panic BEFORE first entry (r91 V1 normal case)",
         "hash_mismatch_panic: no\n/Shell\nprotocol: efi\npath: boot():/x#abc\n");
    both("B: global panic AFTER first entry (entry-first exception)",
         "/Shell\nprotocol: efi\npath: boot():/x#abc\nhash_mismatch_panic: no\n");
    both("C: blank first line then entry (V1: cut kept)",
         "\n/Shell\nprotocol: efi\nhash_mismatch_panic: no\n");
    both("D: measured_boot: yes after entry",
         "/Shell\nprotocol: efi\nmeasured_boot: yes\n");
    both("E: global panic before entry + measured_boot after entry",
         "hash_mismatch_panic: no\n/Shell\nprotocol: efi\nmeasured_boot: yes\n");
    return 0;
}
