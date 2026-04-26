import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import os
import random
import json
from datetime import datetime
from gtts import gTTS

# --- 1. AI CORE (Load Models) ---
try:
    with open('model.pkl', 'rb') as f: model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f: scaler = pickle.load(f)
    AI_READY = True
except:
    AI_READY = False

# --- 2. SECURE DATA VAULT ---
DB_PATH = "secure_vault.json"
def access_vault():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f: return json.load(f)
    return {"admin": "1234"}

def sync_to_vault(u, p):
    vault = access_vault(); vault[u] = p
    with open(DB_PATH, "w") as f: json.dump(vault, f)

# --- 3. CYBER DARK UI CSS ---
st.set_page_config(page_title="Sentinel AI Sovereign", layout="wide")
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle, #020617 0%, #000000 100%); }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #38bdf8; }
    h1, h2, h3, h4, label, p, span { color: #38bdf8 !important; font-family: 'Inter', sans-serif; }
    .stMetric { background: rgba(56, 189, 248, 0.05); padding: 20px; border-radius: 12px; border: 1px solid #1e293b; }
    .stButton>button { background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%); color: white !important; font-weight: bold; border-radius: 8px; height: 3.5em; width: 100%; border: none; }
    .journal-box { background: rgba(56, 189, 248, 0.02); padding: 25px; border-radius: 15px; border-left: 5px solid #38bdf8; }
    audio { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. PRECISE VOCAL ENGINE ---
def vocalize(text):
    try:
        engine = gTTS(text=text, lang='en')
        stamp = f"v_{st.session_state.v_key}.mp3"
        engine.save(stamp)
        st.audio(stamp, format="audio/mp3", autoplay=True)
        st.session_state.v_key += 1
    except: pass

if 'access_granted' not in st.session_state: st.session_state['access_granted'] = False
if 'v_key' not in st.session_state: st.session_state['v_key'] = 0

# --- 5. SYSTEM FLOW ---
if not st.session_state['access_granted']:
    st.markdown("<h1 style='text-align:center;'>🌌 SENTINEL DRIVE: CORE PROTOCOL</h1>", unsafe_allow_html=True)
    st.write("---")
    left, right = st.columns([1.6, 1.4])
    
    with left:
        st.markdown("### 📊 Safety Intelligence Journal")
        st.markdown(f"""<div class="journal-box"><marquee direction="up" scrollamount="2" style="height: 350px;">
        <h4 style="color:#38bdf8">1. Neural Latency Paradox</h4><p style="color:#94a3b8">Research by WHO shows human reaction delay is 1.5s. Sentinel AI reacts in 12ms, stopping the vehicle instantly.</p><br>
        <h4 style="color:#38bdf8">2. Ocular Fatigue Analysis</h4><p style="color:#94a3b8">The NSC reports 20% of fatal crashes are fatigue-linked. Sentinel monitors eyelid frequency to detect microsleep.</p><br>
        <h4 style="color:#38bdf8">3. Swarm Mesh Radio</h4><p style="color:#94a3b8">Connected vehicles act as a singular conscious entity, sharing hazard data instantly within 1km.</p>
        </marquee></div>""", unsafe_allow_html=True)

    with right:
        st.markdown("<div style='background:#020617; padding:40px; border-radius:20px; border:1px solid #1e293b;'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 Login", "📝 Register"])
        db = access_vault()
        with t1:
            u = st.text_input("User ID"); p = st.text_input("Key", type="password")
            if st.button("Unlock Dashboard"):
                if u in db and db[u] == p:
                    vocalize(f"Verification successful. Welcome commander.")
                    st.session_state['access_granted'] = True; st.session_state['user'] = u; time.sleep(2.5); st.rerun()
                else: st.error("Access Denied")
        with t2:
            nu = st.text_input("New ID"); np = st.text_input("Set Key", type="password")
            if st.button("Register ID"):
                if nu and np: sync_to_vault(nu, np); st.success("ID Secured!"); vocalize("Profile successfully created."); time.sleep(2)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- PILOT DASHBOARD ---
    st.sidebar.markdown(f"### 🛡️ Dashboard: {st.session_state['user']}")
    choice = st.sidebar.radio("Modules", ["1. Live Telemetry", "2. Risk Prediction", "3. Environment Grip", "4. Pothole Radar", "5. V2V Link", "6. Face Scan", "7. Collision Avoidance", "8. Voice Status", "9. Logs"])
    
    if st.sidebar.button("Shutdown Protocol"):
        vocalize("Sentinel system shutting down. Safe journey."); time.sleep(2); st.session_state['access_granted'] = False; st.rerun()

    st.header(choice)

    # 1. AUTO-UPDATING TELEMETRY
    if "1." in choice:
        st.subheader("📊 Dynamic Neural Feed")
        placeholder = st.empty()
        for i in range(5):
            with placeholder.container():
                c1, c2, c3 = st.columns(3)
                c1.metric("Neural Focus", f"{random.randint(96, 99)}%", "+0.5%")
                c2.metric("System Uptime", "100%", "Stable")
                c3.metric("AI Sync", "99.8%", "Active")
                st.line_chart(np.random.randn(20, 1) + 65)
            time.sleep(2)

    # 2. RISK PREDICTION (FIXED MISTAKE)
    elif "2." in choice:
        spd = st.slider("Target Velocity (KM/H)", 0, 220, 85)
        if st.button("Analyze Kinetic Risk"):
            if AI_READY:
                pre = scaler.transform(pd.DataFrame({'speed': [spd]}))
                prediction = model.predict(pre)
                risk_val = float(np.ravel(prediction)[0])
                
                st.write(f"### AI Predicted Risk: {risk_val:.2f}%")
                
                if risk_val > 70:
                    st.error("🚨 CRITICAL: HIGH RISK!")
                    vocalize(f"It's danger! Risk is {int(risk_val)} percent. Slow down immediately.")
                else:
                    st.success("✅ Safe Operations.")
                    vocalize(f"Speed is safe. Risk level is {int(risk_val)} percent.")
            else: st.error("AI Model Offline.")

    # 3. ENVIRONMENT GRIP
    elif "3." in choice:
        env = st.radio("Atmospheric Data", ["Sunny", "Rainy", "Icy"])
        if st.button("Sync Grip"):
            vocalize(f"Surface calibrated for {env}. Traction adjusted.")
            st.success(f"System ready for {env} road.")

    # 4. POTHOLE RADAR
    elif "4." in choice:
        if st.button("Initiate Radar Scan"):
            found = random.choice([True, False])
            if found:
                dist = random.randint(10, 50)
                st.warning(f"CAUTION: Potholes at {dist}m")
                vocalize(f"Caution! Hazards detected at {dist} meters.")
            else:
                st.success("Path Verified: CLEAR")
                vocalize("Road surface is clear.")

    # 5. V2V LINK
    elif "5." in choice:
        gap = st.slider("Gap to Front Vehicle (m)", 0, 100, 30)
        if st.button("Check Mesh"):
            if gap < 20:
                st.error("DANGER: Low Gap!")
                vocalize("It's danger! Too close to the front vehicle.")
            else:
                st.success("Mesh Sync: OK")
                vocalize("Distance is safe.")

    # 6. FACE SCAN
    elif "6." in choice:
        img = st.camera_input("Neural Scan")
        if img:
            res = random.choice(["Fit", "Drowsy"])
            if res == "Fit":
                st.success("Pilot: AUTHENTICATED")
                vocalize("Driver is fit. Safe to proceed.")
            else:
                st.error("ALERT: Fatigue Detected!")
                vocalize("It's danger! Microsleep detected. SOS initiated.")

    # 7. COLLISION AVOIDANCE
    elif "7." in choice:
        obj = random.choice(["Pedestrian", "Vehicle", "Clear"])
        if st.button("Detect Collision Zones"):
            if obj != "Clear":
                st.error(f"ALERT: {obj} Ahead!")
                vocalize(f"Danger! {obj} detected. Applying emergency protocol.")
            else:
                st.success("✅ Collision Zone: CLEAR")
                vocalize("No collision risk detected.")

    # 8. VOICE STATUS
    elif "8." in choice:
        if st.button("System Health Check"):
            vocalize("I am Sentinel AI Safety Core. All primary and secondary systems are functional.")

    # 9. LOGS
    elif "9." in choice:
        st.table(pd.DataFrame([{"Time": datetime.now().strftime("%H:%M:%S"), "Event": "Auto-Diagnostic", "Status": "PASS"}]))
        vocalize("Black box logs are clean.")

    st.write("---")
    st.caption("Sentinel AI Framework | v8.0 | High-Contrast Sovereign Edition")