# Cross-claim / cross-sibling overlap scan — round 66 (C2-OVERLAP)

Seat: C2Connector · lane: tsukuroi · round: 66 (hyaku run 15), wave w1 · base `c68bfe97`
Scope: read-only. Serves claim C2 (adjacency, live-verified sibling-ownership table + overlap table).
No tracked file was edited. This draft is a connector artifact only; it does not judge C1 or C2.

## 0. Method and receipts

Scratch (deleted on exit): `/fast/scratch/hyaku/tsukuroi-r66/C2Connector`
Snapshot dir: `/home/vgpnk/Projects/shokunin/<id>-shokunin`, read at each sibling's live `HEAD`.

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T21:02:37Z
```

### 0.1 Snapshot of each sibling `PROVINCE.md` at live HEAD

```
$ for id in kagi kaidoku revenger mori kumitate kama mado tameshi; do
    R=/home/vgpnk/Projects/shokunin/${id}-shokunin
    H=$(git -C "$R" rev-parse HEAD)
    git -C "$R" show "${H}:PROVINCE.md" > $S/${id}.PROVINCE.md
  done
```
rc=0 for all eight (no stderr on `git show`); the per-id `git show` stderr files are empty.

```
$ for id in ...; do git -C $R rev-parse HEAD; sha256sum $S/${id}.PROVINCE.md; wc -c < $S/${id}.PROVINCE.md; done
kagi      HEAD=91f7752ba551092eef20f6bd43d6dd798dc88ba0  sha256=0bbf19b3019e780269259b1acbbd45fcb9a53139fe6337609e7bd6448b364edd  bytes=17256
kaidoku   HEAD=c7fe6898e9a8b3ff04486b4a1d672e9db37610c9  sha256=50b6c259beb6816e26b3af91e44e5317f82e40eaf94993701781221ef7bb98c4  bytes=62928
revenger  HEAD=5915ad8d71c19ad377829d130ba1c35445eb32a4  sha256=c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502  bytes=3789
mori      HEAD=84c6cbc3b47c536a504aaee329c77897d389935e  sha256=2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838  bytes=49447
kumitate  HEAD=3c369336218329e30248b5d69c41348c02658169  sha256=fa9a63a8f62331595858868496c0516df04dfea456b18351d1a01be062ae47ed  bytes=8992
kama      HEAD=6035e952c2521999e192d6f236331f265ac98392  sha256=f0aaae9ccfd0ecb6641ad1646934f4ff5555fcc45d2e397670b2eb5ff083e8a6  bytes=24187
mado      HEAD=524fa1f90b1f2de44b3019bacf833d54e0af13a0  sha256=01c55ed921b1eb9ebb571f5801525d6c1b49576bf3a1d9a28ca9a4c083943a17  bytes=43709
tameshi   HEAD=f20ba482c7441d4c75818e7cd8a3165fee7821a1  sha256=0031aae86d34e39c753ac39ff4daf95a13761f9ba3992f221cc54c6c3bbb5a26  bytes=7786
```

These live HEADs and blob sha256 values are identical to the row values already staged in
`.ufo/waves/round-66/drafts/c2-anchors-live.tsv` (AR1–AR10), so the snapshots this scan read are
the same bytes the C2 recheck note will cite.

### 0.2 Grep A — the systemd boot-credential option plane (the C1/C2 surface under test)

```
$ for id in kagi kaidoku revenger mori kumitate kama mado tameshi; do
    grep -n -i -E 'credentials?_boot|credentials_boot_policy|systemd.*credential|boot.*credential|LoadCredential|TPM2|SecureBoot|UKI' $S/${id}.PROVINCE.md
    echo "rc=$?"
  done
```

| sibling | rc | hits |
|---|---|---|
| kagi | 1 | 0 |
| kaidoku | 1 | 0 |
| revenger | 1 | 0 |
| mori | 1 | 0 |
| kumitate | 1 | 0 |
| kama | 1 | 0 |
| mado | 1 | 0 |
| tameshi | 1 | 0 |

**Grep A returned rc=1 (no match) for all eight siblings.** No sibling `PROVINCE.md` at live HEAD
mentions `credentials_boot_policy`, a systemd credential option, `LoadCredential`, `TPM2`,
`SecureBoot` or `UKI`.

### 0.3 Grep B — who owns "credential" surfaces at all

```
$ for id in ...; do grep -n -i -E 'credential' $S/${id}.PROVINCE.md; echo "rc=$?"; done
```

| sibling | rc | hits | hit lines |
|---|---|---|---|
| kagi | 0 | 5 | 3, 71, 87, 90, 97 |
| kaidoku | 1 | 0 | — |
| revenger | 1 | 0 | — |
| mori | 0 | 4 | 15, 68, 129, 206 |
| kumitate | 1 | 0 | — |
| kama | 0 | 2 | 42, 49 |
| mado | 0 | 1 | 143 |
| tameshi | 0 | 2 | 18, 45 |

### 0.4 Grep C — adjacent wording (second pass, alternate spellings)

```
$ for id in ...; do grep -n -i -E 'systemd-creds|creds|null.key|encrypt|LoadCredential|SetCredential|ImportCredential|vault|secret' $S/${id}.PROVINCE.md; echo "rc=$?"; done
```
rc=0 with hits only for: kagi (lines 3, 25, 81, 87, 88, 89, 90, 99, 101, 104 — vault/secret ground),
kaidoku (298 — `embedded TLS secrets in a test capture are a property of that input`),
mori (68, 206, 392 — routing rows only), kumitate (14 — `secret members shape-only`),
mado (14, 18, 20, 25, 35, 143, 162, 180, 199, 200, 201 — secret-shaped redaction/refusals).
rc=1 (no match): revenger, kama, tameshi.
No sibling `PROVINCE.md` mentions `systemd-creds`, `SetCredential` or `ImportCredential` — the
systemd *unit* credential-passing surface is unclaimed by every sibling.

### 0.5 Grep D — boot / systemd base planes (for the boundary sentences)

```
$ for id in ...; do grep -n -i -E 'systemd' $S/${id}.PROVINCE.md; echo "rc=$?"; done
```
rc=1 (no match): kagi, kaidoku, revenger, kumitate, mado, tameshi.
rc=0: mori (9 hits; 13, 66, 370 are the routing rows), kama (7 hits; 47, 67, 210–211 are the
write-boundary rows).

```
$ for id in ...; do grep -n -i -E 'TPM|null.key|boot.?policy|secure.?boot|efi|unified kernel|limine|kernel command line' $S/${id}.PROVINCE.md; echo "rc=$?"; done
```
No match on any of `TPM`, `null key`, `boot policy`, `Secure Boot`, `EFI`, `unified kernel`,
`limine`, `kernel command line` in any of the eight siblings. Token-level confirmation:

```
$ for id in ...; do
    grep -n -i -o -E '(TPM2?|null.key|boot.?policy|secure.?boot|unified kernel|limine|kernel command line)' $S/${id}.PROVINCE.md | wc -l
    grep -n -i -o -E 'efi' $S/${id}.PROVINCE.md | wc -l
  done
kagi      strong_tokens=0 efi_substring=2
kaidoku   strong_tokens=0 efi_substring=1
revenger  strong_tokens=0 efi_substring=0
mori      strong_tokens=0 efi_substring=4
kumitate  strong_tokens=0 efi_substring=0
kama      strong_tokens=0 efi_substring=0
mado      strong_tokens=0 efi_substring=15
tameshi   strong_tokens=0 efi_substring=0
```

Every rc=0 row in this pass is the bare substring `efi` inside ordinary English words —
`prefix`/`prefixes`/`prefixed` (kagi 72–73, mori 106/391), `undefined` (mori 244/283),
`refinement` (mado), `definitions` (kaidoku 366) — verified by listing the containing words:

```
$ grep -n -i -o -E '[a-z]*efi[a-z]*' mado.PROVINCE.md | awk -F: '{print $2}' | sort -u
prefixed
refinement
$ grep -n -i -o -E '[a-z]*efi[a-z]*' kaidoku.PROVINCE.md | awk -F: '{print $2}' | sort -u
definitions
```

None is a boot-chain, EFI or TPM claim. Cross-check for a line that mentions boot *and* any
credential-family token at once (the shape an actual overlap would take):

```
$ for id in ...; do grep -n -i -E 'boot' $S/${id}.PROVINCE.md | grep -i -c -E 'credential|creds|TPM|secret|vault|encrypt'; done
kagi=0  kaidoku=0  revenger=0  mori=0  kumitate=0  kama=0  mado=0  tameshi=0
```

## 1. Overlap table

Anchor ids are the register's `OUT-<nnn>` ids from `corpus/knowledge/adjacency-anchors-r19.json`
(authority for the ten ownership anchors), read together with the live `PROVINCE.md` snapshots
above. "claims overlap" = the sibling's live text claims the systemd boot-credential / systemd-unit
credential plane that C2's overlap table is about.

| sibling | anchor id | claims overlap (yes/no) | evidence (grep command + hit line) | boundary sentence (sibling's own words) |
|---|---|---|---|---|
| kagi | `OUT-003` (ADJ-02) | **no** | `$ grep -n -i -E 'credentials?_boot\|credentials_boot_policy\|systemd.*credential\|boot.*credential\|LoadCredential\|TPM2\|SecureBoot\|UKI' kagi.PROVINCE.md` → rc=1, no hit. `$ grep -n -i -E 'systemd-creds\|creds\|null.key\|encrypt\|LoadCredential\|SetCredential\|ImportCredential\|vault\|secret' kagi.PROVINCE.md` → rc=0, hits at 3/25/81/87/88/89/90/99/101/104 — e.g. `kagi.PROVINCE.md:3` "**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence"; `kagi.PROVINCE.md:90` "kagi owns runtime auth and credential custody" and "no sibling claims SOPS, OpenBao/Vault, Credential Broker or workload-identity ground" | kagi owns secrets material, vault ops, credential custody and auth flows; it explicitly disclaims the systemd/Credential-Broker ground, so the systemd boot-credential *policy* knob is not kagi's — `kagi.PROVINCE.md:90` "kagi owns runtime auth and credential custody". |
| kaidoku | `OUT-008` (ADJ-06) | **no** | Grep A → rc=1, no hit. Grep B → rc=1, no hit. Grep C → rc=0 with a single hit at `kaidoku.PROVINCE.md:298` "embedded TLS secrets in a test capture are a property of that input" (a pcap-input property, not a systemd credential claim) | kaidoku's scope is shipped-artifact reverse engineering — `kaidoku.PROVINCE.md:3` "**Domain:** reverse engineering of shipped artifacts with REA on this Linux"; a documented kernel-command-line policy option needs no artifact RE, so no boundary is crossed. |
| revenger | `OUT-009` (ADJ-06) | **no** | Grep A → rc=1, no hit. Grep B → rc=1, no hit. Grep C → rc=1, no hit. `$ grep -n -i -E 'systemd' revenger.PROVINCE.md` → rc=1, no hit | revenger owns shipped-artifact reverse engineering — `revenger.PROVINCE.md:3` "Owns: reverse engineering of shipped artifacts — native binaries, managed"; it names no systemd, credential, boot or TPM surface at all. |
| mori | `OUT-001`, `OUT-005`, `OUT-007` (ADJ-04) | **no** | Grep A → rc=1, no hit. Grep B → rc=0, hits at 15/68/129/206 — e.g. `mori.PROVINCE.md:68` "| kagi | Owns secrets, vault operations, and credential-hygiene evidence; mori never reads or reports credential material."; `mori.PROVINCE.md:206` "with kagi advising only on actual credential/vault concerns". `$ grep -n -i -E 'systemd' mori.PROVINCE.md` → rc=0, 9 hits including `mori.PROVINCE.md:13` "systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal" | mori routes boot and systemd-unit state to tsukuroi and credential material to kagi — `mori.PROVINCE.md:13` "systemd unit, driver/firmware and boot state (→ tsukuroi)"; `mori.PROVINCE.md:247-248` "kernel and boot configuration diagnosis belongs to tsukuroi". |
| kumitate | `OUT-006` (ADJ-05) | **no** | Grep A → rc=1, no hit. Grep B → rc=1, no hit. Grep C → rc=0, single hit at `kumitate.PROVINCE.md:14` "rows K1–K5, gated by `scripts/kimi-census.mjs` (member set; secret members shape-only) + `scripts/proxy-check.mjs` (`coverage_kimi`)" | kumitate owns orchestration tooling and treats credential members shape-only — `kumitate.PROVINCE.md:14` "secret members shape-only"; no systemd credential policy surface is claimed or routed here. |
| kama | `OUT-002` (ADJ-01) | **no** | Grep A → rc=1, no hit. Grep B → rc=0, hits at 42/49 — `kama.PROVINCE.md:42` "**Refuses:** model quality/eval (kengaku), credential material & auth flows (kagi),". `$ grep -n -i -E 'systemd' kama.PROVINCE.md` → rc=0, 7 hits including `kama.PROVINCE.md:47` "**Write boundary (hard):** kama never writes to `~/.config`, `~/.omp`, or systemd" | kama refuses credential material and auth flows to kagi and refuses systemd writes — `kama.PROVINCE.md:42` "credential material & auth flows (kagi)"; `kama.PROVINCE.md:47` "kama never writes to `~/.config`, `~/.omp`, or systemd". |
| mado | `OUT-004` (ADJ-03) | **no** | Grep A → rc=1, no hit. Grep B → rc=0, single hit at `mado.PROVINCE.md:143` "…they are desktop facts, not credentials…". Grep C → rc=0, hits are secret-redaction refusals, e.g. `mado.PROVINCE.md:14` "**Refuses:** secrets in configs (shape-only, → kagi), model endpoints" | mado refuses secrets to kagi shape-only and holds the desktop config plane — `mado.PROVINCE.md:14` "secrets in configs (shape-only, → kagi)"; `mado.PROVINCE.md:143` "desktop facts, not credentials". |
| tameshi | `OUT-010` (ADJ-07) | **no** | Grep A → rc=1, no hit. Grep B → rc=0, hits at 18/45 — `tameshi.PROVINCE.md:18` "Credential material (→ kagi), endpoint health (→ kama)." and `tameshi.PROVINCE.md:45` "product clauses (owner lane); credential material (kagi); endpoint". Grep C → rc=1, no hit | tameshi owns the reusable verification method and routes credential material to kagi — `tameshi.PROVINCE.md:18` "Credential material (→ kagi), endpoint health (→ kama)." |

All eight siblings: **claims overlap = no.**

## 2. Boundary: systemd boot-credential option vs. kagi's secrets/vault ownership (ADJ-02)

The two surfaces are adjacent in vocabulary and disjoint in ground. The systemd boot-credential
option is a **boot-policy knob**: it decides *whether the system manager accepts at boot* a
credential envelope that was encrypted with the null key, and it is consumed by the system manager
from the kernel command line — so the ground it touches is the systemd/boot-configuration plane,
not secret custody. Kagi's ADJ-02 row is the opposite kind of claim: it is about **material** and
**custody** — a credential-bearing helper's permission/ownership finding or an auth-flow question,
answered from package owner/version, filesystem mode, uid/gid, and scoped so that secret values,
vault references, session bytes and helper invocation stay out (the lane's own ADJ-02 row, quoted
here only as a paraphrase of its scope, not as sibling text). Kagi itself draws the same line in
its own words: `kagi.PROVINCE.md:3` "**Domain:** secrets & vault ops — the-janitor flows, credential
hygiene evidence"; `kagi.PROVINCE.md:90` "kagi owns runtime auth and credential custody" and, in
the same row, "no sibling claims SOPS, OpenBao/Vault, Credential Broker or workload-identity
ground" — the systemd credential-broker/boot-policy ground is therefore unclaimed by kagi and by
every other sibling in this scan. The crossing point that would matter is a *helper* finding
(a `systemd-creds`/credential file mode or ownership question), which ADJ-02 routes to kagi; the
C1/C2 surface under scan is the *policy switch* — which values exist, what the host's cmdline,
TPM2 and SecureBoot inputs are, and whether the option applies — and it is explicitly routed to
tsukuroi by mori's own rows, `mori.PROVINCE.md:13` "systemd unit, driver/firmware and boot state
(→ tsukuroi)" and `mori.PROVINCE.md:247-248` "kernel and boot configuration diagnosis belongs to
tsukuroi". No sibling claims that surface, and no sibling's credential text reaches it.

## 3. Cross-claim check (C1 vs C2)

C1's predicate is scoped to the systemd v262 `systemd.credentials_boot_policy=` plane (documented
mechanism, host boot chain, host policy inputs, applicability verdict). C2's predicate is a
live-verified sibling-ownership table plus an overlap table for the ADJ-02 / ADJ-06 / ADJ-04
boundaries around the systemd credential plane. The two predicates touch disjoint file sets: C1's
surface is a `corpus/knowledge/` note + one `corpus/SOURCES.md` row; C2's surface is
`corpus/knowledge/adjacency-recheck-r66.md` + the append-only erratum in
`corpus/knowledge/adjacency-anchors-r19.md`. This scan reads sibling `PROVINCE.md` files only and
writes one draft file; it creates no dependency between C1 and C2 and judges neither.

## 4. Notes for the L1

- The `2277` prose that C2's erratum must supersede is at `adjacency-anchors-r19.md:204`
  (`| IN-109 | … | 2277 | check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED |`),
  and the register's authoritative value for that row is `found_line: 2822`
  (`corpus/knowledge/adjacency-anchors-r19.json`, entry `IN-109`). This scan did not edit either
  file; the superseding edit belongs to the C2 anchor seat.
- Grep A's rc=1 across all eight siblings is the citable "found nothing" evidence for the
  systemd-credential-plane non-overlap; Grep B/C are the citable evidence for the
  secrets-material-vs-systemd-unit-credential separation.

**Verdict: NO-OVERLAP — the grep that found nothing is
`grep -n -i -E 'credentials?_boot|credentials_boot_policy|systemd.*credential|boot.*credential|LoadCredential|TPM2|SecureBoot|UKI'` over all eight sibling `PROVINCE.md` files at live HEAD (rc=1 for every sibling; 0 hits); the only `credential` hits are kagi's secrets-material/vault ownership and other siblings' refusals routing to kagi.**
