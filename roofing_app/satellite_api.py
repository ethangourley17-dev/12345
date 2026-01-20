import requests
import base64
import os

def fetch_google_static_map(lat, lon, api_key=None, zoom=20, size="600x400", maptype="satellite"):
    """
    Fetches a satellite image from Google Static Maps API.
    Prioritizes passed api_key, falls back to env var.
    """
    if not api_key:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_MAPS_API_KEY not found in env and no key provided.")
            return None

    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": size,
        "maptype": maptype,
        "key": api_key
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        else:
            print(f"Error fetching Google image: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception fetching Google image: {e}")
        return None

def analyze_resolution(gsd_meters):
    """
    Analyzes if the Ground Sample Distance (GSD) is sufficient for roof reporting.
    """
    THRESHOLD_METERS = 0.5  # Sub-meter required
    if gsd_meters <= THRESHOLD_METERS:
        return True, "Sufficient resolution for detailed analysis."
    else:
        return False, f"Insufficient resolution ({gsd_meters}m). > {THRESHOLD_METERS}m required."
