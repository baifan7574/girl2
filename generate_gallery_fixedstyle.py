import os
import glob
from pathlib import Path

base_dir = Path(__file__).resolve().parent
template_file = base_dir / "custom_homepage_template.html"
output_file = base_dir / "index.html"
images_per_category = 4
exclude_dirs = {"generator", "pages", "single", "assets", "__pycache__"}

def build_category_section(category, image_paths):
    thumbs = ""
    for img_path in image_paths[:images_per_category]:
        filename = os.path.basename(img_path)
        thumbs += f'<a href="{category}/{filename}" data-lightbox="{category}"><img src="{category}/{filename}" alt=""></a>\n'
    section = f"""<!-- {category.capitalize()} Section -->
<div class="section">
  <h2>{category.capitalize()}</h2>
  <div class="gallery">
    {thumbs.strip()}
  </div>
  <div class="more"><a href="{category}.html">→ View More</a></div>
</div>
"""
    return section

def main():
    if not template_file.exists():
        print("❌ 模板文件不存在：", template_file)
        return

    sections = []
    for folder in sorted(base_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith(".") or folder.name in exclude_dirs:
            continue
        images = sorted(glob.glob(str(folder / "*.jpg")))
        if images:
            sections.append(build_category_section(folder.name, images))

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    final_output = template.replace("{category_blocks}", "\n".join(sections))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_output)

    print("✅ 已生成固定结构主页：index.html")

if __name__ == "__main__":
    main()