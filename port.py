import streamlit as st
import json
import streamlit.components.v1 as components
import google.generativeai as genai
import uuid

# --- Page Config ---
st.set_page_config(
    page_title="Sahil Desai | Portfolio",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="collapsed"
)

# --- Gemini Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    model = None

# --- Custom CSS (Global Styles) ---
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* GLOBAL THEME */
    .stApp {
        background-color: #020202;
        background-image: 
            radial-gradient(at 0% 0%, rgba(0, 243, 255, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(188, 19, 254, 0.05) 0px, transparent 50%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    p {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.15rem !important;
        font-weight: 500;
        color: #b0b0b0;
        line-height: 1.5;
    }

    /* NEON TEXT EFFECTS */
    .neon-cyan { color: #00f3ff; text-shadow: 0 0 10px rgba(0, 243, 255, 0.6); }
    .neon-purple { color: #bc13fe; text-shadow: 0 0 10px rgba(188, 19, 254, 0.6); }

    /* PROJECT CARDS */
    .neon-card {
        background: rgba(20, 20, 20, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #333;
        border-radius: 8px;
        padding: 30px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        height: 100%;
    }
    
    .neon-card::before {
        content: ""; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(0, 243, 255, 0.15), transparent);
        transition: all 0.6s;
    }
    .neon-card:hover::before { left: 100%; }
    .neon-card:hover {
        transform: translateY(-8px) scale(1.01);
        border-left: 4px solid #00f3ff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 20px rgba(0, 243, 255, 0.4);
        background: rgba(30, 30, 30, 0.9);
    }

    /* TECH BADGES */
    .tech-badge {
        font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #00f3ff;
        background: rgba(0, 243, 255, 0.08); border: 1px solid rgba(0, 243, 255, 0.3);
        padding: 4px 10px; border-radius: 4px; margin-right: 8px; display: inline-block;
        transition: 0.3s; margin-bottom: 5px;
    }
    .tech-badge:hover { background: rgba(0, 243, 255, 0.2); box-shadow: 0 0 10px rgba(0, 243, 255, 0.4); cursor: default; }

    /* TERMINAL INPUT */
    .stTextInput input {
        background-color: #080808 !important; border: 1px solid #333 !important;
        color: #00f3ff !important; font-family: 'JetBrains Mono', monospace; font-size: 1rem;
    }
    .stTextInput input:focus { border-color: #00f3ff !important; box-shadow: 0 0 15px rgba(0, 243, 255, 0.15) !important; }

    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} .block-container {padding-top: 3rem; padding-bottom: 3rem;}
</style>
""", unsafe_allow_html=True)

# --- HELPER: Load Lottie Local File ---
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

# --- HELPER: Render Lottie in Neon Box (Fixed Method) ---
def st_lottie_neon(json_data, height=300, key=None):
    if json_data is None:
        st.error("Animation file not found or invalid.")
        return
    
    # Generate a unique ID for the Javascript to target
    unique_id = f"lottie_{uuid.uuid4().hex}"
    
    # Dump JSON to string for Javascript embedding
    json_str = json.dumps(json_data)
    
    # HTML Component with JS Loader
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <style>
            body {{ margin: 0; overflow: hidden; background: transparent; }}
            .neon-container {{
                background: rgba(10, 10, 10, 0.6);
                border: 2px solid #00f3ff;
                border-radius: 15px;
                padding: 15px;
                /* Subtract padding and border from height */
                height: {height-40}px; 
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 20px rgba(0, 243, 255, 0.4), inset 0 0 15px rgba(0, 243, 255, 0.1);
                backdrop-filter: blur(5px);
                animation: pulse-border 4s infinite alternate;
                margin: 5px;
            }}
            
            @keyframes pulse-border {{
                0% {{ border-color: #00f3ff; box-shadow: 0 0 20px rgba(0, 243, 255, 0.4); }}
                100% {{ border-color: #bc13fe; box-shadow: 0 0 30px rgba(188, 19, 254, 0.6); }}
            }}
            
            lottie-player {{ width: 100%; height: 100%; }}
        </style>
    </head>
    <body>
        <div class="neon-container">
            <lottie-player 
                id="{unique_id}" 
                background="transparent" 
                speed="1" 
                loop 
                autoplay>
            </lottie-player>
        </div>
        <script>
            // Safely load the animation data using JavaScript
            const animData = {json_str};
            const player = document.getElementById("{unique_id}");
            player.load(animData);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

# --- LOAD ASSETS ---
# Make sure these filenames match exactly what is in your folder
lottie_hero = load_lottiefile("Background looping animation.json")
lottie_about = load_lottiefile("Coding.json") 
lottie_chat = load_lottiefile("Typing Animation.json")

# --- 1. HERO SECTION ---
col1, col2 = st.columns([1.8, 1], gap="medium")

with col1:
    st.markdown('<p style="color:#00f3ff; font-family:JetBrains Mono; font-size:1rem; margin-bottom:0;">> INITIALIZING_PORTFOLIO...</p>', unsafe_allow_html=True)
    st.markdown("""
        <h1 style='font-size: 5rem; line-height: 0.9; margin-bottom: 15px; color: white;'>
            I AM <span class='neon-cyan'>Shressh sandip ghambir</span>
        </h1>
        <h3 style='font-size: 1.8rem; color: #888; margin-bottom: 25px;'>
            ENGINEERING INTELLIGENCE & <span class='neon-purple'>SOLVING COMPLEXITY</span>
        </h3>
        <p>
            VJTI Mumbai Sophomore (EXTC). I don't just write code; I architect systems. 
            Bridging the gap between <b>Hardware (IoT)</b> and <b>High-Level Intelligence (ML)</b>.
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="margin-top: 30px; margin-bottom: 30px;">
            <span class="tech-badge">PYTHON</span>
            <span class="tech-badge">TENSORFLOW</span>
            <span class="tech-badge">C++</span>
            <span class="tech-badge">ESP32</span>
            <span class="tech-badge">STREAMLIT</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the fixed Neon Function
    st_lottie_neon(lottie_hero, height=420, key="hero")

st.markdown("---")

# --- 2. ABOUT ME ---
st.markdown("<h2 style='margin-bottom: 30px;'><span class='neon-cyan'>//</span> ABOUT_ME</h2>", unsafe_allow_html=True)

col_about_text, col_about_anim = st.columns([2, 1], gap="large")

with col_about_text:
    st.markdown("""
    <div class='neon-card'>
        <p style='color: #eee;'>
            I am an engineer at heart. My work focuses on the intersection of <b>embedded systems</b> 
            and <b>algorithmic efficiency</b>.
        </p>
        <p>
            Currently, I am deep-diving into Data Science architectures and Competitive Programming. 
            My goal is simple: Build scalable, intelligent solutions for real-world hardware.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_about_anim:
    # Using the fixed Neon Function
    st_lottie_neon(lottie_about, height=300, key="about")

# --- 3. PROJECTS (2x2 Grid) ---
st.write(" ")
st.markdown("<h2 style='margin-bottom: 30px;'><span class='neon-cyan'>//</span> DEPLOYED_PROJECTS</h2>", unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2, gap="medium")
row2_col1, row2_col2 = st.columns(2, gap="medium")

# --- ROW 1 ---
with row1_col1:
    st.markdown("""
    <div class='neon-card'>
        <h3 style='color: white; font-size: 1.6rem;'>🛡️ AIthentic: Deepfake Detector</h3>
        <p style='font-size: 1rem;'>
            High-precision detection system utilizing <b>EfficientNet-B3</b> and <b>Bi-LSTMs</b>. 
            Features "Active Sampling" to analyze high-motion frames, achieving <b>96.7% accuracy</b>.
        </p>
        <div style="margin-top:15px;">
            <span class='tech-badge'>DEEP LEARNING</span>
            <span class='tech-badge'>COMPUTER VISION</span>
            <span class='tech-badge'>PYTHON</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("""
    <div class='neon-card'>
        <h3 style='color: white; font-size: 1.6rem;'>🤖 Self-Balancing Bot</h3>
        <p style='font-size: 1rem;'>
            Autonomous stabilization using <b>ESP32 & MPU6050</b>. 
            Implemented custom PID algorithms for millisecond-level reaction times to maintain equilibrium.
        </p>
        <div style="margin-top:15px;">
            <span class='tech-badge'>C++</span>
            <span class='tech-badge'>ROBOTICS</span>
            <span class='tech-badge'>EMBEDDED</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ROW 2 ---
with row2_col1:
    st.markdown("""
    <div class='neon-card'>
        <h3 style='color: white; font-size: 1.6rem;'>📡 IoT Telemetry</h3>
        <p style='font-size: 1rem;'>
            Smart distance monitoring system with real-time web visualization.
            Features <b>WebSockets</b> for zero-latency data streaming via Chart.js dashboards.
        </p>
        <div style="margin-top:15px;">
            <span class='tech-badge'>IoT</span>
            <span class='tech-badge'>ESP32</span>
            <span class='tech-badge'>WEBSOCKETS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown("""
    <div class='neon-card'>
        <h3 style='color: white; font-size: 1.6rem;'>🔍 Fuzzy Logic Search</h3>
        <p style='font-size: 1rem;'>
            High-efficiency search engine using <b>Levenshtein Distance</b>. 
            Maps and ranks approximate string matches across large datasets instantly.
        </p>
        <div style="margin-top:15px;">
            <span class='tech-badge'>NLP</span>
            <span class='tech-badge'>PYTHON</span>
            <span class='tech-badge'>ALGORITHMS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. TERMINAL CHATBOT ---
st.write(" ")
st.markdown("---")

c_col1, c_col2 = st.columns([1.5, 1])

with c_col1:
    st.markdown("<h3 class='neon-purple'>INTERACTIVE_TERMINAL</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #888;'>Run a query on the Sahil_Desai database:</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("", placeholder="root@sahil:~$ ask_about_projects --verbose")

    if user_input and model:
        with st.spinner("Processing request..."):
            prompt = f"""
            You are a CLI portfolio assistant for Sahil Desai. 
            Style: Technical, Concise, Professional.
            Context: VJTI Student, 98% JEE, 8.22 CGPA, IoT/ML Developer.
            Query: {user_input}
            """
            try:
                response = model.generate_content(prompt)
                st.markdown(f"""
                <div style='background: #0d0d0d; border-left: 2px solid #00f3ff; padding: 20px; border-radius: 4px; font-family: JetBrains Mono; margin-top: 10px;'>
                    <div style='color: #00f3ff; font-size: 0.8rem; margin-bottom: 5px;'>➜ OUTPUT:</div>
                    <div style='color: #ccc; font-size: 1rem;'>{response.text}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.error("API Connection Failed.")

with c_col2:
    # Using the fixed Neon Function
    st_lottie_neon(lottie_chat, height=250, key="chat")

# --- FOOTER ---
st.markdown("""
    <div style='text-align: center; margin-top: 80px; color: #444; font-family: JetBrains Mono; font-size: 0.8rem;'>
        // SYSTEM_STATUS: ONLINE | © 2024 SAHIL DESAI
    </div>
""", unsafe_allow_html=True)
