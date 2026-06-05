import json

with open('site/data/index.json', encoding='utf-8') as f:
    d = json.load(f)

print('keys:', list(d.keys()))
print('weekly_dates count:', len(d.get('weekly_dates', [])))
print('dates count:', len(d.get('dates', [])))
