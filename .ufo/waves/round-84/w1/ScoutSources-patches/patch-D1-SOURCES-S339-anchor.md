# Patch D1 — SOURCES.md S339 anchor range excludes the "Description" title it names

Status: **proposed, NOT applied.** The lane repo was not modified. The L1 decides whether this lands.
Target: `corpus/SOURCES.md:350` (row S339), lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
lane revision measured: `f19e73f3aa9817e76044e4e43a343c6ca6d929df`.

## Defect

`corpus/SOURCES.md:350` declares, for S339:

    tag v262, raw lines 36-50 (Description); pinned snapshot .ufo/waves/round-84/before/src/systemd-hibernate-resume.service.xml sha256 170fb1f7…

but in `systemd-hibernate-resume.service.xml` (re-fetched live 2026-11-06, sha256
`170fb1f73bf34c85e20418168a649b45cd9e30d8b979a4f247860ec3ca3a43c5`, HTTP 200) the section boundaries are:

```
 31   <refsect1>
 32     <title>Description</title>
 33
 34     <para><filename>systemd-hibernate-resume.service</filename> initiates the resume from hibernation.</para>
 35
 36     <para><command>systemd-hibernate-resume</command> only supports the in-kernel hibernation
 ...
 50     In such cases, the boot is ordinarily continued.</para>
 51   </refsect1>
```

So the `<title>Description</title>` (raw line 32) and the first paragraph (raw lines 34-35) sit outside the
cited 36-50 range: the anchor is labelled "(Description)" but does not cover the Description title.
Verified with `sed -n '31,52p'` on the fetched copy (see the seat report §4/§6).

Impact: no HR row is affected — HR7 cites line 38, inside the range — and the counter still reads 10/10.
This is a registry-anchor accuracy repair only.

## Proposed change (single line, `corpus/SOURCES.md:350`)

```
- tag v262, raw lines 36-50 (Description); pinned snapshot .ufo/waves/round-84/before/src/systemd-hibernate-resume.service.xml sha256 170fb1f73bf34c85e20418168a649b45cd9e30d8b979a4f247860ec3ca3a43c5
+ tag v262, raw lines 31-51 (Description section: title at 32), 38 (the major:minor write); pinned snapshot .ufo/waves/round-84/before/src/systemd-hibernate-resume.service.xml sha256 170fb1f73bf34c85e20418168a649b45cd9e30d8b979a4f247860ec3ca3a43c5
```

Both endpoints were verified against the live-fetched snapshot: 31 = `<refsect1>`, 32 =
`<title>Description</title>`, 51 = `</refsect1>`, 38 = the cited HR7 line.

## Verification after landing (read-only)

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat corpus/SOURCES.md
python3 tools/count-resume-rows-r84.py --root .        # expect verdict met, counted 10, failed 0, rc 0
```
