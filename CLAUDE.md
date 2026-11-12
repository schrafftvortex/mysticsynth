# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Mystic Synth is a personal static website (hand-written HTML/CSS/vanilla JS, no build step, no dependencies, no tests) served at `mysticsynth.net` via GitHub Pages (see `CNAME`). Pushing to `main` deploys it.

To preview locally, run `python3 -m http.server` from the repo root and open `http://localhost:8000`.

`_config.yml` lists repo files that GitHub Pages should not publish (currently `CLAUDE.md`).

## Rules

- This is a deliberately hand-built site: keep it plain HTML/CSS/vanilla JS. Don't introduce frameworks, libraries, package managers, or build tools. (Pillow, used by `new_chart.py`, is a local tool, not part of the site.)
- The author syncs between two Fedora machines through git, so never leave work uncommitted: commit to `main` when a change is done.
- Don't push. The author reviews changes on localhost and pushes them personally, unless they explicitly ask Claude to push.
- Blog workflow: draft in Markdown in `blog/posts/`, then publish with `new_post.py`. Chart workflow: one chart per week, added with `new_chart.py`.

## Structure

- Top-level pages (`index.html`, `about.html`, `mymusic.html`, `links.html`, `gallery.html`, `charts.html`, `blog.html`) each duplicate the same `<header>` hero + nav and `<footer>`. There are no includes/templates, so a nav or footer change must be made in every page, including the pages in `blog/`, `charts/`, and `gallery/` (which use `../` relative paths).
- All pages share `css/styles.css`. Links are light blue `#89CFF0` and turn orange `#FF7F00` on hover.
- Each page has its own `<title>` in the form `Page Name | Mystic Synth` (the home page is just `Mystic Synth`) and its own meta description. The footer reads `&copy; 2026 Mystic Synth` on every page.
- `gallery/` is hand-maintained: each album on `gallery.html` is a manually written block linking to a subpage and cover image. The Pictures of Me and Pictures of Schrafft albums are commented out until their pages get real content.

## Blog system

`js/posts.js` is the list of blog posts: its `page_listing` object is the single source for every post's title, link, date (`YYYY-MM-DD hh:mm AM/PM`), excerpt, and category. Two pages read it, and each loads `js/posts.js` before its own script:

- `blog.html` → `js/blogscripts.js` renders the feed into `#blog_construct_div`, with category filtering and date sorting.
- `index.html` → `js/latestposts.js` fills the "Latest Blog Posts" list with the 2 newest posts by date. The `<noscript>` list under it is a hand-maintained fallback that isn't updated automatically.

Each post is a hand-written `blog/blogNNN.html` (3-digit zero-padded number) with Previous / All Posts / Next buttons in `.navigation-buttons`.

Categories are `life`, `philosophy`, `album_recs`, `gaming`, `movies`, `best`. Adding one requires changing the `CATEGORIES` list in `new_post.py`, a `case` in `createBlogConstruct` in `blogscripts.js`, and a radio button in `blog.html`.

**New posts:** run `python3 new_post.py` from the repo root (interactive). It creates the next `blog/blogNNN.html` from a template, adds a "Next →" link to the previous post, and adds an entry to `page_listing`. It inserts before the last `\n};` in `js/posts.js`, so keep `page_listing` as the only object in that file. Afterward, write the post body inside `.post-content`.

`blog/posts/*.md` holds rough drafts in Markdown. They aren't rendered; the published text is converted by hand into the post's HTML (use `<p>`, and `<h3 class="subtitle">` for section headings).

## Weekly charts

Each chart is a `charts/postNNN.html` page plus a `charts/photoNNN.jpg` image, with a card on `charts.html` (newest first).

**New charts:** run `python3 new_chart.py <image path>` from the repo root (interactive). The default title covers the most recent Friday–Thursday week, e.g. `Top 25 Albums · Week of Nov 6–12, 2026`. The script:

- converts the image to JPG, at most 1200px wide;
- creates the page with a unique title, meta description, alt text, and Open Graph tags (absolute `https://mysticsynth.net/...` URLs, so shared links preview with the chart image);
- adds a "Next →" link to the previous chart;
- inserts a card at the top of `charts.html`, right after the literal text `<main>\n\n`, so keep that intact.
