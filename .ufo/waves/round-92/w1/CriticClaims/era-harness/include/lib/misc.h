#pragma once
#include <stddef.h>
#include <stdbool.h>
void panic(bool x, const char *fmt, ...);
extern bool secure_boot_active;
extern bool editor_enabled;
int digit_to_int(char c);
const char *current_arch(void);
const char *current_firmware(void);
const char *loader_arch(void);
#define CHECKED_ADD(a,b,fail) ({ size_t _r=(a)+(b); if(_r<(a)){fail;} _r; })
#define CHECKED_MUL(a,b,fail) ({ size_t _r=(a)*(b); if((a)!=0&&_r/(a)!=(b)){fail;} _r; })
