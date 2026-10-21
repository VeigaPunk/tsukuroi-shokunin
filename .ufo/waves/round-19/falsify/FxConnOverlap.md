## Attack

C1 adjacency — ownership-overlap scan of OUT-001..OUT-010. Axes: adjacency integrity and ownership-boundary clarity. A proposition is `OVERLAP` if it duplicates a Tsukuroi-claimed surface, repeats a competing sibling scope, or chooses an owner where Tsukuroi records the ownership as unresolved. I compared the propositions at `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:119-132` with the exact pinned sibling snapshots named there and Tsukuroi's own boundary text.

## Method

Read-only inspection of the target revision's `PROVINCE.md`, the ten sibling `PROVINCE.md` snapshots in `.ufo/waves/round-19/l1-capture/siblings/`, `corpus/knowledge/adjacency-anchors-r19.md`, and the cited portions of `tools/tsukuroi-census.sh`. The outbound census supplies the snapshot paths, pinned commits and blob digests. A quote check returned one matching source line for each anchor (OUT-001 9; OUT-002 12; OUT-003 3; OUT-004 6; OUT-005 8; OUT-006 3; OUT-007 12; OUT-008 3; OUT-009 3; OUT-010 7); the source-file hashes matched the census digests. I compared kaidoku's pinned snapshot with the additional captured snapshot: the latter adds lines after the pinned file and does not change OUT-008's cited scope.

Commands run for the comparison:

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture
find siblings -type f -exec sha256sum {} + | sort -k2
```

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings
# Read-only Python substring check: checked the literal quoted fragments for OUT-001..OUT-010 against their respective pinned PROVINCE.md snapshots; each had exactly the source line reported above.
diff <(cat kaidoku/d1d981d2cc04/PROVINCE.md) <(cat kaidoku/8451e4710954/PROVINCE.md)
```

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
 grep -n -i -E 'oom|memory\.events|memory\.pressure|psi|MESSAGE_ID|coredump|fe6faa94|kill' tools/tsukuroi-census.sh
 grep -n -i -E 'credential|op\.env|janitor|1password|secret|config/the' tools/tsukuroi-census.sh
 grep -n -E 'pkg\.tar\.zst|Qkk' tools/tsukuroi-census.sh
 grep -n -i -E 'systemctl --user|hypridle|hyprland|idle' tools/tsukuroi-census.sh
```

The target revision's contents were also read with `git show` (through a read-only `python3 -c` line-selection command). No gate, self-test, service, package, boot, or mutation action was run. The broad host path-name search is disclosed under Residual.

## Verdict

**CONFIRM — C1 adjacency, semantic-overlap attack.** Four anchors need a scope qualification or boundary read: OUT-001 and OUT-005 share kill/memory evidence and triage surfaces; OUT-003 shares credential-helper metadata/hygiene evidence; OUT-008 and OUT-009 repeat the same unresolved shipped-artifact RE scope, and OUT-009 goes further by stating a selected owner. These are evidence-surface overlaps, not permission to repair or access credential contents. The clearest contradiction is OUT-009 against the explicit no-owner-selection statement.

| Anchor | Result | Competing text and finding |
|---|---|---|
| OUT-001 | **OVERLAP — shared evidence surface, purpose split** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:121`. Tsukuroi says host-memory and kill-event measurements support OS triage and its census reports them, while fleet correlation belongs to mori (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:30-33`); its Core also owns journal/boot triage (`...:8-14`) and ADJ-04 retains OS memory/journal/boot diagnosis (`...:49`). Mori's pinned declaration owns kill/OOM journal records and cgroup `memory.events`, but explicitly says it reads those as fleet evidence and never owns OS state (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:8-16`). Thus the signal is shared while the stated purposes split; the broad phrase “Mori owns ... evidence” risks claiming the whole evidence surface rather than the fleet-use boundary. |
| OUT-002 | **OK** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:122`. Kama's quote is its served-model-ID reconciliation row (`.../siblings/kama/e75cf680b534/PROVINCE.md:12`); Tsukuroi refuses endpoint/model-serving health to kama (`...:25-27`) and ADJ-01 expressly retains kernel/driver/device/unit state while routing endpoint diagnosis to kama (`...:46`). No scope collision in the proposition. |
| OUT-003 | **OVERLAP — shared credential-helper metadata, question split** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:123`. Kagi claims credential-hygiene evidence (`.../siblings/kagi/c2cab35bc92e/PROVINCE.md:3-6`); Tsukuroi retains permission/ownership findings plus package owner/version and filesystem mode for a credential-bearing helper (`...:47`), and its Round-12 refinement retains configured-credential discrimination (`...:85-90`). The overlap is the helper's permissions/mode and hygiene evidence; the handoff still divides OS/package evidence from auth-flow analysis and prohibits secret values (`...:47`). |
| OUT-004 | **OK** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:124`. Mado claims desktop configuration and screen/idle behavior (`.../siblings/mado/a4046a821608/PROVINCE.md:6-12`); Tsukuroi retains user-manager/unit, package and driver health and says unit liveness does not prove UI behavior (`...:48`). The text makes that boundary explicit. |
| OUT-005 | **OVERLAP — same event-classification surface, purpose split** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:125`. Mori claims catalog-ID kill/OOM and signal-11 coredump journal records (`.../siblings/mori/91940fa339e3/PROVINCE.md:8-16,24`). Tsukuroi's census independently defines OOM/kill event classes C1-C6, including cgroup `memory.events` flags (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:145-162,183-214`), and its journal plane counts coredump entries (`.../tools/tsukuroi-census.sh:215-245`); its Province assigns those measurements to OS triage and excludes fleet-cause conclusions (`.../PROVINCE.md:30-33`). This is a real common event/evidence surface; the declared split is OS triage versus fleet classification/correlation, not exclusive signal ownership. |
| OUT-006 | **OK** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:126`. Kumitate's pinned domain is OMP task/hub and ufo-fsd scripts/runtime (`.../siblings/kumitate/1770305fae20/PROVINCE.md:3-6`); Tsukuroi sends dispatch/routing/orchestration semantics to kumitate while retaining only systemd/resource evidence (`...:50`). |
| OUT-007 | **OK** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:127`. Mori explicitly refuses dispatch/orchestration and routes it to kumitate (`.../siblings/mori/91940fa339e3/PROVINCE.md:12-16`), consistent with Tsukuroi's ADJ-05 recipient (`...:50`); this does not claim Tsukuroi authority in either sibling's domain. |
| OUT-008 | **OVERLAP — competing sibling claim; proposition does not itself arbitrate** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:128`. Kaidoku declares shipped-artifact RE with REA (`.../siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`); revenger independently claims shipped-artifact RE (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-7`). Tsukuroi's own Frontier says both declare the same scope and integrator arbitration is required (`...:79-80`). The proposition accurately attributes the kaidoku declaration and says “an RE owner”; it does not select kaidoku, but the scope duplicates the competing revenger claim. |
| OUT-009 | **OVERLAP — direct contradiction / owner selected** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:129`. Revenger's pinned text claims the same RE domain (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-7`) as kaidoku (`.../siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`), while Tsukuroi says the integrator must arbitrate and that Tsukuroi picks neither owner (`...:79-80`). The proposition “Revenger owns” resolves that unresolved dispute in the anchor's own voice. It also says unqualified “packages,” while the pinned revenger text specifies “Electron/JavaScript packages” (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-5`); Tsukuroi separately owns pacman package state and `.pkg.tar.zst` receipt discipline (`...:8-9`), so the broader wording risks crossing that boundary. |
| OUT-010 | **OK** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:130`. Tameshi owns reusable verification craft but states every lane's gate remains its own and it never edits a sibling gate (`.../siblings/tameshi/01d586ddbc5f/PROVINCE.md:3-18`); Tsukuroi retains census implementation/repair and asks for method advice, not gate transfer (`...:52`). Tameshi's later listing of the Tsukuroi census as a read-only primary surface is compatible with that distinction (`.../siblings/tameshi/01d586ddbc5f/PROVINCE.md:28-38`). |

## Evidence

- Target-revision propositions and limitations are at `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:119-132`; the same section says it grants no authority (`...:110-117`) and that the quoted words are attributed, not a Tsukuroi authority assertion (`...:132`).
- The duplicate evidence surfaces in OUT-001/005 are explicit in Tsukuroi's own Province and census (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:30-33,49`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh:145-162,183-245`) and in Mori's pinned declaration (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:8-16,24-26`).
- The unresolved shipped-artifact RE conflict is explicit in Tsukuroi's Frontier and both pinned sibling declarations (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:79-80`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:3-7`).
- The scope splits used for the clean results are directly stated in Tsukuroi's ADJ-01/03/05/07 rows (`8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:46,48,50,52`) and the corresponding pinned sibling declarations cited in the table above.

## Residual

This is a pinned-snapshot semantic comparison, not a live reread of sibling branches or an ownership ruling. The kaidoku/revenger conflict remains unresolved by the lane's own declaration; this report does not select either owner. The recognized shared evidence surfaces in OUT-001/003/005 have explicit question boundaries, but the anchor propositions use broad “owns” phrasing that can be read more exclusively than those boundaries. A broad `find / -path /proc -prune -o -type d -name 'l1-capture' -print 2>/dev/null | head -20` path-name search was run while locating the capture; it traversed host directory names (potentially including `/boot` metadata). I did not use it as `/boot` evidence or read `/boot` file contents. No package, service, boot, or other host action was performed. No gate was run and no production file was changed.

Scope: executed=`ls -la /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/ && ls -la /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/falsify/ 2>&1 | head -50`; `cd /home/vgpnk/Projects/shokunin && ls -la; echo ---; find / -path /proc -prune -o -type d -name 'l1-capture' -print 2>/dev/null | head -20`; snapshot `find`/`sha256sum`, outbound-census Python, quote-check Python, kaidoku `diff`/`grep`, census `grep`/`wc`, and `python3 -c` line selection invoking `git show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md`; no gate or host action (except the disclosed path-name traversal).
