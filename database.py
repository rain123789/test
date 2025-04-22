import sqlite3
import os
import pandas as pd
from datetime import datetime

# Database connection
def get_db_connection():
    conn = sqlite3.connect('exam_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_type TEXT NOT NULL,
        content TEXT NOT NULL,
        options TEXT,
        answer TEXT NOT NULL,
        explanation TEXT,
        difficulty INTEGER NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create user_progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_correct INTEGER NOT NULL,
        user_answer TEXT,
        attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    ''')
    
    # Create an admin user if it doesn't exist
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                      ('admin', 'admin123', 1))
    
    conn.commit()
    conn.close()

# User management functions
def create_user(username, password, email=None, is_admin=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
            (username, password, email, is_admin)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(user_id, username=None, email=None, password=None, is_admin=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build update query based on provided parameters
    update_fields = []
    params = []
    
    if username:
        update_fields.append("username = ?")
        params.append(username)
    if email:
        update_fields.append("email = ?")
        params.append(email)
    if password:
        update_fields.append("password = ?")
        params.append(password)
    if is_admin is not None:
        update_fields.append("is_admin = ?")
        params.append(is_admin)
    
    if not update_fields:
        conn.close()
        return False
    
    params.append(user_id)
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return True

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

# Question management functions
def add_question(question_type, content, answer, difficulty, category, options=None, explanation=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO questions (question_type, content, options, answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (question_type, content, options, answer, explanation, difficulty, category)
    )
    conn.commit()
    conn.close()
    return True

def get_question_by_id(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    question = cursor.fetchone()
    conn.close()
    return question

def get_questions_by_category(category, limit=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM questions WHERE category = ?"
    params = [category]
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
        
    cursor.execute(query, params)
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_questions_by_difficulty(difficulty, limit=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM questions WHERE difficulty = ?"
    params = [difficulty]
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
        
    cursor.execute(query, params)
    questions = cursor.fetchall()
    conn.close()
    return questions

def get_random_questions(limit=10, category=None, difficulty=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM questions"
    params = []
    
    conditions = []
    if category:
        conditions.append("category = ?")
        params.append(category)
    if difficulty:
        conditions.append("difficulty = ?")
        params.append(difficulty)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY RANDOM() LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    questions = cursor.fetchall()
    conn.close()
    return questions

def update_question(question_id, question_type=None, content=None, options=None, answer=None, explanation=None, difficulty=None, category=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build update query based on provided parameters
    update_fields = []
    params = []
    
    if question_type:
        update_fields.append("question_type = ?")
        params.append(question_type)
    if content:
        update_fields.append("content = ?")
        params.append(content)
    if options is not None:
        update_fields.append("options = ?")
        params.append(options)
    if answer:
        update_fields.append("answer = ?")
        params.append(answer)
    if explanation is not None:
        update_fields.append("explanation = ?")
        params.append(explanation)
    if difficulty:
        update_fields.append("difficulty = ?")
        params.append(difficulty)
    if category:
        update_fields.append("category = ?")
        params.append(category)
    
    if not update_fields:
        conn.close()
        return False
    
    params.append(question_id)
    query = f"UPDATE questions SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return True

def delete_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return True

def get_all_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM questions")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# User progress functions
def record_attempt(user_id, question_id, is_correct, user_answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_progress (user_id, question_id, is_correct, user_answer) VALUES (?, ?, ?, ?)",
        (user_id, question_id, is_correct, user_answer)
    )
    conn.commit()
    conn.close()
    return True

def get_user_progress(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.question_type, q.content, q.category, q.difficulty, 
               up.is_correct, up.user_answer, up.attempt_time
        FROM user_progress up
        JOIN questions q ON up.question_id = q.id
        WHERE up.user_id = ?
        ORDER BY up.attempt_time DESC
    """, (user_id,))
    progress = cursor.fetchall()
    conn.close()
    return progress

def get_user_wrong_questions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.*, up.user_answer, up.attempt_time
        FROM questions q
        JOIN user_progress up ON q.id = up.question_id
        WHERE up.user_id = ? AND up.is_correct = 0
        GROUP BY q.id
        ORDER BY up.attempt_time DESC
    """, (user_id,))
    wrong_questions = cursor.fetchall()
    conn.close()
    return wrong_questions

def get_user_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total attempts
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE user_id = ?", (user_id,))
    total_attempts = cursor.fetchone()[0]
    
    # Correct answers
    cursor.execute("SELECT COUNT(*) FROM user_progress WHERE user_id = ? AND is_correct = 1", (user_id,))
    correct_answers = cursor.fetchone()[0]
    
    # Accuracy rate
    accuracy = (correct_answers / total_attempts * 100) if total_attempts > 0 else 0
    
    # Questions by category
    cursor.execute("""
        SELECT q.category, COUNT(*) as count, SUM(up.is_correct) as correct
        FROM user_progress up
        JOIN questions q ON up.question_id = q.id
        WHERE up.user_id = ?
        GROUP BY q.category
    """, (user_id,))
    category_stats = cursor.fetchall()
    
    # Questions by difficulty
    cursor.execute("""
        SELECT q.difficulty, COUNT(*) as count, SUM(up.is_correct) as correct
        FROM user_progress up
        JOIN questions q ON up.question_id = q.id
        WHERE up.user_id = ?
        GROUP BY q.difficulty
    """, (user_id,))
    difficulty_stats = cursor.fetchall()
    
    # Daily progress
    cursor.execute("""
        SELECT DATE(attempt_time) as date, COUNT(*) as attempts, SUM(is_correct) as correct
        FROM user_progress
        WHERE user_id = ?
        GROUP BY DATE(attempt_time)
        ORDER BY date DESC
        LIMIT 30
    """, (user_id,))
    daily_progress = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_attempts": total_attempts,
        "correct_answers": correct_answers,
        "accuracy": accuracy,
        "category_stats": category_stats,
        "difficulty_stats": difficulty_stats,
        "daily_progress": daily_progress
    }

# Import questions from text files
def import_questions_from_txt(file_path, category, difficulty=2):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = content.split('\n\n')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for q in questions:
        lines = q.strip().split('\n')
        if len(lines) < 3:  # Skip incomplete questions
            continue
        
        question_content = lines[0]
        
        # Determine question type and parse accordingly
        if any(line.startswith(('A.', 'B.', 'C.', 'D.')) for line in lines):
            # Multiple choice question
            options = '\n'.join([line for line in lines if line.startswith(('A.', 'B.', 'C.', 'D.'))])
            
            # Find answer line (typically starts with "答案:" or similar)
            answer_line = next((line for line in lines if "答案" in line), None)
            if answer_line:
                answer = answer_line.split(":")[-1].strip()
            else:
                continue  # Skip if no answer found
                
            # Find explanation if it exists
            explanation_line = next((line for line in lines if "解析" in line), None)
            explanation = explanation_line.split(":")[-1].strip() if explanation_line else None
            
            cursor.execute(
                "INSERT INTO questions (question_type, content, options, answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('multiple_choice', question_content, options, answer, explanation, difficulty, category)
            )
        else:
            # True/False or short answer question
            answer_line = next((line for line in lines if "答案" in line), None)
            if answer_line:
                answer = answer_line.split(":")[-1].strip()
            else:
                continue
                
            explanation_line = next((line for line in lines if "解析" in line), None)
            explanation = explanation_line.split(":")[-1].strip() if explanation_line else None
            
            question_type = 'true_false' if answer.lower() in ['t', 'f', '对', '错', 'true', 'false'] else 'short_answer'
            
            cursor.execute(
                "INSERT INTO questions (question_type, content, options, answer, explanation, difficulty, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (question_type, question_content, None, answer, explanation, difficulty, category)
            )
    
    conn.commit()
    conn.close()
    return True

def get_all_questions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions

if __name__ == "__main__":
    init_db() 