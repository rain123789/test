import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card, create_question_form
import pandas as pd
from utils.question_parser import check_answer_correctness

@auth.login_required
def practice_page():
    # 检查是否应该显示结果摘要
    if 'show_practice_summary' in st.session_state and st.session_state.show_practice_summary:
        display_practice_summary()
        return

    header("刷题中心", "选择题目类别和难度开始练习")
    
    user = auth.get_current_user()
    user_id = user['id']
    
    # Get all categories
    categories = db.get_all_categories()
    if not categories:
        st.info("题库中暂无题目，请联系管理员添加题目")
        return
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox("选择题目类别", categories)
    
    with col2:
        difficulty = st.slider("选择难度级别", 1, 3, 2, 
                             help="1星: 简单, 2星: 中等, 3星: 困难")
    
    with col3:
        num_questions = st.number_input("题目数量", 1, 20, 5)
    
    if st.button("开始练习", type="primary"):
        # Get random questions based on filters
        questions = db.get_random_questions(
            limit=num_questions, 
            category=selected_category, 
            difficulty=difficulty
        )
        
        if not questions:
            st.warning(f"没有找到符合条件的题目")
            return
        
        # Store questions in session state
        st.session_state.practice_questions = questions
        st.session_state.current_question_index = 0
        st.session_state.practice_answers = []
        st.session_state.practice_results = []
        st.experimental_rerun()
    
    # Display questions if they are in session state
    if 'practice_questions' in st.session_state and st.session_state.practice_questions:
        # Show progress
        questions = st.session_state.practice_questions
        current_index = st.session_state.current_question_index
        total_questions = len(questions)
        
        progress_bar = st.progress((current_index) / total_questions)
        st.write(f"问题 {current_index + 1} / {total_questions}")
        
        # Show current question
        current_question = questions[current_index]
        
        def handle_answer_submission(question, user_answer, user_id):
            # Check if answer is correct
            is_correct = check_answer_correctness(question, user_answer)
            
            # Record attempt in database
            db.record_attempt(user_id, question['id'], 1 if is_correct else 0, user_answer)
            
            # Store result
            st.session_state.practice_answers.append(user_answer)
            st.session_state.practice_results.append(is_correct)
            
            # Show result
            if is_correct:
                st.success("✅ 回答正确！")
            else:
                st.error(f"❌ 回答错误。正确答案是: {question['answer']}")
                
                if question['explanation']:
                    st.info(f"解析: {question['explanation']}")
            
            # Move to next question
            if current_index < total_questions - 1:
                st.session_state.current_question_index += 1
                # 保存会话状态
                auth.save_session_state()
                st.experimental_rerun()
            else:
                # Practice completed - 切换到摘要页面
                st.session_state.show_practice_summary = True
                # 保存会话状态
                auth.save_session_state()
                st.experimental_rerun()
        
        # Display question form
        submitted = create_question_form(current_question, current_question['id'], user_id, handle_answer_submission)
        
        # 创建两列布局，将跳过按钮放在右侧
        col1, col2, col3 = st.columns([2, 3, 2])
        with col3:
            # Skip button - 确保不在表单内部
            if st.button("跳过此题", key=f"skip_btn_{current_index}"):
                # Record as incorrect
                db.record_attempt(user_id, current_question['id'], 0, "跳过")
                st.session_state.practice_answers.append("跳过")
                st.session_state.practice_results.append(False)
                
                # Move to next question
                if current_index < total_questions - 1:
                    st.session_state.current_question_index += 1
                    # 保存会话状态
                    auth.save_session_state()
                    st.experimental_rerun()
                else:
                    # Practice completed - 切换到摘要页面
                    st.session_state.show_practice_summary = True
                    # 保存会话状态
                    auth.save_session_state()
                    st.experimental_rerun()

def display_practice_summary():
    """单独的函数显示练习结果摘要，不在任何表单内部"""
    questions = st.session_state.practice_questions
    results = st.session_state.practice_results
    
    header("练习完成！")
    
    # Calculate stats
    correct_count = sum(results)
    total_count = len(results)
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("题目总数", total_count)
    with col2:
        st.metric("正确数量", correct_count)
    with col3:
        st.metric("正确率", f"{accuracy:.1f}%")
    
    # Show detailed results
    st.subheader("详细结果")
    
    results_data = []
    for i, (question, is_correct) in enumerate(zip(questions, results)):
        results_data.append({
            "序号": i + 1,
            "题目": question['content'],
            "难度": "★" * question['difficulty'],
            "答案": question['answer'],
            "结果": "✅ 正确" if is_correct else "❌ 错误"
        })
    
    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, use_container_width=True)
    
    # 再次练习按钮
    st.markdown("### ")  # 添加一些空间
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        restart_button = st.button("再次练习", type="primary")
        if restart_button:
            # Clear session state
            del st.session_state.practice_questions
            del st.session_state.current_question_index
            del st.session_state.practice_answers
            del st.session_state.practice_results
            del st.session_state.show_practice_summary
            # 保存会话状态
            auth.save_session_state()
            st.experimental_rerun() 