
import os
import re

# 允许的图片扩展名
exts = ['.jpg', '.jpeg', '.png', '.webp']

# 获取所有分类文件夹（排除非图像类的目录）
def get_category_folders():
    return [d for d in os.listdir() if os.path.isdir(d) and not d.startswith(".") and d.lower() not in ['images', 'generator', 'keywords']]

# 找到文件夹中最新的n张图
def find_latest_images(folder, count=4):
    images = []
    for file in os.listdir(folder):
        if os.path.splitext(file)[1].lower() in exts:
            path = os.path.join(folder, file)
            images.append((file, os.path.getmtime(path)))
    images.sort(key=lambda x: x[1], reverse=True)
    return [img[0] for img in images[:count]]

# 替换主页封面图为每类最新4张图
def update_index_html(index_path='index.html'):
    if not os.path.exists(index_path):
        print("❌ index.html 不存在")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    for folder in get_category_folders():
        latest_imgs = find_latest_images(folder, count=4)
        if len(latest_imgs) == 0:
            continue

        # 构建替换区域正则
        pattern = re.compile(
            rf'(<h2>{folder.capitalize()}</h2>\s*<div class="gallery">)(.*?)(</div>)',
            re.DOTALL
        )

        new_block = ""
        for img in latest_imgs:
            new_block += f'<a data-lightbox="{folder}" href="{folder}/{img}"><img alt="" src="{folder}/{img}"/></a>\n'

        def replacer(m):
            return f"{m.group(1)}\n{new_block}{m.group(3)}"

        html = pattern.sub(replacer, html)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ v11_multi 已完成：主页每类展示最新4张图，其他结构保持原样。")

update_index_html()
