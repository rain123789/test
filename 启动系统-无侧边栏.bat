@echo off
echo 计算机考试刷题备考系统启动器
echo ==============================
echo.
echo 1. 正在更新用户界面...
python update_ui.py
echo.
echo 2. 正在启动应用程序...
echo.
echo 提示: 如果浏览器没有自动打开，请手动访问下面显示的网址
echo.
python -m streamlit run app.py
echo.
echo 按任意键退出...
pause > nul 