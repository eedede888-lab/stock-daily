import json, os

wdir = r'C:\Users\羞羞的家\Desktop\stock-daily-test2\site\data\weekly\20260529-0604'

for fn in sorted(os.listdir(wdir)):
    if not fn.endswith('.json') or fn.endswith('_vol.json'):
        continue
    code = fn[:-5]
    path = os.path.join(wdir, fn)
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    print(f'{code}: name={repr(d.get("name"))}')