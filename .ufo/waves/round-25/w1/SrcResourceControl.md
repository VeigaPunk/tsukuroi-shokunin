# SrcResourceControl — C2 source for MP4 (systemd.resource-control(5), systemd 262)

Verdict: the Arch rendering of systemd.resource-control(5) for systemd 262.1 carries located, version-pinned quotes for every MP4 property the declaration names — the `auto`/`kill` value domain of `ManagedOOMSwap=` and `ManagedOOMMemoryPressure=`, the default, the exact rule that an `auto` unit is not actively monitored unless an ancestor sets `kill`, the two per-unit overrides that are inert unless `ManagedOOMMemoryPressure=kill`, the three-value `ManagedOOMPreference=` domain, and the `MemoryPressureWatch=`/`MemoryPressureThresholdSec=` pair — and the frozen capture's four sampled units all carry `auto`, so no ancestor of any of them sets `kill` and the `auto` exception cannot fire on this host.

## 1. The page opened, and its version against the host

1. [obs] The page named in the assignment is `https://man.archlinux.org/man/systemd.resource-control.5`. `curl -sS` returned HTTP 200 and 95517 bytes; the sha256 of those raw bytes is `607c9cfec87f445c84b71c5a2ccadf1e93c4e0be76c85f30bb4bac688627fd1a`. The page footer reads `systemd 262.1`, package `core/systemd`, version `262.1-1`.

2. [obs] Two further renderings of the same document were fetched because the located quotes below are quoted from the plain-text one and cross-checked against the English one: `https://man.archlinux.org/man/systemd.resource-control.5.txt` returned HTTP 200, 82707 bytes, sha256 `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422`; `https://man.archlinux.org/man/systemd.resource-control.5.en` returned HTTP 200, 95523 bytes, sha256 `ffe22eec826a1e5dcc2d4900dd750afd53d383c9931cf99b5d89d8371c08052a`. [obs] Both hashes are already recorded independently by sibling seats on the same URLs — `SrcOomdService` recorded `7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422` for the `.txt` rendering, and `RevMp4Semantics` recorded `ffe22eec826a1e5dcc2d4900dd750afd53d383c9931cf99b5d89d8371c08052a` for the `.en` rendering — so the three seats read byte-identical pages. [obs] Stripping tags from the `.5` HTML and from the `.en` HTML and comparing the resulting text gives byte-identical strings of 67342 characters, so the two HTML renderings carry the same prose.

3. [obs] The host runs `systemd 262 (262-1-arch)` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt:8-9`), and `pacman -Q systemd` prints `systemd 262-1`. [obs] The man page the host itself carries is `/usr/share/man/man5/systemd.resource-control.5.gz`, sha256 `0c822f8a8082656c7da4c2a19e7a3dad430a9d4525e1d114ef1b95c7cbd4635c`, owned by `systemd 262-1` (`pacman -Qo`), with the roff header `.TH "SYSTEMD\&.RESOURCE\-CONTROL" "5" "" "systemd 262" "systemd.resource-control"`. [obs] The web rendering is therefore one upstream patch release ahead of the installed package (`262.1` against `262-1`), which the L1 must not blur.

4. [obs] The upstream source of the same page at the tag matching the host was fetched as the version anchor: `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml` returned HTTP 200, 110159 bytes, sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`. Every quote in section 2 was checked to be present in that XML as well, except the two whose text depends on the renderer (see finding 5).

5. [obs] The two quotes whose literal text depends on the renderer are WATCH-1 and WATCH-2, and the reason is the XML markup, not a wording difference. Upstream writes `<literal>auto</literal>` and `<literal>skip</literal>` without quotation marks, while the man-page renderings print `"auto"` and `"skip"` in straight double quotes. Watch-1 and Watch-2 are therefore exact in the `.txt` and both HTML renderings, and their upstream counterparts are the same sentences without the quote characters. [obs] The host's own installed `.gz` man page was de-rendered (roff font escapes and `\*(Aq` apostrophe escapes removed) and every quote in section 2, Watch-1 and Watch-2 included, was found in it as well, so the wording is identical in the 262 package the host actually ships.

## 2. Located quotes, each of at most 25 words, with location

Locations give three things: the section heading of the plain-text rendering (`systemd.resource-control.5.txt`, sha256 `7d16b3d5…`), the line span inside that rendering, and the line span in the upstream `v262` XML (`man/systemd.resource-control.xml`, sha256 `d57641df…`). Every quote was checked to be present, character for character, in the `.txt` rendering, in both HTML renderings and in the host's installed `.gz` man page, except where finding 5 says otherwise.

### The `auto`/`kill` value domain of `ManagedOOMSwap=` and `ManagedOOMMemoryPressure=` (MP4)

- **MP4-A** — § Memory Pressure Control, `.txt` lines 1305-1306 (option term at 1304), XML lines 1523-1529, 12 words:
  > "Specifies how systemd-oomd.service(8) will act on this unit's cgroups. Defaults to auto."

- **MP4-B** — § Memory Pressure Control, `.txt` lines 1308-1309 (option term at 1304), XML lines 1523-1532, 13 words:
  > "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd."

- **MP4-C** — § Memory Pressure Control, `.txt` lines 1319-1320 (option term at 1304), XML lines 1523-1546, 16 words:
  > "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection."

- **MP4-D** — § Memory Pressure Control, `.txt` lines 1320-1322 (option term at 1304), XML lines 1537-1548, 25 words:
  > "if an ancestor cgroup has one of these properties set to kill, a unit with auto can still be a candidate for systemd-oomd to terminate."

  (the sentence continues "However," before this clause in the page; the 25-word form above drops that one word and is the maximum that fits the quote budget. The 26-word whole sentence "However, if an ancestor cgroup has one of these properties set to kill, a unit with auto can still be a candidate for systemd-oomd to terminate." is also exact, at `.txt` lines 1320-1322 and XML lines 1546-1548, but it exceeds 25 words and therefore may not be used as a quote.)

- **MP4-E** — § Memory Pressure Control, `.txt` lines 1315-1316 (option term at 1304), XML lines 1532-1543, 17 words:
  > "Setting either of these properties to kill will also result in After= and Wants= dependencies on systemd-oomd.service"

  (the page continues "unless DefaultDependencies=no." on the next line, `.txt` line 1317, so the whole sentence spans lines 1315-1317; the 19-word form with that clause is also exact and within budget.)

### `ManagedOOMMemoryPressureLimit=` and `ManagedOOMMemoryPressureDurationSec=` (MP4, and the limits that MP5 covers)

- **LIM-1** — § Memory Pressure Control, `.txt` lines 1327-1328 (option term at 1326), XML lines 1555-1560, 15 words:
  > "Overrides the default memory pressure limit set by oomd.conf(5) for the cgroup of this unit."

- **LIM-2** — § Memory Pressure Control, `.txt` lines 1329-1330 (option term at 1326), XML lines 1555-1562, 12 words:
  > "Defaults to 0%, which means to use the default set by oomd.conf(5)."

- **LIM-3** — § Memory Pressure Control, `.txt` lines 1330-1331 (option term at 1326), XML lines 1555-1563, 6 words:
  > "This property is ignored unless ManagedOOMMemoryPressure=kill."

- **DUR-1** — § Memory Pressure Control, `.txt` lines 1336-1337 (option term at 1335), XML lines 1571-1576, 15 words:
  > "Overrides the default memory pressure duration set by oomd.conf(5) for the cgroup of this unit."

- **DUR-2** — § Memory Pressure Control, `.txt` lines 1339-1340 (option term at 1335), XML lines 1571-1579, 13 words:
  > "Must be set to either empty or a value of at least 1s."

- **DUR-3** — § Memory Pressure Control, `.txt` lines 1340-1341 (option term at 1335), XML lines 1571-1581, 12 words:
  > "Defaults to empty, which means to use the default set by oomd.conf(5)."

### `ManagedOOMPreference=` (MP4)

- **PREF-1** — § Memory Pressure Control, `.txt` lines 1347-1348 (option term at 1346), XML lines 1590-1594, 15 words:
  > "Allows deprioritizing or omitting this unit's cgroup as a candidate when systemd-oomd needs to act."

- **PREF-2** — § Memory Pressure Control, `.txt` lines 1348-1349 (option term at 1346), XML lines 1590-1596, 14 words:
  > "Requires support for extended attributes (see xattr(7)) in order to use avoid or omit."

- **PREF-3** — § Memory Pressure Control, `.txt` lines 1380-1381 (option term at 1346), XML lines 1615-1626, 17 words:
  > "Defaults to none which means systemd-oomd will rank this unit's cgroup as defined in systemd-oomd.service(8) and oomd.conf(5)."

### `MemoryPressureWatch=` with `MemoryPressureThresholdSec=` (MP4)

- **WATCH-1** — § Memory Pressure Control, `.txt` lines 1407-1408 (option term at 1406), 16 words:
  > "Controls memory pressure monitoring for invoked processes. Takes a boolean or one of \"auto\" and \"skip\"."

- **WATCH-2** — § Memory Pressure Control, `.txt` lines 1420-1422 (option term at 1406), 19 words:
  > "If set to \"skip\" the logic is neither enabled, nor disabled and the two environment variables are not set."

- **WATCH-3** — § Memory Pressure Control, `.txt` lines 1435-1436 (option term at 1406), XML lines 1680-1691, 11 words:
  > "If not explicit set, defaults to the DefaultMemoryPressureWatch= setting in systemd-system.conf(5)."

- **THR-1** — § Memory Pressure Control, `.txt` lines 1442-1444 (option term at 1440), XML lines 1697-1701, 18 words:
  > "Specifies the maximum allocation latency before a memory pressure event is signalled to the service, per 2s window."

- **THR-2** — § Memory Pressure Control, option term at `.txt` line 1440 and the sentence at `.txt` lines 1444-1446, XML lines 1693-1704, 16 words:
  > "If not specified, defaults to the DefaultMemoryPressureThresholdSec= setting in systemd-system.conf(5) (which in turn defaults to 200ms)."

  [obs] This one sentence is quoted from the HTML renderings and the upstream XML; the `.txt` rendering breaks it across a line as `systemd-` / `system.conf(5)`, so the literal string is not contiguous in that rendering. The wording is the same in all three, and the de-rendered host `.gz` page contains it as a contiguous string.

## 3. Mapping to the capture lines

The capture is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt`, sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`, re-verified locally with `sha256sum` (exit 0, matching the declaration). It is 155 lines, header timestamp 2026-10-22T10:06:23Z.

### Property-by-property map

| property | capture lines | value read | value unique in capture? |
|---|---|---|---|
| `ManagedOOMSwap=` | 112, 121, 130, 139 | `auto` | no, 4 occurrences |
| `ManagedOOMMemoryPressure=` | 113, 122, 131, 140 | `auto` | no, 4 occurrences |
| `ManagedOOMMemoryPressureLimit=` | 114, 123, 132, 141 | `0` | no, 4 occurrences |
| `ManagedOOMMemoryPressureDurationUSec=` | 115, 124, 133, 142 | `[not set]` | no, 4 occurrences |
| `ManagedOOMPreference=` | 116, 125, 134, 143 | `none` | no, 4 occurrences |
| `MemoryPressureWatch=` on `user@1000.service` | 117 | `skip` | **yes**, 1 occurrence |
| `MemoryPressureWatch=` on the three slices | 126, 135, 144 | `auto` | no, 3 occurrences |
| `MemoryPressureThresholdUSec=` | 118, 127, 136, 145 | `200ms` | no, 4 occurrences |
| `DefaultMemoryPressureWatch=` | 150 | `auto` | **yes**, 1 occurrence |
| `DefaultMemoryPressureThresholdUSec=` | 149 | `200ms` | **yes**, 1 occurrence |
| `systemctl is-active systemd-oomd.service` | 72-74 | `inactive`, exit 3 | `inactive` is **unique**, 1 occurrence |

The four property blocks are the `systemctl show` invocations at capture lines 111, 120, 129 and 138, for `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` respectively. Every property value in those blocks is printed 4 times, so no single property line is unique.

### Unique pointers that satisfy the C2 uniqueness rule

[obs] The C2 rule wants at least one pointer whose line text is unique in the capture and is not a section header, a `$ ` command echo or an `[exit ` line. For this page's properties the single-line unique options are capture lines 117 (`MemoryPressureWatch=skip`), 149 (`DefaultMemoryPressureThresholdUSec=200ms`) and 150 (`DefaultMemoryPressureWatch=auto`); for the oomd state it is line 73 (`inactive`).

[obs] The `ManagedOOM*` values themselves have no unique single line, but the following multi-line strings each occur exactly once in the capture and each starts with a non-header, non-echo, non-exit line, so they are usable as `contains` anchors:

- `ManagedOOMMemoryPressure=auto` / `ManagedOOMMemoryPressureLimit=0` / `ManagedOOMMemoryPressureDurationUSec=[not set]` / `ManagedOOMPreference=none` / `MemoryPressureWatch=skip` / `MemoryPressureThresholdUSec=200ms` — count 1, and it is the `user@1000.service` block.
- `ManagedOOMPreference=none` / `MemoryPressureWatch=skip` — count 1.
- `DefaultMemoryPressureThresholdUSec=200ms` / `DefaultMemoryPressureWatch=auto` — count 1.

## 4. What the page says about this host, for the MP4 row

1. [obs] The `auto` value is the documented default of both properties (MP4-A), and the two properties are documented as taking only `auto` or `kill` (the page's option line at `.txt` line 1304 reads `ManagedOOMSwap=auto|kill, ManagedOOMMemoryPressure=auto|kill`).

2. [obs] The documented answer to "are `auto` units monitored" is MP4-C: systemd-oomd "will not actively use this cgroup's data for monitoring and detection" for an `auto` unit. The page states exactly one exception, MP4-D: an `auto` unit "can still be a candidate for systemd-oomd to terminate" if an ancestor cgroup has one of the two properties set to `kill`.

3. [inf] The exception cannot fire on this host within capture evidence. The four units the capture sampled are `user@1000.service` (line 111), `user-1000.slice` (120), `user.slice` (129) and `-.slice` (138), and every one of them reads `ManagedOOMSwap=auto` and `ManagedOOMMemoryPressure=auto` (lines 112-113, 121-122, 130-131, 139-140). `-.slice` is the topmost ancestor of the other three, and it too reads `auto`; the ancestor chain of `user@1000.service` is `user-1000.slice`, `user.slice`, `-.slice` (the capture reads the service's own pressure file at the path `/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.pressure`, capture.txt:41), all sampled and all `auto`. No ancestor of any sampled unit sets `kill`, so under MP4-C and MP4-D the four sampled cgroups are not monitored and not kill candidates. This is the page-level statement of the same conclusion the reviewer seat `RevMp4Semantics` reached from the v262 sources, and it is what MP4 needs: on this host the `auto` value is inert, not a softer form of monitoring.

4. [obs] The per-unit overrides are inert on this host for a second, independent reason stated on the same page. LIM-3 says the limit property "is ignored unless ManagedOOMMemoryPressure=kill", and the duration property carries the identical sentence (`.txt` lines 1341-1342, XML lines 1582-1583). The capture reads `ManagedOOMMemoryPressure=auto` on all four units, so `ManagedOOMMemoryPressureLimit=0` and `ManagedOOMMemoryPressureDurationUSec=[not set]` are not merely unset but ignored. LIM-2 and DUR-3 explain what their unset values would have meant had the property applied: `0%` and empty "mean to use the default set by oomd.conf(5)".

5. [obs] `ManagedOOMPreference=none` on all four units (capture lines 116, 125, 134, 143) is the documented default (PREF-3), and PREF-3 also states what `none` means for oomd's ranking. PREF-1 and PREF-2 give the domain `none|avoid|omit` (`.txt` line 1346) and the precondition that `avoid` and `omit` need extended-attribute support, which is why the host's uniform `none` is not a missing configuration.

6. [obs] `MemoryPressureWatch=skip` on `user@1000.service` (capture line 117) is the shipped value, not a local edit: `/usr/lib/systemd/system/user@.service:36` reads `MemoryPressureWatch=skip` (that file's sha256 is `96e528b5e7d593dc7e48657b9127a4ad27ffe863d0319956314cb6b954159cfb`). [obs] The page says what `skip` means: WATCH-2, the logic is "neither enabled, nor disabled and the two environment variables are not set", so `skip` is not a prohibition on pressure handling, it is the absence of the export. The three slices read `auto` (lines 126, 135, 144), and the manager default reads `DefaultMemoryPressureWatch=auto` (line 150).

7. [obs, live reads outside the capture] For the `auto` case the page conditions the protocol on accounting: "If the \"auto\" value is set the protocol is enabled if memory accounting is anyway enabled for the unit, and disabled otherwise" (`.txt` lines 1418-1420, 22 words, exact). `systemctl show -p MemoryAccounting -p MemoryPressureWatch -- user.slice user-1000.slice user@1000.service -.slice` prints `MemoryAccounting=yes` for all four units, and `MemoryPressureWatch=auto`, `auto`, `skip`, `auto` respectively. [inf] So the `auto` slices are in the enabled case and `user@1000.service` is in the disabled-by-choice case, and neither reading touches oomd's own polling. The `MemoryAccounting` value is not in the capture, so any row that cites it must mark it as a live read and not as capture evidence.

8. [obs] The threshold matches the documented default end to end. The page's THR-2 says the threshold falls back to `DefaultMemoryPressureThresholdSec=` in `systemd-system.conf(5)`, "which in turn defaults to 200ms"; the capture reads `DefaultMemoryPressureThresholdUSec=200ms` (line 149) and `MemoryPressureThresholdUSec=200ms` on all four units (lines 118, 127, 136, 145). [obs] `systemd-analyze cat-config systemd/systemd-system.conf` prints "Main configuration file systemd/systemd-system.conf not found", so no local file sets either default, and `grep -rn DefaultMemoryPressure /usr/lib/systemd/system/ /etc/systemd/system/` returns nothing.

9. [obs] A naming detail the entry must not get wrong. The capture's property names are D-Bus property names, and two of them differ from the unit-file setting names the page documents. The page names the settings `ManagedOOMMemoryPressureDurationSec=` and `MemoryPressureThresholdSec=`, while the capture shows the D-Bus properties `ManagedOOMMemoryPressureDurationUSec` and `MemoryPressureThresholdUSec`. The upstream mapping is visible in `src/core/dbus-cgroup.c`: line 425 declares `SD_BUS_PROPERTY("ManagedOOMMemoryPressureDurationUSec", "t", …)` and line 434 declares `SD_BUS_PROPERTY("MemoryPressureThresholdUSec", "t", …)`, and line 1768 writes the unit setting back under the name `ManagedOOMMemoryPressureDurationSec=`. The upstream file was fetched at `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-cgroup.c`, HTTP 200, 91721 bytes, sha256 `8a1d7a9cd70e25caa536e1ea623d95dfc05c714bf51720e40cda5b11da6b1298`. [obs] The page's own `MemoryPressureThresholdSec=` is named inside the WATCH text at `.txt` line 1417 and 1441.

10. [obs] `ManagedOOMMemoryPressureLimit` is declared on the D-Bus side as a raw unsigned integer (`src/core/dbus-cgroup.c:424`, `SD_BUS_PROPERTY("ManagedOOMMemoryPressureLimit", "u", NULL, offsetof(CGroupContext, moom_mem_pressure_limit), 0)`), and the internal field is commented "Normalized to 2^32-1 == 100%" (`src/core/cgroup.h:203`). The capture reads `0` for that property on all four units, which is the value the parser writes for an empty setting (`src/core/load-fragment.c:4119-4122` sets the limit to `0` when the value is empty) and is the same `0` the page's LIM-2 describes as "use the default set by oomd.conf(5)". The exact numeric encoding of the D-Bus value is not settled by this page and is not needed for MP4. [unk]

## 5. Draft SOURCES row (one row; the L1 assigns the final id)

Column order per `corpus/SOURCES.md:5`: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1NN | systemd.resource-control(5) — https://man.archlinux.org/man/systemd.resource-control.5 | docs | A | The documented value domain and default of `ManagedOOMSwap=` and `ManagedOOMMemoryPressure=` (`auto`, `kill`, default `auto`), when an `auto` unit is and is not monitored, the per-unit limit and duration overrides that apply only under `ManagedOOMMemoryPressure=kill`, the `ManagedOOMPreference=` domain, and the `MemoryPressureWatch=` / `MemoryPressureThresholdSec=` pair; the systemd 262 unit manual, not host state and not a claim that systemd-oomd runs here | § Memory Pressure Control (`.txt` lines 1303-1450 of the plain-text rendering, sha256 `7d16b3d5…`): the option term at 1304 lists the two properties with the two values `auto` and `kill`; `ManagedOOMMemoryPressureLimit=` at 1326; `ManagedOOMMemoryPressureDurationSec=` at 1335; `ManagedOOMPreference=` takes none, avoid or omit, at 1346; `MemoryPressureWatch=` at 1406; `MemoryPressureThresholdSec=` at 1440; upstream `v262` `man/systemd.resource-control.xml` lines 1523-1709 (sha256 `d57641df…`); systemd 262.1 man-page footer, core/systemd 262.1-1, page opened 2026-10-22 | “Specifies how systemd-oomd.service(8) will act on this unit's cgroups. Defaults to auto.” (12 words, § Memory Pressure Control, `.txt` 1305-1306) — the two properties take only `auto` or `kill` and default to `auto`; “When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection.” (16 words, `.txt` 1319-1320) — an `auto` unit is not actively monitored, and the page's only exception is “if an ancestor cgroup has one of these properties set to kill, a unit with auto can still be a candidate for systemd-oomd to terminate.” (25 words, `.txt` 1320-1322); the per-unit limit and duration “is ignored unless ManagedOOMMemoryPressure=kill” (6 words, `.txt` 1330-1331 and 1340-1341), and both default to the oomd.conf(5) value when unset; `ManagedOOMPreference=` takes none, avoid or omit and “Defaults to none” (`.txt` 1380-1381); `MemoryPressureWatch=` “Controls memory pressure monitoring for invoked processes” and, per the same entry, “Takes a boolean or one of "auto" and "skip"” (`.txt` 1407-1408), and `MemoryPressureThresholdSec=` “Specifies the maximum allocation latency before a memory pressure event is signalled to the service, per 2s window” (18 words, `.txt` 1442-1444) defaulting to `DefaultMemoryPressureThresholdSec=`, “which in turn defaults to 200ms” (`.txt` 1444-1446) | mined | 2026-10-22 | on-release | corpus/knowledge/memory-pressure-r25.md |

Notes for the L1 on this row.

- The id cell is the contract placeholder `S1NN`; the L1 assigns the number. `corpus/SOURCES.md` carries S001 through S114 with no gaps, so S115 is the next free id in the registry as it stands, but five other wave-1 seats have already claimed ids in the same space — `SrcCgroupV2`, `SrcKernelOomCounter` and `SrcPsiDoc` each claim S115, `SrcOomdConf` claims S116, `SrcOomdService` claims S117 — so the L1 must renumber at integration and avoid a duplicate. `RevMp4Semantics` also drafted a row for this same page, with id left as `S1NN`; that draft overlaps this one on the `auto` sentence, and the L1 should fold the two into a single resource-control row rather than register the page twice.
- `kind` is `docs` and `tier` is `A`, matching every other man-page row in the registry. `status` is `mined`: the page was opened, read and cross-checked against the upstream v262 XML and the host's own installed 262 man page. `recheck` is `on-release`, the registry's value for rows pinned to a release series, and the row is pinned to the systemd 262 series. `used-by` names the round-25 C2 entry `corpus/knowledge/memory-pressure-r25.md`, which the C2 rule requires: the row must be `mined`, must name the entry in `used-by`, and must have been opened on 2026-10-22, which it was.
- The `anchor` field carries the section headings and the plain-text line spans plus the upstream XML line span, so a reader can relocate any quote without depending on a rendered line number. The `teaches` field carries the quotes themselves, each within the 25-word budget, with its own locator.
- The row is a page row, not a host-state row. It does not assert that systemd-oomd is running, that any unit on this host is monitored, or that any threshold is in effect; the host facts belong to the capture and to the entry rows.

## 6. The existing S041, S044 and S046 rows cite a different page

1. [obs] The assignment asks that this be recorded, and it is correct as stated. `corpus/SOURCES.md` line 47 (S041), line 50 (S044) and line 52 (S046) all give their source as `systemd.exec(5) — https://man.archlinux.org/man/systemd.exec.5`, and their scopes are the `ProtectSystem=` argument domain and the unit-side read-only mechanisms. This row is for `systemd.resource-control(5)`, a different page.

2. [obs] The two pages are disjoint on the properties in question, so this row neither redefines nor supersedes S041, S044 or S046. `systemd.exec(5)` was fetched as `https://man.archlinux.org/man/systemd.exec.5.txt`, HTTP 200, 291937 bytes, sha256 `08d00c43b9473e96401e152b1649c5b42bfeb0bd34e1bbe84df6adf34434c751`, and `grep -cE 'ManagedOOM|MemoryPressureWatch|MemoryPressureThresholdSec'` over it returns 0: the exec page does not mention a single one of them. The reverse also holds: `grep -c 'ProtectSystem='` over `systemd.resource-control.5.txt` returns 0, so the resource-control page never mentions the exec page's subject. The exec page points at the resource-control page for cgroup details instead (`.txt` lines 23, 147, 524, 607, 1050, 1062, 1111, 1152), so the two rows are complementary rather than overlapping, and the `used-by` of the new row names only the new entry.

3. [obs] The `systemd.exec(5)` page carries the same version footer as the page opened here, `systemd 262.1` (`.txt` line 5005), so the two rows in the registry describe the same systemd release from two different pages.

## 7. Limits and out-of-scope items

- [unk] The numeric encoding of the `ManagedOOMMemoryPressureLimit` D-Bus value is not settled by the page and is not needed for MP4; finding 4.10 records what the page, the parser and the D-Bus declaration each say and stops there.
- [unk] Whether `ManagedOOMMemoryPressureLimit=0` and `ManagedOOMMemoryPressureDurationUSec=[not set]` would have had any effect if the mode were `kill` is an oomd.conf(5) question about the 60 % and 30 s defaults; this page only says the override falls back to oomd.conf(5) and that the property is ignored unless the mode is `kill`. The oomd.conf(5) numbers belong to the `SrcOomdConf` seat.
- [unk] The `MemoryAccounting=yes` reading that decides the `auto` case for the three slices is a live read taken outside the capture (finding 4.7); the capture does not contain it, so a row that uses it must say so.
- [obs] The oomd service manual, the oomd.conf(5) manual and the v262 C sources were opened by other seats (`SrcOomdService`, `SrcOomdConf`, `SrcSystemdCode`, `RevMp4Semantics`). This seat read `systemd-oomd.service(8)` and `oomd.conf(5)` only as cross-checks and drafted no row for either, so the two pages keep one owner each.
- [obs] The weaker prior statements that MP4 sharpens live in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md`: line 344 records `ManagedOOMMemoryPressure=auto` and `ManagedOOMSwap=auto` on `user@1000.service` and `user-1000.slice` and infers from the oomd defaults alone that "oomd would likely have acted before the kernel"; the page's own MP4-C and MP4-D, plus the capture's `-.slice` reading, say the opposite for the sampled cgroups, because `auto` is not monitored unless an ancestor sets `kill` and no ancestor here does. Line 347 describes `MemoryPressureWatch=skip` as pinning a "cooperating-app lever" on `user@1000.service`; the page's WATCH-2 refines that, since `skip` means the export is neither enabled nor disabled. This seat did not edit that note.
- [obs] No file under `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/` or `tools/` was read for modification or written. Only this report was produced, plus scratch copies of the fetched pages under `/fast/scratch/hyaku/tsukuroi-r25/SrcResourceControl/`. No git or jj write command was run, no repository was cloned, nothing was pushed, no service was started, stopped or restarted, no configuration was written, and no package transaction was attempted.

Scope: read=https://man.archlinux.org/man/systemd.resource-control.5 (plus its .txt and .en renderings), https://man.archlinux.org/man/systemd.exec.5.txt, https://man.archlinux.org/man/systemd-oomd.service.8.txt, https://man.archlinux.org/man/oomd.conf.5.txt, https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/dbus-cgroup.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/cgroup.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/cgroup.h, https://raw.githubusercontent.com/systemd/systemd/v262/src/core/manager.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/cgroup-util.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/cgroup-util.h, https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/string-table.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/string-table.h, https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/parse-util.c, https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/conf-parser.c, /usr/share/man/man5/systemd.resource-control.5.gz, /usr/lib/systemd/system/user@.service, /usr/lib/systemd/system/, /etc/systemd/system/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt; wrote=.ufo/waves/round-25/w1/SrcResourceControl.md; executed=curl fetches to /fast/scratch/hyaku/tsukuroi-r25/SrcResourceControl/, sha256sum, grep, python3 string checks, systemctl show/is-active/is-enabled, systemd-analyze cat-config, pacman -Q/-Qo, all read-only
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
