import streamlit as st
from datetime import datetime

# Assignment Page: Shows assignments for students and instructors

def show_assignments(user, get_assignments, add_assignment, get_enrolled_courses, get_assignments_for_course, submit_assignment, get_submissions_for_user, get_submissions_for_assignment, grade_submission):
    # Assignment Page Styling
    st.markdown("""
<style>
.assignment-card {
    background: #fff !important;
    border-radius: 2em;
    border: 1px solid rgba(0,0,0,0.07);
    box-shadow: 0 8px 32px rgba(80, 0, 120, 0.08), 0 1.5px 8px 0 rgba(80,0,120,0.04);
    padding: 2.5em;
    margin-bottom: 2em;
    color: #000 !important;
    transition: all 0.4s cubic-bezier(.4,2,.6,1);
    position: relative;
    overflow: hidden;
    filter: none !important;
    opacity: 1 !important;
}
.assignment-card::before,
.assignment-card::after {
    display: none !important;
    content: none !important;
}
.assignment-title, .assignment-course, .assignment-desc, .assignment-meta {
    background: unset !important;
    -webkit-text-fill-color: unset !important;
    background-clip: unset !important;
}
.assignment-status {
    color: #fff !important;
}
.status-submitted { background: linear-gradient(135deg, #22c55e, #16a34a); }
.status-graded { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.status-pending { background: linear-gradient(135deg, #f97316, #ea580c); }
.status-late { background: linear-gradient(135deg, #ef4444, #dc2626); }
.status-upcoming { background: linear-gradient(135deg, #a855f7, #9333ea); }
.stRadio label, .stRadio div, .stRadio span {
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
}
.stRadio > div:first-child {
    background: linear-gradient(135deg, rgba(162,28,175,0.18) 0%, rgba(99,102,241,0.10) 100%) !important;
    border-radius: 2em !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    padding: 1.2em 2em !important;
    margin-top: 0.5em !important;
}
.stAlert, .stAlert p, .stAlert span {
    color: #fff !important;
}
.stSuccess {
    background: linear-gradient(135deg, #4f46e5 0%, #a21caf 100%) !important;
    color: #fff !important;
    border-radius: 2em !important;
    box-shadow: 0 8px 32px rgba(80, 0, 120, 0.10) !important;
    -webkit-text-fill-color: unset !important;
    text-shadow: none !important;
    font-weight: 600 !important;
    font-size: 1.15em !important;
    padding: 1.5em 2em !important;
    margin-bottom: 1.5em !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    opacity: 0.98 !important;
}
</style>
""", unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="header-card">
            <h2>Assignments</h2>
            <div class="subtitle">Track, submit, and manage all your course assignments.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    is_student = user['user_type'] == 'student'

    # Student Assignment List
    if is_student:
        assignments = [
            {"id": 1, "title": "JavaScript Basics Quiz", "course": "Introduction to Programming", "dueDate": "2025-06-01", "status": "submitted", "description": "Complete the online quiz about JavaScript fundamentals.", "grade": None, "feedback": None},
            {"id": 2, "title": "Binary Search Tree Implementation", "course": "Data Structures", "dueDate": "2025-05-20", "status": "graded", "description": "Implement a binary search tree with insert, delete, and search operations.", "grade": 92, "feedback": "Excellent work!"},
            {"id": 3, "title": "Database Schema Design", "course": "Database Systems", "dueDate": "2025-05-25", "status": "pending", "description": "Design a database schema for an online bookstore.", "grade": None, "feedback": None},
            {"id": 4, "title": "Machine Learning Model Training", "course": "AI Basics", "dueDate": "2025-05-18", "status": "late", "description": "Train a simple classification model using the provided dataset.", "grade": None, "feedback": None},
            {"id": 5, "title": "Neural Network Architecture", "course": "AI Basics", "dueDate": "2025-06-10", "status": "upcoming", "description": "Design a neural network architecture for image recognition.", "grade": None, "feedback": None}
        ]
        
        tabs = ["All", "Pending", "Submitted", "Graded", "Upcoming", "Late"]
        filter_status = st.radio("Filter assignments by status:", tabs, horizontal=True)
        filtered_assignments = [a for a in assignments if filter_status == "All" or a['status'].lower() == filter_status.lower()]
        if not filtered_assignments:
            st.info(f"No {filter_status.lower()} assignments found.")
        else:
            cols = st.columns(2)
            for i, a in enumerate(filtered_assignments):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="card assignment-card">
                        <div class="assignment-title">{a['title']}</div>
                        <div class="assignment-course">{a['course']}</div>
                        <p class="assignment-desc">{a['description']}</p>
                        <div class="assignment-meta">
                            <div>Due: {a['dueDate']}</div>
                            <div class="assignment-status status-{a['status']}">{a['status'].capitalize()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if a['status'] == 'graded' and a['grade']:
                        st.success(f"**Grade: {a['grade']}%** - {a.get('feedback', '')}")
                    with st.expander("Submit or View"):
                        if a['status'] in ['pending', 'upcoming', 'late']:
                            st.text_area("Your submission:", key=f"sub_{a['id']}")
                            st.button("Submit", key=f"btn_sub_{a['id']}", use_container_width=True)
                        else:
                            st.info("You have already submitted this assignment.")
    else:
        # Instructor Assignment Management
        st.subheader("Manage Course Assignments")
        assignments = [
            {"id": 1, "title": "OOP Design Patterns", "course": "Advanced Programming", "dueDate": "2025-05-30", "submissions": 32, "total": 45},
            {"id": 2, "title": "React State Management", "course": "Web Development", "dueDate": "2025-05-26", "submissions": 38, "total": 38},
            {"id": 3, "title": "Cross-platform UI", "course": "Mobile Development", "dueDate": "2025-06-05", "submissions": 0, "total": 32}
        ]
        cols = st.columns(2)
        for i, a in enumerate(assignments):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="card assignment-card">
                    <div class="assignment-title">{a['title']}</div>
                    <div class="assignment-course">{a['course']}</div>
                    <div class="assignment-meta">
                        <div>Due: {a['dueDate']}</div>
                        <div>Submissions: {a['submissions']}/{a['total']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View & Grade Submissions", key=f"grade_{a['id']}", use_container_width=True):
                    st.info(f"Navigating to grading interface for '{a['title']}'...")
        with st.expander("➕ Create a New Assignment", expanded=False):
            with st.form("new_assignment_form", clear_on_submit=True):
                st.text_input("Assignment Title")
                st.selectbox("Course", ["Advanced Programming", "Web Development", "Mobile Development"])
                st.date_input("Due Date")
                st.text_area("Description")
                if st.form_submit_button("Create Assignment", use_container_width=True):
                    st.success("New assignment created successfully!") 