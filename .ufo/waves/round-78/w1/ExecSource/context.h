/* SPDX-License-Identifier: LGPL-2.1-or-later */
#define _GNU_SOURCE
#include <assert.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/statvfs.h>
#include <syslog.h>
#include <unistd.h>

/* Manager is asserted nonnull but no members are accessed. */
typedef struct Manager { int unused; } Manager;
static void closedirp(DIR **d) { if (*d) closedir(*d); }
#define _cleanup_closedir_ __attribute__((cleanup(closedirp)))
/* Real readdir, including dot entries; no modeled directory entries. */
#define FOREACH_DIRENT_ALL(de, d, on_error) \
        for (struct dirent *de; (de = readdir(d)) != NULL; )
/* Logging emits the original format and preserves negative errno return. */
static int harness_log(int error, const char *format, ...) {
        int saved = errno;
        va_list ap;
        errno = error;
        va_start(ap, format);
        vfprintf(stderr, format, ap);
        va_end(ap);
        fputc('\n', stderr);
        errno = saved;
        return -error;
}
#define JOURNAL_LOG_RATELIMIT 0
#define log_ratelimit_full_errno(level, error, rate, ...) harness_log(error, __VA_ARGS__)
#define log_ratelimit_error_errno(error, rate, ...) harness_log(error, __VA_ARGS__)
#define log_debug_errno(error, ...) harness_log(error, __VA_ARGS__)
/* Upstream non-boot type and equality macro; dependency body is verbatim. */
typedef char sd_char;
#define streq(a,b) (strcmp((a),(b)) == 0)
/* No const-generic return annotation needed by these boolean callsites. */
#define endswith(s, suffix) endswith_internal(s, suffix)
