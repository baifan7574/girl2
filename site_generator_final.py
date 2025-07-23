import os
import math
import re
from pathlib import Path
from bs4 import BeautifulSoup

exts = ['.jpg', '.jpeg', '.png', '.webp']

def insert_ads(soup):
    if soup.body and not soup.find('script', src='ads.js'):
        ads = soup.new_tag('script', src='ads.js')
        soup.body.append(ads)

def load_keywords(category):
    try:
        with open(f'keywords/{category}.txt', 'r', encoding='utf-8') as f:
            return [kw.strip() for kw in f if kw.strip()]
    except:
        return []

def get_category_folders():
    return [d for d in os.listdir() if os.path.isdir(d) and not d.startswith('.') and d.lower() not in ['images', 'generator', 'keywords']]

def find_latest_images(folder, count=4):
    images = []
    for file in os.listdir(folder):
        if os.path.splitext(file)[1].lower() in exts:
            path = os.path.join(folder, file)
            images.append((file, os.path.getmtime(path)))
    images.sort(key=lambda x: x[1], reverse=True)
    return [img[0] for img in images[:count]]

def update_index_html(index_path='index.html'):
    if not os.path.exists(index_path):
        print('❌ index.html 不存在')
        return
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
    for folder in get_category_folders():
        latest_imgs = find_latest_images(folder, count=4)
        if len(latest_imgs) == 0:
            continue
        pattern = re.compile(rf'(<h2>{folder.capitalize()}</h2>\s*<div class="gallery">)(.*?)(</div>)', re.DOTALL)
        new_block = ''
        for img in latest_imgs:
            new_block += f'<a data-lightbox="{folder}" href="{folder}/{img}"><img alt="" src="{folder}/{img}"/></a>\n'
        def replacer(m):
            return f"{m.group(1)}\n{new_block}{m.group(3)}"
        html = pattern.sub(replacer, html)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_pages():
    categories = get_category_folders()
    for cat in categories:
        folder = Path(cat)
        images = sorted([f for f in folder.glob('*.jpg')])
        keywords = load_keywords(cat)
        per_page = 20
        total_pages = math.ceil(len(images) / per_page)
        for page in range(total_pages):
            start = page * per_page
            end = start + per_page
            imgs = images[start:end]
            page_file = folder / f'page{page+1}.html'
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(f'<html><head><title>{cat} - Page {page+1}</title></head><body>')
                for idx, img_path in enumerate(imgs):
                    name = img_path.stem
                    html_file = folder / f'{name}.html'
                    kw = keywords[start+idx] if start+idx < len(keywords) else ''
                    with open(html_file, 'w', encoding='utf-8') as imgf:
                        imgf.write(f'<html><head><title>{kw}</title><meta name="description" content="{kw}"></head><body>')
                        imgf.write(f'<h1>{kw}</h1><img src="{img_path.name}" alt="{kw}" style="max-width:100%"/><br>')
                        imgf.write(f'<div><a href="page{page+1}.html">Back to List</a> | <a href="../index.html">Home</a></div>')
                        imgf.write('</body></html>')
                    soup = BeautifulSoup(open(html_file, encoding='utf-8'), 'html.parser')
                    insert_ads(soup)
                    with open(html_file, 'w', encoding='utf-8') as imgf:
                        imgf.write(str(soup))
                    f.write(f'<a href="{name}.html"><img src="{img_path.name}" width=200></a>\n')
                f.write('<div style="margin-top:20px">')
                if page > 0:
                    f.write(f'<a href="page{page}.html">Previous</a> ')
                f.write(f'<a href="../index.html">Home</a> ')
                if page < total_pages - 1:
                    f.write(f'<a href="page{page+2}.html">Next</a>')
                f.write('</div></body></html>')

def generate_sitemap():
    with open('sitemap.xml', 'w', encoding='utf-8') as sm:
        sm.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for cat in get_category_folders():
            folder = Path(cat)
            for file in folder.glob('*.html'):
                sm.write(f'<url><loc>https://example.com/{cat}/{file.name}</loc></url>\n')
        sm.write('</urlset>')

if __name__ == '__main__':
    update_index_html()
    generate_pages()
    generate_sitemap()
    print('✅ 所有页面生成完毕，包含：首页更新、分页、关键词、广告、导航与 sitemap ✅')