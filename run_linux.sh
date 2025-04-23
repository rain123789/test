#!/bin/bash

# 设置颜色
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}计算机考试刷题备考系统启动器${NC}"
echo "=============================="
echo ""

# 检测Python路径
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误: 未找到Python。请先安装Python 3.7+${NC}"
    exit 1
fi

echo -e "${YELLOW}使用: $($PYTHON_CMD --version)${NC}"
echo ""

# 检查是否在虚拟环境中
if [ -d ".venv" ] && [ -f ".venv/bin/python" ]; then
    echo -e "${YELLOW}检测到虚拟环境，是否使用? [Y/n]${NC}"
    read -r USE_VENV
    if [[ ! $USE_VENV =~ ^[Nn]$ ]]; then
        PYTHON_CMD=".venv/bin/python"
        echo -e "${GREEN}使用虚拟环境中的Python${NC}"
    fi
fi

# 检查依赖
if ! $PYTHON_CMD -c "import streamlit" &> /dev/null; then
    echo -e "${YELLOW}未检测到Streamlit，是否安装依赖? [Y/n]${NC}"
    read -r INSTALL_DEPS
    if [[ ! $INSTALL_DEPS =~ ^[Nn]$ ]]; then
        echo -e "${YELLOW}安装依赖...${NC}"
        $PYTHON_CMD -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}依赖安装失败，请手动运行: $PYTHON_CMD -m pip install -r requirements.txt${NC}"
            exit 1
        fi
        echo -e "${GREEN}依赖安装完成${NC}"
    else
        echo -e "${YELLOW}跳过依赖安装，可能导致运行失败${NC}"
    fi
fi

echo ""
echo -e "${YELLOW}1. 正在更新用户界面...${NC}"
# 运行更新UI脚本
$PYTHON_CMD update_ui_sidebar.py
if [ $? -ne 0 ]; then
    echo -e "${RED}更新界面失败${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}2. 正在启动应用程序...${NC}"
echo ""
echo "提示: 如果浏览器没有自动打开，请手动访问下面显示的网址"
echo ""

# 启动Streamlit应用
$PYTHON_CMD -m streamlit run app.py

echo ""
echo -e "${GREEN}程序已退出${NC}" 