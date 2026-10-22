# SrcOmarchyMirror — C2/P4 source: what sets this host's Arch mirror and how the stable mirror advances

Verdict: the primary source that sets this host's Arch repo mirror is the Omarchy installer script `install/post-install/pacman.sh` from the exact release installed on this host (tag `v3.8.4`), whose second command copies the shipped template `default/pacman/mirrorlist-stable` over `/etc/pacman.d/mirrorlist`; the template and the host's live mirrorlist are byte-identical (`Server = https://stable-mirror.omarchy.org/$repo/os/$arch`). What the stable mirror is and how it advances is documented officially in the `omarchy-mirror` README (it serves the Arch snapshot the current Omarchy release was tested against, and changes only when a release ships, by promoting snapshots upstream → rc → stable) and in the official manual page (the stable channel's mirror runs about one month behind the latest Arch). Live probes confirm the mirror advances by promotion and that the host's local databases currently lag the served snapshot.

Scope of this seat: locate and open the primary upstream source that sets this host's repo mirror, plus official documentation of the stable mirror and its update cadence; verify the host's live mirrorlist against the upstream template; probe the live mirror's freshness endpoints; draft two SOURCES rows. Host actions were read-only (no pacman transaction, no service action, no config write, no git write).

---

## 1. What sets this host's mirror: the Omarchy installer, at the installed release

1.1 [obs] The host runs an Omarchy git checkout at `~/.local/share/omarchy`, exactly at tag `v3.8.4` (branch `master`, clean tree, remote `https://github.com/basecamp/omarchy.git`).
- Evidence: `git -C ~/.local/share/omarchy describe --tags --exact-match` → exit 0, output `v3.8.4`; `git -C ~/.local/share/omarchy rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'` → exit 0, output `master`; `git -C ~/.local/share/omarchy status --porcelain` → exit 0, empty; `git -C ~/.local/share/omarchy remote -v` → `origin https://github.com/basecamp/omarchy.git (fetch)`.

1.2 [obs] The installer step that sets the mirror is `install/post-install/pacman.sh:3` of the installed release: it copies the channel template whole onto `/etc/pacman.d/mirrorlist`, defaulting to `stable` when `OMARCHY_MIRROR` is unset.
- Evidence: `/home/vgpnk/.local/share/omarchy/install/post-install/pacman.sh` lines 1–3: `# Configure pacman` / `sudo cp -f ~/.local/share/omarchy/default/pacman/pacman-${OMARCHY_MIRROR:-stable}.conf /etc/pacman.conf` / `sudo cp -f ~/.local/share/omarchy/default/pacman/mirrorlist-${OMARCHY_MIRROR:-stable} /etc/pacman.d/mirrorlist`.
- Evidence: upstream tag URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/install/post-install/pacman.sh` opened 2026-10-22 — same three lines verbatim (quote at most 25 words: `sudo cp -f ~/.local/share/omarchy/default/pacman/mirrorlist-${OMARCHY_MIRROR:-stable} /etc/pacman.d/mirrorlist`).
- Evidence: the host's installed file and the upstream tag file hash identically — `sha256sum` of both is `6dcfba64f096ac0f9d4bc44aaef2d22c90fa8639cdb20d012f62b44189b5c60c`.

1.3 [obs] The mirror template itself at the installed release is the single line the host's live mirrorlist contains.
- Evidence: upstream tag URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/pacman/mirrorlist-stable` opened 2026-10-22 — content: `Server = https://stable-mirror.omarchy.org/$repo/os/$arch`, sha256 `6c4a944bed4bb1c104ed53da8856e5440c22c143511b9989c0e3125697476091`.
- Evidence: `/etc/pacman.d/mirrorlist:1` — `Server = https://stable-mirror.omarchy.org/$repo/os/$arch`; `sha256sum /etc/pacman.d/mirrorlist` → `6c4a944bed4bb1c104ed53da8856e5440c22c143511b9989c0e3125697476091` (byte-identical to the upstream template).
- Evidence: host file mtime `2026-10-03 17:45:41 -0300` (when the installer wrote it).

1.4 [obs] The template's current content was introduced upstream on 2025-11-10 by commit `2425f4d3e0ec868358b2d5cf3e2b28d5f85c0eed` ("Default to the new stable mirror", David Heinemeier Hansson), and the file has not changed there since.
- Evidence: in a shallow-then-full clone of `https://github.com/basecamp/omarchy` into `/fast/scratch/hyaku/tsuku24-SrcOmarchyMirror-2/omarchy`, `git log --format='%H %ci %s' -- default/pacman/mirrorlist-stable` lists only `2425f4d3e0ec868358b2d5cf3e2b28d5f85c0eed 2025-11-10 ... Default to the new stable mirror`; `git show 2425f4d3e0ec868358b2d5cf3e2b28d5f85c0eed -- default/pacman/mirrorlist-stable` confirms the added line.
- [inf] Therefore the host's mirror URL is upstream-set and has been stable in content since 2025-11-10; no local edit or host-side mirror configuration is present.

## 2. What the stable mirror is and how it advances (official documentation)

2.1 [obs] The official `omarchy-mirror` project README defines the stable mirror and its advance rule.
- Evidence: URL `https://raw.githubusercontent.com/omacom/omarchy-mirror/a2a669f858c501e9b90748f2fe1b8f1e08b643d4/README.md` opened 2026-10-22 (master, pinned to commit `a2a669f858c501e9b90748f2fe1b8f1e08b643d4`), line 7 — quote: `it serves the Arch snapshot the current Omarchy release was tested against. It changes only when a release ships` (20 words).
- Evidence: same file line 23 — quote: `Snapshots only move forward, from upstream to rc to stable, and stable never syncs from upstream itself.` (18 words); the same section adds that the copy to stable refuses to move it to an older snapshot than it serves.
- Evidence: same file line 11 — quote: `The edge mirror tracks the very latest Arch repositories every hour.` (for contrast with stable's release-driven cadence).

2.2 [obs] The official Omarchy manual page describes the stable channel's mirror cadence as about one month behind the latest Arch.
- Evidence: URL `https://omarchy.org/manual/updates/` opened 2026-10-22 (native HTML) — quote: `New installations start on the stable channel, which tracks the official releases, as well as the stable Omarchy Arch mirror` (20 words); the page continues `that’s running one month behind the latest, so we can catch any new incompatibilities that require config changes before they cause problems for people`.
- [obs] The manual links the mirror project at `https://github.com/omacom-io/omarchy-mirror`, which 301-redirects to `https://github.com/omacom/omarchy-mirror` (final HTTP 200); the working repo is `omacom/omarchy-mirror` (commit pinned above). The omarchy project itself is at `github.com/basecamp/omarchy`, which redirects to `github.com/omacom/omarchy` (git ls-remote on the basecamp URL returns the same commit IDs).

2.3 [obs] The mirror's own build script implements the promotion rule: stable is a copy of the rc stage, never a sync from upstream.
- Evidence: URL `https://raw.githubusercontent.com/omacom/omarchy-mirror/master/bin/omarchy-mirror-sync-stable-from-rc` opened 2026-10-22 — quote: `Stable never syncs from upstream, which would publish today's Arch instead;` and quote: `Copy the rc stage over the stable stage, then upload that as it is.` The README adds `Promote the mirror before the packages.` and that `stable-mirror.omarchy.org/lastsync` matches `rc-mirror.omarchy.org/lastsync` once the copy is up.

## 3. Live probe of the advancing mirror (relevant to P4)

3.1 [obs] The live stable mirror exposes freshness stamps that confirm recent advancement by promotion.
- Evidence: `curl -sS https://stable-mirror.omarchy.org/lastsync` → `1792636269`, which is 2026-10-22 02:31:09 UTC = 2026-10-21 23:31:09 -0300.
- Evidence: `curl -sS https://stable-mirror.omarchy.org/lastupdate` → `1792635447`, which is 2026-10-22 02:17:27 UTC = 2026-10-21 23:17:27 -0300.
- Evidence: `curl -sSI https://stable-mirror.omarchy.org/core/os/x86_64/core.db` → `Last-Modified: Thu, 22 Oct 2026 04:40:03 GMT` (= 2026-10-22 01:40:03 -0300), HTTP 200.

3.2 [obs] The served core database is not the same content the host synced last: 19 core package versions on the mirror are newer than the host's local sync database.
- Evidence: `bsdtar -tf /var/lib/pacman/sync/core.db | grep '/desc$' | sort` vs same for the downloaded `https://stable-mirror.omarchy.org/core/os/x86_64/core.db` → 19 differing package entries, e.g. `dbus-1.16.2-2` (served) vs `dbus-1.16.2-1` (local), `debuginfod-0.197-1` vs `debuginfod-0.196-1`, `ca-certificates-mozilla-3.131.1-1` vs `ca-certificates-mozilla-3.130.3-1`; served core.db sha256 `d7624a52e83a475cbc4dea040bbb6aa92be6b17a0b39b7b77f5c7a3a44e1ccf` vs local `9b81b888f4e38b35a729dfa8a476837f198778602eb049eb7d8f2f22db3f0e09`.
- Evidence: `stat -c '%y %s %n' /var/lib/pacman/sync/core.db` → `2026-10-17 22:37:29.468679223 -0300`, 130249 bytes (local mtime and size).

3.3 [inf] Chain consistent with both the host capture and the source above: the host's last `pacman -Sy --noconfirm` ran at 2026-10-21 20:32 -0300 (pacman.log line 3188), before the mirror's latest advance (lastsync 2026-10-21 23:31 -0300); at that moment the mirror still served content identical to the host's 2026-10-17 databases, so pacman's conditional GET (If-Modified-Since on the existing db mtime) returned not-modified and did not rewrite the local db files — preserving the 2026-10-17 mtimes. The mirror then advanced a few hours later, so the host's local databases now lag the served snapshot by the 19 versions noted in 3.2.
- Evidence for the pacman mechanism: upstream alpm source `https://gitlab.archlinux.org/pacman/pacman/-/raw/master/lib/libalpm/dload.c` opened 2026-10-22 — lines 419–425 set `CURLOPT_TIMECONDITION = CURL_TIMECOND_IFMODSINCE` with the existing file's mtime when not forced; the 304 path in `curl_download_internal` cleans the temp file and returns without renaming (`file met time condition` → `unlink(payload->tempfile_name)`, `goto cleanup`, `ret = 1`), so the local db file and its mtime are untouched.
- [unk] I did not verify what the mirror served at the exact 20:32 moment on 2026-10-21; the above chain is inferred from the flag stamps, the local db mtime, and the current served content.

## 4. Draft SOURCES rows (for the L1 to number and merge)

All rows: `tier` = A, `opened` = 2026-10-22, `status` = mined, `recheck` = on-release, `used-by` = `corpus/knowledge/pause-lift-gate-r24.json` (planned C2 gate entry). `id` left as `S0NN` placeholders for the L1. Each quote is copied exactly from the opened page and is at most 25 words.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | Omarchy installer pacman setup (release installed on this host) — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/install/post-install/pacman.sh ; https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/pacman/mirrorlist-stable | code | A | The upstream installer step that writes /etc/pacman.d/mirrorlist from the channel template, and the stable template it copies; pinned to the tag installed on this host | tag v3.8.4 opened 2026-10-22; quote: `sudo cp -f ~/.local/share/omarchy/default/pacman/mirrorlist-${OMARCHY_MIRROR:-stable} /etc/pacman.d/mirrorlist`; quote: `Server = https://stable-mirror.omarchy.org/$repo/os/$arch` | The host's mirror is set by Omarchy's installer copying the shipped mirrorlist-stable template; the host's /etc/pacman.d/mirrorlist is byte-identical to that template (sha256 6c4a944b…), and the template content has been unchanged upstream since 2025-11-10 | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |
| S0NN | Omarchy Mirror README — https://raw.githubusercontent.com/omacom/omarchy-mirror/a2a669f858c501e9b90748f2fe1b8f1e08b643d4/README.md | docs | A | What the stable mirror serves and the rule by which it advances; pinned master commit a2a669f858c501e9b90748f2fe1b8f1e08b643d4 | README.md:7 and :23 opened 2026-10-22; quote: `it serves the Arch snapshot the current Omarchy release was tested against. It changes only when a release ships`; quote: `Snapshots only move forward, from upstream to rc to stable, and stable never syncs from upstream itself.` | The stable mirror is a release-tested Arch snapshot that advances only on Omarchy releases by promoting rc → stable; it never syncs from upstream, so it can legitimately lag the latest Arch between releases | mined | 2026-10-22 | on-release | corpus/knowledge/pause-lift-gate-r24.json |

Alternate row candidate (not drafted as a third row, since this seat was asked for one or two): the official manual page `https://omarchy.org/manual/updates/` (quote: `the stable Omarchy Arch mirror that’s running one month behind the latest`) corroborates the cadence in prose; the L1 may prefer it over or alongside the README row.

## 5. Out of scope and limits

- [obs] Not performed: any pacman transaction (including `-Sy`, `-Syu`, `-Scc`), paccache, service action, config write, git/jj write, boot action. All host commands were read-only.
- [obs] Read-only commands used: `git` describe/rev-parse/status/remote/log/show on the host checkout and on the scratch clone at `/fast/scratch/hyaku/tsuku24-SrcOmarchyMirror-2/omarchy` (cloned with `git clone --depth 1` then `git fetch --unshallow`; upstream repo, not a lane repo), `sha256sum`, `stat`, `cat`, `sed -n`, `bsdtar -tf`, `python3` text extraction of the manual HTML, and `curl -sS`/`curl -sSI` GET requests to the public URLs listed above.
- [unk] The live mirror's exact served content at the host's 2026-10-21 20:32 sync moment was not verified; the 304/not-modified explanation is inferred from alpm source and the observed stamps.
- [unk] The `basecamp/omarchy` redirect target `omacom/omarchy` was not cloned; only the basecamp URL was used, consistent with the host checkout's own remote URL.

Scope: read=upstream omarchy installer and mirror template at tag v3.8.4, omarchy-mirror README and sync script (pinned commits), the official manual page /manual/updates/, pacman alpm dload.c, the host's /etc/pacman.d/mirrorlist and /var/lib/pacman/sync/*.db, and live stable-mirror.omarchy.org freshness endpoints; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/SrcOmarchyMirror.md; executed=read-only host queries (git log/show/describe/rev-parse/status/remote, sha256sum, stat, cat, sed, bsdtar, python3) and HTTP GETs of the URLs listed above
Installs: none
