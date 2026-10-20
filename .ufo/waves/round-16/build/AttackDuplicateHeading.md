# AttackDuplicateHeading — R16 critic

Implementation absent: no errata JSON or check-section-citations.py yet. Static `git show db68e62` reads only; nothing run.

Baseline: no duplicate headings in host-health-r3, update-safety-v3 or -v2. Each target heading and row_key appears once in its file.

Falsifiers:
1. Sibling file: v2:244 `## 7. Risk-ordered install recommendation table…` holds the same `| 1 | Do nothing now |` (v2:253). Its notice v2:372 "§7 rank 1" is correct. Searching the corpus by row_key, heading prefix or "§7 rank 1" finds two hits. Bind each record to its path; the only wrong citation is v3:398.
2. "v2 §7" at v3:210 and v3:366 is valid. "§1" (hh:581) points to a real heading, hh:65, that has no row 5. Check the row sits in the section, not that the heading exists.
3. The code block at hh:482–513 has `# update-safety` lines. Match exact heading lines outside code fences; require exactly one. End the section at the next same-or-higher heading (hh 23–64, v3 208–228).
4. R15 used one heading in four files. Name notices by record ID; require one per path.
