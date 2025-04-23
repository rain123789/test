#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
from pathlib import Path

# 颜色定义 (ANSI escape sequences)
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_color(text, color):
    """打印彩色文本"""
    is_windows = platform.system() == "Windows"
    # Windows命令行不支持ANSI颜色
    if is_windows and not "WT_SESSION" in os.environ and not "TERM_PROGRAM" in os.environ:
        print(text)
    else:
        print(f"{color}{text}{Colors.END}")

def run_command(cmd, shell=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, encoding='utf-8')
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except Exception as e:
        return False, str(e)

def check_python_version():
    """检查Python版本"""
    print_color("检查Python版本...", Colors.YELLOW)
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_color(f"错误: 需要Python 3.7或更高版本（当前版本：{sys.version}）", Colors.RED)
        return False
    
    print_color(f"Python版本检查通过：{sys.version}", Colors.GREEN)
    return True

def create_virtual_env():
    """创建虚拟环境"""
    print_color("是否创建虚拟环境? (推荐) [y/N]: ", Colors.YELLOW)
    choice = input().strip().lower()
    
    if choice == 'y':
        print_color("创建虚拟环境...", Colors.YELLOW)
        venv_path = Path(".venv")
        
        if venv_path.exists():
            print_color("虚拟环境已存在，跳过创建步骤", Colors.BLUE)
        else:
            success, output = run_command([sys.executable, "-m", "venv", ".venv"])
            if not success:
                print_color(f"创建虚拟环境失败: {output}", Colors.RED)
                return False
            print_color("虚拟环境已创建", Colors.GREEN)
        
        # 返回激活脚本路径
        if platform.system() == "Windows":
            return str(venv_path / "Scripts" / "python.exe")
        else:
            return str(venv_path / "bin" / "python")
    return sys.executable

def install_dependencies(python_exe):
    """安装依赖"""
    print_color("安装依赖...", Colors.YELLOW)
    
    cmd = [python_exe, "-m", "pip", "install", "-r", "requirements.txt"]
    success, output = run_command(cmd, shell=False)
    
    if not success:
        print_color(f"安装依赖失败: {output}", Colors.RED)
        return False
    
    print_color("依赖安装完成", Colors.GREEN)
    return True

def setup_permissions():
    """设置权限（仅限Unix系统）"""
    if platform.system() != "Windows":
        print_color("设置启动脚本权限...", Colors.YELLOW)
        success, _ = run_command("chmod +x start_app.sh")
        if success:
            print_color("权限设置完成", Colors.GREEN)
        else:
            print_color("权限设置失败，请手动执行: chmod +x start_app.sh", Colors.RED)

def main():
    """主函数"""
    print_color("计算机考试刷题备考系统 - 安装向导", Colors.BLUE + Colors.BOLD)
    print("========================================")
    print("")
    
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 创建虚拟环境
    python_exe = create_virtual_env()
    print("")
    
    # 安装依赖
    if not install_dependencies(python_exe):
        return
    print("")
    
    # 设置权限
    setup_permissions()
    print("")
    
    # 安装完成
    print_color("安装完成！", Colors.GREEN + Colors.BOLD)
    print("")
    print("运行方式:")
    if platform.system() == "Windows":
        print("  1. 双击 start_app.bat")
        print("  2. 运行: python run.py")
    else:
        print("  1. 运行: ./start_app.sh")
        print("  2. 运行: python run.py")
    print("")
    print_color("感谢使用计算机考试刷题备考系统！", Colors.BLUE)

if __name__ == "__main__":
    main() 