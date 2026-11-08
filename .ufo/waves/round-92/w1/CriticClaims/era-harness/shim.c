#include <stddef.h>
extern char *config_addr;
void harness_set_addr(char *p, size_t sz){(void)sz; config_addr=p;}
