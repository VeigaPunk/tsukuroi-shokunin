/* gitspy — LD_PRELOAD constructor that records, for every exec of a process whose
 * argv[0] basename is "git", the git child's own view of the contract variables.
 * Report-only instrumentation: it observes, never alters, the child.
 * Log line (tab separated): argv0 \t HOME \t PATH \t GIT_CONFIG_GLOBAL \t
 * GIT_CONFIG_NOSYSTEM \t GIT_CEILING_DIRECTORIES \t LC_ALL \t cwd \t LD_PRELOAD
 * Destination: $SPY_LOG (appended, O_APPEND, one write per child). */
#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static const char *g(const char *k) {
    const char *v = getenv(k);
    return v ? v : "-";
}

static void base(const char *p, char *out, size_t n) {
    const char *s = strrchr(p, '/');
    s = s ? s + 1 : p;
    snprintf(out, n, "%s", s);
}

__attribute__((constructor)) static void spy(void) {
    const char *log = getenv("SPY_LOG");
    if (!log || !*log) return;
    char cmd[4096];
    ssize_t r = readlink("/proc/self/exe", cmd, sizeof(cmd) - 1);
    if (r <= 0) return;
    cmd[r] = 0;
    char name[256];
    base(cmd, name, sizeof(name));
    if (strcmp(name, "git") != 0 && strcmp(name, "git.real") != 0) return;
    char cwd[4096];
    if (!getcwd(cwd, sizeof(cwd))) snprintf(cwd, sizeof(cwd), "-");
    char line[16384];
    int n = snprintf(line, sizeof(line), "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
                     name, g("HOME"), g("PATH"), g("GIT_CONFIG_GLOBAL"),
                     g("GIT_CONFIG_NOSYSTEM"), g("GIT_CEILING_DIRECTORIES"),
                     g("LC_ALL"), cwd, g("LD_PRELOAD"));
    if (n <= 0) return;
    int fd = open(log, O_WRONLY | O_APPEND | O_CREAT, 0644);
    if (fd < 0) return;
    ssize_t w = write(fd, line, (size_t)n);
    (void)w;
    close(fd);
}
