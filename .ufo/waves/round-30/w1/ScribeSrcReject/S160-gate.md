# S160 gate row (round 30, wave 1, ScribeSrcReject)

Draft row for the round-30 lesson section `## Gate` (same six columns as `corpus/lessons/round-29.md:13`).

| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S160 | https://archive.kernel.org/oldwiki/btrfs.wiki.kernel.org/index.php/FAQ.html | 2026-10-22 | "Until at least 3.14, balance is sometimes needed to fix filesystem full issues" | `.ufo/waves/round-30/w1/ScribeSrcReject/S160-oldwiki-faq.html` line 536, sha256 `961d9b6b9913f1013bf33ea9ee27d75b141f77ec71d97a7ef8d17f5e14b925cc`; the archive banner on line 43 reads "OBSOLETE CONTENT" and "This wiki has been archived and the content is no longer updated."; the ENOSPC recipe's command `btrfs balance start /mountpoint -dlimit=3` is on line 216, and the MediaWiki footer on line 892 dates the revision 1 June 2022 (oldid=33687); the live host btrfs.wiki.kernel.org answers 301 Moved Permanently to this archived URL (2026-10-22) | **reject**: archived and self-declared obsolete (line 43) with no kernel or btrfs-progs pin (line 536 only says "at least 3.14"), and its ENOSPC recipe is absent from the v7.1 manual — `Documentation/btrfs-balance.rst` at tag v7.1 (sha256 `ca245fbf145166ec24c8a84864ffd44fbef98ca66551fdf50cfb8be552d22cea`) documents `-dusage=0` (line 246) and `-dusage=50` (line 168) and contains no `limit` filter at all, while the page's diagnosis is read off `btrfs fi df`, which `Documentation/btrfs-filesystem.rst` at v7.1 (sha256 `a0ce33f5babd8521f0956cf6ce934412c2ab2d6e93f32c2c08ff9ae63f8597bc`) calls "not suitable for quick overview" (lines 22-23) and says `btrfs filesystem usage` is "supposed to replace" (lines 366-367); the C1 counter's rule R4 admits only rows whose status is exactly `mined`. Flip: a claim is explicitly historical (the pre-3.14 partial-balance practice), grounded in a version-pinned btrfs-progs or kernel file of that era, with this page cited only as commentary |

Quote checks (each prints `1`):

```
sed -n '536p' S160-oldwiki-faq.html | grep -cF 'Until at least 3.14, balance is sometimes needed to fix filesystem full issues'
sed -n '43p'  S160-oldwiki-faq.html | grep -cF 'This wiki has been archived and the content is no longer updated.'
sed -n '216p' S160-oldwiki-faq.html | grep -cF 'btrfs balance start /mountpoint -dlimit=3'
sed -n '892p' S160-oldwiki-faq.html | grep -cF 'This page was last modified on 1 June 2022, at 07:21.'
```

Comparison of the page's ENOSPC / balance advice with btrfs-progs v7.1:

| Point | FAQ (archived, line) | v7.1 documentation (line) | Verdict |
|---|---|---|---|
| Partial balance to reclaim data allocation | `btrfs balance start /mountpoint -dlimit=3` (216) | no `limit` filter anywhere in `btrfs-balance.rst` (0 occurrences); the documented reclaim filters are `-dusage=0` (246) and `-dusage=50` (168) | recipe not grounded in v7.1 |
| Free work space test | `btrfs fi show` (206), used equal to total on each device (208) | `*size* - *used* = *free work space*` from `btrfs filesystem show` (`btrfs-balance.rst` 104-114) | consistent |
| Metadata "close to full" threshold | block reserve, "typically 512 MiB" (213) | GlobalReserve total "is dynamic based on the filesystem size, usually not larger than 512MiB" (`btrfs-filesystem.rst` 48-50) | consistent in substance, legacy term |
| Diagnostic command | `btrfs fi df` throughout (211, 214, 227) | `df` is "a debugging helper", output "not suitable for quick overview" (22-23); `usage` is "supposed to replace" it (366-367) | superseded |
| Version pin | "Until at least 3.14" (536); kernel bug 74101; "mkfs.btrfs since v4.2" (588) | v7.1, no such caveat | unpinned |
