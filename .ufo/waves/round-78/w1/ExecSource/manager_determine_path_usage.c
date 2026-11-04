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
