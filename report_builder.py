"""
Report Builder Module
Generates HTML reports for roofing analysis
"""


class ReportBuilder:
    """Builds comprehensive HTML reports for roofing analysis"""
    
    def generate_html(self, scenario_data, structure_results, total_cost, 
                      squares, property_value, solar_roi, damage_assessment, 
                      image_base64=None):
        """
        Generate a comprehensive HTML report
        
        Args:
            scenario_data (dict): Scenario configuration data
            structure_results (list): List of structure analysis results
            total_cost (float): Total estimated cost
            squares (float): Number of roofing squares
            property_value (dict): Property value increase estimates
            solar_roi (dict): Solar ROI calculations
            damage_assessment (dict): Damage assessment results
            image_base64 (str): Base64-encoded satellite image (optional)
        
        Returns:
            str: Complete HTML report
        """
        address = scenario_data.get('address', 'N/A')
        lat = scenario_data.get('lat', 0)
        lon = scenario_data.get('lon', 0)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roofing Analysis Report - {address}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2563eb;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
        }}
        .section {{
            background-color: white;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #1e293b;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .image-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .image-container img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏘️ Roofing Analysis Report</h1>
        <p>{address}</p>
    </div>
    
    <div class="section">
        <h2>Property Information</h2>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Coordinates:</strong> {lat}, {lon}</p>
        <p><strong>Total Squares:</strong> {squares:.2f}</p>
    </div>
    
    <div class="section">
        <h2>Cost Breakdown</h2>
        <div class="metric">
            <div class="metric-label">Total Estimate</div>
            <div class="metric-value">${total_cost:,.2f}</div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Structure</th>
                    <th>Removal Cost</th>
                    <th>Material Cost</th>
                    <th>Labor Cost</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add structure details
        for result in structure_results:
            name = result.get('name', 'Structure')
            estimates = result.get('estimates', {})
            html += f"""
                <tr>
                    <td>{name}</td>
                    <td>${estimates.get('removal_cost', 0):,.2f}</td>
                    <td>${estimates.get('material_cost', 0):,.2f}</td>
                    <td>${estimates.get('labor_cost', 0):,.2f}</td>
                    <td>${estimates.get('total_cost', 0):,.2f}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>Condition Assessment</h2>
"""
        html += f"""
        <p><strong>Status:</strong> {damage_assessment.get('category', 'N/A')}</p>
        <p><strong>Severity Factor:</strong> {damage_assessment.get('severity_factor', 1.0)}x</p>
    </div>
    
    <div class="section">
        <h2>ROI Analysis</h2>
        <div class="metric">
            <div class="metric-label">Property Value Increase</div>
            <div class="metric-value">${property_value.get('low_estimate', 0):,.0f} - ${property_value.get('high_estimate', 0):,.0f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">10-Year Solar Savings</div>
            <div class="metric-value">${solar_roi.get('ten_year_savings', 0):,.2f}</div>
        </div>
    </div>
"""
        
        # Add satellite image if available
        if image_base64:
            html += f"""
    <div class="section">
        <h2>Satellite View</h2>
        <div class="image-container">
            <img src="data:image/png;base64,{image_base64}" alt="Satellite View">
        </div>
    </div>
"""
        
        html += """
    <div class="section">
        <p style="text-align: center; color: #666; font-size: 12px;">
            Generated by Roofing AI Sales Tool
        </p>
    </div>
</body>
</html>
"""
        
        return html
