# Draft: append-only freshness block for corpus/knowledge/pacnew-plane.md

Prepared by seat TsukuroiR35.W2RevHostCapture, 2026-10-23. To be appended verbatim at the end of
`corpus/knowledge/pacnew-plane.md` (after line 67, `R18-FRESH-SUPPLEMENT-32`) by the seat that owns
that file. Nothing in the historical body is rewritten. All values below were re-measured
read-only on 2026-10-23 (11:47:05–11:47:09 UTC); the supporting capture is
`.ufo/waves/round-35/w2/W2RevHostCapture/fresh-capture-20261023T1211Z.txt`
(sha256 `7453404708b59afd5e972f524cc1011230367a2d70f8c867fb7c30cd1d2a84ad`), a re-run of the
round-35 w1 capture script
`.ufo/waves/round-35/w1/ExecHostPacnew/capture-host-pacnew.py`
(sha256 `0d26ab57c41ebd713f1a09c1adf5896d810500fdcdc9613a1293a60b69483638`) whose output is
byte-identical to `.ufo/waves/round-35/w1/ExecHostPacnew/capture.txt`
(sha256 `7c61c7cc7d1b563c2c580b671b9ef3f128a87ffe18492dcec544e583bf829516`) except the two
`date -u` frame lines. No package, service, rebuild, boot or rollback action was performed;
sudo was used only as `sudo -n ls` / `sudo -n stat` / `sudo -n journalctl`.

---

## R35W2-FRESHNESS — host re-measurement (2026-10-23)

Sources S032 (own-work) plus the dated captures cited per supplement. This appended correction
supersedes the current-use readings listed below and every repeated current-use restatement of the
same premise in this file. Historical measurements remain intact. No package, service, rebuild,
boot or rollback action is authorized. Re-measured 2026-10-23 11:47 UTC, twice in one day
(11:31 w1 capture, 11:47 this capture, identical outputs).

- R35W2-FRESH-SUPPLEMENT-A: prior locus `| Filesystem sweep access | **12 — `find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>&1 >/dev/null | grep -ci 'Permission denied'` 2026-10-19** |`. Now: **11 — same command 2026-10-23**. The twelfth path was `/etc/cryptsetup-keys.d` (mode 700 root:root), still present in btrfs snapshots `/.snapshots/1` and `/.snapshots/2` (snapshot set is exactly {1,2}, mtimes 2026-10-20 09:03:02 and 09:29:19) and removed by the operator (`/usr/bin/rmdir /etc/cryptsetup-keys.d`) on 2026-10-20 09:33:19 per the systemd journal; it is absent from live `/etc` today. The remaining 11 denied directories (`/etc/audit/plugins.d`, `/etc/cni/net.d`, `/etc/credstore`, `/etc/credstore.encrypted`, `/etc/cups/ssl`, `/etc/pacman.d/gnupg/crls.d`, `/etc/pacman.d/gnupg/openpgp-revocs.d`, `/etc/pacman.d/gnupg/private-keys-v1.d`, `/etc/polkit-1/rules.d`, `/etc/ssl/private`, `/etc/sudoers.d`) were name-scanned read-only via `sudo -n ls -1A`: 30 entries total, none matching `*.pacnew`, `*.pacsave`, `*.pacsave.N` or `*.pacorig`. [Supporting capture context: fresh-capture-20261023T1211Z.txt:22-40, :144-156, :179-197.]
- R35W2-FRESH-SUPPLEMENT-B: prior locus `[obs] The `pacman-contrib` package query returned “not found” on this host (`pacman -Q pacman-contrib` 2026-10-19). Do not assume the `pacdiff` command is locally available; …` (and the residual caveat of R18-FRESH-SUPPLEMENT-32 that no executable-presence observation is credited). Now: `pacman-contrib 1.13.1-1` is installed (installed 2026-10-20 07:45:37, `/var/log/pacman.log:2444`) and `/usr/bin/pacdiff` is present, `pacman -Qo /usr/bin/pacdiff` → exit 0, owned by `pacman-contrib 1.13.1-1`. The “otherwise use an appropriate comparison/merge tool” branch is currently inapplicable on this host; the compare-and-merge operator action is unchanged. [Supporting capture context: fresh-capture-20261023T1211Z.txt:68-74.]
- R35W2-FRESH-SUPPLEMENT-C: prior locus `## Recheck procedure` (the three-command block and the sentence “Compare names and line numbers; record every count as `<number> — <command> <date>`”). Now: command 1 (`find /etc …`) **exits 1** on this host because find cannot read 11 `/etc` subdirectories, while still printing every reachable match; commands 2 and 3 exit 0. Record command 1 as `<number> — <command> (exit 1: N permission-denied directories, see command 3) <date>`; an exit 1 from command 1 means “sweep incomplete by permission”, not “sweep failed”. Also widen command 1's globs to `*.pacnew`, `*.pacsave`, `*.pacsave.[0-9]*`, `*.pacorig` so the sweep matches the counter plane (tools/score-pacnew-arm-r35*.py); on 2026-10-23 the two extra kinds are 0, so the narrow and wide sweeps agree today. [Supporting capture context: fresh-capture-20261023T1211Z.txt:8-9, :22-25, :28-65.]

Unchanged on 2026-10-23 and re-affirmed: the visible `.pacnew` set is still exactly `/etc/locale.gen.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_ECCP384SHA384.json.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_RSA3072SHA384.json.pacnew`; log targets are still lines 1427, 1645, 1646 dated 2026-10-11; 0 `.pacsave`, 0 numbered `.pacsave`, 0 `.pacorig` on disk and in the log; `/var/log/pacman.log` is still the only unrotated log (3191 lines, 246 903 bytes, mtime 2026-10-22 04:10). Counter-plane constant re-derived twice:
`DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0`.
The `unreadable` value is a property of the sweeping user (`vgpnk`, uid 1000); a root run would report 0.
