import re
from collections import defaultdict

files = [
    r'D:\Users\svk6639\AppData\Local\Temp\claude\D--Users-svk6639-Documents-GitHub-Summer26Research-End-Milling\e28eee67-ccd4-4fc2-9963-0af8eb035ccf\tasks\bsgj81n6o.output',
    r'D:\Users\svk6639\AppData\Local\Temp\claude\D--Users-svk6639-Documents-GitHub-Summer26Research-End-Milling\e28eee67-ccd4-4fc2-9963-0af8eb035ccf\tasks\beh36j3ft.output'
]

results = []
current = {}

for fpath in files:
    with open(fpath, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            m = re.match(r'Target\s*:\s*(\S+)', line)
            if m:
                current = {'target': m.group(1)}
            m = re.match(r'Img dir\s*:\s*(\S+)', line)
            if m:
                current['img_dir'] = m.group(1)
            m = re.match(r'Arch\s*:\s*(\S+)\s+LR:\s*([\d.e-]+)', line)
            if m:
                current['arch'] = m.group(1)
                current['lr'] = m.group(2)
            m = re.match(r'Run-level majority vote acc:\s*([\d.]+)', line)
            if m:
                current['run_acc'] = float(m.group(1))
            if 'History saved to' in line:
                m = re.search(r'\\([^\\]+)_history\.json', line)
                if m:
                    current['tag'] = m.group(1)
                if 'run_acc' in current:
                    results.append(dict(current))
                current = {}

by_target = defaultdict(list)
for r in results:
    by_target[r.get('target', '?')].append(r)

for target in sorted(by_target.keys()):
    runs = by_target[target]
    best = max(runs, key=lambda x: x['run_acc'])
    print('=' * 60)
    print('TARGET: %s  (%d runs)' % (target, len(runs)))
    print('  BEST run-level acc : %.3f' % best['run_acc'])
    print('  Img dir : %s' % best.get('img_dir', '?'))
    print('  Arch    : %s' % best.get('arch', '?'))
    print('  LR      : %s' % best.get('lr', '?'))
    print('  Tag     : %s' % best.get('tag', '?'))
    top5 = sorted(runs, key=lambda x: x['run_acc'], reverse=True)[:5]
    print('  Top 5:')
    for r in top5:
        print('    %.3f  %-42s  %-20s  lr=%-8s  %s' % (
            r['run_acc'], r.get('img_dir', '?'), r.get('arch', '?'),
            r.get('lr', '?'), r.get('tag', '?')))
    print()
