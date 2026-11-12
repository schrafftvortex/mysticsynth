#!/usr/bin/env python3
"""
Mystic Synth - New Chart Generator
Run this from your mysticsynth root folder: python3 new_chart.py <image path>
"""

import os
import re
import sys
from datetime import date, datetime, timedelta
from html import escape

from PIL import Image, ImageOps

# ── CONFIG ─────────────────────────────────────────────────────────────────────
CHARTS_DIR    = "charts"
CHARTS_INDEX  = "charts.html"
SITE_URL      = "https://mysticsynth.net"
MAX_WIDTH     = 1200
# ───────────────────────────────────────────────────────────────────────────────


def next_chart_number(charts_dir):
    """Find the highest existing postXXX.html and return the next number."""
    nums = [
        int(m.group(1)) for f in os.listdir(charts_dir)
        if (m := re.fullmatch(r"post(\d{3})\.html", f))
    ]
    return max(nums) + 1 if nums else 1


def chart_week(today):
    """Return (friday, thursday) for the most recent Fri–Thu week ending on or before today."""
    thursday = today - timedelta(days=(today.weekday() - 3) % 7)
    return thursday - timedelta(days=6), thursday


def format_week(start, end):
    """Format a date range like 'Nov 6–12, 2026' or 'Oct 30–Nov 5, 2026'."""
    if start.year != end.year:
        return f"{start:%b} {start.day}, {start.year}–{end:%b} {end.day}, {end.year}"
    if start.month != end.month:
        return f"{start:%b} {start.day}–{end:%b} {end.day}, {end.year}"
    return f"{start:%b} {start.day}–{end.day}, {end.year}"


def prepare_image(path):
    """Open an image and return it as an RGB image at most MAX_WIDTH wide."""
    img = Image.open(path)
    img.load()
    img = ImageOps.exif_transpose(img)

    # Flatten transparency onto white so PNG charts convert cleanly to JPG
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.getchannel("A"))
        img = background
    else:
        img = img.convert("RGB")

    if img.width > MAX_WIDTH:
        height = round(img.height * MAX_WIDTH / img.width)
        img = img.resize((MAX_WIDTH, height), Image.LANCZOS)

    return img


def alt_text(title):
    """Describe the chart image for screen readers and link previews."""
    return f"Album chart: {title}"


def build_html(num_str, title, blurb, description, date_str, prev_str, width, height):
    """Return the full HTML for a new chart post."""

    t = escape(title)
    alt = escape(alt_text(title))
    page_url = f"{SITE_URL}/charts/post{num_str}.html"
    image_url = f"{SITE_URL}/charts/photo{num_str}.jpg"

    prev_link = f'\n    <a href="post{prev_str}.html" class="nav-button">← Previous</a>' if prev_str else ''
    blurb_html = f'\n            <p><br>{escape(blurb)}<br><br></p>' if blurb else ''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Mystic Synth">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:image:width" content="{width}">
  <meta property="og:image:height" content="{height}">
  <meta property="og:image:alt" content="{alt}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="../css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Funnel+Display&display=swap" rel="stylesheet">
  <title>{t} | Mystic Synth</title>
</head>
<body>
<header>
    <div class="hero">
        <h1>Mystic Synth</h1>
        <p>Digging in deep now.</p>
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

<!-- Previous and Next Buttons -->
<div class="navigation-buttons">{prev_link}
</div>

<main>
    <section class="posts">
        <!-- Post {int(num_str)} -->
        <article class="post">
            <div class="post-date">{date_str}</div>
            <h2 class="post-title">{t}</h2>{blurb_html}
            <a href="../charts/post{num_str}.html">
                <img src="../charts/photo{num_str}.jpg" alt="{alt}" class="post-image">
            </a>
        </article>
    </section>
</main>

    <footer>
        <p>&copy; {datetime.now().year} Mystic Synth</p>
    </footer>
</body>

</html>
"""


def add_next_link(prev_path, num_str):
    """Add a Next → link to the previous chart post's navigation buttons."""
    with open(prev_path, "r", encoding="utf-8") as f:
        content = f.read()

    if f'post{num_str}.html' in content:
        return False

    m = re.search(r'<div class="navigation-buttons">.*?\n(\s*)</div>', content, re.S)
    if not m:
        print(f"\n⚠️  Could not find navigation buttons in {prev_path} — please add the Next link manually.")
        return False

    insert_at = m.start(1)
    link = f'    <a href="post{num_str}.html" class="nav-button">Next →</a>\n'
    content = content[:insert_at] + link + content[insert_at:]

    with open(prev_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def inject_into_charts_index(index_path, num_str, title, date_str):
    """Insert a new card at the top of charts.html."""
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    insert_marker = "<main>\n\n"
    if insert_marker not in content:
        print(f"\n⚠️  Could not auto-update {index_path} — please add the card manually.")
        return False

    alt = escape(alt_text(title))
    card = f"""    <section class="posts">
        <!-- Post {int(num_str)} -->
        <article class="post">
            <div class="post-date">{date_str}</div>
            <h2 class="post-title">{escape(title)}</h2>
            <a href="charts/post{num_str}.html">
                <img src="charts/photo{num_str}.jpg" alt="{alt}" class="post-image">
            </a>
        </article>
    </section>

"""

    updated = content.replace(insert_marker, insert_marker + card, 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated)

    return True


def main():
    print("=" * 50)
    print("  📊  Mystic Synth — New Chart Generator")
    print("=" * 50)

    if len(sys.argv) != 2:
        print("\nUsage: python3 new_chart.py <image path>")
        return

    # Validate we're in the right directory
    if not os.path.isdir(CHARTS_DIR) or not os.path.isfile(CHARTS_INDEX):
        print(f"\n❌  Couldn't find '{CHARTS_DIR}/' or '{CHARTS_INDEX}'.")
        print("    Make sure you run this script from your mysticsynth root folder.")
        return

    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(f"\n❌  Couldn't find image '{image_path}'.")
        return

    try:
        img = prepare_image(image_path)
    except Exception as e:
        print(f"\n❌  Couldn't open '{image_path}' as an image: {e}")
        return

    num      = next_chart_number(CHARTS_DIR)
    num_str  = str(num).zfill(3)
    prev_str = str(num - 1).zfill(3) if num > 1 else None

    html_path  = os.path.join(CHARTS_DIR, f"post{num_str}.html")
    photo_path = os.path.join(CHARTS_DIR, f"photo{num_str}.jpg")
    for path in (html_path, photo_path):
        if os.path.exists(path):
            print(f"\n❌  {path} already exists — not overwriting it.")
            return

    print(f"\nNext chart number: #{num_str}")

    # Gather info
    today = date.today()
    week = format_week(*chart_week(today))
    default_title = f"Top 25 Albums · Week of {week}"

    title = input(f"\nChart title (press Enter for: {default_title}): ").strip() or default_title
    blurb = input("Optional one-line blurb (press Enter to skip): ").strip()

    if blurb:
        description = blurb
    elif title == default_title:
        description = f"My top 25 albums for the week of {week}."
    else:
        description = f"My top 25 albums: {title}."

    date_str = today.strftime("%B %d, %Y")

    # Save the image
    img.save(photo_path, "JPEG", quality=85, optimize=True, progressive=True)
    print(f"\n✅  Created:  {photo_path}  ({img.width}×{img.height})")

    # Write the HTML file
    html = build_html(num_str, title, blurb, description, date_str, prev_str, img.width, img.height)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅  Created:  {html_path}")

    # Update the previous chart's "Next →" link
    if prev_str:
        prev_path = os.path.join(CHARTS_DIR, f"post{prev_str}.html")
        if os.path.isfile(prev_path) and add_next_link(prev_path, num_str):
            print(f"✅  Updated:  {prev_path}  (added Next → link)")

    # Update charts.html
    if inject_into_charts_index(CHARTS_INDEX, num_str, title, date_str):
        print(f"✅  Updated:  {CHARTS_INDEX}  (added card at the top)")

    print(f"\n🎉  Done! Check {html_path} in a browser, then commit.\n")


if __name__ == "__main__":
    main()
