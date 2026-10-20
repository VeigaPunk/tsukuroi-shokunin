# ReviewSourceTier — round 15 source-tier review (read-only)

Baseline 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2. Date 2026-10-20.
Status at review: S046–S048 rows, the C1 pair, the C2 pair and `host-snapshot.json` are **absent** from the tree (SOURCES.md ends at S045; no `*-r15.*` knowledge files). This review covers the existing rows they build on plus pre-landing rules. No verification or tests run.

## Evidence reopened

- systemd.exec(5) native page (footer 262.1) and raw tags `v261.2` and `v262.1` (`man/systemd.exec.xml`): the ProtectSystem= definition "Takes a boolean argument or the special values full or strict" (11 words) and "This setting cannot ensure protection in all cases." are identical in both tags. `full` (/usr, /boot, /efi, /etc) and `strict` (except /dev, /proc, /sys) match S041/S044.
- Comment 6071740243 (S045, #8047): user.id 317366263, type User, COLLABORATOR, created/updated 2026-10-09T00:27:22Z. Quoted fragments are verbatim; word counts 16/14/16/13/6 confirmed. Issue #8047: open, comments 1, updated 2026-10-09T00:27:22Z. Matches.
- Comment 6234472369 (S043, #6629): "Nothing was run on a machine." is verbatim. Body ends "This review is by Claude Opus 5.5 alone." Issue #6629: open, comments 1, updated 2026-10-17T13:31:32Z. Matches.
- pacman(8) native page: no "partial" language. "-Sy" appears only in the `-l` outdated-filter note. `-Syu` = "Update package list and upgrade all packages afterwards."

## Findings (severity order)

1. **S045 overreaches by term absence (medium; laundering in reverse).** The row says "no occurrence of model, generated, triage or automated, so S042's asserted basis is unsupported." The body names "Codex Medium reviewed the same evidence … and reached the same conclusion," a model product name the sweep did not include. The round-14 lesson (lines 181–183) already says a term-absence sweep is not a claim that no model is named. The same account's #6629 comment self-describes as a Claude review. Correct reading: #8047's body does not establish its generation method and names an AI reviewer. Fix: replace "unsupported" with "not established by the body; body names Codex Medium as a second reviewer, which its own caveat says is not independent." Keep the host-cause rejection. Do not transfer #6629's disclaimer or self-description to #8047.

2. **Version skew behind S041/S044 (medium).** The footer is 262.1. The host runs systemd 261.2-1 (`/var/log/pacman.log:1594`, 2026-10-11 16:14:24, `upgraded systemd (261.1-1 -> 261.2-1)`; S029 and S040 agree). The ProtectSystem= domain sentence is identical at v261.2 and v262.1, so the proposition holds for the installed version too. The R15 MD should cite both tags, not the footer alone. The host's own installed man page was not read.

3. **S046 would duplicate S044 (medium; census).** The spec defines S046 as the systemd.exec(5) ProtectSystem= first definition. That is the same URL and quote as S044, and S041 uses the same URL. A new row adds a W04 "duplicate url … across scopes" warning and no new evidence. Fix: reuse S044 for the correction and cite the tag evidence in the MD. If a row is still wanted, its scope must be the tag-version comparison, with a distinct anchor.

4. **S048 must not carry partial-upgrade doctrine (medium).** pacman(8) does not state that partial upgrades are unsupported. That doctrine is ArchWiki (S010 "Partial upgrades are unsupported"; S047). S048 teaches should be limited to: `-Syu` is "update package list and upgrade all packages afterwards"; `-S <pkg>` installs the named package and its dependencies; `-Sy` is documented only as the refresh prerequisite for the `-l` outdated filter.

5. **S047 vs S010 URL reuse (low).** S047 "ArchWiki System maintenance" would share a URL with S010 (oldid 885170) unless it cites a distinct current revision. Reuse S010 or record the distinct revision and recheck date, or expect a W04 warning.

6. **S041 unlabelled negative claim (low).** "`full` … does not cover `/`" is inferred from the listed mounts. The page never mentions `/` for `full`. Mark it [inference] or drop it.

7. **Host evidence for C2 (IncidentEntry input; log reads only, no probe run).** `/var/log/pacman.log`:
   - 2026-10-16 23:52–23:53: last full upgrade visible (`-Syu --needed chatgpt-bin`).
   - 2026-10-11 12:54:13: `-Sy --noconfirm fuse2`. 2026-10-18 14:11:00: `-Sy --noconfirm`, then `-S shellcheck`. Sync-only refresh, then installs without `-u`.
   - 2026-10-20 04:25:16 (line 2429): `pacman -S --needed --noconfirm libinput libinput-tools`, with no `-Sy`/`-Syu`. libinput 1.31.3→1.32.0 (line 2432); python-libevdev, python-pyudev, python-yaml and libinput-tools installed; transaction completed 04:25:17. This matches the operator's partial-upgrade report. Sync-DB freshness at that moment is not in the log; the sync_metadata probe must measure it.

## Authority-laundering check

- C1 chain: S044 (docs A) carries the definition; S041 (docs A) carries mechanisms; S045/S042/S043 (community C) appear only as the correction subject. Acceptable.
- C2 chain as specified cites only S047/S048 plus host evidence. Keep community rows out of C2.
- S036/S037 remain rejected and are not cited as support in any row read.

## Recommendations

1. Reword S045 teaches before L1 cites it (finding 1).
2. Do not create S046. Cite S044 plus the v261.2/v262.1 tag evidence (finding 3).
3. In the MD, locate by heading "SANDBOXING > ProtectSystem=" and tag path, not reader line numbers.
4. Narrow S048 teaches (finding 4). Reuse S010 for S047 or record a distinct revision (finding 5).
5. Label or drop the S041 `/` inference (finding 6).

## Limits

- Not verified here: S041's other mechanisms (ReadOnlyPaths, BindReadOnlyPaths, TemporaryFileSystem `ro`); S010's current revision; the S040 sha256 (not recomputed, since that needs a command); S036/S037/S042 not reopened directly; the host's installed systemd man page; sync-DB state; any live host behavior.
- Reader line numbers are unstable; citations here use headings and tag paths.

## Tools

read (URLs, artifacts, host files) and grep (URLs, artifacts, `/var/log/pacman.log`). No bash, no installs, no package, service or snapper changes, no probes. Tool installs or updates: none.
