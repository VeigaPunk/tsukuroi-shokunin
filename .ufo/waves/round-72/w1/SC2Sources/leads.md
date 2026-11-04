# Round 72 — SOURCES.md `## Leads (unopened)` line (draft)

The round-71 bullet stays in place as filed; this line is appended after it and closes that lead. No
other lead line changes. The working tree already carries a `- Round-72 lead (2026-11-03): kmod's
compiled config-path priority table … not opened this round` bullet; this line supersedes it in one
respect only — that bullet says the table was not opened, while this seat did fetch the file read-only
to locate the array. If the L1 prefers the shorter bullet, the fetch sentence below is the part that
must not be lost.

- Round-72 closure (2026-11-03): the round-71 lead above is closed — the kmod man page was reached this
  round at `man/modprobe.d.5.scd` (tag v34, HTTP 200; committed snapshot sha256
  `aa1a869e57db31c8187a436b5eab3047394da5fd779794e1cdd4ccad598ee46e`) and is opened as S301, joined by
  the implementation rows S302 (`libkmod/libkmod-config.c`) and S303 (`tools/modprobe.c`). What remains
  unopened is kmod's config-path priority table itself: the compiled `default_config_paths` array in
  `libkmod/libkmod.c` (lines 44-50 at v34). A read-only fetch of that file (19158 bytes, sha256
  `a3899a59ee468c1f5b1b5e59de163f589ad0384968ca08e95cc3d6ddc9923b17`) served only to locate the array
  for this line; no registry row cites it and no rule statement is drawn from it, so the code-side order
  of the default directories stays unregistered.
