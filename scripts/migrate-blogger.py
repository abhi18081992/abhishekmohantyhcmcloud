#!/usr/bin/env python3
"""
migrate-blogger.py
==================
Convert a Blogger XML backup into Astro markdown posts for
abhishekmohantyhcmcloud.com.

USAGE
-----
    python3 migrate-blogger.py blog-MM-DD-YYYY.xml

By default it writes posts into ./src/content/posts/ relative to the
current working directory. Run it from the root of the Astro project.

WHAT IT DOES
------------
- Parses the Atom XML produced by Blogger's "Back up content" button.
- Skips drafts, comments, template entries, and pages.
- For each blog post:
    * extracts title, publish date, tags (Blogger labels)
    * pulls the HTML body
    * unwraps Blogger's <pre>/<code> blocks into fenced markdown
    * strips inline styles, fixes relative links, decodes entities
    * converts <h2>/<h3>/<ul>/<ol>/<blockquote>/<a>/<img>/<strong>/<em>
      into clean markdown
    * generates a slug from the title
    * writes a frontmatter + body .md file
- Prints a summary at the end with counts and any skipped entries.

DEPENDENCIES
------------
Standard library only. No pip install needed.
"""

import html
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ATOM_NS = "{http://www.w3.org/2005/Atom}"
BLOGGER_KIND = "http://schemas.google.com/blogger/2008/kind#post"

OUTPUT_DIR = Path("src/content/posts")


# ---------------------------------------------------------------------------
# HTML -> Markdown conversion
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:80] or "post"


def clean_html(raw: str) -> str:
    """Strip Blogger's noisy markup before conversion."""
    if not raw:
        return ""
    # Drop style/script blocks entirely
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.DOTALL | re.I)
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.I)
    # Strip inline style/class attributes
    raw = re.sub(r'\s(style|class|id|data-[a-z-]+)="[^"]*"', "", raw, flags=re.I)
    # Normalize <br>
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    return raw


def html_to_markdown(raw: str) -> str:
    """A small, blog-specific HTML->markdown converter."""
    if not raw:
        return ""

    s = clean_html(raw)

    # Code blocks: <pre><code>...</code></pre> -> fenced
    def _pre_repl(m):
        body = m.group(1)
        body = re.sub(r"^\s*<code[^>]*>|</code>\s*$", "", body, flags=re.I)
        body = html.unescape(body)
        body = re.sub(r"<[^>]+>", "", body)  # strip any leftover spans
        return f"\n\n```text\n{body.rstrip()}\n```\n\n"

    s = re.sub(r"<pre[^>]*>(.*?)</pre>", _pre_repl, s, flags=re.DOTALL | re.I)

    # Inline code
    s = re.sub(r"<code[^>]*>(.*?)</code>", lambda m: f"`{html.unescape(m.group(1))}`", s, flags=re.DOTALL | re.I)

    # Headings
    for level in (2, 3, 4):
        s = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, lv=level: f"\n\n{'#' * lv} {m.group(1).strip()}\n\n",
            s,
            flags=re.DOTALL | re.I,
        )

    # Bold / italic
    s = re.sub(r"<(?:strong|b)>(.*?)</(?:strong|b)>", r"**\1**", s, flags=re.DOTALL | re.I)
    s = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", s, flags=re.DOTALL | re.I)

    # Links
    s = re.sub(
        r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        lambda m: f"[{re.sub('<[^>]+>', '', m.group(2))}]({m.group(1)})",
        s,
        flags=re.DOTALL | re.I,
    )

    # Images
    s = re.sub(
        r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>',
        r"![\2](\1)",
        s,
        flags=re.I,
    )
    s = re.sub(r'<img[^>]*src="([^"]+)"[^>]*/?>', r"![](\1)", s, flags=re.I)

    # Lists
    def _ul_repl(m):
        items = re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), flags=re.DOTALL | re.I)
        return "\n\n" + "\n".join(f"- {it.strip()}" for it in items) + "\n\n"

    def _ol_repl(m):
        items = re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), flags=re.DOTALL | re.I)
        return "\n\n" + "\n".join(f"{i + 1}. {it.strip()}" for i, it in enumerate(items)) + "\n\n"

    s = re.sub(r"<ul[^>]*>(.*?)</ul>", _ul_repl, s, flags=re.DOTALL | re.I)
    s = re.sub(r"<ol[^>]*>(.*?)</ol>", _ol_repl, s, flags=re.DOTALL | re.I)

    # Blockquote
    s = re.sub(
        r"<blockquote[^>]*>(.*?)</blockquote>",
        lambda m: "\n\n" + "\n".join(f"> {ln}" for ln in m.group(1).strip().splitlines() if ln.strip()) + "\n\n",
        s,
        flags=re.DOTALL | re.I,
    )

    # Paragraphs / divs -> blank line breaks
    s = re.sub(r"</?p[^>]*>", "\n\n", s, flags=re.I)
    s = re.sub(r"</?div[^>]*>", "\n\n", s, flags=re.I)
    s = re.sub(r"</?span[^>]*>", "", s, flags=re.I)

    # Anything still tagged -> nuke
    s = re.sub(r"<[^>]+>", "", s)

    # Decode entities
    s = html.unescape(s)

    # Collapse whitespace
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def yaml_escape(value: str) -> str:
    return value.replace('"', '\\"')


def build_frontmatter(title: str, pub_date: datetime, tags: list[str], description: str = "") -> str:
    lines = ["---"]
    lines.append(f'title: "{yaml_escape(title)}"')
    if description:
        lines.append(f'description: "{yaml_escape(description)}"')
    lines.append(f"pubDate: {pub_date.strftime('%Y-%m-%d')}")
    if tags:
        tag_list = ", ".join(f'"{yaml_escape(t)}"' for t in tags)
        lines.append(f"tags: [{tag_list}]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 migrate-blogger.py <blogger-export.xml>")
        return 1

    xml_path = Path(sys.argv[1])
    if not xml_path.exists():
        print(f"ERROR: file not found: {xml_path}")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reading {xml_path} ...")
    tree = ET.parse(xml_path)
    root = tree.getroot()

    written = 0
    skipped_drafts = 0
    skipped_pages = 0
    skipped_other = 0

    for entry in root.findall(f"{ATOM_NS}entry"):
        # Identify the entry kind
        kind = None
        is_draft = False
        for cat in entry.findall(f"{ATOM_NS}category"):
            scheme = cat.get("scheme", "")
            term = cat.get("term", "")
            if scheme == "http://schemas.google.com/g/2005#kind":
                kind = term
            if "blogger/2008/kind#draft" in term or term.endswith("#draft"):
                is_draft = True

        if kind != BLOGGER_KIND:
            if kind and "page" in kind:
                skipped_pages += 1
            else:
                skipped_other += 1
            continue

        # Drafts have an <app:control><app:draft>yes</app:draft></app:control> block
        for ctrl in entry.iter():
            if ctrl.tag.endswith("draft") and (ctrl.text or "").strip().lower() == "yes":
                is_draft = True

        if is_draft:
            skipped_drafts += 1
            continue

        title_el = entry.find(f"{ATOM_NS}title")
        title = (title_el.text or "Untitled").strip() if title_el is not None else "Untitled"

        published_el = entry.find(f"{ATOM_NS}published")
        try:
            pub_raw = published_el.text.replace("Z", "+00:00")
            pub_date = datetime.fromisoformat(pub_raw)
        except Exception:
            pub_date = datetime.now()

        # Tags = categories whose scheme is the Blogger labels scheme
        tags: list[str] = []
        for cat in entry.findall(f"{ATOM_NS}category"):
            scheme = cat.get("scheme", "")
            term = cat.get("term", "")
            if "ns#" in scheme or scheme.endswith("#"):  # blogger label scheme
                tags.append(term)

        content_el = entry.find(f"{ATOM_NS}content")
        body_html = content_el.text if content_el is not None and content_el.text else ""

        body_md = html_to_markdown(body_html)

        # First non-empty line = description hint
        description = ""
        for line in body_md.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith(("#", "```", ">", "-", "*", "!", "[")):
                description = stripped[:200]
                break

        slug = slugify(title)
        out_path = OUTPUT_DIR / f"{slug}.md"
        # Avoid collision
        n = 2
        while out_path.exists():
            out_path = OUTPUT_DIR / f"{slug}-{n}.md"
            n += 1

        frontmatter = build_frontmatter(title, pub_date, tags, description)
        out_path.write_text(frontmatter + body_md, encoding="utf-8")
        written += 1
        print(f"  wrote {out_path.name}")

    print()
    print("=" * 50)
    print(f"  Written : {written}")
    print(f"  Drafts  : {skipped_drafts} (skipped)")
    print(f"  Pages   : {skipped_pages} (skipped)")
    print(f"  Other   : {skipped_other} (skipped)")
    print("=" * 50)
    print()
    print("NEXT STEPS:")
    print("  1. Spot-check a few files in src/content/posts/")
    print("  2. Run `npm run dev` to preview locally, OR commit and push to GitHub")
    print("  3. Cloudflare Pages will rebuild automatically")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
