@echo off
setlocal

git add .
git commit -m "Auto update"
git push origin main

endlocal
pause
