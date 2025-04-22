import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card
import pandas as pd

@auth.login_required
def profile_page():
    header("个人中心", "查看和修改你的个人信息")
    
    user = auth.get_current_user()
    user_id = user['id']
    
    # Get user information
    user_info = db.get_user_by_id(user_id)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display avatar
        st.image("https://www.svgrepo.com/show/452030/avatar-default.svg", width=150)
        
        # Display basic information
        st.markdown(f"### {user_info['username']}")
        st.markdown(f"**邮箱:** {user_info['email'] if user_info['email'] else '未设置'}")
        st.markdown(f"**注册时间:** {user_info['created_at']}")
        st.markdown(f"**账号类型:** {'管理员' if user_info['is_admin'] else '普通用户'}")
    
    with col2:
        # Update user information form
        st.subheader("更新个人信息")
        
        with st.form("update_profile_form"):
            new_email = st.text_input("邮箱", value=user_info['email'] if user_info['email'] else "")
            current_password = st.text_input("当前密码", type="password")
            new_password = st.text_input("新密码 (留空表示不修改)", type="password")
            confirm_password = st.text_input("确认新密码", type="password")
            
            submitted = st.form_submit_button("更新信息")
            
            if submitted:
                if current_password != user_info['password']:
                    st.error("当前密码不正确")
                elif new_password and new_password != confirm_password:
                    st.error("两次输入的新密码不一致")
                else:
                    # Update user information
                    updates = {"email": new_email}
                    if new_password:
                        updates["password"] = new_password
                    
                    if db.update_user(user_id, **updates):
                        st.success("个人信息更新成功！")
                        st.experimental_rerun()
                    else:
                        st.error("更新失败，请稍后重试")
    
    # Display activity summary
    st.markdown("---")
    st.subheader("学习活动概览")
    
    # Get user progress
    progress = db.get_user_progress(user_id)
    
    if not progress:
        st.info("你还没有任何学习记录，请先在刷题中心开始练习！")
        return
    
    # Calculate overall statistics
    total_attempts = len(progress)
    correct_count = sum(1 for p in progress if p['is_correct'])
    accuracy = correct_count / total_attempts * 100 if total_attempts > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总答题数", total_attempts)
    
    with col2:
        st.metric("正确数", correct_count)
    
    with col3:
        st.metric("正确率", f"{accuracy:.1f}%")
    
    # Recent activity
    st.subheader("最近活动")
    
    recent_activity = []
    for p in progress[:10]:  # Get 10 most recent activities
        recent_activity.append({
            "时间": p['attempt_time'],
            "题目": p['content'][:50] + "..." if len(p['content']) > 50 else p['content'],
            "结果": "✅ 正确" if p['is_correct'] else "❌ 错误",
            "难度": "★" * p['difficulty']
        })
    
    activity_df = pd.DataFrame(recent_activity)
    st.dataframe(activity_df, use_container_width=True)
    
    # Advanced account settings
    with st.expander("高级账号设置"):
        st.warning("注意: 以下操作不可逆，请谨慎操作！")
        
        # Export data
        if st.button("导出我的学习数据"):
            # Prepare data for export
            export_data = []
            for p in progress:
                export_data.append({
                    "题目ID": p['id'],
                    "题目内容": p['content'],
                    "类别": p['category'],
                    "难度": p['difficulty'],
                    "提交答案": p['user_answer'],
                    "是否正确": "是" if p['is_correct'] else "否",
                    "提交时间": p['attempt_time']
                })
            
            export_df = pd.DataFrame(export_data)
            
            # Convert to CSV for download
            csv = export_df.to_csv(index=False)
            
            st.download_button(
                label="下载CSV文件",
                data=csv,
                file_name=f"learning_data_{user_info['username']}.csv",
                mime="text/csv"
            )
        
        # Delete account (would require additional confirmation in a real app)
        if st.button("删除我的账号", type="primary"):
            st.error("此功能尚未实现，请联系管理员处理账号删除请求。") 