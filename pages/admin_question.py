import streamlit as st
import database as db
import auth
from utils.ui import header, subheader, card, pagination_nav
import pandas as pd
import os
from utils.question_parser import parse_questions_file

@auth.admin_required
def admin_question_page():
    header("题库管理", "添加、修改和删除题目")
    
    # Create tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs(["题目列表", "添加题目", "批量导入", "类别管理"])
    
    with tab1:
        # Display all questions with filtering and search
        show_question_list()
    
    with tab2:
        # Form to add a single question
        show_add_question_form()
    
    with tab3:
        # Import questions from file
        show_import_questions()
    
    with tab4:
        # Category management
        show_category_management()

def show_question_list():
    """Display and manage the question list"""
    st.subheader("题目列表")
    
    # Get all questions
    questions = db.get_all_questions()
    
    if not questions:
        st.info("题库中暂无题目")
        return
    
    # Get all categories for filter
    categories = db.get_all_categories()
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_category = st.selectbox(
            "按类别筛选",
            ["全部"] + categories
        )
    
    with col2:
        selected_difficulty = st.selectbox(
            "按难度筛选",
            ["全部", "1", "2", "3"]
        )
    
    with col3:
        selected_type = st.selectbox(
            "按题型筛选",
            ["全部", "单选题", "判断题", "简答题"]
        )
    
    # Apply filters
    filtered_questions = questions
    
    if selected_category != "全部":
        filtered_questions = [q for q in filtered_questions if q['category'] == selected_category]
    
    if selected_difficulty != "全部":
        difficulty = int(selected_difficulty)
        filtered_questions = [q for q in filtered_questions if q['difficulty'] == difficulty]
    
    if selected_type != "全部":
        type_map = {
            "单选题": "multiple_choice",
            "判断题": "true_false",
            "简答题": "short_answer"
        }
        question_type = type_map.get(selected_type)
        if question_type:
            filtered_questions = [q for q in filtered_questions if q['question_type'] == question_type]
    
    # Search box
    search_query = st.text_input("搜索题目", placeholder="输入关键词搜索题目内容")
    if search_query:
        filtered_questions = [q for q in filtered_questions if search_query.lower() in q['content'].lower()]
    
    # Display questions
    st.write(f"共找到 {len(filtered_questions)} 个题目")
    
    # Pagination
    items_per_page = 10
    page = pagination_nav(len(filtered_questions), items_per_page, "admin_q_page")
    page_questions = filtered_questions[page * items_per_page:(page + 1) * items_per_page]
    
    # Create a table for display
    question_table = []
    for q in page_questions:
        type_display = {
            "multiple_choice": "单选题",
            "true_false": "判断题",
            "short_answer": "简答题"
        }.get(q['question_type'], q['question_type'])
        
        question_table.append({
            "ID": q['id'],
            "题目": q['content'][:50] + "..." if len(q['content']) > 50 else q['content'],
            "类型": type_display,
            "难度": "★" * q['difficulty'],
            "类别": q['category']
        })
    
    question_df = pd.DataFrame(question_table)
    st.dataframe(question_df, use_container_width=True)
    
    # Edit question modal
    if 'edit_question_id' not in st.session_state:
        st.session_state.edit_question_id = None
    
    # Edit question button for each question
    for i, q in enumerate(page_questions):
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"编辑题目 #{q['id']}", key=f"edit_{q['id']}"):
                st.session_state.edit_question_id = q['id']
                st.experimental_rerun()
        with col2:
            if st.button(f"删除题目 #{q['id']}", key=f"delete_{q['id']}"):
                if db.delete_question(q['id']):
                    st.success(f"题目 #{q['id']} 已删除")
                    st.experimental_rerun()
                else:
                    st.error("删除失败，请稍后重试")
    
    # Show edit form if a question is selected
    if st.session_state.edit_question_id:
        show_edit_question_form(st.session_state.edit_question_id)

def show_edit_question_form(question_id):
    """Display form to edit a question"""
    st.markdown("---")
    st.subheader(f"编辑题目 #{question_id}")
    
    # Get question details
    question = db.get_question_by_id(question_id)
    
    if not question:
        st.error("未找到该题目")
        return
    
    # Get all categories
    categories = db.get_all_categories()
    
    with st.form(key=f"edit_question_form_{question_id}"):
        question_type = st.selectbox(
            "题目类型",
            options=[
                ("单选题", "multiple_choice"), 
                ("判断题", "true_false"), 
                ("简答题", "short_answer")
            ],
            format_func=lambda x: x[0],
            index=[i for i, (_, val) in enumerate([("单选题", "multiple_choice"), ("判断题", "true_false"), ("简答题", "short_answer")]) if val == question['question_type']][0]
        )[1]
        
        content = st.text_area("题目内容", value=question['content'], height=100)
        
        if question_type == "multiple_choice":
            options = st.text_area(
                "选项 (每行一个选项，格式如: A. 选项1)",
                value=question['options'] if question['options'] else "A. \nB. \nC. \nD. ",
                height=150
            )
        else:
            options = None
        
        answer = st.text_input("正确答案", value=question['answer'])
        
        explanation = st.text_area(
            "解析 (可选)",
            value=question['explanation'] if question['explanation'] else "",
            height=100
        )
        
        difficulty = st.slider(
            "难度级别",
            min_value=1,
            max_value=3,
            value=question['difficulty'],
            step=1,
            format="%d星"
        )
        
        category = st.selectbox(
            "所属类别",
            options=categories,
            index=categories.index(question['category']) if question['category'] in categories else 0
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            submitted = st.form_submit_button("保存修改")
        
        with col2:
            cancel = st.form_submit_button("取消")
        
        if submitted:
            if not content or not answer:
                st.error("题目内容和正确答案不能为空")
            else:
                # Update question
                if db.update_question(
                    question_id,
                    question_type=question_type,
                    content=content,
                    options=options,
                    answer=answer,
                    explanation=explanation,
                    difficulty=difficulty,
                    category=category
                ):
                    st.success("题目修改成功！")
                    st.session_state.edit_question_id = None
                    st.experimental_rerun()
                else:
                    st.error("修改失败，请稍后重试")
        
        if cancel:
            st.session_state.edit_question_id = None
            st.experimental_rerun()

def show_add_question_form():
    """Display form to add a new question"""
    st.subheader("添加题目")
    
    # Get all categories
    categories = db.get_all_categories()
    
    if not categories:
        st.warning("请先创建至少一个类别")
        return
    
    with st.form(key="add_question_form"):
        question_type = st.selectbox(
            "题目类型",
            options=[
                ("单选题", "multiple_choice"), 
                ("判断题", "true_false"), 
                ("简答题", "short_answer")
            ],
            format_func=lambda x: x[0]
        )[1]
        
        content = st.text_area("题目内容", height=100)
        
        if question_type == "multiple_choice":
            options = st.text_area(
                "选项 (每行一个选项，格式如: A. 选项1)",
                value="A. \nB. \nC. \nD. ",
                height=150
            )
        else:
            options = None
        
        answer = st.text_input("正确答案")
        
        explanation = st.text_area("解析 (可选)", height=100)
        
        difficulty = st.slider(
            "难度级别",
            min_value=1,
            max_value=3,
            value=2,
            step=1,
            format="%d星"
        )
        
        category = st.selectbox("所属类别", options=categories)
        
        submitted = st.form_submit_button("添加题目")
        
        if submitted:
            if not content or not answer:
                st.error("题目内容和正确答案不能为空")
            else:
                # Add question
                if db.add_question(
                    question_type=question_type,
                    content=content,
                    options=options,
                    answer=answer,
                    explanation=explanation,
                    difficulty=difficulty,
                    category=category
                ):
                    st.success("题目添加成功！")
                    # Clear form (need to rerun)
                    st.experimental_rerun()
                else:
                    st.error("添加失败，请稍后重试")

def show_import_questions():
    """Display interface to import questions from files"""
    st.subheader("批量导入题目")
    
    # Ensure data directory exists
    os.makedirs('data/questions', exist_ok=True)
    
    # Option to create a new category
    with st.expander("创建新类别", expanded=False):
        with st.form(key="add_category_form"):
            new_category = st.text_input("新类别名称")
            submitted = st.form_submit_button("创建类别")
            
            if submitted and new_category:
                # Create a new empty file for the category
                file_path = f"data/questions/{new_category}.txt"
                if not os.path.exists(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("# 在此添加题目，每题之间用空行分隔\n\n")
                    st.success(f"类别 '{new_category}' 创建成功！")
                else:
                    st.warning(f"类别 '{new_category}' 已存在")
    
    # File uploader for importing questions
    uploaded_file = st.file_uploader("上传题目文件 (txt格式)", type=["txt"])
    
    if uploaded_file:
        # Read file content
        file_content = uploaded_file.read().decode('utf-8')
        
        # Parse questions
        questions = parse_questions_file(None, content=file_content)
        
        if not questions:
            st.error("未能解析出有效的题目，请检查文件格式")
        else:
            st.success(f"成功解析出 {len(questions)} 个题目")
            
            # Select category
            categories = db.get_all_categories()
            category = st.selectbox("选择题目类别", options=categories)
            
            # Select difficulty
            difficulty = st.slider(
                "设置默认难度级别",
                min_value=1,
                max_value=3,
                value=2,
                step=1,
                format="%d星"
            )
            
            # Preview parsed questions
            with st.expander("预览解析结果", expanded=True):
                for i, q in enumerate(questions[:5]):  # Show first 5 questions
                    st.markdown(f"### 题目 {i+1}")
                    st.markdown(f"**内容:** {q['content']}")
                    if q['question_type'] == 'multiple_choice' and q['options']:
                        st.markdown("**选项:**")
                        for opt in q['options'].split('\n'):
                            st.markdown(f"- {opt}")
                    st.markdown(f"**答案:** {q['answer']}")
                    if q['explanation']:
                        st.markdown(f"**解析:** {q['explanation']}")
                    st.markdown(f"**类型:** {q['question_type']}")
                    st.markdown("---")
                
                if len(questions) > 5:
                    st.info(f"还有 {len(questions) - 5} 个题目未显示")
            
            # Import button
            if st.button("导入题目"):
                # Save to file
                file_path = f"data/questions/{category}.txt"
                
                # Append to existing file or create new one
                mode = 'a' if os.path.exists(file_path) else 'w'
                with open(file_path, mode, encoding='utf-8') as f:
                    for q in questions:
                        # Format the question for writing to file
                        f.write(f"{q['content']}\n")
                        
                        if q['question_type'] == 'multiple_choice' and q['options']:
                            f.write(f"{q['options']}\n")
                        
                        f.write(f"答案: {q['answer']}\n")
                        
                        if q['explanation']:
                            f.write(f"解析: {q['explanation']}\n")
                        
                        f.write("\n")  # Empty line between questions
                
                # Import to database
                for q in questions:
                    db.add_question(
                        question_type=q['question_type'],
                        content=q['content'],
                        options=q['options'],
                        answer=q['answer'],
                        explanation=q['explanation'],
                        difficulty=difficulty,
                        category=category
                    )
                
                st.success(f"成功导入 {len(questions)} 个题目到类别 '{category}'")
    
    # Instructions for file format
    st.markdown("---")
    st.subheader("文件格式说明")
    st.markdown("""
    题目文件应为纯文本格式（.txt），内容格式如下：
    
    ```
    题目内容
    A. 选项1
    B. 选项2
    C. 选项3
    D. 选项4
    答案: A
    解析: 这里是解析内容
    
    第二个题目内容
    答案: 正确答案
    解析: 解析内容
    ```
    
    注意事项：
    1. 每个题目之间用空行分隔
    2. 选择题需要包含选项，每行一个选项，格式为字母加点加空格
    3. 答案行以"答案:"或"答案："开头
    4. 解析行以"解析:"或"解析："开头（可选）
    5. 系统会自动识别题目类型（选择题、判断题或简答题）
    """)

def show_category_management():
    """Display interface to manage categories"""
    st.subheader("类别管理")
    
    # Get all categories
    categories = db.get_all_categories()
    
    if not categories:
        st.info("暂无题目类别")
    else:
        # Display categories and question counts
        category_data = []
        for category in categories:
            questions = db.get_questions_by_category(category)
            category_data.append({
                "类别": category,
                "题目数量": len(questions),
                "平均难度": sum(q['difficulty'] for q in questions) / len(questions) if questions else 0
            })
        
        category_df = pd.DataFrame(category_data)
        st.dataframe(category_df, use_container_width=True)
    
    # Add new category
    with st.form(key="manage_category_form"):
        new_category = st.text_input("新类别名称")
        submitted = st.form_submit_button("添加类别")
        
        if submitted and new_category:
            # Create a new empty file for the category
            file_path = f"data/questions/{new_category}.txt"
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("# 在此添加题目，每题之间用空行分隔\n\n")
                st.success(f"类别 '{new_category}' 添加成功！")
                st.experimental_rerun()
            else:
                st.warning(f"类别 '{new_category}' 已存在")
    
    # Delete category
    if categories:
        st.markdown("---")
        st.subheader("删除类别")
        st.warning("删除类别将同时删除该类别下的所有题目，此操作不可逆！")
        
        with st.form(key="delete_category_form"):
            category_to_delete = st.selectbox("选择要删除的类别", options=categories)
            confirmed = st.checkbox("我确认要删除此类别及其所有题目")
            submitted = st.form_submit_button("删除类别")
            
            if submitted:
                if not confirmed:
                    st.error("请先确认删除操作")
                else:
                    # Delete questions from database
                    questions = db.get_questions_by_category(category_to_delete)
                    for q in questions:
                        db.delete_question(q['id'])
                    
                    # Delete category file
                    file_path = f"data/questions/{category_to_delete}.txt"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    st.success(f"类别 '{category_to_delete}' 及其题目已删除")
                    st.experimental_rerun() 