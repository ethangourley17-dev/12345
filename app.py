import streamlit as st
from google.cloud import aiplatform
import os

# --- Configuration ---
st.set_page_config(page_title="Roof Damage Classifier", page_icon="🏠", layout="wide")

st.title("🏠 Roof Damage Classifier")
st.markdown("Deploy and manage your roof damage classification model on Vertex AI")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

PROJECT_ID = st.sidebar.text_input("GCP Project ID", value="your-project-id")
REGION = st.sidebar.selectbox("Region", ["us-central1", "us-east1", "us-west1", "europe-west1"])
DISPLAY_NAME = st.sidebar.text_input("Model Display Name", value="roof-damage-classifier")
SCRIPT_PATH = st.sidebar.text_input("Training Script Path", value="roof_model.py")

# Pre-built containers for TensorFlow 2.12
TRAIN_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12:latest'
SERVE_IMAGE_URI = 'us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-12:latest'

# Machine configuration
st.sidebar.header("🖥️ Machine Configuration")
train_machine_type = st.sidebar.selectbox("Training Machine", ["n1-standard-4", "n1-standard-8", "n1-highmem-4"])
deploy_machine_type = st.sidebar.selectbox("Deployment Machine", ["n1-standard-2", "n1-standard-4"])

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Current Settings")
    st.json({
        "Project ID": PROJECT_ID,
        "Region": REGION,
        "Display Name": DISPLAY_NAME,
        "Script Path": SCRIPT_PATH,
        "Training Machine": train_machine_type,
        "Deploy Machine": deploy_machine_type
    })

with col2:
    st.subheader("📁 File Status")
    if os.path.exists(SCRIPT_PATH):
        st.success(f"✅ Training script '{SCRIPT_PATH}' found")
    else:
        st.error(f"❌ Training script '{SCRIPT_PATH}' not found")
        st.info("Create this file with your TensorFlow training code before submitting the job.")

st.divider()

# Training Job Section
st.subheader("🚀 Launch Training Job")

if st.button("Start Training & Deployment", type="primary", use_container_width=True):
    # Validation
    if PROJECT_ID == 'your-project-id':
        st.error("⚠️ Please update the Project ID in the sidebar before running.")
    elif not os.path.exists(SCRIPT_PATH):
        st.error(f"⚠️ Training script '{SCRIPT_PATH}' not found. Please create it first.")
    else:
        try:
            with st.status("Training in progress...", expanded=True) as status:
                st.write(f"Initializing Vertex AI for project {PROJECT_ID}...")
                aiplatform.init(project=PROJECT_ID, location=REGION)
                
                st.write("Submitting Custom Training Job...")
                job = aiplatform.CustomTrainingJob(
                    display_name=DISPLAY_NAME,
                    script_path=SCRIPT_PATH,
                    container_uri=TRAIN_IMAGE_URI,
                    model_serving_container_image_uri=SERVE_IMAGE_URI,
                )
                
                st.write("Starting Model Training (this may take a few minutes)...")
                model = job.run(
                    model_display_name=f"{DISPLAY_NAME}-model",
                    replica_count=1,
                    machine_type=train_machine_type,
                    sync=True
                )
                st.write("✅ Training Complete.")
                
                st.write("Deploying Model to Endpoint...")
                endpoint = model.deploy(
                    machine_type=deploy_machine_type,
                    min_replica_count=1,
                    max_replica_count=1
                )
                
                status.update(label="✅ Deployment Complete!", state="complete")
            
            st.success("🎉 Model Deployed Successfully!")
            st.info(f"**Endpoint Resource Name:** `{endpoint.resource_name}`")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

# Footer
st.divider()
st.caption("Powered by Google Cloud Vertex AI")
