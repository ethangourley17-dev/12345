"""
Satellite API Module
Provides functionality to fetch satellite imagery from Google Maps Static API
"""

import requests
import base64


def fetch_google_static_map(lat, lon, api_key, zoom=19, size="640x640", maptype="satellite"):
    """
    Fetch a satellite image from Google Maps Static API
    
    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
        api_key (str): Google Maps API key
        zoom (int): Zoom level (default: 19)
        size (str): Image size in format "widthxheight" (default: "640x640")
        maptype (str): Map type (default: "satellite")
    
    Returns:
        str: Base64-encoded image data, or None if request fails
    """
    # Check if API key is valid (not a placeholder)
    if not api_key or api_key.startswith("AIzaSyxxxx"):
        return None
    
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": size,
        "maptype": maptype,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            # Encode the image data as base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
        else:
            return None
    except Exception as e:
        print(f"Error fetching satellite imagery: {e}")
        return None
