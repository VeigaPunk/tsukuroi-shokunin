/* Analogue of btrfs-progs `scrub start -B` signal shape (Linux, one process):
 * - one process, 3 "device" threads blocked in a syscall (pipe read stands in
 *   for ioctl(BTRFS_IOC_SCRUB)),
 * - main/leader thread parked in pthread_join, as scrub.c:1608,
 * - SIGINT handler installed process-wide with sa_flags=0 (scrub.c:438-443),
 *   performing one "fs-wide cancel" (writing one byte per device),
 * - SIGCONT (def :_DFL, and with an observer handler) sent to the process.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

#define NDEV 3
static int pfd[2];
static volatile sig_atomic_t int_hits, cont_hits, done_count;
static volatile pid_t int_tid, cont_tid;

static void on_int(int sig) {
    (void)sig;
    int_hits++;
    int_tid = (pid_t)syscall(SYS_gettid);
    for (int i = 0; i < NDEV; i++)        /* fs-wide cancel: unattended */
        if (write(pfd[1], "x", 1) != 1) _exit(9);
}
static void on_cont(int sig) { (void)sig; cont_hits++; cont_tid = (pid_t)syscall(SYS_gettid); }

struct arg { int idx; volatile int ret; };
static void *dev_thread(void *p) {
    struct arg *a = p; char c;
    a->ret = (int)read(pfd[0], &c, 1);    /* stands in for the scrub ioctl */
    done_count++;
    return NULL;
}
static void *sender(void *p) {
    (void)p;
    usleep(200000);
    kill(getpid(), SIGCONT);              /* phase 1: observer handler installed */
    usleep(150000);
    printf("done_before_SIGINT=%d (SIGCONT did not abort the blocked reads)\n", (int)done_count);
    kill(getpid(), SIGINT);
    usleep(150000);
    struct sigaction d; memset(&d, 0, sizeof d);
    d.sa_handler = SIG_DFL;
    sigaction(SIGCONT, &d, NULL);         /* phase 2: default disposition */
    kill(getpid(), SIGCONT);
    usleep(100000);
    return NULL;
}
int main(void) {
    pthread_t dev[NDEV], snd; struct arg a[NDEV] = {{0},{1},{2}};
    alarm(5);
    if (pipe(pfd)) return 8;
    struct sigaction sa; memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_int;               /* sa_flags = 0, as scrub.c:438 */
    if (sigaction(SIGINT, &sa, NULL)) return 7;
    struct sigaction sc; memset(&sc, 0, sizeof sc);
    sc.sa_handler = on_cont;              /* observer, to prove delivery */
    sigaction(SIGCONT, &sc, NULL);
    printf("pid=%d main_tid=%ld\n", (int)getpid(), (long)syscall(SYS_gettid));
    for (int i = 0; i < NDEV; i++) pthread_create(&dev[i], NULL, dev_thread, &a[i]);
    pthread_create(&snd, NULL, sender, NULL);
    for (int i = 0; i < NDEV; i++) pthread_join(dev[i], NULL);   /* scrub.c:1608 */
    pthread_join(snd, NULL);
    printf("sigint_handler_invocations=%d sigint_handler_tid=%ld (main_tid=%ld)\n",
           (int)int_hits, (long)int_tid, (long)syscall(SYS_gettid));
    printf("sigcont_observer_invocations=%d\n", (int)cont_hits);
    printf("device_reads_returned=%d of %d\n", (int)done_count, NDEV);
    for (int i = 0; i < NDEV; i++) printf("dev[%d]_read_ret=%d\n", i, a[i].ret);
    printf("alive_after_default_SIGCONT=1\n");
    return int_hits == 1 ? 0 : 1;
}
