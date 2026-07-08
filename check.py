import os
total_market = 0
for root, dirs, files in os.walk('site/data'):
    for f in files:
        if f == 'market.js':
            p = os.path.join(root, f)
            s = os.path.getsize(p)
            total_market += s
            print(f'{s/1e6:.1f}MB  {p}')
print(f'market.js 合計: {total_market/1e6:.1f}MB')