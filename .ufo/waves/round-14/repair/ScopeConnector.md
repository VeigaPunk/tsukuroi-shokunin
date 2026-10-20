# ScopeConnector — Grounded QUALITY Rule Connecting Value-Domain & Source-Attribution

## 1. Concrete Loci of the Round-13 Defects

Outside review reference: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13-verifier-spotcheck.md`
Prior lane lesson: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13.md`
Active defect entries:
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:97`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:47` (row `S042`)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:24` (criterion 18)

### Locus A: Value-Domain Overclaim (MD:97)
- **Defective text:** `corpus/knowledge/root-dac-correction-r13.md:97` states: "among `ProtectSystem=` values, `strict` is the only value that covers the hierarchy (S041); the value set is not exhaustive".
- **Primary source truth:** `systemd.exec(5)` (S041 / S044) defines `ProtectSystem=` strictly as taking a boolean argument (`true`/`false`, `yes`/`no`, `1`/`0`, `on`/`off`) or the special values `"full"` or `"strict"`. The option's value domain is closed and finite.
- **Root failure:** The author intended to express that the set of *unit-side filesystem isolation mechanisms* is non-exhaustive, but erroneously attached non-exhaustiveness to the *option's value set*.

### Locus B: Source-Attribution Transference (S042 & QUALITY #18)
- **Defective text:** `corpus/SOURCES.md` S042 `teaches` and `corpus/lessons/round-13.md` describe issue #8047 comment 6071740243 as "self-described model-generated automated triage by `omarchybot`". Furthermore, `QUALITY.md` criterion 18 mandated: "record bot comments as automated community triage, never maintainer acceptance."
- **Primary source truth:** The actual comment on #8047 says: "I tried this on a stock Omarchy worker VM" and refers to Codex Medium as a "second opinion"; it does not self-describe as model-generated triage. The phrase "Nothing was run on a machine" belongs exclusively to #6629 comment 6234472369.
- **Root failure:** The lane transferred an attribute from #6629 to #8047 because both shared the GitHub handle `omarchybot`. The lane conflated account identity (`login: omarchybot`, `type: User`, `author_association: COLLABORATOR`) and external model mentions with an explicit first-party disclaimer.

---

## 2. The Unifying Structural Pattern

Both defects stem from **cross-boundary attribute transference**:
1. In the **value-domain mistake**, open-endedness from the *surrounding problem space* (unit sandboxing directives) was projected onto a *closed semantic domain* (an individual directive's parsed value set).
2. In the **source-attribution mistake**, characteristics from an *external instance* (#6629's model disclaimer) were projected onto a *distinct source entity* (#8047's comment) based on an incidental shared handle (`omarchybot`), overgeneralizing triage role across discrete records.

In this lane (host diagnosis and root-DAC triage), precise negative discrimination is vital. Overclaiming non-exhaustiveness creates false uncertainty about well-defined configuration keys; overclaiming automated provenance creates false certainty about third-party claims.

---

## 3. Grounded Reusable QUALITY Rule (Proposed QUALITY #19)

```markdown
19. Every source-scoped property domain and attribution statement must be strictly bounded to the primary text of the exact entity cited:
    - Distinguish the closed value domain of a specific directive (as defined by its syntax/grammar man-page) from the open-ended set of alternative mechanisms across the system; do not assert an option's value set is non-exhaustive when alternatives belong to separate directives.
    - Attribute statements only from verbatim clauses within the specific source locus; do not transfer disclaimers, tooling notices, or generation models across different comments, commits, or issue threads, regardless of shared account handles or bot suffixes.
    - In community issue triage, separate verified API fields (user type, author association) from unverified factual claims in the body, secondary opinions, and maintainer decisions.
```

---

## 4. Concrete Recommendations for Round 14

1. **R14-VALUE-DOMAIN Repair:**
   - In `corpus/knowledge/source-scope-correction-r14.md` and `.json`, cite S044 (`systemd.exec(5)`).
   - Clarify that `ProtectSystem=` accepts boolean or `"full"` / `"strict"`.
   - Anchor non-exhaustiveness strictly to unit-side mount/sandbox mechanisms (`BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, `RootImage=`).

2. **R14-COMMENT-ATTRIBUTION Repair:**
   - In `corpus/SOURCES.md`, append S045 superseding S042.
   - Accurately record S045 attributes: GitHub API user `omarchybot` (`type: User`, `association: COLLABORATOR`), unverified VM test claim, Codex Medium cited as second opinion, deferral to maintainer.
   - Retain rejection of host-cause/maintainer authority without alleging a non-existent self-description.

3. **Update `corpus/QUALITY.md`:**
   - Qualify criterion 18 so it no longer forces blanket attribution of community comments as "automated triage".
   - Adopt criterion 19 as formulated above.

---

## 5. Tooling Record

- Tools installed/updated: None. Standard read tools used within lane bounds.
- Limitations: Report-only leaf member; no verification commands or modifications outside `.ufo/waves/round-14/repair/ScopeConnector.md`.
