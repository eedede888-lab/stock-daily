import json, os

path = r'C:\Users\羞羞的家\Desktop\stock-daily-test2\site\data\index.json'
with open(path, encoding='utf-8') as f:
    idx = json.load(f)

idx['weekly_dates'] = [w for w in idx.get('weekly_dates', []) if w.get('stocks')]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(idx, f, ensure_ascii=False, indent=2)

print('清除完成，remaining:', [w['wkey'] for w in idx['weekly_dates']])