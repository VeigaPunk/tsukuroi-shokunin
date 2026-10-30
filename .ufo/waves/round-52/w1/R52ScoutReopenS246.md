VERDICT: supports

# W-S5: independent S246/S247 reopen

Axes: freshness; byte identity; citation fidelity. Confidence: high for the four pinned files and five literal samples; no semantic admission verdict.

## Scope and version discrepancy

Evidence revision: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Both registry rows are **v7.2.11**, not the item's parenthetical v7.1: `corpus/SOURCES.md:255-256`, extracted with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/SOURCES.md`; preserved as `R52ScoutReopenS246/sources.md:255-256`. Grounding entry agrees at `corpus/knowledge/btrfs-scrub-grounding-r45.md:1-3`, preserved as `R52ScoutReopenS246/gr.md:1-3`. I followed the actual row URLs and pins. v7.1 was not fetched and is not verified by this report.

## Per-source results

Accessed 2026-10-30, receipt timestamp 05:43:23 UTC. All four curl requests exited 0 and returned HTTP/2 200. Raw response bodies, headers, curl logs, and frozen-revision snapshots are retained under `.ufo/waves/round-52/w1/R52ScoutReopenS246/`; machine comparison is `receipt.json`.

Commands: `curl --fail --location --retry 1 --max-time 120 --dump-header <name>.headers --output <name>.live <URL>`; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:.ufo/waves/round-45/frozen/src/<name>`; SHA256 over both bodies. Each live digest below equals both its frozen-revision snapshot digest and registry pin at `sources.md:255-256`.

| Source | Reopened URL | SHA256 (live = frozen = pin) |
|---|---|---|
| S246 cmdline.c | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/cmdline.c?h=v7.2.11 | `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d` |
| S246 vsprintf.c | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/vsprintf.c?h=v7.2.11 | `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca` |
| S246 kstrtox.c | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/kstrtox.c?h=v7.2.11 | `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4` |
| S247 dev-replace.c | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11 | `f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a` |

S246: three files independently reopened; all pinned byte identities hold. S247: file independently reopened; pinned byte identity holds. A preliminary working-tree `sha256sum -c SHA256SUMS` returned all five `OK` (including out-of-scope systemd), but the conclusions above use the subsequently extracted frozen-revision bytes, not mutable working-tree evidence.

## Five citation samples

Each expected literal was extracted from the frozen grounding entry, compared against the indicated fresh response line after stripping indentation only, and returned `match: true` in `receipt.json`. URLs above, access date 2026-10-30; each quote below is under 25 words. Paths in this table are relative to this report's receipt directory.

| Row / grounding line | Live location | Located quote | Result |
|---|---|---|---|
| GR1 `gr.md:38` | `cmdline.c.live:156` | `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);` | exact after indentation removal |
| GR1 `gr.md:56` | `vsprintf.c.live:86` | `cp = _parse_integer_fixup_radix(startp, &base);` | exact after indentation removal |
| GR1 `gr.md:66` | `kstrtox.c.live:33` | `*base = 8;` | exact after indentation removal |
| GR2 `gr.md:141` | `dev-replace.c.live:701` | `ret = btrfs_scrub_dev(fs_info, src_device->devid, 0,` | exact after indentation removal |
| GR2 `gr.md:149` | `dev-replace.c.live:1268` | `&dev_replace->scrub_progress, false, true);` | exact after indentation removal |

## Limits and handling

Observed: HTTP status, full-file digest equality, and five literal/line matches. Inference: these samples provide fresh support for the frozen citations; they do not establish all GR1/GR2 semantics or completeness. No exported-contract change or semantic reference search was undertaken; no LSP absence claim is made. No admission counter, selftest, or scoring battery was run. No tools installed or updated.

Handling deviations: an initial corpus copy was inadvertently written to `/fast/scratch/tmp_r52_gr.md`, then removed immediately; all retained copies are under the authorized receipt path. One concurrent reader attempted to enter scratch before its creation and failed; subsequent reads succeeded after creation. No tracked file was edited. Scratch was removed after receipt preservation.
