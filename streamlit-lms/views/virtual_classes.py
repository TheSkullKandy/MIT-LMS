# Virtual Classes Page
import streamlit as st
import datetime

def show_virtual_classes():
    st.markdown("""
    <style>
    .vc-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a21caf 60%, #ec4899 100%) !important;
        border-radius: 2em !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin-bottom: 2em !important;
        color: #fff !important;
        transition: all 0.4s cubic-bezier(.4,2,.6,1) !important;
        position: relative !important;
    }
    .vc-card:hover {
        transform: translateY(-5px) scale(1.01) !important;
        box-shadow: 0 25px 70px 0 rgba(80, 0, 120, 0.16), 0 2px 12px 0 rgba(80,0,120,0.10) !important;
    }
    .vc-info {
        padding: 1.5em !important;
        background: linear-gradient(135deg, #7c3aed 0%, #a21caf 60%, #ec4899 100%) !important;
        color: #fff !important;
        border-bottom-left-radius: 2em !important;
        border-bottom-right-radius: 2em !important;
    }
    .vc-title, .vc-card * {
        color: #fff !important;
        -webkit-text-fill-color: unset !important;
        text-shadow: none !important;
        background: none !important;
    }
    .vc-course {
        font-size: 1em;
        font-weight: 600;
        color: #e0e7ff !important;
        margin-bottom: 1em;
    }
    .vc-meta {
        margin-bottom: 0.5em;
        color: #f3f4f6 !important;
    }
    .vc-status {
        font-weight: 700;
        padding: 0.3em 0.8em;
        border-radius: 1em;
        color: #fff !important;
        font-size: 0.9em;
        display: inline-block;
        margin-top: 1em;
    }
    .status-live { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .status-upcoming { background: linear-gradient(135deg, #a855f7, #9333ea); }
    .status-completed { background: linear-gradient(135deg, #22c55e, #16a34a); }
    /* Make all text in radio group white */
    .stRadio label, .stRadio div, .stRadio span {
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
    }
    /* Gradient frosted glass style for radio group container */
    .stRadio > div:first-child {
        background: linear-gradient(135deg, #7c3aed 0%, #a21caf 60%, #ec4899 100%) !important;
        border-radius: 2em !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08) !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        padding: 1.2em 2em !important;
        margin-top: 0.5em !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="header-card">
            <h2>Virtual Classes</h2>
            <div class="subtitle">Join live classes, access recordings, and manage your virtual classroom sessions.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    sample_classes = [
        {"id": 1, "title": "Event Loop Deep Dive", "course": "JavaScript", "instructor": "Dr. Sarah Johnson", "startTime": (datetime.datetime.now() + datetime.timedelta(hours=1)), "duration": 60, "status": "upcoming", "thumbnailUrl": "https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?auto=format&fit=crop&w=1470&q=80"},
        {"id": 2, "title": "AVL Trees & Balancing", "course": "Data Structures", "instructor": "Prof. Michael Chen", "startTime": datetime.datetime.now(), "duration": 90, "status": "live", "thumbnailUrl": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1470&q=80"},
        {"id": 3, "title": "SQL Query Optimization", "course": "Database Systems", "instructor": "Dr. David Wilson", "startTime": (datetime.datetime.now() - datetime.timedelta(hours=2)), "duration": 75, "status": "completed", "recordingUrl": "#", "thumbnailUrl": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1470&q=80"},
        {"id": 4, "title": "Intro to Neural Networks", "course": "AI Basics", "instructor": "Prof. E. Rodriguez", "startTime": (datetime.datetime.now() + datetime.timedelta(hours=26)), "duration": 120, "status": "upcoming", "thumbnailUrl": "https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?auto=format&fit=crop&w=1470&q=80"},
        {"id": 5, "title": "Advanced React Patterns", "course": "Web Development", "instructor": "Prof. Alex Morgan", "startTime": (datetime.datetime.now() - datetime.timedelta(days=3)), "duration": 90, "status": "completed", "recordingUrl": "#", "thumbnailUrl": "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=1470&q=80"}
    ]

    tabs = ["All", "Live", "Upcoming", "Completed"]
    filter_status = st.radio("Filter classes by status:", tabs, horizontal=True)

    filtered_classes = [c for c in sample_classes if filter_status == "All" or c['status'].lower() == filter_status.lower()]
    
    if not filtered_classes:
        st.info(f"No {filter_status.lower()} classes found.")
    else:
        cols = st.columns(2)
        for i, cls in enumerate(filtered_classes):
            with cols[i % 2]:
                # The card itself should have no padding as the info div has it
                st.markdown(f"""
                <div class="card vc-card" style="padding: 0 !important;">
                    <div class="vc-thumbnail">
                        <img src="{cls['thumbnailUrl']}" style="width: 100%;" />
                    </div>
                    <div class="vc-info">
                        <div class="vc-title">{cls['title']}</div>
                        <div class="vc-course">{cls['course']}</div>
                        <div class="vc-meta">
                            <span>Instructor: {cls['instructor']}</span><br>
                            <span>Starts: {cls['startTime'].strftime('%b %d, %I:%M %p')}</span><br>
                            <span>Duration: {cls['duration']} min</span>
                        </div>
                        <div class="vc-status status-{cls['status']}">{cls['status'].capitalize()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                action_button_label = ""
                if cls['status'] == 'live':
                    action_button_label = "Join Live Class"
                elif cls['status'] == 'completed':
                    action_button_label = "Watch Recording"
                elif cls['status'] == 'upcoming':
                    action_button_label = "Add to Calendar"
                
                if action_button_label:
                    st.button(action_button_label, key=f"btn_{cls['id']}", use_container_width=True) 