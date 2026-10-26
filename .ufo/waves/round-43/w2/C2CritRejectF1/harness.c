/* preamble (stubs) -- types, UAPI structs, warning/error */
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
#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"
#define SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"
#define SCRUB_FILE_VERSION_PREFIX "scrub status"
#define SCRUB_FILE_VERSION "1"
struct scrub_stats {
	time_t t_start;
	time_t t_resumed;
	u64 duration;
	u64 finished;
	u64 canceled;
	int in_progress;
};

/* TBD: replace with #include "linux/ioprio.h" in some years */
#if !defined (IOPRIO_H)
#define IOPRIO_WHO_PROCESS 1
#define IOPRIO_CLASS_SHIFT 13
#define IOPRIO_PRIO_VALUE(class, data) \
		(((class) << IOPRIO_CLASS_SHIFT) | (data))
#define IOPRIO_CLASS_IDLE 3
#endif

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
static void free_history(struct scrub_file_record **last_scrubs)
{
	struct scrub_file_record **l = last_scrubs;
	if (!l || IS_ERR(l))
		return;
	while (*l)
		free(*l++);
	free(last_scrubs);
}
#define _SCRUB_KVREAD(ret, i, name, avail, l, dest) if (ret == 0) {	  \
	ret = scrub_kvread(i, sizeof(#name), avail, l, #name, dest.name); \
}

/*
 * returns 0 if the key did not match (nothing was read)
 *         1 if the key did match (success)
 *        -1 if the key did match and an error occurred
 */
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
#define _SCRUB_INVALID do {						\
	if (report_errors)						\
		warning("invalid data on line %d pos "			\
			"%d state %d (near \"%.*s\") at %s:%d",		\
			lineno, i, state, 20 > avail ? avail : 20,	\
			l + i,	__FILE__, __LINE__);			\
	goto skip;							\
} while (0)
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
static int scrub_write_buf(int fd, const void *data, int len)
{
	int ret;
	ret = write(fd, data, len);
	return ret - len;
}

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
#define _SCRUB_SUM(dest, data, name) dest->scrub_args.progress.name =	\
			data->resumed->p.name + data->scrub_args.progress.name
#define _SCRUB_COPY(dest, data, name) dest->scrub_args.progress.name =	\
			data->scrub_args.progress.name

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

#define _SCRUB_KVWRITE(fd, buf, name, use)		\
	scrub_kvwrite(fd, buf, sizeof(buf), #name,	\
			use->scrub_args.progress.name)

#define _SCRUB_KVWRITE_STATS(fd, buf, name, use)	\
	scrub_kvwrite(fd, buf, sizeof(buf), #name,	\
			use->stats.name)

static int scrub_kvwrite(int fd, char *buf, int max, const char *key, u64 val)
{
	return scrub_writev(fd, buf, max, "|%s:%lld", key, val);
}
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
int main(int argc, char **argv)
{
    /* one device record: devid = 1 (matches S241 capture root devid=1) */
    struct scrub_progress sp;
    memset(&sp, 0, sizeof(sp));
    sp.scrub_args.devid = 1;
    sp.scrub_args.start = 0;
    sp.scrub_args.progress.data_extents_scrubbed = 11;
    sp.scrub_args.progress.data_bytes_scrubbed = 22;
    sp.scrub_args.progress.csum_errors = 33;
    sp.scrub_args.progress.last_physical = 44;
    sp.stats.t_start = 1000;
    sp.stats.t_resumed = 1001;
    sp.stats.duration = 5;
    sp.stats.canceled = 0;
    sp.stats.finished = 0;   /* unfinished -> resume condition "canceled || !finished" true */

    const char *fsid = "1d02a454-c549-4a35-b567-89d60902af8e"; /* S241 root fsid */
    const char *rec_path = argv[1];

    int fd = open(rec_path, O_RDWR | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) { perror("open"); return 1; }
    int wr = scrub_write_file(fd, fsid, &sp, 1);
    if (wr) { fprintf(stderr, "scrub_write_file -> %d\n", wr); return 2; }
    /* keep fd open: scenario B appends on the same fd (no O_TRUNC, write starts at current offset) */
    /* scenario B: a RESUMED device (sp.resumed set, skip=0) — writer path via
       scrub_resumed_stats; devid must still be emitted (scrub.c:826 copies it) */
    struct scrub_progress sp2;
    struct scrub_file_record oldrec;
    memset(&sp2, 0, sizeof(sp2));
    memset(&oldrec, 0, sizeof(oldrec));
    uuid_parse(fsid, oldrec.fsid);
    oldrec.devid = 1;
    oldrec.stats.t_start = 1500;
    oldrec.stats.duration = 3;
    oldrec.stats.finished = 0;
    oldrec.p.data_extents_scrubbed = 100;
    oldrec.p.last_physical = 999;
    sp2.scrub_args.devid = 1;
    sp2.scrub_args.progress.data_extents_scrubbed = 77;
    sp2.scrub_args.progress.data_bytes_scrubbed = 88;
    sp2.scrub_args.progress.csum_errors = 99;
    sp2.scrub_args.progress.last_physical = 1234;
    sp2.stats.t_start = 2000;
    sp2.stats.duration = 7;
    sp2.stats.canceled = 0;
    sp2.stats.finished = 0;
    sp2.resumed = &oldrec;
    sp2.skip = 0;
    wr = scrub_write_file(fd, fsid, &sp2, 1);
    close(fd);

    /* raw file bytes */
    fd = open(rec_path, O_RDONLY);
    char raw[2048]; int n = read(fd, raw, sizeof(raw) - 1); close(fd);
    raw[n] = 0;
    printf("RAW RECORD (%d bytes):\n%s", n, raw);

    /* read back through the verbatim reader */
    fd = open(rec_path, O_RDONLY);
    struct scrub_file_record **recs = scrub_read_file(fd, 1);
    close(fd);
    if (IS_ERR(recs)) { fprintf(stderr, "scrub_read_file -> %ld\n", PTR_ERR(recs)); return 3; }
    int cnt = 0;
    if (recs) for (struct scrub_file_record **r = recs; *r; r++) {
        char fsid_out[BTRFS_FSID_SIZE * 2 + 1];
        uuid_unparse((*r)->fsid, fsid_out);
        printf("PARSED record[%d]: fsid=%s devid=%llu data_extents=%llu data_bytes=%llu csum_errors=%llu last_physical=%llu t_start=%lld t_resumed=%lld duration=%llu canceled=%llu finished=%llu\n",
               cnt, fsid_out,
               (unsigned long long)(*r)->devid,
               (unsigned long long)(*r)->p.data_extents_scrubbed,
               (unsigned long long)(*r)->p.data_bytes_scrubbed,
               (unsigned long long)(*r)->p.csum_errors,
               (unsigned long long)(*r)->p.last_physical,
               (long long)(*r)->stats.t_start,
               (long long)(*r)->stats.t_resumed,
               (unsigned long long)(*r)->stats.duration,
               (unsigned long long)(*r)->stats.canceled,
               (unsigned long long)(*r)->stats.finished);
        cnt++;
    }
    printf("records=%d warnings=%d errors=%d\n", cnt, warn_count, err_count);

    /* resume selection, verbatim from scrub_start loop (scrub.c:1427-1438) */
    u64 devid = 1;
    struct scrub_file_record *last_scrub = NULL;
    int i; for (i = 0; recs[i]; i++)
        if (recs[i]->devid == devid) { last_scrub = recs[i]; break; }
    int n_resume = 0;
    if (last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished)) {
        n_resume++;
        printf("RESUME-SELECT: device devid=%llu selected, resumed start=last_physical=%llu\n",
               (unsigned long long)devid, (unsigned long long)last_scrub->p.last_physical);
    } else {
        printf("RESUME-SELECT: not selected (last_scrub=%s)\n", last_scrub ? "found" : "NULL");
    }
    printf("n_resume=%d\n", n_resume);
    free_history(recs);
    return 0;
}
