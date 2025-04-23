import os
import sys
import platform
import subprocess
import database as db
import traceback

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux, macOS, etc.
        os.system('clear')

def set_encoding():
    """Set the console encoding to UTF-8."""
    if platform.system() == "Windows":
        # On Windows, ensure UTF-8 encoding
        os.system("chcp 65001 > nul")
    
    # For Python 3, this ensures encoding in stdin/stdout
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8')

def make_executable(script_path):
    """Make a script executable on Unix-like systems."""
    if platform.system() != "Windows":
        os.chmod(script_path, 0o755)

def main():
    """Main function that launches the application based on the platform."""
    set_encoding()
    clear_screen()
    
    print("计算机考试刷题备考系统启动器")
    print("==============================")
    print("")
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Ensure the shell script is executable on Unix-like systems
    if platform.system() != "Windows":
        shell_script = os.path.join(current_dir, "start_app.sh")
        make_executable(shell_script)
    
    print("1. 正在更新用户界面...")
    # Run the UI update script directly
    subprocess.run([sys.executable, "update_ui_sidebar.py"], check=True)
    print("")
    
    print("2. 正在启动应用程序...")
    print("")
    print("提示: 如果浏览器没有自动打开，请手动访问下面显示的网址")
    print("")
    
    # Start the Streamlit app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    
    # Exit message
    print("")
    if platform.system() == "Windows":
        print("程序已退出。按任意键关闭窗口...")
        os.system("pause > nul")
    else:
        print("程序已退出。")

if __name__ == "__main__":
    main() 