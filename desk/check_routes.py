import os
import re

routes = ['market', 'cvd', 'bookwalls', 'liqlevels', 'options', 'signals', 'narrative', 'largeorder', 'oi']
for r in routes:
    p = os.path.join('src', 'app', 'api', 'cg', r, 'route.ts')
    if os.path.exists(p):
        with open(p, 'r') as f:
            txt = f.read()
            m = re.findall(r'get\(["\'](sym|symbol)["\']\)', txt)
            print(f"{r:12} expects: {set(m)}")
