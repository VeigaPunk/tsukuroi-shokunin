# round-12 — SourceReview (author-side advisory; not independent verification)

Seat: SourceReview. Scope: re-open S027, S028, S034 (plus the S019/S020/S023 anchors the snapper note cites) and check quote/scope validity against `corpus/knowledge/snapper-eacces-mechanism.md`; review `corpus/SOURCES.md` mutable-field handling and visible additions. No source writes, no git mutation, no sudo, no systemd-run, no package operations. Read-only fetches and one non-root `strace` probe only.

Verified-at: 2026-10-20T02:15Z (UTC) for fetches; host HEAD `b76b5c3`.

## Tool record

- No installs or upgrades made. `strace` was already present at `/usr/bin/strace` and used read-only as uid 1000 (`strace -e trace=faccessat,faccessat2,access /usr/bin/test -w /`, exit 1 from `test`, which is the expected non-root result).

## Commands and exit codes (read-only)

| Probe | Result |
|---|---|
| `read https://man.archlinux.org/man/capabilities.7` / `systemd.exec.5` / `access.2` | rendered; quotes checked against the rendered text |
| `curl -sS https://man.archlinux.org/man/{capabilities.7,systemd.exec.5,access.2}` + grep for footers | exit 0; footers: capabilities(7) and access(2) `2026-02-08`, `Linux man-pages 6.19`; systemd.exec(5) `systemd 262.1` |
| `curl` S020 master raw (`-/raw/master/install/.../limine-snapper-sync.service`) | exit 0, text/plain, sha256 `6fb0d3d4c39523f7…` |
| S020 pinned, raw form `-/raw/cd909745…/...` via `read` | HTTP 403 (not reproducible via raw path) |
| S020 pinned, API form `api/v4/projects/Zesko%2Flimine-snapper-sync/repository/files/…/raw?ref=cd909745ad4ee136aaf4adca6d018e72df81c740` | HTTP 200; sha256 `6fb0d3d4c39523f7…` == master; `diff` exit 0 (byte-identical) |
| S019 pinned, raw form `-/raw/4695dd1c…/README.md` | HTTP 200 but body is a Cloudflare "Just a moment..." challenge page (5807 bytes); no README content |
| S019 pinned, API form `…/repository/files/README.md/raw?ref=4695dd1c2cf9c9b8bcf1c174a9c8593f666d7b66` | HTTP 200; line 137 contains the 4 GiB sentence (same text as master line 137) |
| `curl …wiki.archlinux.org/title/Snapper?oldid=870168` + grep | exit 0; line 1050 contains the S023 sentence and its precondition (see F4) |
| `git rev-parse --short HEAD`; `git status --short`; `git log -- corpus/SOURCES.md`; `git diff --stat HEAD -- corpus/SOURCES.md` | HEAD `b76b5c3`; untracked only `.ufo/waves/round-12/`; SOURCES.md last commit `549ec0c`; SOURCES.md diff empty |
| `strace … /usr/bin/test -w /` (uid 1000) | `access("/", W_OK) = -1 EACCES`; `test` exit 1 |
| `grep` of `tools/tsukuroi-census.sh` for `%a`, mode, root-dir | no root-directory mode probe found (only `stat -c %Y/%W` on sync DBs, lines 1336–1416) |

## Quote validity (S027, S028, S034 and anchors)

- **S027, capabilities(7) § CAP_DAC_OVERRIDE — VERIFIED verbatim.** "Bypass file read, write, and execute permission checks." Footer `2026-02-08`, `Linux man-pages 6.19` matches the registry row.
- **S028, systemd.exec(5) § CapabilityBoundingSet= — VERIFIED verbatim for the first sentence.** "Capabilities listed will be included in the bounding set, all others are removed." Footer `systemd 262.1` matches. Full source sentence: "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets." (see F5 on the note's paraphrase.)
- **S034, access(2) § DESCRIPTION — VERIFIED verbatim.** "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities." Footer `2026-02-08`, `Linux man-pages 6.19`. Same DESCRIPTION also says: "access() does not answer the 'can I read/write/execute this file?' question." (see F1.)
- **capabilities(7) § execve (not cited by the note; read here to test F1/F5).** For a process whose real and effective UIDs are zero: `P'(permitted) = P(inheritable) | P(bounding)`, `P'(effective) = P'(permitted)`. Under `CapabilityBoundingSet=CAP_SYS_ADMIN` a root exec therefore has permitted = effective = {CAP_SYS_ADMIN} (assuming an empty inheritable set, which the unit does not set — [inf] from the unit text).
- **S019, README § Requirements — VERIFIED text, scope truncated (F2).**
- **S020, unit — VERIFIED text at pinned API and master (identical).** Lines: `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`; no `ProtectSystem=` or `ReadOnlyPaths=` lines. Also present and not cited by the note: `NoNewPrivileges=yes`, `SystemCallFilter=@system-service @mount`, `PrivateNetwork=yes`, `ReadWritePaths=/tmp`.
- **S023, Snapper wiki § Creating a new configuration — VERIFIED words, precondition omitted (F4).**

## Findings

Severity: M = medium, L = low. Ordered by impact on the note's mechanism and falsifier.

### F1 (M) — S034 is cited for a discrimination the probe does not perform; the man page's own limit is omitted

- Note line 30: "`access(2)` (S034) explains why this `test -w` comparison distinguishes root's permitted capabilities from its effective capabilities."
- Under the falsifier's own bounding set (`CapabilityBoundingSet=CAP_SYS_ADMIN`), capabilities(7) execve gives permitted = effective = {CAP_SYS_ADMIN} for root (see above). The falsifier therefore does not separate permitted from effective; it separates the presence of CAP_DAC_OVERRIDE. The permitted/effective sentence is wrong for this probe.
- What S034 does ground: `/usr/bin/test` (coreutils, what `systemd-run … test -w /` and `sudo test -w /` execute, since no shell is involved) issues `access("/", W_OK)` — confirmed by the uid-1000 strace above. So the syscall identity is correct, and the probe is a real `access(2)` check, not a `faccessat(AT_EACCESS)` check.
- The same S034 DESCRIPTION states `access()` "does not answer the 'can I read/write/execute this file?' question". The note's R6 and falsifier text acknowledges it is "a permission probe, not a subvolume-create test", but does not carry the man page's stated limit into the claim.
- Risk: a reader can take S034 as proof that the rc=1/rc=0 prediction tests the failing `create subvolume` path. It tests only root's `access(W_OK)` on `/`.
- Recommended wording (not applied; for the note's author): drop "distinguishes permitted from effective"; state S034 grounds only that `/usr/bin/test -w` calls `access(2)` and that root's answer comes from the capability sets; keep the "not a subvolume-create test" caveat and quote the "does not answer" sentence.

### F2 (M) — S019's 4 GiB recommendation is conditional; the note drops the condition

- Source (master line 137 and pinned API line 137, identical): "A FAT32 boot partition of at least **4 GiB** is recommended, **depending on how many snapshots and kernel versions you keep**."
- Note line 15 and Sources line 52 quote "A FAT32 boot partition of at least 4 GiB is recommended" with no ellipsis or qualifier, then state the current `/boot` (2.0G) "is below that recommendation". The recommendation is conditional on snapshot and kernel retention, which this host has not measured.
- Risk: the `/boot` capacity point is presented as a threshold; as sourced it is a retention-dependent recommendation. The note does say `/boot` sizing is "a separate capacity concern, not a cause of this EACCES", which limits the damage.
- Recommended: add the qualifier to the quote, or write "recommends at least 4 GiB depending on retained snapshots and kernels".

### F3 (M) — The S019 and S020 pins are reproducible only through the API form; the note cites the mutable master raw URL

- S020: the note cites `…/-/raw/master/…`. The registry row pins commit `cd909745…`. Pinned raw form returned HTTP 403 in this pass; pinned API form (`…/repository/files/…/raw?ref=cd909745…`) returned HTTP 200 and is byte-identical to master (sha256 `6fb0d3d4c39523f7…`). So the pin holds today, but only via the API path. The note's Sources line 53 cites master and says "registry row pins commit cd909745" without giving the pin-reproducing URL.
- S019: the registry pins `4695dd1c…`. The pinned raw URL returns a Cloudflare challenge (HTTP 200, 5807 bytes of HTML), not the README. The pinned API form returns the README and the line-137 text. The note's Sources line 52 cites master and says "registry row pins commit 4695dd1c"; the raw pin is not usable.
- Risk: a later non-author check that follows the registry's own URL gets a challenge page or 403 and cannot reproduce the quote. The note's `verified-at` line ("re-opened S019-S020") is accurate only for the API or master forms, not the pinned raw forms.
- Recommended: record the API-form URL for each pinned row in SOURCES.md and cite it in the note; record the sha256 of the fetched body, which is the only check that survives a mutable branch.

### F4 (L) — S023's quoted sentence drops its precondition

- Wiki source (oldid 870168, line 1050): "If you installed Arch using the suggested Btrfs partition layout from archinstall version older than 3.0.5 [1] then the @.snapshots subvolume will already be mounted to /.snapshots, and the snapper create-config command will fail [2]."
- Note line 54 quotes "the `@.snapshots` subvolume will already be mounted to `/.snapshots`, and the `snapper create-config` command will fail" without the archinstall-version precondition. The R6 rejection (line 19) rests on `stat /.snapshots` (no such file) and errno 13 vs "already exists". It does not check the install layout or archinstall version, which the source makes the trigger.
- Risk: low; the rejection is still supported by the errno evidence. But R6 is presented as a rejection of a precondition the host was never shown to fail.
- Recommended: quote the precondition, and note that the archinstall version and install layout were not inspected.

### F5 (L) — S028 paraphrase is stronger than the source

- Note line 14: capabilities omitted from `CapabilityBoundingSet=` "are removed from the process's bounding, effective, and permitted sets." Source (systemd.exec(5)): "all others are removed" refers to the bounding set; the effective, permitted and inheritable sets are described as "also affected".
- The stronger statement is correct under capabilities(7) execve for root (F1 above), but the note cites S028 for it. Cite capabilities(7) execve for the effective/permitted claim.

### F6 (L) — The falsifier restricts only the bounding set; the unit's other hardening is not reproduced

- The unit (S020, master and pinned API) also sets `NoNewPrivileges=yes`, `SystemCallFilter=@system-service @mount`, `PrivateNetwork=yes`, `ProtectHome=yes`, `RestrictNamespaces=yes`, `ReadWritePaths=/tmp`. The note's falsifier is `systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`, which applies none of those. The note's "LSM untested" caveat covers LSM only.
- Consequence: rc=1 under the falsifier shows the bounding-set mechanism in isolation; it does not show the real unit's behavior, and an rc=0 would falsify only the isolated mechanism. The note's wording ("The first returning 0 falsifies the proposed DAC/capability mechanism") is correct for the isolated probe; it should not be read as a test of the unit.
- Recommended: state the falsifier's reduced scope in the falsifier paragraph.

### F7 (L) — SOURCES.md mutable-field handling is ad hoc

- `corpus/SOURCES.md` has no written mutable-field rule. Mutable handling appears only in two row texts: S006 (line 12, "mutable: the earlier recorded blob id did not reproduce … no commit pin is claimed") and S024 (line 30, "mutable: main now opens with CHANGES WITH 263 …; no commit pin claimed"). Both correctly withdraw the pin.
- S019 and S020 carry commit pins while their anchors and the note cite `master`. S023 is pinned by oldid. S027, S028 and S034 are man.archlinux.org renders with no pin; their footers (date and package version) are recorded in the rows and verified here. Footer date is a version marker, not a content hash.
- Recommended rule (proposal, not applied): every mutable-branch row records (a) the API or commit-pinned URL that reproduces, (b) the sha256 of the fetched body, (c) the rendered footer version/date for man pages; and a row whose pin does not reproduce is set to `mutable` with no pin claim, as S006 and S024 do.

### F8 (info) — No visible source additions beyond S034; SOURCES.md unchanged in the working tree

- Registry ends at S034 (rows S030 and S033 rejected; S029 rejected). `git diff --stat HEAD -- corpus/SOURCES.md` is empty; last SOURCES.md commit is `549ec0c`, an ancestor of HEAD `b76b5c3`. `git status --short` shows only `.ufo/waves/round-12/` untracked.
- S030's row cites a path outside this repo (`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md`). It is rejected (tier C), so no support depends on it, but the row is not reproducible from this repository.

### F9 (info, other seats) — census root-directory mode probe not found in the grep

- `grep` of `tools/tsukuroi-census.sh` for `%a`, mode and root-directory patterns matched only `stat -c %Y` and `%W` on sync DBs (lines 1336–1416). I did not read the census for the root-metadata claim; C1 belongs to the census and root-live seats. Flagged, not judged.

## Verified (no finding)

- S027 quote and footer; S028 first quote and footer; S034 quote and footer (exact text matches the note).
- S020 unit text: `CapabilityBoundingSet=CAP_SYS_ADMIN`, `User=root`, `ProtectHome=yes`, no `ProtectSystem`/`ReadOnlyPaths` lines — identical at master and at the pinned API ref.
- The note's mechanism ("the unit's bounding set lacks CAP_DAC_OVERRIDE, and root's DAC bypass is capability-gated") is consistent with S027 and S028 text. Still `[inf]`, as the note says.

## Residual risk and verification gaps

- The falsifier was not run (operator-only). Its predicted rc values are from the mechanism, not observation.
- No root probe was run; the `/` mode, unit, and journal claims are the note's own host measurements and were not re-measured here.
- The note's R6 rejection does not check the archinstall version or btrfs subvolume inventory (F4).
- Author-side advisory only. This is not independent non-author verification.

## Recommended edits to the note (for its author; not applied by this seat)

1. F1: remove the permitted-vs-effective sentence attributed to S034; keep the S034 quote and its "does not answer" limit.
2. F2: add the "depending on how many snapshots and kernel versions you keep" qualifier to the S019 quote.
3. F3: cite the API-form pinned URL for S019 and S020, with the sha256 of the fetched bodies.
4. F4: quote the S023 precondition.
5. F5: cite capabilities(7) execve for the effective/permitted claim.
6. F6: state the falsifier's reduced scope.
## Addendum — exact excerpts for the parent's correction block (2026-10-20T02:17Z UTC)

Scope: this addendum adds exact source excerpts. It does not restate the findings above. The old note is not modified here; the parent appends its correction. Excerpts are ≤25 words each; no secret or host material is included.

### F2 — S019 conditional 4 GiB recommendation

- Location: `## Requirements`, first bullet, line 137 of the README.
- URL (mutable branch): https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/README.md — fetched 2026-10-20T02:17Z UTC (2026-10-19 local, -03). The note's stated fetch date is 2026-10-19; the body sha256 prefix is `ad989ac3c0884f04`.
- Pinned reproduction (commit `4695dd1c2cf9c9b8bcf1c174a9c8593f666d7b66`): the API form `https://gitlab.com/api/v4/projects/Zesko%2Flimine-snapper-sync/repository/files/README.md/raw?ref=4695dd1c2cf9c9b8bcf1c174a9c8593f666d7b66` returns the same line 137. The raw pinned form returns a Cloudflare challenge page and is not usable.
- Exact excerpt (21 words): "A FAT32 boot partition of at least 4 GiB is recommended, depending on how many snapshots and kernel versions you keep."
- Markdown bold markers (`**4 GiB**`) are stripped in the excerpt.

### F5 — S028 CapabilityBoundingSet= paragraph

- Location: systemd.exec(5), `CapabilityBoundingSet=` entry; systemd 262.1 man-page footer. URL: https://man.archlinux.org/man/systemd.exec.5 — fetched 2026-10-20T02:17Z UTC. HTML entities decoded; line wraps joined.
- Paragraph, in ≤25-word segments (no segment is cut mid-sentence except where noted):
  1. "Controls which capabilities to include in the capability bounding set for the executed process. See capabilities(7) for details." (18 words)
  2. "Takes a whitespace-separated list of capability names, e.g. CAP_SYS_ADMIN, CAP_DAC_OVERRIDE, CAP_SYS_PTRACE." (15 words)
  3. "Capabilities listed will be included in the bounding set, all others are removed." (13 words)
  4. "If the list of capabilities is prefixed with "~", all but the listed capabilities will be included, the effect of the assignment inverted." (23 words)
  5. "Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets." (17 words)
  6a. "If this option is not used, the capability bounding set is not modified on process execution," (16 words)
  6b. "hence no limits on the capabilities of the process are enforced." (11 words)
  7a. "This option may appear more than once, in which case the bounding sets are merged by OR, or by AND" (20 words)
  7b. "if the lines are prefixed with "~" (see below)." (9 words)
  8a. "If the empty string is assigned to this option, the bounding set is reset to the empty capability set," (19 words)
  8b. "and all prior settings have no effect." (7 words)
  9. "If set to "~" (without any further argument), the bounding set is reset to the full set of available capabilities, also undoing any previous settings." (25 words)
  10. "This does not affect commands prefixed with "+"." (8 words)
- Bearing on F1/F5: the source says the bounding-set option "also affects" the effective, permitted and inheritable sets (segment 5). It does not say "removed" from those sets. The "removed" wording in the note is an inference from capabilities(7) execve, which for a root exec gives P'(permitted) = P(inheritable) | P(bounding) and P'(effective) = P'(permitted) — the basis for F1 (permitted = effective under the unit's bounding set).

### F1 — S034 scope (for the correction block)

- access(2) DESCRIPTION, https://man.archlinux.org/man/access.2, footer 2026-02-08, Linux man-pages 6.19. Excerpt (≤25 words): "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities." (19 words)
- Same DESCRIPTION, exact excerpt (11 words): "access() does not answer the 'can I read/write/execute this file?' question."
- Operational boundary: the probe `/usr/bin/test -w /` issued `access("/", W_OK)` (non-root strace, exit 1). Under the falsifier's bounding set, permitted and effective are both {CAP_SYS_ADMIN}, so this probe does not separate them. It is a permission probe, not operational proof of the subvolume-create failure.

### Stated limits of this addendum

- Author-side advisory; not independent verification.
- Re-fetched 2026-10-20 UTC, not the note's 2026-10-19 local fetch; the S019 body hash is recorded for the mutable branch only.
- No note text was modified.
