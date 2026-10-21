## Attack
Test C2's 13-row `/boot/limine.conf` event table against both declared event-source probes as captured at revision `8e5916360f2dfe7bc4eb4ba144081af555900116`. Reconstruct the probe output records, compare them with the table, and verify each row's capture line, timestamp, and assigned writer signature. Specifically check that EV-01 (2026-10-11) is in the pacman-log search and distinguish that whole-file search from the journal probe's date window.

## Method
Read-only inspection; no host probes or gates run. The JSON and captures were read from the working tree after their SHA-256 digests matched the blobs at `8e59163` and `7cc59c8`.

Commands used for the core checks:

```sh
git cat-file -p 8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json > /tmp/fx_bw.json
sha256sum .ufo/waves/round-19/l1-capture/host-capture-r19.txt .ufo/waves/round-19/l1-capture/host-capture-r19b.txt .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
git cat-file -p 8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19b.txt | sha256sum
grep -n "Updated: /boot/limine.conf" .ufo/waves/round-19/l1-capture/host-capture-r19.txt
grep -n "Updated: /boot/limine.conf" .ufo/waves/round-19/l1-capture/host-capture-r19b.txt
grep -n "Updated: /boot/limine.conf" .ufo/waves/round-19/l1-capture/host-capture-r19c.txt
```

I also ran this read-only Python check from the repository root; it compares the event rows with their captured probe output lines and checks every row's quoted substring and writer signature (the plugin signature is regex-valued):

```sh
python3 -c 'import json,pathlib,re
D=json.load(open("corpus/knowledge/boot-writers-r19.json")); C={c["path"]:pathlib.Path(c["path"]).read_text().splitlines() for c in D["captures"]}; W={w["id"]:w for w in D["writers"]}
J=".ufo/waves/round-19/l1-capture/host-capture-r19c.txt"; P=".ufo/waves/round-19/l1-capture/host-capture-r19b.txt"
jout=[(n,s) for n,s in enumerate(C[J],1) if 11<=n<=20 and "Updated: /boot/limine.conf" in s]; pout=[(n,s) for n,s in enumerate(C[P],1) if 1689<=n<=1703 and "[ALPM-SCRIPTLET] Updated: /boot/limine.conf" in s]
for cap,out in ((J,jout),(P,pout)):
 rows=sorted((e["line"],C[cap][e["line"]-1]) for e in D["events"] if e["capture"]==cap and "Updated: /boot/limine.conf" in C[cap][e["line"]-1]); print(cap,"row set matches probe output:",rows==out,"count:",len(out),"lines:",[n for n,s in out])
checks=[]
for e in D["events"]:
 s=C[e["capture"]][e["line"]-1]; sig=W[e["writer"]]["signature"]["value"]; ok=(e["quote"] in s and (bool(re.search(sig,s)) if e["writer"]=="W-SNAPPER-PLUGIN" else sig in s)); checks.append(ok)
print("event rows quote + timestamp + writer signature:",sum(checks),"/",len(checks),"pass")'
```

## Verdict
**CONFIRM — C2 event-table enumeration and attribution.** The two declared probe outputs reproduce exactly 10 journal events plus 3 pacman-log events; the table has no missing or extra event within those probe result sets. All 13 cited lines pass the quote, timestamp, and writer-signature check.

## Evidence
- `corpus/knowledge/boot-writers-r19.json:18-28` declares the two sources. Its journal source is `host-capture-r19c.txt`; its pacman source is `host-capture-r19b.txt`.
- The journal command and output are captured at `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:5-21`. The command uses `--since "2026-10-19 00:00"`; lines 11-20 are exactly 10 records, each containing `Updated: /boot/limine.conf`. Those are precisely the 10 rows whose table entries point into r19c (the rows at JSON lines 277-357). This is a separate, later journal window; EV-01's 2026-10-11 timestamp is outside it.
- The pacman command is at `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1688`; its `grep` searches `/var/log/pacman.log` and then applies `tail -n 30`. The captured result is 15 matching lines (capture lines 1689-1703), of which exactly 3 are `[ALPM-SCRIPTLET] Updated: /boot/limine.conf` (lines 1695, 1700, 1702). The 2026-10-11 entry is pacman.log line 2021, shown at capture line 1695; it is included in the output despite the journal window beginning on 2026-10-19. Since 15 result lines are below the 30-line tail cap, the tail does not truncate this captured match set. `.ufo/waves/round-19/l1-capture/host-capture-r19.txt:607-608` records `/var/log/pacman.log` as 3169 lines.
- `corpus/knowledge/boot-writers-r19.json:270-357` contains the 13 rows. Row quotes are substrings of their cited capture lines; each contains the timestamp, and each line matches the assigned writer signature. EV-01, EV-03, EV-04 map to the three pacman records; EV-02 and EV-05 through EV-13 map to the ten journal records.
- The additional occurrences in the other captured queries are repeated appearances of the same timestamped events (for example, r19c:11 and r19c:25 both show the 09:03:03 event; r19c:12 and r19c:42 both show 09:29:19), not additional unique rows in either declared probe result set.
- The JSON's journal `probe` value at `corpus/knowledge/boot-writers-r19.json:21` is truncated at `datetime as d`, and its `pattern` field at line 22 says the exact `Updated:` string. The actual captured command continues at r19c:5-10 and filters for the broader substring `"/boot/limine.conf"` in `MESSAGE` (r19c:8). All ten records it emitted are nevertheless `Updated:` records, so this metadata mismatch does not change the reproduced result set.

## Residual
This confirms only the enumerated records in the committed probe captures, not journal history earlier than the stated `--since` window or pacman-log history outside the captured `/var/log/pacman.log`. The journal probe's JSON `probe` metadata is incomplete and its `pattern` is narrower than the actual filter; the committed capture contains the full command and output, so the event-table comparison remains reproducible from that capture. No tools were installed or updated.

Scope: executed=`git cat-file -p 8e5916360f2dfe7bc4eb4ba144081af555900116:corpus/knowledge/boot-writers-r19.json > /tmp/fx_bw.json`; SHA-256 checks of the JSON and three captures against working tree and attacked blobs; `grep -n "Updated: /boot/limine.conf"` on the three captures; read-only Python JSON/capture comparisons and 13-row validation; read-only git revision/status queries