"""
Solar API Module
Provides functionality to fetch solar potential data from Google Solar API
"""

import requests


def fetch_solar_potential(lat, lon, api_key):
    """
    Fetch solar potential data for a given location from Google Solar API
    
    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        api_key (str): Google Maps API key
    
    Returns:
        dict: Solar potential data including sunlight hours and panel capacity,
              or None if request fails
    """
    # Check if API key is valid (not a placeholder)
    if not api_key or api_key.startswith("AIzaSyxxxx"):
        return None
    
    # Google Solar API endpoint
    base_url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"
    
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching solar data: {e}")
        return None
