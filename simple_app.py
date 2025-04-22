import streamlit as st

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
    
    # Simple login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("计算机考试刷题备考系统")
    st.markdown("<p style='text-align: center;'>登录以开始学习</p>", unsafe_allow_html=True)
    
    # Simple login form elements
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    login_button = st.button("登录")
    
    # Register link
    st.markdown("<p style='text-align: center;'>还没有账号？</p>", unsafe_allow_html=True)
    register_button = st.button("注册新账号")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 