import os, re

d = 'src/content/posts'
fixed = 0

for f in os.listdir(d):
    if not f.endswith('.mdx'):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding='utf-8').read()
    # Remove HTML comments which break MDX parser
    t2 = re.sub(r'<!--.*?-->', '', t, flags=re.DOTALL)
    # Remove <!DOCTYPE and similar
    t2 = re.sub(r'<!(?!--)[^>]*>', '', t2)
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
        fixed += 1

print(f'Fixed {fixed} files')
