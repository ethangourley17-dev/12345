import math

class DamageAssessor:
    def assess(self, damage_probability):
        """
        Assess damage category and severity factor based on probability.
        """
        if damage_probability < 0.3:
            return {
                'category': 'Intact',
                'severity_factor': 1.0
            }
        elif damage_probability < 0.7:
            return {
                'category': 'Minor Damage',
                'severity_factor': 1.2
            }
        else:
            return {
                'category': 'Severe Damage',
                'severity_factor': 1.5
            }

class CostEstimator:
    def __init__(self, removal_price_per_sq=50.0, install_price_per_sq=350.0):
        """
        Initialize the CostEstimator with default pricing.
        :param removal_price_per_sq: Cost to remove old roof per square (100 sq ft).
        :param install_price_per_sq: Cost to install new roof per square (100 sq ft).
        """
        self.removal_price_per_sq = removal_price_per_sq
        self.install_price_per_sq = install_price_per_sq

    def calculate_estimate(self, area_sqft, pitch_factor=1.0, waste_percent=10.0, removal_multiplier=1.0):
        """
        Calculate the estimated cost of the roof replacement.
        Logic: Calculate actual area = area * pitch * (1 + waste/100). Convert to squares (area / 100). Apply rates.
        :param removal_multiplier: Multiplier for removal cost based on damage severity (default 1.0).
        """
        # Calculate actual area accounting for pitch and waste
        actual_area = area_sqft * pitch_factor * (1 + waste_percent / 100.0)
        squares = actual_area / 100.0

        # Calculate component costs with removal multiplier
        removal_cost = squares * self.removal_price_per_sq * removal_multiplier

        # Splitting install price into material and labor for detail (Assumption: 40% material, 60% labor)
        total_install_cost = squares * self.install_price_per_sq
        material_cost = total_install_cost * 0.40
        labor_cost = total_install_cost * 0.60

        total_cost = removal_cost + total_install_cost

        return {
            'removal_cost': round(removal_cost, 2),
            'material_cost': round(material_cost, 2),
            'labor_cost': round(labor_cost, 2),
            'total_cost': round(total_cost, 2),
            'squares': round(squares, 2)
        }

class MaterialComparator:
    def compare(self, base_cost):
        """
        Compare costs across different material types based on a base cost (e.g. Asphalt Shingle).
        """
        return [
            {
                'material_name': 'Asphalt Shingle',
                'estimated_cost': round(base_cost * 1.0, 2),
                'lifespan_years': 20,
                'warranty_years': 15,
                'wind_rating_mph': 110
            },
            {
                'material_name': 'Metal Seam',
                'estimated_cost': round(base_cost * 2.5, 2),
                'lifespan_years': 50,
                'warranty_years': 40,
                'wind_rating_mph': 140
            },
            {
                'material_name': 'Clay Tile',
                'estimated_cost': round(base_cost * 3.0, 2),
                'lifespan_years': 75,
                'warranty_years': 50,
                'wind_rating_mph': 150
            }
        ]

class ROIAnalyzer:
    def calculate_property_value_increase(self, total_project_cost):
        """
        Calculate estimated property value increase based on project cost.
        Return a low (60%) and high (70%) estimate.
        """
        return {
            'low_estimate': round(total_project_cost * 0.60, 2),
            'high_estimate': round(total_project_cost * 0.70, 2)
        }

    def calculate_solar_roi(self, annual_sunlight_hours, kw_capacity, energy_rate_per_kwh=0.15):
        """
        Calculate Solar ROI.
        :param annual_sunlight_hours: Total sunlight hours per year.
        :param kw_capacity: Solar system capacity in kW.
        :param energy_rate_per_kwh: Cost of energy per kWh.
        """
        annual_savings = annual_sunlight_hours * kw_capacity * energy_rate_per_kwh
        ten_year_savings = annual_savings * 10

        return {
            'annual_savings': round(annual_savings, 2),
            'ten_year_savings': round(ten_year_savings, 2)
        }