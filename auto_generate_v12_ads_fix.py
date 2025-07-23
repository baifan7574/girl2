import os
from bs4 import BeautifulSoup

def inject_ads_script(soup):
    if not soup.body:
        return
    if not soup.find("script", src="ads.js"):
        ads_script = soup.new_tag("script", src="ads.js")
        soup.body.append(ads_script)

def process_html_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html") and file != "index.html":
                file_path = os.path.join(subdir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                inject_ads_script(soup)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))

if __name__ == "__main__":
    process_html_files(".")
    print("✅ 所有 HTML 文件已添加 ads.js 引用（不含 index.html）")
