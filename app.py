import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import io
import base64

# Import custom modules
import satellite_api
import solar_api
from measurement_engine import CostEstimator, MaterialComparator, ROIAnalyzer, DamageAssessor
from report_builder import ReportBuilder
from job_manager import JobManager

# --- Page Config ---
st.set_page_config(
    layout="wide",
    page_title="Roofing AI Sales Tool",
    page_icon="🏘️",
    initial_sidebar_state="expanded"
)

# --- Navigation ---
page = st.sidebar.radio("Navigation", ["Calculator", "Job Board"])

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 2px solid #2563eb;
    }
    h1, h2, h3 { color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    st.title("🏘️")
with col_head2:
    st.title("Roofing AI Sales Tool")
    st.markdown("**Intelligent Estimation & Financial Analysis Engine**")

if page == "Calculator":
    # --- Sidebar Input Panel ---
    st.sidebar.header("🏠 Property Config")

    with st.sidebar.expander("Location Details", expanded=True):
        address = st.text_input("Address", "51046 Range Road 224")
        lat = st.number_input("Latitude", value=53.4357, format="%.4f")
        lon = st.number_input("Longitude", value=-113.2185, format="%.4f")
        # IMPORTANT: Replace with your actual Google Maps API Key
        google_maps_api_key = st.text_input("Google Maps API Key", type="password")
        if not google_maps_api_key:
            google_maps_api_key = "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Fallback placeholder

    with st.sidebar.expander("Roof Measurements", expanded=True):
        roof_area_sqft = st.number_input("Total Area (sq ft)", value=3400, min_value=100, step=50)
        roof_pitch_degrees = st.number_input("Pitch (degrees)", value=20, min_value=0, max_value=90)

    with st.sidebar.expander("Condition & Energy", expanded=False):
        damage_probability = st.slider("AI Damage Probability", 0.0, 1.0, 0.85, 0.05)
        solar_panel_capacity_kw = st.number_input("Solar Potential (kW)", value=10.5, min_value=0.0, step=0.5)

    with st.sidebar:
        generate_btn = st.button("⚡ Run Analysis", type="primary", use_container_width=True)

    # --- Main Application Logic ---
    if generate_btn:

        # Initialize Engines
        assessor = DamageAssessor()
        estimator = CostEstimator()
        comparator = MaterialComparator()
        roi_analyzer = ROIAnalyzer()

        # Fetch Solar Data
        with st.spinner("Acquiring solar data..."):
            solar_data = solar_api.fetch_solar_potential(lat, lon, google_maps_api_key)
            
        current_annual_sunlight_hours = st.session_state.get('annual_sunlight_hours', 2200)
        current_solar_panel_capacity_kw = solar_panel_capacity_kw

        if solar_data:
            try:
                current_annual_sunlight_hours = solar_data.get('solarPotential', {}).get('maxSunshineHoursPerYear', 2200)
                current_solar_panel_capacity_kw = solar_data.get('solarPotential', {}).get('maxArrayPanelsCount', 20) * 0.4 # Assuming 400W panels
                st.success(f"Solar Data Fetched: {current_annual_sunlight_hours} hours/yr, {current_solar_panel_capacity_kw:.1f} kW potential")
            except Exception as e:
                st.warning(f"Error parsing solar data: {e}")
        else:
            st.warning("Could not fetch specific solar data. Using defaults.")

        # 1. Run Calculations
        pitch_factor = 1.0 / math.cos(math.radians(roof_pitch_degrees))
        damage_assessment = assessor.assess(damage_probability)

        estimates = estimator.calculate_estimate(
            roof_area_sqft,
            pitch_factor=pitch_factor,
            removal_multiplier=damage_assessment['severity_factor']
        )
        material_comparison = comparator.compare(estimates['total_cost'])
        property_value = roi_analyzer.calculate_property_value_increase(estimates['total_cost'])
        solar_roi = roi_analyzer.calculate_solar_roi(current_annual_sunlight_hours, current_solar_panel_capacity_kw)

        # 2. Tabs Layout
        tab1, tab2, tab3 = st.tabs(["📡 Satellite & Condition", "💰 Cost & Materials", "📈 ROI & Financials"])

        # --- TAB 1: Satellite & Condition ---
        with tab1:
            col_sat, col_cond = st.columns([3, 2])

            with col_sat:
                st.subheader("Satellite Imagery")
                with st.spinner("Acquiring satellite feed..."):
                    image_base64 = satellite_api.fetch_google_static_map(lat, lon, google_maps_api_key)
                    if image_base64:
                        st.image(base64.b64decode(image_base64), caption=f"Satellite View: {address}", use_column_width=True)
                    else:
                        st.warning("Satellite imagery unavailable (Check API Key)")
                        st.info("Displaying placeholder visualization.")

            with col_cond:
                st.subheader("AI Condition Assessment")

                status_color = "green"
                if damage_assessment['category'] == "Severe Damage": status_color = "red"
                elif damage_assessment['category'] == "Minor Damage": status_color = "orange"

                st.markdown(f"### Status: :{status_color}[{damage_assessment['category']}]")
                st.metric("Damage Probability", f"{damage_probability*100:.0f}%")
                st.metric("Severity Multiplier", f"{damage_assessment['severity_factor']}x")
                st.info("Higher severity increases removal and labor costs due to safety requirements.")

        # --- TAB 2: Cost & Materials ---
        with tab2:
            st.subheader("Detailed Cost Estimation")

            # Top Level Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Removal", f"${estimates['removal_cost']:,.2f}")
            m2.metric("Materials", f"${estimates['material_cost']:,.2f}")
            m3.metric("Labor", f"${estimates['labor_cost']:,.2f}")
            m4.metric("TOTAL ESTIMATE", f"${estimates['total_cost']:,.2f}", delta="Final Quote")

            st.divider()

            col_chart, col_table = st.columns([1, 1])

            with col_chart:
                st.markdown("**Cost Breakdown**")
                cost_data = pd.DataFrame({
                    'Category': ['Removal', 'Materials', 'Labor'],
                    'Cost': [estimates['removal_cost'], estimates['material_cost'], estimates['labor_cost']]
                })
                fig_cost, ax_cost = plt.subplots(figsize=(6, 4))
                # Use a modern color palette
                colors = ['#ef4444', '#3b82f6', '#10b981']
                ax_cost.pie(cost_data['Cost'], labels=cost_data['Category'], autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4))
                ax_cost.axis('equal')
                st.pyplot(fig_cost, use_container_width=True)

            with col_table:
                st.markdown("**Material Options (Upsell)**")
                mat_df = pd.DataFrame(material_comparison)
                # formatting for display
                mat_df['Estimated Cost'] = mat_df['estimated_cost'].apply(lambda x: f"${x:,.2f}")
                mat_df = mat_df[['material_name', 'Estimated Cost', 'lifespan_years', 'warranty_years']]
                mat_df.columns = ['Material', 'Cost', 'Lifespan (Yrs)', 'Warranty (Yrs)']
                st.dataframe(mat_df, hide_index=True, use_container_width=True)

        # --- TAB 3: ROI & Financials ---
        with tab3:
            st.subheader("Investment Analysis")

            roi1, roi2 = st.columns(2)
            with roi1:
                st.metric("Property Value Increase", f"${property_value['low_estimate']:,.0f} - ${property_value['high_estimate']:,.0f}")
                st.caption("Estimated increase in home resale value immediately after renovation.")

            with roi2:
                st.metric("10-Year Solar Savings", f"${solar_roi['ten_year_savings']:,.2f}")
                st.caption(f"Based on {current_solar_panel_capacity_kw:.1f}kW system and {current_annual_sunlight_hours} sunlight hours/yr.")

            st.divider()

            # ROI Chart
            roi_data = pd.DataFrame({
                'Metric': ['Value Increase (Low)', 'Value Increase (High)', 'Solar Savings (10yr)'],
                'Amount': [property_value['low_estimate'], property_value['high_estimate'], solar_roi['ten_year_savings']]
            })
            fig_roi, ax_roi = plt.subplots(figsize=(8, 3))
            ax_roi.barh(roi_data['Metric'], roi_data['Amount'], color=['#94a3b8', '#64748b', '#eab308'])
            ax_roi.set_xlabel('USD ($)')
            st.pyplot(fig_roi, use_container_width=True)

        # --- Download Report (Bottom) ---
        st.divider()

        # Prepare Data for Report Builder
        scenario_data_for_report = {
            "address": address,
            "lat": lat, "lon": lon, "api_key": google_maps_api_key,
            "structures": [{"name": "Main Structure", "roof_area_sqft": roof_area_sqft, "roof_pitch_degrees": roof_pitch_degrees}],
            "annual_sunlight_hours": current_annual_sunlight_hours,
            "solar_panel_capacity_kw": current_solar_panel_capacity_kw,
            "damage_probability": damage_probability
        }
        structure_results_for_report = [{"name": "Main Structure", "estimates": estimates, "comparisons": material_comparison}]

        report_builder = ReportBuilder()
        full_html_report = report_builder.generate_html(
            scenario_data_for_report,
            structure_results_for_report,
            estimates['total_cost'],
            estimates['squares'],
            property_value,
            solar_roi,
            damage_assessment,
            image_base64
        )

        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            st.download_button(
                label="📄 Download Professional PDF Report",
                data=full_html_report,
                file_name=f"Roofing_Report_{address.replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )
    else:
        st.info("👈 Please configure property details in the sidebar and click 'Run Analysis' to begin.")
