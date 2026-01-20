import requests
import os

def fetch_solar_potential(lat, lon, api_key=None):
    """
    Fetches solar potential data from Google Solar API.
    Returns a dictionary with solar potential data or None.
    """
    if not api_key:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            print("Warning: API key not provided and GOOGLE_MAPS_API_KEY env var not set.")
            return None

    url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "requiredQuality": "HIGH",
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching Solar API data: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception fetching Solar API data: {e}")
        return None
