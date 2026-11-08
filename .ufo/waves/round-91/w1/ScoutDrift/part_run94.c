static void run94(const char *text) {
    config_size = strlen(text) + 2;
    config_addr = ext_mem_alloc(config_size);
    memcpy(config_addr, text, strlen(text));
    config_addr[config_size - 2] = '\n';
    config_addr[config_size - 1] = '\0';
    { // upstream 12.9.4 strip loop (config.c raw 527-552)
        for (size_t i = 0; i < config_size; i++) {
            size_t skip = 0;
            if (config_addr[i] == ' ' || config_addr[i] == '\t') {
                while (i + skip < config_size && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')) {
                    skip++;
                }
                if (i + skip < config_size && config_addr[i + skip] == '\n') {
                    goto skip_loop;
                }
                skip = 0;
            }
            while (i + skip < config_size
                && ((config_addr[i + skip] == '\r')
                    || ((!i || config_addr[i - 1] == '\n') && (config_addr[i + skip] == ' ' || config_addr[i + skip] == '\t')))
            ) {
                skip++;
            }
skip_loop:
            if (skip) {
                for (size_t j = i; j < config_size - skip; j++)
                    config_addr[j] = config_addr[j + skip];
                config_size -= skip;
                i--;
            }
        }
    }
    config_ready = true;
    menu_tree = create_menu_tree_94(NULL, 1, 0);
    v94_cut();
    const char *v0 = config_get_value(NULL, 0, "HASH_MISMATCH_PANIC");
    char vbuf[64]; snprintf(vbuf, sizeof vbuf, "%s", v0 ? v0 : "(null)");
    const char *m0 = config_get_value(NULL, 0, "MEASURED_BOOT");
    char mbuf[64]; snprintf(mbuf, sizeof mbuf, "%s", m0 ? m0 : "(null)");
    printf("v12.9.4  hash_mismatch_panic=%-8s measured_boot=%-8s visible=[%s]\n",
           vbuf, mbuf, config_addr);
}

