import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard(user):
    # Dashboard Styling
    st.markdown("""
    <style>
    /* Remove card and kpi-card backgrounds and borders */
    .kpi-icon {
        font-size: 2em;
        margin-bottom: 0.5em;
        opacity: 0.8;
        color: #fff !important;
    }
    .kpi-value {
        font-size: 2.5em;
        font-weight: 800;
        background: none !important;
        color: #fff !important;
        margin-bottom: 0.3em;
    }
    .kpi-label {
        font-size: 1.1em;
        font-weight: 600;
        color: #fff !important;
        margin-bottom: 0.5em;
    }
    .kpi-delta {
        font-size: 0.9em;
        font-weight: 600;
        padding: 0.3em 0.8em;
        border-radius: 1em;
        display: inline-block;
        color: #fff !important;
    }
    .delta-pos { 
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white !important;
    }
    .delta-neg { 
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white !important;
    }
    .course-progress-title {
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 1em;
        background: none !important;
        color: #fff !important;
    }
    .progress-bar-container {
        width: 100%;
        background-color: #e2e8f0;
        border-radius: 1em;
        height: 12px;
        overflow: hidden;
        margin-bottom: 0.5em;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a21caf 100%);
        border-radius: 1em;
    }
    .progress-percentage {
        font-size: 0.9em;
        font-weight: 600;
        color: #fff !important;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

    # Gradient header card for main heading
    st.markdown(
        f'''
        <div style="
            max-width: 900px;
            margin: 0 auto 2em auto;
            padding: 2.5em 2em 2em 2em;
            border-radius: 2.5em;
            background: linear-gradient(135deg, rgba(99,102,241,0.85) 0%, rgba(162,28,175,0.85) 100%);
            box-shadow: 0 20px 60px rgba(31, 38, 135, 0.15);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            position: relative;
            overflow: hidden;
            text-align: left;
        ">
            <h2 style="margin-bottom:0.2em; color:#fff; font-size:2.8em; font-weight:800; letter-spacing:-0.02em;">Welcome back, {user["name"]}!</h2>
            <div style="color:#fff; font-size:1.25em; margin-bottom:0; font-weight:500;">Here's a snapshot of your academic progress and upcoming tasks.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Main Performance Graph - Larger and more prominent
    st.subheader("Academic Performance Overview")
    with st.container():
        grades = pd.DataFrame({
            "Course": ["Mathematics", "Physics", "Chemistry", "Programming", "Data Structures", "Database Systems"],
            "Grade": [85, 76, 90, 95, 88, 92]
        })
        fig = px.bar(
            grades, x="Course", y="Grade", color="Grade",
            color_continuous_scale=["#e0e7ff", "#c7d2fe", "#a5b4fc", "#818cf8", "#a78bfa", "#f0abfc"],
            height=400,
            title="Course Performance Analysis",
            opacity=0.85
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="#fff",
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False, title=None, color="#fff"),
            yaxis=dict(showgrid=True, gridcolor="rgba(167,139,250,0.2)", title="Grade (%)", color="#fff"),
            title_font_size=20,
            title_font_color="#fff"
        )
        fig.update_traces(marker_line_color="#fff", marker_line_width=1.5, opacity=0.85)
        st.plotly_chart(fig, use_container_width=True)

    # KPI Cards Section
    st.subheader("Quick Statistics")
    kpi_cols = st.columns(4)
    kpis = [
        {"icon": "📚", "value": "6", "label": "Assignments Due", "delta": "+2", "delta_class": "delta-pos"},
        {"icon": "⭐", "value": "83%", "label": "Average Grade", "delta": "-1%", "delta_class": "delta-neg"},
        {"icon": "💻", "value": "2", "label": "Upcoming Classes", "delta": "", "delta_class": ""},
        {"icon": "✅", "value": "94%", "label": "Attendance", "delta": "", "delta_class": ""}
    ]
    for i, kpi in enumerate(kpis):
        with kpi_cols[i]:
            st.markdown(f"""
                <div class="kpi-icon">{kpi['icon']}</div>
                <div class="kpi-value">{kpi['value']}</div>
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-delta {kpi['delta_class']}">{kpi['delta']}</div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Courses Progress Section
    st.subheader("Course Progress")
    courses = [
        {"title": "Introduction to Programming", "progress": 75},
        {"title": "Data Structures and Algorithms", "progress": 60},
        {"title": "Database Management Systems", "progress": 90},
        {"title": "Artificial Intelligence Basics", "progress": 30}
    ]
    
    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="course-progress-title">{course['title']}</div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: {course['progress']}%"></div>
                </div>
                <div class="progress-percentage">{course['progress']}% Complete</div>
            """, unsafe_allow_html=True)

    # What's Next Section
    st.subheader("Upcoming Activities")
    next_cols = st.columns(2)
    with next_cols[0]:
        st.markdown("""
            <h4 style="color:#fff;">Next Assignment</h4>
            <p style="color: #fff !important;"><strong>Calculus III: Final Exam</strong></p>
            <p style="color: #fff !important;">Due in 3 days</p>
        """, unsafe_allow_html=True)
    with next_cols[1]:
        st.markdown("""
            <h4 style="color:#fff;">Next Virtual Class</h4>
            <p style="color: #fff !important;"><strong>Web Development: State Management</strong></p>
            <p style="color: #fff !important;">Tomorrow at 10:00 AM</p>
        """, unsafe_allow_html=True) 