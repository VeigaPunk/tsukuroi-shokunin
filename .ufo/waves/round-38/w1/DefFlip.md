VERDICT: draft

# Seat DefFlip — item D-2 (routed defect 6): flip condition for the rejected `mount-errno-contract-r26.md`

## 1. What the item is

The round-37 Gate rejected the staged `mount-errno-contract-r26.md` with a reason and no flip condition
(`corpus/lessons/round-37.md:74`). The closure recorded that absence twice: as a status-neutral conformance note
(`corpus/lessons/round-37-verifier-spotcheck.md:28`: “The `mount-errno-contract-r26.md` rejection (`:74`) states a
reason and no flip”) and as routed defect 6 (`:130`: “lacks a flip condition … Append a flip condition”). The
spot-check's own S-table row agrees with the reject and repeats the missing clause (`:95`).

Rejection text, verbatim (read as `:74:raw`): the staged entry “compared its broad `CAP_SYS_ADMIN` → `EPERM`
subvolume-creation claim with the lane's round-12/13 CX2 correction; that claim would revive a known contradiction.”
The reason names a *proposition*, not an unreachable artifact, so a flip condition is expressible.

## 2. Re-opening the source basis (my own read, not the round-37 seat's)

Fetched 2026-10-26 from `raw.githubusercontent.com/torvalds/linux/v7.2/`: `fs/btrfs/ioctl.c`
(sha256 `08992385…d40c13`, 5670 lines), `fs/namei.c` (`d5498d87…d36c4a`), `fs/inode.c` (`ddae1882…9c683`).
Receipt with all commands and numbered excerpts: `.ufo/waves/round-38/w1/DefFlip/evidence.txt`.

The reject's stated basis holds, and one part of it is imprecise:

| Fact | Pinned evidence |
|---|---|
| `btrfs_mksubvol` has no capability test | `ioctl.c:859-904`; `grep 'capable'` over the function body returns no match (rc=1) |
| its refusal is DAC, not capability | `ioctl.c:875` `may_create_dentry(...)` → `fs/namei.c:3742` `inode_permission(idmap, dir, MAY_WRITE \| MAY_EXEC)` → `-EACCES`; the same helper only adds `-EEXIST`/`-ENOENT`/`-EOVERFLOW` (`namei.c:3731-3743`) |
| `create_subvol` also has no capability test | `grep 'capable\|EPERM'` over the function body returns no match (rc=1) |
| the snapshot path's only `-EPERM` is the ownership branch | `ioctl.c:1181` `!inode_owner_or_capable(...)`; comment `:1182-1185` “Subvolume creation is not restricted, but snapshots are limited to own subvolumes only”; `ret = -EPERM` at `:1186` |
| that branch's capability is **CAP_FOWNER**, not CAP_SYS_ADMIN | `fs/inode.c:2764` `ns_capable(ns, CAP_FOWNER)`; header comment `:2744-2745` “CAP_FOWNER … or owns the file” |
| the staged claim is false **as written** because of a universal quantifier | staged `mount-errno-contract-r26.md:39-40` “The ioctls that change the filesystem require `CAP_SYS_ADMIN` and return `EPERM` without it”; `:46` maps `EPERM` to “missing `CAP_SYS_ADMIN` for mount, or snapshotting a subvolume you do not own” |
| but a **scoped** version of it is true, and citable | `btrfs_ioctl_add_dev` gate `ioctl.c:2520-2521`, dispatched from `case BTRFS_IOC_ADD_DEV:` `:5528-5529`; the file has 35 `capable(CAP_SYS_ADMIN)` sites |

Additional defects in the staged bytes, found while drafting (each blocks an admit independently of the CX2 point):

- **No QUALITY check.** `grep -c 'QUALITY'` on the staged file → `0`. QUALITY 14 (`corpus/QUALITY.md:19`) requires an
  explicit `## QUALITY check` before an admit; the r25 rejection was on this same ground.
- **Unresolvable source anchors.** The entry declares `S214` and `S220`; `grep -n '^| S214 \|^| S220 ' corpus/SOURCES.md`
  returns rc=1 — neither id exists in the lane registry, so QUALITY 7 (`corpus/QUALITY.md:11`) is unmet.
- **Revision mismatch.** The entry cites `kernel tag v7.2` in its `source:` line (`:3`) but its `recheck:` line says
  “re-read fs/btrfs/ioctl.c at the host's kernel tag” (`:5`). The host reports `7.2.11-arch1-1` (`uname -r`), which is not
  tag v7.2. A revised entry must pin one revision and cite that revision's bytes.
- **Imprecise capability name.** The `:46` cell presents the snapshot `EPERM` as an ownership fact; the source makes it
  “not owner **and** not CAP_FOWNER” (`fs/inode.c:2764`). A caller holding CAP_FOWNER can snapshot a subvolume it does
  not own, so even the true half of the row is under-specified.

## 3. Proposed flip condition — exact text for the round-38 lesson Gate

Intended placement: the round-38 Gate's assimilation section, as an append-only erratum to the round-37 rejection
(matching the append-only convention at `corpus/QUALITY.md:7`). Wording keeps the lane's `Reason; flip condition` form used
by the r25 row (`corpus/lessons/round-37.md:22`).

> **Round-37 erratum — flip condition for `mount-errno-contract-r26.md`** (`corpus/lessons/round-37.md:74`; routed defect 6,
> `corpus/lessons/round-37-verifier-spotcheck.md:130`). The reject stands unless a revised entry replaces the unquantified
> capability claim at `mount-errno-contract-r26.md:39-40` and its `EPERM` cell at `:46` with per-ioctl, source-resolved
> pairs, and satisfies all four: **(a)** every capability→errno pair names the ioctl and the exact line that tests it, at
> the one revision the entry pins — the shape exists at v7.2, e.g. `BTRFS_IOC_ADD_DEV` (`fs/btrfs/ioctl.c:5528-5529`) →
> `capable(CAP_SYS_ADMIN)` / `return -EPERM` (`:2520-2521`) — and the capability named is the one tested; **(b)** the entry
> states the contrary fact for the creation path it previously covered: `btrfs_mksubvol` carries no capability test
> (`ioctl.c:859-904`), its refusal is `may_create_dentry` → `inode_permission(..., MAY_WRITE|MAY_EXEC)` (`ioctl.c:875`,
> `fs/namei.c:3742`) i.e. `-EACCES`, and its only `-EPERM` is `inode_owner_or_capable` (`ioctl.c:1181-1186`), which tests
> ownership or `CAP_FOWNER` (`fs/inode.c:2764`), not `CAP_SYS_ADMIN`; **(c)** it carries an explicit `## QUALITY check`
> scoring the criteria it invokes (the staged bytes have zero `QUALITY` occurrences, so QUALITY 14 is unmet) and cites only
> `corpus/SOURCES.md` rows that resolve — `S214`/`S220` match no row today, and a new row for the same `ioctl.c` URL under a
> different anchor is admissible, as S202/S203 already share the errno(3) URL (`corpus/SOURCES.md:211-212`) with W04
> duplicate-URL advisories non-blocking (`corpus/lessons/round-37.md:92`); and **(d)** it adds at least one proposition the
> admitted `mount-errno-contract-r37.md` does not carry, because deleting the false sentence alone leaves a duplicate of
> the note that already replaced it, and a duplicate is not a flip. What does **not** flip it: a live `EPERM` capture from
> the host (EPERM is produced by both the gated ioctls and the ownership branch, so the observation cannot discriminate the
> two claims — QUALITY 3, `corpus/QUALITY.md:5`; QUALITY 15, `:20`, forbids certifying a Btrfs ioctl cause from an ordinary
> control), and a re-read of the same path that finds no capability test (which is what v7.2 shows, `ioctl.c:859-904`).

## 4. Why each conjunct is verdict-changing and can fail

| Conjunct | Red-before (fails on the staged bytes) | Green side (mechanically resolved) |
|---|---|---|
| (a) | `:39-40` asserts the gate for all filesystem-changing ioctls; `:46` names CAP_SYS_ADMIN for a path that has none | `ioctl.c:2520-2521` is a real `capable(CAP_SYS_ADMIN) → -EPERM` on `BTRFS_IOC_ADD_DEV`; so (a) is satisfiable without the false universal |
| (b) | the staged entry never says the creation path lacks the gate, which is the CX2 contradiction | the absence is checkable in one command (`sed -n '859,904p' ioctl.c \| grep capable` → rc=1) |
| (c) | `grep -c QUALITY` → 0; `S214`/`S220` → rc=1 | a resolving row is admissible under the S202/S203 shared-URL precedent |
| (d) | the rejected entry's distinctive content *is* the false sentence; remove it and the remainder overlaps the admitted note | `mount-errno-contract-r37.md`'s table has no per-ioctl capability row, so (a)+(b) content is genuinely additive |

If only (c) is fixed, the verdict stays reject (the contradiction remains). If (a)-(c) are fixed by deletion alone, (d)
still fails — the entry becomes a duplicate of `mount-errno-contract-r37.md` and a duplicate rejection is the r25
precedent, not a flip. The condition therefore cannot be satisfied by shrinking the entry, which is the failure mode a
plain “revise it” clause would have licensed.

## 5. Limits of this seat's evidence

- I judged the rejection's source basis and drafted the flip text. I did **not** author, stage, census-validate or admit
  a revised entry; no lane file was created or edited, and no registry row was added.
- I read v7.2 upstream only. I did **not** open Arch's `7.2.11-arch1-1` source, so I cannot say whether the Arch patchset
  adds a creation-path gate; clause (a)'s “at the one revision the entry pins” covers either outcome without asserting it.
- No counter was run and none was needed: the flip condition resolves by line-level source reads plus two greps. I did not
  re-run any lane tool, census or counter (`scripts/sources-census.sh` untouched), and I did not verify the round-38
  claims C1/C2 — they are out of this item's scope.
- The `S214`/`S220` non-resolution is checked against the lane registry at tip `5edb6c2` (read-only); if round 38 appends
  those ids, conjunct (c) is re-evaluated against the new registry, not against this receipt.
- Tooling: nothing installed; no pacman, no service, no host mutation. Scratch
  `/fast/scratch/hyaku/tsukuroi-r38/DefFlip` removed after its hashes and excerpts were copied into
  `.ufo/waves/round-38/w1/DefFlip/evidence.txt`.

## 6. Receipts

- `.ufo/waves/round-38/w1/DefFlip/evidence.txt` — every command and numbered output cited above, plus the three upstream
  sha256 digests.
