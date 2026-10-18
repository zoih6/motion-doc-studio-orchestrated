#!/usr/bin/env python3
"""Wikimedia Commons: search + download REAL high-res, license-checked images.
  python3 tools/commons.py search "thuluth calligraphy panel" [30]
  python3 tools/commons.py get "File:Some name.jpg" assets/real/name.jpg [2560]
Prints size + license + artist; appends credits to docs/CREDITS.md on download.
Rules: prefer PD / CC0 / CC BY / CC BY-SA (credit them). Use Special:FilePath?width=N (arbitrary thumb
URLs like /2400px- often return 2 KB error files). Check the file is > 50 KB after download."""
import sys, json, urllib.request, urllib.parse, os, re
API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'motion-doc-studio/1.0 (documentary research)'}
def q(params):
    url = API + '?' + urllib.parse.urlencode({**params, 'format': 'json'})
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
def info(titles):
    d = q({'action': 'query', 'titles': '|'.join(titles), 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata'})
    for p in d['query']['pages'].values():
        ii = (p.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
        g = lambda k: re.sub('<[^>]+>', '', md.get(k, {}).get('value', ''))[:80]
        yield p['title'], ii.get('width'), ii.get('height'), g('LicenseShortName'), g('Artist'), ii.get('url')
if sys.argv[1] == 'search':
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    d = q({'action': 'query', 'list': 'search', 'srnamespace': 6, 'srlimit': n, 'srsearch': sys.argv[2]})
    titles = [r['title'] for r in d['query']['search']]
    for i in range(0, len(titles), 40):
        for t, w, h, lic, art, url in info(titles[i:i + 40]): print(f'{w}x{h}\t{lic}\t{t}\t{art}')
elif sys.argv[1] == 'get':
    title, dst = sys.argv[2], sys.argv[3]; width = sys.argv[4] if len(sys.argv) > 4 else '2560'
    name = title.replace('File:', '')
    url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(name)}?width={width}'
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
    if len(data) < 50000: sys.exit(f'suspiciously small ({len(data)} B) — try another width or the original URL')
    open(dst, 'wb').write(data)
    t, w, h, lic, art, src = next(info([title]))
    os.makedirs('docs', exist_ok=True)
    with open('docs/CREDITS.md', 'a') as f: f.write(f'- `{dst}` ← [{name}](https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}) · {lic} · {art}\n')
    print(f'saved {dst} ({len(data)//1024} KB) · {lic} · {art}')
