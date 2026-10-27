/* Which thread does a process-directed SIGINT reach? (leader by default) */
#define _GNU_SOURCE
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

static volatile sig_atomic_t where;	/* 1 = leader, 2 = worker */
static pid_t leader_tid;

static void h(int sig)
{
	(void)sig;
	where = (syscall(SYS_gettid) == leader_tid) ? 1 : 2;
}

static void *worker(void *arg)
{
	(void)arg;
	usleep(200 * 1000);
	return NULL;
}

int main(void)
{
	struct sigaction sa;
	pthread_t t;

	setvbuf(stdout, NULL, _IOLBF, 0);
	leader_tid = syscall(SYS_gettid);
	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = h;		/* sa_flags = 0, like the pinned child handler */
	sigaction(SIGINT, &sa, NULL);
	pthread_create(&t, NULL, worker, NULL);
	usleep(50 * 1000);
	kill(getpid(), SIGINT);
	pthread_join(t, NULL);
	printf("process-directed SIGINT handled by %s\n",
	       where == 1 ? "leader/main" : where == 2 ? "worker" : "no-thread");
	return 0;
}
