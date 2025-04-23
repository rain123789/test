#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
import shutil

def ensure_dir(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def fix_streamlit_api():
    """
    修复Streamlit API变更问题，将所有st.experimental_rerun()替换为st.rerun()
    """
    print("修复Streamlit API...")
    
    # 定义要替换的模式
    pattern = r'st\.experimental_rerun\(\)'
    replacement = 'st.rerun()'
    
    # 定义要搜索的文件类型
    extensions = ['.py']
    
    # 计数器
    modified_files = 0
    
    # 遍历所有Python文件
    for root, _, files in os.walk('.'):
        for filename in files:
            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # 检查并替换
                    new_content, count = re.subn(pattern, replacement, content)
                    
                    if count > 0:
                        with open(filepath, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        modified_files += 1
                        print(f"  修复: {filepath} (替换了 {count} 处)")
                except Exception as e:
                    print(f"  错误: 处理 {filepath} 时出错: {e}")
    
    print(f"API修复完成! 修改了 {modified_files} 个文件")

def fix_auth_module():
    """修复auth.py中的装饰器函数"""
    if os.path.exists('auth.py'):
        try:
            with open('auth.py', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 修复login_required装饰器
            if 'def login_required(func):' in content:
                updated = False
                
                # 如果使用experimental_rerun
                if 'st.experimental_rerun()' in content:
                    content = content.replace('st.experimental_rerun()', 'st.rerun()')
                    updated = True
                
                # 确保导入了st
                if 'import streamlit as st' not in content:
                    content = 'import streamlit as st\n' + content
                    updated = True
                
                if updated:
                    with open('auth.py', 'w', encoding='utf-8') as file:
                        file.write(content)
                    print("  修复: auth.py")
        except Exception as e:
            print(f"  错误: 处理auth.py时出错: {e}")

def create_requirements():
    """确保requirements.txt文件存在且包含必要的依赖"""
    req_file = 'requirements.txt'
    required_packages = [
        'streamlit>=1.27.0',  # 使用较新版本的Streamlit
        'pandas',
        'plotly',
        'matplotlib',
        'numpy',
        'pillow',
        'streamlit-option-menu',
        'streamlit-card',
        'streamlit-echarts'
    ]
    
    existing_packages = []
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            existing_packages = [line.strip() for line in f.readlines() if line.strip()]
    
    # 合并现有依赖和必要依赖
    updated_packages = list(existing_packages)
    for package in required_packages:
        # 检查包名（不带版本号）
        pkg_name = package.split('>=')[0].split('==')[0].strip()
        
        # 检查包是否已存在
        if not any(pkg_name == existing.split('>=')[0].split('==')[0].strip() for existing in existing_packages):
            updated_packages.append(package)
    
    # 写入更新的依赖
    with open(req_file, 'w') as f:
        f.write('\n'.join(updated_packages))
    
    print(f"更新了依赖文件: {req_file}")

def create_streamlit_config():
    """创建Streamlit配置文件"""
    config_dir = '.streamlit'
    ensure_dir(config_dir)
    
    config_file = os.path.join(config_dir, 'config.toml')
    with open(config_file, 'w') as f:
        f.write("""[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
runOnSave = true
enableCORS = false

[browser]
gatherUsageStats = false
""")
    
    print(f"创建了Streamlit配置: {config_file}")

def create_streamlit_secrets():
    """创建Streamlit密钥文件模板（实际部署时需要手动配置）"""
    config_dir = '.streamlit'
    ensure_dir(config_dir)
    
    secrets_file = os.path.join(config_dir, 'secrets.example.toml')
    with open(secrets_file, 'w') as f:
        f.write("""# 这是一个示例密钥文件，部署到Streamlit Cloud时需要在Dashboard中配置这些密钥
[general]
app_name = "计算机考试刷题备考系统"

[admin]
username = "admin"
password = "admin"

# 其他可能需要的密钥配置
""")
    
    print(f"创建了密钥模板: {secrets_file}")

def create_gitignore():
    """创建.gitignore文件，排除不需要版本控制的文件"""
    with open('.gitignore', 'w') as f:
        f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/

# Streamlit
.streamlit/secrets.toml

# Database
*.db-journal

# OS specific
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo
""")
    
    print("创建了.gitignore文件")

def create_startup_script():
    """创建启动脚本，用于Streamlit Cloud部署"""
    with open('streamlit_app.py', 'w') as f:
        f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from pathlib import Path
import importlib
import sys

# 确保能正确导入本地模块
app_path = Path(__file__).parent
if str(app_path) not in sys.path:
    sys.path.append(str(app_path))

# 尝试导入应用主模块
try:
    import app
    # 运行应用
    app.main()
except Exception as e:
    st.error(f"应用启动失败: {e}")
    st.exception(e)
""")
    
    print("创建了Streamlit Cloud启动脚本")

def main():
    print("开始准备Streamlit Cloud部署...")
    
    # 修复API问题
    fix_streamlit_api()
    fix_auth_module()
    
    # 创建必要的配置文件
    create_requirements()
    create_streamlit_config()
    create_streamlit_secrets()
    create_gitignore()
    create_startup_script()
    
    print("\n部署准备完成!")
    print("请按照以下步骤完成部署:")
    print("1. 上传代码到GitHub仓库")
    print("2. 在Streamlit Cloud中创建新应用")
    print("3. 连接到GitHub仓库")
    print("4. 设置主文件为 'streamlit_app.py'")
    print("5. 如有必要，在Streamlit Cloud中配置密钥")

if __name__ == "__main__":
    main() 