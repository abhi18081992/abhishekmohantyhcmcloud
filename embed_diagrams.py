import os, re

POST_DIR = "src/content/posts"
IMG_DIR = "public/diagrams"
os.makedirs(IMG_DIR, exist_ok=True)

# Copy PNG files to public/diagrams/
import shutil
src = "diagrams"
if os.path.isdir(src):
    for f in os.listdir(src):
        if f.endswith(".png"):
            shutil.copy(os.path.join(src, f), os.path.join(IMG_DIR, f))
    print(f"Copied {len(os.listdir(IMG_DIR))} PNG files to {IMG_DIR}")

# Replace SVG blocks in markdown with img tags
SVG_COUNTS = {'oracle-hcm-cloud-fast-formula-night-ot': 3, 'oracle-hcm-cloud-fast-formula-night': 3, 'oracle-fast-formula-time-entry-rule-part-4': 4, 'oracle-fast-formula-time-entry-rule-part-3': 2, 'oracle-fast-formula-time-entry-rule-part-2': 15, 'oracle-fast-formula-time-entry-rule-part-1': 4, 'how-oracle-fast-formula-resolves-alias': 3, 'oracle-fast-formula-getplanbalance': 11, 'oracle-fast-formula-how-to-generate': 7, 'oracle-hcm-fast-formula': 4}

replaced = 0
for slug, count in SVG_COUNTS.items():
    md_path = os.path.join(POST_DIR, slug + ".md")
    if not os.path.exists(md_path):
        print(f"NOT FOUND: {md_path}")
        continue
    
    t = open(md_path, encoding="utf-8").read()
    fig_num = [0]
    
    def replace_svg(m):
        fig_num[0] += 1
        fname = f"/diagrams/{slug}-fig{fig_num[0]}.png"
        return f'\n<img src="{fname}" alt="Figure {fig_num[0]}" style="width:100%;max-width:820px;display:block;margin:24px auto;" />\n'
    
    t2 = re.sub(r"<svg[\s\S]*?</svg>", replace_svg, t, flags=re.IGNORECASE)
    
    if t2 != t:
        open(md_path, "w", encoding="utf-8").write(t2)
        print(f"  {slug}: replaced {fig_num[0]} SVGs with img tags")
        replaced += 1

print(f"\nDone: {replaced} posts updated")
