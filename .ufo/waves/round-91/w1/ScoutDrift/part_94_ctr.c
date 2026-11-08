static struct menu_entry *create_menu_tree_94(struct menu_entry *parent,
                                           size_t current_depth, size_t index) {
    if (current_depth > MAX_MENU_NESTING) {
        bad_config = true;
        panic(true, "config: Menu nesting too deep (max %u)", MAX_MENU_NESTING);
    }

    struct menu_entry *root = NULL, *prev = NULL;

    for (size_t i = index; ; i++) {
        switch (is_child(current_depth, i)) {
            case NOT_CHILD:
                return root;
            case INDIRECT_CHILD:
                continue;
            case DIRECT_CHILD:
                break;
        }

        struct menu_entry *entry = ext_mem_alloc(sizeof(struct menu_entry));

        if (root == NULL)
            root = entry;

        char *name = config_get_entry_name(i);

        bool default_expanded = name[current_depth] == '+';

        char *n = &name[current_depth + default_expanded];
        while (*n == ' ') {
            n++;
        }

        entry->name = strdup(n);
        pmm_free(name, strlen(name) + 1);
        entry->parent = parent;

        size_t entry_size;
        char *config_entry = config_get_entry(&entry_size, i);
        entry->body = ext_mem_alloc(entry_size + 1);
        memcpy(entry->body, config_entry, entry_size);
        entry->body[entry_size] = 0;

        if (is_directory(current_depth, i)) {
            entry->sub = create_menu_tree_94(entry, current_depth + 1, i + 1);
            entry->expanded = default_expanded;
        }

        char *comment = config_get_value(entry->body, 0, "COMMENT");
        if (comment != NULL) {
            entry->comment = strdup(comment);
        }

        if (prev != NULL)
            prev->next = entry;
        prev = entry;
    }
}
