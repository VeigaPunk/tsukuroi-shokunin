# Sibling-Overlap Scan & Held-Ground Census — Round 81

**Seat:** ConnectorOverlap  
**Wave:** w1  
**Lane Root:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Base Commit:** `96ad75b84160da58efaee4997576ce718fd72e2b`  
**Declaration Commit:** `8023711867eaa788f68af09d7f29d24db749cca7`  
**Declared Axes:** `depth`, `operability`, `freshness`  

---

## 1. Sibling-Overlap Scan

**Question:** Does any sibling lane already own the `fstab` → `mount unit` ground this round claims?  
**Query Target:** Every sibling lane repository under `/home/vgpnk/Projects/shokunin/*-shokunin/` (read-only), searching `PROVINCE.md`, `SKILL.md`, and `corpus/knowledge/**` for the regex terms:
`fstab`, `automount`, `x-systemd\.`, `mount unit`, `local-fs\.target`.

**Census Command:**
```bash
grep -n -E -i 'fstab|automount|x-systemd\.|mount unit|local-fs\.target' \
  <sibling>/PROVINCE.md <sibling>/SKILL.md <sibling>/corpus/knowledge/**
```

### Lane-by-Lane Report (20 Sibling Lanes)

1. **audio-shokunin**
   - Files examined: 19 files (`PROVINCE.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

2. **chousa-shokunin**
   - Files examined: 94 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

3. **game-dev-2d-shokunin**
   - Files examined: 6 files (`PROVINCE.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

4. **game-dev-3d-shokunin**
   - Files examined: 49 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

5. **kagi-shokunin**
   - Files examined: 37 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

6. **kaidoku-shokunin**
   - Files examined: 172 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership. (Note: owns binary RE and SquashFS decompression, but zero mount-unit/fstab translation rules).

7. **kake-shokunin**
   - Files examined: 85 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

8. **kama-shokunin**
   - Files examined: 61 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership. (PROVINCE explicitly refuses systemd writes and limits scope to model-serving endpoint health).

9. **kasegi-shokunin**
   - Files examined: 85 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
   - Hits: 0
   - Verdict: **Unrelated** / No ownership.

10. **kengaku-shokunin**
    - Files examined: 79 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

11. **kotoba-shokunin**
    - Files examined: 68 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

12. **kotodama-shokunin**
    - Files examined: 262 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership. (Owns bwrap isolation namespace replay, not fstab/mount-unit plane).

13. **kumitate-shokunin**
    - Files examined: 82 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership. (Owns swarm orchestration and runner isolation wrappers).

14. **lore-shokunin**
    - Files examined: 28 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

15. **mado-shokunin**
    - Files examined: 108 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

16. **mori-shokunin**
    - Files examined: 694 lines in `PROVINCE.md`, `SKILL.md`, 70+ knowledge files.
    - Hit: `corpus/knowledge/observability-census-r1.md:217`:
      ```markdown
      217:`MORI_*_BIN` overrides (an operator-supplied `df` can automount via the unquoted
      218:`MORI_DISK_TARGETS` list) — a live-mode refusal unless explicitly allowed is the
      ```
    - Hit Classification: **Incident mention** / carried threat-model debt note regarding `df` invocation risk under operator overrides. It does NOT claim or analyze fstab-to-mount-unit conversion.
    - Furthermore, `mori-shokunin/PROVINCE.md:12-14` explicitly **refuses** this domain and routes it to tsukuroi:
      ```markdown
      Refuses: dispatch and orchestration mechanism (→ kumitate); OS package,
      systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal
      and cgroup events as fleet evidence and reports them, never owning OS state;
      ```
    - Verdict: **Incident mention / Explicit refusal routing to tsukuroi**. No ownership.

17. **revenger-shokunin**
    - Files examined: 25 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

18. **souji-shokunin**
    - Files examined: 43 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

19. **tabi-shokunin**
    - Files examined: 77 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

20. **tameshi-shokunin**
    - Files examined: 72 files (`PROVINCE.md`, `SKILL.md`, `corpus/knowledge/**`)
    - Hits: 0
    - Verdict: **Unrelated** / No ownership.

### Sibling Ownership Conclusion
No sibling lane owns or claims the `fstab` → `mount unit` ground. Across 20 sibling repositories, exactly one hit was found (`mori-shokunin/corpus/knowledge/observability-census-r1.md:217`), which is a threat-model incident note concerning unquoted `df` arguments, accompanied by an explicit refusal in `mori-shokunin/PROVINCE.md:12-14` that assigns all systemd unit and boot state to `tsukuroi-shokunin`.

---

## 2. Adjacency Note Assessment for PROVINCE.md

**One-line verdict:**
No adjacency note is required in `PROVINCE.md` because no sibling lane owns or claims fstab→mount-unit translation, and the ground falls directly within `tsukuroi-shokunin`'s owned OS/systemd substrate domain (with mori explicitly refusing systemd/boot state in favor of tsukuroi).

---

## 3. Held-Ground Sweep in tsukuroi-shokunin (QUALITY 102)

**Command:**
```bash
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -i -E \
  'fstab|automount|systemd\.mount|x-systemd' 96ad75b84160da58efaee4997576ce718fd72e2b -- corpus/
```

**Observed Hits at Base `96ad75b8`:**
1. `corpus/SOURCES.md:62`: S056 source registration notes snapshot-2 `/etc/fstab` diff during round-17 Limine boot chain investigation. (Source metadata, unrelated to mount-unit translation).
2. `corpus/knowledge/boot-chain-r17.md:32`: Notes `/etc/fstab` package install timestamp (09:19:40). (Boot-chain triage, unrelated).
3. `corpus/knowledge/boot-chain-r17.md:90`: Mentions `/etc/fstab` in a list of root configuration files. (Unrelated).
4. `corpus/knowledge/boot-chain-r17.md:102-103`: Notes that snapshot #2 `/etc/fstab` lacks `/tmp` and `/fast` XFS lines (both `nofail`). (Historical snapshot observation, unrelated).
5. `corpus/knowledge/boot-chain-r17.md:184`: Lists S056 capture scope. (Unrelated).
6. `corpus/knowledge/degraded-triage-r4.md:400`: Mentions `/etc/fstab:18` mounting the ESP (`UUID=86D8-C3F6 /boot vfat`) during permission triage. (Unrelated).
7. `corpus/lessons/round-18.md:94`: Reflection text discussing S056 journal/fstab scope. (Unrelated).

**Additional Search for Generator & Unit Terms:**
```bash
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -i -E \
  'systemd-fstab-generator|fstab-generator|mount-unit' 96ad75b84160da58efaee4997576ce718fd72e2b -- corpus/
# Result: 0 matches (exit code 1)
```

**Held-Ground Finding:**
No prior entry in `tsukuroi-shokunin` holds rows MT1–MT8 or the fstab→mount-unit translation decision plane. The fstab→mount-unit plane is verified unheld prior ground, satisfying QUALITY 102(b).
