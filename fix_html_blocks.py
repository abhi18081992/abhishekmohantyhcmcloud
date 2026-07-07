import os, re

d = 'src/content/posts'
n = 0
for f in os.listdir(d):
    if not f.endswith('.md'):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding='utf-8').read()
    # Ensure blank line before block-level HTML tags
    # so markdown parser treats them as HTML blocks, not inline
    for tag in ['<svg', '<div', '<table', '<figure']:
        t = re.sub(r'([^\n])\n(' + re.escape(tag) + r')', r'\1\n\n\2', t)
    # Also ensure blank line AFTER closing tags
    for tag in ['</div>', '</svg>', '</figure>']:
        t = re.sub(r'(' + re.escape(tag) + r')\n([^\n<])', r'\1\n\n\2', t)
    open(p, 'w', encoding='utf-8').write(t)
    n += 1

print(f'Fixed {n} files')
