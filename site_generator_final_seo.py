import os
import math
from datetime import datetime

# 一页显示的图片数量
IMAGES_PER_PAGE = 20

def generate_gallery(folder):
    images = sorted([f for f in os.listdir(folder) if f.endswith(".jpg")])
    total_pages = math.ceil(len(images) / IMAGES_PER_PAGE)

    for page_num in range(total_pages):
        start = page_num * IMAGES_PER_PAGE
        end = start + IMAGES_PER_PAGE
        page_images = images[start:end]

        page_filename = f"{folder}/page{page_num + 1}.html"
        with open(page_filename, "w", encoding="utf-8") as f:
            title = f"{folder.capitalize()} Gallery - Page {page_num + 1}"
            keywords = ", ".join([img.replace(".jpg", "").replace("_", " ") for img in page_images])
            description = f"Explore {folder} gallery page {page_num + 1} with high-quality photo previews."

            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="../lightbox.min.css" rel="stylesheet" />
  <script src="../lightbox-plus-jquery.js"></script>
  <script src="../ads.js"></script>
  <style>
    body {{
      background-color: #111;
      color: white;
      font-family: Georgia, serif;
      padding: 20px;
    }}
    h1 {{
      text-align: center;
      font-size: 36px;
    }}
    .gallery {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-top: 20px;
    }}
    .gallery img {{
      width: 180px;
      height: auto;
      border-radius: 8px;
    }}
    .nav {{
      text-align: center;
      margin-top: 30px;
    }}
    .nav a {{
      color: #ccc;
      margin: 0 12px;
      text-decoration: none;
    }}
  </style>
</head>
<body>
<h1>{folder.capitalize()} Gallery - Page {page_num + 1}</h1>
<div class="gallery">
""")

            for img in page_images:
                alt_text = img.replace(".jpg", "").replace("_", " ")
                f.write(f'<a href="{img}" data-lightbox="{folder}"><img src="{img}" alt="{alt_text}" title="{alt_text}"></a>\n')

            f.write("</div>\n<div class='nav'>\n")
            if page_num > 0:
                f.write(f'<a href="page{page_num}.html">← Previous</a>')
            f.write(f'<a href="../index.html">🏠 Home</a>')
            if page_num < total_pages - 1:
                f.write(f'<a href="page{page_num + 2}.html">Next →</a>')
            f.write("</div>\n</body>\n</html>")

def generate_sitemap(folders):
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for folder in folders:
            total = len([x for x in os.listdir(folder) if x.endswith(".jpg")])
            pages = math.ceil(total / IMAGES_PER_PAGE)
            for i in range(1, pages + 1):
                f.write(f"<url><loc>{folder}/page{i}.html</loc></url>\n")
        f.write("</urlset>")

def main():
    folders = [d for d in os.listdir() if os.path.isdir(d)]
    for folder in folders:
        generate_gallery(folder)
    generate_sitemap(folders)
    print("✅ Gallery pages and SEO metadata generated successfully.")

if __name__ == "__main__":
    main()
