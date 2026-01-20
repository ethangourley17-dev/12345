import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import io
import base64

# Import custom modules
import satellite_api
import solar_api
from sales_tools import CostEstimator, MaterialComparator, ROIAnalyzer, DamageAssessor
from measurement_engine import identify_structures
from report_builder import ReportBuilder
from job_manager import JobManager
from analytics import AnalyticsEngine

# --- Page Config ---
st.set_page_config(
    layout="wide",
    page_title="Roofing AI Sales Tool",
    page_icon="\uD83C\uDFD8\uFE0F",
    initial_sidebar_state="expanded"
)

# --- Navigation ---
page = st.sidebar.radio("Navigation", ["Calculator", "Job Board", "Performance"])

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
    st.title("\uD83C\uDFD8\uFE0F")
with col_head2:
    st.title("Roofing AI Sales Tool")
    st.markdown("**Intelligent Estimation & Financial Analysis Engine**")

if page == "Calculator":
    # --- Sidebar Input Panel ---
    st.sidebar.header("\uD83C\uDFE0 Property Config")

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
        generate_btn = st.button("\u26A1 Run Analysis", type="primary", use_container_width=True)

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
        tab1, tab2, tab3 = st.tabs(["\uD83D\uDCE1 Satellite & Condition", "\uD83D\uDCB0 Cost & Materials", "\uD83D\uDCC8 ROI & Financials"])

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
                label="\uD83D\uDCC4 Download Professional PDF Report",
                data=full_html_report,
                file_name=f"Roofing_Report_{address.replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

            if st.button("Save to Job Board", use_container_width=True):
                job_mgr = JobManager()
                job_mgr.add_job(
                    customer_name="Customer @ " + address,
                    address=address,
                    value=estimates['total_cost']
                )
                st.success("Job saved to board!")

    elif not generate_btn:
        st.info("\uD83D\uDC48 Please configure property details in the sidebar and click 'Run Analysis' to begin.")

elif page == "Job Board":
    st.title("Job Tracking Dashboard")
    st.markdown("**Manage your pipeline**")

    job_mgr = JobManager()

    # Refresh logic (simple rerun workaround)
    if 'refresh_board' not in st.session_state:
        st.session_state.refresh_board = 0

    jobs = job_mgr.get_jobs()

    if jobs.empty:
        st.info("No jobs in the pipeline yet. Go to Calculator to create one.")
    else:
        # Kanban Columns
        cols = st.columns(5)
        stages = ["Lead", "Estimate Sent", "Signed", "In Progress", "Completed"]

        for i, stage in enumerate(stages):
            with cols[i]:
                st.subheader(stage)
                stage_jobs = jobs[jobs['status'] == stage]

                for _, job in stage_jobs.iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: white; padding: 10px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 10px; color: black;">
                            <strong>{job['customer_name']}</strong><br>
                            <span style="font-size: 0.8em; color: #555;">{job['address']}</span><br>
                            <strong style="color: #2563eb;">${job['value']:,.2f}</strong>
                        </div>
                        """, unsafe_allow_html=True)

                        # Move Actions
                        c1, c2 = st.columns(2)
                        with c1:
                            if i > 0:
                                if st.button("←", key=f"prev_{job['id']}"):
                                    job_mgr.update_job_status(job['id'], stages[i-1])
                                    st.rerun()
                        with c2:
                            if i < len(stages) - 1:
                                if st.button("→", key=f"next_{job['id']}"):
                                    job_mgr.update_job_status(job['id'], stages[i+1])
                                    st.rerun()

                        if st.button("🗑️", key=f"del_{job['id']}"):
                             job_mgr.delete_job(job['id'])
                             st.rerun()

elif page == "Performance":
    st.title("Performance Dashboard")
    st.markdown("**Real-time Business Analytics**")

    job_mgr = JobManager()
    df_jobs = job_mgr.get_jobs()

    analytics = AnalyticsEngine(df_jobs)
    kpis = analytics.get_kpis()

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Pipeline Value", f"${kpis['total_value']:,.2f}")
    k2.metric("Avg Job Value", f"${kpis['avg_value']:,.2f}")
    k3.metric("Total Jobs", f"{kpis['total_jobs']}")
    k4.metric("Conversion Rate (Signed+)", f"{kpis['conversion_rate']:.1f}%")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Pipeline Funnel")
        funnel_data = analytics.get_jobs_by_stage()
        if not funnel_data.empty:
            # Sort by custom order
            stage_order = ["Lead", "Estimate Sent", "Signed", "In Progress", "Completed"]
            # Filter out stages not in data to avoid errors if category missing
            funnel_data = funnel_data[funnel_data['status'].isin(stage_order)]
            funnel_data['status'] = pd.Categorical(funnel_data['status'], categories=stage_order, ordered=True)
            funnel_data = funnel_data.sort_values('status')

            fig, ax = plt.subplots()
            ax.bar(funnel_data['status'], funnel_data['count'], color='#3b82f6')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No data available")

    with c2:
        st.subheader("Revenue by Lead Source")
        source_data = analytics.get_revenue_by_source()
        if not source_data.empty:
            fig2, ax2 = plt.subplots()
            # Handle potential None values in lead_source
            source_data['lead_source'] = source_data['lead_source'].fillna('Unknown')
            ax2.pie(source_data['value'], labels=source_data['lead_source'], autopct='%1.1f%%', startangle=90)
            ax2.axis('equal')
            st.pyplot(fig2)
        else:
            st.info("No data available")

    st.subheader("Raw Data")
    st.dataframe(df_jobs)
