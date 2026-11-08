# Review — `corpus/knowledge/limine-metadata-assertions-r98.md` (round 98, seat ScribeKnowledge)

Reviewed draft: the working-tree copy of `corpus/knowledge/limine-metadata-assertions-r98.md`
(uncommitted at review time; the L1 owns the landing copy). The committed copy at
`1cfeb5d5089097fdffef761ad0e2b8dfa75a2793` differs (it cites S393 and the early-return byte pair);
where the two differ, both are reported.

Every number below carries the command that produced it. `RUN` = I executed it in this seat;
`READ` = I read a committed receipt and did not re-run it.

Receipts (all under `.ufo/waves/round-98/w1/ScribeKnowledge/receipts/`):
`c1-gate-runs3.json`, `c1-bend-N07-runs3.json`, `c1-bend-N08-runs3.json`,
`c1-dn-gate-runs3.json`, `c1-dn-N07-runs3.json`, `c1-dn-N08-runs3.json`,
`count-r98-battery.txt`, `count-r97-donothing.txt`,
`mutant-zlz-source-probe-runs3.json`, `mutant-zlz-source-probe-r97-dn-runs3.json`,
`count-mutant-zlz-source-probe.txt`, `count-mutant-zlz-source-probe-r97-dn.txt`,
`mutant-gate-zlz-source-probe.py`, `mutant-gate-zlz-source-probe.diff.txt`,
`gate-era-capture.txt`, `gate-source-capture.txt`, `byte-offsets.txt`,
`ast-family-flags.txt`, `recheck-verbatim.txt`.

Instrument integrity, before any measurement was cited:

```
$ sha256sum -c .ufo/waves/round-98/before/instruments.sha256
… 29 lines, every one OK, no FAILED
```

(`tools/check-limine-pins.py` OK = 7d79ac29…, `tools/limine-pin-battery-r98.py` OK = 8198bd84…,
`tools/make-r98-bends.py` OK, `tools/check-registry-content-r98.py` OK,
`tools/check-registry-coverage.py` OK, `tools/check-r96-calibration.py` OK; both bends OK; both
do-nothing controls OK; all six `before/dev/` receipts OK.)

---

## 1. Per-claim verification

### C1-1 — roster is 105 and unchanged

| | command | observed | matches the sentence |
|---|---|---|---|
| roster length, landed battery | `python3 -c "ast.parse(open('tools/limine-pin-battery-r98.py','rb').read())"`, `FAMILY_ROSTER` literal (`ast-family-flags.txt`) | `r98-landed FAMILY_ROSTER len = 105` | yes |
| roster length, r97 control | same AST over `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py` | `r97-do-nothing-control FAMILY_ROSTER len = 105` | yes |
| family members unchanged | same AST, `Z_DIGIT9` / `LEADING_ZERO_VALUES` / `Y_DIGIT9` / `CASES_PER_FAMILY` | r97 and r98 print identical tuples (`('12.9.999999999','0.9.999999999')`, `('12.09.4','000000012.9.4','12.000000009.000000005','000000000.000000000.000000000')`, `4`) | yes |

### C1-2 — landed gate reads `met 105/105`, 0 error rows, 3 runs — RUN

```
$ python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 \
      --work $S/w-gate --json receipts/c1-gate-runs3.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/c1-gate-runs3.json \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

observed, ×3 identical runs (`count-r98-battery.txt`): `verdict met`, `families_passed 105`,
`families_total 105`, `failed_families []`, `cases 420`, `error_rows 0`,
`REFUSAL-VERSIONS-9DIGIT-Z [4,0]`, `LEADING-ZERO-NORMALIZE [4,0]`; exit 0.

### C1-3 — N07 reads `103/105`, exactly two families, 0 error rows — RUN

```
$ python3 tools/limine-pin-battery-r98.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py \
      --runs 3 --work $S/w-n07 --json receipts/c1-bend-N07-runs3.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/c1-bend-N07-runs3.json \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

observed, ×3 identical runs (`count-r98-battery.txt`): `verdict unmet`, `families_passed 103`,
`failed_families ["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, `cases 420`,
`error_rows 0`; both named families `[0,4]` (4 failed cases each); exit 1.

### C1-4 — N08 reads `104/105`, exactly one family, 0 error rows — RUN

same two commands with `--gate …/N08-echo-norm.py --json receipts/c1-bend-N08-runs3.json`

observed, ×3 identical runs: `verdict unmet`, `families_passed 104`,
`failed_families ["LEADING-ZERO-NORMALIZE"]`, `cases 420`, `error_rows 0`;
`REFUSAL-VERSIONS-9DIGIT-Z [4,0]`, `LEADING-ZERO-NORMALIZE [0,4]`; exit 1.

### C1-5 — the r97 battery is blind to both bends — RUN

```
$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <gate> --runs 3 \
      --work $S/w-dn-* --json receipts/c1-dn-{gate,N07,N08}-runs3.json
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/c1-dn-*-runs3.json \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

observed (`count-r97-donothing.txt`), ×3 identical runs on each of the three gates:
`verdict met`, `105/105`, `failed_families []`, `error_rows 0`, both named families `[4,0]`.

The r97 control is the r97 landed battery, byte for byte:

```
$ git show 9c4b7b164f926ee2cb1f8683b4fe8f3f5796b1a9:tools/limine-pin-battery-r97.py | sha256sum
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  -
$ sha256sum .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  …
```

### C1-6 — the two families gained the two assertions; the r97 battery had neither — RUN (static)

`ast-family-flags.txt`, AST over the two batteries' `fam_*` function bodies:

```
r98-landed:  fam_refusal_versions_9digit []          fam_refusal_versions_9digit_y []
             fam_refusal_versions_9digit_z ['check_echo','check_era']
             fam_leading_zero_normalize  ['check_echo','check_era']
             fam_explicit_version_echo ['check_echo']   fam_explicit_version_era ['check_era']
r97-control: fam_refusal_versions_9digit_z []        fam_leading_zero_normalize []
```

The entry's Limits bullet ("the X and Y boundary families still do not set `check_echo` or
`check_era`") is confirmed by the same AST output.

### C1-7 — the r97 wave's two attack gates read `met 105/105` — READ

```
$ python3 -c "json.load(open('.ufo/waves/round-97/w1/ReviewBattery/attack-1-field.json'))"
$ python3 -c "json.load(open('.ufo/waves/round-97/w1/ReviewBattery/attack-2.json'))"
```

observed: `attack-1-field.json` = 3 runs, each `verdict met`, `families_passed 105`,
`failed_families []`, `cases 420`; `attack-2.json` = 3 runs, each `met 105/105`, `failed_families []`;
`grep -o '"error": [^,]*' attack-1-field.json | sort | uniq -c` → `1260 "error": null` (0 non-null
error rows). The r97 attack gates themselves lived in r97's scratch (`/fast/scratch/hyaku/tsukuroi-r97/…`,
gone) and are not re-derivable from this lane; the receipts are the evidence.

### C1-8 — the draft's `recheck:` procedure, run verbatim — RUN

```
$ env -u TMPDIR python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --json OUT
families_passed 105/105 verdict met failed -      (×3)
rc=0
$ python3 .ufo/waves/round-95/before/controls/count-runs.py OUT \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
… "verdict": "met", "families_passed": 105, "failed_families": [], "error_rows": 0,
  REFUSAL-VERSIONS-9DIGIT-Z [4,0], LEADING-ZERO-NORMALIZE [4,0]
rc=0
```

(`receipts/recheck-verbatim.txt`.) The entry's recheck line names both commands and both expected
values; both hold.

---

## 2. PC1 / PC2 — the echo and the era label, checked at the byte level

```
$ grep -abo '"limine_version": limine_version' tools/check-limine-pins.py
11230:"limine_version": limine_version
16931:"limine_version": limine_version
$ grep -abo '"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"' tools/check-limine-pins.py
11344:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
17037:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
$ grep -abo 'VISIBILITY_ERA_SPLIT = (12, 9, 5)' tools/check-limine-pins.py
7399:VISIBILITY_ERA_SPLIT = (12, 9, 5)
$ grep -abo 'era_b = version >= VISIBILITY_ERA_SPLIT' tools/check-limine-pins.py
10910:era_b = version >= VISIBILITY_ERA_SPLIT
```

offsets → lines (`byte-offsets.txt`): 11230→line 200, 11344→line 202 (the CANNOT-EVALUATE early
return); 16931→line 316, 17037→line 318 (the MAIN return a readable-config run takes).

The working-tree draft's corrected wording — "the main return's emitter at BYTE 16931", "main-return
emitter at BYTE 17037, early-return copy at BYTE 11344" — matches the measurement exactly. The
committed draft cites only 11230 / 11344 and labels them the emission lines; the lane's own
`corpus/lessons/round-98.md` (R98-ANCHOR-FIRST-SITE) and the working-tree S394 row record the same
correction. The working-tree draft is the one that matches the bytes; the committed one does not.

### The era readings, run on the pinned gate — RUN

```
$ python3 tools/check-limine-pins.py --conf $S/esp/limine.conf --esp $S/esp --limine-version <V>
```

(`receipts/gate-era-capture.txt`)

| flag | echo | `limine_version_source` | `visibility_era` | draft's PC2 sentence | match |
|---|---|---|---|---|---|
| `12.09.4` | `12.09.4` | `flag` | `pre-12.9.5` | era A | yes |
| `000000012.9.4` | `000000012.9.4` | `flag` | `pre-12.9.5` | era A | yes |
| `12.000000009.000000005` | verbatim | `flag` | `12.9.5+` | era B | yes |
| `000000000.000000000.000000000` | verbatim | `flag` | `pre-12.9.5` | era A | yes |
| `12.9.999999999` | verbatim | `flag` | `12.9.5+` | era B | yes |
| `0.9.999999999` | verbatim | `flag` | `pre-12.9.5` | (not listed) | — |
| `12.9.5` | `12.9.5` | `flag` | `12.9.5+` | (split boundary) | yes |
| `12.9.4` | `12.9.4` | `flag` | `pre-12.9.5` | (split boundary) | yes |

### The two sources — RUN

`receipts/gate-source-capture.txt`: an explicit `--limine-version 12.09.4` →
`{"limine_version": "12.09.4", "limine_version_source": "flag", "visibility_era": "pre-12.9.5"}`;
`--limine-version auto` with a scratch fake `limine` printing `Limine 12.9.6` on `PATH` →
`{"limine_version": "12.9.6", "limine_version_source": "probe", "visibility_era": "12.9.5+"}`.
The draft's PC1 sentence about the two sources is confirmed.

---

## 3. Over-wide sentences, each with its narrowing

**(O1) PC1's receipt pointer does not carry the era readings.**
Draft: "`--limine-version 12.09.4` reports `"limine_version": "12.09.4"` and `"visibility_era":
"pre-12.9.5"`, while `--limine-version 12.9.999999999` reports … `"visibility_era": "12.9.5+"`
(`before/dev/` receipts of this round's gate capture)."

The `before/dev/` receipts carry the echo and the source but **not** the era label:

```
$ grep -c 'visibility_era' .ufo/waves/round-98/before/dev/c1-*.json        # all 0
$ grep -c '12\.09\.4'       .ufo/waves/round-98/before/dev/c1-gate-runs3.json   # 3
$ grep -c 'pre-12.9.5\|12.9.5+' .ufo/waves/round-98/before/dev/c1-*.json   # all 0
```

Cause, in the battery's own code: the case log records `got[8]` (echo) and `got[9]` (source) and
**drops `got[10]`** (`visibility_era`) — `tools/limine-pin-battery-r98.py` line 2278-2279 appends
`[got[0], got[1], pins, got[3], got[6], got[8], got[9]]`. So the era label is asserted by
`meta_ok` but never printed into the receipt.
**Narrowing:** cite a direct gate run for the era pair (the draft's own PC1 already needs one for
the era), e.g. `python3 tools/check-limine-pins.py --conf <conf> --esp <esp> --limine-version
12.09.4` — the command and output are in `receipts/gate-era-capture.txt` — and keep
`before/dev/` for the echo + source pair only, which it does carry.

**(O2) PC2's pin-consequence sentence covers a fixture class the battery does not exercise.**
Draft: "The pin consequence on a first-line-entry fixture follows the same split (`prompt` for era
A, `panic` for era B)."
The era families use `hash_mismatch_panic: no`; the consequence is `prompt` only when that key is
visible and reads `no`, and the era moves that visibility only in the first-line case. With any
other panic-setting value (e.g. `yes`) the consequence is `panic` in **both** eras, so the sentence
as written is wider than the fixture the battery builds.
**Narrowing:** "On the first-line-entry fixture the Z/LZ families build (`hash_mismatch_panic: no`
after the body), the mismatch pin's consequence follows the era split — `prompt` for era A,
`panic` for era B." The battery's own expectation confirms the split (`want` in the dev receipt:
`12.09.4` → `LP-MISMATCH prompt`, `12.000000009.000000005` → `LP-MISMATCH panic`, `12.9.999999999`
→ `panic`, `0.9.999999999` → `prompt`).

**(O3) PC2's member enumeration is one member short of the families the battery sends.**
The five spellings listed are correct, but the Z family also sends `0.9.999999999` (era A), so the
list reads as complete when it is not.
**Narrowing:** add "`0.9.999999999` is era A", or open the list with "e.g.".

**(O4) PC3's "the same two lies" names the r97 attack gates and the r98 bends as one thing.**
They are different mutants: the r97 attacks (`attack1-eraA-field`, `attack2-echo-norm`) were
scratch gates derived in r97 and are gone; N07/N08 are the r98 re-derivations committed under
`.ufo/waves/round-98/before/controls/bends/`. N07 is also broader than the r97 attack-1: it lies
about the era label for **every** Z/LZ spelling, not for the Z tuple alone.
**Narrowing:** "the same two *classes* of lie, re-derived as the r98 bends: N07 (era-label lie on
the Z/LZ spellings) now reads `103/105` with two families failed, N08 (echo normalized) reads
`104/105` with one; …". Note the sentence's parenthetical "(ReviewBattery `attack-1-field.json`,
`attack-2.json`; amendments A7)" is correct for the `met 105/105` clause — those receipts exist and
read `met 105/105` (C1-7 above).

**(O5) The Limits bullet describes N07's trigger more loosely than the bend's clause.**
Draft: "`N07`'s lie is targeted at the Z/LZ spellings by construction (a 9-digit third component or
a leading-zero component)".
The bend's condition (from the frozen diff, `mutant`/`bends` file, `diff -u tools/check-limine-pins.py
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py`) is
`len(limine_version.split(".")[2]) == 9 or any(len(p) > 1 and p.startswith("0") for p in
limine_version.split("."))` — the second clause fires only on a leading-zero component **of more
than one digit**; a component written as a bare `0` does not trigger it (e.g. `0.9.4` gets no lie).
**Narrowing:** "(a 9-digit third component or a leading-zero component of more than one digit)".
This is what makes N07 fail exactly the Z and LZ families and nothing else (C1-3).

**(O6) No unsupported universal.** Swept for "every spelling", "all families", "always", "never",
"both", "any":

- PC1 "Both spellings are observable" — the two version spellings, both named in the same sentence
  and both run above. Bounded.
- PC3 "answers every pin correctly" — describes the r97 attack gates, whose receipts read
  `met 105/105` with 0 non-null error rows (C1-7). Bounded by that receipt.
- PC3 "a family's expectation must cover every field its claim names" — a normative statement
  about how to write a claim, not a statement about an instrument. Not an instrument claim.
- Limits "The X and Y boundary families … still do not set `check_echo` or `check_era`" — confirmed
  by the AST (C1-6); a negative claim, bounded to two named families.
- Limits "a field lie on any other spelling is outside that bend's clause" — the complement of O5's
  clause; correct once O5's narrowing is applied.

No sentence in the draft asserts a universal the instruments do not enforce.

---

## 4. Provenance trio

The three keys are present, at column 0, outside any fence, in the required relative order
`source:` → `verified-at:` → `recheck:`. In the **working-tree** draft they are at lines 3, 11, 13
(`own-work:` occupies 8-10); in the **committed** copy at `1cfeb5d5` they are at lines 3, 10, 12
(`own-work:` at 7-9). The gate run below reads the committed revision and reports exactly its
line numbers:

```
$ python3 tools/check-knowledge-header.py --revision 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793 \
      --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
{"…": "clean_count": 114, "complete_count": 114, "finding_count": 0, "findings": [],
 "notes": [… {"lines": {"recheck": 12, "source": 3, "verified-at": 10},
              "path": "corpus/knowledge/limine-metadata-assertions-r98.md", "problems": []} …]}
```

The working-tree copy's header was not re-gated here (the gate binds an immutable revision); its
three keys are at column 0 outside fences by inspection (`cat -n` of the working-tree file), and
the L1's landing commit should re-run the gate at that revision.

```
$ python3 tools/check-recheck-commands.py --revision 1cfeb5d5089097fdffef761ad0e2b8dfa75a2793 \
      --paths corpus/knowledge/limine-metadata-assertions-r98.md --branch master
{"status": "PASS", "findings": [], "forbidden": ["pacman","checkupdates","yay","paru","mkinitcpio",
 "limine-update"], "invocation_count": 0, "resolved_count": 0, "flagged_count": 0}
```

Both gates read the **committed** copy. Two caveats, neither a defect:

1. The trio is not literally the first three keys: `own-work:` sits between `source:` and
   `verified-at:` (draft lines 8-10). This is the lane's own shape for these entries — the sibling
   entries `corpus/knowledge/limine-bound-9digit-z-r97.md` and `corpus/knowledge/limine-bound-per-component-r96.md`
   have the identical order (`source:`, `own-work:`, `verified-at:`, `recheck:`) — and both gates are
   order-insensitive (`check-knowledge-header.py` takes each key's **last** occurrence and reports
   `finding_count 0`). No repair needed; flagging so the L1 does not "fix" it and diverge from the
   two siblings.
2. `source:` cites **S393 and S392** in the committed copy, as the round's task expects. The
   working-tree draft cites **S394 and S392** instead, because the same working tree's
   `corpus/SOURCES.md` moves S393 to `queued` with `used-by —` and adds S394 (`mined`,
   `used-by corpus/knowledge/limine-metadata-assertions-r98.md, corpus/lessons/round-98.md`) as
   S393's superseding row, carrying the corrected both-sites byte pair. The census agrees with the
   working tree:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md   (exit 0)
```

Neither S393 nor S394 is flagged. **Conclusion:** the trio is confirmed in both copies; the source
row differs by exactly the supersession the lane already decided, and the landing copy must match
the `SOURCES.md` that lands with it (S394 if S393 is superseded in the same commit, S393 if not).
Landing the entry with `S393` while `SOURCES.md` says S393 is `queued` would leave a dangling
citation — the L1 should land the two in the same commit.

---

## 5. Missing proposition the receipts support — the `flag` vs `probe` source distinction

The entry's PC1 title and first clause say the echo "names its source", but nothing in the entry
says what the **battery** does about the source token, and the `before/dev/` receipts cannot show
it (`visibility_era` is dropped from the case log; the source *is* logged as `got[9]`). The
battery's `meta_ok` asserts the source token literally:

```python
if c.check_echo and not (got[8] == c.version and got[9] == "flag"):
    return False
```

So a gate that echoes the flag spelling **verbatim** but labels the source `"probe"` for the
Z/LZ spellings is caught by the r98 battery and is invisible to the r97 battery. Measured, with a
one-clause mutant of the pinned gate (my own scratch derivation — I did **not** run
`tools/make-r98-bends.py`; the substitution is re-derived here and diffed against the pinned bytes):

```
$ diff -u tools/check-limine-pins.py receipts/mutant-gate-zlz-source-probe.py
-            "limine_version_source": limine_version_source,
+            "limine_version_source": ("probe" if (len(limine_version.split(".")[2]) == 9 or any(len(p) > 1 and p.startswith("0") for p in limine_version.split("."))) else limine_version_source),
```

(`receipts/mutant-gate-zlz-source-probe.diff.txt`; the mutant's sha256
`e076a2f7…`, the pinned gate's `7d79ac29…`.)

```
$ python3 tools/limine-pin-battery-r98.py --gate receipts/mutant-gate-zlz-source-probe.py --runs 3 …
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/mutant-zlz-source-probe-runs3.json \
      --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

observed ×3 (`count-mutant-zlz-source-probe.txt`): `verdict unmet`, `families_passed 103`,
`failed_families ["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, `error_rows 0`, both
named families `[0,4]`.

```
$ python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py \
      --gate receipts/mutant-gate-zlz-source-probe.py --runs 3 …
$ python3 .ufo/waves/round-95/before/controls/count-runs.py receipts/mutant-zlz-source-probe-r97-dn-runs3.json …
```

observed ×3 (`count-mutant-zlz-source-probe-r97-dn.txt`): `verdict met`, `105/105`,
`failed_families []`, `error_rows 0` — the r97 battery is blind to the mislabelled source.

**Proposed added section (draft text for the L1 to place after PC1):**

```markdown
## PC4 — the echo is asserted together with its source token

`meta_ok` does not compare the echoed string alone: it requires the echoed value to equal the
flag spelling **and** `limine_version_source` to equal `flag`. A gate that echoes `12.09.4`
verbatim but labels the source `probe` for the Z/LZ spellings is therefore caught by the r98
battery and is invisible to the r97 battery.

Measured (one-clause mutant of the pinned gate: the source field is replaced by `probe` exactly
when the spelling has a 9-digit third component or a leading-zero component of more than one
digit; `diff -u tools/check-limine-pins.py <mutant>` in the seat receipt):

    python3 tools/limine-pin-battery-r98.py --gate <mutant> --runs 3 --json OUT
    → unmet 103/105, failed_families [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z], 0 error rows
    python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate <mutant> --runs 3 --json OUT
    → met 105/105, failed_families [], 0 error rows

The source token is a third asserted field, distinct from the echo and from the era label; the
r97 battery asserted none of the three for these two families.
```

---

## 6. Corrected draft of the sentences that need it

Only the sentences above are replaced; everything else in the L1's draft stands as written.

**PC1, era-reading clause** (replaces the `(before/dev/ receipts …)` parenthetical):

> Both spellings are observable: `--limine-version 12.09.4` reports `"limine_version": "12.09.4"`
> and `"visibility_era": "pre-12.9.5"`, while `--limine-version 12.9.999999999` reports
> `"limine_version": "12.9.999999999"` and `"visibility_era": "12.9.5+"` — read from the gate's
> own JSON (`python3 tools/check-limine-pins.py --conf <conf> --esp <esp> --limine-version
> 12.09.4`); the `before/dev/` battery receipts carry the echoed spelling and the source token
> but not the era label, which the battery's case log does not record.

**PC2, pin-consequence sentence** (replaces "The pin consequence on a first-line-entry fixture
follows the same split (`prompt` for era A, `panic` for era B)."):

> On the first-line-entry fixture the Z/LZ families build (`hash_mismatch_panic: no` after the
> body), the mismatch pin's consequence follows the same split — `prompt` for era A, `panic` for
> era B.

**PC2, member enumeration** (replaces "the label follows the whole numeric tuple: `12.09.4` and
`000000012.9.4` are era A, `12.000000009.000000005` and `12.9.999999999` era B, and
`000000000.000000000.000000000` era A."):

> Because the parser converts each component with `int()` (S392: leading zeros are a legal spelling
> for an explicit base, and base 0's refusal does not apply), the label follows the whole numeric
> tuple: `12.09.4`, `000000012.9.4` and `0.9.999999999` are era A, `12.000000009.000000005` and
> `12.9.999999999` era B, and `000000000.000000000.000000000` era A.

**PC3, bend clause** (replaces "r98 sets the battery's `check_echo`/`check_era` flags on those two
families, and the same two lies now read `103/105` (`N07-era-field-lie`, two families) and
`104/105` (`N08-echo-norm`, one family) while the r97 battery remains blind at `105/105` on both
bends."):

> r98 sets the battery's `check_echo`/`check_era` flags on those two families. The same two
> *classes* of lie, re-derived as this round's bends, now read `103/105` (`N07-era-field-lie`: the
> era label lied for the Z/LZ spellings, two families) and `104/105` (`N08-echo-norm`: the echo
> normalized, one family), while the r97 battery remains blind at `105/105` on both bends.

**Limits, N07 clause** (replaces "`N07`'s lie is targeted at the Z/LZ spellings by construction (a
9-digit third component or a leading-zero component); a field lie on any other spelling is outside
that bend's clause."):

> `N07`'s lie is targeted at the Z/LZ spellings by construction (a 9-digit third component or a
> leading-zero component of more than one digit — the bend's own condition, `len(p) > 1 and
> p.startswith("0")`); a field lie on any other spelling is outside that bend's clause.

**New section** — PC4 as drafted in §5 above.

---

## 7. Verdict

Every number in the draft that names a receipt is confirmed by a run in this seat (landed gate
`met 105/105` ×3, N07 `103/105` ×3, N08 `104/105` ×3, r97 control `met 105/105` ×3 on all three
gates, 0 error rows throughout, roster 105 unchanged) or by a committed receipt read here (the r97
attack gates' `met 105/105` ×3). The byte offsets the working-tree draft cites are exactly the
measured offsets, and the corrected main-return/early-return distinction is confirmed. Six
sentences need narrowing (O1-O5, plus the added PC4), of which one (O1) is a mis-citation that the
lane's own receipts contradict; the trio is confirmed in both the committed and working-tree copies.
