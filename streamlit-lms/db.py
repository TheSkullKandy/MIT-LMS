import sqlite3
from contextlib import closing

DB_NAME = "lms.db"

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    user_type TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    instructor_id INTEGER,
                    FOREIGN KEY (instructor_id) REFERENCES users(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    course_id INTEGER,
                    due_date TEXT,
                    description TEXT,
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS enrollments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    course_id INTEGER,
                    UNIQUE(user_id, course_id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id INTEGER,
                    user_id INTEGER,
                    content TEXT,
                    submitted_at TEXT,
                    grade REAL,
                    feedback TEXT,
                    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')

def register_user(email, name, user_type):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        try:
            with conn:
                conn.execute(
                    "INSERT INTO users (email, name, user_type) VALUES (?, ?, ?)",
                    (email, name, user_type)
                )
            return True
        except sqlite3.IntegrityError:
            return False

def login_user(email):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, email, name, user_type FROM users WHERE email = ?", (email,))
        return cur.fetchone()

def add_course(title, description, instructor_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO courses (title, description, instructor_id) VALUES (?, ?, ?)",
                (title, description, instructor_id)
            )

def get_courses():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, description, instructor_id FROM courses")
        return cur.fetchall()

def add_assignment(title, course_id, due_date, description):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO assignments (title, course_id, due_date, description) VALUES (?, ?, ?, ?)",
                (title, course_id, due_date, description)
            )

def get_assignments():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, course_id, due_date, description FROM assignments")
        return cur.fetchall()

def enroll_in_course(user_id, course_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        try:
            with conn:
                conn.execute(
                    "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
                    (user_id, course_id)
                )
            return True
        except sqlite3.IntegrityError:
            return False

def get_enrolled_courses(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, c.title, c.description, c.instructor_id
            FROM courses c
            JOIN enrollments e ON c.id = e.course_id
            WHERE e.user_id = ?
        """, (user_id,))
        return cur.fetchall()

def get_assignments_for_course(course_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, course_id, due_date, description FROM assignments WHERE course_id = ?", (course_id,))
        return cur.fetchall()

def submit_assignment(assignment_id, user_id, content, submitted_at):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "INSERT INTO submissions (assignment_id, user_id, content, submitted_at) VALUES (?, ?, ?, ?)",
                (assignment_id, user_id, content, submitted_at)
            )

def get_submissions_for_user(user_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, assignment_id, content, submitted_at, grade, feedback FROM submissions WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def get_students_in_course(course_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.name, u.email
            FROM users u
            JOIN enrollments e ON u.id = e.user_id
            WHERE e.course_id = ? AND u.user_type = 'student'
        """, (course_id,))
        return cur.fetchall()

def get_submissions_for_assignment(assignment_id):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.user_id, u.name, s.content, s.submitted_at, s.grade, s.feedback
            FROM submissions s
            JOIN users u ON s.user_id = u.id
            WHERE s.assignment_id = ?
        """, (assignment_id,))
        return cur.fetchall()

def grade_submission(submission_id, grade, feedback):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "UPDATE submissions SET grade = ?, feedback = ? WHERE id = ?",
                (grade, feedback, submission_id)
            )

if __name__ == "__main__":
    init_db() 