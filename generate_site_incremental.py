import os
import json
from datetime import datetime

# 读取配置
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

domain = config["domain"]
base_dir = os.getcwd()
keywords_dir = os.path.join(base_dir, "keywords")
output_dir = base_dir
existing_pages = set(p for p in os.listdir(output_dir) if p.startswith("image_") and p.endswith(".html"))

sitemap_entries = []

# 遍历分类文件夹
for category in os.listdir(base_dir):
    category_path = os.path.join(base_dir, category)
    if not os.path.isdir(category_path): continue
    if category in ["generator", "keywords", "luxury"]: continue
    images = [f for f in os.listdir(category_path) if f.lower().endswith((".jpg", ".png"))]
    if not images: continue

    # 读取关键词
    keyword_file = os.path.join(keywords_dir, f"{category}.txt")
    keywords = []
    if os.path.exists(keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as kf:
            keywords = [line.strip() for line in kf if line.strip()]

    print(f"📂 正在处理分类：{category}（共 {len(images)} 张图）")
    for i, img in enumerate(images):
        page_name = f"image_{category}_{i+1:04}.html"
        if page_name in existing_pages:
            continue
        img_path = f"{category}/{img}"
        kw = keywords[i % len(keywords)] if keywords else f"{category} photo {i+1}"

        html = f"""<!DOCTYPE html>
<html><head>
<meta charset='UTF-8'>
<title>{kw}</title>
<meta name='description' content='{kw} gallery photo'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
</head>
<body>
<h1>{kw}</h1>
<img src='{img_path}' alt='{kw}' style='max-width:100%;height:auto;'>
</body></html>
"""
        with open(os.path.join(output_dir, page_name), "w", encoding="utf-8") as f:
            f.write(html)
        sitemap_entries.append(f"{domain}/{page_name}")

    # 分类页也加到 sitemap
    cat_page = f"{category}.html"
    if os.path.exists(os.path.join(output_dir, cat_page)):
        sitemap_entries.append(f"{domain}/{cat_page}")

# 生成 sitemap.xml
sitemap_path = os.path.join(output_dir, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in sitemap_entries:
        f.write(f"<url><loc>{url}</loc><lastmod>{datetime.now().date()}</lastmod></url>\n")
    f.write("</urlset>")
print("✅ 增量生成完成，已更新 sitemap.xml")
