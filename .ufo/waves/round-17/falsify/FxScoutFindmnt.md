# FxScoutFindmnt — findmnt --mountpoint canonicalization

**Attacked:** emulation step 1 — `findmnt --mountpoint <R>/new_root` returns the `<R>/sysroot` mount (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:40-42`), relied on at `corpus/knowledge/boot-chain-r17.md:55-56`. **Verdict: SURVIVES** (confidence high).

[obs] util-linux 2.42.4 man page: `-C, --nocanonicalize` — “Do not canonicalize paths at all. This option affects the comparing of paths and the evaluation of tags (LABEL, UUID, etc.).” `-M, --mountpoint` — “Explicitly define the mountpoint file or directory. See also --target.” https://manpages.debian.org/testing/util-linux/findmnt.8.en.html §OPTIONS (2.42.4-1, accessed 2026-10-20; man7.org timed out, local page identical).

[obs] Source v2.42.4: `findmnt.c:1868-1869` `-C`→`FL_NOCACHE`; `:1992-1997` `-M` sets `FL_STRICTTARGET`, falling through to `-T`'s `set_match(COL_TARGET,…)`; `:2161-2167` default builds and attaches the libmount cache. `findmnt.c:1216` matches with `mnt_fs_match_target(fs,m,cache)`; `libmount/src/fs.c:1787` “The 2nd and 3rd attempts are not performed when @cache is NULL”, attempt 2 being `realpath(@target)`; `cache.c:660` → `lib/canonicalize.c:141` `realpath(path, NULL)`.

[inf] `--mountpoint` differs from `--target` only by suppressing parent-directory fallback (`findmnt.c:2207-2215`), not by disabling canonicalization; the hook passes no `-C`. [obs] Host run: `step1 … [tmpfs rc=0]`, `step1b … [realroot R/sysroot]` (E:40-42), on the byte-identical 2.42.4 binary (hash `0b539bae…`, E:11-15). [unk] none material.

Scope: executed=ls -l /usr/share/man/man8/findmnt.8.gz, zcat findmnt.8.gz|gzip>/tmp/findmnt-local.txt.gz, zcat findmnt.8.gz|sed -n 1,400p|head -400>/tmp/findmnt-local.txt, wc -l /tmp/findmnt-local.txt, grep -n -A4 -B2 'canonicalize\|nocanonicalize\|mountpoint' /tmp/findmnt-local.txt|cut -c1-300|head -120
