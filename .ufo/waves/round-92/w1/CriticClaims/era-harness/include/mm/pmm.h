#pragma once
#include <stdlib.h>
static inline void *ext_mem_alloc(size_t n){return calloc(1,n?n:1);}
static inline void *ext_mem_alloc_counted(size_t c,size_t n){return calloc(c?c:1,n?n:1);}
static inline void pmm_free(void *p,size_t n){(void)n;free(p);}
