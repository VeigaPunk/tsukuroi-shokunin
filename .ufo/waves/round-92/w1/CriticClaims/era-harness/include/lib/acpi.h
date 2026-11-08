#pragma once
#include <stddef.h>
#include <stdint.h>
struct smbios_entry_point_64 { uint64_t table_address; uint32_t table_maximum_size; };
struct smbios_entry_point_32 { uint32_t table_address; uint16_t table_length; uint8_t number_of_structures; };
extern struct smbios_entry_point_64 *smbios_entry_64;
extern struct smbios_entry_point_32 *smbios_entry_32;
void acpi_get_smbios(void **a, void **b);
void *smbios_get_table(uint64_t addr, size_t size);
