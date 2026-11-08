    size_t s;
    char *c = config_get_entry(&s, 0);
    if (c != NULL) {
        while (*c != '/' && c > config_addr) {
            c--;
        }
        if (*c == '/' && c > config_addr) {
            c[-1] = 0;
        }
    }

