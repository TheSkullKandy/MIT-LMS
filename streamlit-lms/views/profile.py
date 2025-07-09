import streamlit as st
from PIL import Image
import base64
import os

def show_profile(user):
    # Page Header
    st.markdown(
        '''
        <div class="header-card">
            <h2>Profile</h2>
            <div class="subtitle">Manage your personal information, settings, and preferences.</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Enhanced Profile Styling
    st.markdown("""
        <style>
        /* Main Container */
        .profile-wrapper {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2em 0;
        }
        
        /* Profile Header Section (now with purple gradient) */
        .profile-header {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%) !important;
            border-radius: 2.5em;
            padding: 3em;
            margin-bottom: 3em;
                text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
            box-shadow: 0 20px 60px rgba(31, 38, 135, 0.15);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            position: relative;
            overflow: hidden;
        }
        
        .profile-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #6366f1 0%, #a21caf 50%, #ec4899 100%);
        }
        
        /* Avatar Container */
        .avatar-container {
            position: relative;
            display: inline-block;
            margin-bottom: 2em;
        }
        
            .profile-avatar {
            width: 180px;
            height: 180px;
                border-radius: 50%;
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 50%, #ec4899 100%);
                color: #fff;
            font-size: 5em;
            font-weight: 800;
                display: flex;
                align-items: center;
                justify-content: center;
            box-shadow: 0 15px 50px rgba(99, 102, 241, 0.4);
            border: 8px solid rgba(255,255,255,0.95);
            transition: all 0.5s ease;
            position: relative;
            overflow: hidden;
        }
        
        .profile-avatar::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.15), transparent);
            transform: rotate(45deg);
            transition: all 0.8s ease;
            }
            
            .profile-avatar:hover {
            transform: scale(1.1) rotate(3deg);
            box-shadow: 0 25px 70px rgba(99, 102, 241, 0.6);
        }
        
        .profile-avatar:hover::before {
            transform: rotate(45deg) translate(50%, 50%);
        }
        
        /* Profile Info */
        .profile-info {
            margin-bottom: 2em;
        }
        
            .profile-name {
            font-size: 2.5em;
                font-weight: 800;
            color: white !important;
            -webkit-text-fill-color: white !important;
            background: none !important;
            margin-bottom: 0.5em;
                letter-spacing: -0.02em;
            }
            
            .profile-email {
            color: white !important;
            font-size: 1.2em;
            font-weight: 500;
                margin-bottom: 1.5em;
        }
        
        .profile-badge {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%);
            color: #fff;
            padding: 0.8em 2em;
            border-radius: 3em;
            font-weight: 700;
            font-size: 1em;
            display: inline-block;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
            letter-spacing: 0.02em;
            text-transform: uppercase;
            margin-bottom: 2em;
        }
        
        /* Upload Button */
        .upload-btn {
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.95) 50%, rgba(241,245,249,0.9) 100%);
            color: #475569;
            border: 2px solid #e2e8f0;
            padding: 0.8em 2em;
            font-weight: 600;
                border-radius: 1.5em;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            font-size: 1em;
            cursor: pointer;
            display: inline-block;
            text-decoration: none;
        }
        
        .upload-btn:hover {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%);
            color: white;
            border-color: #6366f1;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }
        
        /* Content Grid */
        .profile-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5em;
            margin-top: 2em;
        }
        
        /* Profile Cards (frosted glass style, now with purple gradient) */
        .profile-card {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%) !important;
            border-radius: 2em;
            padding: 2.5em;
            border: 1px solid rgba(255,255,255,0.25);
            box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition: all 0.4s cubic-bezier(.4,2,.6,1);
            position: relative;
            overflow: hidden;
        }
        .profile-card::before {
            display: none;
        }
            .profile-card:hover {
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 25px 70px 0 rgba(80, 0, 120, 0.16), 0 2px 12px 0 rgba(80,0,120,0.10);
        }
        /* Profile Header Section (now with purple gradient) */
        .profile-header {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%) !important;
            border-radius: 2.5em;
            padding: 3em;
            margin-bottom: 3em;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
            box-shadow: 0 20px 60px rgba(31, 38, 135, 0.15);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            position: relative;
            overflow: hidden;
        }
        /* Add spacing before each card header */
        .profile-card .card-header, .profile-card .card-title {
            margin-top: 1.5em;
        }
        .profile-card:first-child .card-header, .profile-card:first-child .card-title {
            margin-top: 0;
        }
        /* Remove special theme-settings-card override */
        .profile-card.theme-settings-card {
            background: none !important;
        }
        /* Main profile info card (if different class, add here) */
        .profile-info-card, .profile-sidebar {
            background: linear-gradient(135deg, rgba(255,255,255,0.85) 60%, rgba(255,255,255,0.55) 100%);
            border-radius: 2em;
            border: 1px solid rgba(255,255,255,0.25);
            box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            }
            
            /* Card Headers */
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 2em;
            padding-bottom: 1em;
                border-bottom: 2px solid #f1f5f9;
                position: relative;
            }
            
        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 15px;
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 1em;
            font-size: 1.5em;
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .card-title {
            font-size: 1.8em;
            font-weight: 800;
            color: white !important;
            -webkit-text-fill-color: white !important;
            background: none !important;
            letter-spacing: -0.02em;
            }
            
            /* Form Fields */
        .form-group {
            margin-bottom: 2em;
        }
        
        .form-label {
            font-weight: 700;
            background: linear-gradient(135deg, #475569 0%, #64748b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
                display: block;
            margin-bottom: 1em;
                font-size: 1.1em;
            letter-spacing: -0.01em;
            }
            
        /* Enhanced Input Fields */
            .stTextInput>div>div>input,
            .stTextArea>div>textarea {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.98) 50%, rgba(241,245,249,0.95) 100%) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 1.2em !important;
            padding: 1.5em 2em !important;
            font-size: 1.1em !important;
                transition: all 0.3s ease !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05) !important;
            color: #1e293b !important;
            min-height: 60px !important;
            }
            
            .stTextInput>div>div>input:focus,
            .stTextArea>div>textarea:focus {
                border-color: #6366f1 !important;
            box-shadow: 0 0 0 5px rgba(99, 102, 241, 0.15) !important;
            background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(248,250,252,1) 50%, rgba(241,245,249,1) 100%) !important;
            transform: translateY(-2px);
            color: #1e293b !important;
        }
        
        /* Text Area specific styling */
        .stTextArea>div>textarea {
            min-height: 120px !important;
            resize: vertical !important;
        }
        
        /* Placeholder text color */
        .stTextInput>div>div>input::placeholder,
        .stTextArea>div>textarea::placeholder {
            color: #94a3b8 !important;
            opacity: 0.8 !important;
        }
        
        /* Disabled input styling */
        .stTextInput>div>div>input:disabled {
            background: linear-gradient(135deg, rgba(241,245,249,0.9) 0%, rgba(226,232,240,0.95) 50%, rgba(203,213,225,0.9) 100%) !important;
            color: #64748b !important;
            opacity: 0.7 !important;
        }
        
        /* Enhanced Checkboxes */
        .stCheckbox>div>div>div {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.98) 50%, rgba(241,245,249,0.95) 100%) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 1.2em !important;
            padding: 1.5em !important;
            margin-bottom: 1em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05) !important;
            color: #1e293b !important;
            font-size: 1.05em !important;
            min-height: 60px !important;
        }
        
        .stCheckbox>div>div>div:hover {
            background: linear-gradient(135deg, rgba(241,245,249,0.95) 0%, rgba(226,232,240,0.98) 50%, rgba(203,213,225,0.95) 100%) !important;
            border-color: #6366f1 !important;
            transform: translateY(-2px);
        }
        
        /* Enhanced Radio Buttons */
        .stRadio>div>div>div {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.98) 50%, rgba(241,245,249,0.95) 100%) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 1.2em !important;
            padding: 1.5em !important;
            margin-bottom: 1em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05) !important;
            color: #1e293b !important;
            font-size: 1.05em !important;
            min-height: 60px !important;
        }
        
        .stRadio>div>div>div:hover {
            background: linear-gradient(135deg, rgba(241,245,249,0.95) 0%, rgba(226,232,240,0.98) 50%, rgba(203,213,225,0.95) 100%) !important;
            border-color: #6366f1 !important;
            transform: translateY(-2px);
        }
        
        /* Enhanced Buttons */
            .stButton>button {
            background: rgba(99, 102, 241, 0.9) !important;
                color: white !important;
                border: none !important;
            padding: 0.5em 2em !important;
                font-weight: 600 !important;
            border-radius: 2em !important;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
                transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            background: rgba(79, 70, 229, 1) !important;
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Success Messages */
        .success-message {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 1.2em;
            padding: 1.5em 2.5em;
            margin: 1.5em 0;
            color: #059669;
            font-weight: 600;
            text-align: center;
            font-size: 1.1em;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .profile-content {
                grid-template-columns: 1fr;
                gap: 2em;
            }
            
            .profile-header {
                padding: 2em;
            }
            
            .profile-avatar {
                width: 140px;
                height: 140px;
                font-size: 4em;
            }
            
            .profile-name {
                font-size: 2em;
            }
        }
        
        /* Additional text styling for better visibility */
        .stMarkdown {
            color: white !important;
        }
        
        .stMarkdown p {
            color: white !important;
        }
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: white !important;
        }
        
        /* Ensure form labels are visible */
        .form-label {
            color: white !important;
            -webkit-text-fill-color: white !important;
            background: none !important;
        }
        
        /* Card titles with white text */
        .card-title {
            color: white !important;
            -webkit-text-fill-color: white !important;
            background: none !important;
        }
        
        /* Profile name and email with white text */
        .profile-name {
            color: white !important;
            -webkit-text-fill-color: white !important;
            background: none !important;
        }
        
        .profile-email {
            color: white !important;
        }

        /* Make all text inside profile cards and sidebar white (even more specific) */
        .profile-card, .profile-card *,
        .profile-sidebar, .profile-sidebar * {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Streamlit radio/checkbox/inputs inside cards */
        .profile-card .stRadio label, .profile-card .stRadio div, .profile-card .stRadio span,
        .profile-card .stCheckbox label, .profile-card .stCheckbox div, .profile-card .stCheckbox span,
        .profile-card .stSelectbox label, .profile-card .stSelectbox div, .profile-card .stSelectbox span,
        .profile-card .stTextInput label, .profile-card .stTextInput div, .profile-card .stTextInput span,
        .profile-card .stTextArea label, .profile-card .stTextArea div, .profile-card .stTextArea span,
        .profile-sidebar .stRadio label, .profile-sidebar .stRadio div, .profile-sidebar .stRadio span,
        .profile-sidebar .stCheckbox label, .profile-sidebar .stCheckbox div, .profile-sidebar .stCheckbox span,
        .profile-sidebar .stSelectbox label, .profile-sidebar .stSelectbox div, .profile-sidebar .stSelectbox span,
        .profile-sidebar .stTextInput label, .profile-sidebar .stTextInput div, .profile-sidebar .stTextInput span,
        .profile-sidebar .stTextArea label, .profile-sidebar .stTextArea div, .profile-sidebar .stTextArea span {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Streamlit auto-generated classes for form labels/options */
        .profile-card .st-bb, .profile-card .st-c3, .profile-card .st-c4, .profile-card .st-c5,
        .profile-sidebar .st-bb, .profile-sidebar .st-c3, .profile-sidebar .st-c4, .profile-sidebar .st-c5 {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Markdown and form-labels inside cards */
        .profile-card .form-label, .profile-card .stMarkdown,
        .profile-sidebar .form-label, .profile-sidebar .stMarkdown {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Radio/checkbox option text inside cards */
        .profile-card .stRadio > label, .profile-card .stRadio > div, .profile-card .stRadio > span,
        .profile-sidebar .stRadio > label, .profile-sidebar .stRadio > div, .profile-sidebar .stRadio > span {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Make radio button label text white inside profile cards */
        .profile-card .stRadio label,
        .profile-card .stRadio div,
        .profile-card .stRadio span {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Frosted glass style for radio group container (white to purple gradient) */
        .profile-card .stRadio > div:first-child {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(162,28,175,0.18) 100%) !important;
            border-radius: 2em !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            padding: 1.2em 2em !important;
            margin-top: 0.5em !important;
        }
        /* Force radio button label text to white in theme settings */
        .profile-card .stRadio label, .profile-card .stRadio span, .profile-card .stRadio div[data-testid="stMarkdownContainer"] {
            color: #fff !important;
            -webkit-text-fill-color: #fff !important;
        }
        /* Theme Settings card with purple gradient background */
        .profile-card.theme-settings-card {
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%) !important;
            border-radius: 2em !important;
            border: 1px solid rgba(255,255,255,0.25) !important;
            box-shadow: 0 15px 50px 0 rgba(80, 0, 120, 0.10), 0 1.5px 8px 0 rgba(80,0,120,0.08) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
        }
        /* Transparent, borderless, and visible Full Name and Email Address input boxes */
        .profile-card .stTextInput[data-testid="stTextInput-full_name"] input,
        .profile-card .stTextInput[data-testid="stTextInput-email"] input {
            background: transparent !important;
            color: #1e293b !important;
            min-height: 56px !important;
            padding: 1.2em 2em !important;
            font-size: 1.08em !important;
            text-align: left !important;
            vertical-align: middle !important;
            border: none !important;
            box-shadow: none !important;
        }
        /* Fully transparent, aesthetic password input boxes in profile page */
        .profile-card .stTextInput[data-testid^="stTextInput-current_pass"] input,
        .profile-card .stTextInput[data-testid^="stTextInput-new_pass"] input,
        .profile-card .stTextInput[data-testid^="stTextInput-confirm_pass"] input {
            background: transparent !important;
            color: #1e293b !important;
            border-radius: 1.2em !important;
            border: 1.5px solid #a21caf33 !important;
            box-shadow: 0 4px 18px 0 rgba(162,28,175,0.10) !important;
            min-height: 54px !important;
            padding: 1.1em 2em !important;
            font-size: 0.95em !important;
            text-align: left !important;
            vertical-align: middle !important;
            transition: box-shadow 0.2s;
        }
        .profile-card .stTextInput[data-testid^="stTextInput-current_pass"] input:focus,
        .profile-card .stTextInput[data-testid^="stTextInput-new_pass"] input:focus,
        .profile-card .stTextInput[data-testid^="stTextInput-confirm_pass"] input:focus {
            box-shadow: 0 0 0 4px #a21caf22 !important;
            border-color: #a21caf !important;
        }
        /* Align password input fields with the outer profile-card box */
        .profile-card .stTextInput[data-testid^="stTextInput-current_pass"],
        .profile-card .stTextInput[data-testid^="stTextInput-new_pass"],
        .profile-card .stTextInput[data-testid^="stTextInput-confirm_pass"] {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .profile-card .stTextInput[data-testid^="stTextInput-current_pass"] input,
        .profile-card .stTextInput[data-testid^="stTextInput-new_pass"] input,
        .profile-card .stTextInput[data-testid^="stTextInput-confirm_pass"] input {
            width: 100% !important;
            box-sizing: border-box !important;
            border-radius: 1.2em !important;
            margin: 0 !important;
        }
        /* Modern standalone password box */
        .modern-password-box {
            background: linear-gradient(135deg, #a21caf 0%, #6366f1 100%);
            border-radius: 2.2em;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.18), 0 2px 8px rgba(162, 28, 175, 0.12);
            padding: 3em 2.5em 2.5em 2.5em;
            margin-bottom: 2.5em;
            margin-top: 1.5em;
            max-width: 480px;
            margin-left: auto;
            margin-right: auto;
            position: relative;
        }
        .modern-password-header {
            display: flex;
            align-items: center;
            gap: 1em;
            margin-bottom: 2em;
        }
        .modern-password-icon {
            font-size: 2em;
            color: #fff;
            background: linear-gradient(135deg, #6366f1 0%, #a21caf 100%);
            border-radius: 1em;
            padding: 0.3em 0.7em;
            box-shadow: 0 2px 8px #a21caf33;
        }
        .modern-password-title {
            font-size: 1.5em;
            font-weight: 800;
                color: #fff;
            letter-spacing: -0.01em;
        }
        .modern-password-fields .form-group {
            margin-bottom: 1.5em;
        }
        .modern-password-fields .form-label {
            color: #fff !important;
                font-weight: 600;
            font-size: 1.08em;
            margin-bottom: 0.7em;
        }
        .modern-password-fields .stTextInput input {
            background: transparent !important;
            color: #fff !important;
            border: 1.5px solid #fff2 !important;
            border-radius: 1.2em !important;
            min-height: 52px !important;
            padding: 1em 1.5em !important;
            font-size: 1em !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.08) !important;
            margin-bottom: 0.5em;
        }
        .modern-password-fields .stTextInput input:focus {
            border-color: #fff !important;
            box-shadow: 0 0 0 3px #a21caf33 !important;
        }
        /* Forcefully remove underline and border from all input boxes in profile-card */
        .profile-card .stTextInput input,
        .profile-card .stTextArea textarea {
            border: none !important;
            border-bottom: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        /* Force password input fields to match select box look */
        .profile-card .stTextInput[data-testid="stTextInput-current_pass"] input,
        .profile-card .stTextInput[data-testid="stTextInput-new_pass"] input,
        .profile-card .stTextInput[data-testid="stTextInput-confirm_pass"] input {
            background: #f1f5f9 !important;
            color: #1e293b !important;
            border-radius: 2em !important;
            border: 2px solid #a78bfa33 !important;
            min-height: 48px !important;
            padding: 1em 1.5em !important;
            font-size: 1.05em !important;
            box-shadow: none !important;
            outline: none !important;
            border-bottom: none !important;
        }
        .profile-card .stTextInput[data-testid="stTextInput-current_pass"] input:focus,
        .profile-card .stTextInput[data-testid="stTextInput-new_pass"] input:focus,
        .profile-card .stTextInput[data-testid="stTextInput-confirm_pass"] input:focus {
            border-color: #a21caf !important;
            box-shadow: 0 0 0 2px #a21caf22 !important;
        }
        /* Modern frosted glass style for password input fields (high specificity) */
        .profile-card .stTextInput input[type="password"] {
            background: linear-gradient(135deg, rgba(162,28,175,0.18) 0%, rgba(99,102,241,0.10) 100%) !important;
            color: #fff !important;
            border-radius: 1.5em !important;
            border: 1.5px solid #a78bfa55 !important;
            min-height: 52px !important;
            padding: 1.15em 1.7em !important;
            font-size: 1.08em !important;
            box-shadow: 0 4px 18px 0 rgba(99,102,241,0.10) !important;
            outline: none !important;
            border-bottom: none !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            transition: box-shadow 0.2s, border-color 0.2s !important;
        }
        .profile-card .stTextInput input[type="password"]:focus {
            border-color: #a21caf !important;
            box-shadow: 0 0 0 4px #a21caf33, 0 4px 18px 0 rgba(99,102,241,0.13) !important;
        }
        .profile-card .stTextInput input[type="password"]::placeholder {
            color: #e0e7ff !important;
            opacity: 0.8 !important;
        }
        /* Remove white underlaying box for Full Name and Email Address input fields */
        .profile-card .stTextInput[data-testid="stTextInput-full_name"] input,
        .profile-card .stTextInput[data-testid="stTextInput-email"] input {
            background: transparent !important;
            color: #1e293b !important;
            border-radius: 1.5em !important;
            border: 1.5px solid #a78bfa55 !important;
            min-height: 52px !important;
            padding: 1.15em 1.7em !important;
            font-size: 1.08em !important;
            box-shadow: 0 4px 18px 0 rgba(99,102,241,0.10) !important;
            outline: none !important;
            border-bottom: none !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            transition: box-shadow 0.2s, border-color 0.2s !important;
        }
        .profile-card .stTextInput[data-testid="stTextInput-full_name"] input:focus,
        .profile-card .stTextInput[data-testid="stTextInput-email"] input:focus {
            border-color: #a21caf !important;
            box-shadow: 0 0 0 4px #a21caf33, 0 4px 18px 0 rgba(99,102,241,0.13) !important;
        }
        .profile-card .stTextInput[data-testid="stTextInput-full_name"] input::placeholder,
        .profile-card .stTextInput[data-testid="stTextInput-email"] input::placeholder {
            color: #e0e7ff !important;
            opacity: 0.8 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Profile Header
    initials = ''.join([name[0] for name in user['name'].split()]).upper()
    st.markdown(f"""
        <div class="profile-wrapper">
            <div class="profile-header">
                <div class="avatar-container">
                <div class="profile-avatar">{initials}</div>
                </div>
                <div class="profile-info">
                <div class="profile-name">{user["name"]}</div>
                <div class="profile-email">{user["email"]}</div>
                    <div class="profile-badge">{user["user_type"].capitalize()}</div>
                    <button class="upload-btn">📷 Upload Picture</button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Profile Content Grid
    st.markdown('<div class="profile-content">', unsafe_allow_html=True)

    # Left Column
    with st.container():
        st.markdown("""
            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon">👤</div>
                    <div class="card-title">Personal Information</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="form-group"><div class="form-label">Full Name</div></div>', unsafe_allow_html=True)
        st.text_input("Full Name", user["name"], label_visibility="collapsed", key="full_name")
        
        st.markdown('<div class="form-group"><div class="form-label">Email Address</div></div>', unsafe_allow_html=True)
        st.text_input("Email Address", user["email"], disabled=True, label_visibility="collapsed", key="email")
        
        st.markdown('<div class="form-group"><div class="form-label">Bio</div></div>', unsafe_allow_html=True)
        st.text_area("Bio", "Passionate learner and aspiring developer. Eager to contribute to innovative projects.", 
                    label_visibility="collapsed", height=150, key="bio")
        
        if st.button("Update Profile", type="primary", key="update_profile"):
            st.markdown('<div class="success-message">✅ Profile updated successfully!</div>', unsafe_allow_html=True)

    # Right Column
    with st.container():
        st.markdown("""
            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon">🔐</div>
                    <div class="card-title">Account Settings</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="form-group"><div class="form-label">Current Password</div></div>', unsafe_allow_html=True)
        st.text_input("Current Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="current_pass")
        st.markdown('<div class="form-group"><div class="form-label">New Password</div></div>', unsafe_allow_html=True)
        st.text_input("New Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="new_pass")
        st.markdown('<div class="form-group"><div class="form-label">Confirm New Password</div></div>', unsafe_allow_html=True)
        st.text_input("Confirm New Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="confirm_pass")
        if st.button("Change Password", type="primary", key="change_pass"):
            st.markdown('<div class="success-message">✅ Password changed successfully!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Section
    st.markdown('<div class="profile-content">', unsafe_allow_html=True)

    # Notification Settings
    with st.container():
        st.markdown("""
            <div class="profile-card">
                <div class="card-header">
                    <div class="card-icon">🔔</div>
                    <div class="card-title">Notification Settings</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown('<span style="color: #fff; font-weight: 500; font-size: 1.1em;">Email notifications for new assignments</span>', unsafe_allow_html=True)
        with col2:
            st.checkbox("Email notifications for new assignments", value=True, key="notif_assignments", label_visibility="collapsed")
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown('<span style="color: #fff; font-weight: 500; font-size: 1.1em;">Email notifications for upcoming deadlines</span>', unsafe_allow_html=True)
        with col2:
            st.checkbox("Email notifications for upcoming deadlines", value=True, key="notif_deadlines", label_visibility="collapsed")
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown('<span style="color: #fff; font-weight: 500; font-size: 1.1em;">Push notifications for virtual class reminders</span>', unsafe_allow_html=True)
        with col2:
            st.checkbox("Push notifications for virtual class reminders", value=True, key="notif_classes", label_visibility="collapsed")

        # Theme Settings
        st.markdown(
            '''
        <div class="profile-card theme-settings-card">
            <div class="card-header">
                <div class="card-icon">🎨</div>
                <div class="card-title">Theme Settings</div>
            </div>
            </div>
            ''',
            unsafe_allow_html=True
        )
    st.markdown('<span style="color: #fff; font-weight: 500; font-size: 1.1em;">Theme</span>', unsafe_allow_html=True)
    st.radio("Theme", ["Light", "Dark", "System"], horizontal=True, index=2, key="theme", label_visibility="collapsed")

    # Add custom CSS for the radio group container
    st.markdown("""
    <style>
    /* Frosted glass style for radio group container */
    .profile-card .stRadio > div:first-child {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 60%, rgba(255,255,255,0.85) 100%) !important;
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

    st.markdown('</div>', unsafe_allow_html=True) 