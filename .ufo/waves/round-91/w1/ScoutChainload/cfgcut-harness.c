/* Faithful transcription of Limine v12.9.4 common/lib/config.c:
 *   - the whitespace/CR stripping loop (raw 527-552)
 *   - config_get_entry (raw 686-722)
 *   - the global-section cut at the end of init_config (raw 642-651)
 *   - config_get_value's visibility scan (raw 778-820)
 * Only the externals are stubbed.  Output: what config_get_value(NULL,0,KEY)
 * can see after init_config, i.e. the global section.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include <stdint.h>

#define SEPARATOR '\n'

static char *config_addr;
static bool config_ready = false;

static void *ext_mem_alloc(uint64_t n) { return calloc(1, n ? n : 1); }
static void pmm_free(void *p, uint64_t n) { (void)n; free(p); }

/* ---- verbatim: common/lib/config.c raw 686-722 ---- */
static char *config_get_entry(size_t *size, size_t index) {
    if (!config_ready || config_addr == NULL)
        return NULL;

    char *ret;
    char *p = config_addr;

    for (size_t i = 0; i <= index; i++) {
        while (*p != '/') {
            if (!*p)
                return NULL;
            p++;
        }
        p++;
        if ((p - 1) != config_addr && *(p - 2) != '\n')
            i--;
    }

    do {
        p++;
    } while (*p != '\n' && *p != '\0');

    ret = p;

cont:
    while (*p != '/' && *p)
        p++;

    if (*p && *(p - 1) != '\n') {
        p++;
        goto cont;
    }

    *size = p - ret;

    return ret;
}

/* ---- verbatim: common/lib/config.c raw 778-820 (key visibility) ---- */
static char *config_get_value(const char *config, size_t index, const char *key) {
    static char buf[4096];
    if (!key || !config_ready)
        return NULL;
    if (config == NULL)
        config = config_addr;
    if (config == NULL)
        return NULL;
    size_t key_len = strlen(key);
    for (size_t i = 0; config[i]; i++) {
        if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {
            if (i && config[i - 1] != SEPARATOR)
                continue;
            if (index--)
                continue;
            i += key_len + 1;
            while (config[i] == ' ' || config[i] == '\t') i++;
            size_t value_len;
            for (value_len = 0;
                 config[i + value_len] != SEPARATOR && config[i + value_len];
                 value_len++);
            if (value_len >= 4096) value_len = 4095;
            memcpy(buf, config + i, value_len);
            buf[value_len] = '\0';
            return buf;
        }
    }
    return NULL;
}

/* ---- verbatim behaviour of init_config: strip (raw 527-552) then cut (raw 642-651) ---- */
static void init_config_like(size_t config_size) {
    config_addr[config_size - 2] = '\n';
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
    config_ready = true;
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

static void run(const char *name, const char *text) {
    size_t n = strlen(text);
    config_addr = ext_mem_alloc(n + 2);
    memcpy(config_addr, text, n);
    init_config_like(n + 2);
    const char *hp = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
    const char *mb = config_get_value(NULL, 0, "MEASURED_BOOT");
    const char *to = config_get_value(NULL, 0, "TIMEOUT");
    printf("== %s\n", name);
    printf("   visible bytes of config_addr: %zu of %zu\n", strlen(config_addr), n + 2);
    { char *q; printf("   buffer: ");
      for (q = config_addr; q < config_addr + n + 2; q++) {
          if (*q == 0) { printf("<NUL>"); } else if (*q == '\n') { printf("<NL>"); } else putchar(*q);
      }
      printf("\n"); }
    printf("   HASH_MISMATCH_PANIC=%s MEASURED_BOOT=%s TIMEOUT=%s\n",
           hp ? hp : "(null)", mb ? mb : "(null)", to ? to : "(null)");
    /* entry body of the first entry, as Limine would copy it (config.c 377-380) */
    size_t sz = 0;
    char *body = config_get_entry(&sz, 0);
    if (body) {
        char *copy = ext_mem_alloc(sz + 1);
        memcpy(copy, body, sz);
        copy[sz] = 0;
        const char *p = config_get_value(copy, 0, "PATH");
        printf("   entry0 body PATH=%s (body %zu bytes)\n", p ? p : "(null)", sz);
    }
    free(config_addr);
}

int main(void) {
    run("A: global line then entry", "hash_mismatch_panic: no\n/+Omarchy\n  path: boot():/x#h\n");
    run("B: entry line is line 1", "/+Omarchy\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("C: blank first line then entry", "   \n/+Omarchy\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("D: global line, key inside entry body", "measured_boot: yes\n/+Omarchy\n  hash_mismatch_panic: no\n  path: boot():/x#h\n");
    run("E: no entry at all", "hash_mismatch_panic: no\nmeasured_boot: yes\n");
    run("F: indented entry name", "  /+Omarchy\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("G: nested first entry", "measured_boot: yes\n//linux\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("H: nested first entry, indented", "measured_boot: yes\n  //linux\n  path: boot():/x#h\n");
    run("I: first line indented entry", "  /+Omarchy\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("J: CR + tabs", "hash_mismatch_panic: no\r\n\t/+Omarchy\r\n\tpath: x\r\n");
    run("K: nested entry is physical line 1 (unindented)", "//linux\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("L: nested entry is physical line 1 (indented)", "  //linux\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("M: single-slash entry physical line 1 (unindented)", "/+Omarchy\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("N: global line then nested entry", "timeout: 5\n  //linux\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    run("O: three slashes", "///linux\n  path: boot():/x#h\nhash_mismatch_panic: no\n");
    return 0;
}
