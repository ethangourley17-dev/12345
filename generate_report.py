import math
import os
# Import custom modules
import satellite_api
import solar_api
from sales_tools import CostEstimator, MaterialComparator, ROIAnalyzer, DamageAssessor
from measurement_engine import identify_structures
from report_builder import ReportBuilder

# 1. Define Custom Scenario Data
# In a real scenario, this comes from the database or user input
address = "51046 Range Road 224"
lat = 53.4357
lon = -113.2185
annual_sunlight_hours = 2200
solar_panel_capacity_kw = 10.5
damage_probability = 0.85

def main():
    print("Starting Modular Report Generation...")

    # 2. Fetch Satellite Image
    print(f"Fetching satellite image for {lat}, {lon}...")
    # We rely on userdata for the API key here, so we don't pass one explicitly
    image_base64 = satellite_api.fetch_google_static_map(lat, lon)

    if image_base64:
        print("Satellite image fetched successfully.")
    else:
        print("Satellite image could not be retrieved (using placeholder).")

    # Fetch Solar Data
    print(f"Fetching solar data for {lat}, {lon}...")
    solar_data = solar_api.fetch_solar_potential(lat, lon)
    
    current_annual_sunlight_hours = annual_sunlight_hours
    current_solar_panel_capacity_kw = solar_panel_capacity_kw

    if solar_data:
        print("Solar data fetched successfully.")
        try:
            current_annual_sunlight_hours = solar_data.get('solarPotential', {}).get('maxSunshineHoursPerYear', annual_sunlight_hours)
            current_solar_panel_capacity_kw = solar_data.get('solarPotential', {}).get('maxArrayPanelsCount', 20) * 0.4 # Assuming 400W panels
            print(f"Updated Solar Data: {current_annual_sunlight_hours} hours/yr, {current_solar_panel_capacity_kw} kW capacity")
        except Exception as e:
            print(f"Error parsing solar data: {e}")
    else:
        print("Solar data could not be retrieved (using defaults).")

    # 3. Measurement & Sales Logic
    estimator = CostEstimator()
    comparator = MaterialComparator()
    roi_analyzer = ROIAnalyzer()
    assessor = DamageAssessor()

    # Assess Damage
    damage_assessment = assessor.assess(damage_probability)
    print(f"Damage Assessment: {damage_assessment['category']} (Severity Factor: {damage_assessment['severity_factor']}x)")

    # Identify Structures (Mock Data from Engine)
    structures = identify_structures(lat, lon)

    structure_results = []
    grand_total_cost = 0.0
    grand_total_squares = 0.0

    for structure in structures:
        # Calculate pitch factor
        pitch_factor = 1.0 / math.cos(math.radians(structure['roof_pitch_degrees']))

        # Estimate Cost
        estimates = estimator.calculate_estimate(
            structure['roof_area_sqft'],
            pitch_factor=pitch_factor,
            removal_multiplier=damage_assessment['severity_factor']
        )

        # Material Comparison
        comparisons = comparator.compare(estimates['total_cost'])

        structure_results.append({
            "name": structure['name'],
            "estimates": estimates,
            "comparisons": comparisons
        })

        grand_total_cost += estimates['total_cost']
        grand_total_squares += estimates['squares']

    # ROI Analysis
    property_value = roi_analyzer.calculate_property_value_increase(grand_total_cost)
    solar_roi = roi_analyzer.calculate_solar_roi(
        current_annual_sunlight_hours,
        current_solar_panel_capacity_kw
    )

    # 4. Report Generation
    scenario_data = {
        "address": address,
        "annual_sunlight_hours": current_annual_sunlight_hours
    }

    builder = ReportBuilder()
    html_content = builder.generate_html(
        scenario_data,
        structure_results,
        grand_total_cost,
        grand_total_squares,
        property_value,
        solar_roi,
        damage_assessment,
        image_base64
    )

    output_filename = "51046_Range_Road_Report.html"
    with open(output_filename, "w") as f:
        f.write(html_content)

    print(f"Report generated successfully: {output_filename}")

if __name__ == "__main__":
    main()
