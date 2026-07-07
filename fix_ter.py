import os, re, shutil

POST_DIR = "src/content/posts"
IMG_DIR = "public/diagrams"
DIAG_SRC = "diagrams"

# Map the actual file slugs to the diagram slug prefix
TER_FIXES = {
    "oracle-fast-formula-time-entry-rule-part-1-2026-05-22": "oracle-fast-formula-time-entry-rule_01813668993",
    "oracle-fast-formula-time-entry-rule-part-1-2026-05-29": "oracle-fast-formula-time-entry-rule_01788502086",
    # Part 4 was already handled (oracle-fast-formula-time-entry-rule-part-1)
    # but Part 3 and 4 have different diagram slugs
}

# Also check what diagram files exist for TER
print("Diagram files for TER:")
for f in sorted(os.listdir(DIAG_SRC)):
    if 'time-entry' in f or 'entry-rule' in f:
        print(f"  {f}")

print("\nPost files:")
for f in sorted(os.listdir(POST_DIR)):
    if 'time-entry' in f:
        print(f"  {f}")

print("\nFixing...")
for post_slug, diag_slug in TER_FIXES.items():
    md_path = os.path.join(POST_DIR, post_slug + ".md")
    if not os.path.exists(md_path):
        print(f"NOT FOUND: {md_path}")
        continue

    t = open(md_path, encoding="utf-8").read()
    svgs = re.findall(r"<svg[\s\S]*?</svg>", t, re.IGNORECASE)
    
    if not svgs:
        print(f"No SVGs in {post_slug}")
        continue

    fig_num = [0]
    def replace_svg(m):
        fig_num[0] += 1
        # Check if the png exists with this slug
        png_name = f"{diag_slug}-fig{fig_num[0]}.png"
        src = os.path.join(DIAG_SRC, png_name)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(IMG_DIR, png_name))
            return f'\n<img src="/diagrams/{png_name}" alt="Figure {fig_num[0]}" style="width:100%;max-width:820px;display:block;margin:24px auto;" />\n'
        else:
            print(f"  PNG not found: {png_name}")
            return m.group(0)

    t2 = re.sub(r"<svg[\s\S]*?</svg>", replace_svg, t, flags=re.IGNORECASE)
    open(md_path, "w", encoding="utf-8").write(t2)
    print(f"  Fixed: {post_slug} ({fig_num[0]} figures)")

print("\nDone")
