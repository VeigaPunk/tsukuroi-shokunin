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
