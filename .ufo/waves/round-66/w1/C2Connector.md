# C2Connector — seat report (round 66, wave w1)

Seat: C2Connector · item: C2-OVERLAP · lane: tsukuroi · base `c68bfe97`
Serves claim: **C2** (adjacency — live-verified sibling-ownership table + overlap table).
Kind: connector, read-only. No tracked file edited; no claim judged.

Output artifact (full evidence, tables, receipts):
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-66/drafts/overlap-scan-r66.md`

## What was done

1. Snapshotted each of the eight siblings' `PROVINCE.md` at that repo's **live HEAD** into scratch
   (`git -C <repo> show "$(git -C <repo> rev-parse HEAD)":PROVINCE.md`), rc=0 for all eight.
2. Ran four greps over the snapshots and recorded every hit with file:line and rc:
   - **Grep A** — the systemd boot-credential option plane
     (`credentials?_boot|credentials_boot_policy|systemd.*credential|boot.*credential|LoadCredential|TPM2|SecureBoot|UKI`):
     **rc=1 (no match) for all eight siblings.**
   - **Grep B** — `credential`: kagi rc=0/5 hits, mori rc=0/4, kama rc=0/2, mado rc=0/1,
     tameshi rc=0/2; kaidoku, revenger, kumitate rc=1/0 hits.
   - **Grep C** — alternate wording (`systemd-creds|creds|null.key|encrypt|LoadCredential|SetCredential|ImportCredential|vault|secret`):
     rc=1 for revenger/kama/tameshi; rc=0 only for kagi (vault/secret ground), kaidoku (298, a
     pcap-input property), mori (routing rows), kumitate (14, shape-only), mado (secret-shaped
     redaction/refusals). **No sibling mentions `systemd-creds`, `SetCredential` or `ImportCredential`.**
   - **Grep D** — `systemd` (rc=1 except mori 9 hits, kama 7 hits) and a boot/TPM/EFI/kcmdline
     pass whose only matches are the bare substring `efi` inside `prefix`/`prefixes`/`prefixed`/
     `undefined`/`refinement`/`definitions` (token-level counts printed in the draft).
   - Cross-check: no sibling line mentions boot **and** a credential-family token at once
     (all eight = 0).
3. Wrote the overlap table (sibling | anchor id | claims overlap | evidence | boundary sentence),
   the boundary paragraph, and the cross-claim (C1↔C2) note into the draft artifact.

## Result

| sibling | anchor id | claims overlap |
|---|---|---|
| kagi | OUT-003 (ADJ-02) | no |
| kaidoku | OUT-008 (ADJ-06) | no |
| revenger | OUT-009 (ADJ-06) | no |
| mori | OUT-001, OUT-005, OUT-007 (ADJ-04) | no |
| kumitate | OUT-006 (ADJ-05) | no |
| kama | OUT-002 (ADJ-01) | no |
| mado | OUT-004 (ADJ-03) | no |
| tameshi | OUT-010 (ADJ-07) | no |

**Boundary (ADJ-02):** the systemd boot-credential option is a *boot-policy knob* — whether the
system manager accepts a null-key-encrypted credential envelope at boot, read from the kernel
command line; it sits on the systemd/boot-configuration plane. Kagi's ADJ-02 row is *material and
custody* — a credential-bearing helper's permission/ownership or auth-flow question. Sibling text
draws the same line: `kagi.PROVINCE.md:3` "**Domain:** secrets & vault ops — the-janitor flows,
credential hygiene evidence"; `kagi.PROVINCE.md:90` "kagi owns runtime auth and credential custody"
and, in the same row, "no sibling claims SOPS, OpenBao/Vault, Credential Broker or
workload-identity ground". Mori routes the boot/systemd side to tsukuroi —
`mori.PROVINCE.md:13` "systemd unit, driver/firmware and boot state (→ tsukuroi)";
`mori.PROVINCE.md:247-248` "kernel and boot configuration diagnosis belongs to tsukuroi".

**Verdict: NO-OVERLAP** — the grep that found nothing is
`grep -n -i -E 'credentials?_boot|credentials_boot_policy|systemd.*credential|boot.*credential|LoadCredential|TPM2|SecureBoot|UKI'`
over all eight sibling `PROVINCE.md` files at live HEAD (rc=1 for every sibling, 0 hits); the only
`credential` hits are kagi's secrets-material/vault ownership and other siblings' refusals routing
to kagi.

## Notes for the L1

- The live HEADs and blob sha256 values read by this scan match `c2-anchors-live.tsv` (AR1–AR10)
  exactly, so the overlap table and the recheck table are pinned to the same bytes.
- The `2277` prose C2's erratum must supersede is `adjacency-anchors-r19.md:204` (row IN-109);
  the register's authoritative value is `found_line: 2822` in
  `corpus/knowledge/adjacency-anchors-r19.json` (entry IN-109). Not edited here.
- No overlap means no new boundary row is *required*, but the draft's §1 table plus §2 paragraph
  supply the connector-scanned ADJ-02 / ADJ-04 / ADJ-06 boundary sentences the C2 claim's overlap
  table calls for.
- Scratch `/fast/scratch/hyaku/tsukuroi-r66/C2Connector` was deleted before yield; every receipt
  needed for the record is embedded in the draft artifact.

## Verification performed

- Every quoted sibling fragment in the draft was checked programmatically against the snapshot
  lines it cites (25 quoted fragments; all matched at their cited line ranges — the only
  checker misses were markdown line-wrap and ellipsis artifacts of the same fragments, each with
  a matching single-line variant).
- `grep` exit codes recorded for every pass and every file; no value in this report is inferred
  from a run that did not happen.
