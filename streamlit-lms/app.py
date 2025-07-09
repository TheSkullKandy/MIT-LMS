import streamlit as st
from db import (
    init_db, register_user, login_user, add_course, get_courses, add_assignment, get_assignments,
    enroll_in_course, get_enrolled_courses, get_assignments_for_course, submit_assignment, get_submissions_for_user,
    get_students_in_course, get_submissions_for_assignment, grade_submission
)
from views.dashboard import show_dashboard
from views.courses import show_courses
from views.assignments import show_assignments
from views.students import show_students
from views.calendar import show_calendar
from views.virtual_classes import show_virtual_classes
from views.profile import show_profile
from datetime import datetime
from PIL import Image
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("data:image/jpg;base64,%s");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

init_db()

st.set_page_config(page_title="MIT LMS", page_icon=":books:")

# Set background image
bg_image_path = os.path.join(os.path.dirname(__file__), "static", "bg-smoke.jpg")
set_background(bg_image_path)

# --- Sidebar State ---
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'Dashboard'
if 'sidebar_visible' not in st.session_state:
    st.session_state['sidebar_visible'] = True

# Define page configurations
STUDENT_PAGES = [
    {"label": "Dashboard", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><path d='M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z'/></svg>"},
    {"label": "My Courses", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='2' y='7' width='20' height='15' rx='2'/><path d='M16 3v4M8 3v4M2 11h20'/></svg>"},
    {"label": "Assignments", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/></svg>"},
    {"label": "Virtual Classes", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='2' y='7' width='20' height='15' rx='2'/><path d='M16 3v4M8 3v4M2 11h20'/></svg>"},
    {"label": "Calendar", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/></svg>"},
    {"label": "Profile", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><circle cx='12' cy='7' r='4'/><path d='M5.5 21a7.5 7.5 0 0 1 13 0'/></svg>"},
    {"label": "Logout", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><path d='M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4'/><polyline points='16 17 21 12 16 7'/><line x1='21' y1='12' x2='9' y2='12'/></svg>"}
]

FACULTY_PAGES = [
    {"label": "Dashboard", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><path d='M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z'/></svg>"},
    {"label": "My Courses", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='2' y='7' width='20' height='15' rx='2'/><path d='M16 3v4M8 3v4M2 11h20'/></svg>"},
    {"label": "Assignments", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/></svg>"},
    {"label": "Virtual Classes", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='2' y='7' width='20' height='15' rx='2'/><path d='M16 3v4M8 3v4M2 11h20'/></svg>"},
    {"label": "Students", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><circle cx='12' cy='7' r='4'/><path d='M5.5 21a7.5 7.5 0 0 1 13 0'/></svg>"},
    {"label": "Calendar", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/></svg>"},
    {"label": "Profile", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><circle cx='12' cy='7' r='4'/><path d='M5.5 21a7.5 7.5 0 0 1 13 0'/></svg>"},
    {"label": "Logout", "icon": "<svg width='22' height='22' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' viewBox='0 0 24 24'><path d='M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4'/><polyline points='16 17 21 12 16 7'/><line x1='21' y1='12' x2='9' y2='12'/></svg>"}
]

# --- Sidebar Content ---
if st.session_state['user']:
    if st.session_state['sidebar_visible']:
        with st.sidebar:
            st.markdown(
                """
                <style>
                section[data-testid="stSidebar"] {
                    background: linear-gradient(135deg, #4f46e5 0%, #a21caf 100%);
                    opacity: 0.98;
                    color: #fff;
                    padding-top: 2.5em;
                    min-width: 260px;
                    align-items: flex-start !important;
                    border-radius: 1.5em;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.08);
                }
                .sidebar-brand-row {
                    display: flex;
                    align-items: center;
                    gap: 0.8em;
                    margin-bottom: 2em;
                }
                .sidebar-brand-avatar {
                    width: 40px;
                    height: 40px;
                    border-radius: 0.5em;
                    background: #6366f1;
                    color: #fff;
                    font-size: 1.5em;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 8px #6366f144;
                }
                .sidebar-brand-text {
                    font-size: 1.25em;
                    font-weight: 800;
                    letter-spacing: 0.04em;
                    color: #fff;
                    text-align: left;
                }
                .sidebar-user-avatar {
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    background: #fff;
                    color: #4f46e5;
                    font-size: 1.5em;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 0.5em;
                    box-shadow: 0 2px 12px #a21caf33;
                }
                .sidebar-username {
                    font-size: 1.13em;
                    font-weight: 700;
                    color: #fff;
                    margin-bottom: 0.1em;
                    text-align: left;
                }
                .sidebar-role {
                    font-size: 1em;
                    color: #f3e8ff;
                    margin-bottom: 1.5em;
                    text-align: left;
                }
                .sidebar-nav-label {
                    font-size: 1.08em;
                    font-weight: 700;
                    color: #f3e8ff;
                    margin-bottom: 0.7em;
                    margin-top: 1.2em;
                    text-align: left;
                    letter-spacing: 0.03em;
                }
                hr.sidebar-divider {
                    border: none;
                    border-top: 1.5px solid #f3f4f6;
                    margin: 1.2em 0 1em 0;
                    width: 90%;
                    align-self: center;
                }
                /* Selected button override for Streamlit primary - robust */
                section[data-testid="stSidebar"] .stButton > button,
                section[data-testid="stSidebar"] button[data-testid="baseButton-primaryFilled"] {
                    background: #1e293b !important;
                    color: #fff !important;
                    font-weight: 800 !important;
                    border-radius: 2em !important;
                    box-shadow: 0 4px 16px #1e293b33 !important;
                    border: none !important;
                }
                section[data-testid="stSidebar"] .stButton > button:hover,
                section[data-testid="stSidebar"] button[data-testid="baseButton-primaryFilled"]:hover {
                    background: #334155 !important;
                    color: #fff !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            # Select pages based on user type
            PAGES = FACULTY_PAGES if st.session_state['user']['user_type'] == 'faculty' else STUDENT_PAGES

            # Remove duplicate page entries in PAGES (keep only the last occurrence)
            seen = set()
            unique_pages = []
            for page in reversed(PAGES):
                label = page['label'].strip().lower()
                if label not in seen:
                    unique_pages.append(page)
                    seen.add(label)
            PAGES = list(reversed(unique_pages))

            # Brand row
            st.markdown('<div class="sidebar-brand-row">'
                        '<div class="sidebar-brand-avatar">M</div>'
                        '<div class="sidebar-brand-text">MIT LMS</div>'
                        '</div>', unsafe_allow_html=True)
            # User info
            user = st.session_state.get('user', {'name': 'User', 'user_type': 'Student'})
            initials = ''.join([x[0].upper() for x in user['name'].split()]) if user.get('name') else 'U'
            st.markdown(f'<div class="sidebar-user-avatar">{initials}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sidebar-username">{user["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sidebar-role">{user["user_type"].capitalize()}</div>', unsafe_allow_html=True)
            # Navigation label
            st.markdown('<div class="sidebar-nav-label">Navigation</div>', unsafe_allow_html=True)
            # Navigation buttons
            st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
            for idx, page in enumerate(PAGES):
                # Add a divider before Profile/Logout
                if idx == 6:
                    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
                btn_label = page['label']
                if st.button(btn_label, key=f"nav_{page['label']}", type='primary'):
                    st.session_state['page'] = page['label']
            st.markdown('</div>', unsafe_allow_html=True)
            # Hide button
            if st.button("❮❮", key="hide_sidebar_btn", help="Hide sidebar", use_container_width=True):
                st.session_state['sidebar_visible'] = False
    else:
        # Floating unhide button
        st.markdown('''
        <style>
        .unhide-btn {
            position: fixed;
            left: 0.5em;
            top: 50vh;
            z-index: 9999;
            background: linear-gradient(90deg,#6366f1 0%,#a21caf 100%);
            color: #fff;
            border: none;
            border-radius: 2em;
            font-size: 2em;
            font-weight: 900;
            box-shadow: 0 2px 12px #a21caf55;
            padding: 0.2em 0.5em 0.2em 0.5em;
            cursor: pointer;
        }
        </style>
        <button class="unhide-btn" onclick="window.dispatchEvent(new Event('unhideSidebar'))">❯❯</button>
        <script>
        window.addEventListener('unhideSidebar', function() {
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'unhideSidebar', value: true}, '*');
        });
        </script>
        ''', unsafe_allow_html=True)
        # Streamlit button for fallback (for rerun)
        if st.button("Show Sidebar", key="show_sidebar_btn"):
            st.session_state['sidebar_visible'] = True

# --- Page Routing ---
page = st.session_state['page']

# Redirect to Login if user is None
if st.session_state['user'] is None and page != "Login":
    st.session_state['page'] = "Login"
    st.rerun()

# Redirect students if they try to access the Students page
if page == "Students" and st.session_state['user'] and st.session_state['user']['user_type'] != 'faculty':
    st.session_state['page'] = "Dashboard"
    st.rerun()

if page == "Login":
    import base64
    from PIL import Image
    import os
    bg_path = os.path.join(os.path.dirname(__file__), "static", "bg-smoke.jpg")
    def set_background(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            body {{
                background-image: url('data:image/png;base64,{encoded}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            h1 {{
                text-align: center;
                font-size: 3rem;
                color: white;
                margin-bottom: 40px;
            }}
            .form label {{
                color: white !important;
                font-weight: 600;
            }}
            .stTextInput input, .stPasswordInput input {{
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border-radius: 10px;
            }}
            .stButton>button {{
                width: 100%;
                background: linear-gradient(to right, #8e2de2, #4a00e0);
                color: white;
                border: none;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 25px;
                font-weight: bold;
                transition: background 0.3s;
            }}
            .stButton>button:hover {{
                background: linear-gradient(to right, #7b1fa2, #311b92);
            }}
            .avatar-center {{
                display: flex;
                justify-content: center;
                margin-bottom: 24px;
            }}
            </style>
        """, unsafe_allow_html=True)
    set_background(bg_path)
    st.markdown("<h1>Login to MIT LMS</h1>", unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="student@university.edu", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
    login = st.button("Login", key="login_btn")
    signup = st.button("Sign Up", key="signup_btn")
    if login:
        if email and password:
            user = login_user(email)
            if user:
                st.session_state['user'] = {
                    'id': user[0],
                    'email': user[1],
                    'name': user[2],
                    'user_type': user[3]
                }
                st.success("Login successful!")
                st.session_state['page'] = 'Dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials.")
        else:
            st.error("Please fill in all fields.")
    if signup:
        st.session_state['page'] = 'Register'
        st.rerun()
elif page == "Logout":
    st.session_state['user'] = None
    st.session_state['page'] = 'Login'
    st.success("Logged out.")
    st.rerun()
elif page == "Dashboard":
    show_dashboard(st.session_state['user'])
elif page in ["Courses", "My Courses"]:
    show_courses(
        st.session_state['user'],
        get_courses,
        add_course,
        get_enrolled_courses,
        enroll_in_course
    )
elif page == "Assignments":
    show_assignments(
        st.session_state['user'],
        get_assignments,
        add_assignment,
        get_enrolled_courses,
        get_assignments_for_course,
        submit_assignment,
        get_submissions_for_user,
        get_submissions_for_assignment,
        grade_submission
    )
elif page == "Students":
    show_students(
        st.session_state['user'],
        get_courses,
        get_students_in_course
    )
elif page == "Calendar":
    show_calendar()
elif page == "Virtual Classes":
    show_virtual_classes()
elif page == "Profile":
    show_profile(st.session_state['user'])

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    [data-testid="stAppViewBlockContainer"],
    body, .main, .block-container {
        background: transparent !important;
        font-family: 'Inter', sans-serif !important;
    }
    .block-container {
        padding-top: 2.5em !important;
    }
    /* Enhanced Heading Styling with Animations */
    h1, h2, h3, h4, h5, h6, 
    div[data-testid="stHeader"],
    div[data-testid="stMarkdown"] h1,
    div[data-testid="stMarkdown"] h2,
    div[data-testid="stMarkdown"] h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 1em !important;
        transition: all 0.3s ease !important;
    }
    
    /* Main Headers with Enhanced Gradient */
    h1, div[data-testid="stMarkdown"] h1 {
        font-size: 3em !important;
        background: linear-gradient(135deg, #6366f1 0%, #a21caf 50%, #3b82f6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-size: 200% !important;
        animation: gradient 8s ease infinite !important;
        line-height: 1.2 !important;
        margin-top: 0.5em !important;
        padding-bottom: 0.2em !important;
        position: relative !important;
    }
    
    h1::after, div[data-testid="stMarkdown"] h1::after {
        content: "" !important;
        position: absolute !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 2px !important;
        background: linear-gradient(90deg, #6366f1 0%, #a21caf 50%, transparent 100%) !important;
        transform: scaleX(0.8) !important;
        opacity: 0.5 !important;
    }
    
    /* Section Headers with Depth */
    h2, div[data-testid="stMarkdown"] h2 {
        font-size: 2.2em !important;
        color: #f8fafc !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2),
                     0 0 40px rgba(99, 102, 241, 0.2) !important;
        margin-top: 1.2em !important;
        line-height: 1.3 !important;
        position: relative !important;
        padding-left: 1em !important;
    }
    
    h2::before, div[data-testid="stMarkdown"] h2::before {
        content: "" !important;
        position: absolute !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 4px !important;
        height: 70% !important;
        background: linear-gradient(180deg, #6366f1, #a21caf) !important;
        border-radius: 4px !important;
    }
    
    /* Subsection Headers with Style */
    h3, div[data-testid="stMarkdown"] h3 {
        font-size: 1.7em !important;
        background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-top: 1em !important;
        line-height: 1.4 !important;
        display: inline-block !important;
    }
    
    /* Header Cards with Enhanced Design */
    .header-card {
        background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%) !important;
        padding: 2em 2.5em !important;
        border-radius: 1.2em !important;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15),
                    0 2px 8px rgba(162, 28, 175, 0.1) !important;
        margin-bottom: 2em !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .header-card::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%) !important;
        background-size: 200% 200% !important;
        animation: shimmer 3s infinite !important;
        pointer-events: none !important;
    }
    
    .header-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2),
                    0 4px 12px rgba(162, 28, 175, 0.15) !important;
    }
    
    .header-card h1,
    .header-card h2,
    .header-card h3 {
        color: #fff !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2) !important;
        -webkit-text-fill-color: #fff !important;
        font-size: 2.8em !important;
        line-height: 1.2 !important;
        font-weight: 800 !important;
    }
    
    .header-card .subtitle {
        color: #e0e7ff !important;
        font-size: 1.15em !important;
        opacity: 0.95 !important;
        margin-top: 0.5em !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Animations */
    @keyframes gradient {
        0% { background-position: 0% 50% !important; }
        50% { background-position: 100% 50% !important; }
        100% { background-position: 0% 50% !important; }
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0 !important; }
        100% { background-position: -200% 0 !important; }
    }
    
    /* Hover Effects */
    h1:hover, h2:hover, h3:hover {
        transform: translateX(5px) !important;
    }
    
    /* General text color */
    div[data-testid="stMarkdown"] p, 
    div[data-testid="stText"] p,
    .stTextInput label,
    .stSelectbox label,
    .stTextArea label,
    div.stMarkdown,
    div.stText {
        color: #f1f5f9 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2) !important;
        font-size: 1.1em !important;
        line-height: 1.6 !important;
    }
    /* Input fields styling */
    .stTextInput input,
    .stSelectbox select,
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #334155 !important;
        border-radius: 0.5em !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 0.5em 1em !important;
    }
    /* Button styling */
    .stButton > button {
        background: rgba(99, 102, 241, 0.9) !important;
        color: white !important;
        border: none !important;
        padding: 0.5em 2em !important;
        font-weight: 600 !important;
        border-radius: 2em !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: rgba(79, 70, 229, 1) !important;
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 1.5em !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 2em !important;
        margin-bottom: 1.5em !important;
        transition: all 0.3s ease !important;
    }
    .card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.15) !important;
    }
    .card * {
        color: #1e293b !important;
        text-shadow: none !important;
    }
    .card h1, .card h2, .card h3, .card h4, .card h5, .card h6 {
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .card p, .card span, .card div {
        color: #334155 !important;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background: rgba(243, 244, 246, 0.9) !important;
        color: #6366f1 !important;
        border-radius: 1em 1em 0 0 !important;
        font-weight: 700 !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #a21caf !important;
    }
    /* Filter elements styling */
    .stRadio > div {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(162, 28, 175, 0.1) 100%) !important;
        border-radius: 1em !important;
        padding: 1em !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }
    .stRadio > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0.8em !important;
        padding: 0.5em !important;
        margin: 0.2em 0 !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
    }
    .stSelectbox > div {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(162, 28, 175, 0.1) 100%) !important;
        border-radius: 1em !important;
        padding: 0.5em !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }
    .stTextInput > div {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(162, 28, 175, 0.1) 100%) !important;
        border-radius: 1em !important;
        padding: 0.5em !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }
    /* Alert styling */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: 1em !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
    }
    /* Table styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 1em !important;
        overflow: hidden !important;
    }
    .stDataFrame [data-testid="stTable"] {
        background: transparent !important;
    }
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
    }
    /* Sidebar specific styling */
    [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    [data-testid="stSidebar"] div.stText {
        color: #fff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    /* Badge styling */
    .badge-success {
        background: #22c55e !important;
        color: #fff !important;
        padding: 0.2em 0.8em !important;
        border-radius: 1em !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .badge-warning {
        background: #eab308 !important;
        color: #fff !important;
        padding: 0.2em 0.8em !important;
        border-radius: 1em !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .badge-danger {
        background: #ef4444 !important;
        color: #fff !important;
        padding: 0.2em 0.8em !important;
        border-radius: 1em !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    </style>
    """,
    unsafe_allow_html=True
) 