#!/bin/bash

# 计算机考试刷题备考系统 - Linux安装和配置脚本

# 设置颜色
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 获取当前脚本的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 打印带颜色的标题
echo -e "${BLUE}${BOLD}计算机考试刷题备考系统 - Linux安装和配置${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查Python版本
echo -e "${YELLOW}检查Python版本...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # 检查Python版本是否>=3.7
    PY_VERSION=$(python --version 2>&1 | awk '{print $2}')
    PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
    PY_MINOR=$(echo $PY_VERSION | cut -d. -f2)
    
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 7 ]; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}检测到的Python版本 ($PY_VERSION) 低于需求的3.7+${NC}"
        echo -e "${RED}请安装Python 3.7或更高版本${NC}"
        exit 1
    fi
else
    echo -e "${RED}错误: 未找到Python${NC}"
    echo -e "${YELLOW}请安装Python 3.7+:${NC}"
    echo "  - Debian/Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo "  - Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "  - Arch Linux: sudo pacman -S python python-pip"
    exit 1
fi

echo -e "${GREEN}使用: $($PYTHON_CMD --version)${NC}"
echo ""

# 检查pip
echo -e "${YELLOW}检查pip...${NC}"
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}未找到pip${NC}"
    echo -e "${YELLOW}正在尝试安装pip...${NC}"
    
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python-pip
    else
        echo -e "${RED}无法自动安装pip，请手动安装:${NC}"
        echo "  - 下载: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
        echo "  - 安装: $PYTHON_CMD get-pip.py"
        exit 1
    fi
    
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        echo -e "${RED}pip安装失败${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}pip已就绪: $($PYTHON_CMD -m pip --version)${NC}"
echo ""

# 创建虚拟环境
echo -e "${YELLOW}是否创建虚拟环境? [推荐] (Y/n):${NC}"
read -r CREATE_VENV

if [[ ! $CREATE_VENV =~ ^[Nn]$ ]]; then
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    
    # 确保venv模块可用
    if ! $PYTHON_CMD -m venv --help &> /dev/null; then
        echo -e "${YELLOW}安装venv模块...${NC}"
        if command -v apt &> /dev/null; then
            sudo apt install -y python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-venv
        elif command -v pacman &> /dev/null; then
            sudo pacman -S python-virtualenv
        else
            echo -e "${RED}无法安装venv模块，请手动安装后重试${NC}"
            exit 1
        fi
    fi
    
    # 如果.venv目录已存在，询问是否重新创建
    if [ -d ".venv" ]; then
        echo -e "${YELLOW}虚拟环境已存在，是否重新创建? (y/N):${NC}"
        read -r RECREATE_VENV
        if [[ $RECREATE_VENV =~ ^[Yy]$ ]]; then
            rm -rf .venv
            $PYTHON_CMD -m venv .venv
        fi
    else
        $PYTHON_CMD -m venv .venv
    fi
    
    # 激活虚拟环境
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        PYTHON_CMD=".venv/bin/python"
        echo -e "${GREEN}虚拟环境已激活${NC}"
    else
        echo -e "${RED}创建虚拟环境失败${NC}"
        exit 1
    fi
fi

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}依赖安装失败${NC}"
    exit 1
fi

echo -e "${GREEN}依赖安装完成${NC}"
echo ""

# 设置执行权限
echo -e "${YELLOW}设置脚本执行权限...${NC}"
chmod +x run_linux.sh
chmod +x start_app.sh

echo -e "${GREEN}权限设置完成${NC}"
echo ""

# 创建桌面快捷方式
echo -e "${YELLOW}是否创建桌面快捷方式? (y/N):${NC}"
read -r CREATE_SHORTCUT

if [[ $CREATE_SHORTCUT =~ ^[Yy]$ ]]; then
    DESKTOP_DIR="$HOME/Desktop"
    if [ ! -d "$DESKTOP_DIR" ]; then
        DESKTOP_DIR="$HOME/桌面"
    fi
    
    if [ -d "$DESKTOP_DIR" ]; then
        cat > "$DESKTOP_DIR/计算机考试刷题系统.desktop" << EOF
[Desktop Entry]
Type=Application
Name=计算机考试刷题系统
Comment=启动计算机考试刷题备考系统
Exec=bash -c "cd '$SCRIPT_DIR' && ./run_linux.sh"
Icon=
Terminal=true
Categories=Education;
EOF
        chmod +x "$DESKTOP_DIR/计算机考试刷题系统.desktop"
        echo -e "${GREEN}桌面快捷方式已创建${NC}"
    else
        echo -e "${YELLOW}未找到桌面目录，跳过创建快捷方式${NC}"
    fi
fi

# 安装完成
echo ""
echo -e "${GREEN}${BOLD}安装完成!${NC}"
echo ""
echo -e "运行方式:"
echo -e "  ${YELLOW}1. 运行: ./run_linux.sh${NC}"
echo -e "  ${YELLOW}2. 或者: $PYTHON_CMD run.py${NC}"
echo ""

# 询问是否立即启动
echo -e "${YELLOW}是否立即启动应用? (Y/n):${NC}"
read -r START_NOW

if [[ ! $START_NOW =~ ^[Nn]$ ]]; then
    ./run_linux.sh
fi 