#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

def update_streamlit_api():
    """
    修复Streamlit API变更问题，将所有st.experimental_rerun()替换为st.rerun()
    """
    print("开始修复Streamlit API问题...")
    
    # 定义要替换的模式
    pattern = r'st\.experimental_rerun\(\)'
    replacement = 'st.rerun()'
    
    # 定义要搜索的文件类型
    file_types = ['*.py']
    
    # 计数器
    total_files = 0
    modified_files = 0
    total_replacements = 0
    
    # 遍历所有Python文件
    for file_type in file_types:
        for filepath in glob.glob(file_type, recursive=True):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                total_files += 1
                
                # 检查并替换
                new_content, count = re.subn(pattern, replacement, content)
                
                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    modified_files += 1
                    total_replacements += count
                    print(f"修复文件: {filepath} (替换了 {count} 处)")
            except Exception as e:
                print(f"处理文件 {filepath} 时出错: {e}")
    
    # 搜索子目录
    for dirpath, _, _ in os.walk('.'):
        if dirpath == '.':
            continue
        
        os.chdir(dirpath)
        
        for file_type in file_types:
            for filepath in glob.glob(file_type):
                try:
                    full_path = os.path.join(dirpath, filepath)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    total_files += 1
                    
                    # 检查并替换
                    new_content, count = re.subn(pattern, replacement, content)
                    
                    if count > 0:
                        with open(filepath, 'w', encoding='utf-8') as file:
                            file.write(new_content)
                        
                        modified_files += 1
                        total_replacements += count
                        print(f"修复文件: {full_path} (替换了 {count} 处)")
                except Exception as e:
                    print(f"处理文件 {full_path} 时出错: {e}")
        
        os.chdir('../')
    
    # 输出结果
    print("\n修复完成!")
    print(f"总共扫描: {total_files} 个文件")
    print(f"已修改: {modified_files} 个文件")
    print(f"总替换次数: {total_replacements} 处")
    
    if total_replacements > 0:
        print("\n请重新启动应用以应用更改。")
    else:
        print("\n没有发现需要修复的API调用。问题可能出在其他地方。")

    return total_replacements > 0

def update_auth_wrapper():
    """修复auth.py中的wrapper函数"""
    try:
        if os.path.exists('auth.py'):
            with open('auth.py', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 检查是否有需要修复的装饰器
            if 'def login_required(func):' in content:
                # 更新装饰器函数
                pattern = r'(def login_required\(func\):.*?return func\(\*args, \*\*kwargs\).*?return wrapper)'
                replacement = '''def login_required(func):
    """检查用户是否已登录的装饰器"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.session_state.page = 'login'
            st.rerun()  # 使用新版API
        return func(*args, **kwargs)
    return wrapper'''
                
                # 使用re.DOTALL模式匹配跨行内容
                new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
                
                if count > 0:
                    with open('auth.py', 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"修复文件: auth.py (更新了装饰器函数)")
                    return True
    except Exception as e:
        print(f"处理auth.py时出错: {e}")
    
    return False

if __name__ == "__main__":
    api_fixed = update_streamlit_api()
    auth_fixed = update_auth_wrapper()
    
    if api_fixed or auth_fixed:
        print("\n推荐重新启动应用程序以应用修复。")
    else:
        print("\n没有找到需要修复的内容，请检查错误是否有其他原因。") 