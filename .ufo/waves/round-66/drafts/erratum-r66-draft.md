## Erratum (round 66)

Append-only. The inbound row at line 204 of this file is **not** rewritten here; it is named and superseded by the register.

Superseded text, quoted verbatim from `corpus/knowledge/adjacency-anchors-r19.md:204` (read at lane HEAD `aa75398e`):

```
| IN-109 | `tameshi:corpus/knowledge/service-optin-protocol.md:153` | `tools/tsukuroi-census.sh:915-970` | operative | DRIFTED | 2277 | check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED |
```

The `| 2277 |` cell in that row is stale. The authoritative value is the register's: `corpus/knowledge/adjacency-anchors-r19.json` `inbound[108]` (id `IN-109`) carries `found_line` **2822**, the round-65 re-pin (commit `cecc9e3e7fc7c91dddfd3b0fe5d3955d9eebb477`, "adjacency IN-109 found_line 2683->2822 re-pinned to the arm-shifted case line"). At that revision the cited target holds the evidence quote at `tools/tsukuroi-census.sh:2822` (`git show HEAD:tools/tsukuroi-census.sh | grep -n "check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED"` → `2822:`), so the row's `DRIFTED` classification against the cited range `915-970` is unchanged. The prose above is history; the register is the authority for this record. The `HP-IN-109` row at line 231 of this file names the same superseded `line 2277` and is superseded by the same register pin.
