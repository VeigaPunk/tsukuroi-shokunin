#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
__attribute__((constructor)) static void mark(void) {
    const char *log = getenv("R36MARKLOG");
    if (!log) return;
    char comm[64] = {0};
    FILE *f = fopen("/proc/self/comm", "r");
    if (f) { if (!fgets(comm, sizeof comm, f)) comm[0] = 0; fclose(f); }
    for (char *p = comm; *p; p++) if (*p == '\n') *p = 0;
    const char *m = getenv("R36LEAKMARK"), *lp = getenv("LD_PRELOAD");
    FILE *o = fopen(log, "a");
    if (!o) return;
    fprintf(o, "pid=%d comm=%s mark=%s LD_PRELOAD=%s\n", (int)getpid(), comm,
            m ? m : "-", lp ? lp : "-");
    fclose(o);
}
