/* SPDX-License-Identifier: LGPL-2.1-or-later */
int main(int argc, char **argv) {
        Manager m = {0};
        uint64_t used = UINT64_MAX, available = UINT64_MAX;
        if (argc != 2) return 2;
        int r = manager_determine_path_usage(&m, argv[1], &used, &available);
        printf("{\"return\":%d,\"used\":%" PRIu64 ",\"free\":%" PRIu64 "}\n", r, used, available);
        return r < 0 ? 1 : 0;
}
