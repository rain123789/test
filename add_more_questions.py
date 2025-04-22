import os
from database import import_questions_from_txt, get_all_categories, get_all_questions

def add_new_questions():
    print("开始添加新题目到数据库...")
    
    # 获取当前所有题目数量作为参考
    initial_count = len(get_all_questions())
    print(f"当前题库共有 {initial_count} 道题目")
    
    # 获取现有类别
    existing_categories = get_all_categories()
    print(f"现有题目类别: {', '.join(existing_categories)}")
    
    # 导入新题目
    questions_dir = 'data/questions'
    if os.path.exists(questions_dir):
        for filename in os.listdir(questions_dir):
            if filename.endswith('.txt'):
                category = os.path.splitext(filename)[0]
                file_path = os.path.join(questions_dir, filename)
                
                # 导入题目
                print(f"导入 {category} 类别的题目...")
                import_questions_from_txt(file_path, category)
    
    # 获取更新后的题目数量
    final_count = len(get_all_questions())
    print(f"导入完成！题库现在共有 {final_count} 道题目")
    print(f"新增了 {final_count - initial_count} 道题目")
    
    # 显示所有类别及每个类别的题目数量
    updated_categories = get_all_categories()
    print(f"更新后的题目类别: {', '.join(updated_categories)}")
    
    print("新题目添加完成！")

if __name__ == "__main__":
    add_new_questions() 