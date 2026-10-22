def m_snapshot_dotdot_inside_tree(files, rows):
    r = row(rows, 'D01')
    original = r['snapshot']
    r['snapshot'] = EV + '/../' + original.rsplit('/', 1)[-1]
    files[r['snapshot']] = files[original]


def m_quote_outside_cited_window(files, rows):
    r = row(rows, 'D01')
    lines = files[r['snapshot']].splitlines()
    lines[2] = 'x' * 256
    files[r['snapshot']] = '\n'.join(lines) + '\n'
    r['line'] = 3


def m_capture_outside_prefix(files, rows):
    r = row(rows, 'D08')
    original = r['capture']
    r['capture'] = 'corpus/capture-outside-prefix.txt'
    files[r['capture']] = files[original]


def m_capture_dotdot_inside_tree(files, rows):
    r = row(rows, 'D08')
    original = r['capture']
    r['capture'] = EV + '/../' + original.rsplit('/', 1)[-1]
    files[r['capture']] = files[original]


SHOULD_FAIL += [
    ('F47-snapshot-dotdot-resolves-inside-tree', 'D01', m_snapshot_dotdot_inside_tree),
    ('F48-quote-exists-outside-cited-window', 'D01', m_quote_outside_cited_window),
    ('F49-capture-outside-evidence-prefix', 'D08', m_capture_outside_prefix),
    ('F50-capture-dotdot-resolves-inside-tree', 'D08', m_capture_dotdot_inside_tree),
]
