source: corpus/SOURCES.md S395 (own-work, the r99 battery's assertion sites) + S392 (re-opened: CPython `int()` accepts leading zeros for an explicit base)
verified-at: 2026-11-08
recheck: 180d

# The accepted-cap families must read the fields they certify

The lane's Limine path-pin gate reports, for every explicit `--limine-version`, the version it
acted on (`limine_version`), where that value came from (`limine_version_source`: `flag` or
`probe`), and the visibility era it selected (`visibility_era`: `pre-12.9.5` or `12.9.5+`). The
battery that certifies the gate has one family per rule, and a family can answer the *pins*
correctly while never reading those three fields — which is what the r97 and r98 batteries did on
the boundary versions.

## 1. Where the gate emits the fields

Two emission sites, measured at the BYTE level on the gate's landed bytes (sha256
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`):

| site | field | byte | line |
|---|---|---|---|
| MAIN return (after parsing) | `"limine_version": limine_version` | 16931 | 316 |
| MAIN return | `"visibility_era"` | 17037 | 318 |
| CANNOT-EVALUATE early return | `"limine_version": limine_version` | 11230 | 200 |
| CANNOT-EVALUATE early return | `"visibility_era"` | 11344 | 202 |

A third `visibility_era` occurrence sits at BYTE 19205 (line 361) in the gate's own selftest
expectations, not in a return. The measured sentence is the file's own contract, not a
reconstruction: an explicit flag is echoed **verbatim** (`12.09.4` echoes `12.09.4`, never
`12.9.4`) with source `flag`, and the era follows the whole numeric tuple (`int()` of each
component, per S392).

## 2. A family that answers its pins certifies nothing about the fields

Round 97's roster added the Z-cap and leading-zero families; round 98 added `check_echo` /
`check_era` to them. The X-cap family (`REFUSAL-VERSIONS-9DIGIT`, `999999999.9.9`) and the Y-cap
family (`REFUSAL-VERSIONS-9DIGIT-Y`, `12.999999999.4` era B and `0.999999999.0` era A) still sent
their versions and read only the pin answer. Round 98's wave measured the consequence: a gate that
lies in `visibility_era` exactly for the Y-cap spellings read `met 105/105`
(`.ufo/waves/round-98/w1/ReviewBattery/g6-y-era-r98.json`). The r98 report called it the G6
survivor and amendment A4 narrowed the claim to the Z/LZ spellings rather than closing it.

The rule this gives: **a family certifies a reported field only if it reads that field on its own
cases.** Sending the spelling is not reading the answer.

## 3. The three committed one-clause bends and their readings

Each bend is the landed gate with exactly one expression changed; the battery's per-case assertion
is what turns the change into a reading. All readings are one run, canonical lane; three runs and a
`git clone --shared` layout are in the round's wave receipts.

| bend | one clause bent | r98 control battery | r99 battery |
|---|---|---|---|
| `N09-y-era` | `visibility_era` label swapped when the SECOND component is the cap `999999999` | `met 105/105` (blind) | `unmet 104/105`, failed exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` |
| `N11-x-era` | `visibility_era` label swapped when the FIRST component is `999999999` | `unmet 104/105`, failed exactly `[EXPLICIT-VERSION-ERA]` | `unmet 103/105`, failed exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` |
| (dropped) `N10-z-echo` | echoed `limine_version` falsified for the Z spellings | `unmet 104/105` | — |

Receipts: `.ufo/waves/round-99/before/dev/c1-N09-r99.json`,
`c1-N09-r98-control.json`, `c1-N11-r99.json`, `c1-N11-r98-control.json`,
`c1-N10-twin-r98-control.json`.

The X-cap row is the honest shape of a **delta** closure rather than a flip: r98 already caught
that article through one `EXPLICIT-VERSION-ERA` case (amendment A5 said so), so r99's gain is one
additional failed family, not a met-to-unmet change. The Y-cap row is a real flip: the r98 roster
was blind.

The dropped `N10-z-echo` is the twin case worth remembering: the bend changed nothing the r98
control could not already see, because r98 had set `check_echo` on the Z family. A bend the
do-nothing control already kills is a witness for the predecessor, never for this round.

## 4. What the two new selftest lie kinds certify

`tools/limine-pin-battery-r99.py` adds `limine-version` and `visibility-era` to `LIE_KINDS`
(BYTE 108455, line 2370). Each wraps the reference gate and falsifies one field of its answer;
with `--selftest --reference` the battery must read `unmet` for each. Measured directly (one run
each, `.ufo/waves/round-99/before/dev/c1-lie-*.json`):

| lie kind | reading | cap families in `failed_families` |
|---|---|---|
| `limine-version` (echo falsified) | `unmet 93/105` | X, Y, Z, LZ (plus the AUTO and EXPLICIT items) |
| `visibility-era` (label falsified) | `unmet 95/105` | X, Y, Z, LZ (plus EXPLICIT) |

This closes the r98 scoreboard's structural note that `LIE_KINDS` had twelve members and none
falsified either field: an assertion that is removed from a family is now visible to the selftest,
not only to a wave attack.

## 5. What this does not certify

- A lie kind proves the battery **sees** the field; it does not prove that every family asserts
  it. The per-family coverage is carried by the bends in §3.
- The X/Y **echo** legs have no spelling-targeted bend. `N09`/`N11` falsify `visibility_era` only;
  the echo legs are covered by the blanket `lie-limine-version` wrapper (§4) and by the
  r98-carried fixed-echo attack.
- The roster is unchanged at 105. Nothing here re-certifies the r92-r98 families, and no host
  state is read: every reading above comes from generated fixtures and the gate's bytes.
- Nothing on this host is repaired, upgraded or restarted; the lane's detection-only boundary
  stands (`PROVINCE.md`).

## Limits

The three bends target the cap spellings by construction; a field lie on a version whose components
are all short is outside them. The `visibility-era` lie kind proves only that a wrong label is
noticed somewhere in the roster, not in which family. A gate that canonicalizes the echoed spelling
still fails the LZ family by design (the r98 PC1 decision), not by a Limine rule.
