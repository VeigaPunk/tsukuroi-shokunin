Verdict: the privacy and safety of the committed round-24 captures (capture/l1-3, capture/l1-4) and the wave-1 evidence directories at commit 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 survives with defects. No secret, token, key, password, email address, IP address, MAC address or environment dump is committed. However, two committed files and one landed production file carry raw working directories that the contract requires to be reduced to inside or outside the fleet repo, one of them naming an unrelated private project for the first time in the public repository. The l1-3 and l1-4 captures still publish raw `pacman -U` arguments, including home-directory paths, because the capture script reduces only the PWD field.

Context that sets severity: the lane remote `origin` is https://github.com/VeigaPunk/tsukuroi-shokunin.git and `gh repo view VeigaPunk/tsukuroi-shokunin --json visibility,isPrivate` returned `{"isPrivate":false,"visibility":"PUBLIC"}` (exit 0). Commit 22fd1642 is on `origin/master`, so everything below is already published, and removing it from the tip does not remove it from history. [obs] Marginal disclosure was measured against the claim base f169b3ba with `git grep -c` at both revisions:

| Identifier | Lines at base f169b3ba | Lines added by round 24 |
|---|---|---|
| `/home/vgpnk` | 22315 | 391 |
| hostname `plazir27` | 323 | 2259 |
| `.cache/yay` | 68 | 65 |
| btrfs fsid `1d02a454-c549` | 4 | 2 |
| `other-project` | 0 | 3 |
| `tizen-sdb` | 0 | many |
| `openssl-1.0` | 0 | 143 |

## Findings

1. [obs] Defect, new disclosure. A raw sudo working directory naming an unrelated private project is committed in wave-1 evidence. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecPacmanLogCensus.md:94` says the 2026-10-21T20:32:00 `pacman -Sy --noconfirm` ran with `PWD=.../Projects/other-project`. Line 96 quotes the raw journal record `... sudo[2901011]: vgpnk : PWD=.../Projects/other-project ; USER=root ; COMMAND=/usr/bin/pacman -Sy --noconfirm`. The contract says to reduce working directories to inside or outside the fleet repo. The string `other-project` occurs 0 times at base f169b3ba and 3 times at 22fd1642, so round 24 is the first public disclosure of that project name.
   Smallest correction: in lines 94 and 96, replace `PWD=.../Projects/other-project` with `PWD=outside-fleet-repo`. The finding stays fully supported, because the TSV row `.ufo/waves/round-24/w1/ExecSudoAttribution/sudo-records.tsv:23` already records the same event as `outside-fleet-repo`.

2. [obs] Defect, propagated into a landed production file. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24.md:46`, row R24-REDACTION-OVERWRITE (the privacy lesson behind QUALITY criterion 56), describes the L1's synthetic test input as `one with .../Projects/other-project printed outside-fleet-repo`. That input is the real unrelated project directory from finding 1, not a synthetic name. The lesson that enforces redaction therefore leaks the value it redacts.
   Smallest correction: change `.../Projects/other-project` to `.../Projects/other-project`. The test only needs a path under the home directory that is outside the fleet root.

3. [obs] Defect, contract form only, with no marginal disclosure. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecRecapture/cap-head/capture.txt:151-154` contains four unreduced sudo records, for example `[ 2644.043167] plazir27 sudo[3706376]: vgpnk : PWD=/home/vgpnk/Projects/shokunin ; USER=root ; COMMAND=/usr/bin/grep -E mkinitcpio|plymouth /@/.snapshots/1/snapshot/...`.
   - Mechanism: the head script's `plymouth-boot0` probe (`cap-head/capture.txt:137`) is `journalctl -b 0 ... | grep -i -E "plymouth|update-root-fs"`. It swept in every sudo record whose command line mentioned plymouth. Its PWD-reducing `sed` applies only to the separate sudo probe.
   - The same mechanism produced the raw `(command continued)` argument lines at `capture/l1/capture.txt:168-174` and `capture/l1-2/capture.txt:168-174`. Wave 1 already reported those in `w1/SentinelCapture.md:3` and `w1/CritLearningFit.md:79`.
   - The fleet-root path itself is already public (22315 base lines).
   - Smallest correction: replace `PWD=/home/vgpnk/Projects/shokunin` on lines 151-154 with `PWD=inside-fleet-repo`, or drop those four lines. This file is not pinned by any gate.

4. [obs] Defect, raw arguments; residual in the claimed final captures. The `capture.sh` sudo probe reduces only the PWD field (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/capture.sh:47`, an `awk` rule followed by `cut -c1-220`). The `pacman-commands-since-pause` probe (`capture.sh:45`) prints pacman.log `Running` lines verbatim. Both l1-3 and l1-4 therefore publish raw `pacman -U` arguments with home paths on the same six lines:
   - `capture/l1-4/capture.txt:213,215,218` (pacman.log), for example `pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/tizen-sdb/tizen-sdb-2.3.2-3-x86_64.pkg.tar.zst ...`;
   - `capture/l1-4/capture.txt:233,248,251` (sudo journal), for example `COMMAND=/usr/bin/pacman -U --noconfirm --config /etc/pacman.conf -- /home/vgpnk/.cache/yay/openssl-1.0/openssl-1.0-1.0.2.u-...`;
   - `capture/l1-3/capture.txt:213,215,218,233,248,251` (identical, per `diff l1-3/capture.txt l1-4/capture.txt`, which shows no change before line 271);
   - `w1/ExecPacmanLogCensus/table.md:44,49,51,54,67,617,619,622`. These add the pre-window `elephant` build at line 44.

   Duplicate authority: the wave-1 TSV applies a stricter rule to the same records and basenames these arguments. `w1/ExecSudoAttribution.md:72-74` says "sandboxed here to package names per the privacy rule", and `sudo-records.tsv:2,17,20` hold only `zcode-3.16.2-1-x86_64.pkg.tar.zst` and similar names. Two committed views of one event follow two different redaction rules.

   Marginal disclosure is low, because `.cache/yay` already occurs on 68 base lines. [inf] A latent risk remains: `pacman -U` accepts URLs, and `cut -c1-220` truncates without sanitizing. A future `-U https://user:token@host/pkg` would be committed verbatim. No such instance exists today; a pattern scan for tokens, keys, `user:pass@` and emails over all committed round-24 capture and w1 text returned nothing.

   Smallest correction, forward only: in `capture.sh:45` and `:47`, pipe each probe through `sed -E "s#$HOME/[^ ']*/##g; s#://[^/@ ]*@#://#g"` so that home paths become basenames and URL credentials are stripped. Apply the same substitution to `table.md`.
   - Do not rewrite `l1-4/capture.txt` in place. Its sha256 `87f70f82…a56f` is pinned in `corpus/knowledge/pause-lift-gate-r24.json:5`, and `tools/check-pause-gate.py:94` rejects a hash mismatch.
   - Rewriting the capture would therefore break C2. Since the marginal disclosure is nil, this is a tradeoff the judge may accept, not a must-reject.

5. [obs] Defect, host identifier; forward fix only. `capture/l1-4/capture.txt:328-329` (probe `boot0-root-mount`, `capture.sh:55`) publishes the stable root filesystem UUID: `BTRFS: device fsid 1d02a454-c549-4a35-b567-89d60902af8e devid 1 transid 56268 /dev/mapper/root`. The premise needs only the fact that `/dev/mapper/root` was mounted at boot 0, not the UUID. The value was already public on 4 base lines.
   Smallest correction: append `| sed -E "s/[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}/<fsid>/g"` to `capture.sh:55`. Do not edit the pinned l1-4 capture, for the reason given in finding 4.

6. [obs] Low, host identifier. `capture/l1-4/capture.txt:13-16` and `capture/l1-3/capture.txt:13-16` publish four systemd boot IDs, for example `0 6a7f4fdfac624e2ea6c1b3c55d6f94f4`. Two of them (`84755511…`, `3e7084f4…`) were already at base on 5 lines each. No premise uses the ID value.
   Smallest correction: reduce the ID with `awk '{$2="<boot-id>"}1'` in `capture.sh:21`.

7. [obs] Tradeoff, not a defect: identity tokens. Hostname `plazir27` and account `vgpnk` appear on every journal line. Counts are 65 and 42 in l1-3, 76 and 49 in l1-4, and 459 rows of the TSV `user` column, which has the single value `vgpnk`. Wave 1 reported this in `w1/SentinelCapture.md:3`. Both values were public at base (323 hostname lines and 22315 home-path lines), so a cut in round 24 changes nothing externally. Optional correction: drop the constant `user` column from the TSV, and add `sed "s/ $(hostname) / <host> /"` to the journal probes going forward.

8. [inf] Tradeoff: software inventory. `capture/l1-4/capture.txt:40-42` names pending `1password-beta`, `chatgpt-bin` and `claude-code`. Lines `122-126` and `279-281` name the foreign packages `tizen-sdb` and `openssl-1.0 1.0.2.u-7`, which are new to the public repository. Lines `181-183` give exact nvidia and kernel builds. Together these publish a host vulnerability fingerprint: openssl 1.0.2 is end-of-life. The names are the substance of premises P1 and P5, so removing them would remove evidence. This is a tradeoff the judge should weigh, not a correction to demand.

9. [obs] Defect, false provenance found while checking the privacy chain. `w1/CritMirrorReading.md:30` says the 2026-10-21 20:32:00 `-Sy --noconfirm` was "run inside the fleet repo". Three sources contradict it:
   - a read-only reclassification of the live sudo journal printed `outside-fleet no-tty`;
   - `sudo-records.tsv:23` records `outside-fleet-repo`;
   - `ExecPacmanLogCensus.md:94` gives a directory under the home directory outside the fleet root.

   Line 31 of the same file also cites a private agent transcript path for another project, `/home/vgpnk/.omp/agent/sessions/-Documents-nvhelpme/…/125.bash.log:1-8`. No public reader can resolve that pointer. There was precedent at base: 6 such session-path pointers and 21 `nvhelpme` lines.
   Smallest correction: change "run inside the fleet repo" to "run outside the fleet repo" on line 30. Replace the session-log pointer on line 31 with a quote of the 8 relevant output lines, keeping no directory names.

10. [obs] Survives: the TSV's working-directory classes are correct and leak nothing. A read-only re-derivation from `journalctl _COMM=sudo --since '2026-10-20 09:40' --until '2026-10-22 05:47'` printed counts only and no raw values. It found 459 pacman or paccache records:
    - 421 with PWD exactly `/tmp`;
    - 37 elsewhere under the home directory;
    - 1 inside the fleet root.

    This matches the TSV's 458 `outside-fleet-repo` rows and 1 `inside-fleet-root` row (`awk -F'\t' '{print $4}' | uniq -c`). Every one of the 459 rows has 5 fields. The command column contains only `/usr/bin/pacman` or `/usr/bin/paccache`, `--config /etc/pacman.conf`, `-c /var/cache/pacman/pkg`, and package names or archive basenames.

    Minor label drift: the TSV writes `inside-fleet-root` where `capture.sh:47` writes `inside-fleet-repo`. That is two vocabularies for one class, which is against the spirit of QUALITY criterion 56. Smallest correction: rename the TSV label to `inside-fleet-repo`.

11. [obs] Survives: the l1-4 capture script fixed the leak path from finding 3. `capture.sh:37-38` narrowed the Plymouth probes to `systemd\[1\]: .*Plymouth|plymouthd|update-root-fs`. Counting sudo journal lines in boots 0 and -1 that match `update-root-fs|\(plymouthd\)` returned 0 and 0.
    [inf] A residual latent path remains. Any future `sudo` command whose text contains `update-root-fs`, such as an agent running `sudo grep update-root-fs …`, would again pull a raw PWD record into the `plymouth-boot0` and `plymouth-boot-1` probes.
    Smallest correction: add `| grep -v " sudo\["` to `capture.sh:37`, `:38` and `:56`.

12. [obs] Survives: no secrets or raw configuration files.
    - A pattern scan over all committed text under `.ufo/waves/round-24/capture` and `.ufo/waves/round-24/w1` found no secret-shaped strings. The patterns covered GitHub, OpenAI and AWS key prefixes, Slack tokens, bearer headers, private-key armour, `api_key=`, `password=`, `secret=` and `token=`, plus `PWD=`, `TTY=`, IPv4, MAC addresses and email addresses. This excludes public mirror databases, package lists, upstream C source and saved news pages.
    - The only hits were the false positive `retained_key_token` (`w1/ExecRedCauses.md:86`) and version strings that look like IPs.
    - Saved HTML (`w1/SrcArchNews/*.html`) has no csrf, nonce, session or token values.
    - Mirror header files have no `authorization`, `cookie` or `token` fields.
    - Configuration appears only as grep-selected lines: HOOKS lines, `pacman.conf` section headers and Server lines, and the single public mirrorlist URL at `l1-4/capture.txt:99-101,193,199-207`. No whole file is copied.
    - `cmdline-boot-flags` printed only `quiet`, `loglevel=0`, `rd.udev.log_level=0` and `rootflags=subvol=@` (`l1-4/capture.txt:345-349`). [inf] Its `^rd\.` filter would also publish `rd.luks.uuid=` or `rd.luks.name=` on a host that sets them. Smallest correction: narrow the filter to `^rd\.udev`.

Impacted axes: privacy of committed evidence (findings 1-7), duplicate authorities for redaction (findings 4 and 10), provenance (finding 9), and capture-pin integrity for any in-place fix (findings 4 and 5). Corrections that must not be made: rewriting `l1-4/capture.txt` would invalidate the C2 capture pin, and history rewriting would need a destructive VCS operation, which is outside every seat's mandate. Findings 1, 2, 3 and 9 touch unpinned files and can be fixed by the L1 in place.

Scope: read=lane remote and visibility, git trees at 22fd1642 and f169b3ba (git grep counts and lines), capture/capture.sh, capture/l1-3/capture.txt, capture/l1-4/capture.txt, capture/l1-4/checkupdates.out, capture/l1/capture.txt and capture/l1-2/capture.txt (pattern scans), w1/ExecSudoAttribution.md and sudo-records.tsv, w1/ExecRecapture (cap-head, capture-head.sh, diffs), w1/ExecPacmanLogCensus.md and table.md, w1/CritMirrorReading.md, w1/SentinelCapture.md, w1/ExecCensusLive/commands.txt, w1/ExecBootChainAudit/transcript.txt, w1/ExecMirrorTimestamps headers and package lists, w1/SrcArchNews html, corpus/lessons/round-24.md:46, corpus/knowledge/pause-lift-gate-r24.json, tools/check-pause-gate.py, /home/vgpnk/.omp/agent/RULES.md, godspeed skill; wrote=.ufo/waves/round-24/w2/CritCapturePrivacy.md; executed=read-only git (log, ls-tree, grep, diff, branch, remote), gh repo view (visibility), rg and awk scans, file, journalctl _COMM=sudo window and journalctl -b 0/-1 (counts and class labels only, no raw values copied), hostnamectl.
Installs: none
