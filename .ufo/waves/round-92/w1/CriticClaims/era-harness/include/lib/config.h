#pragma once
#include <stddef.h>
#include <stdbool.h>
int init_config(size_t config_size);
char *config_get_value(const char *config, size_t index, const char *key);
struct conf_tuple { const char *value1; const char *value2; };
struct menu_entry { char *name; struct menu_entry *parent, *sub, *next; char *body; bool expanded; char *comment; };
struct conf_tuple config_get_tuple(const char *config, size_t index, const char *key1, const char *key2);
