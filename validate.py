"""Meaningful checks for calendar boundaries, completeness, and local links."""
from collections import Counter
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from materials import MATERIALS

ROOT = Path(__file__).resolve().parent / 'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.ids=set(); self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('href','src'):
            if key in a: self.links.append(a[key])

assert len(MATERIALS)==24
assert len({m['id'] for m in MATERIALS})==24
counts=Counter((m['category'],m['semester']) for m in MATERIALS)
assert counts=={('systems',1):4,('code',2):4,('training',1):4,('training',2):4,('production',1):4,('production',2):4},counts
for m in MATERIALS:
    d=date.fromisoformat(m['date'])
    start,end=(date(2025,9,1),date(2025,12,31)) if m['semester']==1 else (date(2026,1,12),date(2026,7,31))
    assert start+timedelta(days=12)<=d<=end-timedelta(days=12),(m['id'],d)
    if m['category'] in ('training','production'):
        assert d.month in ((11,12) if m['semester']==1 else (6,7))
    assert len(m['steps'])==6 and len(m['questions'])==3
    assert (ROOT/'materials'/f'{m["id"]}.html').is_file()
    assert (ROOT/'downloads'/f'{m["id"]}.md').stat().st_size>2000

pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html')}
for path,page in pages.items():
    for value in page.links:
        url=urlsplit(value)
        if url.scheme or url.netloc: continue
        if url.path=='/metodichka/': target=ROOT/'index.html'
        else: target=(path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.is_file(),(path,value,target)
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids,(path,value)
    text=path.read_text()
    assert 'lang="ru"' in text
    assert '<main id="main"' in text
    assert date.today().isoformat() not in text
    assert 'new Date(' not in text
print(f'PASS: 24 materials; 6 groups of 4; all dates; {len(pages)} pages and all local links.')
