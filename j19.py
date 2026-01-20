from google.cloud import aiplatform
import os
import sys

# --- Configuration ---
# TODO: Replace with your actual Project ID
PROJECT_ID = 'your-project-id' 
REGION = 'us-central1'
DISPLAY_NAME = 'roof-damage-classifier'
SCRIPT_PATH = 'roof_model.py'

# Pre-built containers for TensorFlow 2.12
TRAIN_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12:latest'
SERVE_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest'

def launch_job():
    # 1. Validation Checks
    if PROJECT_ID == 'your-project-id':
        print("⚠️  Error: Please update the PROJECT_ID in the script before running.")
        return

    if not os.path.exists(SCRIPT_PATH):
        print(f"⚠️  Error: The training script '{SCRIPT_PATH}' was not found in the current directory.")
        print("    You must create this file (containing your TensorFlow training code) before submitting the job.")
        return

    try:
        print(f"Initializing Vertex AI for project {PROJECT_ID}...")
        aiplatform.init(project=PROJECT_ID, location=REGION)

        # 2. Define the Custom Job
        print("Submitting Custom Training Job...")
        job = aiplatform.CustomTrainingJob(
            display_name=DISPLAY_NAME,
            script_path=SCRIPT_PATH,
            container_uri=TRAIN_IMAGE_URI,
            model_serving_container_image_uri=SERVE_IMAGE_URI,
        )

        # 3. Run the Job
        print("Starting Model Training (this may take a few minutes)...")
        # specific args can be passed to your script using args=["--epochs=5"]
        model = job.run(
            model_display_name=f"{DISPLAY_NAME}-model",
            replica_count=1,
            machine_type='n1-standard-4',
            sync=True 
        )
        print("✅ Training Complete.")

        # 4. Deploy the Model
        print("Deploying Model to Endpoint...")
        endpoint = model.deploy(
            machine_type='n1-standard-2',
            min_replica_count=1,
            max_replica_count=1
        )

        print(f"✅ Model Deployed!")
        print(f"Endpoint Resource Name: {endpoint.resource_name}")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    launch_job()
