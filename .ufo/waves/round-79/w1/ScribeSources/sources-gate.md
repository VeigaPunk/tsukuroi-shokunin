# `## Gate` block draft — round 79 (wave w1)

Lane lesson format follows the round-77/78 Gate tables. This is a draft for the
round lesson; the L1 assembles the final `corpus/lessons/round-79.md`.

Sources opened 2026-11-04 before the freeze commit `afe1f26128bde87484001cd02ebf11fa524c4059`;
the page is pinned byte-exact at `.ufo/waves/round-79/before/src/systemd.unit.xml`,
SHA-256 `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6` (measured,
equal to the digest frozen in `before/expected.json`, whose own SHA-256
`0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21` also matches).
Line numbers below are upstream **v262 tag** lines in that snapshot — upstream manual
lines, not installed Arch build lines. Quotes are tag-stripped token spans (inline
`<varname>` markup removed), the same normalization the C1 instrument applies.

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S329 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml ; 2026-11-04, :659: `Configures (weak) requirement dependencies on other units.` | admit, tier A/docs/mined for the dependency-propagation and ordering keyword scope only: Wants= :657-679, Requires= :682-708, Requisite= :711-728, BindsTo= :731-758, PartOf= :761-778, Upholds= :781-797, Before=/After= :826-866, RequiresMountsFor= :934-947; eight finite DP rows over documented semantics, not a live-host reading and not an installed-build equivalence claim |
| `After=` pulls the unit in | same page, :855-857: `Note that those settings are independent of and orthogonal to the requirement dependencies as configured by Requires=, Wants=, Requisite=, or BindsTo=.` | reject: ordering and requirement dependencies are orthogonal — an `After=` line alone never creates a requirement dependency and never pulls a unit into the transaction. Flip: a located upstream passage stating that `After=` itself creates or implies a requirement/pull-in dependency |
| `Requires=` guarantees the listed unit stays active | same page, :698-699: `Note that this dependency type does not imply that the other unit always has to be in active state when this unit is running.` | reject: `Requires=` explicitly does not imply the other unit must remain active; the page directs `BindsTo=` with `After=` for that guarantee. Flip: a located upstream passage stating that `Requires=` guarantees continued active state of the listed unit |
| `Upholds=` is a one-time pull-in | same page, :785-787: `While a Wants= dependency on another unit has a one-time effect when this units started, a Upholds= dependency on it has a continuous effect,` | reject: the page contrasts `Wants=` (one-time effect) with `Upholds=` (continuous effect, constantly restarting the unit). Flip: a located upstream passage stating that `Upholds=` has only a one-time pull-in effect |

## Notes the L1 must carry

- **S329 is a new row; no existing row's status, recheck or used-by changes.** The
  registry holds 328 rows ending at `S328`, so `S329` is the next unused id in the
  current registry (`grep -oE '^\| *S[0-9]{3,}' corpus/SOURCES.md | sort -u` ends at
  `S328`). Caveat, recorded and not smoothed: the quarantined staged package
  `shokuknow/merge/tsukuroi/SOURCES.append.md` already uses `S329` for a different
  document (`lanes/tsukuroi/round14/captures/mirror-language-list-capture.txt`,
  own-work mirror/locale capture). That package is not adopted; `S329` here is the
  id the round-79 declaration and the frozen C1 instrument require. The bare id is
  therefore ambiguous across the two documents — namespace/document context, not
  arithmetic renumbering, is the safe resolution, and the L1 should say so in the
  lesson.
- **`W04` expected, `E04` not.** The URL is already used by **S304**
  (systemd.unit.xml, unit-load merge plane). The scopes differ, so the census reads
  the `W04` "duplicate url across scopes" warning, not `E04` (duplicate url within one
  scope). `W04` does not change the validate exit code. The round-79 census start
  already records "W04 duplicate-URL warnings only".
- **`E11` ordering.** `S329` is `mined`, so the census checks that each used-by path
  exists on disk. `corpus/knowledge/systemd-dependency-propagation-r79.md` is produced
  by the ScribeNote seat; the row and the note must land in the same integration step.
- **Scope of the rejection rows.** Each rejection is a claim about *document
  semantics*, refuted by the page's own wording. None of them is an accusation about
  a seat, and none is declared false about any host state: the manual does not
  observe this host.
