import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt  # Import at the top for cleaner structure
import pandas as pd  # Import at the top for cleaner structure
import os
from pathlib import Path
import plotly.graph_objects as go  # Moved to top-level

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
Welcome to the **Cosmic Radiation Research Dashboard** — an interactive platform to explore cumulative radiation exposure over time, factoring in individual sensitivity.

---

**Select a feature tab below to begin your research:**
""")

# Main Feature Tabs
tabs = st.tabs([
    "Biological Effects Visualizer",
])

# Tab: Biological Effects Visualizer
with tabs[0]:
    st.subheader("Biological Effects of Radiation over Time")

    # Separator
    st.write("---")
    st.subheader("Customize for Individual Factors and Duration")

    # Age and Gender Inputs
    age = st.slider("Select Age (Years)", 0, 100, 30)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Prefer not to say"])

    # Duration Input (days)
    days = st.slider("Select Duration (Days)", 0, 3650, 30)

        # Base daily cosmic radiation rate (mSv/day) — average cosmic component at sea level (~0.38 mSv/year ⇒ ~0.00104 mSv/day) based on UNSCEAR reports
    BASE_RATE = 0.00104  # Source: UNSCEAR 2020 report
