#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

def backup_file(file_path):
    """创建文件备份"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        with open(file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())
        print(f"已创建备份: {backup_path}")
        return True
    return False

def fix_practice_py():
    """修复practice.py文件中的API调用"""
    file_path = "pages/practice.py"
    if not os.path.exists(file_path):
        print(f"错误: 未找到文件 {file_path}")
        if os.path.exists("pages"):
            print("pages目录中的文件:")
            for f in os.listdir("pages"):
                print(f"  - {f}")
        return False

    # 备份文件
    backup_file(file_path)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换API调用
    content_new = content.replace("st.experimental_rerun()", "st.rerun()")
    
    # 更新文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f"已修复 {file_path} 中的API调用")
    return True

def fix_auth_py():
    """修复auth.py文件中的API调用"""
    file_path = "auth.py"
    if not os.path.exists(file_path):
        print(f"错误: 未找到文件 {file_path}")
        return False

    # 备份文件
    backup_file(file_path)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换API调用
    content_new = content.replace("st.experimental_rerun()", "st.rerun()")
    
    # 特别处理login_required装饰器函数
    if "def login_required(func):" in content_new:
        pattern = r'def login_required\(func\):(.*?)return wrapper'
        replacement = '''def login_required(func):
    """检查用户是否已登录的装饰器"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.session_state.page = 'login'
            st.rerun()  # 使用新版API
        return func(*args, **kwargs)
    return wrapper'''
        
        content_new = re.sub(pattern, replacement, content_new, flags=re.DOTALL)
    
    # 更新文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f"已修复 {file_path} 中的API调用")
    return True

def fix_app_py():
    """修复app.py文件中的API调用"""
    file_path = "app.py"
    if not os.path.exists(file_path):
        print(f"错误: 未找到文件 {file_path}")
        return False

    # 备份文件
    backup_file(file_path)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换API调用
    content_new = content.replace("st.experimental_rerun()", "st.rerun()")
    
    # 更新文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f"已修复 {file_path} 中的API调用")
    return True

def create_streamlit_app_py():
    """创建streamlit_app.py入口文件"""
    file_path = "streamlit_app.py"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import sys
from pathlib import Path

# 添加当前目录到导入路径
app_path = Path(__file__).parent
if str(app_path) not in sys.path:
    sys.path.append(str(app_path))

try:
    # 导入主应用
    import app
    
    # 运行主应用
    if __name__ == "__main__":
        app.main()
except Exception as e:
    st.error("应用程序启动失败")
    st.error(str(e))
    st.exception(e)
""")
    
    print(f"已创建 {file_path} 入口文件")
    return True

def main():
    print("开始修复API调用问题...")
    
    # 修复文件
    files_fixed = []
    if fix_practice_py():
        files_fixed.append("pages/practice.py")
    if fix_auth_py():
        files_fixed.append("auth.py")
    if fix_app_py():
        files_fixed.append("app.py")
    if create_streamlit_app_py():
        files_fixed.append("streamlit_app.py")
    
    # 总结
    if files_fixed:
        print("\n修复完成! 以下文件已更新:")
        for file in files_fixed:
            print(f"  - {file}")
        
        print("\n部署到Streamlit Cloud说明:")
        print("1. 确保所有文件都已添加到GitHub仓库")
        print("2. 部署时指定 'streamlit_app.py' 作为主文件")
        print("3. 如有数据库，确保在GitHub中包含数据库文件")
    else:
        print("\n未执行任何修复。请确认文件路径是否正确。")

if __name__ == "__main__":
    main() 