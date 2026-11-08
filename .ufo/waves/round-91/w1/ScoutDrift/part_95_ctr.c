static struct menu_entry *create_menu_tree_95v(void) {
    struct menu_entry *root = NULL;
    struct menu_entry *last_at_depth[MAX_MENU_NESTING + 2] = {0};

    char *p = config_addr;
    if (p == NULL) {
        return NULL;
    }

    while (*p != '\0') {
        if (*p == '/' && (p == config_addr || *(p - 1) == '\n')) {
            break;
        }
        p++;
    }

    if (*p == '\0') {
        return NULL;
    }

    // One allocation for all the entries, as each of its own takes a page.
    size_t entry_count = 1;
    for (char *q = p + 1; *q != '\0'; q++) {
        if (*q == '/' && *(q - 1) == '\n') {
            entry_count++;
        }
    }
    struct menu_entry *entries = ext_mem_alloc_counted(entry_count, sizeof(struct menu_entry));
    size_t entries_used = 0;

    if (p > config_addr) {
        *(p - 1) = '\0';
    }

    while (*p != '\0') {
        size_t depth = 0;
        while (*p == '/') {
            depth++;
            p++;
        }

        if (depth > MAX_MENU_NESTING) {
            bad_config = true;
            panic(true, "config: Menu nesting too deep (max %u)", MAX_MENU_NESTING);
        }

        if (depth > 1 && last_at_depth[depth - 1] == NULL) {
            bad_config = true;
            panic(true, "config: Malformed config file. Parentless child.");
        }

        bool default_expanded = (*p == '+');
        if (default_expanded) {
            p++;
        }

        while (*p == ' ' || *p == '\t') {
            p++;
        }

        char *name = p;
        while (*p != '\n' && *p != '\0') {
            p++;
        }
        if (*p == '\n') {
            *p = '\0';
            p++;
        }

        char *body = "";
        if (*p != '/') {
            body = p;
            while (*p != '\0') {
                if (*p == '/' && *(p - 1) == '\n') {
                    break;
                }
                p++;
            }

            if (p > body && *(p - 1) == '\n') {
                *(p - 1) = '\0';
            }
        }

        struct menu_entry *entry = &entries[entries_used++];
        entry->name = name;
        entry->body = body;
        entry->parent = last_at_depth[depth - 1];
        entry->expanded = default_expanded;

        if (entry->parent != NULL) {
            if (entry->parent->sub == NULL) {
                entry->parent->sub = entry;
            }
        }

        if (last_at_depth[depth] != NULL && last_at_depth[depth]->parent == entry->parent) {
            last_at_depth[depth]->next = entry;
        } else if (depth == 1 && root == NULL) {
            root = entry;
        }

        last_at_depth[depth] = entry;
        for (size_t d = depth + 1; d <= MAX_MENU_NESTING; d++) {
            last_at_depth[d] = NULL;
        }
    }

    return root;
}
