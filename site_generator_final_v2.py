
import os
from datetime import datetime

def generate_html(folder, images, page_num, total_pages):
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{folder.capitalize()} Gallery - Page {page_num}</title>
<link href="../lightbox.min.css" rel="stylesheet" />
<script src="../lightbox-plus-jquery.js"></script>
<style>
body {{ background-color: #111; color: white; font-family: Arial, sans-serif; margin: 0; }}
h1 {{ text-align: center; padding: 30px 10px 0; }}
.gallery {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; padding: 20px; }}
.gallery img {{ width: 160px; border-radius: 6px; background: #333; cursor: pointer; }}
.nav {{ text-align: center; margin: 20px; }}
.nav a {{ color: #aaa; margin: 0 10px; text-decoration: none; }}
</style>
</head>
<body>
<h1>{folder.capitalize()}</h1>
<div class="gallery">
'''
    for img in images:
        html += f'<a href="{img}" data-lightbox="{folder}"><img src="{img}" alt=""></a>'
    html += "</div><div class='nav'>"
    if page_num > 1:
        html += f'<a href="page{page_num - 1}.html">← Previous</a>'
    if page_num < total_pages:
        html += f'<a href="page{page_num + 1}.html">Next →</a>'
    html += f'<a href="../index.html">🏠 Home</a>'
    html += "</div></body></html>"
    return html

def save_html(content, folder, filename):
    with open(os.path.join(folder, filename), 'w', encoding='utf-8') as f:
        f.write(content)

def process_folder(folder):
    if not os.path.exists(folder):
        print(f"❌ Skipped missing folder: {folder}")
        return

    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".jpg")])
    total_pages = (len(files) + 19) // 20

    for i in range(total_pages):
        chunk = files[i*20:(i+1)*20]
        html = generate_html(folder, chunk, i+1, total_pages)
        save_html(html, folder, f"page{i+1}.html")

if __name__ == "__main__":
    folders = [f for f in os.listdir() if os.path.isdir(f)]
    for folder in folders:
        process_folder(folder)
    print("✅ Gallery pages generated successfully.")
