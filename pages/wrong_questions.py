import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card, pagination_nav
import pandas as pd
from utils.question_parser import format_question_display

@auth.login_required
def wrong_questions_page():
    # Initialize session state variables if they don't exist
    if 'show_review' not in st.session_state:
        st.session_state.show_review = False
    if 'review_category' not in st.session_state:
        st.session_state.review_category = None
    if 'review_difficulty' not in st.session_state:
        st.session_state.review_difficulty = None
    if 'review_question' not in st.session_state:
        st.session_state.review_question = None

    header("错题概览", "查看和复习做错的题目")
    
    user = auth.get_current_user()
    user_id = user['id']
    
    # Show review question if in review mode
    if st.session_state.get('show_review', False) and st.session_state.get('review_question'):
        show_question_review(st.session_state.review_question, user_id)
        return
    
    # Get wrong questions
    wrong_questions = db.get_user_wrong_questions(user_id)
    
    if not wrong_questions:
        st.info("你还没有做错的题目，继续加油！")
        return
    
    # Display statistics
    total_wrong = len(wrong_questions)
    
    # Group by category
    categories = {}
    for q in wrong_questions:
        cat = q['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("错题总数", total_wrong)
        
        # Display categories
        st.subheader("按类别统计")
        chart_data = pd.DataFrame({
            "类别": list(categories.keys()),
            "数量": list(categories.values())
        })
        st.bar_chart(chart_data.set_index("类别"))
    
    with col2:
        # Filter options
        selected_category = st.selectbox(
            "按类别筛选",
            ["全部"] + list(categories.keys())
        )
        
        sort_by = st.radio(
            "排序方式",
            ["最近错误", "难度升序", "难度降序"]
        )
    
    # Apply filters
    filtered_questions = wrong_questions
    if selected_category != "全部":
        filtered_questions = [q for q in wrong_questions if q['category'] == selected_category]
    
    # Apply sorting
    if sort_by == "难度升序":
        filtered_questions = sorted(filtered_questions, key=lambda q: q['difficulty'])
    elif sort_by == "难度降序":
        filtered_questions = sorted(filtered_questions, key=lambda q: q['difficulty'], reverse=True)
    # For "最近错误", no need to sort as it's already sorted by attempt_time DESC in the database query
    
    # Pagination
    items_per_page = 5
    page = pagination_nav(len(filtered_questions), items_per_page, "wrong_q_page")
    page_questions = filtered_questions[page * items_per_page:(page + 1) * items_per_page]
    
    # Display questions
    for i, question in enumerate(page_questions):
        with st.expander(f"题目 {page * items_per_page + i + 1}: {question['content'][:50]}...", expanded=i==0):
            st.markdown(f"**题目内容:** {question['content']}")
            
            if question['question_type'] == 'multiple_choice' and question['options']:
                st.markdown("**选项:**")
                options = question['options'].split('\n')
                for opt in options:
                    st.markdown(f"- {opt}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**你的回答:** {question['user_answer']}")
            with col2:
                st.markdown(f"**正确答案:** {question['answer']}")
            
            if question['explanation']:
                st.markdown(f"**解析:** {question['explanation']}")
            
            # Show metadata
            st.markdown(f"**难度:** {'★' * question['difficulty']}")
            st.markdown(f"**类别:** {question['category']}")
            st.markdown(f"**回答时间:** {question['attempt_time']}")
            
            # Practice again button - 移到单独的列中，确保不在表单内
            col1, col2, col3 = st.columns([1, 3, 1])
            with col3:
                if st.button("再次练习此类型题", key=f"practice_{question['id']}"):
                    # 获取同类型的问题
                    st.session_state.review_category = question['category']
                    st.session_state.review_difficulty = question['difficulty']
                    st.session_state.review_question = question
                    st.session_state.show_review = True
                    # 保存会话状态
                    auth.save_session_state()
                    st.rerun()
    
    # Show review question if in review mode
    if st.session_state.get('show_review', False) and st.session_state.get('review_question'):
        show_question_review(st.session_state.review_question, user_id)

def show_question_review(question, user_id):
    """Show a single question for review"""
    st.markdown("---")
    st.subheader("题目复习")
    
    # 显示分类和难度信息
    st.markdown(f"**类别:** {question['category']} | **难度:** {'★' * question['difficulty']}")
    
    with st.form(key=f"review_form_{question['id']}"):
        st.markdown(f"### {question['content']}")
        
        if question['question_type'] == 'multiple_choice':
            options = question['options'].split('\n')
            
            for opt in options:
                st.markdown(opt)
            
            user_answer = st.radio(
                "选择正确答案:",
                options=[opt.split('.')[0] for opt in options],
                key=f"review_radio_{question['id']}"
            )
            
        elif question['question_type'] == 'true_false':
            user_answer = st.radio(
                "选择正确答案:",
                options=["对", "错"],
                key=f"review_tf_{question['id']}"
            )
            
        else:  # short_answer
            user_answer = st.text_area(
                "输入你的答案:",
                key=f"review_text_{question['id']}",
                height=100
            )
            
        submitted = st.form_submit_button("提交答案")
        
        if submitted:
            # Check if answer is correct
            is_correct = False
            correct_answer = question['answer'].strip().upper()
            
            if question['question_type'] == 'multiple_choice':
                user_answer = user_answer.strip().upper()
                if len(user_answer) > 1:
                    user_answer = user_answer[0]
                is_correct = user_answer == correct_answer
                
            elif question['question_type'] == 'true_false':
                true_values = ['T', 'TRUE', '对', '正确']
                false_values = ['F', 'FALSE', '错', '错误']
                
                user_normalized = user_answer.strip().upper()
                correct_normalized = correct_answer.upper()
                
                user_is_true = any(user_normalized == val for val in true_values)
                user_is_false = any(user_normalized == val for val in false_values)
                correct_is_true = any(correct_normalized == val for val in true_values)
                
                if user_is_true:
                    is_correct = correct_is_true
                elif user_is_false:
                    is_correct = not correct_is_true
            
            else:  # short_answer
                is_correct = user_answer.strip().upper() == correct_answer.upper()
            
            # Record attempt
            db.record_attempt(user_id, question['id'], 1 if is_correct else 0, user_answer)
            
            # Show result
            if is_correct:
                st.success("✅ 回答正确！")
            else:
                st.error(f"❌ 回答错误。正确答案是: {question['answer']}")
                
                if question['explanation']:
                    st.info(f"解析: {question['explanation']}")
    
    # 返回按钮放在表单外部
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("返回错题列表", key="back_to_list"):
            st.session_state.show_review = False
            # 保存会话状态
            auth.save_session_state()
            st.rerun()
            
    # 找更多同类型题目按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("再来一题同类型", key="more_similar"):
            # 获取同类型的题目
            similar_questions = db.get_random_questions(
                limit=1, 
                category=st.session_state.review_category,
                difficulty=st.session_state.review_difficulty
            )
            
            if similar_questions:
                st.session_state.review_question = similar_questions[0]
                # 保存会话状态
                auth.save_session_state()
                st.rerun()
            else:
                st.warning("没有找到更多同类型题目") 