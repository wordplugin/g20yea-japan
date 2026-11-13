import os, re, sys
from urllib.parse import quote
root = sys.argv[1]
os.chdir(root)

TEXT_EXT = ('.html', '.css', '.js')
def is_text(p): return p.endswith(TEXT_EXT) or '.css' in os.path.basename(p) or '.js' in os.path.basename(p)

# 1) rename files containing '?'
renames = {}
for d, _, fs in os.walk('.'):
    for f in fs:
        if '?' not in f: continue
        base, q = f.split('?', 1)
        stem, ext = os.path.splitext(base)
        if ext == '.php':
            ext = '.css' if q.endswith('.css') else '.js'
            if q.endswith('.css'): q = q[:-4]
        q = re.sub(r'[^A-Za-z0-9._-]', '-', q).strip('-.')
        new = f"{stem}{('-' + q) if q else ''}{ext}"
        renames[f] = new
        os.rename(os.path.join(d, f), os.path.join(d, new))
print(len(renames), 'renamed')

# reference forms: wget writes '?' as '%3F'
pairs = []
for old, new in renames.items():
    for o in {old.replace('?', '%3F'), old}:
        pairs.append((o, new))
pairs.sort(key=lambda x: -len(x[0]))

HEAD_JUNK = re.compile(r'\s*<link[^>]+(?:EditURI|xmlrpc|wp-json|/feed/|oembed|rel=["\']shortlink["\']|rel=["\']alternate["\'][^>]*application/(?:rss|json))[^>]*>', re.I)
RESPOND = re.compile(r'<div id="respond".*?</form>\s*</div>(?:<!--\s*#respond\s*-->)?', re.S)

def rel_prefix(path):
    depth = path.count('/') - 1  # './a/b/index.html' -> 2
    return '../' * depth

for d, _, fs in os.walk('.'):
    for f in fs:
        p = os.path.join(d, f)
        if not is_text(p): continue
        try: s = open(p, encoding='utf-8').read()
        except UnicodeDecodeError: continue
        o = s
        for a, b in pairs:
            if a in s: s = s.replace(a, b)
        if p.endswith('.html'):
            s = HEAD_JUNK.sub('', s)
            s = RESPOND.sub('', s)
            pre = rel_prefix(p)
            # absolute internal links -> relative (keep canonical/og absolute)
            def fix(m):
                attr, path = m.group(1), m.group(2)
                path = path.split('#')[0]
                if path == '' or path.endswith('/'): path += 'index.html'
                return f'{attr}="{pre}{path}"'
            s = re.sub(r'(href|src)="https?://g20yea\.jp/([^"]*)"', fix, s)
        if s != o:
            open(p, 'w', encoding='utf-8').write(s)
