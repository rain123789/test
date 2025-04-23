import streamlit as st
from streamlit_option_menu import option_menu
import database as db
import auth
from utils.ui import set_page_config, apply_custom_css, header

# Import pages
from pages.practice import practice_page
from pages.wrong_questions import wrong_questions_page
from pages.dashboard import dashboard_page
from pages.profile import profile_page
from pages.admin_question import admin_question_page
from pages.admin_user import admin_user_page

# Set page config
set_page_config()
apply_custom_css()

# Initialize authentication
auth.init_auth()

# Add page state to session if not exists
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def login_page():
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 400px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    header("计算机考试刷题备考系统")
    st.markdown("<p style='text-align: center;'>登录以开始学习</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")
        
        if submit:
            if auth.login(username, password):
                st.success("登录成功！")
                st.experimental_rerun()
            else:
                st.error("用户名或密码错误")
    
    st.markdown("<p style='text-align: center;'>还没有账号？</p>", unsafe_allow_html=True)
    if st.button("注册新账号"):
        auth.update_page_state('register')
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    st.markdown("""
    <style>
    .register-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 400px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="register-container">', unsafe_allow_html=True)
    header("注册新账号")
    
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
                if auth.register(username, password, email):
                    st.success("注册成功！请登录")
                    auth.update_page_state('login')
                    st.experimental_rerun()
                else:
                    st.error("用户名已存在")
    
    if st.button("返回登录"):
        auth.update_page_state('login')
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Hide sidebar
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .main .block-container {
        max-width: 800px;
        padding: 2rem;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display appropriate page based on authentication and page state
    if not auth.is_logged_in():
        if st.session_state.page == 'login':
            login_page()
        elif st.session_state.page == 'register':
            register_page()
    else:
        # 如果已登录且页面状态仍为登录或注册页面，则更新为主页
        if st.session_state.page in ['login', 'register']:
            auth.update_page_state('home')
            st.experimental_rerun()
        
        # Create horizontal navigation menu
        if auth.is_admin():
            selected = option_menu(
                menu_title=None,
                options=["刷题中心", "错题概览", "学习数据", "个人中心", "题库管理", "用户管理"],
                icons=['book', 'x-circle', 'clipboard-data', 'person', 'database', 'people'],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )
        else:
            selected = option_menu(
                menu_title=None,
                options=["刷题中心", "错题概览", "学习数据", "个人中心"],
                icons=['book', 'x-circle', 'clipboard-data', 'person'],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )
        
        # 保存当前选中的页面
        auth.update_page_state(selected)
        
        # Display logout button
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("退出登录"):
                auth.logout()
                auth.update_page_state('login')
                st.experimental_rerun()
                
        with col1:
            st.markdown(f"### 你好, {st.session_state.username}!")
            
        # Display page content
        if selected == "刷题中心":
            practice_page()
        elif selected == "错题概览":
            wrong_questions_page()
        elif selected == "学习数据":
            dashboard_page()
        elif selected == "个人中心":
            profile_page()
        elif selected == "题库管理" and auth.is_admin():
            admin_question_page()
        elif selected == "用户管理" and auth.is_admin():
            admin_user_page()

if __name__ == "__main__":
    main() 