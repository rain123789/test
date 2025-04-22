import os
import sys
import subprocess
import time

def install_dependencies():
    print("检查和安装依赖项...")
    
    # List of required packages from requirements.txt
    required_packages = [
        "streamlit==1.32.0",
        "pandas==2.2.0",
        "plotly==5.18.0",
        "matplotlib==3.8.2",
        "numpy==1.26.3",
        "pillow==10.2.0",
        "streamlit-option-menu==0.3.6",
        "streamlit-card==0.0.61",
        "streamlit-echarts==0.4.0"
    ]
    
    # Install each package individually
    for package in required_packages:
        print(f"安装 {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ 安装 {package} 失败: {e}")
    
    print("依赖项安装完成。")

def run_application():
    print("\n初始化数据库...")
    if not os.path.exists('exam_system.db'):
        try:
            # Run database initialization
            subprocess.check_call([sys.executable, "init_db.py"])
            print("数据库初始化完成！")
        except subprocess.CalledProcessError as e:
            print(f"数据库初始化失败: {e}")
            return False
    else:
        print("数据库已存在，跳过初始化步骤。")
    
    print("\n启动应用程序...")
    try:
        subprocess.check_call([sys.executable, "-m", "streamlit", "run", "app.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"应用程序启动失败: {e}")
        return False

def main():
    print("=" * 50)
    print("计算机考试刷题备考系统安装和运行脚本")
    print("=" * 50)
    
    # Install dependencies first
    install_dependencies()
    
    # Wait a moment to ensure all installations are complete
    time.sleep(2)
    
    # Run the application
    print("\n准备启动应用...")
    success = run_application()
    
    if not success:
        print("\n应用启动失败。请手动使用以下命令启动:")
        print("python -m streamlit run app.py")
        
        # Wait for user input before closing
        input("按回车键退出...")

if __name__ == "__main__":
    main() 