import json
import math
import requests
import base64
from datetime import datetime
from sales_tools import CostEstimator, MaterialComparator, ROIAnalyzer

# Function to fetch Google Static Maps satellite image
def fetch_google_static_map(lat, lon, api_key):
    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{lat},{lon}",
        "zoom": 20,
        "size": "600x400",
        "maptype": "satellite",
        "key": api_key
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Return base64 encoded string of the image
            return base64.b64encode(response.content).decode('utf-8')
        else:
            print(f"Error fetching image: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception fetching image: {e}")
        return None

# 1. Define Custom Scenario Data
custom_scenario = {
    "address": "51046 Range Road 224",
    "lat": 53.4357,
    "lon": -113.2185,
    # Using the placeholder key found in the config files
    "api_key": "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "structures": [
        {
            "name": "Main House",
            "roof_area_sqft": 2800,
            "roof_pitch_degrees": 30
        },
        {
            "name": "Detached Garage",
            "roof_area_sqft": 600,
            "roof_pitch_degrees": 15
        }
    ],
    "annual_sunlight_hours": 2200,
    "solar_panel_capacity_kw": 10.5
}

# Fetch Image
print(f"Fetching satellite image for {custom_scenario['lat']}, {custom_scenario['lon']} using Google Maps API...")
image_base64 = fetch_google_static_map(
    custom_scenario['lat'],
    custom_scenario['lon'],
    custom_scenario['api_key']
)

if image_base64:
    print("Satellite image fetched successfully.")
else:
    print("Satellite image could not be retrieved.")

# 2. Logic & Calculations
estimator = CostEstimator()
comparator = MaterialComparator()
roi_analyzer = ROIAnalyzer()

structure_results = []
grand_total_cost = 0.0
grand_total_squares = 0.0

for structure in custom_scenario['structures']:
    # Calculate pitch factor: 1 / cos(radians(pitch))
    pitch_factor = 1.0 / math.cos(math.radians(structure['roof_pitch_degrees']))

    # Estimate Cost
    estimates = estimator.calculate_estimate(
        structure['roof_area_sqft'],
        pitch_factor=pitch_factor
    )

    # Material Comparison (for this structure's cost)
    comparisons = comparator.compare(estimates['total_cost'])

    structure_results.append({
        "name": structure['name'],
        "estimates": estimates,
        "comparisons": comparisons
    })

    grand_total_cost += estimates['total_cost']
    grand_total_squares += estimates['squares']

# ROI Analysis on Grand Total
property_value = roi_analyzer.calculate_property_value_increase(grand_total_cost)
solar_roi = roi_analyzer.calculate_solar_roi(
    custom_scenario['annual_sunlight_hours'],
    custom_scenario['solar_panel_capacity_kw']
)

# 3. HTML Generation
css = """
<style>
    body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #1e293b; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: white; }
    .header { border-bottom: 4px solid #2563eb; padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
    .header h1 { color: #2563eb; margin: 0; font-size: 28px; }
    .header p { color: #64748b; margin: 0; font-size: 14px; }

    .title-section { background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 40px; display: flex; align-items: center; gap: 20px; }
    .title-content { flex: 1; }
    .title-section h2 { margin: 0 0 10px 0; font-size: 32px; }
    .satellite-view { width: 300px; height: 200px; border-radius: 8px; border: 3px solid white; background-color: #cbd5e1; display: flex; align-items: center; justify-content: center; color: #1e293b; font-size: 0.8em; text-align: center; overflow: hidden; }
    .satellite-view img { width: 100%; height: 100%; object-fit: cover; }

    .section { margin-bottom: 50px; }
    .section h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; color: #1e293b; margin-bottom: 25px; font-size: 24px; }

    .structure-block { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
    .structure-title { font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 15px; border-left: 4px solid #2563eb; padding-left: 10px; }

    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
    .box { background: white; padding: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .box h3 { color: #64748b; font-size: 0.75em; text-transform: uppercase; margin: 0 0 5px 0; }
    .box .value { font-size: 1.25em; font-weight: 700; color: #1e293b; }

    .grand-total-box { background: #f0fdf4; border: 2px solid #16a34a; padding: 25px; border-radius: 12px; text-align: center; margin-top: 30px; }
    .grand-total-box h3 { color: #166534; margin: 0 0 10px 0; }
    .grand-total-box .value { font-size: 3em; font-weight: 800; color: #15803d; }

    .roi-section { display: flex; gap: 20px; margin-top: 30px; }
    .roi-card { flex: 1; background: #fffbeb; border: 1px solid #fcd34d; padding: 20px; border-radius: 8px; }

    table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9em; }
    th, td { text-align: left; padding: 8px; border-bottom: 1px solid #e2e8f0; }
    th { background-color: #f1f5f9; }
</style>
"""

# Prepare Image HTML
if image_base64:
    img_html = f'<div class="satellite-view"><img src="data:image/png;base64,{image_base64}" alt="Satellite View"></div>'
else:
    img_html = '<div class="satellite-view">Satellite imagery unavailable</div>'

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Report - {custom_scenario['address']}</title>
    {css}
</head>
<body>
    <div class="header">
        <div class="company-logo">
            <h1>Roof Measure AI</h1>
            <p>Multi-Structure Analysis</p>
        </div>
        <div class="report-meta">
            <p>{datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>

    <div class="title-section">
        <div class="title-content">
            <h2>{custom_scenario['address']}</h2>
            <p>Comprehensive Multi-Structure Estimate</p>
        </div>
        {img_html}
    </div>

    <!-- Structures Breakdown -->
    <div class="section">
        <h2>Structure Breakdown</h2>
"""

for res in structure_results:
    est = res['estimates']
    html_content += f"""
        <div class="structure-block">
            <div class="structure-title">{res['name']}</div>
            <div class="grid">
                <div class="box">
                    <h3>Total Estimate</h3>
                    <div class="value">${est['total_cost']:,}</div>
                </div>
                <div class="box">
                    <h3>Size</h3>
                    <div class="value">{est['squares']} Squares</div>
                </div>
                <div class="box">
                    <h3>Removal</h3>
                    <div class="value">${est['removal_cost']:,}</div>
                </div>
                <div class="box">
                    <h3>Material</h3>
                    <div class="value">${est['material_cost']:,}</div>
                </div>
                <div class="box">
                    <h3>Labor</h3>
                    <div class="value">${est['labor_cost']:,}</div>
                </div>
            </div>
        </div>
    """

html_content += """
    </div>

    <!-- Grand Totals & ROI -->
    <div class="section">
        <h2>Project Summary & Investment Analysis</h2>

        <div class="grand-total-box">
            <h3>PROJECT GRAND TOTAL</h3>
            <div class="value">${:,.2f}</div>
            <p>Total Size: {:.2f} Squares</p>
        </div>

        <div class="roi-section">
            <div class="roi-card">
                <h3>Est. Property Value Increase</h3>
                <div class="value" style="font-size: 1.5em; font-weight: bold; color: #b45309;">
                    ${:,.2f} - ${:,.2f}
                </div>
                <p>60-70% of Project Cost</p>
            </div>
            <div class="roi-card">
                <h3>10-Year Solar Savings</h3>
                <div class="value" style="font-size: 1.5em; font-weight: bold; color: #b45309;">
                    ${:,.2f}
                </div>
                <p>Based on {} annual sunlight hours</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Material Options (Main House Reference)</h2>
        <table>
            <thead><tr><th>Material</th><th>Cost Multiplier Ref</th><th>Lifespan</th><th>Warranty</th></tr></thead>
            <tbody>
""".format(
    grand_total_cost,
    grand_total_squares,
    property_value['low_estimate'], property_value['high_estimate'],
    solar_roi['ten_year_savings'],
    custom_scenario['annual_sunlight_hours']
)

# Add material comparison table (using Main House or just generic reference)
# Using the first structure's comparison as reference
if structure_results:
    ref_comparisons = structure_results[0]['comparisons']
    for comp in ref_comparisons:
        html_content += f"""
                <tr>
                    <td>{comp['material_name']}</td>
                    <td>${comp['estimated_cost']:,} (Approx)</td>
                    <td>{comp['lifespan_years']} Years</td>
                    <td>{comp['warranty_years']} Years</td>
                </tr>
        """

html_content += """
            </tbody>
        </table>
        <p style="font-size: 0.8em; color: #64748b; margin-top: 10px;">*Material costs shown are approximate for the Main House only.</p>
    </div>

</body>
</html>
"""

output_filename = "51046_Range_Road_Report.html"
with open(output_filename, "w") as f:
    f.write(html_content)

print(f"Custom report generated: {output_filename}")
