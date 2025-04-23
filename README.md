# 计算机考试刷题备考系统

这是一个用于计算机考试备考的刷题系统，支持多平台运行（Windows, Linux, macOS）。

## 系统功能

- 用户登录和注册
- 刷题练习
- 错题收集和复习
- 学习数据统计
- 个人信息管理
- 管理员题库管理
- 管理员用户管理

## 环境要求

- Python 3.7+
- 所需的Python包（见requirements.txt）

## 安装

1. 克隆或下载本仓库到本地
2. 安装所需的依赖:

```bash
pip install -r requirements.txt
```

## 运行方法

### 跨平台启动方式（推荐）

使用Python运行启动脚本:

```bash
python run.py
```

这个脚本会自动检测您的操作系统，并使用合适的方式启动应用程序。它会设置侧边栏导航，并启动Streamlit应用。

### Linux系统专用启动方法（推荐）

我们为Linux系统提供了专门的安装和启动脚本：

#### 首次安装

首次使用请运行安装脚本：

```bash
# 添加执行权限
chmod +x setup_linux.sh
# 运行安装脚本
./setup_linux.sh
```

安装脚本会：
- 检查Python版本并安装必要组件
- 创建虚拟环境（可选）
- 安装所有依赖
- 设置执行权限
- 创建桌面快捷方式（可选）

#### 日常启动

安装完成后，日常启动只需运行：

```bash
./run_linux.sh
```

或使用Python启动：

```bash
python run.py
```

### Windows系统

双击`start_app.bat`文件或在命令行中运行:

```cmd
start_app.bat
```

### macOS/其他Unix系统

在终端中运行:

```bash
chmod +x start_app.sh  # 添加执行权限（仅首次运行需要）
./start_app.sh
```

## 系统配置

- 默认使用SQLite数据库存储数据，数据库文件为`exam_system.db`
- 网页界面默认使用侧边栏导航
- 系统会自动在浏览器中打开应用，如未打开，请手动访问终端中显示的URL

## 管理员账号

- 用户名: admin
- 密码: admin

## 问题反馈

如有任何问题或建议，请提交issue或联系系统管理员。

## 许可证

[MIT License](LICENSE) 