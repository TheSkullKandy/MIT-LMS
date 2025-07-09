# Student List Page
import streamlit as st

def show_students(user, get_courses, get_students_in_course):
    # --- Custom CSS for Students Page ---
    st.markdown("""
    <style>
    .student-card {
        display: flex;
        align-items: center;
        gap: 1.5em;
    }
    .student-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #a21caf);
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        font-weight: 700;
    }
    .student-info {
        flex-grow: 1;
    }
    .student-name {
        font-size: 1.4em;
        font-weight: 800;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .student-email {
        font-size: 1em;
        margin-bottom: 0.8em;
        color: #334155 !important;
    }
    .student-meta {
        display: flex;
        gap: 1.5em;
        color: #334155 !important;
    }
    .student-status {
        font-weight: 700;
        padding: 0.3em 0.8em;
        border-radius: 1em;
        color: #fff !important;
        font-size: 0.9em;
    }
    .status-active { background: linear-gradient(135deg, #22c55e, #16a34a); }
    .status-warning { background: linear-gradient(135deg, #f97316, #ea580c); }
    .status-at-risk { background: linear-gradient(135deg, #ef4444, #dc2626); }
    </style>
    """, unsafe_allow_html=True)

    # --- Page Header ---
    st.markdown(
        '''
        <div class="header-card">
            <h2>Student Management</h2>
            <div class="subtitle">Monitor and manage student performance and progress.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if user['user_type'] != 'faculty':
        st.warning("You must be a faculty member to view this page.")
        return

    # --- Sample Data ---
    sample_students = [
        {"id": 1, "name": "Alice Johnson", "email": "alice.j@university.edu", "grade": "A", "attendance": "98%", "status": "active", "courses": 4},
        {"id": 2, "name": "Bob Smith", "email": "bob.s@university.edu", "grade": "B+", "attendance": "92%", "status": "active", "courses": 3},
        {"id": 3, "name": "Charlie Brown", "email": "charlie.b@university.edu", "grade": "A-", "attendance": "95%", "status": "active", "courses": 4},
        {"id": 4, "name": "Diana Prince", "email": "diana.p@university.edu", "grade": "C", "attendance": "85%", "status": "warning", "courses": 4},
        {"id": 5, "name": "Eric Williams", "email": "eric.w@university.edu", "grade": "B", "attendance": "90%", "status": "active", "courses": 3},
        {"id": 6, "name": "Fiona Garcia", "email": "fiona.g@university.edu", "grade": "A", "attendance": "97%", "status": "active", "courses": 5},
        {"id": 7, "name": "George Miller", "email": "george.m@university.edu", "grade": "D+", "attendance": "75%", "status": "at-risk", "courses": 4},
        {"id": 8, "name": "Hannah Lee", "email": "hannah.l@university.edu", "grade": "B-", "attendance": "88%", "status": "active", "courses": 4},
    ]

    # --- Filters ---
    filter_cols = st.columns([3, 1])
    with filter_cols[0]:
        search_query = st.text_input("Search students by name or email...", placeholder="🔍 Search...")
    with filter_cols[1]:
        status_filter = st.selectbox("Filter by status", ["All", "Active", "Warning", "At-risk"])

    # --- Student List ---
    filtered_students = sample_students
    if search_query:
        filtered_students = [s for s in filtered_students if search_query.lower() in s['name'].lower() or search_query.lower() in s['email'].lower()]
    if status_filter != "All":
        filtered_students = [s for s in filtered_students if s['status'].lower() == status_filter.lower()]

    if not filtered_students:
        st.info(f"No students found matching your criteria.")
    else:
        for s in filtered_students:
            initials = ''.join([name[0] for name in s['name'].split()]).upper()
            st.markdown(f"""
            <div class="card student-card">
                <div class="student-avatar">{initials}</div>
                <div class="student-info">
                    <div class="student-name">{s['name']}</div>
                    <div class="student-email">{s['email']}</div>
                    <div class="student-meta">
                        <span>Grade: {s['grade']}</span>
                        <span>Attendance: {s['attendance']}</span>
                        <span>Courses: {s['courses']}</span>
                    </div>
                </div>
                <div class="student-status status-{s['status']}">{s['status'].replace('-', ' ').title()}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("View Details & Actions"):
                st.write(f"Detailed performance for **{s['name']}**...")
                st.button("Send Message", key=f"msg_{s['id']}")
                st.button("View Full Report", key=f"report_{s['id']}") 