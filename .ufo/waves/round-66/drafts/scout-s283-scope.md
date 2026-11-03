# S283 Scope Scout Receipt — systemd v262 credentials_boot_policy
Timestamp: 2026-11-03T21:05:00Z

## 1. Commands, Return Codes, and Hashes

Command:
$ curl -sSf https://raw.githubusercontent.com/systemd/systemd/v262/man/kernel-command-line.xml -o /fast/scratch/hyaku/tsukuroi-r66/S1Scout/kcl.xml
rc: 0
sha256: eedf5d2ab6053de955367ef410221e95e935e8d2efb818bb21c27762f9243ff2
bytes: 45823

Command:
$ curl -sSf https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.xml -o /fast/scratch/hyaku/tsukuroi-r66/S1Scout/systemd.xml
rc: 0
sha256: 458fc5efe5c00ee566d19fb842b0b6b914984fcb6d68af68788175d484372463
bytes: 80075

Command:
$ curl -sSf https://api.github.com/repos/systemd/systemd/releases/tags/v262 -o /fast/scratch/hyaku/tsukuroi-r66/S1Scout/rel.json
rc: 0
sha256: 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b
bytes: 55194

## 2. Man Page Locations and Option Documentation

### Location in `kernel-command-line.xml` (man kernel-command-line(7))
Option indexed at line 70:
$ grep -n 'credentials_boot_policy' /fast/scratch/hyaku/tsukuroi-r66/S1Scout/kcl.xml
70:        <term><varname>systemd.credentials_boot_policy=</varname></term>

Verbatim block (lines 65–80 of `kernel-command-line.xml`):
```xml
        <term><varname>systemd.setenv=</varname></term>
        <term><varname>systemd.machine_id=</varname></term>
        <term><varname>systemd.set_credential=</varname></term>
        <term><varname>systemd.set_credential_binary=</varname></term>
        <term><varname>systemd.import_credentials=</varname></term>
        <term><varname>systemd.credentials_boot_policy=</varname></term>
        <term><varname>systemd.reload_limit_interval_sec=</varname></term>
        <term><varname>systemd.reload_limit_burst=</varname></term>
        <term><varname>systemd.minimum_uptime_sec=</varname></term>
        <listitem>
          <para>Parameters understood by the system and service
          manager to control system behavior. For details, see
          <citerefentry><refentrytitle>systemd</refentrytitle><manvolnum>1</manvolnum></citerefentry>.</para>

          <xi:include href="version-info.xml" xpointer="v186"/>
        </listitem>
```
Documented status in `kernel-command-line.xml`:
Listed as a recognized kernel command line parameter delegated to `systemd(1)`.
Quoted listitem (16 words):
"Parameters understood by the system and service manager to control system behavior. For details, see systemd(1)."

### Location in `systemd.xml` (man systemd(1))
Option fully documented at line 969:
$ grep -n 'credentials_boot_policy' /fast/scratch/hyaku/tsukuroi-r66/S1Scout/systemd.xml
969:        <term><varname>systemd.credentials_boot_policy=</varname></term>

Verbatim block (lines 968–1001 of `systemd.xml`):
```xml
      <varlistentry>
        <term><varname>systemd.credentials_boot_policy=</varname></term>

        <listitem><para>Controls under which conditions a credential encrypted with a <literal>null</literal>
        key (i.e. a credential wrapped in a <command>systemd-creds</command> envelope but offering neither
        confidentiality nor authenticity, see
        <citerefentry><refentrytitle>systemd-creds</refentrytitle><manvolnum>1</manvolnum></citerefentry>)
        is accepted at boot. This provides a fallback for provisioning credentials before a machine has a key
        to encrypt them against, for example during first boot or on systems without a TPM2 device. Takes
        one of <option>strict</option>, <option>tofu</option>, <option>relaxed</option> or
        <option>off</option>:</para>

        <itemizedlist>
          <listitem><para><option>strict</option> never accepts a <literal>null</literal> key, i.e. always
          insists on proper encryption.</para></listitem>

          <listitem><para><option>tofu</option> (trust on first use) accepts a <literal>null</literal> key
          during first boot, or when no TPM2 device is available.</para></listitem>

          <listitem><para><option>relaxed</option> accepts a <literal>null</literal> key when SecureBoot is
          disabled, or when no TPM2 device is available.</para></listitem>

          <listitem><para><option>off</option> always accepts a <literal>null</literal> key.</para></listitem>
        </itemizedlist>

        <para>Defaults to <option>relaxed</option>. Note that this policy only applies to the default acceptance
        decision; it has no effect on credentials encrypted against a host key or TPM2 device, which are
        always accepted.</para>

        <para>For further information see <ulink url="https://systemd.io/CREDENTIALS">System and Service
        Credentials</ulink> documentation.</para>

        <xi:include href="version-info.xml" xpointer="v262"/></listitem>
      </varlistentry>
```

## 3. Comparison: S283 Bullet vs. Upstream Documentation

### S283 Bullet (Release v262 Body, lines 248–253)
Verbatim text from pinned release body (sha256: 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b):
```
        * The new systemd.credentials_boot_policy= kernel command line option
          controls when boot credentials encrypted with the "null" key are
          accepted. It accepts "strict" (never), "tofu" (first boot or no
          TPM2), "relaxed" (SecureBoot disabled or no TPM2, the default and
          previous behavior), and "off" (always). It does not affect
          credentials encrypted with host or TPM2 keys.
```
Gate quote candidate (18 words):
"The new systemd.credentials_boot_policy= kernel command line option controls when boot credentials encrypted with the "null" key are accepted."

### Value and Scope Comparison Matrix

| Item | S283 Release Note | Man Page (`systemd(1)`) | Status | Comparison Detail |
|---|---|---|---|---|
| `strict` | "strict" (never) | `strict never accepts a null key, i.e. always insists on proper encryption.` | AGREE | Both define strict as never accepting null-key encrypted credentials. |
| `tofu` | "tofu" (first boot or no TPM2) | `tofu (trust on first use) accepts a null key during first boot, or when no TPM2 device is available.` | AGREE | Both specify acceptance during first boot or when no TPM2 is available. |
| `relaxed` | "relaxed" (SecureBoot disabled or no TPM2, the default and previous behavior) | `relaxed accepts a null key when SecureBoot is disabled, or when no TPM2 device is available.` and `Defaults to relaxed.` | AGREE | Both specify SecureBoot disabled or no TPM2, and default/previous behavior. |
| `off` | "off" (always) | `off always accepts a null key.` | AGREE | Both define off as always accepting null-key encrypted credentials. |
| Scope: null key only | `controls when boot credentials encrypted with the "null" key are accepted` | `Controls under which conditions a credential encrypted with a null key ... is accepted at boot.` | AGREE | Both restrict policy scope to credentials encrypted with the null key. |
| Scope: host / TPM2 keys | `It does not affect credentials encrypted with host or TPM2 keys.` | `it has no effect on credentials encrypted against a host key or TPM2 device, which are always accepted.` | AGREE | Both confirm policy does not affect credentials encrypted with host or TPM2 keys. |

## 4. Documented Details Omitted by S283 Bullet
The man page (`systemd(1)`) provides technical elaborations not present in the release bullet:
1. Envelope semantics: Defines a null key as "a credential wrapped in a systemd-creds envelope but offering neither confidentiality nor authenticity, see systemd-creds(1)".
2. Provisioning rationale: Explains purpose as "provides a fallback for provisioning credentials before a machine has a key to encrypt them against, for example during first boot or on systems without a TPM2 device".
3. TOFU expansion: Spells out acronym as "trust on first use".
4. Strict elaboration: Adds "i.e. always insists on proper encryption".
5. Non-null credentials behavior: Explicitly adds that host/TPM2 credentials "are always accepted".
6. Canonical reference: Cites upstream documentation URL "https://systemd.io/CREDENTIALS".
7. Command line cataloging: `kernel-command-line(7)` lists the parameter at line 70 and references `systemd(1)` for full configuration semantics.

(Note: None of these omissions alter the four policy values or the null-key operational boundary; they do not amend the C1 claim).

## 5. Verdict
Verdict: SCOPE-AGREES
