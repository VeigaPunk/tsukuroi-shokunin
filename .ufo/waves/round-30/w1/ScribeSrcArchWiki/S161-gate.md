# S161 Gate row draft (unlanded; round 30, § Gate)

Column shape follows `corpus/lessons/round-29.md` § Gate (Source | URL | Opened | Located quote
(at most 25 words) | Location | Decision).

| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S161 | https://wiki.archlinux.org/title/Btrfs | 2026-10-22 | “will inaccurately report free space on a Btrfs partition as they do not account for both file and metadata usage” | `.ufo/waves/round-30/w1/ScribeSrcArchWiki/S161-archwiki-btrfs.html` line 1846, sha256 `73558a5cef7854cb4130ba88fbcacc10a228c502aed294f0b52bd2ed075d5523`; revision oldid 887521, last edited 2026-10-11T22:41 | **reject** as tier-B `mined`: this sentence restates the `df`-versus-`usage` point already carried by btrfs-filesystem(8) (S152:22-23, "not suitable for quick overview"; S152:367-368, `usage` "is supposed to replace the `btrfs filesystem df` command in the long run"), and no frozen token for D01, D02 or D05 occurs anywhere on the page. Flip: admit as tier-B `mined` when a knowledge statement needs this page's own operational remark that the btrfs-progs v7.1 docs do not state — the mixed RAID5/6 plus DUP-profile inaccuracy note at line 1850 or the temporary-device remedy at line 2181 — cited at a dated oldid and approved by the L1 |

Supporting locators (read this round, not quoted in the Gate row above):

- line 1850: “`btrfs filesystem usage` and `btrfs filesystem df` show inaccurate results if `RAID5`
  or `RAID6` profile coexist with other profiles in the same filesystem” — the page's only
  non-derivative caveat; cites btrfs-man5, and no host filesystem uses RAID5/6.
- line 1894: “On a single-device filesystem, a balance may be also useful for (temporarily)
  reducing the amount of allocated but unused (meta)data chunks.” — restates the usage-filter
  mechanism of btrfs-balance(8) S153:154-183 and its `usage=0` note at S153:118.
- lines 2174-2182 (Troubleshooting > No space left on device): a five-item list attributed to an
  external blog at line 2175 (“suggests and explains the following checks/steps”) plus a pointer to
  a second external page at line 2182; it states no mechanism of its own. The one operational item,
  line 2181 (“Balance cannot run because the filesystem is full (temporarily add a device …)”),
  is the remedy implied by the work-space explanation already in S153:97-100.

## Quote verification (run 2026-10-22 in this seat)

```
$ sed -n '1846p' S161-archwiki-btrfs.html | grep -cF 'will inaccurately report free space on a Btrfs partition as they do not account for both file and metadata usage'
1
$ printf '%s\n' 'will inaccurately report free space on a Btrfs partition as they do not account for both file and metadata usage' | wc -w
20
$ sed -n '1894p' S161-archwiki-btrfs.html | grep -cF 'On a single-device filesystem, a balance may be also useful for (temporarily) reducing the amount of allocated but unused (meta)data chunks.'
1
$ sed -n '2175p' S161-archwiki-btrfs.html | grep -cF 'suggests and explains the following checks/steps'
1
$ sha256sum S161-archwiki-btrfs.html
73558a5cef7854cb4130ba88fbcacc10a228c502aed294f0b52bd2ed075d5523  S161-archwiki-btrfs.html
```

The command prefix for each `sed`/`sha256sum` line is
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcArchWiki`; each
`grep -cF` printed 1, so each quoted fragment is verbatim on exactly one line of the saved bytes.
