    // remove windows carriage returns and spaces at the start and end of lines, if any
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
            i--; // re-examine character shifted into position i
        }
    }

