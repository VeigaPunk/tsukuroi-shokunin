# `## Gate` block draft — round 80 (wave w1)

Draft for the L1's `corpus/lessons/round-80.md`. Format follows the round-77/78/79
Gate tables. The L1 owns the final lesson; this seat owns the source row and
the Gate rows below.

## Provenance of the cited page

The upstream page was opened by the L1 before the freeze commit
`61ec89ec6e6f284b6fba2127721359e6931a5789` and pinned byte-exact at
`.ufo/waves/round-80/before/systemd.service.xml`, SHA-256
`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44` (measured
read-only by this seat; equal to `snapshot_sha256` in `before/expected.json` and
to the digest frozen in `SCORECARD.md`). `before/expected.json` SHA-256 is
`05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`, the value
frozen in the scorecard.

Quotes are located in the **tag-stripped, whitespace-normalised** snapshot by
token position — the same normalisation the round-79 instrument applied — so
every line number below is an upstream **v262 tag** line in that snapshot, not
an installed Arch build line. Every quoted span occurs exactly once in the
1977-line file (occurrence counts in `ScribeFrontier/derivation.md`).

## Gate table

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S330 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml ; 2026-11-04, :877-878: `Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.` | admit, tier A/docs/mined for the `Restart=` settings-to-exit-cause matrix and the conditions that qualify it only: the six-cause × seven-setting table at :913-994 (title :914, header :920-929, six cause rows :932-991), the clean-exit definition :889-897, the no-restart-after-stop sentences :881-882 and :996-1000, the `RestartPreventExitStatus=` / `RestartForceExitStatus=` overrides :1108-1109 and :1140-1141, the `Type=oneshot` exclusion :909-911, and the start rate limiting :1004-1006; 42 finite cells over documented semantics, not a live-host reading and not an installed-build equivalence claim |
| `Restart=always` restarts the service even after an operator's `systemctl stop` | same page, :999-1000: `the service is stopped with systemctl stop or an equivalent operation.` | reject: the page makes an explicit stop an exception to every setting, and separately says a death resulting from systemd operation is never restarted (:881-882) — so `always` cannot be read as "always". Flip: a located upstream passage stating that an explicit `systemctl stop` does not suppress the restart under `Restart=always` |
| `Restart=always` is accepted for `Type=oneshot` services | same page, :909-911: `Type=oneshot services will never be restarted on a clean exit status,` / `always and on-success are rejected for them.` | reject: the page rejects `always` and `on-success` for `Type=oneshot` outright, and `RestartForceExitStatus=` cannot override that for a success status (:1144-1146). Flip: a located upstream passage stating that `Restart=always` is allowed for `Type=oneshot` |
| `Restart=on-watchdog` restarts the service after an unclean exit code | same page, :906-907: `the service will be restarted only if the watchdog timeout for the service expires.` | reject: `on-watchdog` is scoped to the watchdog timeout alone; the table's `Unclean exit code` row (:942-951) marks no `on-watchdog` cell. Flip: a located upstream passage stating that `on-watchdog` also covers unclean exit codes |
| `RestartPreventExitStatus=` suppresses restarts caused by `ExecStopPost=` or `ExecReload=` processes | same page, :1126-1128: `this setting has no effect on processes configured via ExecStartPre=, ExecStartPost=, ExecStop=, ExecStopPost= or ExecReload=,` | reject: the option binds only the main service process; helper processes are outside it, so the override is narrower than "any status". Flip: a located upstream passage stating that the option applies to those helper processes as well |

## Rejected history preserved (not silently dropped)

- **This round's four rejections above** are kept with their reason and flip
  condition, per QUALITY 5 (a rejection is kept, not silently dropped). Each
  one is a refutation of a claim about **documentation semantics**; none is an
  accusation about a seat and none is declared false about any host state —
  the manual does not observe this host.
- **Round 79's three rejections** (the `After=` pull-in claim, the `Requires=`
  continued-active claim, the `Upholds=` one-time-pull-in claim) stand
  unchanged in `corpus/lessons/round-79.md`. Round 80 opens a different page
  (`systemd.service.xml`, not `systemd.unit.xml`), so it neither re-opens nor
  re-judges them; this round's S330 admits a new row and changes no existing
  row's status, recheck or used-by.
- **The registry's 33 `rejected` rows** (`S029 S030 S033 S036 S037 S042 S043
  S045 S080 S147 S151 S160 S161 S170 S178 S179 S183 S184 S185 S190 S197 S254
  S271 S294 S295 S296 S307 S308 S312 S313 S317 S326 S328`) are untouched by this
  round; their reasons and flip conditions remain in their own rows.

## Notes the L1 must carry

- **S330 is a new row; no existing row's status, recheck or used-by changes.**
  The committed registry holds 329 rows, `S001`–`S329` contiguous, so `S330` is
  the next unused id and no id is reused. The id is also *forced*: the frozen
  instrument greps the registry literally for a line starting `| S330 |`
  (`tools/measure-round80.py:35`), so this round's predicate fixes the number.
- **Id-collision caveat, recorded and not smoothed.** The read-only staged
  package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`
  already uses the bare id `S330` for a different document
  (`lanes/tsukuroi/round14/captures/mirror-language-list-capture.txt`, an
  own-work mirror changelog capture; the package used `S329` for the same
  capture file). The package is **not adopted**, no bytes are copied, and the
  lane registry is **not** renumbered: the id is a document-scoped label, so
  the safe resolution is document context, never arithmetic renumbering. The
  collision verdict belongs to ConnectorScope's lane; this seat records the
  collision and adopts nothing.
- **No `W04`/`E04` duplicate-URL finding is expected for S330.** The census
  `url_of()` takes the *first* URL in the source cell —
  `raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml` — and
  no existing row's first URL is that string (`S070` is the only row that
  mentions a `systemd.service` page; its first URL is the freedesktop one).
  This is derived by reading the census rule code and the registry, **not** by
  a census run: this seat ran no census and claims no green census.
- **`E11` at census time is the real landing risk.** The census requires every
  used-by path of a `mined` row to exist on disk
  (`scripts/sources-census.sh`, `usedby_findings`). Both planned companions
  are produced this wave, so the row and both companions must land in the same
  integration step. `E12` likewise: the row must land inside the `## Registry`
  section (the table runs `corpus/SOURCES.md:7`–`:340`; `## Paths` starts at
  `:342`).
- **The matrix is documentation, not installed-build or live-restart
  behaviour.** The row's `teaches` cell says so, the companion note must say
  so, and the r79 "upstream line ≠ host line" discipline (QUALITY 103) applies
  unchanged: every line number above is a v262 tag line in the pinned
  snapshot.
