"""
revert_to_md.py
Converts all .mdx files back to .md files with safe markdown content.
Strips problematic HTML that breaks MDX but keeps text content.
Run from: C:\Users\mohan\abhishekmohantyhcmcloud\
"""
import os, re, xml.etree.ElementTree as ET, html as html_mod

XML_PATH = 'blogpost.xml'
OUT_DIR  = 'src/content/posts'

def html_to_safe_md(raw):
    """Convert HTML to markdown, preserving code blocks and text."""
    if not raw: return ''
    t = html_mod.unescape(raw)
    # Remove style/script blocks
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL|re.I)
    t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL|re.I)
    # Remove HTML comments
    t = re.sub(r'<!--.*?-->', '', t, flags=re.DOTALL)
    # Convert headings
    for n in range(6,0,-1):
        t = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', 
                   lambda m,n=n: '\n'+'#'*n+' '+strip_tags(m.group(1))+'\n', 
                   t, flags=re.I|re.DOTALL)
    # Convert code blocks FIRST (before other conversions)
    t = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',
               lambda m: '\n```\n'+html_mod.unescape(strip_tags(m.group(1)))+'\n```\n',
               t, flags=re.I|re.DOTALL)
    t = re.sub(r'<pre[^>]*>(.*?)</pre>',
               lambda m: '\n```\n'+html_mod.unescape(strip_tags(m.group(1)))+'\n```\n',
               t, flags=re.I|re.DOTALL)
    # Inline code
    t = re.sub(r'<code[^>]*>(.*?)</code>',
               lambda m: '`'+strip_tags(m.group(1))+'`',
               t, flags=re.I|re.DOTALL)
    # Bold/italic
    t = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>',
               lambda m: '**'+strip_tags(m.group(2))+'**',
               t, flags=re.I|re.DOTALL)
    t = re.sub(r'<(em|i)[^>]*>(.*?)</\1>',
               lambda m: '*'+strip_tags(m.group(2))+'*',
               t, flags=re.I|re.DOTALL)
    # Links
    t = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
               lambda m: '['+strip_tags(m.group(2))+']('+m.group(1)+')',
               t, flags=re.I|re.DOTALL)
    # List items
    t = re.sub(r'<li[^>]*>(.*?)</li>',
               lambda m: '\n- '+strip_tags(m.group(1)),
               t, flags=re.I|re.DOTALL)
    t = re.sub(r'<[uo]l[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</[uo]l>', '\n', t, flags=re.I)
    # Tables
    t = re.sub(r'<th[^>]*>(.*?)</th>', lambda m: '| '+strip_tags(m.group(1))+' ', t, flags=re.I|re.DOTALL)
    t = re.sub(r'<td[^>]*>(.*?)</td>', lambda m: '| '+strip_tags(m.group(1))+' ', t, flags=re.I|re.DOTALL)
    t = re.sub(r'</tr>', '|\n', t, flags=re.I)
    t = re.sub(r'<tr[^>]*>', '', t, flags=re.I)
    t = re.sub(r'</?t(?:head|body|foot|able)[^>]*>', '\n', t, flags=re.I)
    # Blockquote
    t = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>',
               lambda m: '\n> '+strip_tags(m.group(1)).replace('\n','\n> ')+'\n',
               t, flags=re.I|re.DOTALL)
    # Paragraphs and divs → newlines
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'</?p[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</?div[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'</?span[^>]*>', '', t, flags=re.I)
    t = re.sub(r'<hr[^>]*/?>', '\n---\n', t, flags=re.I)
    # Strip ALL remaining tags
    t = strip_tags(t)
    # Clean whitespace
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{4,}', '\n\n\n', t)
    t = t.strip()
    return t

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)

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
    return re.sub(r'["\'{}\[\]\\]', '', d)[:200]

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
os.makedirs(OUT_DIR, exist_ok=True)

# Remove ALL existing posts (md and mdx)
removed = 0
for f in os.listdir(OUT_DIR):
    if f.endswith(('.md', '.mdx')):
        os.remove(os.path.join(OUT_DIR, f))
        removed += 1
print(f'Removed {removed} old files')

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

    body = html_to_safe_md(p['content'])
    title_safe = p['title'].replace('"', "'")
    desc = get_desc(p['title'], p['content'])
    tags = infer_tags(p['title'])
    tags_yaml = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
    # Add link to original Blogspot post for diagrams
    blogspot_link = f'\n\n---\n\n> 📊 **Note:** This post contains interactive diagrams. [View the full version with diagrams on Blogspot]({p["url"]})\n'

    fm  = f'---\ntitle: "{title_safe}"\n'
    fm += f'description: "{desc}"\n'
    fm += f'pubDate: {p["date"]}\n'
    fm += f'tags: {tags_yaml}\n'
    fm += f'---\n\n'

    path = os.path.join(OUT_DIR, slug + '.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fm + body + blogspot_link)
    print(f'  wrote: {slug}.md')
    written += 1

print(f'\n{"="*52}')
print(f'  Written : {written} MD files')
print(f'{"="*52}')
print('\nNEXT STEPS:')
print('  git add src/content/posts/')
print('  git commit -m "Revert to MD with Blogspot diagram links"')
print('  git push')
