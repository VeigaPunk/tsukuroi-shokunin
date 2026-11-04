source: S330 — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml — Restart= table, v262 :875-1016 and exit-status options :1063-1149
verified-at: 2026-11-04
recheck: on-release

# Service restart policy — six-cause documentation matrix (round 80)

The JSON companion `corpus/knowledge/service-restart-matrix-r80.json` records
six causes × seven settings (42 Boolean cells). Source header order (:920-929):
`no`, `always`, `on-success`, `on-failure`, `on-abnormal`, `on-abort`, `on-watchdog`.
This is a reading of upstream v262 documentation, not installed-build equivalence,
a runtime simulation, a live restart test, or a prediction for an individual unit.
Snapshot: `.ufo/waves/round-80/before/systemd.service.xml`, SHA256
`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`.
Recheck procedure: reopen the pinned URL and the next upstream release, compare
the table and surrounding exceptions; retain changes as dated errata. Upstream
line numbers below are not distribution-build line numbers.

## Decision table

| Cause | Marked settings (all other cells empty) | Raw source range |
|---|---|---|
| Clean exit code or signal | always, on-success | :932-941 |
| Unclean exit code | always, on-failure | :942-951 |
| Unclean signal | always, on-failure, on-abnormal, on-abort | :952-961 |
| Timeout | always, on-failure, on-abnormal | :962-971 |
| Watchdog | always, on-failure, on-abnormal, on-watchdog | :972-981 |
| Termination due to OOM | always, on-failure, on-abnormal | :982-991 |

The table contains 18 marked and 24 empty cells (row marked counts 2,2,4,3,4,3).
The OOM row differs from unclean exit code in its on-abnormal cell; it is not
permission to infer a historical OOM cause. `no` is empty in all six rows.

## Conditions before applying the table

- Systemd-initiated stop/restart deaths do not cause automatic restart; explicit
  `systemctl stop` is an exception to the policy (:881-883, :996-1002).
- Clean exit classification includes exit0, SIGHUP/SIGINT/SIGTERM/SIGPIPE for
  non-oneshot services, and configured SuccessExitStatus values (:889-897).
  SuccessExitStatus concerns the main process and does not rename numeric statuses
  (:1066-1083). A displayed numeric/name mapping is not changed by this option.
- Type=oneshot rejects always/on-success and never auto-restarts after a successful
  exit, including when that status is force-listed (:909-911, :1144-1146).
- RestartPreventExitStatus suppresses main-process matching exits irrespective
  of Restart=; it does not apply to the listed ExecStartPre/ExecStartPost/ExecStop/
  ExecStopPost/ExecReload helper processes (:1107-1131).
- RestartForceExitStatus forces matching main-process exits irrespective of
  Restart=, subject to the oneshot successful-exit qualification (:1139-1146).
- StartLimitIntervalSec and StartLimitBurst still constrain restart attempts
  (:1004-1008). A marked table cell is not a promise that a restart occurs.
- on-abnormal covers the table's signal, timeout, watchdog and OOM rows;
  on-abort marks only its unclean-signal row. Neither is equivalent to on-failure.

Read-only workflow: obtain the service's effective Restart, Result, NRestarts,
RestartUSec and start-limit properties; retain argv/rc/capture time. Determine
which event and override information remains unavailable. Report limits and
operator next steps; never start, stop, restart or edit the service.
Executed example: `.ufo/waves/round-80/w1/ExecHost/handoff.md`; its transient failed
scope units are not services and this service matrix does not diagnose their cause.

## Complete raw row excerpts

Each following excerpt preserves the complete cited XML lines (including markup)
and contains at most25 whitespace-delimited words. The source table's title is
at :914 and its column header at :920-929. These blocks ground every matrix cell;
quotes are not substring fragments cut before a branch condition.

### systemd.service.xml:932-941

```xml
              <row>
                <entry>Clean exit code or signal</entry>
                <entry/>
                <entry>X</entry>
                <entry>X</entry>
                <entry/>
                <entry/>
                <entry/>
                <entry/>
              </row>
```

### systemd.service.xml:942-951

```xml
              <row>
                <entry>Unclean exit code</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry/>
                <entry/>
              </row>
```

### systemd.service.xml:952-961

```xml
              <row>
                <entry>Unclean signal</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
                <entry>X</entry>
                <entry>X</entry>
                <entry/>
              </row>
```

### systemd.service.xml:962-971

```xml
              <row>
                <entry>Timeout</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
                <entry>X</entry>
                <entry/>
                <entry/>
              </row>
```

### systemd.service.xml:972-981

```xml
              <row>
                <entry>Watchdog</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
              </row>
```

### systemd.service.xml:982-991

```xml
              <row>
                <entry>Termination due to OOM</entry>
                <entry/>
                <entry>X</entry>
                <entry/>
                <entry>X</entry>
                <entry>X</entry>
                <entry/>
                <entry/>
              </row>
```

## QUALITY check and limits

QUALITY1/2/7/19/21/23: this finite decision table is falsifiable against S330,
the version-pinned digest and complete raw source rows above. S330's scope is
upstream documentation only. QUALITY8: provenance trio begins the file and the
cadence is literal on-release. QUALITY14: this check is performed on this note.
QUALITY66: explicit stop, oneshot, clean-status, main-process scope, overrides
and rate-limit branches remain visible. QUALITY94: complete raw row excerpts,
not truncated quoted fragments; every cited line lies in S330's registered
ranges. QUALITY103: upstream anchors are not installed-build anchors.

The numeric counter measures exact finite matrix equality and digest/file binding,
not semantic entailment, authentic authorship, proof a reviewer read, arbitrary
runtime policy, or whole-province conformance. A fabricated complete review bundle
can pass it. Source review is a separate kill rule. No service mutation or repair
is authorized, no new frontier surface or capability is claimed, and rejected
historical round79 claims remain rejected.
