Era differential harness (CriticClaims, round 92).

src/config394.c and src/config395.c are byte copies of
`.ufo/waves/round-92/before/src/limine-v12.9.4-common_lib_config.c` and
`...-v12.9.5-common_lib_config.c` with one edit each: `static char *config_addr;` made
non-static so shim.c can point it at the buffer. include/ holds stub headers; harness.c
stubs malloc/panic/blake2b/smbios and prints `config_get_value(NULL,0,<key>)` plus the
visible buffer prefix after `init_config(size)`.

Build and run (from this directory, cc = gcc/clang):

  cc -O0 -g -Iinclude -Dfopen=limine_fopen -Dfread=limine_fread -Dfclose=limine_fclose \
     -c src/config394.c -o obj-394.o
  cc -O0 -g -Iinclude -Dfopen=limine_fopen -Dfread=limine_fread -Dfclose=limine_fclose \
     -c src/config395.c -o obj-395.o
  cc -O0 -g -Iinclude harness.c shim.c obj-394.o -o h394
  cc -O0 -g -Iinclude harness.c shim.c obj-395.o -o h395
  ./h394 <conf> hash_mismatch_panic measured_boot wallpaper term_font

The 30 shapes used are listed in ../era-differential-run.txt; every DIFF it prints is a
key-visibility difference between the eras, and all of them are the first-line-is-entry
class. `h395` on a file whose first line is an entry shows the visible buffer is the
entry label (`/boot`), not an empty string.
