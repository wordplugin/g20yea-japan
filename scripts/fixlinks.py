import os, re, sys, json, urllib.parse
root = sys.argv[1]; idmap = json.load(open(sys.argv[2]))
for d, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f); rel = os.path.relpath(p, root)
        pre = '../' * rel.count('/')
        s = open(p, encoding='utf-8').read(); o = s
        def fix(m):
            pid, frag = m.group(1), m.group(2) or ''
            slug = idmap.get(pid)
            target = pre + (slug + '/' if slug else '') + 'index.html'
            # same-page anchor
            if os.path.normpath(os.path.join(os.path.dirname(rel), target)) == rel and frag: return f'href="{frag}"'
            return f'href="{target}{frag}"'
        s = re.sub(r'href="(?:\.\./)*index\.html%3Fp=(\d+)\.html(#[^"]*)?"', fix, s)
        s = re.sub(r'url\((?:\.\./)*wp-content/plugins/vk-all-in-one-expansion-unit/assets/images/to-top-btn-icon\.svg\)',
                   'url(../../plugins/vk-all-in-one-expansion-unit/assets/images/to-top-btn-icon.svg)', s)
        if s != o: open(p, 'w', encoding='utf-8').write(s)
