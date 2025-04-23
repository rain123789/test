import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# UI Theme and Style
def set_page_config():
    st.set_page_config(
        page_title="计算机考试刷题备考系统",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    
    # 隐藏默认的Streamlit菜单、页脚和顶部内容
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        .stToolbar {display:none !important;}
        div[data-testid="stDecoration"] {display:none;}
        div[data-testid="stStatusWidget"] {display:none;}
        #stConnectionStatus {display:none}
        div.stSidebar > div:first-child {min-height: 0;}
        /* 移除app菜单项 */
        div.stSidebar div.stSelectbox label {display:none;}
        section[data-testid="stSidebar"] > div {padding-top: 0rem;}
        /* 隐藏其他Streamlit默认元素 */
        .css-1inwz65 {display:none;}
        .css-18e3th9 h2 {padding-top: 0;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def apply_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stat-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 100%;
    }
    .stat-card h3 {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 5px;
    }
    .stat-card h1 {
        font-size: 2.5rem;
        color: #1E88E5;
        margin: 0;
    }
    .highlight {
        color: #1E88E5;
        font-weight: bold;
    }
    .correct {
        color: #4CAF50;
        font-weight: bold;
    }
    .incorrect {
        color: #F44336;
        font-weight: bold;
    }
    .difficulty-1 {
        color: #4CAF50;
    }
    .difficulty-2 {
        color: #FF9800;
    }
    .difficulty-3 {
        color: #F44336;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #f1f3f4;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #f1f3f4;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
    }
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Components
def header(title, description=None):
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    if description:
        st.markdown(f'<p style="text-align: center;">{description}</p>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def subheader(title):
    st.markdown(f'<h2 class="sub-header">{title}</h2>', unsafe_allow_html=True)

# Card Components
def card(content=None, title=None):
    """
    一个简单的卡片组件，可以显示标题和内容。
    
    Args:
        content: 要显示的内容，可以是字符串或者一个函数
        title: 卡片标题
    """
    # 创建卡片容器
    container = st.container()
    
    # 在容器内添加卡片样式和内容
    container.markdown('<div class="card">', unsafe_allow_html=True)
    
    if title:
        container.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    
    # 处理内容
    if content is not None:
        if callable(content):
            with container:
                content()
        else:
            container.markdown(f"{content}", unsafe_allow_html=True)
    
    container.markdown('</div>', unsafe_allow_html=True)
    
    return container

def stat_card(title, value, suffix=None):
    html = f"""
    <div class="stat-card">
        <h3>{title}</h3>
        <h1>{value}{suffix if suffix else ''}</h1>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Chart Components
def create_bar_chart(data, x, y, title, color=None, height=400):
    fig = px.bar(data, x=x, y=y, title=title, color=color, height=height)
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_font_size=16,
        xaxis_tickfont_size=14,
        yaxis_tickfont_size=14,
    )
    return fig

def create_pie_chart(data, names, values, title, height=400):
    fig = px.pie(data, names=names, values=values, title=title, height=height)
    fig.update_layout(
        title_font_size=20,
        legend_title_font_size=16,
    )
    return fig

def create_line_chart(data, x, y, title, color=None, height=400):
    fig = px.line(data, x=x, y=y, title=title, color=color, height=height)
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_font_size=16,
        xaxis_tickfont_size=14,
        yaxis_tickfont_size=14,
    )
    return fig

def create_gauge_chart(value, title, min_val=0, max_val=100, height=300):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [min_val, max_val*0.3], 'color': '#FF9E9E'},
                {'range': [max_val*0.3, max_val*0.7], 'color': '#FFEC9E'},
                {'range': [max_val*0.7, max_val], 'color': '#9EFF9E'},
            ],
        }
    ))
    fig.update_layout(height=height)
    return fig

# Form Components
def create_question_form(question, question_id, user_id, on_submit):
    with st.form(key=f"question_form_{question_id}"):
        st.markdown(f"### {question['content']}")
        
        if question['question_type'] == 'multiple_choice':
            options = question['options'].split('\n')
            
            user_answer = st.radio(
                "选择正确答案:",
                options=[opt.split('.')[0] for opt in options],
                key=f"radio_{question_id}"
            )
            
            for opt in options:
                st.markdown(opt)
        
        elif question['question_type'] == 'true_false':
            user_answer = st.radio(
                "选择正确答案:",
                options=["对", "错"],
                key=f"tf_{question_id}"
            )
            
        else:  # short_answer
            user_answer = st.text_area(
                "输入你的答案:",
                key=f"text_{question_id}",
                height=100
            )
            
        difficulty = question['difficulty']
        st.markdown(f"<p>难度级别: <span class='difficulty-{difficulty}'>{'★' * difficulty}</span></p>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("提交答案")
        
        if submitted:
            on_submit(question, user_answer, user_id)
            return True
    
    return False

# Helper functions
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%m-%d")

def show_difficulty(level):
    colors = {1: "#4CAF50", 2: "#FF9800", 3: "#F44336"}
    return f"<span style='color: {colors.get(level, '#333')}'>{'★' * level}</span>"

def paginate(items, page_size, page_num):
    """Return a slice of items for the selected page."""
    start = page_num * page_size
    end = start + page_size
    return items[start:end]

def pagination_nav(total_items, page_size, page_key="page"):
    """Display pagination controls and return current page."""
    num_pages = (total_items + page_size - 1) // page_size
    
    if num_pages <= 1:
        return 0
    
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
    
    col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
    
    with col1:
        if st.button("◀", key=f"prev_{page_key}"):
            st.session_state[page_key] = max(0, st.session_state[page_key] - 1)
    
    with col4:
        if st.button("▶", key=f"next_{page_key}"):
            st.session_state[page_key] = min(num_pages - 1, st.session_state[page_key] + 1)
    
    with col2:
        st.write(f"页面 {st.session_state[page_key] + 1}/{num_pages}")
    
    return st.session_state[page_key] 