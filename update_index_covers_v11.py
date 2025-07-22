import os
import re
from bs4 import BeautifulSoup

# 当前目录路径
root_path = os.getcwd()
index_file = os.path.join(root_path, 'index.html')

# 排除非分类文件夹
exclude_dirs = {'.git', 'generator', 'images', 'keywords', '__pycache__'}

# 支持的图片扩展名
exts = {'.jpg', '.jpeg', '.png', '.webp'}

# 遍历一级文件夹，识别为分类
def get_category_folders():
    return [name for name in os.listdir(root_path)
            if os.path.isdir(os.path.join(root_path, name)) and name not in exclude_dirs]

# 找到文件夹中最新的图片
def find_latest_image(folder):
    folder_path = os.path.join(root_path, folder)
    images = [f for f in os.listdir(folder_path)
              if os.path.splitext(f)[1].lower() in exts]
    if not images:
        return None
    images.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)
    return os.path.join(folder, images[0])  # 返回相对路径

# 更新 index.html 中对应 <img src="xxx"> 内容
def update_index_html(category_to_img):
    with open(index_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 查找所有 <img> 标签，替换 src
    changed = False
    for img in soup.find_all('img'):
        src = img.get('src', '')
        match = re.search(r'^(\w+)/', src)
        if match:
            folder = match.group(1)
            if folder in category_to_img:
                img['src'] = category_to_img[folder]
                changed = True

    if changed:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("✅ index.html 已更新封面图。")
    else:
        print("⚠️ 没有找到需要更新的 <img> 标签。")

if __name__ == "__main__":
    folders = get_category_folders()
    mapping = {}
    for folder in folders:
        latest = find_latest_image(folder)
        if latest:
            mapping[folder] = latest
            print(f"✔ 分类 [{folder}] 更新为最新封面：{latest}")
        else:
            print(f"⚠️ 分类 [{folder}] 没有找到图片，跳过")
    update_index_html(mapping)
