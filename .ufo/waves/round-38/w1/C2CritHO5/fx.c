/* C2CritHO5: probe alpm_trans_commit's Pre-hook gate with a fake root.
 * usage: fx <root/> <dbpath/> <extra_hookdir> <pkgname>
 * read-only w.r.t. the host: everything lives under the fake root. */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <alpm.h>

static void logcb(void *ctx, alpm_loglevel_t level, const char *fmt, va_list args)
{
	(void)ctx;
	const char *tag;
	switch(level) {
		case ALPM_LOG_ERROR:   tag = "E"; break;
		case ALPM_LOG_WARNING: tag = "W"; break;
		case ALPM_LOG_DEBUG:   tag = "D"; break;
		default:               tag = "F"; break;
	}
	fprintf(stderr, "[%s] ", tag);
	vfprintf(stderr, fmt, args);
}

int main(int argc, char **argv)
{
	alpm_errno_t err = 0;
	alpm_handle_t *h;
	alpm_db_t *db;
	alpm_pkg_t *pkg;
	alpm_list_t *i, *data = NULL;
	int rc;

	if(argc < 5) {
		fprintf(stderr, "usage: %s <root/> <dbpath/> <extra_hookdir> <pkg> [logfile]\n", argv[0]);
		return 2;
	}

	h = alpm_initialize(argv[1], argv[2], &err);
	if(!h) {
		printf("RESULT init_fail str=\"%s\"\n", alpm_strerror(err));
		return 3;
	}

	printf("ROOT=%s\n", alpm_option_get_root(h));
	printf("DBPATH=%s\n", alpm_option_get_dbpath(h));

	if(alpm_option_add_hookdir(h, argv[3]) != 0) {
		printf("RESULT add_hookdir_fail str=\"%s\"\n", alpm_strerror(alpm_errno(h)));
		alpm_release(h);
		return 4;
	}
	printf("HOOKDIRS:");
	for(i = alpm_option_get_hookdirs(h); i; i = alpm_list_next(i)) {
		printf(" %s", (char *)i->data);
	}
	printf("\n");

	alpm_option_set_logcb(h, logcb, NULL);
	if(argc > 5 && alpm_option_set_logfile(h, argv[5]) != 0) {
		printf("RESULT set_logfile_fail str=\"%s\"\n", alpm_strerror(alpm_errno(h)));
	}

	db = alpm_get_localdb(h);
	pkg = alpm_db_get_pkg(db, argv[4]);
	if(!pkg) {
		printf("RESULT pkg_missing pkg=%s\n", argv[4]);
		alpm_release(h);
		return 5;
	}

	if(alpm_trans_init(h, ALPM_TRANS_FLAG_NODEPS) != 0) {
		printf("RESULT trans_init_fail str=\"%s\"\n", alpm_strerror(alpm_errno(h)));
		alpm_release(h);
		return 6;
	}
	if(alpm_remove_pkg(h, pkg) != 0) {
		printf("RESULT remove_pkg_fail str=\"%s\"\n", alpm_strerror(alpm_errno(h)));
		alpm_release(h);
		return 7;
	}
	if(alpm_trans_prepare(h, &data) != 0) {
		printf("RESULT prepare_fail str=\"%s\"\n", alpm_strerror(alpm_errno(h)));
		alpm_release(h);
		return 8;
	}

	rc = alpm_trans_commit(h, &data);
	err = alpm_errno(h);
	printf("RESULT rc=%d errnum=%d str=\"%s\" is_hook_failed=%d\n",
			rc, (int)err, alpm_strerror(err),
			err == ALPM_ERR_TRANS_HOOK_FAILED ? 1 : 0);
	alpm_release(h);
	return 0;
}
