import xml.etree.ElementTree as ET
import re, os, html as html_mod

XML_PATH = r'C:\Users\mohan\Downloads\blogpost.xml'
OUT_DIR  = r'src\content\posts'

# ── HTML → Markdown (stdlib only, no pip) ──────────────────────────────────
def html_to_md(raw):
    if not raw: return ''
    t = html_mod.unescape(raw)
    # remove style/script
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL|re.I)
    t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL|re.I)
    # headings
    for n in range(6,0,-1):
        t = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', lambda m,n=n: '\n'+'#'*n+' '+_strip(m.group(1))+'\n', t, flags=re.I|re.DOTALL)
    # code blocks
    t = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', lambda m: '\n```\n'+html_mod.unescape(re.sub('<[^>]+>','',m.group(1)))+'\n```\n', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<pre[^>]*>(.*?)</pre>', lambda m: '\n```\n'+html_mod.unescape(re.sub('<[^>]+>','',m.group(1)))+'\n```\n', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<code[^>]*>(.*?)</code>', lambda m: '`'+_strip(m.group(1))+'`', t, flags=re.I|re.DOTALL)
    # bold/italic
    t = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', lambda m: '**'+_strip(m.group(2))+'**', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', lambda m: '*'+_strip(m.group(2))+'*', t, flags=re.I|re.DOTALL)
    # links
    t = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', lambda m: '['+_strip(m.group(2))+']('+m.group(1)+')', t, flags=re.I|re.DOTALL)
    # lists
    t = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '- '+_strip(m.group(1))+'\n', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<[uo]l[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</[uo]l>', '\n', t, flags=re.I)
    # tables - basic
    t = re.sub(r'<th[^>]*>(.*?)</th>', lambda m: '| '+_strip(m.group(1))+' ', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<td[^>]*>(.*?)</td>', lambda m: '| '+_strip(m.group(1))+' ', t, flags=re.I|re.DOTALL)
    t = re.sub(r'</tr>', '|\n', t, flags=re.I)
    t = re.sub(r'<tr[^>]*>', '', t, flags=re.I)
    t = re.sub(r'<t(?:head|body|foot)[^>]*>|</t(?:head|body|foot)>', '', t, flags=re.I)
    t = re.sub(r'<table[^>]*>|</table>', '\n', t, flags=re.I)
    # blockquote
    t = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> '+_strip(m.group(1)).replace('\n','\n> ')+'\n', t, flags=re.I|re.DOTALL)
    # paragraphs and breaks
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'<p[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</p>', '\n', t, flags=re.I)
    t = re.sub(r'<div[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</div>', '\n', t, flags=re.I)
    # strip all remaining tags
    t = re.sub(r'<[^>]+>', '', t)
    # clean up
    t = re.sub(r'\n{4,}', '\n\n\n', t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    return t.strip()

def _strip(s):
    return re.sub(r'<[^>]+>', '', s).strip()

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

# ── Parse XML ──────────────────────────────────────────────────────────────
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
    # skip non-post entries (settings, templates etc) by checking URL pattern
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

# TER part slug fixes
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

    body = html_to_md(p['content'])
    title_safe = p['title'].replace('"',"'")
    lines = [l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#') and len(l.strip())>40]
    desc = re.sub(r'[`*_\[\]\\|]','', lines[0] if lines else title_safe)[:200].replace('"',"'")
    tags = infer_tags(p['title'])
    tags_yaml = '[' + ', '.join(f'"{t}"' for t in tags) + ']'

    fm  = f'---\n'
    fm += f'title: "{title_safe}"\n'
    fm += f'description: "{desc}"\n'
    fm += f'pubDate: {p["date"]}\n'
    fm += f'tags: {tags_yaml}\n'
    fm += f'---\n\n'

    path = os.path.join(OUT_DIR, slug + '.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fm + body)
    print(f'  wrote: {slug}.md')
    written += 1

print(f'\n{"="*48}')
print(f'  Written : {written}')
print(f'{"="*48}')
print('\nNEXT STEPS:')
print('  git add src/content/posts/')
print('  git commit -m "Add all Blogger posts"')
print('  git push')
