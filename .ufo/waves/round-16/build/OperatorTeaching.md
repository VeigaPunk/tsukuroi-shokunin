# OperatorTeaching — corpus/lessons/operator-* probe

Question: do any operator-* lesson files exist under corpus/lessons/?

Result: **absence**. `corpus/lessons/` contains exactly 10 entries, none matching
`operator-*` or any case variant of `operator`.

Evidence (observed):
- `glob corpus/lessons/operator-*` → no files.
- `glob corpus/lessons/operator*` and `*operator*` → no files.
- Shell glob (nullglob, dotglob) in that directory: `total=10
  operator_exact=0 operator_anycase=0`.
- Complete listing, exact names: round-1.md, round-1-verifier-spotcheck.md,
  round-12.md, round-12-verifier-spotcheck.md, round-13.md,
  round-13-verifier-spotcheck.md, round-14.md, round-14-verifier-spotcheck.md,
  round-15.md, round-15-verifier-spotcheck.md.

Limits: `read` directory listings cap child listings at 12; 10 entries are below
that cap and the independent shell glob count agrees (10), so the listing is
complete. No file contents were read; only directory names were enumerated, all
under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. No files outside the scoped
directory were accessed. No tools installed, no commands run beyond directory-name
enumeration.
