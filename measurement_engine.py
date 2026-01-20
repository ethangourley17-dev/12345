"""
Measurement Engine Module
Provides classes for roofing cost estimation, material comparison, ROI analysis, and damage assessment
"""


class DamageAssessor:
    """Assesses roof damage based on probability"""
    
    def assess(self, damage_probability):
        """
        Assess damage level and return severity information
        
        Args:
            damage_probability (float): Damage probability (0.0 to 1.0)
        
        Returns:
            dict: Dictionary containing category and severity_factor
        """
        if damage_probability >= 0.7:
            category = "Severe Damage"
            severity_factor = 1.5
        elif damage_probability >= 0.4:
            category = "Minor Damage"
            severity_factor = 1.2
        else:
            category = "Good Condition"
            severity_factor = 1.0
        
        return {
            "category": category,
            "severity_factor": severity_factor
        }


class CostEstimator:
    """Estimates roofing costs based on area and various factors"""
    
    def __init__(self):
        # Cost per square foot
        self.removal_cost_per_sqft = 1.50
        self.material_cost_per_sqft = 3.50
        self.labor_cost_per_sqft = 2.00
    
    def calculate_estimate(self, roof_area_sqft, pitch_factor=1.0, removal_multiplier=1.0):
        """
        Calculate detailed cost estimate
        
        Args:
            roof_area_sqft (float): Total roof area in square feet
            pitch_factor (float): Multiplier for roof pitch (default: 1.0)
            removal_multiplier (float): Multiplier for removal difficulty (default: 1.0)
        
        Returns:
            dict: Dictionary containing cost breakdown
        """
        # Calculate effective area with pitch factor
        effective_area = roof_area_sqft * pitch_factor
        
        # Calculate individual costs
        removal_cost = effective_area * self.removal_cost_per_sqft * removal_multiplier
        material_cost = effective_area * self.material_cost_per_sqft
        labor_cost = effective_area * self.labor_cost_per_sqft * pitch_factor
        
        # Calculate total
        total_cost = removal_cost + material_cost + labor_cost
        
        # Calculate squares (100 sq ft = 1 square)
        squares = effective_area / 100
        
        return {
            "removal_cost": removal_cost,
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "total_cost": total_cost,
            "squares": squares
        }


class MaterialComparator:
    """Compares different roofing material options"""
    
    def __init__(self):
        self.materials = [
            {
                "material_name": "Asphalt Shingles",
                "cost_multiplier": 1.0,
                "lifespan_years": 20,
                "warranty_years": 15
            },
            {
                "material_name": "Metal Roofing",
                "cost_multiplier": 2.0,
                "lifespan_years": 50,
                "warranty_years": 30
            },
            {
                "material_name": "Composite Shingles",
                "cost_multiplier": 1.5,
                "lifespan_years": 30,
                "warranty_years": 25
            },
            {
                "material_name": "Clay Tiles",
                "cost_multiplier": 2.5,
                "lifespan_years": 50,
                "warranty_years": 50
            }
        ]
    
    def compare(self, base_cost):
        """
        Generate material comparison based on base cost
        
        Args:
            base_cost (float): Base estimated cost
        
        Returns:
            list: List of dictionaries with material options and costs
        """
        comparisons = []
        for material in self.materials:
            comparison = material.copy()
            comparison["estimated_cost"] = base_cost * material["cost_multiplier"]
            comparisons.append(comparison)
        
        return comparisons


class ROIAnalyzer:
    """Analyzes return on investment for roofing and solar improvements"""
    
    def calculate_property_value_increase(self, project_cost):
        """
        Calculate estimated property value increase from roof replacement
        
        Args:
            project_cost (float): Total project cost
        
        Returns:
            dict: Dictionary with low and high estimates
        """
        # Typical ROI for roof replacement is 60-70% of cost
        low_estimate = project_cost * 0.60
        high_estimate = project_cost * 0.70
        
        return {
            "low_estimate": low_estimate,
            "high_estimate": high_estimate
        }
    
    def calculate_solar_roi(self, annual_sunlight_hours, solar_capacity_kw):
        """
        Calculate solar ROI over 10 years
        
        Args:
            annual_sunlight_hours (float): Annual sunlight hours
            solar_capacity_kw (float): Solar panel capacity in kW
        
        Returns:
            dict: Dictionary with solar savings information
        """
        # Average electricity rate per kWh
        electricity_rate = 0.13  # $0.13 per kWh
        
        # Calculate annual energy production
        # Assuming 75% efficiency factor
        annual_energy_kwh = annual_sunlight_hours * solar_capacity_kw * 0.75
        
        # Calculate annual savings
        annual_savings = annual_energy_kwh * electricity_rate
        
        # Calculate 10-year savings
        ten_year_savings = annual_savings * 10
        
        return {
            "annual_savings": annual_savings,
            "ten_year_savings": ten_year_savings,
            "annual_energy_kwh": annual_energy_kwh
        }
