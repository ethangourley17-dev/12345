from datetime import datetime

class ReportBuilder:
    def generate_html(self, scenario_data, structure_results, grand_total_cost, grand_total_squares, property_value, solar_roi, damage_assessment, image_base64=None):
        """
        Generates the HTML report string based on the provided data, including damage assessment and material lists.
        """

        # Determine Status Color
        category = damage_assessment.get('category', 'Unknown')
        status_class = 'status-unknown'
        if category == 'Intact':
            status_class = 'status-intact'
        elif category == 'Minor Damage':
            status_class = 'status-minor'
        elif category == 'Severe Damage':
            status_class = 'status-severe'

        css = """
        <style>
            body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #1e293b; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: white; }
            .header { border-bottom: 4px solid #2563eb; padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
            .header h1 { color: #2563eb; margin: 0; font-size: 28px; }
            .header p { color: #64748b; margin: 0; font-size: 14px; }

            .title-section { background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; display: flex; align-items: center; gap: 20px; }
            .title-content { flex: 1; }
            .title-section h2 { margin: 0 0 10px 0; font-size: 32px; }
            .satellite-view { width: 300px; height: 200px; border-radius: 8px; border: 3px solid white; background-color: #cbd5e1; display: flex; align-items: center; justify-content: center; color: #1e293b; font-size: 0.8em; text-align: center; overflow: hidden; }
            .satellite-view img { width: 100%; height: 100%; object-fit: cover; }

            .section { margin-bottom: 50px; }
            .section h2 { border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; color: #1e293b; margin-bottom: 25px; font-size: 24px; }

            /* Damage Assessment Styles */
            .assessment-box { padding: 20px; border-radius: 8px; margin-bottom: 40px; border-left: 6px solid #ccc; background-color: #f8fafc; }
            .status-intact { border-left-color: #22c55e; background-color: #f0fdf4; }
            .status-minor { border-left-color: #f97316; background-color: #fff7ed; }
            .status-severe { border-left-color: #ef4444; background-color: #fef2f2; }
            .assessment-title { font-weight: bold; font-size: 1.2em; margin-bottom: 10px; color: #334155; }
            .assessment-detail { font-size: 1em; color: #475569; }

            .structure-block { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
            .structure-title { font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 15px; border-left: 4px solid #2563eb; padding-left: 10px; }

            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .box { background: white; padding: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
            .box h3 { color: #64748b; font-size: 0.75em; text-transform: uppercase; margin: 0 0 5px 0; }
            .box .value { font-size: 1.25em; font-weight: 700; color: #1e293b; }

            /* Material List Styles */
            .material-list-container { margin-top: 15px; padding-top: 15px; border-top: 1px dashed #cbd5e1; }
            .material-list-title { font-size: 0.85em; font-weight: bold; color: #64748b; text-transform: uppercase; margin-bottom: 8px; }
            .material-list ul { list-style-type: none; padding: 0; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
            .material-list li { font-size: 0.9em; color: #334155; background: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #e2e8f0; }
            .material-list strong { color: #1e293b; }

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
            <title>Report - {scenario_data['address']}</title>
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
                    <h2>{scenario_data['address']}</h2>
                    <p>Comprehensive Multi-Structure Estimate</p>
                </div>
                {img_html}
            </div>

            <!-- Roof Condition Assessment -->
            <div class="section">
                <h2>Roof Condition Assessment</h2>
                <div class="assessment-box {status_class}">
                    <div class="assessment-title">Condition: {category.upper()}</div>
                    <div class="assessment-detail">
                        Based on AI analysis of recent satellite imagery, this roof has been categorized as <strong>{category}</strong>.
                        <br><br>
                        <strong>Impact on Estimate:</strong> A removal cost multiplier of <strong>{damage_assessment.get('severity_factor', 1.0)}x</strong> has been applied to account for the increased labor and disposal requirements associated with this condition.
                    </div>
                </div>
            </div>

            <!-- Structures Breakdown -->
            <div class="section">
                <h2>Structure Breakdown</h2>
        """

        for res in structure_results:
            est = res['estimates']
            # Material List Logic
            mats = res.get('material_details', {})
            mat_items = ""
            if mats:
                for k, v in mats.items():
                    mat_items += f"<li><strong>{k}:</strong> {v}</li>"
            else:
                mat_items = "<li>No material data available.</li>"

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

                    <!-- Material List Section -->
                    <div class="material-list-container">
                        <div class="material-list-title">Calculated Material Requirements</div>
                        <div class="material-list">
                            <ul>
                                {mat_items}
                            </ul>
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
            scenario_data['annual_sunlight_hours']
        )

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

        return html_content
