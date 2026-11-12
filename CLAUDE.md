# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Mystic Synth is a personal static website (hand-written HTML/CSS/vanilla JS, no build step, no dependencies, no tests) served at `mysticsynth.net` via GitHub Pages (see `CNAME`). Deploying means committing and pushing to `main`.

To preview locally, open the HTML files directly or run `python -m http.server` from the repo root.

`_config.yml` lists repo files that GitHub Pages should not publish (currently `CLAUDE.md`).

## Rules

- This is a deliberately hand-built site: keep it plain HTML/CSS/vanilla JS. Don't introduce frameworks, libraries, package managers, or build tools.
- The author syncs between two Fedora machines through git, so never leave work uncommitted. Commit and push to `main` when a change is done.
- Post workflow: draft in Markdown in `blog/posts/`, then publish with `new_post.py` (see below).

## Structure

- Top-level pages (`index.html`, `about.html`, `mymusic.html`, `links.html`, `gallery.html`, `charts.html`, `blog.html`) each duplicate the same `<header>` hero + nav and `<footer>`. There are no includes/templates, so a nav or footer change must be made in every page, including the pages in `blog/`, `charts/`, and `gallery/` (which use `../` relative paths).
- All pages share `css/styles.css`.
- `charts/` and `gallery/` are hand-maintained: each entry on `charts.html` / `gallery.html` is a manually written block linking to a subpage and image.
- Each page has its own `<title>` in the form `Page Name | Mystic Synth` (the home page is just `Mystic Synth`) and its own meta description. The footer reads `&copy; 2026 Mystic Synth` on every page.

## Blog system

The blog is the only dynamic part and spans several files that must stay in sync:

1. `blog/blogNNN.html` — one hand-written HTML page per post (3-digit zero-padded number). Each has Previous / All Posts / Next buttons in `.navigation-buttons`.
2. `js/blogscripts.js` — the `page_listing` object is the post index. `blog.html` loads this script, which renders the feed into `#blog_construct_div` and handles category filtering and date sorting (by the `date` field, format `YYYY-MM-DD hh:mm AM/PM`).
3. Categories are `life`, `philosophy`, `album_recs`, `gaming`, `movies`, `best`. Adding a category requires changing the `CATEGORIES` list in `new_post.py`, a `case` in `createBlogConstruct` in `blogscripts.js`, and a radio button in `blog.html`.
4. `index.html` has a hand-maintained "Latest Blog Posts" list that isn't updated automatically.

**New posts:** run `python new_post.py` from the repo root (interactive). It creates the next `blog/blogNNN.html` from a template, adds a "Next →" link to the previous post, and inserts an entry into `page_listing`. The insertion depends on the literal text `};\n\nlet included_pages` in `blogscripts.js`, so keep that boundary intact. Afterward, write the post body inside `.post-content` and update `index.html` if needed.

`blog/posts/*.md` holds rough drafts in Markdown. They aren't rendered; the published text is converted by hand into the post's HTML (use `<p>`, and `<h3 class="subtitle">` for section headings).
