@echo off
chcp 65001 >nul
echo 🚀 正在生成网站页面，请稍候...

python generate_site.py

echo ✅ 所有页面已生成完毕，按任意键关闭窗口...
pause >nul
