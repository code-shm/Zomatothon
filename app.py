import streamlit as st
import time
import random

# --- PAGE STYLING ---
st.set_page_config(page_title="Zomato KPT Engine v2.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stCodeBlock { background-color: #0a0c10 !important; border: 1px solid #3d414d; color: #00ff00 !important; }
    .metric-card { background-color: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #cb202d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM INPUTS ---
st.sidebar.title("📡 System Signals")
mri = st.sidebar.slider("Merchant Reliability Index (MRI)", 0.4, 1.0, 0.82)
area_load = st.sidebar.slider("Area-wide Order Density (Rush)", 1.0, 3.0, 1.5)
cuisine_complexity = st.sidebar.selectbox("Cuisine Complexity", ["Low (Snacks)", "Medium (Fast Food)", "High (Fine Dining)"], index=1)

# --- BACKEND LOGIC (The "Black Box") ---
def calculate_advanced_kpt(base, mri, load, complexity):
    # Mapping complexity to a multiplier
    c_map = {"Low (Snacks)": 0.8, "Medium (Fast Food)": 1.0, "High (Fine Dining)": 1.5}
    
    # Simulation of Hierarchical Smoothing (Page 7 of PDF)
    # We combine Cuisine Average + Specific Merchant Average
    historical_median = base * c_map[complexity]
    
    # P90 Tail Risk Adjustment (Exponential growth under high load)
    tail_risk_buffer = (load ** 2) * 1.2 
    
    # Final Formula: (Median + Rush Buffer) / Reliability
    prediction = (historical_median + tail_risk_buffer) / mri
    return round(prediction, 2)

base_val = 12.0
predicted_kpt = calculate_advanced_kpt(base_val, mri, area_load, cuisine_complexity)

# --- MAIN DASHBOARD ---
st.title("🚀 KPT Reconstruction Engine")
st.markdown("### Team Paradox: Operationalizing Ground Truth")

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-card"><h4>Predicted KPT</h4><h2>{predicted_kpt} min</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><h4>Reliability Score</h4><h2>{mri}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><h4>P90 Tail Risk</h4><h2>{round(area_load * 1.8, 1)}m</h2></div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("📟 Digital Handshake Live Feed")
terminal = st.empty()

def run_simulation():
    log_history = ""

    def log(msg, log_type="INFO", delay=0.01):
        nonlocal log_history
        prefix = f"[{time.strftime('%H:%M:%S')}] [{log_type}] "
        new_line = prefix + msg + "\n"
        for i in range(len(new_line) + 1):
            terminal.code(log_history + new_line[:i] + "▒", language="bash")
            time.sleep(delay)
        log_history += new_line
        terminal.code(log_history, language="bash")

    # --- 1. FEATURE EXTRACTION ---
    log("BACKEND: CALLING FEATURE STORE...", "DB")
    time.sleep(1)
    log(f"FETCHED: Historical_Median={base_val}m, Cuisine_Complexity={cuisine_complexity}")
    log(f"FETCHED: Area_Rush_Signal={area_load}x, MRI={mri}")
    
    # --- 2. INFERENCE RUN ---
    log("BACKEND: RUNNING GBDT (GRADIENT BOOSTING) MODEL...", "AI")
    time.sleep(1.5)
    log(f"RECALIBRATING: Applying tail-risk buffer for high load state (+{round(area_load**2, 1)}m)")
    log(f"FINAL INFERENCE: {predicted_kpt}m. Probability of On-Time Pickup: 94.2%", "AI")
    
    # --- 3. DISPATCH ---
    log("DISPATCHER: Calculating Rider Buffer...", "SYSTEM")
    # Dispatching rider so they arrive exactly when food is ready
    log(f"DISPATCHER: Order broadcast to Rider Partners at T + {round(predicted_kpt - 5, 1)}m", "SUCCESS")
    time.sleep(2)

    # --- 4. PHASE A HANDSHAKE ---
    log("PHASE A: ATTEMPTING HANDSHAKE (RIDER -> MERCHANT)", "INFO")
    time.sleep(1)
    log("HANDSHAKE: QR/NFC Verified. Ground Truth T1 established.", "SUCCESS")
    log("TELEMETRY: Start counting RIT (Rider Idle Time). Current bias: 0.0s")
    time.sleep(2)

    # --- 5. THE "FOR" BIAS ---
    log("SIGNAL RECEIVED: Merchant pushed 'Food Ready' button.", "WARN")
    log("VALIDATION: Physical pickup signal NOT detected. Potential FOR-Bias.", "AI")
    time.sleep(3)

    # --- 6. PHASE B HANDSHAKE ---
    log("PHASE B: ATTEMPTING HANDSHAKE (MERCHANT -> RIDER)", "INFO")
    actual_t2 = predicted_kpt + random.uniform(1, 4)
    time.sleep(1.5)
    log(f"HANDSHAKE: NFC Tag confirmed. Ground Truth T2 established at {round(actual_t2, 1)}m", "SUCCESS")

    # --- 7. THE FEEDBACK LOOP (Page 7) ---
    draw_error = round(actual_t2 - predicted_kpt, 2)
    bias_error = round(actual_t2 - (predicted_kpt - 1.5), 2)
    log("--------------------------------------------------")
    log(f"ERROR RECONCILIATION: ETA Variance = {draw_error} mins", "DB")
    log(f"BIAS RECONCILIATION: FOR Label Noise = {bias_error} mins", "DB")
    
    new_mri = round(mri - 0.05, 2) if bias_error > 2 else mri
    log(f"AI TRAINING: Recalibrating MRI for Merchant... {mri} -> {new_mri}", "AI")
    log("BACKEND: Ground truth synced to Production Feature Store.")
    st.balloons()

if st.button("▶ START BACKEND SIMULATION"):
    run_simulation()
