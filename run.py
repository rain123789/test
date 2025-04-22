import os
import sys
import subprocess
import database as db
import traceback

def main():
    print("欢迎使用计算机考试刷题备考系统!")
    
    # Check if database exists
    if not os.path.exists('exam_system.db'):
        print("初始化数据库中...")
        try:
            from init_db import main as init_db_main
            init_db_main()
            print("数据库初始化完成!")
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            traceback.print_exc()
            return
    
    # Run Streamlit app
    print("启动应用程序...")
    try:
        # Try to import streamlit first to check if it's installed
        import streamlit
        print(f"Streamlit版本: {streamlit.__version__}")
        
        # Use Python module to run streamlit
        print("正在启动Streamlit...")
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Streamlit启动失败，返回码: {result.returncode}")
            print("标准输出:")
            print(result.stdout)
            print("标准错误:")
            print(result.stderr)
    except ImportError:
        print("错误: Streamlit未安装或无法导入")
        print("请使用以下命令安装Streamlit和其他依赖项:")
        print("python -m pip install -r requirements.txt")
    except Exception as e:
        print(f"启动失败: {e}")
        traceback.print_exc()
        print("请确保已安装所有依赖项: python -m pip install -r requirements.txt")

if __name__ == "__main__":
    main() 