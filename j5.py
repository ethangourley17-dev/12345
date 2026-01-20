import json
import math
from datetime import datetime
from sales_tools import CostEstimator, MaterialComparator, ROIAnalyzer

# 1. Mock Data
mock_data = {
    "order_number": "RM-20260115-0001",
    "address": "718 Windjammer Rd, Bowen Island, BC V0N 1G2, Canada",
    "customer_name": "John Doe",
    "roof_area_sqft": 2500,
    "roof_pitch_degrees": 20,
    "annual_sunlight_hours": 2000,
    "roof_material": "Asphalt Shingle",
    "solar_panel_capacity_kw": 8.5
}

# 2. Calculations
# Pitch factor estimation: 1 / cos(radians(pitch))
pitch_factor = 1.0 / math.cos(math.radians(mock_data['roof_pitch_degrees']))

estimator = CostEstimator()
estimates = estimator.calculate_estimate(
    mock_data['roof_area_sqft'],
    pitch_factor=pitch_factor
)

comparator = MaterialComparator()
material_comparison = comparator.compare(estimates['total_cost'])

roi_analyzer = ROIAnalyzer()
property_value = roi_analyzer.calculate_property_value_increase(estimates['total_cost'])
solar_roi = roi_analyzer.calculate_solar_roi(
    mock_data['annual_sunlight_hours'],
    mock_data['solar_panel_capacity_kw']
)

# 3. HTML Generation
css = """
<style>
    body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #1e293b; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: white; }
    .header { border-bottom: 4px solid #2563eb; padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
    .header h1 { color: #2563eb; margin: 0; font-size: 28px; }
    .header p { color: #64748b; margin: 0; font-size: 14px; }

    .title-section { background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 40px; }
    .title-section h2 { margin: 0 0 10px 0; font-size: 32px; }
    .title-section p { margin: 0; opacity: 0.9; font-size: 16px; }

    .section { margin-bottom: 50px; }
    .section h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; color: #1e293b; margin-bottom: 25px; font-size: 24px; }
    .section p.desc { color: #64748b; margin-bottom: 20px; }

    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 25px; }
    .box { background: #f8fafc; padding: 25px; border-radius: 8px; border-left: 4px solid #2563eb; }
    .box h3 { color: #64748b; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 10px 0; }
    .box .value { font-size: 1.5em; font-weight: 700; color: #1e293b; }
    .box .sub-text { font-size: 0.9em; color: #64748b; margin-top: 5px; }

    table { width: 100%; border-collapse: collapse; margin-top: 15px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    th, td { text-align: left; padding: 15px; border-bottom: 1px solid #e2e8f0; }
    th { background-color: #f1f5f9; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }
    tr:last-child td { border-bottom: none; }
    tr:hover { background-color: #f8fafc; }

    .highlight { color: #16a34a; font-weight: bold; }
    .total-box { border-left-color: #16a34a; background-color: #f0fdf4; }
    .roi-box { border-left-color: #ca8a04; background-color: #fefce8; }

    .footer { text-align: center; margin-top: 60px; color: #94a3b8; font-size: 0.8em; border-top: 1px solid #e2e8f0; padding-top: 20px; }
</style>
"""

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Roof Report - {mock_data['order_number']}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {css}
</head>
<body>
    <div class="header">
        <div class="company-logo">
            <h1>Roof Measure AI</h1>
            <p>Advanced Roofing Intelligence</p>
        </div>
        <div class="report-meta">
            <p><strong>Order:</strong> {mock_data['order_number']}</p>
            <p>{datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </div>

    <div class="title-section">
        <h2>{mock_data['address']}</h2>
        <p>Comprehensive Sales & Measurement Report</p>
    </div>

    <!-- Standard Section: Property & Measurements -->
    <div class="section">
        <h2>Property & Measurement Details</h2>
        <div class="grid">
            <div class="box">
                <h3>Roof Area</h3>
                <div class="value">{mock_data['roof_area_sqft']:,} sq ft</div>
            </div>
            <div class="box">
                <h3>Pitch</h3>
                <div class="value">{mock_data['roof_pitch_degrees']}&deg;</div>
            </div>
            <div class="box">
                <h3>Current Material</h3>
                <div class="value">{mock_data['roof_material']}</div>
            </div>
             <div class="box">
                <h3>Solar Capacity</h3>
                <div class="value">{mock_data['solar_panel_capacity_kw']} kW</div>
            </div>
        </div>
    </div>

    <!-- New Section 1: Premium Cost Estimates -->
    <div class="section">
        <h2>Premium Cost Estimates</h2>
        <p class="desc">Estimated total cost for roof replacement based on current measurements and market rates.</p>
        <div class="grid">
            <div class="box">
                <h3>Removal Cost</h3>
                <div class="value">${estimates['removal_cost']:,}</div>
            </div>
             <div class="box">
                <h3>Material Cost</h3>
                <div class="value">${estimates['material_cost']:,}</div>
            </div>
             <div class="box">
                <h3>Labor Cost</h3>
                <div class="value">${estimates['labor_cost']:,}</div>
            </div>
             <div class="box total-box">
                <h3>TOTAL ESTIMATE</h3>
                <div class="value highlight">${estimates['total_cost']:,}</div>
                <div class="sub-text">{estimates['squares']} Squares</div>
            </div>
        </div>
    </div>

    <!-- New Section 2: Material Upgrade Options -->
    <div class="section">
        <h2>Material Upgrade Options</h2>
        <p class="desc">Compare long-term value across different roofing materials.</p>
        <table>
            <thead>
                <tr>
                    <th>Material</th>
                    <th>Estimated Cost</th>
                    <th>Lifespan</th>
                    <th>Warranty</th>
                    <th>Wind Rating</th>
                </tr>
            </thead>
            <tbody>
"""

for item in material_comparison:
    html_content += f"""
                <tr>
                    <td><strong>{item['material_name']}</strong></td>
                    <td>${item['estimated_cost']:,}</td>
                    <td>{item['lifespan_years']} Years</td>
                    <td>{item['warranty_years']} Years</td>
                    <td>{item['wind_rating_mph']} MPH</td>
                </tr>
    """

html_content += f"""
            </tbody>
        </table>
    </div>

    <!-- New Section 3: Investment Analysis -->
    <div class="section">
        <h2>Investment Analysis</h2>
        <p class="desc">Financial benefits and ROI projections for your property.</p>
        <div class="grid">
            <div class="box">
                <h3>Property Value Increase (Est.)</h3>
                <div class="value">${property_value['low_estimate']:,} - ${property_value['high_estimate']:,}</div>
                <div class="sub-text">Approx. 60-70% of project cost</div>
            </div>
            <div class="box roi-box">
                <h3>Solar ROI (10-Year Savings)</h3>
                <div class="value">${solar_roi['ten_year_savings']:,}</div>
                <div class="sub-text">Based on {mock_data['annual_sunlight_hours']} annual sunlight hours</div>
            </div>
        </div>
    </div>

    <div class="footer">
        Generated by Roof Measure AI Prototype | Confidential
    </div>
</body>
</html>
"""

output_file = "best_ever_roof_report.html"
with open(output_file, "w") as f:
    f.write(html_content)

print(f"Report successfully generated: {output_file}")
