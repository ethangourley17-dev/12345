from google.cloud import aiplatform
import time

# Configuration
# NOTE: Ensure PROJECT_ID is set correctly in your environment or replace here
PROJECT_ID = 'your-project-id'
REGION = 'us-central1'
DISPLAY_NAME = 'roof-damage-classifier'

# Pre-built container for TensorFlow 2.x
TRAIN_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12:latest'
SERVE_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest'

def launch_job():
    if PROJECT_ID == 'your-project-id':
        print("\u26a0\ufe0f Please update the PROJECT_ID in the script before running.")
        return

    print(f"Initializing Vertex AI for project {PROJECT_ID}...")
    aiplatform.init(project=PROJECT_ID, location=REGION)

    print("Submitting Custom Training Job...")
    job = aiplatform.CustomTrainingJob(
        display_name=DISPLAY_NAME,
        script_path='roof_model.py',
        container_uri=TRAIN_IMAGE_URI,
        model_serving_container_image_uri=SERVE_IMAGE_URI,
    )

    print("Starting Model Training (this may take a few minutes)...")
    model = job.run(
        model_display_name=f"{DISPLAY_NAME}-model",
        replica_count=1,
        machine_type='n1-standard-4',
    )
    print("\u2705 Training Complete.")

    print("Deploying Model to Endpoint...")
    endpoint = model.deploy(
        machine_type='n1-standard-2',
        min_replica_count=1,
        max_replica_count=1
    )

    print(f"\u2705 Model Deployed!")
    print(f"Endpoint Resource Name: {endpoint.resource_name}")

if __name__ == "__main__":
    launch_job()