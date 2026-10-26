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

/* ==== COPY BEGIN scrub.c:72-79 (scrub_stats) ==== */
struct scrub_stats {
	time_t t_start;
	time_t t_resumed;
	u64 duration;
	u64 finished;
	u64 canceled;
	int in_progress;
};
/* ==== COPY END scrub.c:72-79 ==== */

/* ==== COPY BEGIN scrub.c:90-110 (scrub_progress_structs) ==== */
struct scrub_progress {
	struct btrfs_ioctl_scrub_args scrub_args;
	int fd;
	int ret;
	int skip;
	struct scrub_stats stats;
	struct scrub_file_record *resumed;
	int ioctl_errno;
	pthread_mutex_t progress_mutex;
	int ioprio_class;
	int ioprio_classdata;
	u64 old_limit;
	u64 limit;
};

struct scrub_file_record {
	u8 fsid[BTRFS_FSID_SIZE];
	u64 devid;
	struct scrub_stats stats;
	struct btrfs_scrub_progress p;
};
/* ==== COPY END scrub.c:90-110 ==== */

/* ==== COPY BEGIN scrub.c:402-410 (free_history) ==== */
static void free_history(struct scrub_file_record **last_scrubs)
{
	struct scrub_file_record **l = last_scrubs;
	if (!l || IS_ERR(l))
		return;
	while (*l)
		free(*l++);
	free(last_scrubs);
}
/* ==== COPY END scrub.c:402-410 ==== */

/* ==== COPY BEGIN scrub.c:446-476 (scrub_datafile) ==== */
static int scrub_datafile(const char *fn_base, const char *fn_local,
				const char *fn_tmp, char *datafile, int size)
{
	int ret;
	int end = size - 2;

	datafile[end + 1] = '\0';
	strncpy(datafile, fn_base, end);
	ret = strlen(datafile);

	if (ret + 1 > end)
		return -EOVERFLOW;

	datafile[ret] = '.';
	strncpy(datafile + ret + 1, fn_local, end - ret - 1);
	ret = strlen(datafile);

	if (ret + 1 > end)
		return -EOVERFLOW;

	if (fn_tmp) {
		datafile[ret] = '_';
		strncpy(datafile + ret + 1, fn_tmp, end - ret - 1);
		ret = strlen(datafile);

		if (ret > end)
			return -EOVERFLOW;
	}

	return 0;
}
/* ==== COPY END scrub.c:446-476 ==== */

/* ==== COPY BEGIN scrub.c:478-495 (scrub_open_file) ==== */
static int scrub_open_file(const char *datafile, int m)
{
	int fd;
	int ret;

	fd = open(datafile, m, 0600);
	if (fd < 0)
		return -errno;

	ret = flock(fd, LOCK_EX|LOCK_NB);
	if (ret) {
		ret = errno;
		close(fd);
		return -ret;
	}

	return fd;
}
/* ==== COPY END scrub.c:478-495 ==== */

/* ==== COPY BEGIN scrub.c:497-506 (scrub_open_file_r) ==== */
static int scrub_open_file_r(const char *fn_base, const char *fn_local)
{
	int ret;
	char datafile[PATH_MAX];
	ret = scrub_datafile(fn_base, fn_local, NULL,
				datafile, sizeof(datafile));
	if (ret < 0)
		return ret;
	return scrub_open_file(datafile, O_RDONLY);
}
/* ==== COPY END scrub.c:497-506 ==== */

/* ==== COPY BEGIN scrub.c:508-518 (scrub_open_file_w) ==== */
static int scrub_open_file_w(const char *fn_base, const char *fn_local,
				const char *tmp)
{
	int ret;
	char datafile[PATH_MAX];
	ret = scrub_datafile(fn_base, fn_local, tmp,
				datafile, sizeof(datafile));
	if (ret < 0)
		return ret;
	return scrub_open_file(datafile, O_WRONLY|O_CREAT);
}
/* ==== COPY END scrub.c:508-518 ==== */

/* ==== COPY BEGIN scrub.c:520-536 (scrub_rename_file) ==== */
static int scrub_rename_file(const char *fn_base, const char *fn_local,
				const char *tmp)
{
	int ret;
	char datafile_old[PATH_MAX];
	char datafile_new[PATH_MAX];
	ret = scrub_datafile(fn_base, fn_local, tmp,
				datafile_old, sizeof(datafile_old));
	if (ret < 0)
		return ret;
	ret = scrub_datafile(fn_base, fn_local, NULL,
				datafile_new, sizeof(datafile_new));
	if (ret < 0)
		return ret;
	ret = rename(datafile_old, datafile_new);
	return ret ? -errno : 0;
}
/* ==== COPY END scrub.c:520-536 ==== */

/* ==== COPY BEGIN scrub.c:538-540 (_SCRUB_KVREAD_macro) ==== */
#define _SCRUB_KVREAD(ret, i, name, avail, l, dest) if (ret == 0) {	  \
	ret = scrub_kvread(i, sizeof(#name), avail, l, #name, dest.name); \
}
/* ==== COPY END scrub.c:538-540 ==== */

/* ==== COPY BEGIN scrub.c:547-567 (scrub_kvread) ==== */
static int scrub_kvread(int *i, int len, int avail, const char *buf,
			const char *key, u64 *dest)
{
	int j;

	if (*i + len + 1 < avail && strncmp(&buf[*i], key, len - 1) == 0) {
		*i += len - 1;
		if (buf[*i] != ':')
			return -1;
		*i += 1;
		for (j = 0; isdigit(buf[*i + j]) && *i + j < avail; ++j)
			;
		if (*i + j >= avail)
			return -1;
		*dest = atoll(&buf[*i]);
		*i += j;
		return 1;
	}

	return 0;
}
/* ==== COPY END scrub.c:547-567 ==== */

/* ==== COPY BEGIN scrub.c:569-576 (_SCRUB_INVALID_macro) ==== */
#define _SCRUB_INVALID do {						\
	if (report_errors)						\
		warning("invalid data on line %d pos "			\
			"%d state %d (near \"%.*s\") at %s:%d",		\
			lineno, i, state, 20 > avail ? avail : 20,	\
			l + i,	__FILE__, __LINE__);			\
	goto skip;							\
} while (0)
/* ==== COPY END scrub.c:569-576 ==== */

/* ==== COPY BEGIN scrub.c:578-771 (scrub_read_file) ==== */
static struct scrub_file_record **scrub_read_file(int fd, int report_errors)
{
	int avail = 0;
	int old_avail = 0;
	char l[SZ_16K];
	int state = 0;
	int curr = -1;
	int i = 0;
	int j;
	int ret;
	bool eof = false;
	int lineno = 0;
	u64 version;
	char empty_uuid[BTRFS_FSID_SIZE] = {0};
	struct scrub_file_record **p = NULL;

again:
	old_avail = avail - i;
	if (old_avail < 0) {
		error("scrub record file corrupted near byte %d", i);
		return ERR_PTR(-EINVAL);
	}
	if (old_avail)
		memmove(l, l + i, old_avail);
	avail = read(fd, l + old_avail, sizeof(l) - old_avail);
	if (avail == 0)
		eof = true;
	if (avail == 0 && old_avail == 0) {
		if (curr >= 0 &&
		    memcmp(p[curr]->fsid, empty_uuid, BTRFS_FSID_SIZE) == 0) {
			p[curr] = NULL;
		} else if (curr == -1) {
			p = ERR_PTR(-ENODATA);
		}
		return p;
	}
	if (avail == -1) {
		free_history(p);
		return ERR_PTR(-errno);
	}
	avail += old_avail;

	i = 0;
	while (i < avail) {
		void *tmp;

		switch (state) {
		case 0: /* start of file */
			ret = scrub_kvread(&i,
				sizeof(SCRUB_FILE_VERSION_PREFIX), avail, l,
				SCRUB_FILE_VERSION_PREFIX, &version);
			if (ret != 1)
				_SCRUB_INVALID;
			if (version != atoll(SCRUB_FILE_VERSION))
				return ERR_PTR(-ENOTSUP);
			state = 6;
			continue;
		case 1: /* start of line, alloc */
			/*
			 * this state makes sure we have a complete line in
			 * further processing, so we don't need wrap-tracking
			 * everywhere.
			 */
			if (!eof && !memchr(l + i, '\n', avail - i))
				goto again;
			++lineno;
			if (curr > -1 && memcmp(p[curr]->fsid, empty_uuid,
						BTRFS_FSID_SIZE) == 0) {
				state = 2;
				continue;
			}
			++curr;
			tmp = reallocarray(p, curr + 2, sizeof(*p));
			if (!tmp) {
				free_history(p);
				return ERR_PTR(-errno);
			}
			p = tmp;
			p[curr] = malloc(sizeof(**p));
			if (!p[curr]) {
				free_history(p);
				return ERR_PTR(-errno);
			}
			memset(p[curr], 0, sizeof(**p));
			p[curr + 1] = NULL;
			++state;
			fallthrough;
		case 2: /* start of line, skip space */
			while (i < avail && isspace(l[i])) {
				if (l[i] == '\n')
					++lineno;
				++i;
			}
			if (i >= avail ||
			    (!eof && !memchr(l + i, '\n', avail - i)))
				goto again;
			++state;
			fallthrough;
		case 3: /* read fsid */
			if (i == avail)
				continue;
			for (j = 0; l[i + j] != ':' && i + j < avail; ++j)
				;
			if (i + j + 1 >= avail)
				_SCRUB_INVALID;
			if (j != BTRFS_UUID_UNPARSED_SIZE - 1)
				_SCRUB_INVALID;
			l[i + j] = '\0';
			ret = uuid_parse(l + i, p[curr]->fsid);
			if (ret)
				_SCRUB_INVALID;
			i += j + 1;
			++state;
			fallthrough;
		case 4: /* read dev id */
			for (j = 0; isdigit(l[i + j]) && i+j < avail; ++j)
				;
			if (j == 0 || i + j + 1 >= avail)
				_SCRUB_INVALID;
			p[curr]->devid = atoll(&l[i]);
			i += j + 1;
			++state;
			fallthrough;
		case 5: /* read key/value pair */
			ret = 0;
			_SCRUB_KVREAD(ret, &i, data_extents_scrubbed, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, tree_extents_scrubbed, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, data_bytes_scrubbed, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, tree_bytes_scrubbed, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, read_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, csum_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, verify_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, no_csum, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, csum_discards, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, super_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, malloc_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, uncorrectable_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, corrected_errors, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, last_physical, avail, l,
					&p[curr]->p);
			_SCRUB_KVREAD(ret, &i, finished, avail, l,
					&p[curr]->stats);
			_SCRUB_KVREAD(ret, &i, t_start, avail, l,
					(u64 *)&p[curr]->stats);
			_SCRUB_KVREAD(ret, &i, t_resumed, avail, l,
					(u64 *)&p[curr]->stats);
			_SCRUB_KVREAD(ret, &i, duration, avail, l,
					(u64 *)&p[curr]->stats);
			_SCRUB_KVREAD(ret, &i, canceled, avail, l,
					&p[curr]->stats);
			if (ret != 1)
				_SCRUB_INVALID;
			++state;
			fallthrough;
		case 6: /* after number */
			if (l[i] == '|')
				state = 5;
			else if (l[i] == '\n')
				state = 1;
			else
				_SCRUB_INVALID;
			++i;
			continue;
		case 99: /* skip rest of line */
skip:
			state = 99;
			do {
				++i;
				if (l[i - 1] == '\n') {
					state = 1;
					break;
				}
			} while (i < avail);
			continue;
		}
		error("internal error: unknown parser state %d near byte %d",
				state, i);
		return ERR_PTR(-EINVAL);
	}
	goto again;
}
/* ==== COPY END scrub.c:578-771 ==== */

/* ==== COPY BEGIN scrub.c:773-778 (scrub_write_buf) ==== */
static int scrub_write_buf(int fd, const void *data, int len)
{
	int ret;
	ret = write(fd, data, len);
	return ret - len;
}
/* ==== COPY END scrub.c:773-778 ==== */

/* ==== COPY BEGIN scrub.c:780-793 (scrub_writev) ==== */
static int scrub_writev(int fd, char *buf, int max, const char *fmt, ...)
				__attribute__ ((format (printf, 4, 5)));
static int scrub_writev(int fd, char *buf, int max, const char *fmt, ...)
{
	int ret;
	va_list args;

	va_start(args, fmt);
	ret = vsnprintf(buf, max, fmt, args);
	va_end(args);
	if (ret >= max)
		return ret - max;
	return scrub_write_buf(fd, buf, ret);
}
/* ==== COPY END scrub.c:780-793 ==== */

/* ==== COPY BEGIN scrub.c:795-798 (_SCRUB_SUM_macros) ==== */
#define _SCRUB_SUM(dest, data, name) dest->scrub_args.progress.name =	\
			data->resumed->p.name + data->scrub_args.progress.name
#define _SCRUB_COPY(dest, data, name) dest->scrub_args.progress.name =	\
			data->scrub_args.progress.name
/* ==== COPY END scrub.c:795-798 ==== */

/* ==== COPY BEGIN scrub.c:800-828 (scrub_resumed_stats) ==== */
static struct scrub_progress *scrub_resumed_stats(struct scrub_progress *data,
						  struct scrub_progress *dest)
{
	if (!data->resumed || data->skip)
		return data;

	_SCRUB_SUM(dest, data, data_extents_scrubbed);
	_SCRUB_SUM(dest, data, tree_extents_scrubbed);
	_SCRUB_SUM(dest, data, data_bytes_scrubbed);
	_SCRUB_SUM(dest, data, tree_bytes_scrubbed);
	_SCRUB_SUM(dest, data, read_errors);
	_SCRUB_SUM(dest, data, csum_errors);
	_SCRUB_SUM(dest, data, verify_errors);
	_SCRUB_SUM(dest, data, no_csum);
	_SCRUB_SUM(dest, data, csum_discards);
	_SCRUB_SUM(dest, data, super_errors);
	_SCRUB_SUM(dest, data, malloc_errors);
	_SCRUB_SUM(dest, data, uncorrectable_errors);
	_SCRUB_SUM(dest, data, corrected_errors);
	_SCRUB_COPY(dest, data, last_physical);
	dest->stats.canceled = data->stats.canceled;
	dest->stats.finished = data->stats.finished;
	dest->stats.t_resumed = data->stats.t_start;
	dest->stats.t_start = data->resumed->stats.t_start;
	dest->stats.duration = data->resumed->stats.duration +
							data->stats.duration;
	dest->scrub_args.devid = data->scrub_args.devid;
	return dest;
}
/* ==== COPY END scrub.c:800-828 ==== */

/* ==== COPY BEGIN scrub.c:830-836 (_SCRUB_KVWRITE_macros) ==== */
#define _SCRUB_KVWRITE(fd, buf, name, use)		\
	scrub_kvwrite(fd, buf, sizeof(buf), #name,	\
			use->scrub_args.progress.name)

#define _SCRUB_KVWRITE_STATS(fd, buf, name, use)	\
	scrub_kvwrite(fd, buf, sizeof(buf), #name,	\
			use->stats.name)
/* ==== COPY END scrub.c:830-836 ==== */

/* ==== COPY BEGIN scrub.c:838-841 (scrub_kvwrite) ==== */
static int scrub_kvwrite(int fd, char *buf, int max, const char *key, u64 val)
{
	return scrub_writev(fd, buf, max, "|%s:%lld", key, val);
}
/* ==== COPY END scrub.c:838-841 ==== */

/* ==== COPY BEGIN scrub.c:843-895 (scrub_write_file) ==== */
static int scrub_write_file(int fd, const char *fsid,
				struct scrub_progress *data, int n)
{
	int ret = 0;
	int i;
	char buf[1024];
	struct scrub_progress local;
	struct scrub_progress *use;

	if (n < 1)
		return -EINVAL;

	/* each -1 is to subtract one \0 byte, the + 2 is for ':' and '\n' */
	ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"
				SCRUB_FILE_VERSION "\n",
				(sizeof(SCRUB_FILE_VERSION_PREFIX) - 1) +
				(sizeof(SCRUB_FILE_VERSION) - 1) + 2);
	if (ret)
		return -EOVERFLOW;

	for (i = 0; i < n; ++i) {
		use = scrub_resumed_stats(&data[i], &local);
		if (scrub_write_buf(fd, fsid, strlen(fsid)) ||
		    scrub_write_buf(fd, ":", 1) ||
		    scrub_writev(fd, buf, sizeof(buf), "%lld",
					use->scrub_args.devid) ||
		    scrub_write_buf(fd, buf, ret) ||
		    _SCRUB_KVWRITE(fd, buf, data_extents_scrubbed, use) ||
		    _SCRUB_KVWRITE(fd, buf, tree_extents_scrubbed, use) ||
		    _SCRUB_KVWRITE(fd, buf, data_bytes_scrubbed, use) ||
		    _SCRUB_KVWRITE(fd, buf, tree_bytes_scrubbed, use) ||
		    _SCRUB_KVWRITE(fd, buf, read_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, csum_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, verify_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, no_csum, use) ||
		    _SCRUB_KVWRITE(fd, buf, csum_discards, use) ||
		    _SCRUB_KVWRITE(fd, buf, super_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, malloc_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, uncorrectable_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, corrected_errors, use) ||
		    _SCRUB_KVWRITE(fd, buf, last_physical, use) ||
		    _SCRUB_KVWRITE_STATS(fd, buf, t_start, use) ||
		    _SCRUB_KVWRITE_STATS(fd, buf, t_resumed, use) ||
		    _SCRUB_KVWRITE_STATS(fd, buf, duration, use) ||
		    _SCRUB_KVWRITE_STATS(fd, buf, canceled, use) ||
		    _SCRUB_KVWRITE_STATS(fd, buf, finished, use) ||
		    scrub_write_buf(fd, "\n", 1)) {
			return -EOVERFLOW;
		}
	}

	return 0;
}
/* ==== COPY END scrub.c:843-895 ==== */

/* ==== COPY BEGIN scrub.c:897-947 (scrub_write_progress) ==== */
static int scrub_write_progress(pthread_mutex_t *m, const char *fsid,
				struct scrub_progress *data, int n)
{
	int ret;
	int err;
	int fd = -1;
	int old;

	ret = pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);
	if (ret) {
		err = -ret;
		goto out3;
	}

	ret = pthread_mutex_lock(m);
	if (ret) {
		err = -ret;
		goto out2;
	}

	fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");
	if (fd < 0) {
		err = fd;
		goto out1;
	}
	err = scrub_write_file(fd, fsid, data, n);
	if (err)
		goto out1;
	err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");
	if (err)
		goto out1;

out1:
	if (fd >= 0) {
		ret = close(fd);
		if (ret)
			err = -errno;
	}

	ret = pthread_mutex_unlock(m);
	if (ret && !err)
		err = -ret;

out2:
	ret = pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, &old);
	if (ret && !err)
		err = -ret;

out3:
	return err;
}
/* ==== COPY END scrub.c:897-947 ==== */

/* ==== driver.c: harness main (NOT from scrub.c) ==== */
static const char *FSID = "11111111-2222-3333-4444-555555555555";
static const char *DIR  = "/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib/btrfs";
static const char *FINAL = "/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555";
static const char *TMPF  = "/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib/btrfs/scrub.status.11111111-2222-3333-4444-555555555555_tmp";

static void mkdirtree(void)
{
	mkdir("/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var", 0700);
	mkdir("/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/var/lib", 0700);
	mkdir(DIR, 0700);
}

static void clean_state(void)
{
	unlink(FINAL);
	unlink(TMPF);
}

/* mirrors scrub_write_progress() minus mutex/cancelstate (see report diff) */
static int record(struct scrub_progress *d, int n, int do_rename, long *written)
{
	int fd, err, ret;

	fd = scrub_open_file_w(SCRUB_DATA_FILE, FSID, "tmp");
	if (fd < 0)
		return fd;
	err = scrub_write_file(fd, FSID, d, n);
	if (!err && written)
		*written = lseek(fd, 0, SEEK_CUR);
	if (!err && do_rename)
		err = scrub_rename_file(SCRUB_DATA_FILE, FSID, "tmp");
	ret = close(fd);
	if (ret)
		err = -errno;
	return err;
}

static void fill_long(struct scrub_progress *d)
{
	u64 base = 1234567890123ULL;
	memset(d, 0, sizeof(*d));
	d->scrub_args.devid = 7;
	d->scrub_args.progress.data_extents_scrubbed = base + 1;
	d->scrub_args.progress.tree_extents_scrubbed = base + 2;
	d->scrub_args.progress.data_bytes_scrubbed   = base + 3;
	d->scrub_args.progress.tree_bytes_scrubbed   = base + 4;
	d->scrub_args.progress.read_errors           = base + 5;
	d->scrub_args.progress.csum_errors           = base + 6;
	d->scrub_args.progress.verify_errors         = base + 7;
	d->scrub_args.progress.no_csum               = base + 8;
	d->scrub_args.progress.csum_discards         = base + 9;
	d->scrub_args.progress.super_errors          = base + 10;
	d->scrub_args.progress.malloc_errors         = base + 11;
	d->scrub_args.progress.uncorrectable_errors  = base + 12;
	d->scrub_args.progress.corrected_errors      = base + 13;
	d->scrub_args.progress.last_physical         = base + 14;
	d->stats.t_start   = (time_t)(base + 15);
	d->stats.t_resumed = (time_t)(base + 16);
	d->stats.duration  = base + 17;
	d->stats.canceled  = 0;
	d->stats.finished  = 1;
	d->resumed = NULL;
	d->skip = 0;
}

static void fill_short(struct scrub_progress *d)
{
	memset(d, 0, sizeof(*d));
	d->scrub_args.devid = 7;
	d->scrub_args.progress.data_extents_scrubbed = 1;
	d->scrub_args.progress.tree_extents_scrubbed = 2;
	d->scrub_args.progress.data_bytes_scrubbed   = 3;
	d->scrub_args.progress.tree_bytes_scrubbed   = 4;
	d->scrub_args.progress.read_errors           = 5;
	d->scrub_args.progress.csum_errors           = 6;
	d->scrub_args.progress.verify_errors         = 7;
	d->scrub_args.progress.no_csum               = 8;
	d->scrub_args.progress.csum_discards         = 9;
	d->scrub_args.progress.super_errors          = 10;
	d->scrub_args.progress.malloc_errors         = 11;
	d->scrub_args.progress.uncorrectable_errors  = 12;
	d->scrub_args.progress.corrected_errors      = 13;
	d->scrub_args.progress.last_physical         = 14;
	d->stats.t_start   = 101;
	d->stats.t_resumed = 102;
	d->stats.duration  = 5;
	d->stats.canceled  = 0;
	d->stats.finished  = 1;
	d->resumed = NULL;
	d->skip = 0;
}

static long slurp(const char *path, char **out)
{
	int fd = open(path, O_RDONLY);
	struct stat st;
	char *buf;
	ssize_t n, off = 0;

	if (fd < 0)
		return -errno;
	if (fstat(fd, &st) < 0) { close(fd); return -errno; }
	buf = malloc(st.st_size + 1);
	if (!buf) { close(fd); return -ENOMEM; }
	while (off < st.st_size) {
		n = read(fd, buf + off, st.st_size - off);
		if (n <= 0)
			break;
		off += n;
	}
	close(fd);
	buf[off] = '\0';
	*out = buf;
	return off;
}

static void dump(const char *tag, const char *buf, long len)
{
	long i, j;

	printf("--- %s (%ld bytes) ---\n", tag, len);
	for (i = 0; i < len; i += 32) {
		printf("%08lx  ", i);
		for (j = 0; j < 32; ++j) {
			if (i + j < len)
				printf("%02x ", (unsigned char)buf[i + j]);
			else
				printf("   ");
		}
		printf(" |");
		for (j = 0; j < 32 && i + j < len; ++j) {
			unsigned char c = buf[i + j];
			putchar(c >= 32 && c < 127 ? c : '.');
		}
		printf("|\n");
	}
}

static void readback(const char *tag, int report_errors)
{
	int fd;
	struct scrub_file_record **p;
	int i;

	printf("\n### readback %s (report_errors=%d)\n", tag, report_errors);
	stub_warn_count = 0;
	fd = scrub_open_file_r(SCRUB_DATA_FILE, FSID);
	if (fd < 0) {
		printf("open failed: %d (%s)\n", fd, strerror(-fd));
		return;
	}
	p = scrub_read_file(fd, report_errors);
	close(fd);
	if (IS_ERR(p)) {
		printf("scrub_read_file -> ERR_PTR(%ld)\n", -PTR_ERR(p));
	} else if (!p) {
		printf("scrub_read_file -> NULL\n");
	} else {
		for (i = 0; p[i]; ++i) {
			char u[64];
			uuid_unparse(p[i]->fsid, u);
			printf("record[%d]: fsid=%s devid=%llu data_extents=%llu "
			       "last_physical=%llu t_start=%lld t_resumed=%lld "
			       "duration=%llu finished=%llu canceled=%llu\n",
			       i, u, (unsigned long long)p[i]->devid,
			       (unsigned long long)p[i]->p.data_extents_scrubbed,
			       (unsigned long long)p[i]->p.last_physical,
			       (long long)p[i]->stats.t_start,
			       (long long)p[i]->stats.t_resumed,
			       (unsigned long long)p[i]->stats.duration,
			       (unsigned long long)p[i]->stats.finished,
			       (unsigned long long)p[i]->stats.canceled);
		}
		printf("scrub_read_file -> %d record(s)\n", i);
		free_history(p);
	}
	printf("warnings emitted: %d, errors emitted: %d\n",
	       stub_warn_count, stub_err_count);
}

int main(void)
{
	struct scrub_progress longrec, shortrec;

	setvbuf(stdout, NULL, _IOLBF, 0);
	char *A = NULL, *B = NULL, *F = NULL;
	long lenA = 0, lenB = 0, lenF = 0, writtenLong = 0, writtenShort = 0;
	int err;

	mkdirtree();
	fill_long(&longrec);
	fill_short(&shortrec);

	/* --- baseline 0: long record alone, normal path (rename performed) --- */
	clean_state();
	err = record(&longrec, 1, 1, &writtenLong);
	lenA = slurp(FINAL, &A);
	printf("### case 0 (baseline): long record, rename performed\n");
	printf("record() -> %d, write offset at end = %ld, file size = %ld\n",
	       err, writtenLong, lenA);
	dump("A = final file, long record only", A, lenA);

	/* --- baseline 1: short record alone, fresh dir (no _tmp) --- */
	clean_state();
	err = record(&shortrec, 1, 1, &writtenShort);
	lenB = slurp(FINAL, &B);
	printf("\n### case 1 (baseline): short record, fresh dir, rename performed\n");
	printf("record() -> %d, write offset at end = %ld, file size = %ld\n",
	       err, writtenShort, lenB);
	dump("B = final file, short record only", B, lenB);

	/* --- case 2: REPRODUCTION --- */
	clean_state();
	printf("\n### case 2 (reproduction): long record, rename SKIPPED (_tmp left behind)\n");
	err = record(&longrec, 1, 0, &writtenLong);
	{
		char *T = NULL;
		long lenT = slurp(TMPF, &T);
		printf("record(long, do_rename=0) -> %d; _tmp size = %ld; final exists = %d\n",
		       err, lenT, access(FINAL, F_OK) == 0);
		free(T);
	}
	printf("now writing the SHORTER record through the normal path:\n");
	err = record(&shortrec, 1, 1, &writtenShort);
	lenF = slurp(FINAL, &F);
	printf("record(short, do_rename=1) -> %d, write offset at end = %ld, final file size = %ld\n",
	       err, writtenShort, lenF);
	dump("F = final file after short-over-long", F, lenF);

	printf("\n### case 2 invariants\n");
	printf("size(F)=%ld  size(A)=%ld  writtenShort=%ld  size(B)=%ld\n",
	       lenF, lenA, writtenShort, lenB);
	printf("CHECK size(F) == size(A)            : %s\n",
	       lenF == lenA ? "yes" : "NO");
	printf("CHECK F[0:writtenShort] == B        : %s\n",
	       (writtenShort == lenB && memcmp(F, B, lenB) == 0) ? "yes" : "NO");
	printf("CHECK F[writtenShort:] == A[writtenShort:] : %s\n",
	       (lenF >= writtenShort &&
		memcmp(F + writtenShort, A + writtenShort, lenF - writtenShort) == 0) ?
	       "yes" : "NO");
	printf("trailing bytes = %ld\n", lenF - writtenShort);
	printf("trailing bytes as text: \"");
	fwrite(F + writtenShort, 1, lenF - writtenShort, stdout);
	printf("\"\n");

	/* write the bytes out for external xxd/od receipts */
	{
		FILE *o;
		o = fopen("final.bin", "wb"); fwrite(F, 1, lenF, o); fclose(o);
		o = fopen("longA.bin", "wb"); fwrite(A, 1, lenA, o); fclose(o);
		o = fopen("freshshort.bin", "wb"); fwrite(B, 1, lenB, o); fclose(o);
	}

	/* --- case 3: control, short then long (longer next record) --- */
	clean_state();
	printf("\n### case 3 (control): short record, rename skipped, then LONGER record\n");
	err = record(&shortrec, 1, 0, NULL);
	printf("record(short, do_rename=0) -> %d\n", err);
	err = record(&longrec, 1, 1, &writtenShort);
	lenF = slurp(FINAL, &F);
	printf("record(long, do_rename=1) -> %d, final size = %ld (A size %ld)\n",
	       err, lenF, lenA);
	printf("CHECK final == A (no residue)       : %s\n",
	       (lenF == lenA && memcmp(F, A, lenA) == 0) ? "yes" : "NO");

	/* --- case 4: readback of the reproduced file, and controls --- */
	clean_state();
	record(&longrec, 1, 0, NULL);	/* leave _tmp */
	record(&shortrec, 1, 1, NULL);	/* shorter record renames over the tail */
	readback("REPRODUCED short-over-long file", 1);
	readback("REPRODUCED short-over-long file, report_errors=0", 0);

	clean_state();
	record(&longrec, 1, 1, NULL);
	readback("control: clean long record", 1);

	clean_state();
	record(&shortrec, 1, 1, NULL);
	readback("control: clean short record", 1);

	/* --- case 5: every later attempt reuses the same stale _tmp (still no O_TRUNC) --- */
	clean_state();
	printf("\n### case 5 (reuse): long record abandoned in _tmp, then three shorter attempts\n");
	record(&longrec, 1, 0, NULL);
	printf("_tmp after abandoned long record: size = %ld, final exists = %d\n",
	       slurp(TMPF, &F), access(FINAL, F_OK) == 0);
	free(F); F = NULL;
	{
		int k;
		for (k = 0; k < 3; ++k) {
			struct scrub_progress d;
			long w = 0;
			memset(&d, 0, sizeof(d));
			d.scrub_args.devid = 1 + k;
			d.scrub_args.progress.data_extents_scrubbed = k;
			d.scrub_args.progress.last_physical = k;
			d.stats.t_start = k;
			d.stats.finished = 1;
			record(&d, 1, 0, &w);            /* attempt fails/aborts before rename */
			printf("attempt %d: wrote %ld bytes into _tmp, _tmp size = %ld\n",
			       k, w, slurp(TMPF, &F));
			free(F); F = NULL;
		}
	}
	{
		struct scrub_progress d;
		long w = 0;
		memset(&d, 0, sizeof(d));
		d.scrub_args.devid = 9;
		d.scrub_args.progress.data_extents_scrubbed = 9;
		d.scrub_args.progress.last_physical = 9;
		d.stats.t_start = 9;
		d.stats.finished = 1;
		record(&d, 1, 1, &w);                    /* this one renames */
		lenF = slurp(FINAL, &F);
		printf("final attempt renames: wrote %ld bytes, final size = %ld, residue = %ld\n",
		       w, lenF, lenF - w);
		printf("trailing bytes as text: \"");
		fwrite(F + w, 1, lenF - w, stdout);
		printf("\"\n");
		readback("REUSED ABANDONED _tmp (3 failed attempts, then rename)", 1);
		free(F); F = NULL;
	}

	/* --- case 6: rename fails EACCES inside the copied error branch of scrub_write_progress --- */
	clean_state();
	printf("\n### case 6 (failure path): abandoned long _tmp, rename returns EACCES\n");
	err = record(&longrec, 1, 0, NULL);          /* _tmp = long record, final absent */
	printf("abandoned long _tmp: record err = %d, _tmp size = %ld\n",
	       err, slurp(TMPF, &F));
	free(F); F = NULL;
	if (chmod(DIR, 0500) != 0) {
		printf("chmod 0500 failed: %s\n", strerror(errno));
	} else {
		err = record(&shortrec, 1, 1, NULL);  /* open(existing _tmp) ok, rename EACCES */
		printf("record(short) with dir mode 0500 -> err = %d (%s)\n",
		       err, err ? strerror(-err) : "ok");
		printf("_tmp size after failed rename = %ld ; final exists = %d\n",
		       slurp(TMPF, &F), access(FINAL, F_OK) == 0);
		free(F); F = NULL;
		chmod(DIR, 0700);
		err = record(&shortrec, 1, 1, &writtenShort); /* same _tmp reused, rename ok */
		lenF = slurp(FINAL, &F);
		printf("record(short) retry after chmod 0700 -> err = %d, wrote %ld, final size = %ld (long was %ld)\n",
		       err, writtenShort, lenF, lenA);
		printf("CHECK final size > writtenShort (residue) : %s\n",
		       lenF > writtenShort ? "yes" : "NO");
		printf("trailing bytes as text: \"");
		fwrite(F + writtenShort, 1, lenF - writtenShort, stdout);
		printf("\"\n");
		readback("REPRODUCED VIA EACCES RENAME FAILURE", 1);
	}

	/* --- case 7: parity, my record() vs the real scrub_write_progress() --- */
	{
		pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
		char *R = NULL;
		long lenR;
		clean_state();
		printf("\n### case 7 (parity): real scrub_write_progress() vs driver record()\n");
		err = scrub_write_progress(&mtx, FSID, &longrec, 1);
		lenR = slurp(FINAL, &R);
		printf("real scrub_write_progress(long) -> %d, file size %ld\n", err, lenR);
		printf("CHECK real == case-0 driver bytes    : %s\n",
		       (lenR == lenA && memcmp(R, A, lenA) == 0) ? "yes" : "NO");
		clean_state();
		err = scrub_write_progress(&mtx, FSID, &shortrec, 1);
		free(R); R = NULL;
		lenR = slurp(FINAL, &R);
		printf("real scrub_write_progress(short) -> %d, file size %ld\n", err, lenR);
		printf("CHECK real == case-1 driver bytes    : %s\n",
		       (lenR == lenB && memcmp(R, B, lenB) == 0) ? "yes" : "NO");
		free(R);
	}

	/* --- case 8 (control): abandonment by a FAILED write leaves only a shorter prefix --- */
	{
		pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
		struct rlimit rl, saved;
		char *R = NULL;
		long lenR;
		clean_state();
		signal(SIGXFSZ, SIG_IGN);
		getrlimit(RLIMIT_FSIZE, &saved);
		rl.rlim_cur = 200;
		rl.rlim_max = saved.rlim_max;
		setrlimit(RLIMIT_FSIZE, &rl);
		printf("\n### case 8 (control): long record with RLIMIT_FSIZE=200 makes the write fail\n");
		err = scrub_write_progress(&mtx, FSID, &longrec, 1);
		setrlimit(RLIMIT_FSIZE, &saved);
		printf("real scrub_write_progress(long) -> %d (%s)\n",
		       err, err ? strerror(-err) : "ok");
		printf("_tmp size = %ld, final exists = %d\n",
		       slurp(TMPF, &R), access(FINAL, F_OK) == 0);
		free(R); R = NULL;
		err = scrub_write_progress(&mtx, FSID, &shortrec, 1);
		lenR = slurp(FINAL, &R);
		printf("then real short record -> %d, final size = %ld (short is %ld)\n",
		       err, lenR, lenB);
		printf("CHECK no residue (abandoned content was shorter) : %s\n",
		       (lenR == lenB && memcmp(R, B, lenB) == 0) ? "yes" : "NO");
		free(R);
	}

	free(A); free(B); free(F);
	return 0;
}
