# 计算机考试刷题备考系统 - Linux部署指南

## 系统要求
- Python 3.7 或更高版本
- pip 包管理工具
- Linux 操作系统

## 安装步骤

1. 克隆或下载项目到本地

2. 进入项目目录
```bash
cd 计算机考试刷图备考系统
```

3. 创建并激活虚拟环境（可选但推荐）
```bash
python -m venv venv
source venv/bin/activate
```

4. 安装依赖
```bash
pip install -r requirements.txt
```

5. 使脚本可执行
```bash
chmod +x start_app.sh
```

## 启动应用

使用以下命令启动应用：
```bash
./start_app.sh
```

或者直接使用：
```bash
python -m streamlit run app.py
```

应用将在浏览器中打开，默认地址为 http://localhost:8501

## 侧边栏导航

本应用已经配置为使用侧边栏导航，与Linux系统更加兼容。登录后，您可以通过侧边栏访问所有功能。 