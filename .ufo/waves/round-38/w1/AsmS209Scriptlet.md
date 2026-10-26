VERDICT: supports

# AsmS209Scriptlet — Item A-3 (staged S209 re-open)

Access date: 2026-10-26 (host `date +%F`). Page: https://man.archlinux.org/man/alpm-install-scriptlet.5, HTTP 200, 8737 bytes, sha256 `a18a5c60aac7d1488849cf6deeacf21261ededcdf122dc522301026f11174dc7`. Receipt: `.ufo/waves/round-38/w1/AsmS209Scriptlet/s209-alpm-install-scriptlet.5-2026-10-26.html`.
Version footer (HTML `Package information`): `Package name: extra/alpm-docs`, `Version: 0.13.0-1`, `Licenses: CC-BY-SA-4.0`. The page prints no man-page date. This matches the staged header `package extra/alpm-docs 0.13.0-1` (staged `pacman-hook-timing-r25.md:4`).
Staged claim under test: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md:47-51`, "The scriptlet contract".

## 1. Claim verification (alpm-install-scriptlet(5), alpm-docs 0.13.0-1, accessed 2026-10-26)

| # | staged claim (r25.md:47-51) | verdict | section | quote (≤25 words) |
|---|---|---|---|---|
| 1a | `.INSTALL` functions run in the system root `/`, so paths must be absolute | **present** | `DESCRIPTION` (opening paragraphs; not `Functions`) | "The shell functions are executed in the root (/) of the system, so all paths inside of it must be absolute." |
| 1b | `pre_upgrade` and `post_upgrade` take the **new** version first, old second | **present** | `DESCRIPTION` → `Functions` (`h2 id=Functions`) | `pre_upgrade`: "Executed before a package is upgraded, with the following arguments: 1. New package version 2. Old package version". `post_upgrade` has the same two arguments in the same order. |
| 1c | interpreter is chosen globally by the distribution and cannot be selected per package | **present, staged wording slightly tighter** | `DESCRIPTION` → `General Format` (`h2 id=General_Format`; not `Functions`) | "the shell interpreter used by package management software to run the script is defined globally (e.g. per distribution)"; "This implies that the shell interpreter cannot be changed on a per-package basis." |

Also on the page and consistent with the staged table row (r25.md:17):
- File location and name: "Such files are located at the root of ALPM packages and are named .INSTALL."
- All six functions are listed: `pre_install`, `post_install`, `pre_upgrade`, `post_upgrade`, `pre_remove`, `post_remove`.
- Install and remove functions take a single version argument. Install passes the new version, remove passes the old.
- The interpreter must support `-c` and calling named functions, and "No shebang is used in the script".

Defects in the staged entry (none flips a claim; all are citation precision):
1. **Citation locator.** `r25.md:4` cites `# DESCRIPTION` / `# Functions`. Claim 1c lives in `General Format`, and claim 1a in the DESCRIPTION lead-in. Both are inside DESCRIPTION, but only 1b is in `Functions`. Proposed locator: `# DESCRIPTION` / `## General Format` / `## Functions`.
2. **"by the distribution".** The page says "defined globally (e.g. per distribution)" and "typically set at the distribution or system level". The staged text states the distribution as the sole chooser. Proposed wording: "chosen globally (typically per distribution or system), never from package metadata".
3. **Order claim is not in S209.** `r25.md:35-39` ("old version's pre-transaction hooks, then the new version's install-scriptlet functions, then the new version's post-transaction hooks") is **absent** from this man page. The page has no transaction-order statement. That claim must stay on its S202/S201 sources and must not be read as backed by S209.
4. **Source-id collision.** The staged entry uses S201, S202, S209 and S212. The lane registry `corpus/SOURCES.md` already assigns these ids to other sources:
   - S201 = Btrfs ioctl.c (`SOURCES.md:210`)
   - S202 = errno(3) (`SOURCES.md:211`)
   - S209 = alpm-hooks(5) source at pacman 54d9411 (`SOURCES.md:218`)
   - S212 = round-38 host hook capture (`SOURCES.md:221`)

   The registry's last row is S212 (`grep -oE '^\| S[0-9]+' corpus/SOURCES.md | tail -3` → S210, S211, S212). `grep -n alpm-install-scriptlet` over `corpus/SOURCES.md` and `corpus/knowledge` returns nothing, so the scriptlet man page is unregistered in the lane. Importing the staged entry as written would make "S209" ambiguous with the C2 source row that HO1-HO7 depend on. It needs fresh ids (next free is S213+, subject to what other seats claim) and a registry row before admission.
5. The staged `ground:` line cites `corpus/README.md:38-42` for a "packaging-and-hook-semantics frontier". In this lane at HEAD `5edb6c2e`, README:38-42 hold the mkinitcpio-42 and errno:13 items, and `grep -n -iE 'packaging-and-hook|hook-semantics|install scriptlet'` over `corpus/README.md SKILL.md PROVINCE.md` has no hit. The ground pointer does not resolve here.

Not done: I did not fetch the `.txt` rendering (TLS EOF on one attempt; the HTML was fetched and hashed instead). I did not re-verify S201/S202/S212 (outside item A-3).

## 2. PROVINCE.md: Core or Frontier?

**Judgement: Core (read-only detection and attribution of package install scriptlets); there is no Frontier row for it. Authoring or running scriptlets, or any remediation, is not owned.**

Evidence:
- Core "Owns" pacman state (`PROVINCE.md:8-9`), "`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline", plus update-safety questions ("what an -Syu would touch", `PROVINCE.md:13-14`). An install scriptlet is a member of a package's installed state: it is recorded as `Install Script` and as the `install` file under `/var/lib/pacman/local/<pkg>-*/`.
- The lane already reads scriptlets under that Core surface. `corpus/knowledge/aur-risk-plane.md:202` has an R6 row, "install-time code execution — `install` scriptlet in the package", read from `%INSTALL%` / `/var/lib/pacman/local/<pkg>-*/install` (fires 0/16, "all `Install Script: No`"). `SKILL.md:753` repeats it ("install-scriptlets 0/16"). `corpus/knowledge/degraded-triage-r4.md:61,113` use a vendor `.INSTALL` script as evidence of package drift by design.
- Scriptlet effects are already attributed in the Core boot-writer work. `corpus/knowledge/boot-writers-r19.md:40,68-71,91` and `tools/check-boot-writers.py:45,196-197` classify `[ALPM-SCRIPTLET]` pacman.log lines.
- Frontier (`PROVINCE.md:75-80`, plus the dated round-26 storage frontier at `:154-174`) lists only: handoff acknowledgement, the kaidoku/revenger RE ownership, and storage integrity. Storage integrity is the only area with the "Core only after a census arm exists" rule (`PROVINCE.md:169-170`). No Frontier text mentions scriptlets, hooks or `.INSTALL`.
- Boundary from Core: "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates" (`PROVINCE.md:27-28`). Reading a scriptlet's existence, arguments and effects stays in scope. Executing, editing or replaying one, or running a transaction, does not.
- Gap, not a province change: `grep -n -iE 'ALPM-SCRIPTLET|Install Script|hook' tools/tsukuroi-census.sh` returned no match. The census has no scriptlet arm (the R6 reading comes from an AUR-plane capture). By the storage precedent, this means the scriptlet contract is "Core by owned surface, but a documented reference without a census probe". It is not a Frontier item the province text lists. If the lane wants the stricter "Core only with a census arm" reading it applied to storage, scriptlets would be Core-by-surface with a carried-debt census arm. That would be a new declaration for a later round, not an A-3 finding.

Proposed text for a staged-entry placement note (not applied; I wrote nothing outside my report):

> Install scriptlets (`.INSTALL`, `alpm-install-scriptlet(5)`) sit inside the Core "pacman state" surface (`PROVINCE.md:8-9`) as read-only detection: presence per package (`Install Script`, `/var/lib/pacman/local/<pkg>/install`) and `[ALPM-SCRIPTLET]` attribution in pacman.log. The contract (run in `/`, absolute paths, new-version-first upgrade arguments, one global interpreter) is reference for that reading. Running, editing or replaying scriptlets stays operator-owned.

## Reproduction

- `date +%F` → 2026-10-26.
- `curl -sSL -o page.html https://man.archlinux.org/man/alpm-install-scriptlet.5 -w '%{http_code} %{size_download}'` → `200 8737`.
- `sha256sum` of the receipt matches the hash above.
- Text rendering via a regex strip, then compared against the quotes above.
- `grep -A3 'Version:'` on the receipt → `0.13.0-1`. `grep -c alpm-docs` → 2.

No lane or host mutation, no installs. Scratch `/fast/scratch/hyaku/tsukuroi-r38/AsmS209Scriptlet/` removed. Only the receipt dir and this report were written.
