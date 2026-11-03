# Round 69 — C1 registry rows S288 and S289 (scribe draft, prose only)

Timestamp: 2026-11-03T23:23:00Z (date -u +%Y-%m-%dT%H:%M:%SZ at drafting; the seat receipt carries its own line)
Lane base: acce353bacad74043636018d829e9e9b8e0fdf1c. Declaration: SCORECARD.md "Round 69 — declaration" at 920a9eea3c5c5400567be0e96141014f338973df.
Schema copied from corpus/SOURCES.md line 5 (11 columns, table delimiter NF 13 row). Snapshot bytes re-measured before drafting:
`sha256sum .ufo/waves/round-69/before/src/tk-v7211.rst .ufo/waves/round-69/before/src/vm-v7211.h` → the two declared digests, rc 0.

| S288 | Linux v7.2.11 Documentation/admin-guide/tainted-kernels.rst — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11 | docs | A | The closed taint bit-to-log table for bits 0-19 and the runtime /proc/sys/kernel/tainted query, at the host kernel release tag v7.2.11 in the stable tree | tag v7.2.11, Documentation/admin-guide/tainted-kernels.rst lines 72-73 (bitfield sentence), 83-105 (table header, rows for bits 0-19 and the closing rule) and 50-52 (runtime query); raw bytes sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841; bytes byte-identical to S140's torvalds v7.2 snapshot (L1 cmp rc 0 against .ufo/waves/round-27/sources/S140.rst), so this row is the host release-tag re-pin; snapshot .ufo/waves/round-69/before/src/tk-v7211.rst (191 lines) | supersedes S140 — re-pin: the running kernel's own tag v7.2.11; bytes byte-identical to S140's torvalds v7.2 snapshot (sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 for both; L1 cmp rc 0 against .ufo/waves/round-27/sources/S140.rst), so no new document content is claimed; the document decodes taint per bit 0-19 through its log-letter table and the runtime /proc/sys/kernel/tainted query; the re-pin exists so the entry's applicability claim cites the tag the host runs, and S140 stays current for the torvalds v7.2 tag: "number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint." (lines 72-73, 20 words) | mined | 2026-11-03 | on-release | corpus/knowledge/kernel-taint-plane-r69.md |
| S289 | Linux v7.2.11 include/linux/vermagic.h — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11 | code | A | The module vermagic token set a built kernel stamps on modules — UTS_RELEASE plus the SMP, preempt, mod_unload, modversions, arch and randstruct tokens — at the host kernel release tag v7.2.11 | tag v7.2.11, include/linux/vermagic.h line 12 (sanity-stamp comment) with lines 9, 14, 21, 26 and 31 (utsrelease include and the SMP, preempt, mod_unload and modversions macros) and 41-46 (VERMAGIC_STRING composition); raw bytes sha256 0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea; snapshot .ufo/waves/round-69/before/src/vm-v7211.h (48 lines) | Vermagic is the built release string followed by a fixed option-token set, so a module whose vermagic carries SMP preempt mod_unload was built for a kernel with those options: "/* Simply sanity version stamp for modules. */" (line 12, 8 words by wc -w, the two comment delimiters included) | mined | 2026-11-03 | on-release | corpus/knowledge/kernel-taint-plane-r69.md |

## Measured cell and quote counts

Cell count (each row must read NF 13 under the pipe separator, i.e. 11 cells plus the two edge fields):

    $ awk -F'|' '/^\| S28[89] /{print $2": NF="NF" cells="NF-2}' .ufo/waves/round-69/drafts/c1/sources-rows.md
     S288 : NF=13 cells=11
     S289 : NF=13 cells=11
    (rc 0; re-runs 2026-11-03T23:22:14Z after the anchor line-range fixes and 2026-11-03T23:26:00Z after the L1 re-pin
    correction, same output both times)

Quote location and word counts:

    $ grep -n 'bitfield' .ufo/waves/round-69/before/src/tk-v7211.rst
    72:number, as it is a bitfield, where each bit indicates the absence or presence of
    $ sed -n '72,73p' .ufo/waves/round-69/before/src/tk-v7211.rst | tr '\n' ' ' | grep -cF 'number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint.'
    1
    $ printf '%s\n' 'number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint.' | wc -w
    20

    $ grep -n 'Simply sanity' .ufo/waves/round-69/before/src/vm-v7211.h
    12:/* Simply sanity version stamp for modules. */
    $ grep -cF '/* Simply sanity version stamp for modules. */' .ufo/waves/round-69/before/src/vm-v7211.h
    1
    $ printf '%s\n' '/* Simply sanity version stamp for modules. */' | wc -w
    8

Notes for the integrator, no verdict claimed here:
- S288 is worded as a re-pin under the L1 correction of 2026-11-03 and the registry convention of S280/S281: its teaches cell begins `supersedes S140 — re-pin:` and states that the bytes are byte-identical to S140's torvalds v7.2 snapshot, so no new document content is claimed. The word "supersedes" is the registry's re-pin verb here; S140 itself stays current for the torvalds v7.2 tag, as the cell says.
- The `cmp` rc 0 against `.ufo/waves/round-27/sources/S140.rst` is L1-reported in the row, not run by this scribe; this seat verified only the v7.2.11 snapshot digests against `before/src/SHA256SUMS` and read S140's recorded digest from `corpus/SOURCES.md:146`.
- The S288 quote spans two source lines (72-73); it is one sentence and is verbatim after whitespace normalisation. The single-line fragment search returns 0, as expected (grep -cF → 0), so the row cites the line pair, not a one-line match.
- The S289 quote is the file's own purpose comment; the load-bearing token composition sits at lines 41-46 and is named in the anchor cell rather than quoted, because those lines carry macro line continuations and double quotes that would break a pipe-row quote envelope. A critic should read that as a stated anchor, not as quoted evidence.
- Neither row contains a literal or escaped pipe inside a cell; the only pipes are the 12 cell separators.
