#!/bin/bash

# 计算机考试刷题备考系统安装和运行脚本

# 设置颜色
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}计算机考试刷题备考系统 - 安装与运行${NC}"
echo "=================================="
echo ""

# 检查Python版本
echo -e "${YELLOW}检查Python版本...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误: 未找到Python。请先安装Python 3.7+${NC}"
    exit 1
fi

echo -e "使用: $($PYTHON_CMD --version)"
echo ""

# 确保pip可用
echo -e "${YELLOW}检查pip...${NC}"
if ! $PYTHON_CMD -m pip --version &>/dev/null; then
    echo "安装pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PYTHON_CMD get-pip.py
    rm get-pip.py
fi
echo -e "pip已就绪"
echo ""

# 检查是否需要创建虚拟环境
echo -e "${YELLOW}是否创建虚拟环境? (推荐)[y/N]${NC}"
read -r CREATE_VENV

if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo "安装venv模块..."
    $PYTHON_CMD -m pip install venv
    
    echo "创建虚拟环境..."
    $PYTHON_CMD -m venv .venv
    
    # 激活虚拟环境
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo -e "${GREEN}虚拟环境已激活${NC}"
    else
        echo "警告: 无法激活虚拟环境，继续使用系统Python"
    fi
fi

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
$PYTHON_CMD -m pip install -r requirements.txt
echo -e "${GREEN}依赖已安装${NC}"
echo ""

# 使启动脚本可执行
echo -e "${YELLOW}设置启动脚本权限...${NC}"
chmod +x start_app.sh
echo -e "${GREEN}权限已设置${NC}"
echo ""

# 运行应用
echo -e "${YELLOW}启动应用程序...${NC}"
echo ""
./start_app.sh 