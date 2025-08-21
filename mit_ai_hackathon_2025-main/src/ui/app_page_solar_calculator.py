# app_page_solar_calculator.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def generate_ui(i):
    st.title("☀️ Solar Potential Explorer")
    st.markdown("Estimate your rooftop solar potential, cost, savings, and subsidy benefits.")

    # --- Layout ---
    col1, col2 = st.columns([1, 1.5])

    # -----------------------
    # Left Panel - User Inputs
    # -----------------------
    with col1:
        st.subheader("🔧 Input Parameters")

        # Pincode / Location Selector
        pincode = st.text_input("📍 Enter Pincode", "600001", key=f"pincode_{i}")

        # Rooftop Area
        rooftop_area = st.slider(
            "🏠 Rooftop Area (m²)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            key=f"area_{i}"
        )

        # Electricity consumption
        monthly_consumption = st.number_input(
            "💡 Monthly Electricity Consumption (kWh)",
            min_value=50,
            max_value=5000,
            value=500,
            key=f"consumption_{i}"
        )

        # Tariff
        tariff = st.number_input(
            "⚡ Electricity Tariff (₹/kWh)",
            min_value=2.0,
            max_value=15.0,
            value=6.0,
            step=0.1,
            key=f"tariff_{i}"
        )

        # Efficiency
        efficiency = st.selectbox(
            "☀️ Panel Efficiency (%)",
            [15, 18, 20, 22],
            index=1,
            key=f"efficiency_{i}"
        )

        # Financing option
        financing = st.radio(
            "🏦 Financing Option",
            ["Self", "Loan (Bank Financing)"],
            key=f"financing_{i}"
        )

        # Subsidy (State-wise %)
        states = {
            "Tamil Nadu": 40,
            "Karnataka": 35,
            "Kerala": 30,
            "Delhi": 40,
            "Maharashtra": 20,
            "Other": 20
        }
        state = st.selectbox("🌍 Select State", list(states.keys()), key=f"state_{i}")
        subsidy_percent = states[state]
        st.info(f"✅ MNRE/State Subsidy for {state}: **{subsidy_percent}%**")

        st.markdown("---")
        st.info(
            "📌 These values are demo estimates. "
            "Actual results depend on location, DISCOM, and MNRE/state policies."
        )

    # -----------------------
    # Right Panel - Results
    # -----------------------
    with col2:
        st.subheader("📊 Estimated Results")

        # Base Calculations
        system_capacity = round(rooftop_area * 0.15, 2)   # 0.15 kW per m² approx
        annual_generation = round(system_capacity * 1500) # kWh/year per kW
        gross_cost = round(system_capacity * 60000)       # ₹ 60,000 per kW approx
        subsidy_amount = round(gross_cost * (subsidy_percent / 100))
        net_cost = gross_cost - subsidy_amount
        monthly_savings = round(monthly_consumption * tariff * 0.6) # assume 60% offset
        payback_years = round(net_cost / (monthly_savings * 12), 1)

        # Display Cards
        colA, colB = st.columns(2)
        with colA:
            st.metric("⚡ System Capacity", f"{system_capacity} kW")
            st.metric("💰 Gross Cost", f"₹ {gross_cost:,}")
            st.metric("🏷️ Subsidy", f"₹ {subsidy_amount:,}")
        with colB:
            st.metric("🌞 Annual Generation", f"{annual_generation} kWh")
            st.metric("💳 Net Payable", f"₹ {net_cost:,}")
            st.metric("🔋 Payback Period", f"{payback_years} years")

        # Savings Chart
        months = np.arange(1, 13)
        savings = [monthly_savings for _ in months]
        df = pd.DataFrame({"Month": months, "Savings (₹)": savings})
        fig = px.bar(
            df,
            x="Month",
            y="Savings (₹)",
            title="Monthly Savings Estimate",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Financing Info
        if financing == "Loan (Bank Financing)":
            st.markdown("💡 **Loan Option Selected:** EMI calculator integration will be added here.")
