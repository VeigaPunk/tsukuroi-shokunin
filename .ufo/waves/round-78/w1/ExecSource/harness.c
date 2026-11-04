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

sd_char* endswith_internal(const sd_char *s, const sd_char *suffix) {
        size_t sl, pl;

        assert(s);
        assert(suffix);

        sl = strlen(s);
        pl = strlen(suffix);

        if (pl == 0)
                return (sd_char*) s + sl;

        if (sl < pl)
                return NULL;

        if (!streq(s + sl - pl, suffix))
                return NULL;

        return (sd_char*) s + sl - pl;
}

static int manager_determine_path_usage(
                Manager *m,
                const char *path,
                uint64_t *ret_used,
                uint64_t *ret_free) {

        _cleanup_closedir_ DIR *d = NULL;
        struct statvfs ss;

        assert(m);
        assert(path);
        assert(ret_used);
        assert(ret_free);

        d = opendir(path);
        if (!d)
                return log_ratelimit_full_errno(errno == ENOENT ? LOG_DEBUG : LOG_ERR,
                                                errno, JOURNAL_LOG_RATELIMIT, "Failed to open %s: %m", path);

        if (fstatvfs(dirfd(d), &ss) < 0)
                return log_ratelimit_error_errno(errno, JOURNAL_LOG_RATELIMIT,
                                                 "Failed to fstatvfs(%s): %m", path);

        *ret_free = ss.f_bsize * ss.f_bavail;
        *ret_used = 0;
        FOREACH_DIRENT_ALL(de, d, break) {
                struct stat st;

                if (!endswith(de->d_name, ".journal") &&
                    !endswith(de->d_name, ".journal~"))
                        continue;

                if (fstatat(dirfd(d), de->d_name, &st, AT_SYMLINK_NOFOLLOW) < 0) {
                        log_debug_errno(errno, "Failed to stat %s/%s, ignoring: %m", path, de->d_name);
                        continue;
                }

                if (!S_ISREG(st.st_mode))
                        continue;

                *ret_used += (uint64_t) st.st_blocks * 512UL;
        }

        return 0;
}

/* SPDX-License-Identifier: LGPL-2.1-or-later */
int main(int argc, char **argv) {
        Manager m = {0};
        uint64_t used = UINT64_MAX, available = UINT64_MAX;
        if (argc != 2) return 2;
        int r = manager_determine_path_usage(&m, argv[1], &used, &available);
        printf("{\"return\":%d,\"used\":%" PRIu64 ",\"free\":%" PRIu64 "}\n", r, used, available);
        return r < 0 ? 1 : 0;
}
