#!/usr/bin/env python3
"""
Mystic Synth - New Blog Post Generator
Run this from your mysticsynth root folder: python new_post.py
"""

import os
import re
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────────────────────────────
BLOG_DIR      = "blog"
BLOGSCRIPTS   = "js/blogscripts.js"
CATEGORIES    = ["life", "philosophy", "album_recs", "gaming", "movies", "best"]
# ───────────────────────────────────────────────────────────────────────────────


def next_post_number(blog_dir):
    """Find the highest existing blogXXX.html and return the next number."""
    existing = [
        f for f in os.listdir(blog_dir)
        if re.match(r"blog\d{3}\.html", f)
    ]
    if not existing:
        return 1
    nums = [int(re.search(r"\d{3}", f).group()) for f in existing]
    return max(nums) + 1


def prompt_category():
    print("\nCategories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Pick a category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("  Please enter a number from the list.")


def build_html(num, num_str, title, date_str, prev_str, next_str):
    """Return the full HTML for a new post."""

    prev_link = f'<a href="blog{prev_str}.html" class="nav-button">← Previous</a>\n            ' if prev_str else ''
    next_link = f'\n            <a href="blog{next_str}.html" class="nav-button">Next →</a>' if next_str else ''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Mystic Synth - The website you wish you visited 20 years ago.">
  <link rel="stylesheet" href="../css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Funnel+Display&display=swap" rel="stylesheet">
  <title>Blog Post {num_str} | Mystic Synth</title>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="hero">
            <h1>Welcome to Mystic Synth</h1>
            <p>Endless searching.</p>
        </div>
        <nav>
            <ul>
                <li><a href="../index.html">Home</a></li>
                <li><a href="../about.html">About</a></li>
                <li><a href="../mymusic.html">My Music</a></li>
                <li><a href="../links.html">Links</a></li>
                <li><a href="../gallery.html">Gallery</a></li>
                <li><a href="../charts.html">Charts</a></li>
                <li><a href="../blog.html">Blog</a></li>
            </ul>
        </nav>
    </header>

        <!-- Navigation Buttons -->
        <div class="navigation-buttons">
            {prev_link}<a href="../blog.html" class="nav-button center-button">All Posts</a>{next_link}
        </div>

    <!-- Main Content -->
    <main>
        <article class="blog-post">
            <h2>#{num_str}: {title}</h2>
            <p class="post-date">{date_str}</p>
            <div class="post-content">

                <!-- ✏️  Write your post here -->
                <p><br><br></p>

            </div>
        </article>
    </main>

    <!-- Footer -->
    <footer>
        <p>&copy; {datetime.now().year} Mystic Synth</p>
    </footer>

</body>
</html>
"""


def inject_into_blogscripts(js_path, num_str, title, excerpt, category, dt):
    """Append a new entry to page_listing in blogscripts.js."""
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the last closing brace of the page_listing object
    # We look for the pattern };  that closes the const page_listing = { ... };
    insert_marker = "};\n\nlet included_pages"
    if insert_marker not in content:
        print(f"\n⚠️  Could not auto-update {js_path} — please add the entry manually.")
        return False

    date_formatted = dt.strftime("%Y-%m-%d %I:%M %p")
    num_int = int(num_str)

    new_entry = f"""    "{num_str}": {{ 
        title: "{title}", 
        link: "blog/blog{num_str}.html", 
        displaynum: "{num_str}", 
        date: "{date_formatted}", 
        excerpt: "{excerpt}",
        var: "{num_int}", 
        category: "{category}" 
    }},\n"""

    # Insert before the closing }; of page_listing
    updated = content.replace(
        insert_marker,
        new_entry + "};\n\nlet included_pages"
    )

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(updated)

    return True


def main():
    print("=" * 50)
    print("  🎛️  Mystic Synth — New Post Generator")
    print("=" * 50)

    # Validate we're in the right directory
    if not os.path.isdir(BLOG_DIR):
        print(f"\n❌  Couldn't find '{BLOG_DIR}/' folder.")
        print("    Make sure you run this script from your mysticsynth root folder.")
        return

    if not os.path.isfile(BLOGSCRIPTS):
        print(f"\n❌  Couldn't find '{BLOGSCRIPTS}'.")
        print("    Make sure you run this script from your mysticsynth root folder.")
        return

    # Gather info
    num       = next_post_number(BLOG_DIR)
    num_str   = str(num).zfill(3)
    prev_str  = str(num - 1).zfill(3) if num > 1 else None
    next_str  = None  # there's no next post yet

    print(f"\nNext post number: #{num_str}")

    title    = input("\nPost title: ").strip()
    excerpt  = input("Short excerpt (one sentence for the index): ").strip()
    category = prompt_category()

    # Date/time — default to now
    now      = datetime.now()
    date_input = input(f"\nPost date/time (press Enter for now: {now.strftime('%Y-%m-%d %I:%M %p')}): ").strip()
    if date_input:
        try:
            dt = datetime.strptime(date_input, "%Y-%m-%d %I:%M %p")
        except ValueError:
            print("  Couldn't parse that date — using current time.")
            dt = now
    else:
        dt = now

    display_date = dt.strftime("%B %d, %Y")

    # Write the HTML file
    html_path = os.path.join(BLOG_DIR, f"blog{num_str}.html")
    html      = build_html(num, num_str, title, display_date, prev_str, next_str)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅  Created:  {html_path}")

    # Update also the previous post's "Next →" link
    if prev_str:
        prev_path = os.path.join(BLOG_DIR, f"blog{prev_str}.html")
        if os.path.isfile(prev_path):
            with open(prev_path, "r", encoding="utf-8") as f:
                prev_content = f.read()

            # If the previous post has no Next link, add one
            if f'blog{num_str}.html' not in prev_content:
                old_all_posts = '<a href="../blog.html" class="nav-button center-button">All Posts</a>'
                new_all_posts = f'<a href="../blog.html" class="nav-button center-button">All Posts</a>\n            <a href="blog{num_str}.html" class="nav-button">Next →</a>'
                prev_content  = prev_content.replace(old_all_posts, new_all_posts)

                with open(prev_path, "w", encoding="utf-8") as f:
                    f.write(prev_content)

                print(f"✅  Updated:  {prev_path}  (added Next → link)")

    # Update blogscripts.js
    success = inject_into_blogscripts(BLOGSCRIPTS, num_str, title, excerpt, category, dt)
    if success:
        print(f"✅  Updated:  {BLOGSCRIPTS}  (added post to index)")

    print(f"\n🎉  Done! Open {html_path} and write your post.")
    print("    When you're ready, push to GitHub as usual.\n")


if __name__ == "__main__":
    main()
