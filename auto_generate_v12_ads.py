import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def get_latest_images(folder_path, count=4):
    exts = ['.jpg', '.jpeg', '.png', '.webp']
    images = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in exts]
    images.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    return images[:count]

def inject_ads_script(soup):
    if not soup.find("script", src="ads.js"):
        ads_script = soup.new_tag("script", src="ads.js")
        soup.body.append(ads_script)

def add_navigation(soup, index, total, category):
    nav_div = soup.new_tag("div", attrs={"class": "navigation"})

    if index > 1:
        prev_link = soup.new_tag("a", href=f"{category}_page{index-1}.html")
        prev_link.string = "← Previous"
        nav_div.append(prev_link)

    home_link = soup.new_tag("a", href="index.html")
    home_link.string = "🏠 Home"
    nav_div.append(home_link)

    if index < total:
        next_link = soup.new_tag("a", href=f"{category}_page{index+1}.html")
        next_link.string = "Next →"
        nav_div.append(next_link)

    soup.body.append(nav_div)

def process_html_file(filepath, index=None, total=None, category=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    inject_ads_script(soup)

    if index and total and category:
        add_navigation(soup, index, total, category)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def update_index_with_latest_images(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    section_divs = soup.find_all("div", class_="section")
    for section in section_divs:
        title = section.find("h2").text.strip()
        folder_name = title.lower()
        folder_path = os.path.join(os.path.dirname(index_path), folder_name)
        if not os.path.exists(folder_path):
            continue
        latest_images = get_latest_images(folder_path, count=4)
        gallery_div = section.find("div", class_="gallery")
        gallery_div.clear()
        for img_file in latest_images:
            a = soup.new_tag("a", href=f"{folder_name}/{img_file}", attrs={"data-lightbox": folder_name})
            img = soup.new_tag("img", src=f"{folder_name}/{img_file}", alt="")
            a.append(img)
            gallery_div.append(a)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def process_site():
    base_path = os.getcwd()
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                if "index.html" in filepath:
                    update_index_with_latest_images(filepath)
                elif re.match(r".+_page\d+.html", file):
                    match = re.match(r"(.+)_page(\d+).html", file)
                    if match:
                        category = match.group(1)
                        index = int(match.group(2))
                        total = len([f for f in os.listdir(root) if re.match(rf"{category}_page\d+.html", f)])
                        process_html_file(filepath, index=index, total=total, category=category)
                else:
                    process_html_file(filepath)

if __name__ == "__main__":
    process_site()
