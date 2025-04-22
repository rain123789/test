import streamlit as st
import database as db
import json
import os

# 保存会话状态的文件路径
SESSION_FILE = '.session_state.json'

def init_auth():
    """初始化认证状态，并尝试从文件恢复会话状态"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
        
    # 尝试从文件恢复会话状态
    load_session_state()

def login(username, password):
    """用户登录，验证成功后保存状态"""
    user = db.verify_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_id = user['id']
        st.session_state.username = user['username']
        st.session_state.is_admin = bool(user['is_admin'])
        
        # 登录成功后保存会话状态
        save_session_state()
        return True
    return False

def logout():
    """用户登出，清除会话状态"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    
    # 清除保存的会话状态
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def is_logged_in():
    """检查用户是否已登录"""
    return st.session_state.logged_in

def is_admin():
    """检查用户是否是管理员"""
    return st.session_state.is_admin

def get_current_user():
    """获取当前登录用户信息"""
    if not is_logged_in():
        return None
    return {
        'id': st.session_state.user_id,
        'username': st.session_state.username,
        'is_admin': st.session_state.is_admin
    }

def register(username, password, email=None):
    """注册新用户"""
    return db.create_user(username, password, email)

def login_required(func):
    """登录验证装饰器"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.error("请先登录")
            st.session_state.page = 'login'
            st.experimental_rerun()
            return None
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """管理员验证装饰器"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.error("请先登录")
            st.session_state.page = 'login'
            st.experimental_rerun()
            return None
        if not is_admin():
            st.error("您没有访问该页面的权限")
            return None
        return func(*args, **kwargs)
    return wrapper

def save_session_state():
    """保存会话状态到文件"""
    session_data = {
        'logged_in': st.session_state.logged_in,
        'user_id': st.session_state.user_id,
        'username': st.session_state.username,
        'is_admin': st.session_state.is_admin,
        'page': st.session_state.get('page', 'login')
    }
    
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
    except Exception as e:
        print(f"保存会话状态失败: {e}")

def load_session_state():
    """从文件加载会话状态"""
    if not os.path.exists(SESSION_FILE):
        return
    
    try:
        with open(SESSION_FILE, 'r') as f:
            session_data = json.load(f)
            
        # 恢复会话状态
        st.session_state.logged_in = session_data.get('logged_in', False)
        st.session_state.user_id = session_data.get('user_id')
        st.session_state.username = session_data.get('username')
        st.session_state.is_admin = session_data.get('is_admin', False)
        
        # 恢复页面状态
        if 'page' in session_data:
            st.session_state.page = session_data['page']
    except Exception as e:
        print(f"加载会话状态失败: {e}")

# 在页面状态改变时保存会话
def update_page_state(new_page):
    """更新页面状态并保存"""
    st.session_state.page = new_page
    save_session_state()

def show_login_form():
    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")
        
        if submit:
            if login(username, password):
                st.success("登录成功！")
                st.experimental_rerun()
            else:
                st.error("用户名或密码错误")
    
    st.markdown("还没有账号？")
    if st.button("注册新账号"):
        st.session_state.show_register = True
    
    if st.session_state.get('show_register', False):
        show_register_form()

def show_register_form():
    with st.form("register_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        confirm_password = st.text_input("确认密码", type="password")
        email = st.text_input("邮箱(可选)")
        submit = st.form_submit_button("注册")
        
        if submit:
            if not username or not password:
                st.error("用户名和密码不能为空")
            elif password != confirm_password:
                st.error("两次输入的密码不一致")
            else:
                if register(username, password, email):
                    st.success("注册成功！请登录")
                    st.session_state.show_register = False
                    st.experimental_rerun()
                else:
                    st.error("用户名已存在") 