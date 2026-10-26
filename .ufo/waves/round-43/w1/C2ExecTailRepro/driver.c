
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
