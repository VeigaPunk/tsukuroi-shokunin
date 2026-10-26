"""Build the proposed missing control E7-opened-stale: the E6 candidate entry
verbatim, but in SOURCES.md the `opened` cell of every row the entry cites
(S208, S213-S218) is 2026-10-25 instead of 2026-10-26, so the counter's
opened-date term is the only failing source_ok conjunct."""
import pathlib, re, sys
src = pathlib.Path(sys.argv[1]).read_text()
ids = {'S208', 'S213', 'S214', 'S215', 'S216', 'S217', 'S218'}
out, changed = [], 0
for line in src.splitlines():
    m = re.match(r'^\| (S\d{3,}) \|', line)
    if m and m.group(1) in ids:
        parts = line.split('|')
        assert parts[9].strip() == '2026-10-26', (m.group(1), parts[9])
        parts[9] = parts[9].replace('2026-10-26', '2026-10-25')
        line = '|'.join(parts)
        changed += 1
    out.append(line)
assert changed == 7, f'expected 7 cited rows, changed {changed}'
pathlib.Path(sys.argv[2]).write_text('\n'.join(out) + '\n')
print(f'E7 SOURCES.md written, {changed} opened cells flipped')
