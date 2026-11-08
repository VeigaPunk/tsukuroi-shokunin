#pragma once
#include <stddef.h>
#include <stdbool.h>
struct volume { int fd; size_t size; };
struct file_handle { int fd; size_t size; };
extern bool case_insensitive_fopen;
struct file_handle *limine_fopen(struct volume *part, const char *path);
void limine_fclose(struct file_handle *f);
size_t limine_fread(struct file_handle *f, void *buf, size_t offset, size_t count);
