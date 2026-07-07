"""
fix_diagrams.py
1. Updates astro.config.mjs to enable MDX
2. Updates package.json to add @astrojs/mdx dependency
Run from inside: C:\Users\mohan\abhishekmohantyhcmcloud\
"""
import os, re, xml.etree.ElementTree as ET, html as html_mod

# ── 1. Fix astro.config.mjs ──────────────────────────────────────────────
new_config = """import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://www.abhishekmohantyhcmcloud.com',
  integrations: [mdx()],
  markdown: {
    shikiConfig: {
      theme: 'one-dark-pro',
      wrap: true,
    },
  },
  build: {
    format: 'directory',
  },
});
"""

with open('astro.config.mjs', 'w', encoding='utf-8') as f:
    f.write(new_config)
print('✓ astro.config.mjs updated (MDX enabled)')

# ── 2. Fix package.json to add @astrojs/mdx ──────────────────────────────
import json
with open('package.json', 'r', encoding='utf-8') as f:
    pkg = json.load(f)

deps = pkg.get('dependencies', {})
if '@astrojs/mdx' not in deps:
    deps['@astrojs/mdx'] = '^3.0.0'
    pkg['dependencies'] = deps
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(pkg, f, indent=2)
    print('✓ package.json updated (@astrojs/mdx added)')
else:
    print('✓ package.json already has @astrojs/mdx')

# ── 3. Regenerate posts as .mdx with clean HTML ──────────────────────────
XML_PATH = 'blogpost.xml'
OUT_DIR  = 'src/content/posts'

def clean_html(raw):
    if not raw: return ''
    t = html_mod.unescape(raw)
    # Remove @import font URLs (not needed, Cloudflare blocks them anyway)
    t = re.sub(r'@import url\([^)]+\);?\s*', '', t)
    # Unwrap the outer max-width div - keep inner content
    t = re.sub(
        r'<div style="font-family:[^"]{0,200}max-width:\s*820px[^"]{0,200}">\s*',
        '<div class="blog-content">',
        t
    )
    # Fix any curly quotes that break MDX
    t = t.replace('\u2018', "'").replace('\u2019', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    # Remove MDX-breaking characters: curly braces in HTML text nodes
    # (only replace { } that are NOT inside HTML tags or attributes)
    def safe_replace_braces(text):
        result = []
        in_tag = False
        i = 0
        while i < len(text):
            c = text[i]
            if c == '<': in_tag = True
            elif c == '>': in_tag = False
            if not in_tag and c == '{':
                result.append('&#123;')
            elif not in_tag and c == '}':
                result.append('&#125;')
            else:
                result.append(c)
            i += 1
        return ''.join(result)
    t = safe_replace_braces(t)
    return t.strip()

def make_slug(title, url):
    m = re.search(r'/([^/]+)\.html$', url or '')
    if m:
        slug = m.group(1)
        slug = re.sub(r'_\d{8,}$', '', slug)
        return slug
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    return slug[:70].rstrip('-')

def infer_tags(title):
    t = title.lower()
    tags = ['Fast Formula', 'Oracle HCM Cloud']
    if 'hdl' in t or 'transformation' in t or 'wsa' in t: tags += ['HDL']
    if 'benefit' in t or 'periodization' in t or 'election' in t: tags += ['Benefits']
    if 'recruiting' in t or 'csp' in t: tags += ['Recruiting']
    if 'tcr' in t or 'time calculation' in t or 'ot bucket' in t or 'night' in t or 'day-type' in t or 'regular and ot' in t: tags += ['TCR','OTL','Time and Labor']
    if 'ter' in t or 'time entry rule' in t: tags += ['TER','Time Entry Rule','OTL']
    if 'absence' in t or 'get_plan_balance' in t: tags += ['Absence Management']
    if 'null' in t or 'defaulted' in t or 'isnull' in t or 'alias' in t: tags += ['Null Handling']
    if 'array' in t or 'dbi' in t or 'change_contexts' in t or 'get_context' in t: tags += ['DBI','CHANGE_CONTEXTS']
    if 'log' in t or 'debug' in t: tags += ['Debugging']
    seen = set(); out = []
    for tag in tags:
        if tag not in seen: seen.add(tag); out.append(tag)
    return out[:8]

def get_desc(title, content):
    text = re.sub(r'<[^>]+>', ' ', content)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    sents = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
    d = sents[0] if sents else title
    return re.sub(r'["\'{}\[\]]', '', d)[:200]

tree = ET.parse(XML_PATH)
root = tree.getroot()
NS = '{http://www.w3.org/2005/Atom}'

posts = []
for entry in root.findall(f'{NS}entry'):
    title_el   = entry.find(f'{NS}title')
    pub_el     = entry.find(f'{NS}published')
    content_el = entry.find(f'{NS}content')
    link_els   = entry.findall(f'{NS}link')
    if title_el is None or pub_el is None: continue
    title = (title_el.text or '').strip()
    if not title: continue
    url = next((l.get('href','') for l in link_els if l.get('rel')=='alternate'), '')
    if url and 'blogspot.com' not in url: continue
    if not url and not content_el: continue
    posts.append({
        'title':   title,
        'date':    pub_el.text[:10],
        'content': content_el.text if content_el is not None else '',
        'url':     url,
    })

posts.sort(key=lambda x: x['date'])
os.makedirs(OUT_DIR, exist_ok=True)

# Clear old posts
removed = 0
for f in os.listdir(OUT_DIR):
    if f.endswith(('.md', '.mdx')):
        os.remove(os.path.join(OUT_DIR, f))
        removed += 1
print(f'✓ Cleared {removed} old posts')

SLUG_REMAP = {
    'oracle-fast-formula-time-entry-rule':             'oracle-fast-formula-time-entry-rule-part-1',
    'oracle-fast-formula-time-entry-rule_01813668993': 'oracle-fast-formula-time-entry-rule-part-2',
    'oracle-fast-formula-time-entry-rule_01788502086': 'oracle-fast-formula-time-entry-rule-part-3',
    'oracle-fast-formula-time-entry-rule_01764150804': 'oracle-fast-formula-time-entry-rule-part-4',
}

written = 0
seen_slugs = set()
for p in posts:
    raw_slug = make_slug(p['title'], p['url'])
    slug = SLUG_REMAP.get(raw_slug, raw_slug)
    if slug in seen_slugs:
        slug = slug + '-' + p['date']
    seen_slugs.add(slug)

    content = clean_html(p['content'])
    title_safe = p['title'].replace('"', "'")
    desc = get_desc(p['title'], p['content'])
    tags = infer_tags(p['title'])
    tags_yaml = '[' + ', '.join(f'"{t}"' for t in tags) + ']'

    mdx  = f'---\ntitle: "{title_safe}"\n'
    mdx += f'description: "{desc}"\n'
    mdx += f'pubDate: {p["date"]}\n'
    mdx += f'tags: {tags_yaml}\n'
    mdx += f'---\n\n'
    mdx += content

    path = os.path.join(OUT_DIR, slug + '.mdx')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(mdx)
    print(f'  wrote: {slug}.mdx')
    written += 1

print(f'\n{"="*52}')
print(f'  Written : {written} MDX files with HTML diagrams')
print(f'{"="*52}')
print('\nNEXT STEPS (run one by one):')
print('  npm install')
print('  git add .')
print('  git commit -m "Enable MDX + restore all diagrams"')
print('  git push')
