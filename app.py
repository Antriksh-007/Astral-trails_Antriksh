import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt # Import at the top for cleaner structure
import pandas as pd # Import at the top for cleaner structure

# App configuration
st.set_page_config(
    page_title="Cosmic Radiation Research Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Cosmic Radiation Research Dashboard")

# Intro section on homepage
st.markdown("""
Welcome to the **Cosmic Radiation Research Dashboard** — an interactive platform to explore real-time and simulated data on cosmic rays, their biological and technological effects, and mission safety.

---

**Select a feature tab below to begin your research:**
""")

# Main Feature Tabs
tabs = st.tabs([
    "Biological Effects Visualizer",
])

# Tab: Biological Effects Visualizer
with tabs[0]:
    st.subheader("Biological Effects of Radiation")

    # Add Age and Gender Inputs
    st.write("---") # Separator for new inputs
    st.subheader("Customize for Individual Factors")
    
    age = st.slider("Select Age (Years)", 0, 100, 30)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Prefer not to say"])

    st.write("---") # Separator for original content

    dose = st.slider("Select Radiation Dose (mSv)", 0, 10000, 200)

    # --- Calculate Age and Gender Risk Modifiers ---
    # These modifiers influence the effective dose or risk threshold based on general radiobiological understanding.
    # Base modifier: 1.0 (no change)
    age_modifier = 1.0
    gender_modifier = 1.0
    
    # Age-based modifier: Children are generally more radiosensitive
    if age < 10: # Very young children
        age_modifier = 1.4 # ~40% higher sensitivity
        st.warning("Note: Children under 10 are significantly more radiosensitive due to rapidly dividing cells and longer potential lifespan for cancer manifestation. The displayed effect considers this increased sensitivity. (Source: ICRP, UNSCEAR)")
    elif age < 20: # Adolescents
        age_modifier = 1.2 # ~20% higher sensitivity
        st.info("Note: Younger individuals (under 20) are generally more radiosensitive than adults. The displayed effect considers this increased sensitivity. (Source: ICRP, UNSCEAR)")
    elif age > 60: # Older adults might have some specific sensitivities/resiliencies depending on tissue
        age_modifier = 0.9 # Slightly less sensitive for long-term cancer risk, but acute effects still apply
        st.info("Note: For older adults, the long-term cancer risk from radiation may be slightly lower due to a shorter remaining lifespan. However, pre-existing health conditions can influence resilience to acute effects. (Source: General radiobiological principles)")

    # Gender-based modifier: Females generally have a slightly higher lifetime cancer risk from radiation.
    if gender == "Female":
        gender_modifier = 1.1 # ~10% higher sensitivity, primarily for cancer risk
        st.info("Note: Females generally have a slightly higher lifetime cancer risk from radiation exposure, particularly for breast and thyroid cancers. The displayed effect considers this increased sensitivity. (Source: ICRP, EPA)")
    elif gender == "Male":
        gender_modifier = 1.0 # Baseline
        st.info("Note: Males have a baseline sensitivity to radiation exposure. (Source: ICRP)")
    else: # "Prefer not to say" or any other value
        st.info("Individual biological responses to radiation can vary. Factors like age and gender can influence susceptibility, with younger individuals and females generally having slightly higher sensitivities to radiation-induced cancer risks. (Source: ICRP, WHO)")

    # Combine modifiers to get an "effective dose" for biological impact assessment
    adjusted_dose = dose * age_modifier * gender_modifier
    st.markdown(f"***Adjusted Biological Dose for your profile: {adjusted_dose:.2f} mSv*** (This adjusted dose reflects an individual's relative sensitivity to radiation for biological effects)")

    # Define effect stage and corresponding image path
    image_path = "" # Initialize image path
    if adjusted_dose < 100:
        effect = "No observable effects. Normal background exposure level."
        image_path = "images/human_body_healthy.png" # Path to healthy image
    elif adjusted_dose < 500:
        effect = "Minor biological impact. Slight increase in cancer risk."
        image_path = "images/human_body_minor_damage.png" # Path to minor damage image
    elif adjusted_dose < 1000:
        effect = "Possible nausea, vomiting. Risk of Acute Radiation Syndrome (ARS)."
        image_path = "images/human_body_moderate_damage.png" # Path to moderate damage image
    elif adjusted_dose < 3000:
        effect = "Severe ARS symptoms. Temporary sterility possible."
        image_path = "images/human_body_severe_damage.png" # Path to severe damage image
    elif adjusted_dose < 6000:
        effect = "Life-threatening dose. Intensive treatment required."
        image_path = "images/human_body_critical_damage.png" # Path to critical damage image
    else:
        effect = "Fatal in most cases. Survival unlikely without immediate medical care."
        image_path = "images/human_body_critical_damage.png" # Path to critical damage image (or a "fatal" specific one)

    st.info(f"Biological Effect at **{dose} mSv** (Adjusted for your profile): **{effect}**")

    # --- Human Body Diagram ---
    st.write("---")
    st.subheader("Visualizing Biological Impact")
    
    # Display the appropriate image based on the effect
    try:
        st.image(image_path, caption=f"Visualized Impact at {adjusted_dose:.0f} mSv (Adjusted)", use_column_width="auto")
        st.caption("Disclaimer: This diagram is a simplified, conceptual representation and not a medical diagnosis. Consult a medical professional for actual health concerns.")
    except FileNotFoundError:
        st.error(f"Image not found at '{image_path}'. Please ensure you have created the 'images' folder in your script directory and placed the required PNG files (e.g., human_body_healthy.png, human_body_minor_damage.png, etc.) inside it.")
    # --- END HUMAN BODY DIAGRAM ---


    # Plot: Dose vs Risk Severity
    st.subheader("Risk Severity Chart")

    doses = [0, 100, 500, 1000, 3000, 6000, 10000]
    risks = [0, 1, 2, 3, 4, 5, 6]
    labels = [
        "None", "Minor Risk", "Mild ARS", "Severe ARS", "Lethal Risk", "Extreme Lethal", "Fatal"
    ]

    fig, ax = plt.subplots()
    ax.plot(doses, risks, color='darkred', linewidth=3)
    ax.axvline(dose, color='blue', linestyle='--', label=f'Selected Dose: {dose} mSv')
    ax.axvline(adjusted_dose, color='red', linestyle=':', label=f'Adjusted Dose: {adjusted_dose:.0f} mSv')
    ax.set_xticks(doses)
    ax.set_xticklabels([str(d) for d in doses])
    ax.set_yticks(risks)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Dose (mSv)")
    ax.set_ylabel("Biological Risk")
    ax.set_title("Radiation Dose vs. Health Risk")
    ax.legend()
    st.pyplot(fig)

    # Table: Organ-specific susceptibility (simplified)
    st.subheader("Organ Susceptibility (Generalized)")

    df = pd.DataFrame({
        "Organ": ["Bone Marrow", "GI Tract", "Skin", "Brain", "Reproductive Organs"],
        "Effect at 1000 mSv+": [
            "Reduced blood cell count", "Nausea, diarrhea", "Burns, hair loss",
            "Cognitive impairment", "Sterility"
        ]
    })
    st.dataframe(df)

# Footer
st.markdown(f"""
---
<p style='text-align: center; color: gray'>
Built by Tanmay Rajput | Last updated: {datetime.today().strftime('%B %d, %Y')}
</p>
""", unsafe_allow_html=True)
