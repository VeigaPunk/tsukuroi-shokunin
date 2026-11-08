    size_t write = 0;
    bool at_line_start = true;
    for (size_t read = 0; read < config_size - 1; read++) {
        char c = config_addr[read];

        if (c == '\r') {
            continue;
        }

        if (at_line_start && (c == ' ' || c == '\t')) {
            continue;
        }

        if (c == '\n') {
            while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) {
                write--;
            }
            at_line_start = true;
        } else {
            at_line_start = false;
        }

        config_addr[write++] = c;
    }

    while (write > 0 && (config_addr[write - 1] == ' ' || config_addr[write - 1] == '\t')) {
        write--;
    }
    config_addr[write++] = '\0';
    config_size = write;
