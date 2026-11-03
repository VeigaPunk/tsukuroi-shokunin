# S1Scout — C1-SCOPE (round 66 w1, scout, READ-ONLY)

Seat: S1Scout. Item: C1-SCOPE, serves claim C1 (S283).
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Host plazir27, 2026-11-03.
Timestamp: 2026-11-03T21:05:00Z.

## Verdict

`SCOPE-AGREES`

The systemd v262 kernel command line option `systemd.credentials_boot_policy=` as documented in
systemd v262 upstream man pages (`man/kernel-command-line.xml` line 70 and `man/systemd.xml` lines 968–1001)
strictly agrees with the S283 bullet in the pinned release body
(sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, section
"Changes in the system and service manager:", lines 248–253).
All four policy values (`strict`, `tofu`, `relaxed`, `off`), their respective definitions, default value
(`relaxed`), and the operational scope boundary (restricted to credentials encrypted with the "null" key,
having no effect on credentials encrypted with host or TPM2 keys) match between source documents.

## What I did

1. Initialized scratch directory `/fast/scratch/hyaku/tsukuroi-r66/S1Scout/`.
2. Fetched the systemd v262 kernel command-line options XML documentation:
   `https://raw.githubusercontent.com/systemd/systemd/v262/man/kernel-command-line.xml` to `$S/kcl.xml`.
   Verified rc 0, sha256 `eedf5d2ab6053de955367ef410221e95e935e8d2efb818bb21c27762f9243ff2`, 45823 bytes.
3. Searched for `credentials_boot_policy` in `$S/kcl.xml`:
   Located at line 70 (`<term><varname>systemd.credentials_boot_policy=</varname></term>`) in a block of
   system and service manager parameters (lines 65–80) pointing to `systemd(1)`.
4. Fetched the referenced `systemd(1)` XML documentation:
   `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.xml` to `$S/systemd.xml`.
   Verified rc 0, sha256 `458fc5efe5c00ee566d19fb842b0b6b914984fcb6d68af68788175d484372463`, 80075 bytes.
   Located full documentation block at lines 968–1001.
5. Re-fetched and verified the pinned v262 release body:
   `https://api.github.com/repos/systemd/systemd/releases/tags/v262` to `$S/rel.json`.
   Verified rc 0, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b`, 55194 bytes.
   Extracted the `systemd.credentials_boot_policy=` bullet from section "Changes in the system and service manager:".
6. Executed a line-by-line comparison of the four values and scope between the man pages and the S283 bullet.
7. Identified documented details present in the man page that the release bullet omits without amending the claim.
8. Authored `.ufo/waves/round-66/drafts/scout-s283-scope.md` and this wave report `.ufo/waves/round-66/w1/S1Scout.md`.

## Commands run (all rc)

```text
mkdir -p /fast/scratch/hyaku/tsukuroi-r66/S1Scout                                              rc 0
curl -sSf https://raw.githubusercontent.com/systemd/systemd/v262/man/kernel-command-line.xml  rc 0 (sha eedf5d2a… 45823 B)
grep -n 'credentials_boot_policy' $S/kcl.xml                                                 rc 0 (line 70)
curl -sSf https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.xml              rc 0 (sha 458fc5ef… 80075 B)
grep -n 'credentials_boot_policy' $S/systemd.xml                                             rc 0 (line 969)
curl -sSf https://api.github.com/repos/systemd/systemd/releases/tags/v262                    rc 0 (sha 008e1265… 55194 B)
sha256sum $S/kcl.xml $S/systemd.xml $S/rel.json                                              rc 0
wc -c $S/kcl.xml $S/systemd.xml $S/rel.json                                                  rc 0
```

No mutating, privileged, git, or package manager commands were run.

## Evidence Details

### 1. Document Locations and Line Numbers
- **`kernel-command-line.xml`**:
  - Line 70: `<term><varname>systemd.credentials_boot_policy=</varname></term>`
  - Lines 74–78:
    `<para>Parameters understood by the system and service manager to control system behavior. For details, see systemd(1).</para>` (16 words)
- **`systemd.xml`**:
  - Lines 968–1001: `<varlistentry>` defining `systemd.credentials_boot_policy=`.
  - Lines 971–978: Defines scope: "Controls under which conditions a credential encrypted with a null key is accepted at boot." (15 words)
  - Lines 980–991: Itemized list of values (`strict`, `tofu`, `relaxed`, `off`).
  - Lines 993–995: Default `relaxed`, specifies host/TPM2 key credentials are not affected and always accepted.

### 2. Value and Scope Comparison Matrix

| Option / Dimension | Release v262 Bullet (S283) | Man Page (`systemd(1)`) | Status |
|---|---|---|---|
| `strict` | "strict" (never) | `strict never accepts a null key, i.e. always insists on proper encryption.` | AGREE |
| `tofu` | "tofu" (first boot or no TPM2) | `tofu (trust on first use) accepts a null key during first boot, or when no TPM2 device is available.` | AGREE |
| `relaxed` | "relaxed" (SecureBoot disabled or no TPM2, the default and previous behavior) | `relaxed accepts a null key when SecureBoot is disabled, or when no TPM2 device is available.` and `Defaults to relaxed.` | AGREE |
| `off` | "off" (always) | `off always accepts a null key.` | AGREE |
| Scope: null key | controls when boot credentials encrypted with the "null" key are accepted | Controls under which conditions a credential encrypted with a null key ... is accepted at boot. | AGREE |
| Scope: host / TPM2 | It does not affect credentials encrypted with host or TPM2 keys. | it has no effect on credentials encrypted against a host key or TPM2 device, which are always accepted. | AGREE |

### 3. Documented Details Omitted by S283 Bullet
1. Envelope technical description: Credential wrapped in a `systemd-creds` envelope offering neither confidentiality nor authenticity (cites `systemd-creds(1)`).
2. Provisioning fallback purpose: Explicit explanation that this provides a fallback before a machine has a key to encrypt credentials against.
3. Acronym expansion: "trust on first use" for TOFU.
4. Strict clarification: "always insists on proper encryption".
5. Non-null credentials behavior: Explicit statement that host and TPM2 encrypted credentials "are always accepted".
6. Documentation pointer: Links to `https://systemd.io/CREDENTIALS`.
7. Cataloging: `kernel-command-line(7)` indexes the parameter at line 70 and references `systemd(1)`.

None of these omissions conflict with or narrow the scope asserted in S283.

## Files Written
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-66/drafts/scout-s283-scope.md`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-66/w1/S1Scout.md`

No tracked repository files were modified.

## Scratch Cleanup Confirmation
Scratch directory `/fast/scratch/hyaku/tsukuroi-r66/S1Scout/` held only fetched source artifacts and has been scheduled for clean removal before exit (`rm -rf`).
