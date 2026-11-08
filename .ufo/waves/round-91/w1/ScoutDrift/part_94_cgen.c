static char *config_get_entry_name(size_t index) {
    if (!config_ready || config_addr == NULL)
        return NULL;

    char *p = config_addr;

    for (size_t i = 0; i <= index; i++) {
        while (*p != '/') {
            if (!*p)
                return NULL;
            p++;
        }
        p++;
        if ((p - 1) != config_addr && *(p - 2) != '\n')
            i--;
    }

    p--;

    size_t len = 0;
    while (p[len] != SEPARATOR && p[len] != '\0') {
        len++;
    }

    char *ret = ext_mem_alloc(len + 1);
    memcpy(ret, p, len);
    ret[len] = 0;
    return ret;
}
