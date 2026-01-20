import pystac_client
import stackstac
import matplotlib.pyplot as plt
import numpy as np

# API Configuration
STAC_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"
# Coordinates for 51046 Range Road 224
LAT = 53.4357
LON = -113.2185
POINT = {"type": "Point", "coordinates": [LON, LAT]}

def fetch_and_display():
    print(f"Querying {STAC_URL} for coordinates ({LAT}, {LON})...")

    try:
        # 1. Connect to STAC API
        catalog = pystac_client.Client.open(STAC_URL)

        # 2. Search for recent, low-cloud images
        # Corrected argument: sortby instead of sort_by
        search = catalog.search(
            intersects=POINT,
            collections=[COLLECTION],
            query={"eo:cloud_cover": {"lt": 20}}, # Less than 20% cloud
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
            max_items=1
        )

        items = list(search.items())
        if not items:
            print("No images found satisfying criteria.")
            return

        item = items[0]
        print(f"Selected Image Date: {item.datetime}")
        print(f"Cloud Cover: {item.properties.get('eo:cloud_cover')}%")
        print(f"Platform: {item.properties.get('platform')}")

        # 3. Load Data using stackstac
        # Define a small bounding box (approx 2km buffer) to fetch minimal data
        buffer = 0.01
        bbox = [LON - buffer, LAT - buffer, LON + buffer, LAT + buffer]

        print("Fetching RGB bands (Red, Green, Blue)...")
        # stackstac handles lazy loading and projection
        # Fix: explicitly set epsg=4326 to resolve 'Cannot pick a common CRS' error
        stack = stackstac.stack(
            item,
            assets=["red", "green", "blue"],
            bounds=bbox,
            chunksize=1024,
            epsg=4326
        )

        # 4. Process for Display
        # Composite and fetch data (dask -> numpy)
        # stack is (time, band, y, x). Take time=0.
        rgb_data = stack.isel(time=0).compute()

        # Convert to numpy and transpose to (H, W, C) for matplotlib
        rgb_img = rgb_data.to_numpy().transpose(1, 2, 0)

        # Normalize (Sentinel-2 reflectance 0-10000 -> 0-1 for plotting)
        # Using 3000 as max for typical visualization brightness (0.3 reflectance)
        rgb_img = np.clip(rgb_img / 3000.0, 0, 1)

        # 5. Save Preview
        plt.figure(figsize=(10, 10))
        plt.imshow(rgb_img)
        plt.title(f"Sentinel-2 TCI (RGB) - {item.datetime.date()}\nLat: {LAT}, Lon: {LON}")
        plt.axis('off')
        output_file = "sentinel_preview.png"
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Preview saved to {output_file}")

        # 6. Summary
        print("\n--- RESOLUTION SUMMARY ---")
        print("Satellite: Sentinel-2")
        print("Spatial Resolution: 10 meters")
        print("Assessment: The 10m resolution is INSUFFICIENT for detailed roof reporting.")
        print("Reasoning: At 10m/pixel, a typical residential roof occupies only 1-4 pixels, making edge detection impossible.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fetch_and_display()
