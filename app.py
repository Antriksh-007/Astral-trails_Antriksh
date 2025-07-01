import streamlit as st
import requests
import numpy as np

st.set_page_config(page_title="Radiation Risk Calculator", layout="centered")
st.title("Cosmic Radiation Risk Calculator")

# Inputs
mission_days = st.slider("Mission Duration (days)", 1, 1000, 180)
material = st.selectbox("Shielding Material", ["None", "Aluminum", "Polyethylene"])
thickness = st.slider("Shield Thickness (cm)", 0.0, 20.0, 0.0, 0.1)

# Fetch live proton flux
url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"
try:
    data = requests.get(url).json()
    flux = float(data[-1]['flux'])
    st.success(f"Live Proton Flux (≥10 MeV): {flux:.2e} p/cm²·s·sr")
except:
    flux = 100
    st.warning("Fetching live flux failed. Using default = 100 p/cm²·s·sr")

# Base dose model
base_dose_day = flux * 0.00005

# Attenuation factors
mu_values = {'Aluminum': 0.36, 'Polyethylene': 0.69}  # tuned to your data
if material != "None" and thickness > 0:
    transmitted = np.exp(-mu_values[material] * thickness)
else:
    transmitted = 1.0

daily_dose = base_dose_day * transmitted
total_dose = daily_dose * mission_days

risk_percent = total_dose / 1000 * 5

st.metric("☢️ Estimated Total Dose (mSv)", f"{total_dose:.2f}")
st.metric("⚠️ Estimated Cancer Risk", f"{risk_percent:.2f} %")
st.caption("Model uses Beer–Lambert attenuation and ICRP linear dose-risk; for illustrative purposes only.")
