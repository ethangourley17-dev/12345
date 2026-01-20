import os
import base64
import satellite_api
from google.cloud import storage

# Configuration
PROJECT_ID = 'your-project-id'  # Ideally fetched from env or main config in a real app
REGION = 'us-central1'
BUCKET_NAME = f"{PROJECT_ID}-roofing-data"

# Target Location: 51046 Range Road 224
LOCATION = {
    "lat": 53.4357,
    "lon": -113.2185,
    # Placeholder API Key
    "api_key": "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}

def ingest_satellite_data():
    print(f"Starting ingestion for location: {LOCATION['lat']}, {LOCATION['lon']}...")

    # 1. Fetch Image via Modular API
    image_base64 = satellite_api.fetch_google_static_map(
        LOCATION['lat'],
        LOCATION['lon'],
        LOCATION['api_key']
    )

    local_filename = "satellite_ingest_preview.png"

    if image_base64:
        # Save locally first
        with open(local_filename, "wb") as f:
            f.write(base64.b64decode(image_base64))
        print(f"\u2705 Image successfully fetched and saved locally to: {local_filename}")

        # 2. Upload to Cloud Storage (if Configured)
        if PROJECT_ID == 'your-project-id':
            print("\u26a0\ufe0f PROJECT_ID is a placeholder. Skipping Cloud Storage upload.")
        else:
            try:
                print(f"Attempting upload to gs://{BUCKET_NAME}...")
                storage_client = storage.Client(project=PROJECT_ID)
                bucket = storage_client.bucket(BUCKET_NAME)
                blob = bucket.blob(local_filename)
                blob.upload_from_filename(local_filename)
                print(f"\u2705 Uploaded to Cloud Storage: gs://{BUCKET_NAME}/{local_filename}")
            except Exception as e:
                print(f"\u274c Cloud Upload Failed: {e}")
    else:
        print("\u274c Failed to fetch satellite image via API.")

if __name__ == "__main__":
    ingest_satellite_data()