char *config_get_value(const char *config, size_t index, const char *key) {
    // Static buffer for return values.
    // Callers must copy the result if they need persistence across calls.
    #define CONFIG_VALUE_BUF_SIZE 4096
    static char buf[CONFIG_VALUE_BUF_SIZE];

    if (!key || !config_ready)
        return NULL;

    if (config == NULL)
        config = config_addr;

    // config_ready does not imply a config file was loaded: the blank entry
    // editor sets it with config_addr still unset.
    if (config == NULL)
        return NULL;

    size_t key_len = strlen(key);

    for (size_t i = 0; config[i]; i++) {
        if (!strncasecmp(&config[i], key, key_len) && config[i + key_len] == ':') {
            if (i && config[i - 1] != SEPARATOR)
                continue;
            if (index--)
                continue;
            i += key_len + 1;
            while (config[i] == ' ' || config[i] == '\t') {
                i++;
            }
            size_t value_len;
            for (value_len = 0;
                 config[i + value_len] != SEPARATOR && config[i + value_len];
                 value_len++);
            if (value_len >= CONFIG_VALUE_BUF_SIZE) {
                value_len = CONFIG_VALUE_BUF_SIZE - 1;
            }
            memcpy(buf, config + i, value_len);
            buf[value_len] = '\0';
            lastkey = config + i;
            return buf;
        }
    }

    return NULL;
}
