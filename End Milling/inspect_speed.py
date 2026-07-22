import re
from collections import defaultdict

files = [
    r'D:\Users\svk6639\AppData\Local\Temp\claude\D--Users-svk6639-Documents-GitHub-Summer26Research-End-Milling\e28eee67-ccd4-4fc2-9963-0af8eb035ccf\tasks\bsgj81n6o.output',
    r'D:\Users\svk6639\AppData\Local\Temp\claude\D--Users-svk6639-Documents-GitHub-Summer26Research-End-Milling\e28eee67-ccd4-4fc2-9963-0af8eb035ccf\tasks\beh36j3ft.output'
]

# Collect all speed runs with full per-class info
results = []
current = {}
in_report = False
report_lines = []

for fpath in files:
    with open(fpath, encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            m = re.match(r'Target\s*:\s*(\S+)', s)
            if m:
                current = {'target': m.group(1)}
                in_report = False
                report_lines = []
            m = re.match(r'Img dir\s*:\s*(\S+)', s)
            if m: current['img_dir'] = m.group(1)
            m = re.match(r'Arch\s*:\s*(\S+)\s+LR:\s*([\d.e-]+)', s)
            if m: current['arch'] = m.group(1); current['lr'] = m.group(2)
            m = re.match(r'Best window-level test acc\s*:\s*([\d.]+)', s)
            if m: current['win_acc'] = float(m.group(1))
            m = re.match(r'Run-level majority vote acc:\s*([\d.]+)', s)
            if m: current['run_acc'] = float(m.group(1))
            if 'Per-class report' in s:
                in_report = True
                report_lines = []
            if in_report:
                report_lines.append(line)
                if 'weighted avg' in s:
                    in_report = False
                    current['report'] = ''.join(report_lines)
            if 'History saved to' in s:
                m2 = re.search(r'\\([^\\]+)_history\.json', s)
                if m2: current['tag'] = m2.group(1)
                if 'run_acc' in current:
                    results.append(dict(current))
                current = {}

# All speed runs sorted by run_acc
speed = [r for r in results if r.get('target') == 'speed']
speed.sort(key=lambda x: x['run_acc'], reverse=True)

print('All speed runs (%d total), sorted by run-level acc:' % len(speed))
print('%-8s  %-8s  %-42s  %-20s  %-8s  %s' % ('RUN_ACC','WIN_ACC','IMG_DIR','ARCH','LR','TAG'))
print('-'*140)
for r in speed:
    print('%-8s  %-8s  %-42s  %-20s  %-8s  %s' % (
        '%.1f%%' % (r['run_acc']*100),
        '%.1f%%' % (r.get('win_acc',0)*100),
        r.get('img_dir','?'),
        r.get('arch','?'),
        r.get('lr','?'),
        r.get('tag','?')))

# Print per-class report for the best
print('\n\n=== PER-CLASS REPORT FOR BEST SPEED MODEL ===')
print(speed[0].get('report','not found'))
