# S1Scout probe index — round 72 / w1

`route2.txt`    C1 sources re-opened through raw.githubusercontent.com/kmod-project/kmod/v34/<path>
                (HTTP 200 ×3, sha256 equal to the committed snapshots and to src/SOURCES.json, `cmp`
                byte-identical). Includes the v34.2 cross-check that found `libkmod-config.c`
                differing at patch level while both S302 quotes survive (+2 lines).
`quotes.tsv`    the six requested strings with exact line:col spans in the committed snapshots,
                word counts, pipe/double-quote flags, per-quote distinct-token scores, plus the
                three pipe-bearing code anchors that must stay out of a quote cell and the one
                35-word candidate that exceeds the 25-word ceiling.
`host-enum.txt` read-only host re-capture against before/host.txt: kernel, kmod, five modprobe.d
                paths + modes, /lib resolution, names only, /proc/cmdline, 136 /sys/module/*/parameters.
                HOST_DRIFT=0; only `ls` ordering of /usr/lib/modprobe.d differs (same name set).

Headline: ROUTE2_OK=3/3, QUOTES_LOCATED=6/6, PIPES_OR_QUOTES=2, HOST_DRIFT=0.
Seat report: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-72/w1/S1Scout.md
