import os, re

d = 'src/content/posts'
n = 0

for f in os.listdir(d):
    if not f.endswith('.md'):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding='utf-8').read()
    
    # Find divs that contain SVGs and extract just the SVG
    # Pattern: <div ...>\n<svg ...>...</svg>\n</div>
    # Replace with just the SVG
    t2 = re.sub(
        r'<div[^>]*>\n(<svg[\s\S]*?</svg>)\n</div>',
        r'\1',
        t
    )
    
    # Also ensure every SVG starts on its own line with no indentation
    t2 = re.sub(r'\n +(<svg)', r'\n\1', t2)
    t2 = re.sub(r'\n +(<defs)', r'\n\1', t2)
    
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
        n += 1

print(f'Fixed {n} files')
