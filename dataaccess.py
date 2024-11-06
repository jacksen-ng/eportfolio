import sqlite3
from models import *

def get_connection(autocommit=False):
    if autocommit:
        return sqlite3.connect('portfolio.db', isolation_level=None)
    else:
        return sqlite3.connect('portfolio.db')

def create_users_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'admin' CHECK (role IN ('teacher', 'admin'))
            )
        ''')
        conn.commit()

def insert_user(username, password, role='admin'):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                            (username, password, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, role FROM users WHERE username = ?', 
                        (username,))
        user_data = cursor.fetchone()

    if user_data:
        return {
            'id': user_data[0],
            'username': user_data[1],
            'password': user_data[2],
            'role': user_data[3]
        }
    return None

def verify_user(username, password):
    user = get_user(username)
    if user and user['password'] == password:
        return user
    return None

def create_home_content_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_home_content(content):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO content (content) VALUES (?)', (content,))
        conn.commit()

def get_home_content(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM content WHERE id = ?", (id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None  

def create_skill_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_skill(skill):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            print(f"Attempting to insert skill: {skill}")  
            cursor.execute('INSERT INTO skills (skill) VALUES (?)', (skill,))
            conn.commit()
            new_id = cursor.lastrowid
            print(f"New skill ID: {new_id}")  
            return new_id
        except Exception as e:
            print(f"Database error in insert_skill: {e}")  
            conn.rollback()
            return False

def get_skill(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT skill FROM skills WHERE id = ?", (id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

def update_home_content(id, new_content):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE content SET content = ? WHERE id = ?", (new_content, id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating home content: {e}")
            return False

def update_skill(id, new_skill):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE skills SET skill = ? WHERE id = ?", (new_skill, id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating skill: {e}")
            return False

def get_all_home_content():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM content")
        results = cursor.fetchall()
        return [HomeContent(id=row[0], content=row[1]) for row in results]

def get_all_skills():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, skill FROM skills ORDER BY id')
        return cursor.fetchall()

def verify_content_update(id, expected_content, table="content"):
    with get_connection() as conn:
        cursor = conn.cursor()
        if table == "content":
            cursor.execute("SELECT content FROM content WHERE id = ?", (id,))
        else:
            cursor.execute("SELECT skill FROM skills WHERE id = ?", (id,))
        result = cursor.fetchone()
        return result and result[0] == expected_content
    
def create_about_page_content_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS about_page_content (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
        ''')
        conn.commit()
        
        
def insert_about_page_content(id, content):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO about_page_content (id, content) VALUES (?, ?)", (id, content))
        conn.commit()
        
def get_about_page_content(id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM about_page_content WHERE id = ?", (id,))
        result = cursor.fetchone()
        return result[0] if result else None

def update_about_page_content(id, new_content):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE about_page_content SET content = ? WHERE id = ?", (new_content, id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating about page content: {e}")
            return False
        
def get_all_about_page_content():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM about_page_content")
        results = cursor.fetchall()
        return [AboutPageContent(id=row[0], content=row[1]) for row in results]
    
def verify_about_page_content_update(id, expected_content):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM about_page_content WHERE id = ?", (id,))
        result = cursor.fetchone()
        return result and result[0] == expected_content
    
def delete_skill(skill_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting skill: {e}")
            return False

def ensure_skill_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill TEXT NOT NULL
            )
        ''')
        conn.commit()
        
def create_teacher_comment_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
def insert_teacher_comment(comment):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO teacher_comments (comment) VALUES (?)', (comment,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting teacher comment: {e}")
            return False

def get_all_teacher_comments():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, comment, created_at 
            FROM teacher_comments 
            ORDER BY created_at DESC
        ''')
        return cursor.fetchall()

if __name__ == "__main__":
    print("Initializing database...")
    create_users_table()
    create_home_content_table()
    create_skill_table()
    create_about_page_content_table()
    create_teacher_comment_table()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='content' OR name='skills')")
        tables = cursor.fetchall()
        print(f"Existing tables: {tables}")
        
        cursor.execute("SELECT * FROM content")
        content_rows = cursor.fetchall()
        print(f"Content rows: {len(content_rows)}")
        
        cursor.execute("SELECT * FROM skills")
        skill_rows = cursor.fetchall()
        print(f"Skill rows: {len(skill_rows)}")
        
        cursor.execute("SELECT * FROM about_page_content")
        about_page_content_rows = cursor.fetchall()
        print(f"About page content rows: {len(about_page_content_rows)}")
    
    test_username = "admin"
    test_password = "password"
    teacher_username = "teacher"
    teacher_password = "password"
    content1 = "Hello My Name Is Jacksen"
    content2 = "I build things for the web and AI"
    content3 = "I'm a software developer with a passion for creating innovative solutions at the intersection of AI and web development."
    skills = [
        "Python",
        "JavaScript",
        "Three.js",
        "Machine Learning",
        "Web Development",
        "HTML",
        "CSS",
        "Node.js",
        "Express.js",
        "Flask",
        "Django",
        "FastAPI",
        "Next.js",
        "AWS",
        "Git",
        "PyTorch"
    ]
    

    about_me = "Student at Musashino University"
    who_i_am = "Hello! I'm Jacksen, a student from Malaysia, currently studying at Musashino University in Tokyo, Japan. I specialize in creating innovative solutions at the intersection of AI and web development."
    education1 = "Musashino University, Tokyo, Japan"
    education2 = "Bachelor of Data Science, Expected Graduation: 2027"
    education3 = "Relevant Coursework: Web Development, Cloud Computing"
    interests1 = "I'm interested in AI, Web Development, and Cloud Computing."
    interests2 = "Outside of coding, I enjoy Basketball, Badminton. I believe these activities help me maintain a creative and balanced approach to problem-solving in my technical work."
    connect = "Feel free to reach out to me via email or LinkedIn."
    internship = "Still in progress"
    parttime_job = "I worked as a Manager at McDonald's"
    
    if insert_user(test_username, test_password, 'admin'):
        print(f"Admin user '{test_username}' created successfully.")
    else:
        print(f"Admin user '{test_username}' already exists or there was an error.")
        
    if insert_user(teacher_username, teacher_password, 'teacher'):
        print(f"Teacher user '{teacher_username}' created successfully.")
    else:
        print(f"Teacher user '{teacher_username}' already exists or there was an error.")
    
    insert_home_content(content1)
    insert_home_content(content2)
    insert_home_content(content3)
    
    for skill in skills:
        insert_skill(skill)
    
    insert_about_page_content(1, about_me)
    insert_about_page_content(2, who_i_am)
    insert_about_page_content(3, education1)
    insert_about_page_content(4, education2)
    insert_about_page_content(5, education3)
    insert_about_page_content(6, interests1)
    insert_about_page_content(7, interests2)
    insert_about_page_content(8, connect)
    insert_about_page_content(9, internship)
    insert_about_page_content(10, parttime_job)

    for i in range(1, 4):
        content = get_home_content(i)
        print(f"Content {i}: {content}")

    for i in range(1, 6):
        skill = get_skill(i)
        print(f"Skill {i}: {skill}")

    content4 = "Currently, I'm focused on developing a Text-to-3D Simulation project..."
    content5 = "I'm always eager to take on new challenges..."
    
    if not get_home_content(4):
        insert_home_content(content4)
    if not get_home_content(5):
        insert_home_content(content5)
