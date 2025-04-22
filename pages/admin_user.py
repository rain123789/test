import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card
import pandas as pd

@auth.admin_required
def admin_user_page():
    header("用户管理", "查看、添加和管理用户")
    
    # Create tabs for different operations
    tab1, tab2 = st.tabs(["用户列表", "添加用户"])
    
    with tab1:
        # Display all users
        show_user_list()
    
    with tab2:
        # Form to add a new user
        show_add_user_form()

def show_user_list():
    """Display and manage user list"""
    st.subheader("用户列表")
    
    # Get all users
    users = db.get_all_users()
    
    if not users:
        st.info("暂无用户")
        return
    
    # Convert to dataframe for display
    user_data = []
    for user in users:
        # Get user progress data
        progress = db.get_user_progress(user['id'])
        
        # Calculate statistics
        total_attempts = len(progress)
        correct_count = sum(1 for p in progress if p['is_correct'])
        accuracy = correct_count / total_attempts * 100 if total_attempts > 0 else 0
        
        user_data.append({
            "ID": user['id'],
            "用户名": user['username'],
            "邮箱": user['email'] if user['email'] else "-",
            "角色": "管理员" if user['is_admin'] else "普通用户",
            "注册时间": user['created_at'],
            "总答题数": total_attempts,
            "正确率": f"{accuracy:.1f}%" if total_attempts > 0 else "-"
        })
    
    user_df = pd.DataFrame(user_data)
    st.dataframe(user_df, use_container_width=True)
    
    # Edit user modal
    if 'edit_user_id' not in st.session_state:
        st.session_state.edit_user_id = None
    
    # User actions
    st.markdown("---")
    st.subheader("用户操作")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_user_id = st.selectbox(
            "选择用户",
            options=[user['id'] for user in users],
            format_func=lambda x: next((user['username'] for user in users if user['id'] == x), "")
        )
    
    with col2:
        action = st.selectbox(
            "选择操作",
            options=["编辑用户信息", "查看用户数据", "删除用户"]
        )
    
    if st.button("执行操作"):
        if action == "编辑用户信息":
            st.session_state.edit_user_id = selected_user_id
        elif action == "查看用户数据":
            show_user_data(selected_user_id)
        elif action == "删除用户":
            if selected_user_id == auth.get_current_user()['id']:
                st.error("不能删除自己的账号")
            else:
                # Confirm deletion
                if st.checkbox("确认删除此用户？此操作不可恢复！"):
                    if db.delete_user(selected_user_id):
                        st.success("用户删除成功")
                        st.experimental_rerun()
                    else:
                        st.error("删除失败，请稍后重试")
    
    # Show edit form if a user is selected
    if st.session_state.edit_user_id:
        show_edit_user_form(st.session_state.edit_user_id)

def show_edit_user_form(user_id):
    """Display form to edit a user"""
    st.markdown("---")
    st.subheader("编辑用户信息")
    
    # Get user details
    user = db.get_user_by_id(user_id)
    
    if not user:
        st.error("未找到该用户")
        return
    
    with st.form(key=f"edit_user_form_{user_id}"):
        username = st.text_input("用户名", value=user['username'])
        email = st.text_input("邮箱", value=user['email'] if user['email'] else "")
        password = st.text_input("新密码 (留空表示不修改)", type="password")
        is_admin = st.checkbox("设为管理员", value=bool(user['is_admin']))
        
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button("保存修改")
        
        with col2:
            cancel = st.form_submit_button("取消")
        
        if submitted:
            if not username:
                st.error("用户名不能为空")
            else:
                # Update user
                updates = {
                    "username": username,
                    "email": email,
                    "is_admin": int(is_admin)
                }
                
                if password:
                    updates["password"] = password
                
                if db.update_user(user_id, **updates):
                    st.success("用户信息更新成功！")
                    st.session_state.edit_user_id = None
                    st.experimental_rerun()
                else:
                    st.error("更新失败，请稍后重试")
        
        if cancel:
            st.session_state.edit_user_id = None
            st.experimental_rerun()

def show_add_user_form():
    """Display form to add a new user"""
    st.subheader("添加用户")
    
    with st.form(key="add_user_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        confirm_password = st.text_input("确认密码", type="password")
        email = st.text_input("邮箱 (可选)")
        is_admin = st.checkbox("设为管理员")
        
        submitted = st.form_submit_button("添加用户")
        
        if submitted:
            if not username or not password:
                st.error("用户名和密码不能为空")
            elif password != confirm_password:
                st.error("两次输入的密码不一致")
            else:
                # Add user
                if db.create_user(username, password, email, int(is_admin)):
                    st.success("用户添加成功！")
                    st.experimental_rerun()
                else:
                    st.error("添加失败，用户名可能已存在")

def show_user_data(user_id):
    """Display detailed user data"""
    st.markdown("---")
    st.subheader("用户数据详情")
    
    # Get user details
    user = db.get_user_by_id(user_id)
    
    if not user:
        st.error("未找到该用户")
        return
    
    # Display user info
    st.markdown(f"### {user['username']} 的学习数据")
    st.markdown(f"**邮箱:** {user['email'] if user['email'] else '-'}")
    st.markdown(f"**注册时间:** {user['created_at']}")
    st.markdown(f"**账号类型:** {'管理员' if user['is_admin'] else '普通用户'}")
    
    # Get user statistics
    stats = db.get_user_stats(user_id)
    
    if stats["total_attempts"] == 0:
        st.info("该用户还没有答题记录")
        return
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总答题数", stats["total_attempts"])
    
    with col2:
        st.metric("正确题数", stats["correct_answers"])
    
    with col3:
        st.metric("正确率", f"{stats['accuracy']:.1f}%")
    
    with col4:
        wrong_count = stats["total_attempts"] - stats["correct_answers"]
        st.metric("错题数", wrong_count)
    
    # Category breakdown
    if stats["category_stats"]:
        st.subheader("类别统计")
        
        category_data = []
        for cat_stat in stats["category_stats"]:
            category = cat_stat[0]
            count = cat_stat[1]
            correct = cat_stat[2]
            accuracy = (correct / count * 100) if count > 0 else 0
            category_data.append({
                "类别": category,
                "题目数": count,
                "正确数": correct,
                "正确率": f"{accuracy:.1f}%"
            })
        
        category_df = pd.DataFrame(category_data)
        st.dataframe(category_df, use_container_width=True)
    
    # Recent activity
    st.subheader("最近活动")
    
    progress = db.get_user_progress(user_id)
    if progress:
        recent_data = []
        for p in progress[:10]:  # Get 10 most recent activities
            recent_data.append({
                "时间": p['attempt_time'],
                "题目": p['content'][:50] + "..." if len(p['content']) > 50 else p['content'],
                "结果": "✅ 正确" if p['is_correct'] else "❌ 错误",
                "难度": "★" * p['difficulty'],
                "类别": p['category']
            })
        
        recent_df = pd.DataFrame(recent_data)
        st.dataframe(recent_df, use_container_width=True)
    else:
        st.info("无活动记录")
    
    # Export user data
    if st.button("导出用户数据"):
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
            file_name=f"user_data_{user['username']}.csv",
            mime="text/csv"
        ) 