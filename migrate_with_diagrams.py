"""
migrate_with_diagrams.py
Converts Blogger XML posts to .mdx files, preserving all HTML diagrams/SVGs intact.
"""
import xml.etree.ElementTree as ET
import re, os, html as html_mod

XML_PATH = 'blogpost.xml'
OUT_DIR  = 'src/content/posts'

def clean_content(raw):
    """Keep full HTML but strip only Google fonts imports and inline style resets."""
    if not raw: return ''
    t = html_mod.unescape(raw)
    # Remove @import font lines (not needed, site loads fonts globally)
    t = re.sub(r'@import url\([^)]+\);?\s*', '', t)
    # Remove wrapping outer div that sets font-family (site CSS handles it)
    t = re.sub(r'<div style="font-family:[^"]*;[^"]*max-width:\s*820px[^"]*">', '<div class="post-html">', t)
    # Clean up excessive whitespace between tags
    t = re.sub(r'\n{3,}', '\n\n', t)
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

def get_description(title, content):
    """Extract first real text paragraph for description."""
    text = re.sub(r'<[^>]+>', ' ', content)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
    desc = sentences[0] if sentences else title
    return re.sub(r'["\']', '', desc)[:200]

# Parse XML
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

# Remove old .md posts and recreate as .mdx
os.makedirs(OUT_DIR, exist_ok=True)

# Remove existing migrated posts
for f in os.listdir(OUT_DIR):
    if f.endswith('.md') or f.endswith('.mdx'):
        # Only remove ones we generated (keep manually written ones)
        path = os.path.join(OUT_DIR, f)
        os.remove(path)
        
print(f'Cleared {OUT_DIR}')

SLUG_REMAP = {
    'oracle-fast-formula-time-entry-rule':              'oracle-fast-formula-time-entry-rule-part-1',
    'oracle-fast-formula-time-entry-rule_01813668993':  'oracle-fast-formula-time-entry-rule-part-2',
    'oracle-fast-formula-time-entry-rule_01788502086':  'oracle-fast-formula-time-entry-rule-part-3',
    'oracle-fast-formula-time-entry-rule_01764150804':  'oracle-fast-formula-time-entry-rule-part-4',
}

written = 0
seen_slugs = set()

for p in posts:
    raw_slug = make_slug(p['title'], p['url'])
    slug = SLUG_REMAP.get(raw_slug, raw_slug)
    if slug in seen_slugs:
        slug = slug + '-' + p['date']
    seen_slugs.add(slug)

    content = clean_content(p['content'])
    title_safe = p['title'].replace('"', "'")
    desc = get_description(p['title'], p['content'])
    tags = infer_tags(p['title'])
    tags_yaml = '[' + ', '.join(f'"{t}"' for t in tags) + ']'

    # MDX frontmatter + raw HTML body (MDX renders HTML natively)
    mdx  = f'---\n'
    mdx += f'title: "{title_safe}"\n'
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

print(f'\n{"="*50}')
print(f'  Written : {written} MDX files with full HTML diagrams')
print(f'{"="*50}')
print('\nNEXT STEPS:')
print('  git add src/content/posts/')
print('  git commit -m "Restore full HTML diagrams in all posts"')
print('  git push')
