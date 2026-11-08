#define NOT_CHILD      (-1)
#define DIRECT_CHILD   0
#define INDIRECT_CHILD 1
static int is_child(size_t current_depth, size_t index) {
    char *buf = config_get_entry_name(index);
    if (buf == NULL)
        return NOT_CHILD;
    int ret;
    if (strlen(buf) < current_depth + 1) {
        ret = NOT_CHILD;
    } else {
        ret = DIRECT_CHILD;
        for (size_t j = 0; j < current_depth; j++) {
            if (buf[j] != '/') {
                ret = NOT_CHILD;
                break;
            }
        }
        if (ret == DIRECT_CHILD && buf[current_depth] == '/')
            ret = INDIRECT_CHILD;
    }
    pmm_free(buf, strlen(buf) + 1);
    return ret;
}

static bool is_directory(size_t current_depth, size_t index) {
    switch (is_child(current_depth + 1, index + 1)) {
        default:
        case NOT_CHILD:
            return false;
        case INDIRECT_CHILD:
            bad_config = true;
            panic(true, "config: Malformed config file. Parentless child.");
        case DIRECT_CHILD:
            return true;
    }
}
