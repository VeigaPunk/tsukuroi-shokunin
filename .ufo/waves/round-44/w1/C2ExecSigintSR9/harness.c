/*
 * C2ExecSigintSR9 harness: compiles lines 416-444 of the pinned
 * btrfs-progs v7.1 cmds/scrub.c verbatim (handlers.h) and observes
 * (1) the disposition each handler installer produces,
 * (2) that a process-directed SIGINT with the child handler installed
 *     leaves the main thread alive across pthread_join,
 * (3) that a SIGINT delivered to a worker thread makes its poll() return
 *     EINTR, and
 * (4) the exact `canceled = !!ret` mapping.
 * No btrfs fd, no ioctl on a real filesystem, no privileged call.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <linux/btrfs.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include "handlers.h"	/* verbatim scrub.c:416-444 */

static void report_flags(const char *name)
{
	struct sigaction q;

	memset(&q, 0, sizeof(q));
	if (sigaction(SIGINT, NULL, &q)) {
		printf("%s QUERY-FAILED errno=%d\n", name, errno);
		return;
	}
	printf("%s sa_flags=0x%08x SA_RESTART=%d handler=%s\n", name,
	       (unsigned)q.sa_flags, !!(q.sa_flags & SA_RESTART),
	       q.sa_handler == scrub_sigint_record_progress ? "pinned-child"
	       : q.sa_handler == SIG_IGN ? "SIG_IGN"
	       : q.sa_handler == SIG_DFL ? "SIG_DFL" : "other");
}

static void *sleeper(void *arg)
{
	(void)arg;
	usleep(200 * 1000);
	return NULL;
}

static void *poller(void *arg)
{
	struct pollfd p = { .fd = *(int *)arg, .events = POLLIN, .revents = 0 };
	int r;

	errno = 0;
	r = poll(&p, 1, 5000);
	printf("worker poll_ret=%d errno=%d (%s)\n", r, r < 0 ? errno : 0,
	       r < 0 ? strerror(errno) : "n/a");
	return NULL;
}

static int wpipe[2];

static void *blocked_writer(void *arg)
{
	char buf[4096] = { 0 };
	ssize_t w;

	(void)arg;
	errno = 0;
	w = write(wpipe[1], buf, sizeof(buf));
	printf("worker write_ret=%zd errno=%d (%s)\n", w, w < 0 ? errno : 0,
	       w < 0 ? strerror(errno) : "n/a");
	return NULL;
}

int main(void)
{
	int fd, pfd[2], ret;
	pthread_t t;

	setvbuf(stdout, NULL, _IOLBF, 0);

	/* (1) dispositions */
	scrub_handle_sigint_parent();
	report_flags("parent-install");
	fd = open("cancel.target", O_RDONLY | O_CREAT, 0600);
	if (fd < 0) {
		printf("open cancel.target failed errno=%d\n", errno);
		return 1;
	}
	ret = scrub_handle_sigint_child(fd);
	printf("child-install ret=%d cancel_fd=%d\n", ret, cancel_fd);
	report_flags("child-install");

	/* (2) process-directed SIGINT while main is in pthread_join */
	pthread_create(&t, NULL, sleeper, NULL);
	usleep(50 * 1000);
	kill(getpid(), SIGINT);		/* process-directed, as systemd does */
	ret = pthread_join(t, NULL);
	printf("main pthread_join ret=%d (0 = main thread survived the SIGINT)\n",
	       ret);

	/* (3) SIGINT delivered to a worker thread that is in poll() */
	if (pipe(pfd) == 0) {
		pthread_create(&t, NULL, poller, &pfd[0]);
		usleep(50 * 1000);
		pthread_kill(t, SIGINT);	/* thread-directed delivery */
		pthread_join(t, NULL);
	} else {
		printf("pipe failed errno=%d\n", errno);
	}

	/* (4) a blocked write() in a worker with the pinned handler: EINTR */
	if (pipe(wpipe) == 0) {
		char fill[4096] = { 0 };
		int fl = fcntl(wpipe[1], F_GETFL);

		fcntl(wpipe[1], F_SETFL, fl | O_NONBLOCK);
		while (write(wpipe[1], fill, sizeof(fill)) > 0)
			;	/* fill the pipe */
		fcntl(wpipe[1], F_SETFL, fl & ~O_NONBLOCK);
		pthread_create(&t, NULL, blocked_writer, NULL);
		usleep(50 * 1000);
		pthread_kill(t, SIGINT);
		pthread_join(t, NULL);
	} else {
		printf("pipe for write test failed errno=%d\n", errno);
	}

	/* (5) the exact expression at scrub.c:969 */
	{
		int one = -1, zero = 0;

		printf("ret=%d -> canceled=%d ; ret=%d -> canceled=%d "
		       "(errno not consulted)\n", one, !!one, zero, !!zero);
	}

	return 0;
}
