import os

base_dir = os.path.abspath(os.path.dirname(__file__))
output_dir = base_dir
image_extensions = [".jpg", ".jpeg", ".png"]
exclude_folders = {"assets", "pages", "generator", "__pycache__"}

def generate_gallery_html(category, image_files):
    image_tags = ""
    for img in sorted(image_files):
        rel_path = os.path.join(category, img).replace("\\", "/")
        image_tags += f'<div class="thumb"><a href="{rel_path}"><img src="{rel_path}" loading="lazy"></a></div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{category.capitalize()} Gallery</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #111; color: #fff; margin: 0; padding: 1em; }}
    .gallery {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .thumb img {{ width: 200px; height: auto; border-radius: 8px; box-shadow: 0 0 6px #000; }}
    a {{ text-decoration: none; color: #aaa; }}
    .back {{ margin-bottom: 20px; display: inline-block; }}
  </style>
</head>
<body>
  <a class="back" href="index.html">← Back to Home</a>
  <h1>{category.capitalize()} Gallery</h1>
  <div class="gallery">
    {image_tags}
  </div>
</body>
</html>
"""
    return html

def main():
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path) or folder in exclude_folders:
            continue

        image_files = [f for f in os.listdir(folder_path)
                       if os.path.splitext(f)[1].lower() in image_extensions]

        if image_files:
            html = generate_gallery_html(folder, image_files)
            html_path = os.path.join(output_dir, f"{folder}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ 已生成页面：{folder}.html")

if __name__ == "__main__":
    main()
