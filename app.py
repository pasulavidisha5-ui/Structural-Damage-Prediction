import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Structural Damage and Risk Prediction System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("structural_damage_simple_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()

# ---------------- PROFESSIONAL DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f4f7fc;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

header, footer, #MainMenu {
    visibility: hidden;
}

.topbar {
    background: white;
    border: 1px solid #e5eaf2;
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: 23px;
    font-weight: 800;
    color: #17233c;
}

.brand span {
    color: #2563eb;
}

.brand-caption {
    font-size: 12px;
    color: #718096;
    margin-top: 4px;
}

.status {
    background: #ecfdf5;
    color: #047857;
    padding: 8px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.heading {
    color: #17233c;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subheading {
    color: #718096;
    font-size: 14px;
    margin-bottom: 24px;
}

.panel {
    background: white;
    border: 1px solid #e5eaf2;
    border-radius: 16px;
    padding: 24px;
    min-height: 540px;
    box-shadow: 0 4px 15px rgba(25, 45, 85, 0.035);
}

.panel-title {
    font-size: 19px;
    font-weight: 750;
    color: #17233c;
    margin-bottom: 5px;
}

.panel-caption {
    font-size: 12px;
    color: #718096;
    margin-bottom: 22px;
}

label {
    font-weight: 600 !important;
    color: #344054 !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] {
    border-radius: 9px;
}

.stButton > button {
    width: 100%;
    height: 47px;
    border-radius: 9px;
    background: #2563eb;
    color: white;
    border: none;
    font-weight: 700;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
}

.result {
    padding: 25px 15px;
    text-align: center;
    border-radius: 13px;
    margin: 15px 0;
}

.result-label {
    font-size: 11px;
    letter-spacing: 1.3px;
    font-weight: 700;
    margin-bottom: 9px;
}

.result-value {
    font-size: 27px;
    font-weight: 800;
}

.risk-box {
    background: #f8fafc;
    border: 1px solid #e5eaf2;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 18px;
}

.risk-label {
    color: #718096;
    font-size: 11px;
    font-weight: 700;
}

.risk-value {
    color: #17233c;
    font-size: 21px;
    font-weight: 800;
    margin-top: 5px;
}

.confidence-box {
    background: #eff6ff;
    border-radius: 12px;
    text-align: center;
    padding: 16px;
    margin-bottom: 22px;
}

.confidence-value {
    color: #2563eb;
    font-size: 28px;
    font-weight: 800;
}

.confidence-label {
    color: #64748b;
    font-size: 12px;
}

.probability-heading {
    font-size: 15px;
    font-weight: 750;
    color: #17233c;
    margin-bottom: 17px;
}

.probability-row {
    margin-bottom: 15px;
}

.probability-label {
    display: flex;
    justify-content: space-between;
    color: #475569;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.track {
    background: #e8edf5;
    height: 8px;
    border-radius: 20px;
    overflow: hidden;
}

.fill {
    background: #3b82f6;
    height: 8px;
    border-radius: 20px;
}

.empty-state {
    min-height: 420px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.empty-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.empty-title {
    color: #17233c;
    font-size: 20px;
    font-weight: 750;
}

.empty-caption {
    color: #718096;
    font-size: 13px;
    line-height: 1.7;
    margin-top: 8px;
}

@media (max-width: 768px) {
    .brand {
        font-size: 19px;
    }

    .panel {
        padding: 18px;
        min-height: auto;
    }

    .heading {
        font-size: 24px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- APP HEADER ----------------
st.markdown("""
<div class="topbar">
    <div>
        <div class="brand">🏗️ StructuralGuard <span>AI</span></div>
        <div class="brand-caption">Structural Damage Assessment</div>
    </div>
    <div class="status">● AI Ready</div>
</div>
<div class="heading">Building Assessment</div>
<div class="subheading">
    Enter building details to generate a structural damage prediction.
</div>
""", unsafe_allow_html=True)

# ---------------- TWO-COLUMN LAYOUT ----------------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">Building Information</div>
        <div class="panel-caption">Enter the available building details.</div>
    </div>
    """, unsafe_allow_html=True)

    age = st.number_input("Building Age (years)", 0, 200, 20)
    floors = st.number_input("Number of Floors", 1, 20, 2)
    families = st.number_input("Number of Families", 1, 50, 2)

    size = st.selectbox(
        "Building Size",
        ["Small", "Medium", "Large"]
    )

    height = st.selectbox(
        "Building Height",
        ["Low", "Medium", "High"]
    )

    material = st.selectbox(
        "Construction Material",
        [
            "Reinforced Concrete",
            "Concrete",
            "Cement Brick",
            "Cement Stone",
            "Mud Brick",
            "Mud Stone",
            "Stone",
            "Adobe/Mud",
            "Wood",
            "Bamboo",
            "Other"
        ]
    )

    usage = st.selectbox(
        "Building Usage",
        ["Residential", "Other"]
    )

    predict = st.button("ASSESS BUILDING", use_container_width=True)

# ---------------- AI ASSESSMENT ----------------
with right:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">AI Assessment</div>
        <div class="panel-caption">Structural damage prediction results</div>
    """, unsafe_allow_html=True)

    if predict:
        input_data = pd.DataFrame({
            "age": [age],
            "count_floors_pre_eq": [floors],
            "count_families": [families],
            "building_size": [size],
            "building_height": [height],
            "construction_material": [material],
            "building_usage": [usage]
        })

        try:
            prediction = int(model.predict(input_data)[0])
            probabilities = model.predict_proba(input_data)[0]
            probability_map = dict(zip(model.classes_, probabilities))

            labels = {
                1: "LOW DAMAGE",
                2: "MEDIUM DAMAGE",
                3: "HIGH DAMAGE"
            }

            damage = labels[prediction]
            confidence = probability_map[prediction] * 100

            low = probability_map.get(1, 0) * 100
            medium = probability_map.get(2, 0) * 100
            high = probability_map.get(3, 0) * 100

            if prediction == 3:
                risk = "HIGH RISK" if confidence >= 70 else "MEDIUM RISK"
                bg, border, color = "#fef2f2", "#fecaca", "#dc2626"
            elif prediction == 2:
                risk = "MEDIUM RISK"
                bg, border, color = "#fff7ed", "#fed7aa", "#c2410c"
            else:
                risk = "LOW RISK" if confidence >= 70 else "MEDIUM RISK"
                bg, border, color = "#f0fdf4", "#bbf7d0", "#15803d"

            st.markdown(f"""
            <div class="result"
                 style="background:{bg};border:1px solid {border};color:{color}">
                <div class="result-label">PREDICTED STRUCTURAL DAMAGE</div>
                <div class="result-value">{damage}</div>
            </div>
            <div class="risk-box">
                <div class="risk-label">INFRASTRUCTURE RISK</div>
                <div class="risk-value">{risk}</div>
            </div>
            <div class="confidence-box">
                <div class="confidence-value">{confidence:.1f}%</div>
                <div class="confidence-label">Prediction Confidence</div>
            </div>
            <div class="probability-heading">Damage Probability</div>
            """, unsafe_allow_html=True)

            for name, value in [
                ("Low", low),
                ("Medium", medium),
                ("High", high)
            ]:
                st.markdown(f"""
                <div class="probability-row">
                    <div class="probability-label">
                        <span>{name} Damage</span>
                        <span>{value:.1f}%</span>
                    </div>
                    <div class="track">
                        <div class="fill" style="width:{value}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction failed: {e}")

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🏢</div>
            <div class="empty-title">Ready for Assessment</div>
            <div class="empty-caption">
                Fill in the building details on the left<br>
                and select Assess Building.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)