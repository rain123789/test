import os
import re

def parse_question(text):
    """Parse a single question from text format."""
    lines = text.strip().split('\n')
    if len(lines) < 3:  # Need at least question, answer, and explanation
        return None
    
    question_content = lines[0]
    
    # Default values
    question_type = None
    options = None
    answer = None
    explanation = None
    
    # Check if it's a multiple choice question
    if any(line.startswith(('A.', 'B.', 'C.', 'D.')) for line in lines):
        question_type = 'multiple_choice'
        options = '\n'.join([line for line in lines if re.match(r'^[A-D]\.', line)])
    
    # Find answer line
    answer_line = next((line for line in lines if line.startswith('答案:') or line.startswith('答案：')), None)
    if answer_line:
        answer = answer_line.split(':', 1)[1].strip() if ':' in answer_line else answer_line.split('：', 1)[1].strip()
        
        # Determine question type if not already set
        if not question_type:
            if answer.lower() in ['t', 'f', '对', '错', 'true', 'false']:
                question_type = 'true_false'
            else:
                question_type = 'short_answer'
    
    # Find explanation
    explanation_line = next((line for line in lines if line.startswith('解析:') or line.startswith('解析：')), None)
    if explanation_line:
        explanation = explanation_line.split(':', 1)[1].strip() if ':' in explanation_line else explanation_line.split('：', 1)[1].strip()
    
    if not question_type or not answer:
        return None
    
    return {
        'question_type': question_type,
        'content': question_content,
        'options': options,
        'answer': answer,
        'explanation': explanation
    }

def parse_questions_file(file_path, content=None):
    """Parse a file containing multiple questions.
    
    Args:
        file_path: Path to the file to read
        content: If provided, parse this content instead of reading from file_path
    """
    try:
        if content is not None:
            # Use provided content
            file_content = content
        else:
            # Read from file
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
    except Exception as e:
        print(f"Error reading content: {e}")
        return []
    
    # Split the content by double newlines (each question is separated by a blank line)
    question_blocks = [q.strip() for q in file_content.split('\n\n') if q.strip()]
    
    questions = []
    for block in question_blocks:
        question = parse_question(block)
        if question:
            questions.append(question)
    
    return questions

def read_all_question_files(directory='data/questions'):
    """Read all question files in a directory."""
    all_questions = []
    
    if not os.path.exists(directory):
        return all_questions
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            category = os.path.splitext(filename)[0]  # Use filename as category
            
            questions = parse_questions_file(file_path)
            for q in questions:
                q['category'] = category
                # Default difficulty to 2 (medium) if not specified
                q['difficulty'] = 2
                all_questions.append(q)
    
    return all_questions

def check_answer_correctness(question, user_answer):
    """Check if user's answer is correct for a given question."""
    correct_answer = question['answer'].strip().upper()
    
    if question['question_type'] == 'multiple_choice':
        # For multiple choice, normalize to just the letter
        user_answer = user_answer.strip().upper()
        if len(user_answer) > 1:
            # If the user entered the full option (like "A. Option text")
            user_answer = user_answer[0]
        return user_answer == correct_answer
    
    elif question['question_type'] == 'true_false':
        # Normalize true/false answers
        true_values = ['T', 'TRUE', '对', '正确']
        false_values = ['F', 'FALSE', '错', '错误']
        
        user_normalized = user_answer.strip().upper()
        correct_normalized = correct_answer.upper()
        
        user_is_true = any(user_normalized == val for val in true_values)
        user_is_false = any(user_normalized == val for val in false_values)
        correct_is_true = any(correct_normalized == val for val in true_values)
        
        if user_is_true:
            return correct_is_true
        elif user_is_false:
            return not correct_is_true
        else:
            return False
    
    else:  # short_answer
        # For short answer, do a simple string comparison for now
        # This could be enhanced with more sophisticated matching
        return user_answer.strip().upper() == correct_answer.upper()

def format_question_display(question):
    """Format a question for display."""
    formatted = f"## {question['content']}\n\n"
    
    if question['question_type'] == 'multiple_choice' and question['options']:
        formatted += question['options'] + "\n\n"
    
    formatted += f"**答案:** {question['answer']}\n\n"
    
    if question['explanation']:
        formatted += f"**解析:** {question['explanation']}\n\n"
    
    difficulty = question.get('difficulty', 2)
    formatted += f"**难度:** {'★' * difficulty}\n\n"
    formatted += f"**类别:** {question.get('category', '未分类')}\n\n"
    
    return formatted 