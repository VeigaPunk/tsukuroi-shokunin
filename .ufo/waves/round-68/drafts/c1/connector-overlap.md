2026-11-03T22:31:27Z

# Round 68 — C1Connector: cross-claim and sibling-overlap scan (claims C1 and C2)

Seat C1Connector, lane tsukuroi-shokunin @ base `42400ec6`, wave w1 (round 68, hyaku run 15).
Classification only. This file grants no authority, edits no tracked file, and does not judge,
admit, integrate or ship either claim. Every number below carries its command and rc.

## 1. Method and read boundary

| # | what | command | result | rc |
|---|---|---|---|---|
| M1 | adjacency table rows | `grep -n 'ADJ-0' PROVINCE.md` | ADJ-01..ADJ-07 at `PROVINCE.md:46-52` | 0 |
| M2 | ownership anchors | `grep -n 'OUT-0' PROVINCE.md` | OUT-001..OUT-010 rows at `PROVINCE.md:121-130`; digest list `PROVINCE.md:137-146` | 0 |
| M3 | mori declaration | `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` | `2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838` | 0 |
| M4 | mori pinned blob | `git -C …/mori-shokunin cat-file -p 91940fa339e38006f8db5bd7d78bb6f037f4d016:PROVINCE.md \| sha256sum` | `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130` | 0 |
| M5 | mori live head | `git -C …/mori-shokunin rev-parse HEAD` | `84c6cbc3b47c536a504aaee329c77897d389935e` | 0 |
| M6 | mori drift | `git … diff --stat 91940fa3…HEAD -- PROVINCE.md` | `1 file changed, 423 insertions(+), 7 deletions(-)` | 0 |
| M7 | sibling `KNOWLEDGE-REF` | `grep -rl 'KNOWLEDGE-REF' /home/vgpnk/Projects/shokunin/*-shokunin/tools` | no output | 1 |
| M8 | sibling v7 URL holders | `grep -rl 'raw.githubusercontent.com/torvalds/linux/v7' …/*-shokunin/corpus \| awk -F/ '{print $6}' \| sort \| uniq -c` | `2 kama-shokunin`, `2 kumitate-shokunin`, `40 mori-shokunin`, `14 tsukuroi-shokunin` | 0 |
| M9 | sibling v7.3 raw URLs | `grep -rho 'raw\.githubusercontent\.com/torvalds/linux/v7\.3/[…]*' <repo>/corpus \| sort -u \| wc -l` | kama 0, kumitate 0, tsukuroi 0, mori 1 (a brace-form locator in a lesson, no C1 path) | 0 |

Read scope honoured: sibling `PROVINCE.md`, sibling `tools/`, and sibling `corpus` registry/knowledge
lines only (steps 3-5 of the item). No sibling file was written; no git mutation was issued anywhere.
Scratch `/fast/scratch/hyaku/tsukuroi-r68/C1Connector` was created, used for nothing else, and removed
before yield (no receipt depends on it).

## 2. Mori declaration digest — MATCH=no, and why it is not an anchor failure

The item asks for the file's `sha256sum` compared with the OUT-001 digest. They differ:

- file digest (M3): `2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838`
- OUT-001 digest (`PROVINCE.md:137`, repeated at `:141`/`:142`/`:143` for OUT-005/007): `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130`

Reconciliation, not repair: the digest at the pinned commit **does** match the pin. The pinned blob
at `91940fa339e3` hashes to `73abda79…` (M4), and mori's live HEAD is `84c6cbc3` (M5), five commits
past the pin for this path (M6), all append-only in the two anchor quotes:

- `sed -n '9p' PROVINCE.md` at HEAD → `independently labeled user/system journals, plus cgroup …`
  (1 hit for the OUT-001 string, as at the pin: `git cat-file -p 91940fa3:PROVINCE.md | grep -c` → `1`)
- `sed -n '8p' PROVINCE.md` at HEAD → `pair); kill/OOM-related catalog-ID records and signal-11 …`
  (1 hit for the OUT-005 string, as at the pin)

So `MORI_MATCH=no` is a **locator-freshness finding**: the anchor table pins bytes that still exist and
still carry both quoted clauses, but the sibling's live file has moved. The anchor remains valid for the
bytes it names; it is not valid as "mori's current PROVINCE.md". No fix is proposed here.

## 3. The memory-controller reading — which sibling owns each surface

C1's note is not yet written (`ls corpus/knowledge/linux-v73-pinwatch-r68.md` → `No such file or
directory`, rc 2; `.ufo/waves/round-68/drafts/c1/` empty at start, `ls -la` rc 0). The claim is therefore
read from the frozen declaration only (`SCORECARD.md:5119`, rows RW1-RW6).

| surface (C1 row) | owner per anchor | anchor quote (located) | reading |
|---|---|---|---|
| cgroup v2 `memory.events` and `memory.events.local` fields (RW1) | **mori** | OUT-001, `PROVINCE.md:121`, quoting mori `PROVINCE.md:9` @`91940fa3`: "independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;" — proposition cell: "Mori owns kill/OOM and cgroup memory evidence" | C1 may record **byte identity at drifted lines** (the declared spot-check: `memory.events` 1468 → 1495, `memory.events.local` 1517 → 1544). It may not claim what the counters mean or whether they date an event. |
| `memory.events` `oom_kill` field and the `Out of memory` / `Memory cgroup out of memory` label split (RW1, RW4; S182) | **mori** | OUT-005, `PROVINCE.md:125`, quoting mori `PROVINCE.md:8`: "kill/OOM-related catalog-ID records and signal-11 coredump records"; ADJ-04, `PROVINCE.md:49`: "cumulative counters are not dated incidents", recipient `mori` | Same: byte and line identity pass through; classification of a kill as dated/undated, or as memcg-versus-global, is mori's. ADJ-04 also states the evidence it wants back: "Capture time, boot/window, exact counter or PSI command/exit and observed value". |
| `mm/oom_kill.c` code reading for victim selection (S149, S182) | **no anchor** | none of OUT-001..OUT-010 names upstream kernel *source* reading; ADJ-06 (`PROVINCE.md:51`) covers "shipped-artifact reverse engineering", not upstream source | `NONE` — unassigned, not free. The adjacent risk is the derived finding: OOM victim/kill semantics route to mori under OUT-005. Mori independently pins the same bytes already (`mori corpus/SOURCES.md:270` S491 = `mm/oom_kill.c` @v7.2; `:295` S516 = @v7.3), so a code *finding* would land on an already-occupied surface. |

One tension inside the sibling, stated not smoothed (mori `PROVINCE.md:66` @`91940fa3` and at HEAD):
"It was the only sibling hit in R12Connector's corpus search for `systemd-oomd`, `earlyoom`,
`memory.events`, and `MESSAGE_ID`" — mori's own sibling table calls tsukuroi the host-diagnosis owner
while `PROVINCE.md:9` claims "cgroup `memory.events`" as mori's evidence surface. Both sentences
coexist in the pinned bytes; they split as *reading the file* (tsukuroi, host diagnosis) versus *using
its counters as fleet kill/OOM evidence* (mori). C1's RW1 spot-check stays on the first side only.

## 4. C2 gate — the same cross-check already exists in a sibling

Item 4's command found nothing: `grep -rl 'KNOWLEDGE-REF' /home/vgpnk/Projects/shokunin/*-shokunin/tools`
→ no output, **rc 1**; a widened run over `tools/` and `corpus/` also returned **rc 1**. The tool the C2
claim names is itself absent at base: `ls -la tools/check-knowledge-refs-r68.py` → `No such file or
directory`, **rc 2** (only `check-knowledge-header.py` exists, 23058 B).

The *check*, however, is not new fleet-wide. Two souji tools already resolve `source:` S-ids against the
registry, one of them revision-aware over committed bytes:

| sibling artifact | located text | what it already does |
|---|---|---|
| `souji-shokunin/tools/souji-gate-check.py:14` | "every 'source: S<digits>' id cited in the entry resolves in corpus/SOURCES.md" | check5, `:40` `SOURCE_RE = re.compile(r"^\s*(?:[-*]\s*)?source:\s*(S\d{3,})", re.M)`, `:128` `check5-dangling-source: %s`, fixture `:244` `source: S999 — missing` → `dangling-source` |
| `souji-shokunin/tools/souji-registry-agreement.py:9-10` | "every S### cited in the front-matter `source:` lines of a corpus/knowledge/*.md" | K1 registry↔entry over `git cat-file` at a required `--rev`; **stricter** than membership — the row's `used-by` must also name the entry |

Delta that survives (the C2 claim is not weakened by this, but its novelty is lane-scoped, not fleet-novel):
the header gate's binding and fence rules — operative `source:` line only, fenced blocks ignored, established
by `tools/check-knowledge-header.py:5,11` and its own fixture at `:415` (`source: S999.` passes today, only
header findings expected), which is exactly the round-66 routed gap. `souji-gate-check.py` has no fence
handling (`grep -n 'fence\|```' tools/souji-gate-check.py` → no output, rc 1).

Action: keep C2; the gate's docstring and its `--selftest` red cases should name the two souji tools as
prior art and state the delta (fence/binding semantics; membership only, no `used-by` reverse edge).

## 5. v7.3 registry rows — the bytes are already registered in mori

C1 opens S286 (`cgroup-v2.rst` @v7.3) and S287 (`fs/btrfs/sysfs.c` @v7.3) as new reference rows, fetched
from `raw.githubusercontent.com/torvalds/linux/v7.3/…` (`.ufo/waves/round-68/before/src/FETCH.txt`).
mori's registry already holds the same tag content, by a different route:

| mori row | locator route | content evidence |
|---|---|---|
| `mori corpus/SOURCES.md:313` S533 | `…git.kernel.org/…/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3` | mori `corpus/knowledge/cgroup-pressure-r62.md:4` — pinned copy `corpus/evidence/sources-r61/cgroup-v2.rst` sha256 `2750c11a…` |
| `mori corpus/SOURCES.md:319` S539 | `…plain/fs/btrfs/sysfs.c?h=v7.3` | row text carries `sha256 098cb…` |
| `mori corpus/SOURCES.md:295` S516 | `…plain/mm/oom_kill.c?h=v7.3` | v7.3, quote lines 424… |
| `mori corpus/SOURCES.md:309` S529 | `…plain/Documentation/accounting/psi.rst?h=v7.3` | v7.3 |

`2750c11a…` and `098cb…` are the digests C1 declares for the same two files (SHA256SUMS in
`before/src/`), so the *v7.3 bytes* are fleet-registered; what is new is the host-applicability read
(host `linux 7.2.11.arch1-1` → registry pin @v7.2) and the route-independent confirmation.

The route is the risk, and a sibling has already measured it — `mori corpus/lessons/round-53-verifier-spotcheck.md:136`:
"`mm/util.c` → HTTP 429 (324 bytes), `mman.h` and `mmap.c` → 200 with bytes equal to the cgit copies",
vote `reject`, reason "it cannot be the stable locator of a row". C1's own fetch succeeded on all four
paths on 2026-11-03 (`before/src/SHA256SUMS`, eight digests), so the rows are payable today; a later
recheck of S286/S287 on a throttled path would read as drift, not as transport failure.

## 6. Overlap register

| id | surface | this lane's claim | sibling | sibling anchor (quote ≤25 words, located) | class | action |
|---|---|---|---|---|---|---|
| OV-01 | cgroup v2 `memory.events` / `memory.events.local` field anchors | RW1 records byte identity at line 1468 → 1495 and 1517 → 1544 | mori | "independently labeled user/system journals, plus cgroup `memory.events` and the explicit same-boot journal window after a retained anchor;" — OUT-001, `tsukuroi PROVINCE.md:121` citing mori `PROVINCE.md:9` @`91940fa3` | INBOUND-RESOLVES | RW1 states bytes and line numbers only; cite OUT-001; claim no counter semantics |
| OV-02 | `oom_kill` field, dated-vs-cumulative, memcg-vs-global label | RW1/RW4 read `oom_kill` 1507 → 1533 and the S182 label split | mori | "kill/OOM-related catalog-ID records and signal-11 coredump records" — OUT-005, `tsukuroi PROVINCE.md:125` citing mori `PROVINCE.md:8`; ADJ-04 `:49` "cumulative counters are not dated incidents" | INBOUND-RESOLVES | RW4 records the byte pair only; any dated-event reading is mori's correlation, not C1's finding |
| OV-03 | `mm/oom_kill.c` victim-selection code reading (S149, S182) | RW3/RW4 read the same code at v7.2 and v7.3 | none named (mori has the bytes: `SOURCES.md:270` S491, `:295` S516) | OUT-001 proposition "Mori owns kill/OOM and cgroup memory evidence" (`PROVINCE.md:121`); no anchor assigns upstream source reading | NONE | Unassigned surface; keep to byte/line verdicts; do not derive a victim-selection finding ADJ-04 would route |
| OV-04 | S286 — `cgroup-v2.rst` @v7.3 as a new row on the `raw.githubusercontent` route | new reference row, v7.3 sha256 `2750c11a…`, CHANGED vs S138 | mori | "it cannot be the stable locator of a row" — mori `corpus/lessons/round-53-verifier-spotcheck.md:136` (HTTP 429 on 1 of 3 paths, vote `reject`) | CONFLICTS | Sibling precedent rejects this route as a row locator while C1 opens a row on it. Keep the row (separate registry, bytes pinned locally) and make its recheck name the pinned bytes, or add the cgit secondary locator, so transport cannot read as drift |
| OV-05 | S287 — `fs/btrfs/sysfs.c` @v7.3 as a new row on the same route | new reference row, v7.3 sha256 `098cb522…`, CHANGED vs S158 | mori | same precedent, `round-53-verifier-spotcheck.md:136`; bytes already at mori `SOURCES.md:319` S539 "sha256 098cb…" | CONFLICTS | Same as OV-04; cite S539 and state the route delta (raw vs cgit), not "first v7.3 pin" |
| OV-06 | RW3/RW5 UNCHANGED verdicts (`mm/oom_kill.c`, `psi.rst` @v7.3) | sha256 identical to the v7.2 rows (`452f1348…`, `11c6b712…`) | mori | `SOURCES.md:295` S516 (v7.3 `oom_kill.c`), `:309` S529 (v7.3 `psi.rst`) | AGREES | Cite as independent confirmation; no action |
| OV-07 | dangling `source:` S-id vs registry (C2) | new gate reports `KNOWLEDGE-REF-DANGLING` per absent id at `--revision` | souji | "every S### cited in the front-matter `source:` lines of a corpus/knowledge/*.md" — `souji-registry-agreement.py:9-10`; `souji-gate-check.py:14` `resolves in corpus/SOURCES.md` | AGREES | Not fleet-novel; name both souji tools as prior art and state the fence/binding delta |
| OV-08 | mori declaration locator vs live bytes | OUT-001/OUT-005 pin `91940fa3` sha256 `73abda79…` | mori | "kill/OOM-related catalog-ID records and signal-11 coredump records" present at both `91940fa3:8` and live `PROVINCE.md:8` | AGREES | Locator is stale-by-commits but quote-intact; no re-pin proposed this round |
| OV-09 | the v7.2 `cgroup-v2.rst` upstream URL itself | S138's URL is the same URL kumitate registered | kumitate | `kumitate corpus/SOURCES.md:92` S079 "Linux kernel cgroup v2 admin guide, tag v7.2" (2 corpus files hold the URL) | NONE | Registry-level sharing only; no ownership claim, no action |

`OVERLAP_ROWS=9`; `CONFLICTS=2` (OV-04, OV-05 — both the same sibling precedent against the new-row
route choice); `NONE` rows stated explicitly: OV-03, OV-09.

## 7. Tensions stated, not resolved

1. **C1 v7.3 rows vs mori's route precedent** (OV-04/OV-05) — a sibling's measured vote says the raw
   route cannot locate a row; C1 uses it for two rows. The rows survive on locally pinned bytes; the
   contradiction is not dissolved.
2. **Mori `PROVINCE.md:9` vs `:66`** — cgroup `memory.events` claimed as mori evidence, yet tsukuroi is
   named the sole host-diagnosis hit for `memory.events`. Split reading (own it) versus evidence use
   (mori) is the only reading the bytes support; C1 must stay on the first.
3. **C2 "new gate" vs souji check5/K1** — the frozen claim's baseline is this lane's header gate, so no
   overreach; but "new" is lane-scoped and the register says so.
4. **`MORI_MATCH=no`** — the literal comparison fails while the pinned blob passes. Both facts are
   recorded; neither is scored away.

## 8. Limits

- C1's note and C2's tool do not exist at base, so this scan compares the frozen declaration
  (`SCORECARD.md:5119-5120`) against sibling material; it cannot audit the unwritten artifacts.
- Sibling state is committed bytes at each sibling's HEAD on 2026-11-03; a later sibling commit is
  uncovered. A located quote proves presence, not sibling agreement.
- No sibling acknowledged, accepted or acted on any row. `prepared` is not `reported`.
- No host command beyond read-only `grep`/`sed -n`/`sha256sum`/`ls`/`git show|cat-file|log|diff` was run;
  no pacman, no systemctl, no sudo, no network fetch.
