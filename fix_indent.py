import os, re

d = 'src/content/posts'
n = 0
for f in os.listdir(d):
    if not f.endswith('.md'):
        continue
    p = os.path.join(d, f)
    t = open(p, encoding='utf-8').read()
    # Remove leading whitespace from lines starting with HTML tags
    # This prevents markdown from treating indented HTML as code blocks
    lines = t.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('<') or stripped.startswith('</'):
            new_lines.append(stripped)
        else:
            new_lines.append(line)
    t2 = '\n'.join(new_lines)
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
        n += 1

print(f'Fixed {n} files')
