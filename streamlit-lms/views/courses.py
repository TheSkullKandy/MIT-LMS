# Courses Page
import streamlit as st
import numpy as np
from collections import defaultdict

def show_courses(user, get_courses, add_course, get_enrolled_courses, enroll_in_course):
    # Custom CSS for card, badge, button, and progress bar
    st.markdown('''<style>
    .course-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1.5em;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 1.5em;
        margin-bottom: 1.5em;
        transition: all 0.3s ease;
    }
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.15);
    }
    .course-title {font-size: 1.5em; font-weight: 800; color: #1e293b; margin-bottom: 0.5em;}
    .course-desc {font-size: 1.05em; color: #475569; margin-bottom: 1em; min-height: 3.2em;}
    .course-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%);
        color: #fff;
        font-weight: 600;
        padding: 0.3em 1em;
        border-radius: 1em;
        font-size: 0.9em;
        margin-right: 0.5em;
        margin-bottom: 1em;
    }
    .course-progress-bar {
        height: 8px;
        width: 100%;
        background: #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    .course-progress-inner {
        height: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a21caf 100%);
        border-radius: 8px;
    }
    </style>''', unsafe_allow_html=True)

    # Page header
    st.markdown(
        '''
        <div class="header-card">
            <h2>Courses</h2>
            <div class="subtitle">Explore, enroll, and manage your courses.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    is_student = user['user_type'] == 'student'

    # Get all courses and enrolled courses
    all_courses = get_courses()
    enrolled_courses = get_enrolled_courses(user['id']) if is_student else []
    enrolled_ids = {c[0] for c in enrolled_courses}
    
    # Determine which courses to display as "My Courses"
    my_courses_data = enrolled_courses if is_student else all_courses

    # Prepare course data
    def get_category(title):
        if "web" in title.lower(): return "Information Technology"
        return "Computer Science"

    my_courses = [
        {"id": c[0], "title": c[1], "description": c[2], "instructor": "Faculty", "progress": np.random.randint(30, 100), "category": get_category(c[1])}
        for c in my_courses_data
    ]
    
    grouped = defaultdict(list)
    for c in my_courses:
        grouped[c["category"]].append(c)

    # Section: My Courses / Courses You Teach
    section_title = "My Enrolled Courses" if is_student else "Courses You Teach"
    st.header(section_title)
    
    if my_courses:
        for cat, courses in grouped.items():
            st.subheader(cat)
            cols = st.columns(2)
            for i, course in enumerate(courses):
                with cols[i % 2]:
                    st.markdown(f'''
                    <div class="course-card">
                        <div class="course-title">{course['title']}</div>
                        <div class="course-desc">{course['description']}</div>
                        <div class="course-badge">Instructor: {course['instructor']}</div>
                        <div class="course-progress-bar">
                            <div class="course-progress-inner" style="width:{course['progress']}%"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    elif is_student:
        st.info("You are not enrolled in any courses yet. Enroll in a course below to get started!")
    else: # Faculty
        st.info("You haven't created any courses yet. Add a course below to get started!")


    # Student: Enroll in Course
    if is_student:
        available_courses = [c for c in all_courses if c[0] not in enrolled_ids]
        if available_courses:
            st.header("Enroll in a New Course")
            cols = st.columns(2)
            for i, c in enumerate(available_courses):
                with cols[i % 2]:
                    st.markdown(f'''
                    <div class="course-card">
                        <div class="course-title">{c[1]}</div>
                        <div class="course-desc">{c[2]}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    if st.button("Enroll Now", key=f"enroll_{c[0]}", use_container_width=True):
                        if enroll_in_course(user['id'], c[0]):
                            st.success(f"Successfully enrolled in {c[1]}!")
                            st.rerun()
                        else:
                            st.warning(f"You are already enrolled in {c[1]}.")
        elif not my_courses:
             st.info("There are no new courses available for enrollment at this time. Please check back later.")
    
    # Faculty: Add Course
    else: # Faculty
        with st.expander("➕ Add a New Course", expanded=False):
            with st.form("new_course_form", clear_on_submit=True):
                title = st.text_input("Course Title")
                desc = st.text_area("Course Description")
                submitted = st.form_submit_button("Create Course")
                
                if submitted:
                    if title and desc:
                        add_course(title, desc, user['id'])
                        st.success(f"Course '{title}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Please provide both a title and description for the course.") 