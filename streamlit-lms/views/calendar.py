# Calendar Page
import streamlit as st
import calendar as pycal
from datetime import date, timedelta, datetime

def show_calendar():
    # Calendar Display
    st.markdown("""
    <style>
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0.4em;
        margin: 1.5em 0;
    }
    .calendar-day {
        background: rgba(255, 255, 255, 0.98) !important;
        border: 2px solid rgba(124, 58, 237, 0.18) !important; /* soft indigo border */
        border-radius: 1em;
        padding: 0.8em;
        text-align: center;
        min-height: 100px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.10), 0 2px 8px rgba(162, 28, 175, 0.08) !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        color: #1e293b !important;
    }
    .calendar-day:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.18) !important;
        background: #f3f4f6 !important;
    }
    .calendar-day.selected {
        background: linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%) !important;
        border: 2.5px solid #a21caf !important;
        transform: scale(1.02);
    }
    .calendar-day.today {
        background: linear-gradient(135deg, #e0e7ff 0%, #ede9fe 100%) !important;
        border: 2.5px solid #6366f1 !important;
    }
    .calendar-day.other-month {
        opacity: 0.4;
        background: rgba(255, 255, 255, 0.6);
    }
    .day-name, .day-number, .event-count {
        color: #4f46e5 !important;
        background: none !important;
        -webkit-text-fill-color: unset !important;
    }
    .day-number {
        font-size: 1.6em;
        font-weight: 700;
        margin-bottom: 0.6em;
    }
    .day-number.other-month {
        background: linear-gradient(135deg, #94a3b8 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .event-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #a21caf);
        margin: 2px auto;
        display: inline-block;
    }
    .event-count {
        font-size: 0.7em;
        color: #6366f1 !important;
        font-weight: 600;
        margin-top: 0.3em;
    }
    .month-header {
        text-align: center;
        margin-bottom: 2em;
        padding: 1.5em;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(162, 28, 175, 0.1) 100%);
        border-radius: 1.2em;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .month-title {
        font-size: 2.2em;
        font-weight: 800;
        color: #fff !important;
        background: none !important;
        -webkit-text-fill-color: #fff !important;
        background-clip: unset !important;
        margin-bottom: 0.5em;
    }
    .month-subtitle {
        font-size: 1.2em;
        color: #fff !important;
        font-weight: 500;
    }
    .day-header {
        text-align: center;
        font-weight: 700;
        color: #6366f1;
        font-size: 1.1em;
        padding: 0.6em 0;
        margin-bottom: 0.8em;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(162, 28, 175, 0.05) 100%);
        border-radius: 0.8em;
    }
    .week-row {
        margin-bottom: 1.2em;
    }
    .event-details {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(162, 28, 175, 0.1) 100%);
        border-radius: 1.2em;
        padding: 1.5em;
        margin-top: 2em;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .event-item {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 1em;
        padding: 1em;
        margin-bottom: 1em;
        border-left: 4px solid #6366f1;
        box-shadow: 0 4px 16px rgba(31, 38, 135, 0.1);
    }
    .event-title {
        font-size: 1.2em;
        font-weight: 700;
        background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5em;
    }
    .event-meta {
        font-size: 0.9em;
        color: #334155 !important;
        margin-bottom: 0.3em;
    }
    .event-type-badge {
        display: inline-block;
        padding: 0.2em 0.6em;
        border-radius: 0.8em;
        font-size: 0.8em;
        font-weight: 600;
        color: white !important;
        margin-top: 0.5em;
    }
    .type-class { background: linear-gradient(135deg, #3b82f6, #2563eb); }
    .type-assignment { background: linear-gradient(135deg, #f97316, #ea580c); }
    .type-exam { background: linear-gradient(135deg, #ef4444, #dc2626); }
    .type-deadline { background: linear-gradient(135deg, #a855f7, #9333ea); }
    .card, .card * {
        color: #1e293b !important;
        background: none !important;
        -webkit-text-fill-color: #1e293b !important;
        text-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="header-card">
            <h2>Academic Calendar</h2>
            <div class="subtitle">Stay organized with your academic schedule, events, and deadlines.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Sample events data with more details
    sample_events = [
        {"id": 1, "title": "JavaScript Event Loop Deep Dive", "date": (date.today() + timedelta(days=1)), "type": "class", "course": "Introduction to Programming", "time": "10:00 AM - 11:00 AM", "description": "Virtual class on JavaScript's event loop"},
        {"id": 2, "title": "JavaScript Basics Quiz", "date": date.today(), "type": "assignment", "course": "Introduction to Programming", "time": "Due by 11:59 PM", "description": "Online quiz covering JavaScript fundamentals"},
        {"id": 3, "title": "Database Schema Design", "date": (date.today() + timedelta(days=2)), "type": "assignment", "course": "Database Systems", "time": "Due by 11:59 PM", "description": "Design a database schema for an online bookstore"},
        {"id": 4, "title": "Introduction to Neural Networks", "date": (date.today() + timedelta(days=3)), "type": "class", "course": "AI Basics", "time": "2:00 PM - 3:30 PM", "description": "Live session on neural network fundamentals"},
        {"id": 5, "title": "Data Structures Midterm Exam", "date": (date.today() + timedelta(days=5)), "type": "exam", "course": "Data Structures", "time": "9:00 AM - 11:00 AM", "description": "Comprehensive exam on data structures"},
        {"id": 6, "title": "AVL Trees Implementation", "date": date.today(), "type": "class", "course": "Data Structures", "time": "1:00 PM - 2:30 PM", "description": "Hands-on session on AVL tree implementation"},
        {"id": 7, "title": "SQL Query Optimization", "date": (date.today() - timedelta(days=1)), "type": "class", "course": "Database Systems", "time": "3:00 PM - 4:30 PM", "description": "Advanced SQL optimization techniques"},
        {"id": 8, "title": "Final Project Submission", "date": (date.today() + timedelta(days=14)), "type": "deadline", "course": "All Courses", "time": "Due by 11:59 PM", "description": "Final project submission deadline"}
    ]

    # Create event lookup by date
    events_by_date = {}
    for event in sample_events:
        event_date = event['date']
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)

    # Month header
    current_month = datetime.now().strftime('%B %Y')
    st.markdown(f"""
    <div class="month-header">
        <div class="month-title">{current_month}</div>
        <div class="month-subtitle">Current Month Overview</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Day names header
    day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    day_header_cols = st.columns(7)
    for i, day_name in enumerate(day_names):
        with day_header_cols[i]:
            st.markdown(f'<div class="day-header">{day_name}</div>', unsafe_allow_html=True)
    
    # Calendar grid
    today = date.today()
    year, month = today.year, today.month
    cal = pycal.Calendar(firstweekday=6)
    month_days = list(cal.itermonthdates(year, month))

    # Group days into weeks
    weeks = []
    week = []
    for day in month_days:
        week.append(day)
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:  # Add the last week if it's not full
        weeks.append(week)

    # Initialize session state for selected date
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = None

    # Create a date selector
    st.markdown("### Select a Date to View Events")
    date_options = []
    for event in sample_events:
        date_str = event['date'].strftime('%A, %B %d, %Y')
        if date_str not in date_options:
            date_options.append(date_str)
    
    # Add today's date if no events
    today_str = date.today().strftime('%A, %B %d, %Y')
    if today_str not in date_options:
        date_options.insert(0, today_str)
    
    selected_date_str = st.selectbox(
        "Choose a date:",
        date_options,
        index=0 if not st.session_state.selected_date else None,
        key="date_selector"
    )
    
    # Convert selected date string back to date object
    if selected_date_str:
        try:
            # Parse the date string
            selected_date = datetime.strptime(selected_date_str, '%A, %B %d, %Y').date()
            st.session_state.selected_date = selected_date
        except:
            st.session_state.selected_date = date.today()

    # Display calendar grid
    for week_idx, week_data in enumerate(weeks):
        st.markdown('<div class="week-row">', unsafe_allow_html=True)
        cols = st.columns(7)
        for i, day in enumerate(week_data):
            with cols[i]:
                is_today = day == today
                is_current_month = day.month == month
                is_selected = st.session_state.selected_date == day
                # Get events for this day
                day_events = events_by_date.get(day, [])
                # Determine CSS classes
                day_class = "calendar-day"
                if is_today:
                    day_class += " today"
                if not is_current_month:
                    day_class += " other-month"
                if is_selected:
                    day_class += " selected"
                number_class = "day-number"
                if not is_current_month:
                    number_class += " other-month"
                # Create day name
                day_name = day_names[day.weekday()]
                # Build events HTML
                events_html = ""
                if day_events:
                    events_html = '<div class="event-dot"></div>'
                    if len(day_events) > 1:
                        events_html += f'<div class="event-count">{len(day_events)} events</div>'
                st.markdown(f"""
                <div class="{day_class}">
                    <div class="day-name">{day_name}</div>
                    <div class="{number_class}">{day.day}</div>
                    {events_html}
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Display selected date events
    if st.session_state.selected_date:
        selected_date = st.session_state.selected_date
        selected_events = events_by_date.get(selected_date, [])
        
        if selected_events:
            st.markdown(f"""
            <div class="event-details">
                <h3 style="background: linear-gradient(135deg, #1e293b 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1em;">
                    Events for {selected_date.strftime('%A, %B %d, %Y')}
                </h3>
            """, unsafe_allow_html=True)
            
            for event in selected_events:
                st.markdown(f"""
                <div class="event-item">
                    <div class="event-title">{event['title']}</div>
                    <div class="event-meta">Course: {event['course']}</div>
                    <div class="event-meta">Time: {event['time']}</div>
                    <div class="event-meta">Description: {event['description']}</div>
                    <div class="event-type-badge type-{event['type']}">{event['type'].title()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="event-details">
                <h3 style="background: linear-gradient(135deg, #1e293b 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1em;">
                    {selected_date.strftime('%A, %B %d, %Y')}
                </h3>
                <p style="color: #334155 !important; text-align: center; font-style: italic;">No events scheduled for this date.</p>
            </div>
            """, unsafe_allow_html=True)

    # Summary section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("This Month's Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="background: linear-gradient(135deg, #1e293b 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Total Events</h4>
            <p style="color: #334155 !important;">8 events scheduled</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="background: linear-gradient(135deg, #1e293b 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Assignments</h4>
            <p style="color: #334155 !important;">3 assignments due</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4 style="background: linear-gradient(135deg, #1e293b 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Classes</h4>
            <p style="color: #334155 !important;">4 virtual classes</p>
        </div>
        """, unsafe_allow_html=True) 