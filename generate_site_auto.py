import os
from pathlib import Path
from datetime import datetime
import random
import requests
import json

# === 自动路径 ===
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = BASE_DIR / "config.json"
KEYWORDS_DIR = BASE_DIR / "keywords"
SITEMAP_ENTRIES = []
EXCLUDE_DIRS = {"generator", "keywords", "pages", "static"}

# === 读取配置文件 ===
if not CONFIG_PATH.exists():
    print("❌ 找不到 config.json，终止执行。")
    exit(1)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DOMAIN = config.get("domain", "https://yourdomain.com")
CATEGORY_CSS = config.get("category_css", "style.css")

# === 模板结构 ===
html_template = """<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <h1>{category}</h1>
  {image_blocks}
  <div>{ad_block}</div>
</body>
</html>"""

image_block_template = """
<div class="image-block">
  <img src="{img_src}" alt="{alt}">
  <p>{alt}</p>
</div>
"""

ad_block_script = "<script src='https://example-adnetwork.com/script.js'></script>"

# === 工具函数 ===
def load_keywords(category):
    path = KEYWORDS_DIR / f"{category}.txt"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def generate_meta_keywords(keywords, count=5):
    return ", ".join(random.sample(keywords, min(len(keywords), count))) if keywords else ""

# === 主逻辑 ===
for folder in sorted(BASE_DIR.iterdir()):
    if not folder.is_dir() or folder.name in EXCLUDE_DIRS or folder.name.startswith("."):
        continue

    print(f"👉 正在处理分类：{folder.name}")
    category = folder.name
    keywords = load_keywords(category)
    if not keywords:
        print(f"⚠️ 无关键词，跳过：{category}")
        continue

    image_files = sorted([f for f in folder.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    if not image_files:
        print(f"⚠️ 无图片，跳过：{category}")
        continue

    image_blocks = ""
    for i, img in enumerate(image_files):
        img_src = f"{category}/{img.name}"
        alt_text = random.choice(keywords) if keywords else img.stem
        image_blocks += image_block_template.format(img_src=img_src, alt=alt_text)

    meta_keywords = generate_meta_keywords(keywords, 8)
    description = f"Discover {category} style images: {meta_keywords}"
    title = f"{category.capitalize()} - Realistic AI Gallery"
    css_path = CATEGORY_CSS

    html = html_template.format(
        title=title,
        description=description,
        keywords=meta_keywords,
        css=css_path,
        category=category.capitalize(),
        image_blocks=image_blocks,
        ad_block=ad_block_script
    )

    page_name = f"{category}.html"
    with open(BASE_DIR / page_name, "w", encoding="utf-8") as f:
        f.write(html)

    SITEMAP_ENTRIES.append(f"{DOMAIN}/{page_name}")

# === 写 sitemap.xml ===
now = datetime.utcnow().strftime("%Y-%m-%d")
with open(BASE_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in SITEMAP_ENTRIES:
        f.write(f"  <url><loc>{url}</loc><lastmod>{now}</lastmod></url>\n")
    f.write("</urlset>")

# === Ping Google 通知更新 ===
try:
    ping_url = f"https://www.google.com/ping?sitemap={DOMAIN}/sitemap.xml"
    requests.get(ping_url)
    print("✅ 已通知 Google 爬虫更新 sitemap")
except Exception as e:
    print("❌ Google Ping 失败：", e)
