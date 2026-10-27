# R47RevGR1b receipts

## Section hash (frozen counter)
$ python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash
GR1 = fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
structural_ok = 1, problems = []

## Independent re-derivation
sha256 over LF-joined lines `## GR1`..(exclusive)`## GR2` at 77e9e2b2e96b85d8f048ae2087e246a542b71611:
fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8  (match)

## Snapshot digest verification
.ufo/waves/round-45/frozen/src: cmdline.c OK, vsprintf.c OK, kstrtox.c OK, dev-replace.c OK, systemd.kill.xml OK
.ufo/waves/round-44/frozen/src: sysfs.c OK, scrub.c OK, btrfs-scrub@.timer OK, btrfs-scrub@.service OK, PKGBUILD OK
.ufo/waves/round-45/frozen/hostcap/capture.txt: f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 (matches entry header)

## Quote line verification (grep -n, all verbatim hits)
cmdline.c:147,156,159,189,191,192; vsprintf.c:86; kstrtox.c:29,30,33; sysfs.c:2040,2043
Call chain: vsprintf.c:112-115 simple_strtoull -> simple_strntoull; fixup at vsprintf.c:86.
