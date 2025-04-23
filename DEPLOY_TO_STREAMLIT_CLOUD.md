# 在Streamlit Cloud上部署计算机考试刷题备考系统

本指南将帮助您将系统成功部署到Streamlit Cloud平台，以便在线访问您的应用程序。

## 错误排查

如您在部署过程中遇到了AttributeError，这是因为Streamlit API的变更。旧版使用的`st.experimental_rerun()`在新版中已更改为`st.rerun()`。我们提供了修复脚本来解决这个问题。

## 部署前的准备工作

1. **运行修复脚本**：
   ```bash
   # 在项目根目录运行
   python fix_streamlit_api.py
   ```
   这将自动扫描并替换所有过时的API调用。

2. **运行部署准备脚本**：
   ```bash
   python cloud_deploy.py
   ```
   这个脚本会生成所需的配置文件，并确保项目结构符合Streamlit Cloud的部署要求。

3. **检查requirements.txt**：
   确保它包含所有必要的依赖，特别是新版本的Streamlit：
   ```
   streamlit>=1.27.0
   pandas
   plotly
   matplotlib
   numpy
   pillow
   streamlit-option-menu
   streamlit-card
   streamlit-echarts
   ```

## 部署到Streamlit Cloud

### 方法1：通过GitHub部署（推荐）

1. **创建GitHub仓库**：
   - 在GitHub上创建新仓库
   - 将本地项目推送到GitHub:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin 您的仓库地址
     git push -u origin main
     ```

2. **在Streamlit Cloud中部署**：
   - 登录[Streamlit Cloud](https://streamlit.io/cloud)
   - 点击"New app"按钮
   - 选择GitHub仓库和分支
   - 设置主Python文件为：`streamlit_app.py`
   - 点击"Deploy"按钮

### 方法2：直接上传（仅适用于小型项目）

1. 登录[Streamlit Cloud](https://streamlit.io/cloud)
2. 点击"New app"按钮
3. 选择"Upload a folder"选项
4. 上传整个项目文件夹
5. 设置主Python文件为：`streamlit_app.py`
6. 点击"Deploy"按钮

## 配置密钥（如有需要）

如果您的应用需要保密信息（数据库凭据、API密钥等）：

1. 在Streamlit Cloud的应用设置中，找到"Secrets"部分
2. 根据`.streamlit/secrets.example.toml`的格式，配置您的密钥

## 添加数据库（如适用）

Streamlit Cloud支持持久存储，但对于SQLite数据库，您需要特别注意：

1. 确保数据库文件位于项目中，且已提交到GitHub
2. 在应用中使用相对路径访问数据库
3. 注意，Streamlit Cloud重启时数据库将重置为提交到GitHub时的状态

对于需要保持数据更新的应用，建议迁移到云数据库服务（如PostgreSQL、MySQL等）。

## 常见问题解决

### 1. API调用错误

如果遇到AttributeError或其他API错误：
- 再次运行`fix_streamlit_api.py`
- 检查是否有其他使用了过时API的代码

### 2. 模块导入错误

如果遇到导入模块错误：
- 确保`streamlit_app.py`中的代码正确设置了导入路径
- 检查模块名称是否正确，大小写匹配

### 3. 数据库连接问题

如果遇到数据库连接错误：
- 检查数据库文件路径是否正确
- 考虑使用`st.cache`减少数据库操作

## 后续维护

成功部署后，您可以：
1. 通过GitHub更新代码（自动部署）
2. 监控应用使用情况
3. 根据需要调整资源配置

---

如有任何部署问题，请参阅[Streamlit文档](https://docs.streamlit.io/streamlit-cloud)或在GitHub上提交Issue。 