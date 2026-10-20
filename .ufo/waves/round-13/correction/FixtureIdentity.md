# FixtureIdentity — Round 13 Scoped Findings

## Axes
- **Depth**: Ground exact caller-owned fixture execution vs hypothetical root-owned inference distinction across r12 SC1/SC2 and committed smoke evidence.

## 1. Observed Evidence & Discrepancy

### 1.1 Round 12 JSON Specifications (`corpus/knowledge/root-dac-decision-r12.json`)
- **SC1 declaration** (lines 179–192):
  - Declared input parent: `"0555 root:root, base ACL entries only"`
  - Declared caller: `"uid 1000 (no capabilities)"`
  - Declared basis: `"actual isolated ordinary mkdir (uid 1000): parent 0555 + new target -> EACCES, .ufo/waves/round-12/discriminator-smoke.json fixture_results[0]; mkdir(2) EACCES (S035)"`
- **SC2 declaration** (lines 193–206):
  - Declared input parent: `"0555 root:root, base ACL entries only"`
  - Declared caller: `"uid 1000 (no capabilities)"`
  - Declared basis: `"actual isolated ordinary mkdir: parent 0555 + existing target -> EEXIST, .ufo/waves/round-12/error-order-smoke.json; mkdir(2) EEXIST (S035)"`

### 1.2 Committed Historical Smoke Evidence
- **`discriminator-smoke.json`**:
  - `uid`: 1000
  - `fixture_scope`: `"new isolated temporary directory; removed; no host root writes"`
  - `fixture_code`: `"TemporaryDirectory; chmod(parent,0555); mkdir(child); chmod(parent,0755); mkdir(child); mkdir(existing_child)"`
  - Result: `fixture_results[0]` = `{ "mode": "0555", "result": "EACCES", "errno": 13 }`
- **`error-order-smoke.json`**:
  - `uid`: 1000
  - `fixture_scope`: `"isolated disposable temporary directory; restored ownerwrite for cleanup"`
  - Result: `parent_mode: "0555", target: "existing", result: "EEXIST"`

### 1.3 Verifier Defect Ruling (`corpus/lessons/round-12-verifier-spotcheck.md` §Routed defects 4)
- Verifier noted:
  > "tsukuroi / evidence precision: SC1/SC2 specify root-owned hypothetical inputs but cite caller-owned smoke controls as their actual basis; distinguish the inferred same-mode outcome from executed fixture identity."

## 2. Distinction: Executed Fixture Identity vs Inferred Hypothetical

| Dimension | Executed Fixture Identity (Empirical Fact) | Hypothetical Root-Owned Scenario (Inference / Prediction) |
|---|---|---|
| **Parent Inode Owner** | `uid 1000` (`vgpnk`), unprivileged user | `uid 0` (`root:root`) |
| **Creation Context** | Python `tempfile.TemporaryDirectory()` created by runner process (uid 1000) | System root directory `/` or root-owned subtree |
| **Parent Permissions** | `0555` (`r-xr-xr-x`), owned by uid 1000 | `0555` (`r-xr-xr-x`), owned by root |
| **Caller Relation** | Caller (uid 1000) is the **owner** of the directory, operating under missing owner-write bit (`w=0`) | Caller (uid 1000) is a **non-owner (other)**, operating under other read/search (`o=r-x`, missing other-write `w=0`) |
| **DAC Check Path (S035)** | Fails owner-write permission check in kernel VFS DAC path | Fails other-write permission check in kernel VFS DAC path |
| **Authority Category** | Direct empirical measurement (`[obs]`) in temporary fixture | Source-grounded derivation (`[inf]`) via S035 (`mkdir(2)`) |

## 3. Required Correction Specification for Round 13

1. **SC1/SC2 Scenario Framing**:
   - Explicitly label SC1 and SC2 as **hypothetical/predicted root-owned scenarios** evaluated under S035 DAC rules for non-owner caller (uid 1000).
   - In the `basis` field, clearly distinguish:
     1. The **executed fixture control** (`discriminator-smoke.json` and `error-order-smoke.json`) was executed against an **invoker-owned (`uid 1000`) 0555 parent** where the owner-write bit was absent.
     2. The **root-owned 0555 outcome** is an **inferred prediction**: mode `0555 root:root` grants write to neither owner, group, nor other; non-owner uid 1000 falls to other `r-x`, yielding identical `EACCES` (new target) and `EEXIST` (existing target) outcomes under ordinary `mkdir` ordering.
2. **Quality & Evidence Separation**:
   - Do not claim that caller-owned temporary directory execution constitutes empirical demonstration of a root-owned parent.
   - Sibling note `corpus/knowledge/root-dac-correction-r13.md` and `.json` must preserve this explicit boundary between executed caller-owned controls and inferred root-owned predictions.

## 4. Tooling & Environment
- No tools installed or upgraded. Tooling requirements satisfied by standard environment.
