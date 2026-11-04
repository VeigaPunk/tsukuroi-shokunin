status: complete
verdict: held

# E3HostProbe — binding file

Full report: `.ufo/waves/round-73/w1/E3HostProbe/report.md` (same text at
`.ufo/waves/round-73/w1/E3HostProbe.md`).

Probe `probe.sh` (418 lines, sha256 `da25458a721040d9dd7ada71e29435434c2435fc1ce62b12450edf7d66d419ac`)
emits five closed-grammar readings on the unit-load merge plane, degrades to
`BLOCKED reason=tool-absent` without `systemctl`/`systemd-analyze`, and refuses to echo a unit name
carrying `|`, a newline, a tab or `=`; hermetic selftest 16/16. Receipts A-D in this directory.

Instruments at `583eea87`, both committed and both reading met: C1 `542f9c2… → 97f6f5ec…`
`UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0 met=1` rc 0; C2
`93f034e3… → 71931c1c…` `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0. Before controls hold at `eb105757…`
(rc 128 / `ROUTED_STALE=3`, rc 1). Both selftests pass (12/12, 11/11).

Two residuals survive the final bytes, both with reproducible attacks (receipt-g): C1 credits a
mechanically copied snapshot slice as a rule row, and C2 credits a bare token list under the
capability heading. The instruments' freeze was broken for several minutes mid-wave and was closed
at the landing commit; the digest sequence is recorded in receipt-e.
