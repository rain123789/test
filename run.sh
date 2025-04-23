#!/bin/bash

echo "计算机考试刷题备考系统启动中..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3未安装，请先安装Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "错误: pip3未安装，请先安装pip3"
    exit 1
fi

# 检查streamlit是否安装
if ! pip3 list | grep streamlit &> /dev/null; then
    echo "正在安装Streamlit..."
    pip3 install -r requirements.txt
fi

# 检查是否首次启动
if [ ! -f ".first_run_complete" ]; then
    echo "首次启动系统，正在安装依赖..."
    pip3 install -r requirements.txt
    touch .first_run_complete
    echo "安装完成！"
fi

# 启动应用
echo "正在启动应用，请在浏览器中访问 http://localhost:8501"
python3 -m streamlit run app.py 