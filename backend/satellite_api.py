import requests
import base64
import os

# Placeholder for userdata
# from google.colab import userdata

def fetch_google_static_map(lat, lon, api_key=None, zoom=20, size="600x400", maptype="satellite"):
    """
    Fetches a satellite image from Google Static Maps API.
    Prioritizes passed api_key, falls back to env var.
    """
    if not api_key:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_MAPS_API_KEY not found in environment and no key provided.")
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

def fetch_stac_imagery(lat, lon, cloud_cover_limit=20):
    """
    Fetches metadata for the most recent Sentinel-2 image from Earth Search STAC API.
    Returns a dictionary with basic info or None.
    """
    # Note: pystac_client would need to be installed.
    # For now, we will just print a warning if it fails to import or mock it if needed.
    try:
        import pystac_client
    except ImportError:
        print("pystac_client not installed. Skipping STAC imagery fetch.")
        return None

    STAC_URL = "https://earth-search.aws.element84.com/v1"
    COLLECTION = "sentinel-2-l2a"
    point = {"type": "Point", "coordinates": [lon, lat]}

    try:
        catalog = pystac_client.Client.open(STAC_URL)
        search = catalog.search(
            intersects=point,
            collections=[COLLECTION],
            query={"eo:cloud_cover": {"lt": cloud_cover_limit}},
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
            max_items=1
        )
        items = list(search.items())
        if items:
            item = items[0]
            return {
                "date": item.datetime,
                "platform": item.properties.get("platform"),
                "cloud_cover": item.properties.get("eo:cloud_cover"),
                "id": item.id
            }
        else:
            print("No STAC items found.")
            return None
    except Exception as e:
        print(f"Exception fetching STAC imagery: {e}")
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
