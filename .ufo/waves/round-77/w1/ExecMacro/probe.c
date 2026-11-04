#include <inttypes.h>
#include <stdio.h>
#include "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src/macro.h"

struct vector {
    const char *id;
    uint64_t used, free, keep_free, min_use, max_use;
};

int main(void) {
    const struct vector vectors[] = {
        {"A1", UINT64_C(100), UINT64_C(1000), UINT64_C(100), UINT64_C(0), UINT64_C(2000)},
        {"A2", UINT64_C(100), UINT64_C(50), UINT64_C(100), UINT64_C(0), UINT64_C(2000)},
        {"A3", UINT64_C(100), UINT64_C(100), UINT64_C(100), UINT64_C(0), UINT64_C(2000)},
        {"A4", UINT64_C(100), UINT64_C(1000), UINT64_C(100), UINT64_C(0), UINT64_C(500)},
        {"A5", UINT64_C(100), UINT64_C(50), UINT64_C(100), UINT64_C(300), UINT64_C(2000)},
        {"A6", UINT64_C(700), UINT64_C(50), UINT64_C(100), UINT64_C(0), UINT64_C(500)},
    };
    for (size_t i = 0; i < sizeof(vectors) / sizeof(vectors[0]); ++i) {
        const struct vector *v = &vectors[i];
        const uint64_t avail = LESS_BY(v->free, v->keep_free);
        const uint64_t limit = CLAMP(v->used + avail, v->min_use, v->max_use);
        const uint64_t available = LESS_BY(limit, v->used);
        printf("%s %" PRIu64 " %" PRIu64 " %" PRIu64 "\n", v->id, avail, limit, available);
    }
    return 0;
}
