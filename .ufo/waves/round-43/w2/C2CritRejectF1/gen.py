#!/usr/bin/env python3
"""Assemble harness.c from verbatim line-ranges of the frozen scrub.c (S237)."""
import pathlib, hashlib, sys

SRC = pathlib.Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c")
lines = SRC.read_text().splitlines(keepends=True)

def ext(a, b):
    return "".join(lines[a-1:b])

ranges = [
    (67, 70), (72, 110), (402, 410), (538, 567), (569, 576),
    (578, 771), (773, 793), (795, 841), (843, 895),
]

pre = r'''/* preamble (stubs) -- types, UAPI structs, warning/error */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>
#include <sys/types.h>
#include <time.h>
#include <uuid/uuid.h>
#define fallthrough __attribute__((__fallthrough__))

typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;
typedef unsigned long long u64; typedef long long s64;
typedef unsigned long long __u64;
#define BTRFS_FSID_SIZE 16
#define BTRFS_UUID_UNPARSED_SIZE 37
#define SZ_16K (16 * 1024)
#define MAX_ERRNO 4095
#define IS_ERR_VALUE(x) ((unsigned long)(void *)(x) >= (unsigned long)-MAX_ERRNO)
#define IS_ERR(ptr) IS_ERR_VALUE((unsigned long)(ptr))
#define ERR_PTR(error) ((void *)(long)(error))
#define PTR_ERR(ptr) ((long)(ptr))

struct btrfs_scrub_progress {
    __u64 data_extents_scrubbed;
    __u64 tree_extents_scrubbed;
    __u64 data_bytes_scrubbed;
    __u64 tree_bytes_scrubbed;
    __u64 read_errors;
    __u64 csum_errors;
    __u64 verify_errors;
    __u64 no_csum;
    __u64 csum_discards;
    __u64 super_errors;
    __u64 malloc_errors;
    __u64 uncorrectable_errors;
    __u64 corrected_errors;
    __u64 last_physical;
    __u64 unverified_errors;
};
struct btrfs_ioctl_scrub_args {
    __u64 devid;
    __u64 start;
    __u64 end;
    __u64 flags;
    struct btrfs_scrub_progress progress;
    __u64 unused[7];
};

static int warn_count = 0, err_count = 0;
static void warning(const char *fmt, ...) { va_list ap; va_start(ap, fmt); warn_count++; vfprintf(stdout, fmt, ap); fputc('\n', stdout); va_end(ap); }
static void error(const char *fmt, ...) { va_list ap; va_start(ap, fmt); err_count++; vfprintf(stdout, fmt, ap); fputc('\n', stdout); va_end(ap); }
static void pr_default(const char *fmt, ...) { va_list ap; va_start(ap, fmt); vfprintf(stdout, fmt, ap); va_end(ap); }
'''

# driver: the two-scenario main (verbatim from the working harness.c at generation time is
# not needed; this file is the *source of truth* for the copied ranges; the driver is
# appended from driver.c if present, else a minimal driver)
driver = pathlib.Path("driver.c").read_text() if pathlib.Path("driver.c").exists() else ""

parts = [pre]
for (a, b) in ranges:
    parts.append(ext(a, b))
parts.append(driver)
pathlib.Path("harness.c").write_text("".join(parts))
print("generated harness.c; frozen sha256:", hashlib.sha256(SRC.read_bytes()).hexdigest())
