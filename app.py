import requests # Make sure requests is imported at the top of your script if not already
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

# Tab 3: Biological Effects
with tabs[0]:
    st.subheader("Biological Effects of Radiation")

    # --- NEW: Live Data Fetch for Ambient Radiation Environment ---
    st.write("---")
    st.subheader("Current Ambient Space Radiation Environment")
    
    url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"
    
    ambient_flux = 0 # Initialize with a default value
    try:
        data = requests.get(url, timeout=5).json() # Added a timeout for robustness
        # Assuming the last data point is the most recent
        if data and isinstance(data, list) and len(data) > 0 and 'flux' in data[-1]:
            ambient_flux = float(data[-1]['flux']) # protons/cm²/s/sr
            st.success(f"Live Proton Flux (≥10 MeV from GOES-Primary): **{ambient_flux:.2e} p/cm²/s/sr**")
            st.caption("Source: NOAA Space Weather Prediction Center (GOES satellite data)")
            
            # --- CONTEXTUAL INFORMATION based on ambient flux ---
            if ambient_flux > 1e3: # Example threshold for elevated flux
                st.warning("Note: The current ambient proton flux is elevated. Prolonged exposure in such an environment, particularly in space or high altitude, would contribute significantly to your accumulated radiation dose.")
            elif ambient_flux < 1e1: # Example threshold for low flux
                st.info("Note: The current ambient proton flux is low, indicating relatively calm space weather conditions.")
            else:
                st.info("Note: The current ambient proton flux is within typical background levels for space environment.")
        else:
            ambient_flux = 100 # Fallback if data is empty or malformed
            st.warning("Unable to parse live data. Using default ambient flux: 100 p/cm²/s/sr")

    except requests.exceptions.RequestException as e:
        ambient_flux = 100 # fallback if API fails due to network/server issues
        st.error(f"Error fetching live data: {e}") # Show specific error for debugging
        st.warning("Unable to fetch live data. Using default ambient flux: 100 p/cm²/s/sr")
    except Exception as e: # Catch any other unexpected errors during data processing
        ambient_flux = 100
        st.error(f"An unexpected error occurred during data processing: {e}")
        st.warning("Using default ambient flux: 100 p/cm²/s/sr")
        
    st.write("---") # Separator

    # --- END NEW LIVE DATA FETCH ---

    st.subheader("Customize for Individual Factors")
    
    age = st.slider("Select Age (Years)", 0, 100, 30)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Prefer not to say"])

    st.write("---") # Separator for original content

    dose = st.slider("Select Radiation Dose (mSv)", 0, 10000, 200)

    # --- Calculate Age and Gender Risk Modifiers ---
    age_modifier = 1.0
    gender_modifier = 1.0
    
    if age < 10:
        age_modifier = 1.4
        st.warning("Note: Children under 10 are significantly more radiosensitive due to rapidly dividing cells and longer potential lifespan for cancer manifestation. The displayed effect considers this increased sensitivity. (Source: ICRP, UNSCEAR)")
    elif age < 20:
        age_modifier = 1.2
        st.info("Note: Younger individuals (under 20) are generally more radiosensitive than adults. The displayed effect considers this increased sensitivity. (Source: ICRP, UNSCEAR)")
    elif age > 60:
        age_modifier = 0.9
        st.info("Note: For older adults, the long-term cancer risk from radiation may be slightly lower due to a shorter remaining lifespan. However, pre-existing health conditions can influence resilience to acute effects. (Source: General radiobiological principles)")

    if gender == "Female":
        gender_modifier = 1.1
        st.info("Note: Females generally have a slightly higher lifetime cancer risk from radiation exposure, particularly for breast and thyroid cancers. The displayed effect considers this increased sensitivity. (Source: ICRP, EPA)")
    elif gender == "Male":
        gender_modifier = 1.0
        st.info("Note: Males have a baseline sensitivity to radiation exposure. (Source: ICRP)")
    else:
        st.info("Individual biological responses to radiation can vary. Factors like age and gender can influence susceptibility, with younger individuals and females generally having slightly higher sensitivities to radiation-induced cancer risks. (Source: ICRP, WHO)")

    adjusted_dose = dose * age_modifier * gender_modifier
    st.markdown(f"***Adjusted Biological Dose for your profile: {adjusted_dose:.2f} mSv*** (This adjusted dose reflects an individual's relative sensitivity to radiation for biological effects)")

    # Define effect stage (MODIFIED to use adjusted_dose)
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

    # --- NEW: Human Body Diagram ---
    st.write("---")
    st.subheader("Visualizing Biological Impact")
    
    # Display the appropriate image based on the effect
    # Ensure the image path is correct and the images exist
    try:
        st.image(image_path, caption=f"Visualized Impact at {adjusted_dose:.0f} mSv (Adjusted)", use_column_width="auto")
        st.caption("Disclaimer: This diagram is a simplified, conceptual representation and not a medical diagnosis. Consult a medical professional for actual health concerns.")
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}. Please ensure images are in the 'images' folder.")
    # --- END NEW HUMAN BODY DIAGRAM ---


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
