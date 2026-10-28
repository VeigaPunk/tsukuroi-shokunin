VERDICT: supports

S248 re-opened live on 2026-10-28T21:13:21Z. The raw v262 `man/systemd.kill.xml` is byte-identical to the pin `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72` and to the round-45 snapshot. None of the GR3 quoted lines fall outside the SOURCES anchor range 62-116. `lint-grounding-r51.py --emit-gaps` does not list S248.

## Re-open

Command (cwd scratch; 120 s cap; finished in one shot):

```
date -u +%Y-%m-%dT%H:%M:%SZ
curl -sSfL --max-time 120 'https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml' -o /fast/scratch/hyaku/tsukuroi-r51/R51ScoutReopenS248/live.bin
wc -c live.bin; sha256sum live.bin
```

Observed:

- access time UTC: `2026-10-28T21:13:21Z` (printed immediately before and after curl; both stamps that second)
- curl exit 0
- size: 11224 bytes
- sha256: `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`
- LF only, file ends in newline, 209 lines (`splitlines` 209)

Pin named in the item: `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`.

Snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/systemd.kill.xml`: 11224 bytes, same sha256. `SHA256SUMS` line 3: `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72  systemd.kill.xml`. `FETCH.txt` line 4: `GET https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml -> systemd.kill.xml`.

`cmp -s` live vs snapshot: byte-identical (`python3` `live==snap`, both length 11224). `diff -q` produced no output. `diff -u` of numbered lines 62-116 is an empty file (0 bytes). No differing lines, so no first-20-line diff.

Receipt copy: `.ufo/waves/round-51/w1/R51ScoutReopenS248/live.bin` (same sha256; `cmp` against the snapshot again printed `RECEIPT_BYTE_IDENTICAL`).

No tool was installed.

## Cited lines (live vs snapshot)

Anchor span asked: 62-116. Quoted lines named by the item, each equal to the same snapshot line (`nl -ba` / `sed -n`). Leading whitespace kept as in the file.

| line | equal to snapshot | live text |
|---|---|---|
| 68 | yes | `        <para>If set to <option>control-group</option>, all remaining processes in the control group of this` |
| 91 | yes | `          <listitem><para>the delay configured via the <varname>TimeoutStopSec=</varname> has passed` |
| 96 | yes | `        the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via` |
| 101 | yes | `        <para>Defaults to <option>control-group</option>.</para>` |
| 108 | yes | `        <listitem><para>Specifies which signal to use when stopping a service. This controls the signal that` |
| 114 | yes | `        <para>Note that, right after sending the signal specified in this setting, systemd will always send` |
| 115 | yes | `        <constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>` |

Lines 62 and 116 of the same span were also compared: 62 is `      <varlistentry>` (equal); 116 is empty (equal). The whole 62-116 block matches the snapshot.

Frozen entry quotes at `2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md` GR3 (lines 202, 204, 206, 208, 210, 212, 214) are the stripped live lines, exact:

- :202 quotes line 68
- :204 quotes line 91
- :206 quotes line 96
- :208 quotes line 101
- :210 quotes line 108
- :212 quotes line 114
- :214 quotes line 115

## Anchor range and gaps

`git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 257, anchor cell (column `anchor`):

`tag v262 (peeled commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492), man/systemd.kill.xml lines 62-116; raw bytes sha256 448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`

Declared range: **62-116** inclusive. Lines 68, 91, 96, 101, 108, 114, 115 all fall inside it. Outside that range: **none**.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` exit 0. Full block (receipt `emit-gaps.txt`):

```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139
- S243 sysfs.c: 1288, 2015
- S247 dev-replace.c: 1197
```

S248 is absent. That matches an empty outside-list. The same block is the entry's `### Range gaps (R51)` at the frozen revision (`btrfs-scrub-grounding-r45.md`, immediately after the GR rows).

## Gate

- Access date: 2026-10-28 (UTC timestamp 2026-10-28T21:13:21Z)
- URL: https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml
- sha256: `448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72`
- Located quote, live line 115 (11 words), the GR3 SIGCONT quote at entry line 214: `<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>`

Not done: no second fetch (the first curl succeeded); no line-by-line print of the unquoted lines 63-67, 69-90, 92-95, 97-100, 102-107, 109-113 beyond the empty `diff -u` of 62-116.
