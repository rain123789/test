import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Helper functions for dashboard
def create_gauge_chart(value, title, height=300):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "royalblue"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightgreen"}
            ]
        }
    ))
    
    fig.update_layout(height=height)
    return fig

def get_user_stats(user_id):
    # Get user stats directly from database
    stats = db.get_user_stats(user_id)
    
    # If no stats are found, return empty stats
    if not stats or stats["total_attempts"] == 0:
        return {
            "total_attempts": 0,
            "correct_attempts": 0,
            "accuracy": 0,
            "category_stats": [],
            "daily_progress": [],
            "streak": 0
        }
    
    # Calculate streak
    progress = db.get_user_progress(user_id)
    today = datetime.now().date()
    
    dates = []
    if progress:
        dates = sorted([datetime.strptime(attempt["attempt_time"], "%Y-%m-%d %H:%M:%S").date() 
                       for attempt in progress], reverse=True)
    
    streak = 0
    if dates:
        current_date = today
        for date in dates:
            if date == current_date:
                streak += 1
                current_date = current_date - timedelta(days=1)
            elif date < current_date:
                # Skip ahead to this date
                current_date = date
                streak += 1
                current_date = current_date - timedelta(days=1)
            else:
                # Future date, should not happen
                pass
    
    # Return modified stats
    return {
        "total_attempts": stats["total_attempts"],
        "correct_attempts": stats["correct_answers"],
        "accuracy": stats["accuracy"],
        "category_stats": stats["category_stats"] if "category_stats" in stats else [],
        "daily_progress": stats["daily_progress"] if "daily_progress" in stats else [],
        "streak": streak
    }

@auth.login_required
def dashboard_page():
    header("学习仪表盘", "查看你的学习进度和表现")
    
    user = auth.get_current_user()
    user_id = user['id']
    
    stats = get_user_stats(user_id)
    
    # 如果用户没有任何数据，显示提示
    if stats["total_attempts"] == 0:
        st.info("你还没有做过题目，请先在刷题中心开始练习！")
        return
    
    # Overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card_container = card(title="总答题数")
        card_container.markdown(f"<p class='big-number'>{stats['total_attempts']}</p>", unsafe_allow_html=True)
    
    with col2:
        card_container = card(title="正确率")
        card_container.markdown(f"<p class='big-number'>{stats['accuracy']:.1f}%</p>", unsafe_allow_html=True)
    
    with col3:
        card_container = card(title="连续学习")
        card_container.markdown(f"<p class='big-number'>{stats['streak']} 天</p>", unsafe_allow_html=True)
    
    with col4:
        # 安全地获取用户已回答的独立题目数量
        progress = db.get_user_progress(user_id)
        unique_count = 0
        if progress:
            unique_questions = set()
            for attempt in progress:
                if "question_id" in attempt:
                    unique_questions.add(attempt["question_id"])
            unique_count = len(unique_questions)
        
        card_container = card(title="已练习题目")
        card_container.markdown(f"<p class='big-number'>{unique_count}</p>", unsafe_allow_html=True)
    
    # Accuracy trend
    st.markdown("---")
    st.subheader("近期学习趋势")
    
    if stats["daily_progress"]:
        df = pd.DataFrame(stats["daily_progress"], columns=["date", "attempts", "correct"])
        df["accuracy"] = (df["correct"] / df["attempts"] * 100).round(1)
        
        fig = px.line(df, x="date", y=["attempts", "correct"], 
                      title="每日答题数量",
                      labels={"value": "题目数量", "date": "日期", "variable": "类型"},
                      color_discrete_map={"attempts": "gray", "correct": "green"})
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Accuracy by day
        fig = px.line(df, x="date", y="accuracy", 
                      title="每日正确率变化",
                      labels={"accuracy": "正确率 (%)", "date": "日期"},
                      color_discrete_sequence=["royalblue"])
        
        fig.update_layout(
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无近期学习数据，开始做题后可查看趋势。")
    
    # Category performance
    if stats["category_stats"]:
        st.markdown("---")
        st.subheader("类别表现")
        
        df = pd.DataFrame(stats["category_stats"], columns=["category", "attempts", "correct"])
        df["accuracy"] = (df["correct"] / df["attempts"] * 100).round(1)
        
        fig = px.bar(df, x="category", y="accuracy", 
                     title="各类别正确率",
                     labels={"accuracy": "正确率 (%)", "category": "类别"},
                     text_auto='.1f')
        
        fig.update_layout(
            yaxis=dict(range=[0, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Overall progress
    st.markdown("---")
    st.subheader("总体学习进度")
    
    # Get total questions count
    total_questions = len(db.get_all_questions())
    
    # 安全地获取用户已回答的独立题目数量
    user_progress = db.get_user_progress(user_id)
    unique_answered = 0
    if user_progress:
        unique_questions = set()
        for attempt in user_progress:
            if "question_id" in attempt:
                unique_questions.add(attempt["question_id"])
        unique_answered = len(unique_questions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        progress_percent = (unique_answered / total_questions * 100) if total_questions > 0 else 0
        fig = create_gauge_chart(
            progress_percent,
            "题库覆盖率",
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculate mastery level based on accuracy and coverage
        mastery = (stats["accuracy"] * 0.7 + progress_percent * 0.3) / 100
        
        if mastery < 0.3:
            level = "初学者"
            description = "刚刚开始学习，继续加油！"
        elif mastery < 0.5:
            level = "进阶学习者"
            description = "已经有了基础，但还需要不断练习！"
        elif mastery < 0.7:
            level = "熟练学习者"
            description = "理解了大部分知识点，再接再厉！"
        elif mastery < 0.9:
            level = "专家级学习者"
            description = "掌握了绝大部分知识，接近精通！"
        else:
            level = "大师级学习者"
            description = "接近完美的掌握，考试必定大获全胜！"
        
        st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
        st.subheader("学习水平评估")
        st.markdown(f"<p class='big-number'>{level}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{description}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Study recommendations
    st.subheader("学习建议")
    
    # Find weakest categories
    weak_categories = []
    if stats["category_stats"]:
        category_accuracy = {}
        
        for cat_stat in stats["category_stats"]:
            category = cat_stat[0]
            count = cat_stat[1]
            correct = cat_stat[2]
            accuracy = (correct / count * 100) if count > 0 else 0
            category_accuracy[category] = accuracy
        
        # Sort by accuracy ascending
        weak_categories = sorted(category_accuracy.items(), key=lambda x: x[1])[:3]
        
        st.write("建议重点复习以下类别:")
        
        for i, (cat, acc) in enumerate(weak_categories):
            st.markdown(f"{i+1}. **{cat}** (正确率: {acc:.1f}%)")
    
    # Suggested study schedule
    st.write("建议学习计划:")
    
    daily_goal = max(10, int(stats["total_attempts"] / 7)) if stats["daily_progress"] else 10
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**每日目标:** {daily_goal}题")
    
    with col2:
        st.markdown(f"**每周目标:** {daily_goal * 7}题")
    
    with col3:
        weak_cat = weak_categories[0][0] if stats["category_stats"] and weak_categories else "所有类别"
        st.markdown(f"**重点复习:** {weak_cat}")
    
    # Exam readiness
    readiness = stats["accuracy"] / 100
    
    st.subheader("考试准备度")
    
    readiness_gauge = create_gauge_chart(
        readiness * 100,
        "考试准备度",
        height=250
    )
    st.plotly_chart(readiness_gauge, use_container_width=True)
    
    if readiness < 0.6:
        st.warning("你的准备度还不足以应对考试，请继续练习！")
    elif readiness < 0.8:
        st.info("你正在良好地准备考试，继续保持！")
    else:
        st.success("你已经做好了充分准备，相信你能取得好成绩！") 