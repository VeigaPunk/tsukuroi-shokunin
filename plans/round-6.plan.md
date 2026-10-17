# WWKD plan — tsukuroi round 6 (ufo-round-plan-v1)
Axis move: coverage (the foreign/AUR-risk plane) + freshness (per-package
provenance re-measured from live state and logs, never quoted).

Claim: the lane's owned surface "foreign/AUR census" (PROVINCE.md:6-7) —
counted by the gate but never measured per package — becomes a plane: all 16
foreign packages (re-measured 2026-10-14T17:03Z: 1188 installed, 16 foreign,
3 explicit + 13 omarchy-walker deps; all 16 absent from every sync db,
`pacman -Si` rc≠0; deps satisfied now, `pacman -T` rc=0) get a provenance +
risk register (`corpus/knowledge/foreign-aur-risk-plane.md`) with at least
these two measured classes and their operator actions: (i) **offline-exile**
— the 13 elephant-* + omarchy-walker: channel was the installer's
`offline.db` (installed 2026-10-03 17:44:26, never configured after), no
update path; exposure `omarchy-walker → walker` (omarchy channel, 2.17.0-1),
so a silent version break degrades the launcher; (ii) **AUR-local** —
android-apktool-bin (2026-10-13 13:52:59) and obsidian-cli-inspector
(16:21:20): `pacman -U` of yay build-cache artifacts (`~/.cache/yay/<pkg>`),
`Validated By: None`, Packager unknown; update path = the AUR helper itself
(yay 13.0.1-1, omarchy channel), so the risk is review-on-update discipline.
The register lands P4's owed "record the accepted baseline" as a
machine-readable baseline the census reads, so the packages plane reports
`foreign=` as known-vs-new instead of a bare count — fail-closed: a baseline
entry can hide neither a new foreign package nor a version change — with
selftest fixtures; SKILL.md's package/update-safety rows gain the
foreign-risk rule. Gate extension point (draft-verified):
`tools/tsukuroi-census.sh:303-325` (foreign count arm) + the
`degraded-foreign` fixture at `:820-822`.

Anti-claim: provenance a read-only probe cannot settle (a build dir cleaned,
no cache/log trail) gets an honest `unknown-provenance` row with the exact
operator probe — never a guessed channel; no ELF/linkage internals
(`readelf`/`ldd`) — if a risk class needs linkage evidence the row reads
`out of reach` and the question is reported to kaidoku/revenger, never
absorbed; the baseline splits the count but must not raise a DEGRADED verdict
to HEALTHY.

Measure: register rows = the live foreign count (16 at draft); census
selftest green incl. ≥3 new baseline fixtures (hit / new / version-drift);
every class cites its probe (date + command); zero host mutation.
