import streamlit as st
import google.generativeai as genai
import json
import re
import urllib.parse
from PIL import Image
import io
import time
import hashlib

# ==========================================
# 1. THE BRAIN (Backend Setup)
# ==========================================
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

from PIL import Image
import os

# Create the variable first so Python knows it exists
logo_img = None 

# Check if the file is actually there
# Check if the file exists AND if it's a valid image
try:
    if os.path.exists("logo.png"):
        logo_img = Image.open("logo.png")
except Exception:
    logo_img = None  # If the image is broken, this prevents the crash!
# This function is used later in the app (like at Line 268)
def render_logo(size=120):
    if logo_img is not None:
        st.image(logo_img, width=size)
    else:
        st.info("Trust Lens AI: System Active")

# Display the logo immediately at the top
render_logo(size=200)
# Initialize Session State for Auth and History
if 'users' not in st.session_state:
    st.session_state.users = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'result_data' not in st.session_state:
    st.session_state.result_data = None

# Helper functions for Auth
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def show_educational_hub():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🛡️ SCAM INTELLIGENCE HUB (APRIL 2026)")
    st.caption("Real-time awareness of trending digital fraud tactics across India.")

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🚨 Digital Arrest / CBI Scam"):
            st.write("**Modus Operandi:** Fake officers on WhatsApp video claiming you have an illegal parcel.")
            st.error("FACT: Indian law has NO 'Digital Arrest' concept. Hang up immediately.")
        with st.expander("📦 Courier / Customs Scam"):
            st.write("**Modus Operandi:** SMS about a 'failed delivery' asking for a ₹5-₹10 're-delivery fee'.")
            st.error("FACT: They want your CVV/OTP to wipe your account, not deliver a box.")
    with col2:
        with st.expander("💼 AI-Powered Job/Task Scam"):
            st.write("**Modus Operandi:** 'Like YouTube videos' for money. Uses AI to sound very real.")
            st.error("FACT: If they pay you ₹500 and then ask for ₹5000 'investment', it's a scam.")
        with st.expander("💳 UPI / Reward Points Scam"):
            st.write("**Modus Operandi:** Fake 'Collect' requests or QR codes sent to your WhatsApp.")
            st.error("FACT: You NEVER need to enter your PIN or scan a QR to RECEIVE money.")

    # Community Intelligence Section
    st.markdown("### 🏘️ Community Intelligence")
    if 'reports' in st.session_state and st.session_state.reports:
        for r in st.session_state.reports[::-1]:
            st.warning(f"⚠️ **{r['type']} Alert**: {r['detail']}")
    else:
        st.info("No localized community reports yet. Be the first to alert others in the sidebar!")
def scam_iq_quiz():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🧠 NEURAL DEFENSE: SCAM IQ TEST")
    
    # This makes the message pop in a bright box
    st.warning("📩 **NEW MESSAGE RECEIVED:**\n\n'Dear Customer, your Electricity power will be disconnected tonight at 9:30 PM. Please contact our officer at 98123-XXXXX immediately.'")
    
    # The question and options
    st.markdown("### **Is this message legitimate or a scam?**")
    choice1 = st.radio("", ["✅ Legitimate", "🚨 Scam"], key="quiz_q1")
    
    if st.button("VERIFY NEURAL MATCH"):
        if "Scam" in choice1:
            st.success("🎯 **CORRECT!** Red Flags: Extreme urgency, random mobile number, and unofficial language. Real utility companies never threaten immediate disconnection via SMS.")
        else:
            st.error("❌ **INCORRECT.** This is a 'Panic Scam'. Always verify through the official App or Website, never by calling a number in an SMS.")
def community_reporter():
    with st.sidebar:
        st.markdown("---")
        st.subheader("📢 Report a New Scam")
        with st.form("report_form", clear_on_submit=True):
            scam_type = st.selectbox("Type", ["WhatsApp Fraud", "Job Scam", "Bank/UPI Call", "Courier Scam", "Digital Arrest"])
            scam_details = st.text_area("Describe the tactics used:")
            submitted = st.form_submit_button("SUBMIT THREAT REPORT")
            
            if submitted:
                if scam_details:
                    if 'reports' not in st.session_state:
                        st.session_state.reports = []
                    st.session_state.reports.append({"type": scam_type, "detail": scam_details})
                    st.success("Identity Verified. Threat Logged.")
                else:
                    st.warning("Please provide details for the database.")
def render_logo(size=100):
    if 'logo_img' in globals() and logo_img is not None:
        st.image(logo_img, width=size)
    else:
        st.info("🛡️ Trust Lens AI: System Active")

# ==========================================
# 2. THE LOOK (Animated Neo-Digital Realism UI)
# ==========================================
st.set_page_config(page_title="Trust Lens AI", page_icon="🛡️", layout="wide")

# Custom CSS for Motion Effects & Global Atmosphere
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Montserrat:wght@700;800&display=swap');

    /* Global Atmosphere: Digital Background Animation */
    .stApp {{
        background: linear-gradient(180deg, #050A30 0%, #000000 100%);
        background-attachment: fixed;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        opacity: 0.05;
        pointer-events: none;
        z-index: 0;
    }}

    /* Auth Page Specific Styles */
    .auth-container {{
        max-width: 450px;
        margin: 100px auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        box-shadow: 0 25px 60px rgba(0, 245, 255, 0.1);
        text-align: center;
        animation: slide-in 0.8s ease-out forwards;
    }}

    /* Keyframes for Animations */
    @keyframes pulse-cyan {{
        0% {{ box-shadow: 0 0 10px rgba(0, 245, 255, 0.2); }}
        50% {{ box-shadow: 0 0 25px rgba(0, 245, 255, 0.5); border-color: rgba(0, 245, 255, 0.6); }}
        100% {{ box-shadow: 0 0 10px rgba(0, 245, 255, 0.2); }}
    }}

    @keyframes pulse-amethyst {{
        0% {{ box-shadow: 0 10px 30px rgba(191, 64, 191, 0.1); }}
        50% {{ box-shadow: 0 15px 45px rgba(191, 64, 191, 0.25); }}
        100% {{ box-shadow: 0 10px 30px rgba(191, 64, 191, 0.1); }}
    }}

    @keyframes slide-in {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes radar-spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    /* Futuristic Scanner Portal (Input) */
    .stTextArea textarea, .stTextInput input {{
        background: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid rgba(0, 245, 255, 0.2) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 12px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: #00F5FF !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.4) !important;
        background: rgba(0, 0, 0, 0.6) !important;
    }}

    /* Functional Buttons with 'Pressed' State */
    .stButton>button {{
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 50%, rgba(255,255,255,0.1) 100%), 
                    linear-gradient(90deg, #00F5FF, #BF40BF) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 15px 30px !important;
        font-weight: 800 !important;
        font-family: 'Montserrat', sans-serif !important;
        letter-spacing: 1.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        position: relative;
        overflow: hidden;
    }}

    .stButton>button:active {{
        transform: scale(0.98) !important;
        filter: brightness(0.8);
    }}

    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0, 245, 255, 0.5);
    }}

    /* Result Grid Cards */
    .grid-card {{
        background: rgba(255, 255, 255, 0.04);
        border-left: 5px solid #00F5FF;
        padding: 20px;
        border-radius: 18px;
        height: 100%;
        box-shadow: 0 10px 30px rgba(191, 64, 191, 0.1);
        animation: pulse-amethyst 6s infinite ease-in-out;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .grid-card:hover {{
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 50px rgba(191, 64, 191, 0.4);
    }}

    /* Sidebar Dashboard Styling */
    .sidebar-dashboard {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}
    
    .history-item {{
        background: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        border-left: 4px solid #00F5FF;
        transition: all 0.3s ease;
    }}
    
    .stat-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        border: 1px solid rgba(0, 245, 255, 0.1);
    }}

    .cyan-glow {{ color: #00F5FF; text-shadow: 0 0 15px rgba(0, 245, 255, 0.6); font-family: 'Montserrat', sans-serif; }}
    .amethyst-glow {{ color: #BF40BF; text-shadow: 0 0 15px rgba(191, 64, 191, 0.6); font-family: 'Montserrat', sans-serif; }}
    
    .punchy-point {{
        background: rgba(0, 245, 255, 0.12);
        padding: 8px 14px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 0.95rem;
    }}

    /* Circular Gauge */
    .gauge-container {{ position: relative; width: 220px; height: 220px; margin: auto; }}
    .gauge-outer {{
        width: 220px; height: 220px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.2);
    }}
    .gauge-inner {{
        width: 185px; height: 185px; border-radius: 50%;
        background: #050A30; display: flex; flex-direction: column; align-items: center; justify-content: center;
    }}

    /* Floating Footer */
    .floating-footer {{
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(5, 10, 48, 0.85); backdrop-filter: blur(15px);
        padding: 20px 0; border-top: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 999; text-align: center;
    }}
    
    .whatsapp-btn {{
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 50%, rgba(255,255,255,0.15) 100%), #25D366 !important;
        color: white !important; padding: 15px 40px; border-radius: 35px; text-decoration: none;
        font-weight: 800; font-family: 'Montserrat', sans-serif; display: inline-flex; align-items: center;
        gap: 12px; box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4); transition: all 0.3s ease;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. AUTHENTICATION GATEWAY
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    # Assuming you named your variable 'logo_img' earlier
    render_logo(size=120)
    st.markdown("<h1 class='cyan-glow'>TRUST LENS AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.7;'>Neural Security Gateway</p>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["LOGIN", "SIGN UP"])
    
    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("AUTHORIZE ACCESS"):
            if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.user_id = username
                st.success("Access Granted. Initializing Dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Neural match failed.")
                
    with tab_signup:
        new_user = st.text_input("Create Username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", key="signup_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.button("CREATE NEURAL ID"):
            if not new_user or not new_pass:
                st.warning("All fields required.")
            elif new_user in st.session_state.users:
                st.error("Username already exists in mainframe.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                st.session_state.users[new_user] = hash_password(new_pass)
                st.success("Identity Created. Please Login.")
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 4. SIDEBAR (Neural History Dashboard)
# ==========================================
with st.sidebar:
    st.markdown(f"<p class='cyan-glow' style='font-size:0.8rem;'>AUTHORIZED: {st.session_state.user_id.upper()}</p>", unsafe_allow_html=True)
    if st.button("LOGOUT / SECURE TERMINAL"):
        st.session_state.authenticated = False
        st.rerun()
        
    st.divider()
    st.markdown("<h2 class='cyan-glow'>INTEL DASHBOARD</h2>", unsafe_allow_html=True)
    
    # Quick Stats
    total_scans = len(st.session_state.scan_history)
    threats = len([s for s in st.session_state.scan_history if s['status'] in ['FRAUDULENT', 'SUSPICIOUS']])
    
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"<div class='stat-card'><p style='margin:0; font-size:0.7rem; opacity:0.6;'>TOTAL SCANS</p><h3 style='margin:0; color:#00F5FF;'>{total_scans}</h3></div>", unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"<div class='stat-card'><p style='margin:0; font-size:0.7rem; opacity:0.6;'>THREATS</p><h3 style='margin:0; color:#BF40BF;'>{threats}</h3></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; font-weight:bold; margin-bottom:10px;'>RECENT ACTIVITY</p>", unsafe_allow_html=True)
    
    if not st.session_state.scan_history:
        st.markdown("<div class='sidebar-dashboard'><p style='opacity:0.5; text-align:center; font-size:0.8rem;'>No scan logs found.</p></div>", unsafe_allow_html=True)
    else:
        for scan in reversed(st.session_state.scan_history[-5:]):
            badge_color = "#00F5FF" if scan['status'] == 'VERIFIED' else "#BF40BF" if scan['status'] == 'SUSPICIOUS' else "#FF4B4B"
            st.markdown(f"""
                <div class='history-item'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;'>
                        <span style='background:{badge_color}22; color:{badge_color}; border-radius:4px; padding:2px 8px; font-size:0.7rem; font-weight:bold;'>{scan['status']}</span>
                        <span style='font-size:0.7rem; opacity:0.4;'>Just Now</span>
                    </div>
                    <p style='margin:0; font-size:0.8rem; font-weight:bold;'>{scan['score']}% Trust Index</p>
                    <p style='margin:0; font-size:0.7rem; opacity:0.6; line-height:1.2;'>{scan['text'][:50]}...</p>
                </div>
            """, unsafe_allow_html=True)
            
    st.divider()
    st.markdown("<p style='text-align:center; font-size:0.7rem; opacity:0.4;'>SYSTEM STATUS: OPERATIONAL</p>", unsafe_allow_html=True)

# ==========================================
# 5. MAIN APP INTERFACE
# ==========================================

cols = st.columns([1, 4, 1])
with cols[1]:
    render_logo(size=80)
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;' class='cyan-glow'>TRUST LENS AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Animated Intelligence Dashboard</p>", unsafe_allow_html=True)

# Main Scanner Area
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
col_in1, col_in2 = st.columns([3, 1])
with col_in1:
    user_input = st.text_area("SCANNER INTERFACE", placeholder="Paste suspicious message or link here...", height=150, label_visibility="collapsed")
    file_col1, file_col2 = st.columns(2)
    with file_col1:
        uploaded_image = st.file_uploader("UPLOAD SCREENSHOT", type=['png', 'jpg', 'jpeg'])
    with file_col2:
        uploaded_audio = st.file_uploader("UPLOAD VOICE NOTE", type=['wav', 'mp3', 'm4a'])

with col_in2:
    language = st.selectbox("INTEL LANGUAGE", ["English", "Kannada", "Hindi"])
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("INITIATE NEURAL SCAN")
st.markdown("</div>", unsafe_allow_html=True)

if analyze_btn:
    if not user_input and not uploaded_image and not uploaded_audio:
        st.warning("Input required for neural analysis.")
    else:
        # FORENSIC LOADING EXPERIENCE
        loading_placeholder = st.empty()
        status_messages = ["Executing Deep Forensic Analysis...", "Scanning Source Reliability...", "Checking AI Patterns...", "Finalizing Neural Verdict..."]
        for msg in status_messages:
            loading_placeholder.markdown(f"<div style='text-align:center; padding:50px;'><div style='width:80px; height:80px; border:4px solid #00F5FF; border-top-color:transparent; border-radius:50%; animation: radar-spin 1.5s linear infinite; margin:auto;'></div><p class='cyan-glow' style='margin-top:20px;'>{msg}</p></div>", unsafe_allow_html=True)
            time.sleep(1)
        loading_placeholder.empty()

        with st.spinner("Finalizing Verdict..."):
            try:
                # Prepare Multimodal Content
                prompt = f"""
                You are a world-class forensic investigator and cybersecurity expert. Analyze this input in {language}.
                Return ONLY a JSON object with this structure:
                {{
                  "trust_score": (integer 0-100),
                  "status": "VERIFIED" or "SUSPICIOUS" or "FRAUDULENT",
                  "grid": {{
                    "source": {{ "title": "Source Check", "points": ["EMOJI_SHORT_TAG_1", "EMOJI_SHORT_TAG_2"] }},
                    "tone": {{ "title": "Vibe Check", "points": ["EMOJI_SHORT_TAG_1", "EMOJI_SHORT_TAG_2"] }},
                    "facts": {{ "title": "Fact Check", "points": ["EMOJI_SHORT_TAG_1", "EMOJI_SHORT_TAG_2"] }},
                    "flags": {{ "title": "Red Flags", "points": ["EMOJI_SHORT_TAG_1", "EMOJI_SHORT_TAG_2"] }}
                  }},
                  "shield_tips": ["SHORT_TIP_1", "SHORT_TIP_2", "SHORT_TIP_3"],
                  "smart_reply": "A direct 1st-person casual message in {language}.",
                  "cautionary_forward": "A message in {language} to forward to groups."
                }}
                """
                content_parts = [prompt, user_input if user_input else "Analyze the attached file."]
                if uploaded_image: content_parts.append(Image.open(uploaded_image))
                if uploaded_audio: content_parts.append({"mime_type": uploaded_audio.type, "data": uploaded_audio.read()})

                response = model.generate_content(content_parts)
                clean_json = re.search(r'\{.*\}', response.text, re.DOTALL).group()
                data = json.loads(clean_json)
                
                st.session_state.scan_history.append({'text': user_input[:50] if user_input else "Media Scan", 'score': data['trust_score'], 'status': data['status']})
                st.session_state.result_data = data

                # RESULT REVEAL
                st.markdown("---")
                res_col1, res_col2 = st.columns([1, 2])
                with res_col1:
                    score = data['trust_score']
                    status_color = "#00F5FF" if score > 70 else "#BF40BF" if score > 40 else "#FF4B4B"
                    st.markdown(f"""<div class="gauge-container"><div class="gauge-outer" style="--score: {score * 3.6}deg; background: conic-gradient({status_color} {score * 3.6}deg, #1A1A1B 0deg);"><div class="gauge-inner"><h1 style="color:{status_color}; font-family:'Montserrat'; font-size:3rem; margin:0;">{score}%</h1><p style="margin:0; opacity:0.6; font-size:0.8rem;">TRUST SCORE</p></div></div></div><h3 style='text-align: center; color: {status_color}; margin-top: 15px;'>{data['status']}</h3>""", unsafe_allow_html=True)
                
                with res_col2:
                    grid = data['grid']
                    gcol1, gcol2 = st.columns(2)
                    for idx, (key, card_data) in enumerate(grid.items()):
                        target_col = gcol1 if idx < 2 else gcol2
                        glow = "cyan-glow" if idx % 2 == 0 else "amethyst-glow"
                        with target_col:
                            st.markdown(f"""<div class='grid-card'><p class='{glow}' style='margin-bottom:10px;'><b>{card_data['title']}</b></p>{"".join([f"<div class='punchy-point'>{p}</div>" for p in card_data['points']])}</div><br>""", unsafe_allow_html=True)

                st.markdown(f"""<div class='glass-card' style='border: 1px solid #BF40BF;'><p class='amethyst-glow' style='font-size: 1.1rem;'><b>🛡️ EDUCATION SHIELD TIPS</b></p><ul>{"".join([f"<li>{tip}</li>" for tip in data['shield_tips']])}</ul></div>""", unsafe_allow_html=True)

                st.markdown("<br><h3 class='cyan-glow'>WHATSAPP TOOLKIT</h3>", unsafe_allow_html=True)
                tk_col1, tk_col2 = st.columns(2)
                with tk_col1:
                    st.markdown(f"""<div class='glass-card' style='height: 100%;'><p class='cyan-glow'><b>💬 DIRECT REPLY</b></p><p style='font-style: italic; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px;'>"{data['smart_reply']}"</p></div>""", unsafe_allow_html=True)
                with tk_col2:
                    st.markdown(f"""<div class='glass-card' style='height: 100%; border-color: #BF40BF;'><p class='amethyst-glow'><b>🛡️ CAUTIONARY FORWARD</b></p><p style='font-style: italic; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px;'>"{data['cautionary_forward']}"</p></div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Neural scan interrupted: {str(e)}")
community_reporter()                
show_educational_hub() 
scam_iq_quiz()
# FLOATING FOOTER
if st.session_state.result_data:
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(st.session_state.result_data['cautionary_forward'])}"
    st.markdown(f"""<div class="floating-footer"><div style="display: flex; justify-content: center; gap: 20px; align-items: center;"><p style="margin:0; font-size: 0.8rem; opacity: 0.6;">QUICK FORWARD:</p><a href="{whatsapp_url}" target="_blank" class="whatsapp-btn"><span>FORWARD CAUTIONARY MESSAGE</span><span style="font-size: 1.2rem;">🛡️</span></a></div></div><div style="margin-bottom: 120px;"></div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div class="floating-footer"><p style="opacity: 0.5; font-size: 0.9rem;">Scan a message or media to enable sharing toolkit</p></div><div style="margin-bottom: 120px;"></div>""", unsafe_allow_html=True)
