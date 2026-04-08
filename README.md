# abhishekmohantyhcmcloud.com

The personal site and blog of **Abhishek Mohanty** — Oracle HCM Cloud Technical Lead, Oracle ACE Apprentice, AIOUG member.

Built with [Astro](https://astro.build), styled with a custom editorial design system, and deployed on Cloudflare Pages.

---

## Stack at a glance

| Concern              | Choice                                          |
| -------------------- | ----------------------------------------------- |
| Framework            | Astro 4 (static output)                         |
| Content              | Markdown files in `src/content/posts/`          |
| Syntax highlighting  | Shiki, theme: **One Dark Pro**                  |
| Typography           | Lora (display) + IBM Plex Sans (body) + IBM Plex Mono (code) |
| Hosting              | Cloudflare Pages (free tier)                    |
| Domain               | abhishekmohantyhcmcloud.com (Cloudflare Registrar) |
| Source control       | GitHub (any free public or private repo works)  |

---

## First-time deployment (one-time setup)

You only do this once. After that, publishing a new post is just a Git commit.

### Step 1 — Create a GitHub repository

1. Sign in at [github.com](https://github.com).
2. Click **New repository**.
3. Name it `abhishekmohantyhcmcloud` (or whatever you like — it doesn't have to match the domain).
4. Leave it **private** if you want, public is fine too.
5. Do **not** initialize it with a README, `.gitignore`, or license — this folder already has those.
6. Click **Create repository**. Copy the URL it shows (looks like `https://github.com/yourusername/abhishekmohantyhcmcloud.git`).

### Step 2 — Push this folder to GitHub

From the root of this folder, in a terminal:

```bash
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/abhishekmohantyhcmcloud.git
git push -u origin main
```

If you don't have Git installed locally, the simpler mobile-friendly path is to use GitHub Desktop or — easier still — drag and drop the entire folder into the GitHub web UI after creating the empty repo. GitHub will accept a folder upload.

### Step 3 — Connect Cloudflare Pages to the repo

1. Open the Cloudflare dashboard → **Workers & Pages** in the sidebar.
2. Click **Create application** → **Pages** → **Connect to Git**.
3. Authorize Cloudflare to access your GitHub account.
4. Pick the `abhishekmohantyhcmcloud` repo.
5. On the build settings screen:
   - **Framework preset:** Astro
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** leave blank
   - **Node version:** 20 (set this as an environment variable: `NODE_VERSION` = `20`)
6. Click **Save and Deploy**.

The first build takes 1–2 minutes. When it finishes you'll get a URL like `abhishekmohantyhcmcloud.pages.dev`. Open it — your site should be live with the two sample posts.

### Step 4 — Point the custom domain at Pages

1. In the Pages project settings, go to **Custom domains** → **Set up a custom domain**.
2. Enter `www.abhishekmohantyhcmcloud.com`. Cloudflare will automatically create the right CNAME because the domain is already on the same Cloudflare account.
3. Add a second domain entry for the apex `abhishekmohantyhcmcloud.com`. Cloudflare will set up the redirect.
4. Wait 1–2 minutes. SSL is provisioned automatically — you don't have to configure anything.
5. Test all four URL variants in a browser; they should all land on `https://www.abhishekmohantyhcmcloud.com/`.

**Important:** if you previously added DNS records for Blogger (the `ghs.google.com` CNAMEs and the four Google A records), **delete them now**. Cloudflare Pages will manage the DNS for you.

---

## Migrating your existing Blogger posts

This is a one-shot job. You run it once with your Blogger XML export, and it dumps all the posts into `src/content/posts/` as ready-to-commit markdown files.

### Step 1 — Export from Blogger

1. Go to Blogger → **Settings** → scroll to **Manage blog** → **Back up content**.
2. Click **Download**. You get a file named something like `blog-04-08-2026.xml`.
3. Save it somewhere you can find it. Don't open it in a text editor and accidentally re-save it — Blogger's encoding is fussy.

### Step 2 — Run the migration script

You need Python 3 (it's pre-installed on macOS and most Linux; on Windows install from python.org). The script uses **standard library only**, no `pip install` needed.

From the root of this folder:

```bash
python3 scripts/migrate-blogger.py /path/to/blog-04-08-2026.xml
```

The script will print one line per post as it writes them, then a summary like:

```
==================================================
  Written : 47
  Drafts  : 3 (skipped)
  Pages   : 1 (skipped)
  Other   : 0 (skipped)
==================================================
```

### Step 3 — Spot-check before committing

Open a few of the generated `.md` files in `src/content/posts/`. Check for:

- **Code blocks** — should be in fenced ```text blocks. If any of your old Blogger code blocks were nested in unusual ways the script may have left HTML fragments behind. Search for `<` in the markdown to spot them.
- **Tags** — Blogger labels become Astro tags. They get carried across as-is, so capitalisation will match what you used on Blogger.
- **Frontmatter** — every file should start with `---`, have a `title`, `pubDate`, and a `tags` array. If `description` is missing for some posts, that's fine — the homepage and post layouts handle empty descriptions gracefully.

You can also add a `module:` field manually to any post you want grouped on the homepage by Oracle module (e.g. `module: "Absence Management"`). The two sample posts in this folder show the format.

### Step 4 — Commit and push

```bash
git add src/content/posts/
git commit -m "Migrate Blogger posts"
git push
```

Cloudflare Pages will rebuild within ~30 seconds and your live site will have all the posts.

---

## Writing new posts

Create a new file in `src/content/posts/`, named like `my-post-slug.md`. The frontmatter looks like this:

```markdown
---
title: "Your post title"
description: "Short subtitle that shows under the title and in social previews."
pubDate: 2026-04-15
module: "Absence Management"
tags: ["Fast Formula", "APAC", "Debug Logging"]
---

Your markdown body goes here. Code blocks use fenced syntax:

​```text
DEFAULT FOR PER_PERSON_ID IS 0
INPUTS ARE IV_ACCRUAL
RETURN IV_ACCRUAL
​```
```

### Mobile publishing workflow

The whole point of using GitHub + Cloudflare Pages is that you can publish from your phone:

1. Open your repo on the GitHub mobile app or in a mobile browser.
2. Navigate to `src/content/posts/`.
3. Tap **Add file** → **Create new file**.
4. Type a filename ending in `.md`, paste the frontmatter and body.
5. Tap **Commit changes**.
6. Cloudflare Pages auto-rebuilds in 30–60 seconds. The post is live.

---

## Search Console migration

Once the new site is live and the old Blogger URLs are 301-redirecting via the `_redirects` file, do this in Google Search Console:

### Step 1 — Add the new property

In Search Console, click the property dropdown → **Add property**. Choose **Domain property** (not URL prefix) and enter `abhishekmohantyhcmcloud.com`. Google will give you a TXT record to verify — add it in your Cloudflare DNS settings.

Domain property is the right choice because it covers `http`, `https`, `www`, non-www, and any future subdomains in one go.

### Step 2 — Submit the new sitemap

In the new property, go to **Sitemaps** → enter `sitemap-index.xml` → Submit. Astro generates this automatically at build time.

### Step 3 — Use the Change of Address tool on the old property

In your **old** `abhishekmohanty-hcm.blogspot.com` property:

1. **Settings** (gear icon) → **Change of address**.
2. Select the new property (`abhishekmohantyhcmcloud.com`).
3. Google will run a few checks — it specifically looks for the 301 redirects, which the `_redirects` file in this project provides.
4. Confirm.

This tells Google to transfer all the ranking signals from the old domain to the new one. It's not instant — expect 1–4 weeks for the full migration to settle.

### Step 4 — Don't request re-indexing for at least 48 hours

After the switch, some posts will briefly 404 in Search Console while Google's crawler catches up to the new URLs. This is normal. If you panic-request re-indexing on day one you'll just confuse the crawler. Wait two days, then check the **Pages** report — it should be reporting the new URLs as indexed.

---

## Project layout

```
.
├── astro.config.mjs              # Astro config (site URL, sitemap, Shiki theme)
├── package.json                  # Dependencies
├── tsconfig.json                 # Strict TypeScript
├── scripts/
│   └── migrate-blogger.py        # Blogger XML -> markdown converter
├── public/
│   ├── _headers                  # Cloudflare security & cache headers
│   ├── _redirects                # 301 redirects from old Blogger URLs
│   ├── favicon.svg               # AM mark in brand red
│   └── robots.txt
└── src/
    ├── styles/
    │   └── global.css            # Design system, typography, code blocks
    ├── components/
    │   ├── Header.astro
    │   └── Footer.astro
    ├── layouts/
    │   ├── BaseLayout.astro      # HTML shell, meta, OG, RSS link
    │   └── PostLayout.astro      # Individual post wrapper
    ├── content/
    │   ├── config.ts             # Post schema (Zod)
    │   └── posts/                # Your markdown posts
    └── pages/
        ├── index.astro           # Homepage (hero + featured + archive)
        ├── about.astro           # About page
        ├── rss.xml.js            # RSS feed endpoint
        ├── posts/[...slug].astro # Dynamic post route
        └── tags/
            ├── index.astro       # Tag cloud
            └── [tag].astro       # Per-tag post listing
```

---

## Local development (optional)

If you want to preview changes locally before pushing:

```bash
npm install
npm run dev
```

Then open `http://localhost:4321` in your browser. Hot reload is on — edits show up instantly.

You don't need to do this. You can edit markdown files directly in GitHub's web UI and let Cloudflare Pages build them. Local dev is only useful if you're tweaking the design or templates.

---

## When something breaks

**Build fails on Cloudflare Pages.**
Check the build log in the Pages dashboard. The most common cause is a syntax error in a markdown frontmatter block — usually a missing quote around a title with a colon in it. Astro's error messages are very specific about which file and which line.

**A post isn't showing up.**
Check that the file is in `src/content/posts/`, has the `.md` extension, has valid frontmatter, and that `draft: true` is **not** set in the frontmatter. Drafts are filtered out of the homepage and the RSS feed.

**Old Blogger URLs aren't redirecting.**
Cloudflare Pages reads `_redirects` from `public/`. Make sure the file is committed and the latest deployment includes it. You can check by visiting `https://www.abhishekmohantyhcmcloud.com/_redirects` — it should serve as a text file. If it 404s, your build didn't pick it up.

**Custom domain won't activate in Pages.**
Make sure you've removed the old Blogger DNS records (the `ghs.google.com` CNAME and the four Google A records) from the Cloudflare DNS settings. Pages cannot bind to a domain whose DNS is pointing somewhere else.

---

## Credits

Design and build by Claude (Anthropic) for Abhishek Mohanty, April 2026.

The notes published on this site are personal and reflect the author's views, not those of any employer or client. Oracle and the Oracle product names referenced are trademarks of Oracle Corporation.
