# Independent pinned-source derivation

Axes: depth and operability. Companion not yet reviewed; this is not a verdict.

`before/journald-manager.c` SHA256 observed: `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`.
`before/journalctl.xml` SHA256 observed: `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`.
Both match expected.json pins.

Assumptions: directory open and fstatvfs succeed; each case describes an individual directory-entry contribution, not a return code or whole-filesystem usage. Function initializes ret_used=0 at :115, filters names at :119–121, stats without following symlinks at :123, skips stat failure at :124–125, skips nonregular modes at :128–129, and adds blocks*512 at :131.

| Case | Independent derivation | Contribution |
|---|---|---:|
| U1 | active.journal passes suffix; successful regular stat; 8*512. Apparent size 1048576 unused. | 4096 |
| U2 | archived.journal~ passes second suffix; successful regular stat; 16*512. | 8192 |
| U3 | ignored.txt fails both suffix tests before stat. | 0 |
| U4 | link.journal passes suffix; no-follow stat returns symlink mode; nonregular rejected. | 0 |
| U5 | directory.journal passes suffix; directory mode nonregular rejected. | 0 |
| U6 | unstatable.journal passes suffix; failed fstatat logs and continues, not fatal. | 0 |

Source does not inspect journal headers, contents, file ages or archival state. A label archived.journal~ is not itself evidence of a valid archived journal. `ret_free` is independently f_bsize*f_bavail at :114, not a sum/subtraction based on these six rows. The immediate caller cache_space_refresh :161–166 propagates negative directory/fstatvfs failures, then stores distinct vfs_used and vfs_available fields. Initial opendir/fstatvfs failure returns before setting ret_used; zero contribution for U6 must not be generalized to those failures.

Manual journalctl.xml :941–944 says --disk-usage includes active and archived journals; :969–973 limits vacuum to archived files. That manual is contextual and does not establish identical CLI implementation or turn these six entries into CLI integration coverage.

LSP unavailable: read xd://lsp returned 'No such tool'. No semantic references/definition/diagnostics service was available; source excerpts and literal search are fallback evidence only. No runtime/test invocation by this reviewer. No installs or privileged probes.
