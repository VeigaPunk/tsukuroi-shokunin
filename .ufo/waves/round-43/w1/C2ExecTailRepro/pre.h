/* Harness preamble: stubs only.  Everything after the "COPY BEGIN" markers is
 * extracted byte-for-byte from
 *   /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c
 * (btrfs-progs v7.1, sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801)
 * by gen.sh's sed line-range extraction.  The only textual change is SCRUB_DATA_FILE's
 * base path, rewritten to this scratch dir; SCRUB_PROGRESS_SOCKET_PATH keeps its
 * original value because no copied function uses it.
 */
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/file.h>
#include <sys/resource.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>
#include <stdarg.h>
#include <limits.h>
#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <uuid/uuid.h>
#include <linux/btrfs.h>

/* --- btrfs-progs kerncompat.h/top-level typedefs (stub) --- */
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
/* btrfs-progs kerncompat.h spells u64 as unsigned long long so that it matches the
 * kernel UAPI __u64 type on this target; %lld in scrub_kvwrite confirms that. */
typedef unsigned long long u64;
typedef long long s64;
#ifndef SZ_16K
#define SZ_16K (16 * 1024)
#endif
#ifndef PATH_MAX
#define PATH_MAX 4096
#endif
/* kerncompat.h's fallthrough */
#define fallthrough __attribute__ ((__fallthrough__))

/* --- common/messages.h (stub): warning()/error() print to stderr --- */
static int stub_warn_count;
static int stub_err_count;
static void warning(const char *fmt, ...)
	__attribute__ ((format (printf, 1, 2)));
static void error(const char *fmt, ...)
	__attribute__ ((format (printf, 1, 2)));
static void warning(const char *fmt, ...)
{
	va_list args;

	printf("WARNING: ");
	va_start(args, fmt);
	vprintf(fmt, args);
	va_end(args);
	printf("\n");
	fflush(stdout);
	stub_warn_count++;
}

static void error(const char *fmt, ...)
{
	va_list args;

	printf("ERROR: ");
	va_start(args, fmt);
	vprintf(fmt, args);
	va_end(args);
	printf("\n");
	fflush(stdout);
	stub_err_count++;
}

/* --- kerncompat.h error-pointer helpers (stub, same semantics) --- */
#define MAX_ERRNO 4095
#define IS_ERR_VALUE(x) ((x) >= (unsigned long)-MAX_ERRNO)
static inline void *ERR_PTR(long error) { return (void *)error; }
static inline long PTR_ERR(const void *ptr) { return (long)ptr; }
#ifndef IS_ERR
#define IS_ERR(ptr) IS_ERR_VALUE((unsigned long)ptr)
#endif

/* --- scrub.c:67-70 with SCRUB_DATA_FILE rebased into scratch --- */
#define SCRUB_DATA_FILE "/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib/btrfs/scrub.status"
#define SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"
#define SCRUB_FILE_VERSION_PREFIX "scrub status"
#define SCRUB_FILE_VERSION "1"
