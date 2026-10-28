#!/usr/bin/env python3
"""Build a C harness whose function bodies are the VERBATIM pinned bytes of
lib/kstrtox.c, lib/vsprintf.c, lib/cmdline.c (S246) and the scrub_speed_max store of
fs/btrfs/sysfs.c (S243), then drive the write path over the GR1 examples.

Only the kernel helpers the pinned code calls are stubbed; every stub is named in the
emitted PRELUDE comment so the receipt cannot be mistaken for a full kernel build.
"""
import os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC45 = LANE + "/.ufo/waves/round-45/frozen/src"
SRC44 = LANE + "/.ufo/waves/round-44/frozen/src"
S = "/fast/scratch/hyaku/tsukuroi-r50/R50RevGR1Radix"


def read(p):
    with open(p, "r", encoding="utf-8", errors="surrogateescape") as f:
        return f.read().split("\n")


def grab(path, sig_regex):
    """Return the verbatim text of the function whose signature line matches sig_regex,
    found by brace-depth scan so the extent is exact."""
    lines = read(path)
    start = None
    for i, ln in enumerate(lines):
        if re.search(sig_regex, ln):
            start = i
            break
    if start is None:
        raise SystemExit("signature not found: %s in %s" % (sig_regex, path))
    depth = 0
    seen = False
    for j in range(start, len(lines)):
        for ch in lines[j]:
            if ch == "{":
                depth += 1
                seen = True
            elif ch == "}":
                depth -= 1
        if seen and depth == 0:
            return "\n".join(lines[start:j + 1]), start + 1, j + 1
    raise SystemExit("unterminated function: %s" % sig_regex)


PRELUDE = r"""
/* ---- harness prelude: kernel helpers stubbed, pinned bodies verbatim below ---- */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdlib.h>
#include <stddef.h>

/* linux/compiler_attributes.h: #define fallthrough __attribute__((__fallthrough__)) */
#define fallthrough __attribute__((__fallthrough__))
#define noinline __attribute__((noinline))
#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)
#define EXPORT_SYMBOL(x)
#define KSTRTOX_OVERFLOW (1u << 31)

/* include/linux/kstrtox.h: #define _tolower(c) ((c) | 0x20) */
static inline unsigned int _tolower_stub(unsigned int c) { return c | 0x20u; }
#define _tolower(c) _tolower_stub((unsigned int)(c))

/* include/linux/ctype.h isxdigit() for the ASCII set */
static inline int isxdigit_stub(int c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
}
#define isxdigit(c) isxdigit_stub((int)(c))

/* include/linux/ctype.h isspace() for the ASCII set */
static inline int isspace_stub(int c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
}

/* include/linux/overflow.h generic versions */
#define check_mul_overflow(a, b, d) __builtin_mul_overflow((a), (b), (d))
#define check_add_overflow(a, b, d) __builtin_add_overflow((a), (b), (d))
static inline bool check_shl_overflow(unsigned long long a, unsigned int s,
                                      unsigned long long *d) {
    if (s >= sizeof(a) * 8) { *d = a; return true; }
    *d = a << s;
    if (a != *d >> s) return true;
    return false;
}

/* lib/string.c skip_spaces() */
static char *skip_spaces(const char *str) {
    while (isspace_stub(*str)) ++str;
    return (char *)str;
}
/* ---- end prelude ---- */
"""


def main():
    k_fixup, kf_a, kf_b = grab(SRC45 + "/kstrtox.c", r"^const char \*_parse_integer_fixup_radix")
    k_lim, kl_a, kl_b = grab(SRC45 + "/kstrtox.c", r"^unsigned int _parse_integer_limit")
    k_int, ki_a, ki_b = grab(SRC45 + "/kstrtox.c", r"^unsigned int _parse_integer\(")
    v_snt, vs_a, vs_b = grab(SRC45 + "/vsprintf.c", r"^static unsigned long long simple_strntoull")
    v_ull, vu_a, vu_b = grab(SRC45 + "/vsprintf.c", r"^unsigned long long simple_strtoull")
    c_mem, cm_a, cm_b = grab(SRC45 + "/cmdline.c", r"^unsigned long long memparse")
    s_store, ss_a, ss_b = grab(SRC44 + "/sysfs.c", r"^static ssize_t btrfs_devinfo_scrub_speed_max_store")

    # the store replica: verbatim pinned body with the container_of/device access removed
    store_replica = r"""
/* replica of the pinned store body (S243 sysfs.c:%d-%d); the container_of lookup and
   the WRITE_ONCE target are replaced by a file-scope variable, nothing else changes. */
static unsigned long long device_scrub_speed_max = 0;
static ssize_t store(const char *buf, size_t len)
{
    char *endptr;
    unsigned long long limit;

    limit = memparse(buf, &endptr);
    /* There could be trailing '\n', also catch any typos after the value. */
    endptr = skip_spaces(endptr);
    if (*endptr != 0)
        return -22;
    device_scrub_speed_max = limit;
    return (ssize_t)len;
}
""" % (ss_a, ss_b)

    driver = r"""
struct kase { const char *bytes; const char *label; };

int main(void)
{
    struct kase cases[] = {
        {"100M\n",          "named: 100M"},
        {"100m\n",          "named: 100m"},
        {"010\n",           "named: 010"},
        {"0x10\n",          "named: 0x10"},
        {"10MB\n",          "named: 10MB"},
        {"10 M\n",          "named: 10 M"},
        {"-1\n",            "named: -1"},
        {"\n",              "named: bare newline"},
        {"0X10\n",          "extra: 0X10 (upper X)"},
        {"0x\n",            "extra: 0x no hex digit"},
        {"0X\n",            "extra: 0X no hex digit"},
        {"+10\n",           "extra: leading +"},
        {" 100\n",          "extra: leading space"},
        {"\t100\n",         "extra: leading tab"},
        {"M\n",             "extra: suffix only, no digits"},
        {"K\n",             "extra: K only"},
        {"0\n",             "extra: 0"},
        {"1K\n",            "extra: 1K"},
        {"1k\n",            "extra: 1k"},
        {"1G\n",            "extra: 1G"},
        {"1E\n",            "extra: 1E"},
        {"100M \n",         "extra: suffix then space"},
        {"100M\n",          "extra: suffix then newline"},
        {"100M\t\n",        "extra: suffix then tab+newline"},
        {"100 \n",          "extra: number then space+newline"},
        {"100\n \n",        "extra: number then newline+space+newline"},
        {"100Mx\n",         "extra: suffix then junk"},
        {"0x10M\n",         "extra: hex then suffix"},
        {"08\n",            "extra: 08 (octal rejects 8)"},
        {"0x1g\n",          "extra: hex digit then non-hex"},
        {"1e3\n",           "extra: 1e3 (e is the E suffix)"},
        {"18446744073709551615\n", "extra: 2^64-1"},
        {"18446744073709551616\n", "extra: 2^64 (decimal overflow)"},
        {"0xFFFFFFFFFFFFFFFFK\n",  "extra: suffix shift overflow"},
        {"0xFFFFFFFFFFFFFFFFKK\n", "extra: suffix overflow + second letter"},
        {"1024K\n",         "extra: 1024K"},
        {"\n\n",            "extra: two newlines"},
        {"",                "extra: empty write buffer"},
    };
    size_t i, n = sizeof(cases) / sizeof(cases[0]);
    for (i = 0; i < n; i++) {
        char *endp = NULL;
        unsigned long long raw = memparse(cases[i].bytes, &endp);
        ssize_t rc = store(cases[i].bytes, strlen(cases[i].bytes));
        if (rc < 0)
            printf("%-42s | memparse=%-20llu endptr=%td | store=EINVAL(%zd)\n",
                   cases[i].label, raw, (ptrdiff_t)(endp - cases[i].bytes), rc);
        else
            printf("%-42s | memparse=%-20llu endptr=%td | store=ACCEPT(%zd) limit=%llu\n",
                   cases[i].label, raw, (ptrdiff_t)(endp - cases[i].bytes), rc,
                   device_scrub_speed_max);
        device_scrub_speed_max = 0;
    }
    return 0;
}
"""

    src = (PRELUDE
           + "\n/* ===== lib/kstrtox.c:%d-%d (verbatim) ===== */\n" % (kf_a, kf_b) + k_fixup + "\n"
           + "\n/* ===== lib/kstrtox.c:%d-%d (verbatim) ===== */\n" % (kl_a, kl_b) + k_lim + "\n"
           + "\n/* ===== lib/kstrtox.c:%d-%d (verbatim) ===== */\n" % (ki_a, ki_b) + k_int + "\n"
           + "\n/* ===== lib/vsprintf.c:%d-%d (verbatim) ===== */\n" % (vs_a, vs_b) + v_snt + "\n"
           + "\n/* ===== lib/vsprintf.c:%d-%d (verbatim) ===== */\n" % (vu_a, vu_b) + v_ull + "\n"
           + "\n/* ===== lib/cmdline.c:%d-%d (verbatim) ===== */\n" % (cm_a, cm_b) + c_mem + "\n"
           + store_replica
           + driver)
    with open(S + "/radix.c", "w") as f:
        f.write(src)
    print("pinned extents: fixup %d-%d, _parse_integer_limit %d-%d, _parse_integer %d-%d, "
          "simple_strntoull %d-%d, simple_strtoull %d-%d, memparse %d-%d, store %d-%d"
          % (kf_a, kf_b, kl_a, kl_b, ki_a, ki_b, vs_a, vs_b, vu_a, vu_b, cm_a, cm_b, ss_a, ss_b))


if __name__ == "__main__":
    main()
